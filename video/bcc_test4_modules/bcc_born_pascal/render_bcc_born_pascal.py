#!/usr/bin/env python3
"""v2_sound (v4 suite, synthesized SFX): explainer video for bcc_born_pascal.py (module imported unchanged; the
per-tick states are the module's own function called with n_ticks = 1..12)."""
import sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from bccvid import *
import_src()
import bcc_born_pascal as bp

OUT = "/workspace/bcc_test4_videos/v2_sound/bcc_born_pascal"
STEPS = {n: bp.compute_dual_pascal_distribution(n_ticks=n) for n in range(1, 13)}
R12 = STEPS[12]['rows']
DARK = [r['x'] for r in R12 if r['net_psi'] == 0]
assert DARK == [-10, -6, -2, 2, 6, 10]
assert [(r['pos'], r['neg']) for r in R12][6] == (452, 472)
ERR = {n: bp.compute_dual_pascal_distribution(n_ticks=n)['max_abs_diff'] for n in (12, 24, 48, 100)}
assert [round(ERR[n], 6) for n in (12, 24, 48, 100)] == [0.217776, 0.144931, 0.098975, 0.067291]

v = Video(OUT, "_silent", "bcc_test4 · bcc_born_pascal.py",
          "Toy model · integer path counting · numbers from the actual run of bcc_born_pascal.py")
v.add(4, title_card("Two-channel Pascal walk", "Counting paths in + and − channels; cancellations make dark nodes"))

def walk(fig, t, T):
    n = min(1 + int(t / 0.85), 12)
    rows = STEPS[n]['rows']
    m = max(max(r['pos'], r['neg']) for r in rows)
    ax = style_ax(fig.add_axes([0.07, 0.18, 0.86, 0.66]))
    xs = [r['x'] for r in rows]
    ax.bar(xs, [r['pos'] / m for r in rows], width=0.8, color=CYAN, label="N₊")
    ax.bar(xs, [-r['neg'] / m for r in rows], width=0.8, color=ORANGE, label="N₋")
    ax.axhline(0, color=FG, lw=1)
    if n == 12:
        for r in rows:
            ax.text(r['x'], 1.06, f"{r['pos']}", ha="center", fontsize=13, color=CYAN)
            ax.text(r['x'], -1.12, f"{r['neg']}", ha="center", fontsize=13, color=ORANGE)
            if r['net_psi'] == 0:
                ax.axvspan(r['x'] - 0.5, r['x'] + 0.5, color=GREEN, alpha=0.18)
    ax.set_xlim(-13, 13); ax.set_ylim(-1.25, 1.25); ax.set_yticks([])
    ax.set_xticks(range(-12, 13, 2)); ax.set_xlabel("position x", fontsize=16)
    ax.legend(loc="upper left", frameon=False, fontsize=20)
    ax.text(12.6, 1.15, f"tick {n}", ha="right", fontsize=24, color=FG)

v.add(15, walk, [(0.3, "Each tick every path steps left or right"),
                 (4.0, "On even ticks a right step swaps channel + ↔ −"),
                 (10.5, "Green: N₊ = N₋, so net ψ = 0 (dark node)")], "1 · Path counts")

def born(fig, t, T):
    ax = style_ax(fig.add_axes([0.07, 0.18, 0.86, 0.66]))
    xs = [r['x'] for r in R12]
    g = ramp(t, 0.3, 1.5); gw = ramp(t, 4.0, 1.0)
    ax.bar(xs, [r['p_born'] * g for r in R12], width=1.2, color=CYAN, label="(N₊ − N₋)²  normalised")
    if gw > 0:
        ax.plot(xs, [r['p_wave'] for r in R12], "o-", color=YELLOW, lw=3, ms=10, alpha=gw,
                label="reference: e^(−x²/N)·cos²(πx/4)")
    for x in DARK:
        ax.text(x, 0.015, "0", ha="center", fontsize=20, color=GREEN, weight="bold")
    for r in R12:
        if r['p_born'] > 0.1 and g > 0.9:
            ax.text(r['x'], r['p_born'] + 0.012, f"{r['p_born']:.4f}", ha="center", fontsize=15)
    ax.set_xlim(-13, 13); ax.set_ylim(0, 0.72); ax.set_xticks(range(-12, 13, 2))
    ax.set_xlabel("position x  (N = 12)", fontsize=16); ax.set_ylabel("probability", fontsize=16)
    ax.legend(loc="upper left", frameon=False, fontsize=18)

v.add(13, born, [(0.3, "Square the net count: six exact zeros"),
                 (4.0, "Yellow: a chosen comparison curve, not a solved wave equation"),
                 (8.5, "Biggest gap at the centre: 0.4329 vs 0.6507")], "2 · Born-style weights")

def conv(fig, t, T):
    ax = style_ax(fig.add_axes([0.12, 0.20, 0.76, 0.62]))
    ns = [12, 24, 48, 100]
    k = min(int(t / 1.2) + 1, 4)
    ax.plot(ns[:k], [ERR[n] for n in ns[:k]], "o-", color=CYAN, lw=4, ms=16)
    for n in ns[:k]:
        ax.text(n + 2, ERR[n] + 0.008, f"{ERR[n]:.6f}", fontsize=20)
    ax.set_xlim(0, 115); ax.set_ylim(0, 0.25); ax.set_xticks(ns)
    ax.set_xlabel("ticks N", fontsize=18); ax.set_ylabel("max |Born − reference|", fontsize=18)

v.add(10, conv, [(0.3, "More ticks, smaller gap to the reference curve"),
                 (5.5, "Still 0.067 at N = 100: shrinking, not shown to reach zero")], "3 · Convergence")

v.add(7, end_card([("Pure integer counting in two channels", CYAN),
                   ("Exact dark nodes at x = ±2, ±6, ±10 (N = 12)", GREEN),
                   ("Reference curve is hand-chosen; its zeros sit on the dark nodes", YELLOW),
                   ("Gap shrinks 0.218 → 0.067 from N = 12 to 100", DIM)]))

def timeline():
    sc = scene_starts(v); a = [x["start"] for x in sc]
    return {"total": v.duration, "scenes": sc, "title": [0, a[1]],
            "ticks": [a[1] + (n - 1) * 0.85 for n in range(1, 13)], "dark": a[1] + 11 * 0.85,
            "born_rise": [a[2] + 0.3, a[2] + 1.8], "ref": a[2] + 4.0,
            "conv": [[a[3] + 1.2 * k, ERR[n]] for k, n in enumerate((12, 24, 48, 100))], "end": a[4]}

if __name__ == "__main__":
    finish(v, "bcc_born_pascal", timeline(), os.path.join(OUT, "sfx_bcc_born_pascal.py"),
           thumb_t=4 + 14.5, audio_only="--audio-only" in sys.argv)
