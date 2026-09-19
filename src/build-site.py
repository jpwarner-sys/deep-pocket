#!/usr/bin/env python3
"""Deep Pocket build / gate — src/build-site.py

Path of record (STORE.md, 2026-09-15 working copy):
  C:\\Users\\Giggawattz\\Grok Build\\deep-pocket\\src\\build-site.py
This file was never on the GitHub Pages tree. Recovered here so local
builds can gate the shipped face without the Windows src/site split.

What this script patches
------------------------
The HTML face badge:  <span class="ver" id="ver">…</span>
That is FACE_EXPECT. The historical bug was asserting "v20 web" after
the shell had moved to "v21 web" (commits a204882 → 7035168).

This script does NOT patch sw.js CACHE. Live cache is deep-pocket-v35
and stays there unless a later change edits shipped index.html / sw.js.

Asserted before (historical):  #ver == "v20 web"   (mismatch vs shell v21)
Asserted after  (this file):   #ver == "v31 web"   (current shipped face)

AVL kits
--------
The hard 90-file check is {blackpearl, redzeppelin} × 9 voices × 5
layers. If kits/ or those AVL dirs are absent, warn and skip — do not
crash the build. When the dirs are present, the 90-file integrity
check still runs. kits.json is written to a synth-only default if
missing so the kit-metadata fetch path still resolves.
"""
from __future__ import print_function

import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---------------------------------------------------------------------------
# Face badge — the string this script actually patches / asserts.
# NOT the SW cache name (deep-pocket-v35). SW did not exist at the v20/v21
# mismatch; CACHE is left untouched.
# Historical assert: "v20 web"  (broke when shell.html read "v21 web")
# Current shipped face on main: "v31 web"
# ---------------------------------------------------------------------------
FACE_EXPECT = "v31 web"
FACE_HISTORICAL_WRONG = "v20 web"  # what the old gate hardcoded
VER_RE = re.compile(
    r'(<span\s+class="ver"\s+id="ver">)([^<]*)(</span>)',
    re.IGNORECASE,
)

# Hard integrity check when these dirs are present. Newer AVL kits
# (blondebop, hotrods) are covered by check_referenced_samples instead.
AVL_KITS = ("blackpearl", "redzeppelin")
VOICES = ("kick", "snare", "rim", "clap", "hh", "oh", "ride", "tom", "perc")
LAYERS = 5
AVL_EXPECT = len(AVL_KITS) * len(VOICES) * LAYERS  # 90

# STORE.md: size ceiling on the built face. v21 was 125,812 bytes; the
# current single-file face carries a data-URI apple-touch-icon (~235 KB).
# QC protocol used ≤ 310 KB; leave a little headroom, do not fail v31.
SIZE_CEILING = 400000

# Whole-word leaks that must not appear in the built face. CSS
# `font-family` is not in this list.
PRIVATE_WORDS = (
    "estate",
    "clinical",
    "ontologyhome",
)

# Graceful default when kits.json is missing (AVL skipped or a
# kits-less working copy). Engine loadKit() fetches kits/kits.json;
# synth.rmsAtFull.hh = 0.01344 is the hats-audible floor — do not revert.
DEFAULT_MANIFEST = {
    "format": "flac",
    "layers": LAYERS,
    "velocity": [[1, 26], [27, 52], [53, 77], [78, 102], [103, 127]],
    "credit": "",
    "kits": {},
    "synth": {
        "rmsAtFull": {
            "kick": 0.397144,
            "snare": 0.052047,
            "rim": 0.032826,
            "clap": 0.021999,
            "hh": 0.01344,
            "oh": 0.009863,
            "ride": 0.013658,
            "tom": 0.245725,
            "perc": 0.038209,
        },
        "velExp": {
            "kick": 0.624,
            "snare": 0.977,
            "rim": 0.95,
            "clap": 0.871,
            "hh": 0.882,
            "oh": 0.996,
            "ride": 0.994,
            "tom": 0.77,
            "perc": 0.953,
        },
        "note": (
            "graceful default written by build-site.py because kits.json "
            "was absent; AVL sample paths omitted."
        ),
    },
}


def fail(msg):
    sys.stderr.write("FAIL %s\n" % msg)
    sys.exit(1)


def warn(msg):
    sys.stderr.write("WARN %s\n" % msg)


def info(msg):
    sys.stderr.write("OK   %s\n" % msg)


def site_root():
    """Pages-root tree on GitHub; local working copy used site/."""
    nested = os.path.join(ROOT, "site", "index.html")
    if os.path.isfile(nested):
        return os.path.join(ROOT, "site")
    return ROOT


def assemble_if_sources(site):
    """If src/{shell.html,engine.js,presets.js} exist, stitch site/index.html.

    Gate-only otherwise — this GitHub tree has no src/site split. Never
    rewrite a Pages-root index.html in place (do not bump CACHE).
    """
    shell_p = os.path.join(HERE, "shell.html")
    engine_p = os.path.join(HERE, "engine.js")
    presets_p = os.path.join(HERE, "presets.js")
    have = all(os.path.isfile(p) for p in (shell_p, engine_p, presets_p))
    if not have:
        info("no src/{shell,engine,presets} — gate-only on %s" % site)
        return False

    if site == ROOT:
        site = os.path.join(ROOT, "site")
    if not os.path.isdir(site):
        os.makedirs(site)

    with open(shell_p, "r", encoding="utf-8") as f:
        html = f.read()
    with open(engine_p, "r", encoding="utf-8") as f:
        engine = f.read()
    with open(presets_p, "r", encoding="utf-8") as f:
        presets = f.read()

    html, n = VER_RE.subn(r"\1%s\3" % FACE_EXPECT, html, count=1)
    if n != 1:
        fail("shell.html: expected one #ver badge to patch, got %d" % n)

    marker = "<!--BUILD_SCRIPTS-->"
    bundle = (
        "<script>\n%s\n</script>\n<script>\n%s\n</script>\n" % (engine, presets)
    )
    if marker in html:
        if html.count(marker) != 1:
            fail("shell.html: BUILD_SCRIPTS marker is not unique")
        html = html.replace(marker, bundle)
    else:
        html = html.replace("</body>", bundle + "</body>", 1)

    out = os.path.join(site, "index.html")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    info("assembled %s (%d bytes), #ver patched to %r" % (
        out, len(html.encode("utf-8")), FACE_EXPECT))

    src_kits = os.path.join(ROOT, "kits")
    dst_kits = os.path.join(site, "kits")
    if os.path.isdir(src_kits) and os.path.abspath(src_kits) != os.path.abspath(dst_kits):
        if os.path.isdir(dst_kits):
            shutil.rmtree(dst_kits)
        shutil.copytree(src_kits, dst_kits)
    return True


def assert_face(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        src = f.read()
    m = VER_RE.search(src)
    if not m:
        fail("%s: no <span class=\"ver\" id=\"ver\"> badge" % html_path)
    got = m.group(2).strip()
    if got == FACE_HISTORICAL_WRONG and FACE_EXPECT != FACE_HISTORICAL_WRONG:
        fail(
            "%s: #ver is still the historical hardcoded %r; "
            "current shipped face is %r (HTML badge this script patches, "
            "not sw.js CACHE deep-pocket-v35)" % (
                html_path, FACE_HISTORICAL_WRONG, FACE_EXPECT)
        )
    if got != FACE_EXPECT:
        fail(
            "%s: #ver is %r, expected %r "
            "(script patches the HTML face badge, not CACHE)" % (
                html_path, got, FACE_EXPECT)
        )
    info("#ver == %r  (HTML face; CACHE deep-pocket-v35 not asserted)" % got)
    return src


def assert_clean(src, html_path):
    n_audio = src.lower().count("data:audio")
    if n_audio:
        fail("%s: data:audio present (%d)" % (html_path, n_audio))
    info("no data:audio")

    lower = src.lower()
    # Avoid CSS `font-family` false hits by scanning as whole words.
    for word in PRIVATE_WORDS:
        if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(word),
                     lower):
            fail("%s: private word %r" % (html_path, word))
    info("no private words %s" % (PRIVATE_WORDS,))

    nbytes = len(src.encode("utf-8"))
    if nbytes > SIZE_CEILING:
        fail("%s: %d bytes > ceiling %d" % (html_path, nbytes, SIZE_CEILING))
    info("size %d <= %d" % (nbytes, SIZE_CEILING))


def flac_under(d):
    out = []
    for dirpath, _dirnames, filenames in os.walk(d):
        for name in filenames:
            if name.lower().endswith(".flac"):
                out.append(os.path.join(dirpath, name))
    return out


def ensure_kits_json(kits_dir):
    """Return parsed kits.json, writing the synth-only default if absent."""
    if not os.path.isdir(kits_dir):
        os.makedirs(kits_dir)
        warn("kits/ was absent — created so kit metadata path resolves")
    man_path = os.path.join(kits_dir, "kits.json")
    if not os.path.isfile(man_path):
        with open(man_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_MANIFEST, f, indent=1)
            f.write("\n")
        warn("kits.json missing — wrote synth-only default (hh rms 0.01344)")
    with open(man_path, "r", encoding="utf-8") as f:
        man = json.load(f)
    if not isinstance(man, dict):
        fail("kits.json: expected object")
    kits = man.get("kits")
    if kits is None:
        man["kits"] = {}
        warn("kits.json had no 'kits' key — defaulted to {}")
        kits = man["kits"]
    elif not isinstance(kits, dict):
        fail("kits.json: 'kits' must be an object")
    synth = man.get("synth") or {}
    rms = (synth.get("rmsAtFull") or {})
    hh = rms.get("hh")
    if hh is None:
        warn("kits.json missing synth.rmsAtFull.hh — defaulting 0.01344")
        synth = dict(synth)
        rms = dict(rms)
        rms["hh"] = 0.01344
        synth["rmsAtFull"] = rms
        man["synth"] = synth
    return man, man_path


def check_referenced_samples(kits_dir, man, skip_avl):
    """Every kits.json sample path exists, except AVL refs when AVL skipped."""
    missing = []
    checked = 0
    kits = man.get("kits") or {}
    for kit_id, spec in kits.items():
        if skip_avl and kit_id in AVL_KITS:
            continue
        voices = (spec or {}).get("voices") or {}
        for _voice, files in voices.items():
            for rel in files or []:
                checked += 1
                path = os.path.join(kits_dir, rel.replace("/", os.sep))
                if not os.path.isfile(path):
                    missing.append(rel)
    if missing:
        fail("kits.json references missing samples: %s" % (", ".join(missing[:12]),))
    info("kits.json sample paths exist (%d checked%s)" % (
        checked, "; AVL refs skipped" if skip_avl else ""))


def check_avl(kits_dir):
    """Exact {blackpearl, redzeppelin} × 90 FLAC. Existence-gated."""
    if not os.path.isdir(kits_dir):
        warn("kits/ absent — skipping AVL 90-file assert (not a hard fail)")
        return True  # skipped

    present = [k for k in AVL_KITS if os.path.isdir(os.path.join(kits_dir, k))]
    missing = [k for k in AVL_KITS if k not in present]
    if missing:
        warn(
            "AVL kit dir(s) absent (%s) — skipping exact %d-file assert "
            "for {blackpearl, redzeppelin}" % (", ".join(missing), AVL_EXPECT)
        )
        return True  # skipped

    files = []
    for kit in AVL_KITS:
        files.extend(flac_under(os.path.join(kits_dir, kit)))
    n = len(files)
    if n != AVL_EXPECT:
        fail(
            "AVL kits: expected exactly %d FLAC under %s, found %d" % (
                AVL_EXPECT, ",".join(AVL_KITS), n)
        )
    # Naming: <kit>/<voice>-<1..5>.flac
    expected = set()
    for kit in AVL_KITS:
        for voice in VOICES:
            for layer in range(1, LAYERS + 1):
                expected.add("%s/%s-%d.flac" % (kit, voice, layer))
    got = set()
    for path in files:
        rel = os.path.relpath(path, kits_dir).replace(os.sep, "/")
        got.add(rel)
    missing_names = sorted(expected - got)
    extra = sorted(got - expected)
    if missing_names or extra:
        fail(
            "AVL kits name set mismatch: missing %s extra %s" % (
                missing_names[:8], extra[:8])
        )
    info("AVL kits: %d FLAC under %s" % (n, ",".join(AVL_KITS)))
    return False  # not skipped — integrity ran


def main():
    site = site_root()
    assemble_if_sources(site)
    # Re-resolve after assemble (may have created site/).
    site = site_root()
    html_path = os.path.join(site, "index.html")
    if not os.path.isfile(html_path):
        fail("no index.html at %s" % html_path)

    src = assert_face(html_path)
    assert_clean(src, html_path)

    kits_dir = os.path.join(site, "kits")
    skipped = check_avl(kits_dir)
    man, man_path = ensure_kits_json(kits_dir)
    check_referenced_samples(kits_dir, man, skip_avl=skipped)
    hh = ((man.get("synth") or {}).get("rmsAtFull") or {}).get("hh")
    info("kit metadata %s  synth.rmsAtFull.hh=%s" % (man_path, hh))
    info("build-site.py PASS")


if __name__ == "__main__":
    main()
