# Bob's House Defense: what is left before the stores

The web app is a complete game with test placeholders where the stores' own systems go. This list is what turns it into a store release. Points marked "check" are from my general knowledge and should be confirmed against the current Apple and Google rules.

## 1. Fill in the documents
- [ ] `privacy.html` and `terms.html`: developer name, city, contact email, date, the ad provider, the minimum age
- [ ] Have both read by a lawyer
- [ ] `docs/STORE-LISTING.md`: support URL and contact

## 2. Wrap the game as a native app
The game is one HTML file. A wrapper such as Capacitor turns it into an iPhone and an Android app without rewriting it.
- [ ] Apple Developer account (yearly fee) and Google Play developer account (one-time fee): check current prices
- [ ] Build the wrapper, lock orientation to landscape, add the icons
- [ ] Test on real phones, old and new. Performance on real devices has not been measured yet

## 3. Connect the three placeholders
The game calls three things that are placeholders in the web build. Each is one function.

| In the game | Now | Store version |
|---|---|---|
| `showAd(why, done)` | a 3-second placeholder | the ad network's rewarded and full-screen ads; call `done` only when the reward is earned |
| `buy(price, name, grant, back)` | a free test unlock | the store purchase for the matching product ID; call `grant` only after the store confirms |
| `window.BobCloud = {put(key, text), get(key, callback)}` | absent | iCloud key-value storage on iPhone, the Google account backup on Android |

- [ ] Purchases must be read back from the store at start-up, not from the device's own storage. In the web build anyone can unlock everything by editing browser storage; store receipts close that hole
- [ ] "Restore purchases" in Settings must call the store (Apple requires a restore button: check)
- [ ] With `BobCloud` in place, a reinstalled game finds its wave again. This path was tested with a simulated cloud copy only

## 4. Ads and consent
- [ ] Choose the ad network and create the placements listed in the store listing document
- [ ] EU players must be asked for consent before personalised ads. The game already asks before the first ad and stores the answer; pass that answer to the ad network, or replace the sheet with the network's own certified consent form (check which is required)
- [ ] iPhone: Apple's tracking permission prompt is required before using the advertising ID (check)
- [ ] Declare the data the ad network collects in App Store "App Privacy" and Google Play "Data safety"

## 5. Age rating
Both stores ask a questionnaire and compute the rating. Answer it as the game is:
- Cartoon violence: yes, frequent. Zombies are shot, burn, and lose arms and legs. No blood beyond small red marks, no gore, no human victims
- Horror or fear themes: mild (zombies, comic tone)
- Gambling, alcohol, drugs, sexual content, bad language: none
- Ads and in-app purchases: yes
- Unrestricted web access, user-generated content, chat: none

Expect a rating around 9+ to 12+ rather than 4+. The questionnaire decides, not this note.

## 6. Names and likenesses
- [ ] Gun names are generic. No real brands appear in the game
- [ ] The red cross on the zombie helicopter was removed
- [ ] Search both stores for "Bob's House Defense" and close variants before committing to the name

## 7. Known weaknesses, not blockers
- Difficulty is uneven: in simulated campaigns defeats cluster around waves 8 to 10, 17 to 20, 30 and 63 to 78
- The game is in English only
- Sound is synthesised in the browser and has not been listened to on a phone
- Vibration does not work in Safari on iPhone; in a native wrapper use the wrapper's haptics
