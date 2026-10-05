# Bob's House Defense: από το repository στο Google Play

Η εφαρμογή Android βρίσκεται στο `app/android/`. Είναι το ίδιο παιχνίδι με το web και το iPhone, με το ίδιο native layer (`app/native/`), και στη θέση των τεσσάρων placeholders έχει πραγματικές υπηρεσίες:

| Στο παιχνίδι | Στο Android |
|---|---|
| Διαφημίσεις | Google AdMob: rewarded και full-screen, με τη φόρμα συγκατάθεσης της Google (UMP) πριν από την πρώτη διαφήμιση |
| Αγορές | Google Play Billing (Billing Library 9), με επιβεβαίωση από το κατάστημα πριν δοθεί οτιδήποτε |
| Αντίγραφο προόδου | Android Auto Backup στον λογαριασμό Google του παίκτη |
| Βαθμολογία | Το in-app review του Google Play |
| Δόνηση | Τα haptics του κινητού |

Επιπλέον: μόνο οριζόντια, full screen, και η οθόνη μένει ανοιχτή όσο τρέχει το παιχνίδι (αλλιώς το κινητό θα έσβηνε μέσα στο κύμα, αφού ο παίκτης δεν αγγίζει την οθόνη).

Ταυτότητα εφαρμογής (package name): `com.psarrisalexandros.bobshousedefense`. **Δεν αλλάζει ποτέ μετά το πρώτο ανέβασμα.** Αν θέλεις άλλο, πες το πριν από το βήμα 5.

Τα βήματα παρακάτω χρειάζονται τον δικό σου λογαριασμό Google, άρα μόνο εσύ μπορείς να τα κάνεις. Με τη σειρά.

## 1. Λογαριασμός προγραμματιστή Google Play
1. https://play.google.com/console/signup: εφάπαξ τέλος **25 USD**. Η Google μπορεί να ζητήσει ταυτότητα και κάρτα στο νόμιμο όνομά σου.
2. Επαλήθευση συσκευής: πρέπει να δείξεις ότι έχεις πρόσβαση σε συσκευή Android, μέσω της εφαρμογής **Play Console** για κινητά. Χρειάζεσαι λοιπόν ένα Android κινητό (ή δανεικό).
3. **Προσωπικός λογαριασμός που φτιάχτηκε μετά τις 13/11/2023:** πριν ζητήσεις δημοσίευση στην παραγωγή πρέπει να τρέξεις **closed test με τουλάχιστον 12 testers, εγγεγραμμένους συνεχόμενα για 14 ημέρες**. Μετά κάνεις αίτηση για production access (η Google απαντά συνήθως μέσα σε 7 ημέρες). Αυτό είναι το μεγαλύτερο χρονικό εμπόδιο: υπολόγισε τουλάχιστον 3 εβδομάδες από το πρώτο ανέβασμα. Ξεκίνα να μαζεύεις 12 άτομα με Android και λογαριασμό Google από τώρα.

## 2. Προφίλ πληρωμών
Play Console > Setup > **Payments profile**. Χωρίς αυτό δεν δημιουργούνται in-app προϊόντα. Προσοχή: λογαριασμοί που πουλάνε (in-app αγορές) **εμφανίζουν δημόσια την πλήρη διεύθυνσή τους** στο Google Play, από το προφίλ πληρωμών. Αν δεν θέλεις τη διεύθυνση του σπιτιού σου δημόσια, βάλε επαγγελματική διεύθυνση.

## 3. Δημιουργία της εφαρμογής
Play Console > **Create app**: όνομα "Bob's House Defense", γλώσσα English, **Game**, **Free**.

## 4. Το κλειδί υπογραφής (upload key)
Το κλειδί έχει ήδη δημιουργηθεί στον υπολογιστή σου, στον φάκελο `Bobs House Defense/android-upload-key/` (δεν είναι στο GitHub και δεν πρέπει να μπει ποτέ). Κράτα δεύτερο αντίγραφο του φακέλου σε ασφαλές μέρος.

GitHub > το repository > Settings > Secrets and variables > Actions > **New repository secret**, τέσσερις φορές:

| Όνομα secret | Τιμή |
|---|---|
| `ANDROID_KEYSTORE_BASE64` | όλο το περιεχόμενο του `keystore-base64.txt` |
| `ANDROID_KEYSTORE_PASSWORD` | το περιεχόμενο του `keystore-password.txt` |
| `ANDROID_KEY_PASSWORD` | το ίδιο με το προηγούμενο |
| `ANDROID_KEY_ALIAS` | `upload` |

Βάλ' τα ο ίδιος στο GitHub· μην τα επικολλήσεις σε συνομιλία.

Το Google Play χρησιμοποιεί **Play App Signing**: το τελικό κλειδί της εφαρμογής το κρατά η Google, εσύ υπογράφεις μόνο με το upload key. Αν το χάσεις, ζητάς reset από το Play Console και δεν χάνεις την εφαρμογή.

## 5. Build και πρώτο ανέβασμα
1. GitHub > Actions > **Android release bundle** > Run workflow (branch `android-app`). Σε λίγα λεπτά, στο κάτω μέρος της σελίδας του run, στα **Artifacts**, υπάρχει το `.aab`. Κατέβασέ το και αποσυμπίεσε το zip.
2. Play Console > Test and release > Testing > **Internal testing** > Create new release > ανέβασε το `app-release.aab`. Στην πρώτη φορά αποδέξου το Play App Signing.
3. Πρόσθεσε τον εαυτό σου ως tester, άνοιξε το link συμμετοχής στο Android κινητό και εγκατάστησε από το Play.

Κάθε νέο run παίρνει αυτόματα μεγαλύτερο version code, όπως απαιτεί το Play.

Για γρήγορη δοκιμή χωρίς Play: το workflow **Android build check** αφήνει στα Artifacts ένα debug APK που εγκαθίσταται απευθείας σε Android κινητό. Σε αυτό οι αγορές δεν λειτουργούν (το Play Billing δουλεύει μόνο σε build που έχει εγκατασταθεί από το Play).

## 6. Πραγματικές διαφημίσεις
Το build έχει τα δημόσια **δοκιμαστικά** ad IDs της Google: δείχνουν "Test Ad" και δεν αποφέρουν τίποτα.
1. https://admob.google.com > Apps > Add app > **Android** (ξεχωριστή εγγραφή από το iPhone) > μία **Interstitial** και μία **Rewarded** ad unit.
2. Privacy & messaging > δημοσίευσε μήνυμα **European regulations** (τη φόρμα συγκατάθεσης) και για την εφαρμογή Android.
3. Βάλε τα τρία IDs: το App ID (με `~`) στο `app/android/app/src/main/res/values/strings.xml` (`admob_app_id`), και τα δύο ad unit IDs (με `/`) στο `app/native/config.js`, στο `android`. Για την τελική έκδοση βάλε `testing: false`.
4. Όταν η εφαρμογή βγει στο κατάστημα, σύνδεσέ τη στο AdMob και πρόσθεσε `app-ads.txt` στον ιστότοπο προγραμματιστή.

Ποτέ μην πατάς τις δικές σου πραγματικές διαφημίσεις. Στα builds που παίζεις ο ίδιος κράτα `testing: true`.

## 7. In-app προϊόντα
Play Console > Monetize with Play > Products > **One-time products**. Εμφανίζεται αφού ανέβει το πρώτο build (βήμα 5). Δημιούργησε αυτά τα οκτώ, με **ακριβώς** αυτά τα Product IDs (είναι τα ίδια με του App Store) και κατάσταση **Active**:

| Product ID | Όνομα | Τιμή |
|---|---|---|
| `speed_x2` | x2 speed, forever | περίπου 1 € |
| `speed_x3` | x3 speed | περίπου 3 € |
| `auto_skills` | Auto-skills | περίπου 1 € |
| `no_ads` | No ads, all rewards free | περίπου 5 € |
| `sandbox` | Sandbox mode | περίπου 5 € |
| `everything` | Everything | περίπου 10 € |
| `crate_small` | Supply crate | περίπου 1 € |
| `crate_big` | Big supply crate | περίπου 3 € |

Τα δύο crates αγοράζονται πολλές φορές· αυτό το χειρίζεται η εφαρμογή (τα "καταναλώνει" μετά την αγορά). Το παιχνίδι δείχνει την τιμή που ορίζεις εδώ, στο νόμισμα του παίκτη.

Για δοκιμαστικές αγορές χωρίς χρέωση: Play Console > Settings > **License testing** > πρόσθεσε το Gmail σου.

## 8. Δήλωση περιεχομένου (App content)
Play Console > Policy and programs > **App content**. Απάντησε όπως είναι το παιχνίδι:
- **Privacy policy:** δημόσιο URL. Το `privacy.html` είναι στο repository, αλλά έχει ακόμη κενά σε [αγκύλες] (όνομα, email, ημερομηνία, ηλικία). Πρέπει να συμπληρωθούν πριν δοθεί το URL.
- **Ads:** Ναι, περιέχει διαφημίσεις.
- **App access:** όλη η εφαρμογή είναι προσβάσιμη χωρίς σύνδεση.
- **Content rating:** το ερωτηματολόγιο IARC. Απαντήσεις στο `docs/RELEASE-CHECKLIST.md`, ενότητα 5 (καρτουνίστικη βία, καμία άλλη ευαίσθητη κατηγορία, έχει διαφημίσεις και αγορές).
- **Target audience:** 13 ετών και άνω. Αν δηλώσεις παιδιά κάτω των 13, ισχύει η πολιτική Families με πολύ αυστηρότερους κανόνες για διαφημίσεις.
- **Data safety:** το παιχνίδι δεν συλλέγει τίποτα το ίδιο. Το Google Mobile Ads SDK συλλέγει και μοιράζεται δεδομένα (αναγνωριστικά συσκευής, IP από την οποία προκύπτει κατά προσέγγιση τοποθεσία, αλληλεπιδράσεις με διαφημίσεις, διαγνωστικά), κρυπτογραφημένα κατά τη μεταφορά. Συμπλήρωσε τη φόρμα με βάση τον επίσημο πίνακα της Google: https://developers.google.com/admob/android/privacy/play-data-disclosure (δεν μπόρεσα να ανοίξω τη σελίδα από εδώ για να επιβεβαιώσω την τρέχουσα λίστα· ακολούθησε τον πίνακα, όχι τη δική μου περίληψη).
- **Advertising ID:** Ναι, χρησιμοποιείται, για διαφημίσεις. Το build δηλώνει ήδη το δικαίωμα `AD_ID`.

## 9. Σελίδα καταστήματος
Τα κείμενα είναι στο `docs/STORE-LISTING.md` (σύντομη περιγραφή έως 80 χαρακτήρες, πλήρης περιγραφή). Τα γραφικά είναι έτοιμα στο `docs/play-store-assets/`:

| Αρχείο | Απαίτηση Google |
|---|---|
| `icon-512.png` | εικονίδιο 512 x 512, PNG 32-bit, έως 1024 KB |
| `feature-graphic-1024x500.png` | feature graphic 1024 x 500, PNG 24-bit χωρίς διαφάνεια |
| `screenshot-1` έως `-4` (1920 x 1080) | τουλάχιστον 2 screenshots· 4 σε 1920 x 1080 για να προτείνεται η εφαρμογή |

Τα screenshots είναι πραγματικές εικόνες του παιχνιδιού, αλλά οι τρεις τελευταίες σκηνές έχουν στηθεί (αναβαθμίσεις τοποθετημένες απευθείας, όχι παιγμένες). Καλό είναι να αντικατασταθούν με λήψεις από πραγματικό κινητό.

Κατηγορία: Games > Strategy. Χρειάζεται email επικοινωνίας (εμφανίζεται δημόσια).

## 10. Closed test και παραγωγή
1. Testing > **Closed testing** > δημιούργησε track, ανέβασε το ίδιο `.aab`, πρόσθεσε τους 12 testers (λίστα email ή Google Group) και στείλε τους το link. Πρέπει να κάνουν opt-in και να μείνουν 14 συνεχόμενες ημέρες.
2. Dashboard > **Apply for production access**: ερωτήσεις για το closed test, την εφαρμογή και την ετοιμότητα.
3. Πριν από την παραγωγή: πραγματικά ad IDs με `testing: false` (βήμα 6), νέο run του **Android release bundle**, ανέβασμα στο Production.

## Τι να δοκιμάσεις στο κινητό
- Αγορά με license tester: αγορά, ακύρωση, "Restore purchases", απεγκατάσταση και επανεγκατάσταση
- Rewarded διαφήμιση μέχρι το τέλος, και μία που την κλείνεις νωρίς
- Η φόρμα συγκατάθεσης εμφανίζεται πριν από την πρώτη διαφήμιση· Settings > Ads > Change την ξανανοίγει
- Η εγκοπή της κάμερας δεν καλύπτει κουμπιά· οι μπάρες συστήματος μένουν κρυμμένες και μετά από διαφήμιση
- Ήχος και δόνηση
- Ένα παλιό ή φτηνό Android: η ταχύτητα έχει μετρηθεί μόνο σε browser υπολογιστή. Τα φτηνά Android είναι το πιο πιθανό σημείο προβλήματος

## Τι ισχύει για το αντίγραφο προόδου
Στο Android το αντίγραφο προόδου ανεβαίνει με το Auto Backup της Google, όχι αμέσως όπως στο iCloud:
- γίνεται μόνο αν ο παίκτης έχει ενεργό το backup της συσκευής
- περίπου μία φορά το 24ωρο, με το κινητό σε αδράνεια και σε Wi-Fi
- επαναφέρεται όταν η εφαρμογή εγκατασταθεί ξανά ή σε νέο κινητό

Άρα όποιος σβήσει το παιχνίδι λίγες ώρες μετά την εγκατάσταση μπορεί να βρει παλαιότερη πρόοδο ή καθόλου. Οι **αγορές** δεν επηρεάζονται: διαβάζονται από το Play σε κάθε εκκίνηση. Ο κωδικός backup στα Settings δουλεύει πάντα. Αν χρειαστεί άμεσος συγχρονισμός, η λύση είναι τα Saved Games των Play Games Services (απαιτεί σύνδεση του παίκτη και επιπλέον ρύθμιση).

## Τι ελέγχθηκε και τι όχι
- **Compile:** το GitHub έχτισε το debug APK (target SDK 36, όπως απαιτεί το Play για νέες εφαρμογές από 31/8/2026).
- **Προσομοίωση:** με ψεύτικο κατάστημα, δίκτυο διαφημίσεων και backup: αγορά επιβεβαιωμένη, ακυρωμένη και αποτυχημένη· rewarded ολόκληρη και κλεισμένη νωρίς· full-screen· σειρά συγκατάθεσης· η ερώτηση tracking της Apple δεν γίνεται στο Android· το iPhone layer συμπεριφέρεται όπως πριν.
- **Δεν ελέγχθηκε:** οτιδήποτε σε πραγματικό Android κινητό, πραγματική αγορά, πραγματική διαφήμιση, πραγματική επαναφορά backup, και το υπογεγραμμένο `.aab` (το release workflow δεν έχει τρέξει, γιατί χρειάζεται τα secrets του βήματος 4). Περίμενε μικροδιορθώσεις μετά το πρώτο build στο κινητό.
- Οι επιστροφές χρημάτων (refunds) δεν αφαιρούν την αγορά από τη συσκευή.

## Πηγές (Google, ελέγχθηκαν 5/10/2026)
- Target API level: https://support.google.com/googleplay/android-developer/answer/11926878
- Testers για νέους προσωπικούς λογαριασμούς: https://support.google.com/googleplay/android-developer/answer/14151465
- Εγγραφή και επαλήθευση λογαριασμού: https://support.google.com/googleplay/android-developer/answer/6112435
- Γραφικά σελίδας καταστήματος: https://support.google.com/googleplay/android-developer/answer/9866151
- Εκδόσεις Play Billing Library: https://developer.android.com/google/play/billing/deprecation-faq
- Play App Signing: https://support.google.com/googleplay/android-developer/answer/9842756
- Auto Backup: https://developer.android.com/identity/data/autobackup
- 16 KB page size: https://developer.android.com/guide/practices/page-sizes
- Advertising ID: https://support.google.com/googleplay/android-developer/answer/6048248
- Στοιχεία επικοινωνίας και δημόσια διεύθυνση: https://support.google.com/googleplay/android-developer/answer/13634081
