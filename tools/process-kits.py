#!/usr/bin/env python3
"""Process source drum kits into Deep Pocket's 9-voice × 5-layer FLAC layout.

Matches the shipped AVL derivative pipeline:
  mono 44.1 kHz s16 FLAC, onset trim, per-voice tail caps, short end fade,
  peak ceiling 0.985 (AVL kits), RMS measured over 0.25 s from -60 dBFS onset.

Expected sources under /tmp/kit-src (not shipped):

  blondebop/h2/AVLDrumkits-BlondeBop/          Hydrogen AVLDrumkits-BlondeBop
  blondebop/hr/AVLDrumkits-BlondeBop-HotRod/   Hydrogen AVLDrumkits-BlondeBop-HotRod
  lm2/*.wav                                    oramics/sampled DM/LM-2

Writes kits/{blondebop,hotrods,lm2}/*.flac and merges entries into kits/kits.json.
"""
from __future__ import print_function

import json
import os
import re
import sys

import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KITS_DIR = os.path.join(ROOT, "kits")
MAN_PATH = os.path.join(KITS_DIR, "kits.json")

SR = 44100
LAYERS = 5
VOICES = ("kick", "snare", "rim", "clap", "hh", "oh", "ride", "tom", "perc")
PEAK_CEIL = 0.985
FADE_S = 0.02
ONSET_DB = -60
RMS_WINDOW = 0.25

# Tail caps tuned to the shipped Black Pearl / Red Zeppelin derivatives.
CAPS = {
    "kick": 1.20,
    "snare": 0.90,
    "rim": 0.30,
    "clap": 0.40,
    "hh": 0.30,
    "oh": 0.60,
    "ride": 2.00,
    "tom": 1.50,
    "perc": 0.55,
}


def load_mono(path, target_sr=SR):
    data, sr = sf.read(path, dtype="float64", always_2d=True)
    mono = data.mean(axis=1)
    if sr != target_sr:
        # Linear resample — fine for one-shots; avoids an extra dependency.
        n = int(round(len(mono) * float(target_sr) / sr))
        x_old = np.linspace(0.0, 1.0, num=len(mono), endpoint=False)
        x_new = np.linspace(0.0, 1.0, num=n, endpoint=False)
        mono = np.interp(x_new, x_old, mono)
        sr = target_sr
    return mono, sr


def find_onset(x, thr_db=ONSET_DB):
    peak = float(np.max(np.abs(x))) if len(x) else 0.0
    if peak <= 0:
        return 0
    thr = peak * (10.0 ** (thr_db / 20.0))
    idx = int(np.argmax(np.abs(x) >= thr))
    return idx


def process_sample(path, voice, peak_normalize=True):
    x, sr = load_mono(path)
    onset = find_onset(x)
    # Keep a tiny pre-roll so hard transients are not clipped.
    start = max(0, onset - int(0.002 * sr))
    x = x[start:]
    cap = int(round(CAPS[voice] * sr))
    if len(x) > cap:
        x = x[:cap]
    fade = min(int(round(FADE_S * sr)), max(1, len(x) // 4))
    if fade > 1 and len(x) > fade:
        x = x.copy()
        x[-fade:] *= np.linspace(1.0, 0.0, fade, endpoint=True)
    peak = float(np.max(np.abs(x))) if len(x) else 0.0
    if peak > 0:
        if peak_normalize:
            x = x * (PEAK_CEIL / peak)
        elif peak > PEAK_CEIL:
            x = x * (PEAK_CEIL / peak)
    return x.astype(np.float64), sr


def onset_rms(x, sr):
    onset = find_onset(x)
    n = int(round(RMS_WINDOW * sr))
    seg = x[onset : onset + n]
    if len(seg) < n:
        seg = np.pad(seg, (0, n - len(seg)))
    return float(np.sqrt(np.mean(seg ** 2)))


def write_flac(path, x, sr):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Clip to s16 range after float processing.
    y = np.clip(x, -1.0, 1.0)
    sf.write(path, y, sr, subtype="PCM_16", format="FLAC")


def glob_one(directory, pattern):
    """Return a single path matching pattern, or raise."""
    rx = re.compile("^" + pattern.replace("*", ".*") + "$")
    hits = sorted(
        os.path.join(directory, n)
        for n in os.listdir(directory)
        if rx.match(n)
    )
    if not hits:
        raise FileNotFoundError("%s / %s" % (directory, pattern))
    return hits[0]


def avl_layers(directory, stem):
    """Five velocity files: stem-1.wav … stem-5.wav (Hydrogen naming)."""
    out = []
    for i in range(1, LAYERS + 1):
        path = os.path.join(directory, "%s-%d.wav" % (stem, i))
        if not os.path.isfile(path):
            raise FileNotFoundError(path)
        out.append(path)
    return out


def dup_layers(paths):
    """Pad/trim a list of source paths to exactly five layers."""
    if not paths:
        raise ValueError("no paths")
    if len(paths) >= LAYERS:
        # Evenly pick five across the available set.
        idx = [int(round(i * (len(paths) - 1) / float(LAYERS - 1))) for i in range(LAYERS)]
        return [paths[j] for j in idx]
    out = list(paths)
    while len(out) < LAYERS:
        out.append(paths[-1])
    return out


def emit_kit(kit_id, voice_sources, peak_normalize=True):
    """voice_sources: {voice: [path, path, path, path, path]}"""
    out_dir = os.path.join(KITS_DIR, kit_id)
    os.makedirs(out_dir, exist_ok=True)
    voices = {}
    rms = {}
    for voice in VOICES:
        srcs = voice_sources[voice]
        if len(srcs) != LAYERS:
            raise ValueError("%s/%s: expected %d layers, got %d" % (kit_id, voice, LAYERS, len(srcs)))
        files = []
        rms_v = []
        for li, src in enumerate(srcs):
            x, sr = process_sample(src, voice, peak_normalize=peak_normalize)
            rel = "%s/%s-%d.flac" % (kit_id, voice, li + 1)
            dest = os.path.join(KITS_DIR, rel.replace("/", os.sep))
            write_flac(dest, x, sr)
            files.append(rel)
            rms_v.append(round(onset_rms(x, sr), 6))
            print("  %s  %6.3fs  rms=%.4f  <- %s" % (rel, len(x) / float(sr), rms_v[-1], os.path.basename(src)))
        voices[voice] = files
        rms[voice] = rms_v
    return voices, rms


def build_blondebop():
    src = "/tmp/kit-src/blondebop/h2/AVLDrumkits-BlondeBop"
    mapping = {
        "kick": "36-TAMA-18-Kick",
        "snare": "38-TAMA-13-Snare",
        "rim": "37-TAMA-13-SideStick",
        "clap": "39-HandClap",
        "hh": "42-Zildjian-13-HatClosed",
        "oh": "46-Zildjian-13-HatSemi",
        "ride": "51-SabianAAX-20-RideTip",
        "tom": "45-TAMA-10-Tom",
        "perc": "56-LP-1-Cowbell",
    }
    sources = {v: avl_layers(src, stem) for v, stem in mapping.items()}
    print("=== blondebop ===")
    return emit_kit("blondebop", sources, peak_normalize=True)


def build_hotrods():
    src = "/tmp/kit-src/blondebop/hr/AVLDrumkits-BlondeBop-HotRod"
    mapping = {
        "kick": "36-TAMA-18-Kick-HR",
        "snare": "38-TAMA-13-SnareCenter-HR",
        "rim": "37-TAMA-13-SnareSidestick-HR",
        "clap": "39-HandClap",
        "hh": "42-Zildjian-13-HatClosed-HR",
        "oh": "46-Zildjian-12-HatSemi-HR",
        "ride": "51-SabianAAX-20-RideTip-HR",
        "tom": "45-TAMA-10-TomCenter-HR",
        "perc": "56-LP-1-Cowbell-HR",
    }
    sources = {v: avl_layers(src, stem) for v, stem in mapping.items()}
    print("=== hotrods ===")
    return emit_kit("hotrods", sources, peak_normalize=True)


def build_lm2():
    src = "/tmp/kit-src/lm2"

    def p(name):
        return os.path.join(src, name)

    # snare-l/m/h and stick-l/m/h are pitch tiers on the LM-2, not velocity —
    # pin the classic mid/low voices and let kitGain supply dynamics (808-style).
    # Closed-hat short/med/long and the five toms are decay/pitch variants that
    # read well as soft→hard layers, same idea as the Fischer 808 decay rows.
    sources = {
        "kick": dup_layers([p("kick-alt.wav"), p("kick.wav")]),
        "snare": dup_layers([p("snare-l.wav")]),
        "rim": dup_layers([p("stick-m.wav")]),
        "clap": dup_layers([p("clap.wav")]),
        "hh": dup_layers([
            p("hihat-closed-short.wav"),
            p("hihat-closed.wav"),
            p("hihat-closed-long.wav"),
        ]),
        "oh": dup_layers([p("hihat-open.wav")]),
        "ride": dup_layers([p("ride.wav")]),
        "tom": [
            p("tom-ll.wav"),
            p("tom-l.wav"),
            p("tom-m.wav"),
            p("tom-h.wav"),
            p("tom-hh.wav"),
        ],
        "perc": dup_layers([p("cowb.wav")]),
    }
    print("=== lm2 ===")
    # Machine samples are already one-shot; keep natural levels (808-style),
    # only ceiling if a file clips past PEAK_CEIL.
    return emit_kit("lm2", sources, peak_normalize=False)


def kit_entry(name, credit, voices, rms, note=None):
    entry = {"name": name, "credit": credit, "voices": voices, "rms": rms}
    if note:
        entry["note"] = note
    return entry


def main():
    bb_v, bb_r = build_blondebop()
    hr_v, hr_r = build_hotrods()
    lm_v, lm_r = build_lm2()

    man = json.load(open(MAN_PATH))
    man["kits"]["blondebop"] = kit_entry(
        "Blonde Bop",
        "AVL Blonde Bop by Glen MacArthur — CC BY-SA 3.0",
        bb_v,
        bb_r,
    )
    man["kits"]["hotrods"] = kit_entry(
        "Hot Rods",
        "AVL Blonde Bop Hot Rods by Glen MacArthur — CC BY-SA 3.0",
        hr_v,
        hr_r,
    )
    man["kits"]["lm2"] = kit_entry(
        "LinnDrum LM-2",
        "LinnDrum LM-2 samples via oramics/sampled (hyperreal.org) — Public Domain",
        lm_v,
        lm_r,
        note=(
            "snare, rim, clap, oh, ride and perc map one source sample to all five "
            "layers (the LM-2 has no velocity layers there; snare-l/m/h are pitch "
            "tiers). kick uses kick-alt→kick; hh uses closed short/med/long; tom "
            "uses the five pitched toms soft→hard."
        ),
    )

    # Top-level credit covers the shared AVL family; per-kit credits override in UI.
    with open(MAN_PATH, "w") as f:
        json.dump(man, f, indent=1, sort_keys=False)
        f.write("\n")
    print("wrote", MAN_PATH)


if __name__ == "__main__":
    main()
