/* Bob's House Defense: the native layer of the store build.
   Loaded before the game, and only inside the app. It gives the game four things the web build fakes:
     window.BobAds    real rewarded and full-screen ads, with the ad network's own consent form
     window.BobStore  real purchases through the store, read back from the store at start-up
     window.BobCloud  a copy of the save in the player's iCloud, which survives a reinstall
     window.BobRate   the store's own rating sheet
   plus window.BobBuzz for haptics. In a browser none of this runs and the game uses its placeholders. */
(function () {
  'use strict';
  var Cap = window.Capacitor;
  if (!Cap || !Cap.isNativePlatform || !Cap.isNativePlatform()) return;
  var CFG = window.BOB_CONFIG || {}, PLATFORM = Cap.getPlatform();
  /* a plugin that is not built into this app comes back as null, and its feature stays off */
  var plug = function (name) { try { return Cap.isPluginAvailable(name) ? Cap.registerPlugin(name) : null; } catch (e) { return null; } };
  function once(f) { var d = false; return function () { if (d) return; d = true; return f && f.apply(null, arguments); }; }
  function after(ms, p) { return Promise.race([p, new Promise(function (_, no) { setTimeout(function () { no(new Error('timeout')); }, ms); })]); }

  /* ---------------- ads ---------------- */
  var AdMob = plug('AdMob'), UNITS = (CFG.ads || {})[PLATFORM] || {}, TESTING = !!(CFG.ads || {}).testing;
  if (AdMob && UNITS.rewarded) {
    var readyP = null, loaded = { inter: null, reward: null };
    /* consent first (the certified form, shown only where the law asks for it), then Apple's tracking question, then the ad network starts */
    var consentFlow = function () {
      return AdMob.requestConsentInfo().then(function (info) {
        if (info && info.isConsentFormAvailable && info.status === 'REQUIRED') return AdMob.showConsentForm();
      }).catch(function () {}).then(function () {
        return AdMob.trackingAuthorizationStatus().then(function (r) {
          if (r && r.status === 'notDetermined') return AdMob.requestTrackingAuthorization();
        });
      }).catch(function () {});
    };
    var ready = function () {
      if (!readyP) readyP = consentFlow().then(function () { return AdMob.initialize({ initializeForTesting: TESTING }); })
        .catch(function (e) { readyP = null; throw e; });
      return readyP;
    };
    var load = function (kind) {
      if (!loaded[kind]) {
        var p = kind === 'inter' ? AdMob.prepareInterstitial({ adId: UNITS.interstitial, isTesting: TESTING })
                                 : AdMob.prepareRewardVideoAd({ adId: UNITS.rewarded, isTesting: TESTING });
        loaded[kind] = p.catch(function (e) { loaded[kind] = null; throw e; });
      }
      return loaded[kind];
    };
    var preload = function () { load('inter').catch(function () {}); load('reward').catch(function () {}); };
    /* one listener set for the whole session; the ad on screen is described by `cur` */
    var cur = null;
    var finish = function () {
      var c = cur; if (!c) return; cur = null; loaded[c.kind] = null;
      c.end();
      if (c.kind === 'inter' || c.earned) c.reward();
      else if (c.failed) c.say('No ad is available right now. Check your connection and try again.');
      preload();
    };
    AdMob.addListener('onRewardedVideoAdReward', function () { if (cur) cur.earned = true; });
    AdMob.addListener('onRewardedVideoAdDismissed', finish);
    AdMob.addListener('onRewardedVideoAdFailedToShow', function () { if (cur) cur.failed = true; finish(); });
    AdMob.addListener('interstitialAdDismissed', finish);
    AdMob.addListener('interstitialAdFailedToShow', finish);

    window.BobAds = {
      /* reward: call only when the ad was watched to the end (or, for a break between waves, when it is over)
         end: always called once, when the game may move again */
      show: function (why, reward, end, say) {
        if (cur) return;
        var kind = /^Reward/.test(why) ? 'reward' : 'inter';
        cur = { kind: kind, reward: once(reward), end: once(end), say: say || function () {}, earned: false, failed: false };
        if (kind === 'reward') cur.say('Loading the ad…');
        after(12000, ready().then(function () { return load(kind); })).then(function () {
          if (!cur) return;
          return kind === 'inter' ? AdMob.showInterstitial() : AdMob.showRewardVideoAd();
        }).catch(function () { if (cur) { cur.failed = true; finish(); } });
      },
      /* Settings > Ads > Change: reopen the privacy choices. Outside the regions that need the form this is a short note */
      consent: function (then) {
        ready().catch(function () {}).then(function () { return AdMob.showPrivacyOptionsForm(); }).catch(function () {}).then(function () { if (then) then(); });
      }
    };
  }

  /* ---------------- purchases ---------------- */
  var PROD = CFG.products || {}, KEYS = Object.keys(PROD), store = null, storeReady = false, pending = {};
  var keyOf = function (id) { for (var i = 0; i < KEYS.length; i++) if (PROD[KEYS[i]].id === id) return KEYS[i]; return null; };
  var reportOwned = function () {
    if (!store || !window.BobGame) return;
    var got = KEYS.filter(function (k) { return !PROD[k].consumable && store.owned(PROD[k].id); });
    if (got.length) window.BobGame.owned(got);
  };
  var startStore = function () {
    var C = window.CdvPurchase; if (!C || store) return;
    store = C.store;
    var platform = PLATFORM === 'ios' ? C.Platform.APPLE_APPSTORE : C.Platform.GOOGLE_PLAY;
    store.register(KEYS.map(function (k) {
      return { id: PROD[k].id, platform: platform, type: PROD[k].consumable ? C.ProductType.CONSUMABLE : C.ProductType.NON_CONSUMABLE };
    }));
    store.when()
      .approved(function (t) { t.verify(); })
      .verified(function (r) { r.finish(); })
      .finished(function (t) {
        /* a finished transaction is the store's confirmation: only now does the game hand anything over */
        (t.products || []).forEach(function (p) { var k = keyOf(p.id), cb = k && pending[k]; if (cb) { delete pending[k]; cb(true); } });
        reportOwned();
      })
      .receiptUpdated(reportOwned);
    store.initialize([platform]).then(function () { storeReady = true; reportOwned(); }, function () {});
  };
  window.BobStore = {
    start: function () { if (window.CdvPurchase) startStore(); else document.addEventListener('deviceready', startStore, false); },
    /* the store's own price in the player's currency; the round euro figure until the store has answered */
    price: function (key, fallback) {
      try { var p = store && PROD[key] && store.get(PROD[key].id); return (p && p.pricing && p.pricing.price) || fallback; } catch (e) { return fallback; }
    },
    /* done(true) after the store confirms, done(false) on an error, done(null) when the player cancels */
    buy: function (key, done) {
      done = once(done);
      var C = window.CdvPurchase, p = store && PROD[key] && store.get(PROD[key].id), offer = p && p.getOffer();
      if (!storeReady || !offer) { done(false); return; }
      pending[key] = done;
      store.order(offer).then(function (err) {
        if (!err) return;                               /* no error: the answer arrives through finished() above */
        delete pending[key];
        done(err.code === C.ErrorCode.PAYMENT_CANCELLED ? null : false);
      }, function () { delete pending[key]; done(false); });
    },
    restore: function (tell) {
      if (!store) { tell('The store is not available right now.'); return; }
      store.restorePurchases().then(function (err) {
        reportOwned();
        var n = KEYS.filter(function (k) { return !PROD[k].consumable && store.owned(PROD[k].id); }).length;
        tell(err ? 'The store could not be reached. Try again later.' : n ? 'Purchases restored.' : 'No earlier purchases were found for this account.');
      }, function () { tell('The store could not be reached. Try again later.'); });
    }
  };

  /* ---------------- save copy in the player's account ---------------- */
  var Cloud = plug('BobCloud');
  if (Cloud) {
    window.BobCloud = {
      put: function (key, text) { Cloud.put({ key: key, value: text }).catch(function () {}); },
      get: function (key, cb) { Cloud.get({ key: key }).then(function (r) { if (r && r.value) cb(r.value); }, function () {}); }
    };
  }

  /* ---------------- rating and haptics ---------------- */
  var Review = plug('InAppReview'), Haptics = plug('Haptics');
  if (Review) window.BobRate = function () { Review.requestReview().catch(function () {}); };
  if (Haptics) window.BobBuzz = function (ms) { Haptics.impact({ style: ms >= 40 ? 'HEAVY' : ms >= 15 ? 'MEDIUM' : 'LIGHT' }).catch(function () {}); };
})();
