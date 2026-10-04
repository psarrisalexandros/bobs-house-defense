# Bob's House Defense

An idle house-defence game. Bob shoots on his own; you buy the upgrades.

The whole game is `index.html`: code, drawings, sounds and fonts are inside it, and it loads nothing from anywhere else. `manifest.webmanifest`, `sw.js` and the icons make it installable on a phone home screen and playable offline.

- `privacy.html`, `terms.html`: drafts of the privacy policy and terms of use
- `docs/STORE-LISTING.md`: store texts, purchases and ad placements
- `docs/RELEASE-CHECKLIST.md`: what is left before the App Store and Google Play
- `LICENSES.md`: font licences
- `app/`: the iPhone app (Capacitor wrapper with real ads, purchases, iCloud save and rating)
- `docs/APP-STORE-STEPS.md`: the steps from here to the App Store

Purchases and ads in this web build are test placeholders: nothing is charged and no ad network is contacted.
