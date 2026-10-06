/* Bob's House Defense: the values that differ between a test build and the real release.
   Everything marked TEST must be replaced before the app is submitted for review. */
window.BOB_CONFIG = {
  ads: {
    /* TEST: Google's public demo ad units. They always show a "Test Ad" and never earn money.
       Replace with the ad unit IDs from your own AdMob account (see docs/APP-STORE-STEPS.md, step 5).
       iPhone and Android need separate ad units.
       The AdMob *app* ID lives in app/ios/App/App/Info.plist under GADApplicationIdentifier. */
    ios: {
      interstitial: 'ca-app-pub-3940256099942544/4411468910',
      rewarded: 'ca-app-pub-3940256099942544/1712485313'
    },
    /* TEST: Google's demo units for Android. The AdMob app ID for Android lives in
       app/android/app/src/main/res/values/strings.xml under admob_app_id (docs/PLAY-STORE-STEPS.md, step 6). */
    android: {
      interstitial: 'ca-app-pub-3940256099942544/1033173712',
      rewarded: 'ca-app-pub-3940256099942544/5224354917'
    },
    /* while true, the ad network is told these are test requests, so tapping an ad can never count against the account */
    testing: true
  },
  /* SHA-256 fingerprint of the Google Play review code (see native.js, review access). Android only. */
  review: { android: '4009b28c9f2f52f72b5bf1444a30dac3304f4b1b4acc759d6fae30eee548055d' },
  /* game key -> product ID in App Store Connect and in the Play Console. The same IDs are used in both, and they must match exactly. */
  products: {
    x2: { id: 'speed_x2', consumable: false },
    x3: { id: 'speed_x3', consumable: false },
    auto: { id: 'auto_skills', consumable: false },
    noads: { id: 'no_ads', consumable: false },
    sandbox: { id: 'sandbox', consumable: false },
    all: { id: 'everything', consumable: false },
    crate1: { id: 'crate_small', consumable: true },
    crate2: { id: 'crate_big', consumable: true }
  }
};
