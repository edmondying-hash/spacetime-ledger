#!/usr/bin/env python3
"""v2_sound: explainer video for baryon_calculator.py on the v4 suite (code imported unchanged), with synthesized SFX."""
import sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from bccvid import *
import_src()
import baryon_calculator as bc

OUT = "/workspace/bcc_test4_videos/v2_sound/baryon_calculator"
NAMES = ['p', 'Delta+', 'Lambda', 'Sigma0', 'Xi0', 'Omega-']
LABEL = {'p': 'p', 'Delta+': 'Δ⁺', 'Lambda': 'Λ', 'Sigma0': 'Σ⁰', 'Xi0': 'Ξ⁰', 'Omega-': 'Ω⁻'}
R = {n: bc.calculate(n) for n in NAMES}
P = bc.Parameters()
# Cross-check against the printed suite output (Model / Compare columns).
PRINTED = {'p': (938.92, 938.27), 'Delta+': (1232.00, 1232.00), 'Lambda': (1115.68, 1115.68),
           'Sigma0': (1179.81, 1192.64), 'Xi0': (1329.77, 1314.86), 'Omega-': (1681.89, 1672.45)}
for n, (m, c) in PRINTED.items():
    assert round(R[n]['mass_MeV'], 2) == m and round(R[n]['comparison_MeV'], 2) == c, n
CAL = {'p', 'Delta+', 'Lambda'}

v = Video(OUT, "_silent", "bcc_test4 · baryon_calculator.py",
          "Effective model calibrated to PDG 2024 · all numbers from the actual run of baryon_calculator.py")

v.add(4, title_card("Baryon mass calculator", "One pair-spin rule for light + strange baryons",
                    "EFFECTIVE MODEL · CALIBRATED TO PDG 2024"))


def fit_scene(fig, t, T):
    ins = [("N  (p/n mean)", f"{bc.DEFAULT_N_MEV:.2f}"), ("Δ  (mixed-charge proxy)", f"{bc.DEFAULT_DELTA_MEV:.2f}"),
           ("Λ", f"{bc.DEFAULT_LAMBDA_MEV:.2f}")]
    outs = [("m_light", f"{P.m_light:.2f}"), ("m_strange", f"{P.m_strange:.2f}"), ("A  (spin coupling)", f"{P.A:.2f}")]
    fig.text(0.25, 0.80, "3 measured masses (PDG 2024)", fontsize=28, ha="center", color=ORANGE, alpha=ramp(t, 0.2))
    fig.text(0.75, 0.80, "3 fitted parameters", fontsize=28, ha="center", color=CYAN, alpha=ramp(t, 2.2))
    for i, (k, val) in enumerate(ins):
        y = 0.65 - i * 0.15; a = ramp(t, 0.4 + 0.4 * i)
        fig.text(0.25, y, f"{k}\n{val} MeV", fontsize=26, ha="center", va="center", alpha=a,
                 bbox=dict(boxstyle="round,pad=0.6", fc=PANEL, ec=ORANGE, alpha=a))
    a = ramp(t, 1.8)
    fig.text(0.5, 0.50, "fit  ➜", fontsize=40, ha="center", va="center", color=DIM, alpha=a)
    for i, (k, val) in enumerate(outs):
        y = 0.65 - i * 0.15; a = ramp(t, 2.4 + 0.4 * i)
        fig.text(0.75, y, f"{k}\n{val} MeV", fontsize=26, ha="center", va="center", alpha=a,
                 bbox=dict(boxstyle="round,pad=0.6", fc=PANEL, ec=CYAN, alpha=a))


v.add(9, fit_scene, [(0.3, "Three known masses fix the three model parameters"),
                     (5.0, "Mass = quark terms + pair-spin shift")], "1 · Calibration")


def bars_scene(fig, t, T):
    ax = style_ax(fig.add_axes([0.08, 0.17, 0.86, 0.68]))
    xs = range(len(NAMES))
    gb = ramp(t, 0.3, 2.5); gs = ramp(t, 4.0, 2.0); gm = ramp(t, 8.5, 1.0)
    for i, n in enumerate(NAMES):
        r = R[n]; base, sh, m, c = r['baseline_MeV'], r['spin_shift_MeV'], r['mass_MeV'], r['comparison_MeV']
        col = DIM if n in CAL else CYAN
        h = 800 + (base - 800) * gb
        ax.bar(i, h - 800, bottom=800, width=0.55, color=col, alpha=0.35, ec=col, lw=1.5)
        if gb > 0.95:
            ax.text(i, h + 8, f"{base:.0f}", ha="center", va="bottom", fontsize=14, color=DIM, alpha=1 - gs)
        if gs > 0:
            top = base + sh * gs
            ax.annotate("", xy=(i, top), xytext=(i, base),
                        arrowprops=dict(arrowstyle="-|>", color=ORANGE if sh > 0 else GREEN, lw=3, mutation_scale=22))
            ax.plot([i - 0.32, i + 0.32], [top, top], color=FG, lw=3)
            if gs > 0.95:
                ax.text(i + 0.36, top, f"{m:.2f}", va="center", fontsize=15, color=FG)
        if gm > 0:
            ax.plot(i, c, marker="D", ms=13, color=YELLOW, alpha=gm, mec=BG)
    ax.set_xticks(list(xs)); ax.set_xticklabels([LABEL[n] for n in NAMES], fontsize=28, color=FG)
    ax.set_ylim(800, 1800); ax.set_xlim(-0.6, 5.9); ax.set_ylabel("MeV", fontsize=20)
    a = ramp(t, 9.5)
    ax.text(1.0, 1745, "CALIBRATION INPUTS", ha="center", fontsize=18, color=DIM, alpha=a, weight="bold")
    ax.text(4.0, 1745, "OUT-OF-FIT COMPARISON", ha="center", fontsize=18, color=CYAN, alpha=a, weight="bold")
    ax.axvline(2.5, color=GRID, lw=2, ls="--", alpha=a)
    if gm > 0:
        ax.plot([], [], "D", color=YELLOW, ms=11, label="PDG 2024 value"); ax.plot([], [], "-", color=FG, lw=3, label="model")
        ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.93), frameon=False, fontsize=17)


v.add(15, bars_scene, [(0.3, "Baseline: sum of effective quark terms"),
                       (4.0, "Pair-spin shift pushes each mass down or up"),
                       (8.5, "◆ = PDG 2024 value"),
                       (11.0, "Left three are fit inputs (p via the p/n mean): matched by construction")], "2 · Six baryons")


def diff_scene(fig, t, T):
    ax = style_ax(fig.add_axes([0.10, 0.20, 0.82, 0.62]))
    for i, n in enumerate(NAMES):
        d = R[n]['difference_MeV']; g = ramp(t, 0.3 + 0.3 * i, 0.8)
        col = DIM if n in CAL else CYAN
        ax.bar(i, d * g, width=0.55, color=col, alpha=0.85)
        if g > 0.9:
            ax.text(i, d + (1.2 if d >= 0 else -1.2), f"{d:+.2f}", ha="center",
                    va="bottom" if d >= 0 else "top", fontsize=20, color=FG)
    ax.axhline(0, color=FG, lw=1.5)
    ax.set_xticks(range(6)); ax.set_xticklabels([LABEL[n] for n in NAMES], fontsize=28, color=FG)
    ax.set_ylim(-20, 20); ax.set_ylabel("model − PDG  (MeV)", fontsize=20)


v.add(9, diff_scene, [(0.3, "Model minus PDG"),
                      (3.5, "Σ⁰, Ξ⁰, Ω⁻ land within 15 MeV: a comparison, not a blind prediction")], "3 · Residuals")

v.add(7, end_card([("3 masses in → 3 fitted parameters", ORANGE),
                   ("3 other baryons: −12.83, +14.91, +9.44 MeV off", CYAN),
                   ("Code's own label: not a BCC or time-evolution simulation", DIM),
                   ("Δ value is a mixed-charge proxy, not a per-charge measurement", DIM)]))

def timeline():
    sc = scene_starts(v); a = [x["start"] for x in sc]
    return {"total": v.duration, "scenes": sc,
            "title": [0, a[1]],
            "inputs": [a[1] + 0.4 + 0.4 * i for i in range(3)], "fit_arrow": a[1] + 1.8,
            "outputs": [a[1] + 2.4 + 0.4 * i for i in range(3)],
            "baseline": [a[2] + 0.3, a[2] + 2.8], "spin": [a[2] + 4.0, a[2] + 6.0], "pdg": a[2] + 8.5,
            "split": a[2] + 9.5,
            "diff_bars": [a[3] + 0.3 + 0.3 * i for i in range(6)],
            "diff_signs": [1 if R[n]['difference_MeV'] >= 0 else -1 for n in NAMES],
            "end": a[4]}

if __name__ == "__main__":
    finish(v, "baryon_calculator", timeline(), os.path.join(OUT, "sfx_baryon_calculator.py"),
           thumb_t=4 + 9 + 13, audio_only="--audio-only" in sys.argv)
