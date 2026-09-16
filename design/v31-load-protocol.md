LOAD PROTOCOL — DEEP POCKET v31 "unified look"
Read this whole file, then read the three context files, THEN report what you found. No code until you have reported.

────────────────────────────────────────────────────────
0. WHAT THE END GOAL ACTUALLY IS
────────────────────────────────────────────────────────
Not a preview. Not a sandbox artifact. The finish line is:

  Joe opens Safari on his iPhone → jpwarner-sys.github.io/deep-pocket
  → Share → Add to Home Screen → taps the icon → it opens FULL SCREEN,
  no Safari chrome, correct icon, correct name, and it plays.

Everything below serves that. A beautiful build that only exists in your
sandbox is a failure. Judge yourself on the live URL, from a phone.

────────────────────────────────────────────────────────
1. WHAT IT IS
────────────────────────────────────────────────────────
Deep Pocket is a rhythm trainer for bass practice. Nine drum voices, 18
grooves, a 32-bar arranger with chord changes, a synth bass voice that
follows the changes, and a lock-screen mode that keeps the loop alive
when the phone sleeps.

NON-ONTOLOGY app. No estate, clinical, client or firm data. No family
tokens. It exists to be fun. Don't drag other machinery into it.

────────────────────────────────────────────────────────
2. WHERE IT STANDS — verify this yourself before trusting it
────────────────────────────────────────────────────────
LIVE      jpwarner-sys.github.io/deep-pocket — face reads "v30 web".
          Single file, 141,033 bytes. No service worker. No external JS.
REPO      github.com/jpwarner-sys/deep-pocket, branch main.
          Flat Pages tree: index.html, manifest.webmanifest, icon-180/192/512.png,
          kits/, README.md. There is NO src/ or site/ split on main — an
          earlier CSS/JS split was local-only and is dead. v31 STAYS SINGLE FILE.
FROZEN    v21 on branch backup/v21-20260915 (164b3c1). Never delete, never force-push.
KITS      Synth (live oscillators) + three sampled: Black Pearl, Red Zeppelin
          (AVL, CC BY-SA 3.0, Glen MacArthur) and TR-808 Fischer (45 FLAC, CC0).
          All on main, all 200 on the live URL. Keep both attributions.

AUDIO STATE — do not change audio in this pass
  MASTER_CAL 0.70. kitGain reads synth.rmsAtFull and synth.velExp out of
  kits/kits.json and clamps to 0.02–8.
  synth.rmsAtFull.hh WAS 0.001371, which computed a gain of 0.0158 — BELOW
  the 0.02 clamp floor. Every velocity therefore rendered identically, about
  55 dB under the kick. That is the "hats light up but don't play" bug.
  It is fixed: hh = 0.01344. No voice pinned, 12.3 dB of velocity range
  restored across all three sampled kits. DO NOT REVERT IT. Do not
  "re-measure" it into a different number without showing the arithmetic.

────────────────────────────────────────────────────────
3. THE JOB
────────────────────────────────────────────────────────
Ship v31: the v30 engine, unchanged, wearing one unified look across six
surfaces — portrait lock / play / edit, landscape lock / play / edit.

DO NOT TOUCH: the engine, the grooves, the arranger, the bass voice, the
kit loader, kitGain, MASTER_CAL, anything under kits/, or the manifest
identity. If changing one of those looks necessary, stop and tell Joe why.

────────────────────────────────────────────────────────
4. WHAT IS LOCKED vs WHAT IS YOURS
────────────────────────────────────────────────────────
LOCKED — use verbatim, these are decided:
  · The material system and every token in v31_THEME_LOCK.css.
  · Two tones of ONE species. Bezel = lighter steamed walnut, slim, the only
    place grain reads at a glance. Deck = black walnut, dark grain, present
    but never competing with a chord you're reading. Wells are NOT wood.
  · Amber #ffa02c is the only accent. There is no second hue.
  · LEDs are ROUND, and UNLIT IS A DARK LAMP, NOT A HOLE. The field of dark
    lamps behind the lit ones is the whole character of the machine.
  · The bass-clef lamp (U+1D122) replaces any BASS ON/OFF text label.
  · NINE voice rows. See §6.
  · The density rule. See §5.
  · The contrast gate. See §7.

YOURS — solve these, you're the builder:
  · All layout, spacing, sizing, type scale, grid proportions, breakpoints.
  · How the six surfaces transition and how state is remembered.
  · Touch targets, gestures, scroll behaviour, what collapses on a small phone.
  · Whether a knob is a drag, a tap-cycle, or both. Whether swing gets a knob
    at all. Composition is craft and craft is your job.
  · Anything the concept file does clumsily. It is a material study, not a
    layout spec. Beat it.

────────────────────────────────────────────────────────
5. THE DENSITY RULE — this is what makes six screens one machine
────────────────────────────────────────────────────────
LOCK and PLAY are HARDWARE-dense. Knobs, bat switches, lamps, physical
affordances. The bass is in his hands; he is not reading, he is glancing.

EDIT is SCREEN-dense. Chrome collapses to a single line. Grid and arranger
take every pixel they can get. Controls that aren't the grid go behind MIX
and MEMORY. Target: grid + arranger ≥ 70% of face height at 430 x 932. If you can't hit
that, cut chrome — never cut steps.

Same parts bin on all six. Different ratio. That's the whole trick.

────────────────────────────────────────────────────────
6. NINE ROWS — this one keeps getting broken, including by the art
────────────────────────────────────────────────────────
  1 Kick | 2 Snare | 3 Hats | 4 Open | 5 Rim | 6 CYM-A | 7 CYM-B | 8 TOM | 9 COLOR

Kits rename the last four. CYM-B is the crash — every kit has one because
CYM-B is a crash sample. There is no tenth row, and there is never a second
Crash row. Concept frames 80 and 81 in the art thread draw ten and eleven
rows and list Crash twice. THE ART IS WRONG THERE. This spec is right.
Count the rows in your built file and report the number.

────────────────────────────────────────────────────────
7. THE CONTRAST GATE — pass/fail, not preference
────────────────────────────────────────────────────────
The reason v30 needs replacing is not that it's ugly. It's that the art
thread diagnosed it precisely: "walnut-on-walnut, splash sitting on top of
a machine that's already dim, every section the same weight," with amber
pads at roughly 30% contrast.

So: every lit amber element sits on a WELL or on the BLACK-WALNUT DECK.
Never on bezel walnut. Lit element vs its immediate background must clear
4.5:1. Measure it, report the number. If a surface can't carry amber at
4.5:1, the surface is too light — don't dim the amber to compensate.

Corollary: the splash cannot be a brown veil over a brown machine. Whatever
you do there, it has to read as a different layer.

────────────────────────────────────────────────────────
8. HOME-SCREEN INSTALL — the part that is easy to get silently wrong
────────────────────────────────────────────────────────
Every Pages project on this account shares the jpwarner-sys.github.io
origin. BLOCKBALL and NOW live there too. Without an absolute, directory-
exact identity, iOS keys the install to the WRONG app's record — that is
the real defect that once made opening /now/ launch BLOCKBALL.

MUST hold on the live URL:
  manifest.webmanifest:  "id", "scope", "start_url" ALL exactly "/deep-pocket/"
                         display "standalone", orientation "any"
  meta apple-mobile-web-app-capable        = yes
  meta apple-mobile-web-app-status-bar-style = black-translucent
  meta apple-mobile-web-app-title          = Deep Pocket
  link rel=apple-touch-icon href=icon-180.png   (iOS IGNORES the manifest icons — this
                                                 link is what the home-screen icon comes from)
  theme-color set
  NO service worker anywhere. NO root-scoped anything.
  localStorage keys namespaced deeppocket.* — never bare keys.

THE TARGET DEVICE — design to this, not to a generic phone
  iPhone 16 Plus, iOS 26.x. This is the home for years. iPad and desktop are
  a bonus and must not drive a single decision.
    portrait  CSS viewport 430 x 932 points  (2796 x 1290 native, 3x)
    landscape CSS viewport 932 x 430 points
  NOT 390 x 844 — that is the base iPhone. Every earlier sizing note in this
  project assumed 390 and is superseded. You have 40 more points of width
  and 88 more of height in portrait, and 430 points of HEIGHT in landscape
  instead of 390. The old "ten rows is tight on a 390-tall landscape" worry
  is gone: nine rows on 430 is comfortable. Spend the room on the grid.
  Design fluid with 430 as the reference, not hard-coded to it. 390 must
  still lay out correctly; it just is not what you tune against.

DYNAMIC ISLAND, NOT A NOTCH — and it moves when you rotate
  Status-bar is black-translucent, so the app draws underneath it. Pad with
  env(safe-area-inset-*) on ALL FOUR sides, plus extra top padding under
  @media (display-mode:standalone).
  Portrait insets run about 59pt top, 34pt bottom.
  LANDSCAPE IS THE ONE THAT GETS FORGOTTEN: rotated, the Island eats a
  horizontal strip, so the inset lands left or right depending on which way
  the phone was turned. That is exactly where the landscape editor puts its
  voice-name column, and it will clip. Handle left AND right.
  Do not trust those numbers — MEASURE them. Render the four computed
  env(safe-area-inset-*) values into the face behind a debug flag, have Joe
  read them off the phone in standalone in both orientations and both
  rotation directions, then size against what actually came back.
  A gorgeous layout with the clock sitting on the brand name is a fail.

iOS TRAPS ALREADY PAID FOR — inherit these, don't rediscover them:
  · On backgrounding iOS parks the AudioContext as 'suspended' OR Safari's
    non-standard 'interrupted'. Accept anything that isn't 'running'.
  · resume() can settle on a context that never ticks again. PROVE
    currentTime advanced before claiming success. Hold the in-flight promise
    so a second caller joins it rather than racing.
  · A live Web Audio graph cannot play in the background; an HTML audio element
    playing real media can. That is how lock-screen mode works.
  · Folding the loop tail can clip. Measure the folded peak, trim above ~0.985.
  · HIDE the splash, never .remove() it, or there's no gesture surface left
    to recover with.
  · matchMedia(orientation) LIES during rotate — after a turn iOS still
    reports height 844, which is why the landscape editor didn't appear in
    v28. Key landscape off the real viewport (width greater than height) and retry on
    orientationchange and visualViewport. v29 fixed this. Keep the fix.
  · Chromium cannot decode AAC. FLAC only, or you can't test headlessly.

────────────────────────────────────────────────────────
9. CONTEXT FILES — read these before you design
────────────────────────────────────────────────────────
LIVE ON PAGES — no login, open them in a browser:

jpwarner-sys.github.io/deep-pocket/design/v31-concept.html
jpwarner-sys.github.io/deep-pocket/design/v31-theme-lock.css

  v31-concept.html     All six surfaces rendered. LOOK at it, don't just read
                       the source. It shows what the material does once it is
                       assembled. The LAYOUT in it is a study, not a spec —
                       you are expected to beat it.
  v31-theme-lock.css   The material, as literal CSS. Locked. Use verbatim.

Those two live in design/ inside the app repo. They are reference only, they
are not wired to the app, and index.html must not link them.

Same two files also sit on Google Drive, 2_NOW/Deep_Pocket, in case your
sandbox cannot reach Pages:
drive.google.com/drive/folders/1VIHB52xLrAxrqBUQlpIBhNGDqiz30OoW
  plus CONTINUITY_2026-09-15.md — where the v27 IA was frozen: player/edit/
  lock, BEAT and COMPOSE landscapes, the nine-row kit-rename map
  plus 01 through 10 *.jpg — earliest concept boards: lock, stand, gig bag.

Grok project "DEEP POCKET", chat "Deep Pocket Bass App Concept Art":
  81 Imagine frames, numbered here in thread order. The ones that matter:
   67  open player. Joe: "like this vibe, but a little more wood showing."
   73, 74  editor pair, squarer slab.
   80  BEAT landscape.   81  COMPOSE landscape.
   77, 78, 79  the three lock candidates.
  Every frame is 116 BPM / Motown / Am7-D7-Gmaj7. They are LOOK studies.
  Take material, lighting and proportion from them. Take IA from this file.
  Where they disagree with §6, they are wrong.

Grok build thread "Deep Pocket Rhythm Trainer Setup":
  The v21→v30 technical history. Volume calibration (v21 too loud at
  MASTER_CAL 1.10, v22 too quiet at 0.50, 0.70 is the answer), the phone-width
  pass (v26, sized for 390 and now superseded by 430), the portrait/landscape split (v27), the rotate fix
  (v29), the TR-808 wire-in. Read it before you re-solve something.

────────────────────────────────────────────────────────
10. HOW TO PUBLISH — this exact path is proven, it ran today
────────────────────────────────────────────────────────
Your sandbox cannot reach the Pages domain and the token cannot push.
Publish through Joe's Chrome:

  github.com/jpwarner-sys/deep-pocket/upload/main

  · file_upload onto the type=file input. NEVER click it — a click opens a
    native dialog you cannot see, and the run stalls silently.
  · Set the commit message with the native setter, not by typing:
      const i=document.querySelector('input#commit-summary-input, input[name="message"]');
      const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
      s.call(i, MESSAGE_STRING); i.dispatchEvent(new Event('input',{bubbles:true}));
    Without this the commit lands as "Add files via upload".
  · Then JS-click the Commit button. A coordinate click fails silently there.
  · Assets first. index.html LAST, so the live app is never briefly broken.
  · Wait 2–4 minutes for Pages to build.

Every substitution asserts. Never a bare str.replace — that once shipped a
"fix" that was reported as done and wasn't:
  if src.count(old) != 1: sys.exit("FAIL %s: %d matches" % (label, src.count(old)))

A staged copy is a snapshot. If minutes pass, re-check mtime before deriving
from it or you'll overwrite an edit Joe made.

────────────────────────────────────────────────────────
11. DONE MEANS — read the LIVE URL, paste what came back
────────────────────────────────────────────────────────
  GET jpwarner-sys.github.io/deep-pocket/
      title:                        Deep Pocket
      apple-mobile-web-app-capable: yes
      apple-touch-icon:             present
      face version:                 v31 web
  GET .../manifest.webmanifest   → id, scope, start_url all "/deep-pocket/"
  GET .../kits/kits.json         → 200, synth.rmsAtFull.hh still 0.01344
  GET .../kits/tr808/kick-1.flac → 200
  Plus, in your own words with numbers:
      · measured contrast ratio, lit step against its well
      · voice-row count in the built file
      · grid + arranger as a % of face height in V-EDIT, measured at
        430 x 932, not 390 x 844
      · the four measured env(safe-area-inset-*) values, portrait and
        landscape, read off the phone in standalone
      · proof the splash still unlocks audio: tap through, show ctx.state is
        'running' AND that currentTime advanced, play Motown, confirm the
        hats are audible on Black Pearl. The splash IS the gesture surface.
        Reskinning it is the likeliest way to break sound in this pass, and
        no pixel measurement will catch that.

Pages lags. If the face still says v30, wait and re-read. Never declare done
on a v30 face. "It should work" is not a report.

Before publishing: grep the built file for real names, client or firm
references, and file paths — comments count. Say the count. Never type a
credential; the app gets a field and Joe pastes it.

────────────────────────────────────────────────────────
12. HOW TO WORK WITH JOE
────────────────────────────────────────────────────────
Dense over trimmed; he reads fast. Don't ask permission for reversible
things on his own machine or accounts — fetching, reading, running, driving
his browser. Just do them. Only confirm before sending something as him to
another person, or before something irreversible. Make choices on his
behalf; only ask when it's extremely material. Any paste you give him is the
complete final paste — never a partial, never "append this". Links on their
own line as a bare address, no scheme, no markdown wrapper — he reads these
on a phone.

────────────────────────────────────────────────────────
13. NEVER PUT THESE IN THE REPO
────────────────────────────────────────────────────────
design/ is published on the public internet. Device serial numbers, Wi-Fi or
Bluetooth MAC addresses, IMEI, account names, real names, client or firm
references, and local file paths never go into any file that lands in this
repo — comments count. Device MODEL is fine and useful. Identifiers are not.

────────────────────────────────────────────────────────
START BY
────────────────────────────────────────────────────────
1. Read the live URL. Report: face version, voice-row count, current hh value.
2. Open v31_CONCEPT.html in a browser and say what you think the material is
   doing well and where the layout is weak.
3. Tell Joe which surface you'll build first and what it will cost.
Then build.
