#!/usr/bin/env python3
"""v2_sound (v4 suite, synthesized SFX): explainer video for bcc_em_wave_sim.py (module imported unchanged; the dipole
solver is copied only to keep its potential V for display, and asserted to
reproduce the module's printed residuals)."""
import sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from bccvid import *
import_src()
import numpy as np
import bcc_em_wave_sim as em

OUT = "/workspace/bcc_test4_videos/v2_sound/bcc_em_wave_sim"

class KeepV(em.BCCMaxwellGrid):
    def place_dipole_charges(self, pos_plus, pos_minus, q_mag=10.0, iterations=300):
        L = self.L
        V = [[[0.0] * L for _ in range(L)] for _ in range(L)]
        for node in self.rho: self.rho[node] = 0.0
        self.rho[pos_plus] = +q_mag; self.rho[pos_minus] = -q_mag
        for _ in range(iterations):
            nV = [[[0.0] * L for _ in range(L)] for _ in range(L)]
            for x in range(L):
                for y in range(L):
                    for z in range(L):
                        s = 0.0
                        for d in range(8):
                            nx, ny, nz = self.neighbor(x, y, z, d); s += V[nx][ny][nz]
                        nV[x][y][z] = (s + self.rho[(x, y, z)]) / 8.0
            V = nV
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    for d in range(8):
                        nx, ny, nz = self.neighbor(x, y, z, d)
                        self.E[(x, y, z)][d] = V[x][y][z] - V[nx][ny][nz]
        self.V = np.array(V)

mx = KeepV(L=10)
mx.place_dipole_charges((3, 5, 5), (7, 5, 5), q_mag=10.0)
g_static = mx.verify_gauss_law()
cur = (3, 5, 5); HOPS = [cur]
for d in (7, 3, 5):
    cur = mx.redraw_charge_step(cur, d, dq=10.0); HOPS.append(cur)
g_hop = mx.verify_gauss_law()
RES = [("static", g_static['max_gauss_residual']), ("after 3 hops", g_hop['max_gauss_residual']),
       ("global flux sum", g_hop['net_global_flux'])]
assert [f"{r:.2e}" for _, r in RES] == ["3.61e-16", "9.16e-16", "-1.39e-17"], RES
assert cur == (4, 6, 8)
VSL = mx.V[:, :, 5].T  # V[x][y][z] -> rows y, cols x

# ---- double slit: module class run unchanged, u_curr snapshot each tick ----
un = em.BCCDoubleSlitSim(width=36, height=45, barrier_x=10, slit_ys=(17, 27), wavelength_ticks=6)
ob = em.BCCDoubleSlitSim(width=36, height=45, barrier_x=10, slit_ys=(17, 27), wavelength_ticks=6,
                         detector_slit_y=17, seed=42)
FU, FO = [], []
for t in range(120):
    un.step_redraw_wave(t); ob.step_redraw_wave(t)
    FU.append(np.array(un.u_curr)); FO.append(np.array(ob.u_curr))
IU = [un.detector_intensity[y] / max(un.detector_intensity) for y in range(15, 30)]
IO = [ob.detector_intensity[y] / max(ob.detector_intensity) for y in range(15, 30)]
PR_U = [0.107, 0.477, 0.077, 0.229, 0.056, 0.734, 0.069, 0.978, 0.069, 0.734, 0.056, 0.229, 0.077, 0.477, 0.107]
PR_O = [0.461, 0.273, 1.000, 0.332, 0.470, 0.251, 0.229, 0.262, 0.183, 0.348, 0.121, 0.439, 0.112, 0.413, 0.085]
assert [round(x, 3) for x in IU] == PR_U and [round(x, 3) for x in IO] == PR_O

v = Video(OUT, "_silent", "bcc_test4 · bcc_em_wave_sim.py",
          "Toy model on an 8-neighbour BCC grid · numbers from the actual run of bcc_em_wave_sim.py")
v.add(4, title_card("Grid electromagnetism", "Gauss's law check · double slit with a which-slit sensor"))

def gauss(fig, t, T):
    ax = fig.add_axes([0.04, 0.17, 0.42, 0.68])
    m = np.abs(VSL).max() / 6
    ax.imshow(VSL, origin="lower", cmap="berlin", vmin=-m, vmax=m)
    ax.plot(3, 5, "o", ms=30, mfc="none", mec=RED, mew=3); ax.text(3, 6.1, "+10", color=RED, ha="center", fontsize=20)
    ax.plot(7, 5, "o", ms=30, mfc="none", mec=CYAN, mew=3); ax.text(7, 6.1, "−10", color=CYAN, ha="center", fontsize=20)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title("potential on slice z = 5 (10³ grid)", fontsize=17, color=DIM)
    b = style_ax(fig.add_axes([0.56, 0.22, 0.40, 0.58]))
    for i, (lab, r) in enumerate(RES):
        g = ramp(t, 1.5 + 1.2 * i, 0.8)
        if g > 0:
            val = abs(r)
            b.barh(i, np.log10(val) + 18, left=-18, color=GREEN, height=0.55, alpha=g)
            b.text(np.log10(val) + 0.3, i, f"{r:.2e}", va="center", fontsize=22, alpha=g)
    b.axvline(0, color=RED, lw=2); b.text(-0.3, 2.55, "1", color=RED, ha="right", fontsize=18)
    b.set_xlim(-18, 2); b.set_ylim(-0.6, 2.8); b.set_yticks(range(3)); b.set_yticklabels([l for l, _ in RES], fontsize=19, color=FG)
    b.invert_yaxis(); b.set_xlabel("log₁₀ |residual|", fontsize=16)
    b.set_title("Gauss's law residual (div E − ρ)", fontsize=18, color=FG)

v.add(13, gauss, [(0.3, "A ± charge pair on the grid"),
                  (3.0, "Residual stays at rounding level, even after the charge hops"),
                  (8.5, "Conservation is built into the link update")], "1 · Gauss's law")

def binned(F, k):
    # display only: intensity averaged over the last 6 ticks (one source period),
    # summed over x and x-1 like the module's two-sublattice detector bin
    acc = sum(F[i] ** 2 for i in range(max(0, k - 5), k + 1)) / 6.0
    b = acc.copy(); b[:, 1:] += acc[:, :-1]
    return b[:, 11:35]

from matplotlib.colors import PowerNorm
def field(fig, t, T):
    k = min(int(t / 10.5 * 119), 119)
    for j, (F, lab) in enumerate(((FU, "both slits, no sensor"), (FO, "sensor on slit at y = 17"))):
        ax = fig.add_axes([0.07 + 0.47 * j, 0.17, 0.40, 0.68])
        ax.imshow(binned(F, k), origin="lower", cmap="magma", norm=PowerNorm(0.5, vmin=0, vmax=1.5),
                  aspect="auto", extent=(10.5, 34.5, -0.5, 44.5))
        ax.plot([10.5] * 2, [-0.5, 44.5], color="#8b94a8", lw=6)
        for y in (17, 27):
            ax.plot(10.5, y, "s", ms=11, color=BG)
        if j == 1: ax.plot(10.5, 17, "s", ms=16, color=YELLOW)
        ax.axvline(32.5, color=GREEN, lw=2, ls="--")
        ax.set_xlim(9.8, 34.5); ax.set_ylim(-0.5, 44.5)
        ax.set_xticks([]); ax.set_yticks([17, 27]); ax.set_yticklabels(["slit 17", "slit 27"], fontsize=15)
        ax.set_title(lab, fontsize=20, color=YELLOW if j else FG)
    fig.text(0.5, 0.915, f"tick {k + 1} / 120 · wave intensity behind the barrier", ha="center", fontsize=18, color=DIM)

v.add(13, field, [(0.3, "A wave from the left passes two slits"),
                  (5.0, "Right: the sensor scrambles the phase at one slit"),
                  (9.0, "Screen (dashed green) sums intensity from tick 35 on")], "2 · Double slit")

def screen(fig, t, T):
    ys = list(range(15, 30))
    for j, (I, lab, col) in enumerate(((IU, "no sensor", CYAN), (IO, "with sensor", YELLOW))):
        ax = style_ax(fig.add_axes([0.10 + 0.46 * j, 0.18, 0.38, 0.64]))
        g = ramp(t, 0.4 + 1.5 * j, 1.2)
        ax.barh(ys, [x * g for x in I], color=col, height=0.75)
        ax.set_xlim(0, 1.05); ax.set_ylim(14.4, 29.6)
        ax.set_yticks(ys[::2]); ax.set_xlabel("normalised intensity", fontsize=16); ax.set_ylabel("screen row y", fontsize=16)
        ax.set_title(lab, fontsize=22, color=col)

v.add(10, screen, [(0.3, "No sensor: strong row-to-row alternation (2-row period)"),
                   (4.5, "With sensor: weaker, irregular pattern; peak at row 17")], "3 · Screen pattern")

v.add(7, end_card([("Gauss residual 3.61e-16 → 9.16e-16 after hops", GREEN),
                   ("Phase-scrambling one slit reshapes the screen pattern", YELLOW),
                   ("Not a clean single-slit envelope; toy wave rule", DIM),
                   ("Does not show Maxwell's equations emerge", DIM)]))

def timeline():
    sc = scene_starts(v); a = [x["start"] for x in sc]
    return {"total": v.duration, "scenes": sc, "title": [0, a[1]],
            "residuals": [a[1] + 1.5 + 1.2 * i for i in range(3)], "built_in": a[1] + 8.5,
            "slit": [a[2], a[2] + 13], "sensor": a[2] + 5.0, "screen_sum": a[2] + 9.0,
            "screen_bars": [a[3] + 0.4, a[3] + 1.9], "end": a[4]}

if __name__ == "__main__":
    finish(v, "bcc_em_wave_sim", timeline(), os.path.join(OUT, "sfx_bcc_em_wave_sim.py"),
           thumb_t=4 + 13 + 9, audio_only="--audio-only" in sys.argv)
