# Deep Pocket

A rhythm trainer for bass practice. Nine voices, 18 grooves, a 32-bar arranger
with chord changes, a bass voice that follows the changes, and a lock-screen mode
that keeps the loop playing when the phone sleeps.

Everything runs in the browser — Web Audio synthesis, a lookahead scheduler with
swing and per-groove micro-timing, and two sampled acoustic kits.

Saved setups live in this browser's local storage. Nothing is sent anywhere.

## Kits

**Synth** — every voice synthesised live at its exact velocity.

**Black Pearl** and **Red Zeppelin** — samples from
[AVL Drumkits](https://github.com/studiorack/avl-drumkits) by **Glen MacArthur**,
used under **CC BY-SA 3.0**. Five velocity layers per voice, trimmed and
tail-capped for this app; the samples in `kits/` are a derivative work and carry
the same CC BY-SA 3.0 licence.

AVL normalises each sample, so its velocity layers carry the *timbre* of a soft
or hard hit but not its loudness, and its SFZ sets no `amp_veltrack` — meaning
the player is expected to supply the velocity gain. This app measures its own
synth's velocity response per voice and reproduces that curve over the samples,
so a sampled kit has the same dynamics as the synth rather than a flat one.

## Licence

App code: see `LICENSE` if present, otherwise all rights reserved by the author.
Sample content under `kits/`: CC BY-SA 3.0, © Glen MacArthur (AVL Drumkits).
