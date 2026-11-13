#!/usr/bin/env python3
"""v2_sound (v4 suite, synthesized SFX): explainer video for bcc_meson_sim.py (module imported unchanged)."""
import sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from bccvid import *
import_src()
import bcc_meson_sim as ms
from matplotlib.patches import Rectangle

OUT = "/workspace/bcc_test4_videos/v2_sound/bcc_meson_sim"
S = ms.BCCMesonSim()
SPEC = S.run_spectrum()
STR = S.simulate_flux_tube_stretch(max_hops=9)
PRINTED = {'pi': (140.00, 138.04, 1.96), 'rho': (780.00, 775.26, 4.74), 'K': (488.20, 495.64, -7.44),
           'K*': (897.27, 893.60, 3.67), 'phi': (1035.37, 1019.46, 15.91), 'D': (1764.00, 1867.20, -103.20),
           'D*': (1892.00, 2008.55, -116.55), 'J/psi': (3106.40, 3096.90, 9.50)}
for r in SPEC:
    assert (r['ModelMeV'], r['PDGMeV'], r['DiffMeV']) == PRINTED[r['name']], r['name']
assert STR['snapped_at_hop'] == 7 and STR['steps'][7]['tube_mev'] == 315.0
LAB = {'pi': 'π', 'rho': 'ρ', 'K': 'K', 'K*': 'K*', 'phi': 'φ', 'D': 'D', 'D*': 'D*', 'J/psi': 'J/ψ'}

v = Video(OUT, "_silent", "bcc_test4 · bcc_meson_sim.py",
          "Closed-form toy model · quark masses and couplings are hand-set inputs · numbers from the actual run")
v.add(4, title_card("Meson spectrum & flux tube", "Quark–antiquark pairs on the 6-face grid"))

def spec(fig, t, T):
    ax = style_ax(fig.add_axes([0.07, 0.18, 0.88, 0.66]))
    gr = ramp(t, 0.3, 2.5); gp = ramp(t, 4.0, 1.0); gd = ramp(t, 7.5, 0.8)
    for i, r in enumerate(SPEC):
        bad = abs(r['DiffMeV']) > 50
        col = RED if (bad and gd > 0) else CYAN
        ax.bar(i, r['ModelMeV'] * gr, width=0.6, color=col, alpha=0.75)
        if gp > 0:
            ax.plot(i, r['PDGMeV'], "D", ms=13, color=YELLOW, mec=BG, alpha=gp)
        if gd > 0:
            ax.text(i, max(r['ModelMeV'], r['PDGMeV']) + 70, f"{r['DiffMeV']:+.2f}", ha="center", fontsize=18,
                    color=RED if bad else FG, alpha=gd)
    ax.set_xticks(range(8)); ax.set_xticklabels([LAB[r['name']] for r in SPEC], fontsize=26, color=FG)
    ax.set_ylim(0, 3800); ax.set_ylabel("MeV", fontsize=18)
    ax.plot([], [], "s", color=CYAN, ms=14, label="model"); ax.plot([], [], "D", color=YELLOW, ms=11, label="PDG")
    ax.legend(loc="upper left", frameon=False, fontsize=18)
    ax.text(0.45, 0.97, f"hand-set inputs: u/d = {ms.QUARK_MASS_MEV['l']:.0f},  s = {ms.QUARK_MASS_MEV['s']:.0f},  c = {ms.QUARK_MASS_MEV['c']:.0f} MeV",
            transform=ax.transAxes, ha="center", va="top", fontsize=18, color=DIM)

v.add(16, spec, [(0.3, "Model mass = quark masses + spin term"),
                 (4.0, "◆ = PDG value"),
                 (7.5, "Six of eight within 16 MeV"),
                 (11.5, "D and D* miss by about 100 MeV")], "1 · Ground-state spectrum")

PAIRS = [(0, 1), (2, 3), (5, 6)]
def hyper(fig, t, T):
    ax = style_ax(fig.add_axes([0.10, 0.20, 0.80, 0.62]))
    xs = []
    for j, (a, b) in enumerate(PAIRS):
        for k, idx in enumerate((a, b)):
            r = SPEC[idx]; x = j * 3 + k; xs.append((x, LAB[r['name']]))
            g = ramp(t, 0.4 + 0.5 * j, 0.8)
            ax.bar(x, r['SpinT'] * g, width=0.7, color=GREEN if r['SpinT'] < 0 else ORANGE)
            if g > 0.9:
                ax.text(x, r['SpinT'] + (4 if r['SpinT'] > 0 else -4), f"{r['SpinT']:+.2f}", ha="center",
                        va="bottom" if r['SpinT'] > 0 else "top", fontsize=18)
    ax.axhline(0, color=FG, lw=1.2)
    ax.set_xticks([x for x, _ in xs]); ax.set_xticklabels([l for _, l in xs], fontsize=24, color=FG)
    ax.set_ylim(-120, 60); ax.set_ylabel("spin term (ticks)", fontsize=18)
    for j, lab in enumerate(["spin 0 vs 1", "", ""]):
        pass

v.add(10, hyper, [(0.3, "Spin 0 pushes down, spin 1 pushes up"),
                  (4.5, "The 3 : 1 ratio is built into the rule"),
                  (7.5, "Heavier quarks → smaller split (1/m₁m₂ by rule)")], "2 · Spin splitting")

def tube(fig, t, T):
    hop_t = 0.8  # seconds per hop
    h = min(int(max(t - 0.6, 0) / hop_t), 7)
    stp = STR['steps'][h]
    snapped = stp['broken']
    ax = fig.add_axes([0.05, 0.42, 0.90, 0.36]); ax.axis("off")
    ax.set_xlim(-1, 13); ax.set_ylim(-1.5, 1.5)
    for i in range(12):
        ax.add_patch(Rectangle((i - 0.5, -0.5), 1, 1, fc=PANEL, ec=GRID, lw=1.5))
    qx, qbx = 1, 1 + h
    if not snapped:
        ax.plot([qx, qbx], [0, 0], color=VIOLET, lw=10, alpha=0.8, solid_capstyle="round")
        ax.plot(qx, 0, "o", ms=34, color=RED, mec=FG); ax.plot(qbx, 0, "o", ms=34, color=CYAN, mec=FG)
    else:
        mid = (qx + qbx) / 2
        ax.plot([qx, mid - 0.6], [0, 0], color=VIOLET, lw=10, alpha=0.8)
        ax.plot([mid + 0.6, qbx], [0, 0], color=VIOLET, lw=10, alpha=0.8)
        for x, c in ((qx, RED), (mid - 0.6, CYAN), (mid + 0.6, RED), (qbx, CYAN)):
            ax.plot(x, 0, "o", ms=34, color=c, mec=FG)
        ax.text(mid, 1.0, "SNAPPED → 2 mesons", ha="center", fontsize=26, color=YELLOW, weight="bold")
    ax.text(-0.9, -1.25, f"hops: {h}", fontsize=24)
    b = style_ax(fig.add_axes([0.10, 0.17, 0.80, 0.18]))
    b.barh(0, stp['tube_mev'], color=YELLOW if snapped else VIOLET, height=0.6)
    b.axvline(STR['threshold_mev'], color=RED, lw=3)
    b.text(STR['threshold_mev'] + 5, 0.42, f"threshold {STR['threshold_mev']:.0f} MeV", color=RED, fontsize=17)
    b.text(stp['tube_mev'] + 5, 0, f"{stp['tube_mev']:.0f} MeV", va="center", fontsize=20)
    b.set_xlim(0, 360); b.set_yticks([]); b.set_ylim(-0.6, 0.9); b.set_xlabel("energy stored in tube", fontsize=16)

v.add(14, tube, [(0.3, "Pull the pair apart: +45 MeV per hop (set by rule)"),
                 (6.3, "Hop 7: 315 MeV passes the 275 MeV threshold"),
                 (9.0, "Tube breaks into two pairs (threshold is an input)")], "3 · Flux tube")

v.add(7, end_card([("Quark masses 310 / 485 / 1550 MeV are hand-set", DIM),
                   ("6 of 8 mesons within 16 MeV; D, D* off by −103, −117", CYAN),
                   ("3 : 1 spin split and 45 MeV/hop are rule inputs", ORANGE),
                   ("Breaking at 7 hops follows from 7 × 45 > 275", YELLOW)]))

def timeline():
    sc = scene_starts(v); a = [x["start"] for x in sc]
    hop_t = [a[3] + 0.6 + 0.8 * h for h in range(1, 8)]
    return {"total": v.duration, "scenes": sc, "title": [0, a[1]],
            "spec_rise": [a[1] + 0.3, a[1] + 2.8], "pdg": a[1] + 4.0, "diffs": a[1] + 7.5, "bad": a[1] + 11.5,
            "hyper": [[a[2] + 0.4 + 0.5 * j, SPEC[i]['SpinT']] for j, (p, q) in enumerate(PAIRS) for i in (p, q)],
            "hops": hop_t, "energies": [STR['steps'][h]['tube_mev'] for h in range(1, 8)],
            "snap": hop_t[-1], "end": a[4]}

if __name__ == "__main__":
    finish(v, "bcc_meson_sim", timeline(), os.path.join(OUT, "sfx_bcc_meson_sim.py"),
           thumb_t=4 + 16 + 10 + 9, audio_only="--audio-only" in sys.argv)
