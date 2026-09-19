# Deep Pocket

A rhythm trainer for bass practice. Nine voices, 18 grooves, a 32-bar arranger
with chord changes, a bass voice that follows the changes, and a lock-screen mode
that keeps the loop playing when the phone sleeps.

Live at: https://pocket.ontologyhome.ca/

(Formerly hosted at `https://jpwarner-sys.github.io/deep-pocket/`. The PWA manifest and service worker are now scoped to the root `/` for the custom domain.)

Everything runs in the browser — Web Audio synthesis, a lookahead scheduler with
swing and per-groove micro-timing, and sampled kits (AVL Black Pearl / Red Zeppelin /
Blonde Bop / Hot Rods, Fischer TR-808, LinnDrum LM-2).

Saved setups live in this browser under `deeppocket.*` keys. Nothing is sent anywhere.
The service worker is scoped to the root `/` for the custom domain. It only manages caches prefixed with `deep-pocket-` to avoid collision with other apps if ever hosted on a shared origin.

v21 freeze: branch `backup/v21-20260915`.

## Kits

**Synth** — every voice synthesised live at its exact velocity.

**Black Pearl** and **Red Zeppelin** — samples from
[AVL Drumkits](https://github.com/studiorack/avl-drumkits) by **Glen MacArthur**,
used under **CC BY-SA 3.0**. Five velocity layers per voice, trimmed and
tail-capped for this app; the samples in `kits/blackpearl` and `kits/redzeppelin`
are a derivative work and carry the same CC BY-SA 3.0 licence.

**Blonde Bop** and **Hot Rods** — AVL Blonde Bop (TAMA Club Jam maple, sticks)
and Blonde Bop Hot Rods (same kit with Promark Hot Rods) by **Glen MacArthur**,
**CC BY-SA 3.0**, from the Hydrogen AVLDrumkits packages. Same 9 × 5 layout in
`kits/blondebop` and `kits/hotrods`; derivatives carry CC BY-SA 3.0.

**TR-808** — Roland TR-808 samples by **Michael Fischer** (Technopolis, 1994),
from [tidalcycles/sounds-tr808-fischer](https://github.com/tidalcycles/sounds-tr808-fischer),
[CC0](https://creativecommons.org/publicdomain/zero/1.0/). Five layers per voice
in `kits/tr808`.

**LinnDrum** — LinnDrum LM-2 one-shots via
[oramics/sampled](https://oramics.github.io/sampled/DM/LM-2/) (Public Domain,
hyperreal.org archive). Mapped to 9 × 5 in `kits/lm2`.

AVL normalises each sample, so its velocity layers carry the *timbre* of a soft
or hard hit but not its loudness, and its SFZ sets no `amp_veltrack` — meaning
the player is expected to supply the velocity gain. This app measures its own
synth's velocity response per voice and reproduces that curve over the samples,
so a sampled kit has the same dynamics as the synth rather than a flat one.

Rebuild derivatives with `python3 tools/process-kits.py` (expects source trees
under `/tmp/kit-src` as documented in that script).

## Licence

App code: see `LICENSE` if present, otherwise all rights reserved by the author.
Sample content under `kits/blackpearl`, `kits/redzeppelin`, `kits/blondebop`, and
`kits/hotrods`: CC BY-SA 3.0, © Glen MacArthur (AVL Drumkits).
Sample content under `kits/tr808`: CC0, Michael Fischer / Technopolis.
Sample content under `kits/lm2`: Public Domain (oramics/sampled / hyperreal.org).
