/* Bob's House Defense: the values that differ between a test build and the real release.
   Everything marked TEST must be replaced before the app is submitted for review. */
window.BOB_CONFIG = {
  ads: {
    /* TEST: Google's public demo ad units. They always show a "Test Ad" and never earn money.
       Replace with the ad unit IDs from your own AdMob account (see docs/APP-STORE-STEPS.md, step 5).
       The AdMob *app* ID lives in app/ios/App/App/Info.plist under GADApplicationIdentifier. */
    ios: {
      interstitial: 'ca-app-pub-3940256099942544/4411468910',
      rewarded: 'ca-app-pub-3940256099942544/1712485313'
    },
    /* while true, the ad network is told these are test requests, so tapping an ad can never count against the account */
    testing: true
  },
  /* game key -> product ID in App Store Connect. The IDs must match exactly. */
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
