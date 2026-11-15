#!/usr/bin/env python3
"""
Render a 3-Panel Animated GIF (dirac4_planck_cube.gif) of Dirac4 on the 6-Face Planck Cube:
  1. 720-degree Spin-1/2 Double-Cover Phase Rotor (360 deg -> -psi, 720 deg -> +psi)
  2. Rest-Mass Zitterbewegung Chiral Oscillation (P(L) <-> P(R), |psi|^2 = 1)
  3. Chiral Wave-Packet Ratchet Along Orthogonal +x Cube Faces
"""

import cmath
import math
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def build_dirac4_animation(out_gif: str = "dirac4_planck_cube.gif") -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    frames = 48
    grid_len = 25
    center = 6

    # Precompute split-step chiral wave-packet history across 48 ticks (repeating/evolving)
    theta_m = 0.28
    c_m, s_m = math.cos(theta_m), math.sin(theta_m)
    k_mom = 0.55

    def init_packet():
        pr = [0.0j] * grid_len
        pl = [0.0j] * grid_len
        for dx in (-1, 0, 1):
            pr[center + dx] = math.exp(-0.5 * (dx ** 2)) * cmath.exp(1j * k_mom * dx)
        norm0 = math.sqrt(sum(abs(a) ** 2 + abs(b) ** 2 for a, b in zip(pr, pl)))
        return [a / norm0 for a in pr], [b / norm0 for b in pl]

    psi_r, psi_l = init_packet()
    wp_history = []
    for f in range(frames):
        if f > 0 and f % 16 == 0:
            psi_r, psi_l = init_packet()
        elif f > 0:
            mix_r = [c_m * r - 1j * s_m * l for r, l in zip(psi_r, psi_l)]
            mix_l = [-1j * s_m * r + c_m * l for r, l in zip(psi_r, psi_l)]
            nxt_r, nxt_l = [0.0j] * grid_len, [0.0j] * grid_len
            for x in range(1, grid_len - 1):
                nxt_r[x + 1] = mix_r[x]
                nxt_l[x - 1] = mix_l[x]
            psi_r, psi_l = nxt_r, nxt_l
        prob_r = np.array([abs(r) ** 2 for r in psi_r])
        prob_l = np.array([abs(l) ** 2 for l in psi_l])
        mean_x = float(np.sum(np.arange(grid_len) * (prob_r + prob_l)))
        wp_history.append((f % 16, prob_r, prob_l, mean_x))

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.5, 4.8), dpi=130)
    fig.suptitle("Dirac4 Spinor on the 6-Face Planck Cube — Spin-1/2 Double Cover, Zitterbewegung & +x Transport",
                 fontsize=12.5, fontweight="bold", y=0.98)

    xs = np.arange(grid_len)

    def update(frame: int):
        ax1.clear(); ax2.clear(); ax3.clear()

        # Panel 1: 720-degree double cover (0 -> 720 deg across 48 frames)
        deg = (720.0 * frame) / frames
        rad_half = math.radians(0.5 * deg)
        px, py = math.cos(rad_half), -math.sin(rad_half)
        circle = plt.Circle((0, 0), 1.0, color="#cbd5e1", fill=False, lw=2)
        ax1.add_patch(circle)
        col_arrow = "#dc2626"
        ax1.set_title(f"1. 720° Double Cover\nCube Turn: {deg:5.1f}° | {sign_txt}", fontweight="bold", fontsize=10)
        ax1.set_xlabel("Re<ψ|ψ'>"); ax1.set_ylabel("Im<ψ|ψ'>")

        # Panel 2: Rest-Mass Zitterbewegung (L <-> R oscillation)
        t_now = (2.0 * math.pi * frame) / frames
        p_l = math.cos(t_now) ** 2
        p_r = math.sin(t_now) ** 2
        bars = ax2.bar(["Left ψ_L", "Right ψ_R", "Total |ψ|²"], [p_l, p_r, p_l + p_r],
                       color=["#2563eb", "#dc2626", "#16a34a"], width=0.52)
        for b, val in zip(bars, [p_l, p_r, p_l + p_r]):
            ax2.text(b.get_x() + b.get_width() / 2, val + 0.04, f"{val:.2f}", ha="center", fontsize=8.5, fontweight="bold")
        ax2.set_ylim(0, 1.22)
        ax2.set_title(f"2. Rest-Mass Zitterbewegung\nγ⁰ Chiral Swap (ωt = {t_now:.2f} rad)", fontweight="bold", fontsize=10)
        ax2.set_ylabel("Probability Density")

        # Panel 3: Orthogonal +x Cube Face Wave-Packet Transport
        tick, pr, pl, mx = wp_history[frame]
        ax3.bar(xs, pr, color="#2563eb", alpha=0.85, label="Right +x |ψ_R|²")
        ax3.bar(xs, pl, bottom=pr, color="#dc2626", alpha=0.85, label="Left -x |ψ_L|²")
        ax3.axvline(mx, color="#1e293b", ls="--", lw=1.6, label=f"Centroid <x>={mx - center:+.2f}")
        ax3.set_xlim(2, grid_len - 2); ax3.set_ylim(0, 0.72)
        ax3.set_title(f"3. +x Cube-Face Chiral Walk\nTick = {tick:2d} | Group Speed v_g < c", fontweight="bold", fontsize=10)
        ax3.set_xlabel("Planck Cube Coordinate x (l_P)")
        ax3.legend(fontsize=7.5, loc="upper right")

        fig.tight_layout(rect=[0, 0, 1, 0.92])

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=110)
    ani.save(out_gif, writer="pillow", fps=9)
    plt.close(fig)
    print(f"Saved Dirac4 animation to: {out_gif}")


if __name__ == "__main__":
    build_dirac4_animation()
