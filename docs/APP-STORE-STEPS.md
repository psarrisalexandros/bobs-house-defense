# Bob's House Defense: from this repository to the App Store

The iPhone app is in `app/`. It is the same game as the web version, wrapped with Capacitor, with the four placeholders replaced by real services:

| In the game | In the app |
|---|---|
| Ads | Google AdMob: rewarded and full-screen ads, Google's certified consent form, Apple's tracking question |
| Purchases | Apple's in-app purchase system (StoreKit), read back from the store at every start |
| Save copy | The player's iCloud (key-value store): it comes back after a reinstall |
| Rating | Apple's own rating sheet |

The steps below need your Apple and Google accounts, so only you can do them. Do them in order.

## 1. Register the app with Apple
1. https://developer.apple.com/account > Certificates, Identifiers & Profiles > Identifiers > add an **App ID** with bundle ID `com.bobshousedefense.game`. Tick the **iCloud** capability (key-value storage needs it). In-App Purchase is on by default.
2. https://appstoreconnect.apple.com > Apps > **New App**: platform iOS, name "Bob's House Defense", language English, the bundle ID above, any SKU (for example `bobshouse1`).

The bundle ID can never be changed after the first upload. If you want a different one, say so before step 4.

## 2. Agreements, tax and banking
App Store Connect > **Business**: accept the **Paid Apps Agreement** and fill in bank and tax details. Without it, in-app purchases do not work at all, not even in testing. For the EU you must also declare your **trader status** (Digital Services Act); without it the app is not shown in EU stores.

## 3. Create the in-app purchases
App Store Connect > your app > Monetization > **In-App Purchases**. Create these eight. The product IDs must match exactly.

| Product ID | Type | Reference name | Price to choose |
|---|---|---|---|
| `speed_x2` | Non-Consumable | x2 speed, forever | about 1 € |
| `speed_x3` | Non-Consumable | x3 speed | about 3 € |
| `auto_skills` | Non-Consumable | Auto-skills | about 1 € |
| `no_ads` | Non-Consumable | No ads, all rewards free | about 5 € |
| `sandbox` | Non-Consumable | Sandbox mode | about 5 € |
| `everything` | Non-Consumable | Everything | about 10 € |
| `crate_small` | Consumable | Supply crate | about 1 € |
| `crate_big` | Consumable | Big supply crate | about 3 € |

Each needs a display name, a description and one screenshot for review. The game shows whatever price you set here, in the player's currency.

## 4. Let GitHub build and upload the app
No Mac is needed for this route.
1. App Store Connect > Users and Access > Integrations > **App Store Connect API** > generate a **Team key** with the **Admin** role. Download the `.p8` file (it can be downloaded once) and note the **Key ID** and the **Issuer ID**.
2. Your **Team ID** is at https://developer.apple.com/account under Membership details.
3. GitHub > the repository > Settings > Secrets and variables > Actions > add four secrets:
   - `APPLE_TEAM_ID`: the Team ID
   - `ASC_KEY_ID`: the Key ID
   - `ASC_ISSUER_ID`: the Issuer ID
   - `ASC_KEY_P8`: the whole text of the `.p8` file
4. GitHub > Actions > **iOS to TestFlight** > Run workflow. After about 15 minutes the build appears in App Store Connect > TestFlight.
5. Install the **TestFlight** app on your iPhone and play the build.

These secrets give full control of your developer account. Enter them yourself in GitHub; do not paste them into a chat.

With a Mac instead: install Xcode, then in `app/` run `npm install`, `npm run sync`, `npm run open`, choose your team under Signing & Capabilities, and use Product > Archive.

## 5. Real ads
The app ships with Google's public **test** ad IDs: ads say "Test Ad" and earn nothing.
1. https://admob.google.com > create an account > add an iOS app > create one **Interstitial** and one **Rewarded** ad unit.
2. Privacy & messaging > create and publish a **European regulations** message (the consent form) and an **IDFA explainer** if you want one.
3. Put the three IDs in: `app/ios/App/App/Info.plist` (`GADApplicationIdentifier`, the app ID with `~`) and `app/native/config.js` (the two ad unit IDs with `/`), and set `testing: false`.
4. Add Google's current list of `SKAdNetworkItems` to `Info.plist` (only Google's own is there now).
5. After the app is live, add `app-ads.txt` to your developer website, as AdMob asks.

Never tap your own live ads. Keep `testing: true` on builds you play yourself.

## 6. Test on the phone before review
- A purchase with a **Sandbox tester** (App Store Connect > Users and Access > Sandbox): buy, cancel, restore, and reinstall
- Delete the game and install it again: the wave and the purchases come back
- A rewarded ad to the end, and one closed early
- The notch or island does not cover any button; the home indicator does not get in the way
- Sound, and vibration (it now uses the iPhone's haptics)
- An old iPhone if you can: speed has only been measured in a desktop browser

## 7. Store page and review
Texts are in `docs/STORE-LISTING.md`. Still needed:
- Screenshots in landscape from a real iPhone, in the sizes App Store Connect asks for
- **App Privacy** answers: the ad network collects device identifiers and usage data for advertising; the game itself collects nothing
- The age rating questionnaire (answers in `docs/RELEASE-CHECKLIST.md`, section 5)
- `privacy.html` and `terms.html` filled in with your name, contact email and "Google AdMob" as the ad provider, and a support URL
- Attach the in-app purchases to the first version when you submit it

## What has and has not been tested
- Tested here with a simulated store, ad network and iCloud: purchase confirmed, cancelled and failed; rewarded ad watched, closed early and unavailable; consent order; save and purchases coming back after the device storage is wiped; restore; the web version unchanged
- Not tested: anything on a real iPhone, a real purchase, a real ad, real iCloud, and the signed upload to App Store Connect. Expect to fix small things after the first TestFlight build
- The app icon is drawn at 1024 pixels with the game's own drawing code (`app/tools/make-icon.py`)
- iPhone only for now; it runs on iPad in iPhone mode
- Refunded purchases are not taken away again on the device
