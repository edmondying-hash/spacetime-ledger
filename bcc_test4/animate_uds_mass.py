#!/usr/bin/env python3
"""3-Act Animation: uds (Lambda^0) Bare Valence Quarks -> Gluon-Dressed Baryon Mass."""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def _generate_hop_path(n_frames, seed=7):
    """Generate deterministic orthogonal 1-hop quark trajectories on an 8x8 grid."""
    rng = np.random.default_rng(seed)
    u_pos, d_pos, s_pos = (2, 6), (6, 6), (4, 2)
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1), (0, 0))
    path = []
    for f in range(n_frames):
        if f >= 50 and f % 4 == 0:
            ux, uy = u_pos
            dx, dy = d_pos
            sx, sy = s_pos
            dux, duy = dirs[int(rng.integers(0, len(dirs)))]
            ddx, ddy = dirs[int(rng.integers(0, len(dirs)))]
            # Strange quark redraws slower (heavier lag on 6-face grid)
            dsx, dsy = dirs[int(rng.integers(0, len(dirs)))] if f % 8 == 0 else (0, 0)
            u_pos = (int(np.clip(ux + dux, 1, 6)), int(np.clip(uy + duy, 1, 6)))
            d_pos = (int(np.clip(dx + ddx, 1, 6)), int(np.clip(dy + ddy, 1, 6)))
            s_pos = (int(np.clip(sx + dsx, 1, 6)), int(np.clip(sy + dsy, 1, 6)))
        path.append((u_pos, d_pos, s_pos))
    return path


def build_animation(out_path="uds_gluon_mass_jump.mp4", fps=20):
    n_frames = 240  # 12 seconds at 20 fps
    path = _generate_hop_path(n_frames)

    plt.rcParams.update({"font.sans-serif": "DejaVu Sans", "axes.edgecolor": "#334155"})
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 6.2), dpi=140, facecolor="#0b0f19")
    ax_grid, ax_meter, ax_comp = axes
    for ax in axes:
        ax.set_facecolor("#111827")
        ax.tick_params(colors="#cbd5e1", labelsize=8.5)

    # Top title & transparent TOY MODEL footer matching your video aesthetic
    fig.suptitle("6-Face Planck Grid  •  uds (Λ⁰) Bare Quarks vs. Gluon-Dressed Mass",
                 color="#f8fafc", fontsize=13.5, fontweight="bold", y=0.96)
    subtitle = fig.text(0.5, 0.905, "ACT 1: Bare Valence Quarks Only (Gluon Routing OFF)",
                        ha="center", color="#38bdf8", fontsize=10.5, fontweight="bold")
    fig.text(0.5, 0.025,
             "TOY MODEL • Grid ticks from bcc_unified_sim.py (BareT=103.0, RouteT=534.9, SpinT=-6.2) • PDG Λ⁰ = 1115.68 MeV",
             ha="center", color="#94a3b8", fontsize=8)

    # Panel 1: 8x8 Planck-Cube Slice
    ax_grid.set_xlim(-0.5, 7.5)
    ax_grid.set_ylim(-0.5, 7.5)
    ax_grid.set_xticks(range(8))
    ax_grid.set_yticks(range(8))
    ax_grid.grid(True, color="#1e293b", lw=0.9)
    ax_grid.set_aspect("equal")
    ax_grid.set_title("1. 8³ Lattice Slice (x–y view)", color="#e2e8f0", fontsize=10, fontweight="bold")

    link_u, = ax_grid.plot([], [], color="#a855f7", lw=2.6, alpha=0.85, zorder=2)
    link_d, = ax_grid.plot([], [], color="#a855f7", lw=2.6, alpha=0.85, zorder=2)
    link_s, = ax_grid.plot([], [], color="#ec4899", lw=2.6, alpha=0.85, zorder=2)
    pulse_pts = ax_grid.scatter([], [], color="#f0abfc", s=34, zorder=3)
    steiner_pt = ax_grid.scatter([], [], color="#c084fc", marker="D", s=55, zorder=4)

    u_dot = ax_grid.scatter([], [], color="#38bdf8", s=210, edgecolor="white", lw=1.2, zorder=5, label="u (light)")
    d_dot = ax_grid.scatter([], [], color="#fbbf24", s=210, edgecolor="white", lw=1.2, zorder=5, label="d (light)")
    s_dot = ax_grid.scatter([], [], color="#f43f5e", s=260, edgecolor="white", lw=1.2, zorder=5, label="s (strange)")
    ax_grid.legend(loc="lower left", facecolor="#0f172a", edgecolor="#334155", labelcolor="#e2e8f0", fontsize=8)
    grid_note = ax_grid.text(3.5, 7.05, "Links: 0 (Static Bare Quarks)", ha="center", color="#94a3b8", fontsize=8.5)

    # Panel 2: Live Stacked Mass Jump Meter
    ax_meter.set_xlim(-0.6, 0.6)
    ax_meter.set_ylim(0, 760)
    ax_meter.grid(True, axis="y", color="#1e293b", lw=0.8)
    ax_meter.set_xticks([])
    ax_meter.set_ylabel("Grid Ticks / Cycle  (1 tick ≈ 1.77 MeV)", color="#cbd5e1", fontsize=9)
    ax_meter.set_title("2. Λ⁰ (uds) Total Mass Jump", color="#e2e8f0", fontsize=10, fontweight="bold")

    bar_bare = ax_meter.bar(["Λ⁰ (uds)"], [103.0], width=0.45, color="#f43f5e", label="Bare Valence (103.0)")
    bar_route = ax_meter.bar(["Λ⁰ (uds)"], [0.0], bottom=[103.0], width=0.45, color="#8b5cf6", label="Gluon Routing (+534.9)")
    bar_spin = ax_meter.bar(["Λ⁰ (uds)"], [0.0], bottom=[103.0], width=0.45, color="#10b981", label="u–d Spin Pair (-6.2)")
    ax_meter.legend(loc="upper left", facecolor="#0f172a", edgecolor="#334155", labelcolor="#e2e8f0", fontsize=7.8)
    mass_readout = ax_meter.text(0.0, 125.0, "103.0 ticks\n(~100 MeV bare)",
                                 ha="center", va="bottom", color="#f8fafc", fontsize=10, fontweight="bold")

    # Panel 3: Baryon Family Comparison (Act 3)
    ax_comp.set_xlim(-0.5, 2.5)
    ax_comp.set_ylim(0, 950)
    ax_comp.grid(True, axis="y", color="#1e293b", lw=0.8)
    ax_comp.set_xticks((0, 1, 2))
    ax_comp.set_xticklabels(("p (uud)\n938.9 MeV", "Λ⁰ (uds)\n1115.7 MeV", "Ω⁻ (sss)\n1681.9 MeV"), fontsize=8.5)
    ax_comp.set_title("3. Constant Gluon Sea Across Baryons", color="#e2e8f0", fontsize=10, fontweight="bold")

    fam_bare = (12.0, 103.0, 285.0)
    fam_tot = (544.65, 631.75, 821.23)
    comp_b = ax_comp.bar((0, 1, 2), (0.0, 0.0, 0.0), width=0.48, color="#f43f5e", label="Bare Valence")
    comp_g = ax_comp.bar((0, 1, 2), (0.0, 0.0, 0.0), bottom=(0.0, 0.0, 0.0), width=0.48, color="#8b5cf6", label="Gluon + Spin")
    ax_comp.legend(loc="upper left", facecolor="#0f172a", edgecolor="#334155", labelcolor="#e2e8f0", fontsize=7.8)

    def update(frame):
        (ux, uy), (dx, dy), (sx, sy) = path[frame]
        u_dot.set_offsets([[ux, uy]])
        d_dot.set_offsets([[dx, dy]])
        s_dot.set_offsets([[sx, sy]])

        # Act 1 (0..49): Bare only | Act 2 (50..169): Gluon ramp | Act 3 (170..239): Family compare
        if frame < 50:
            ramp = 0.0
            subtitle.set_text("ACT 1: Bare Valence Quarks Only — Gluon Routing Links OFF")
            subtitle.set_color("#38bdf8")
        elif frame < 170:
            ramp = min(1.0, (frame - 50) / 95.0)
            subtitle.set_text("ACT 2: Gluon Flux Links Kick In — Dynamic Routing Generates ~84% of Mass!")
            subtitle.set_color("#c084fc")
        else:
            ramp = 1.0
            subtitle.set_text("ACT 3: Gluon Routing Sea (~535 ticks) Dominates Across All Light & Strange Baryons")
            subtitle.set_color("#34d399")

        if ramp > 0.0:
            jx, jy = (ux + dx + sx) / 3.0, (uy + dy + sy) / 3.0
            link_u.set_data((ux, jx), (uy, jy))
            link_d.set_data((dx, jx), (dy, jy))
            link_s.set_data((sx, jx), (sy, jy))
            steiner_pt.set_offsets([[jx, jy]])
            t_pulse = (frame % 10) / 10.0
            pxs = (ux + (jx - ux) * t_pulse, dx + (jx - dx) * t_pulse, sx + (jx - sx) * t_pulse)
            pys = (uy + (jy - uy) * t_pulse, dy + (jy - dy) * t_pulse, sy + (jy - sy) * t_pulse)
            pulse_pts.set_offsets(np.column_stack((pxs, pys)))
            manh = abs(ux - dx) + abs(uy - dy) + abs(sx - jx) + abs(sy - jy)
            grid_note.set_text(f"Steiner Flux Links Active • Span: {manh:.1f} hops")
            grid_note.set_color("#e879f9")
        else:
            link_u.set_data([], [])
            link_d.set_data([], [])
            link_s.set_data([], [])
            steiner_pt.set_offsets(np.empty((0, 2)))
            pulse_pts.set_offsets(np.empty((0, 2)))
            grid_note.set_text("Links: OFF (Static Bare Quarks)")
            grid_note.set_color("#94a3b8")

        r_ticks = 534.9 * ramp
        s_ticks = -6.2 * ramp
        tot_ticks = 103.0 + r_ticks + s_ticks
        mev_est = 100.0 + (1115.68 - 100.0) * ramp

        for rect in bar_route:
            rect.set_height(r_ticks)
        for rect in bar_spin:
            rect.set_y(103.0 + r_ticks + s_ticks)
            rect.set_height(abs(s_ticks))

        mass_readout.set_y(tot_ticks + 18.0)
        mass_readout.set_text(f"{tot_ticks:.2f} ticks\n({mev_est:.1f} MeV)")

        c_ramp = min(1.0, max(0.0, (frame - 165) / 45.0))
        for rect_b, rect_g, b_val, t_val in zip(comp_b, comp_g, fam_bare, fam_tot):
            hb = b_val * c_ramp
            hg = (t_val - b_val) * c_ramp
            rect_b.set_height(hb)
            rect_g.set_y(hb)
            rect_g.set_height(hg)

        return (link_u, link_d, link_s, pulse_pts, steiner_pt, u_dot, d_dot, s_dot,
                grid_note, mass_readout, subtitle)

    plt.tight_layout(rect=(0.01, 0.05, 0.99, 0.88))
    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000 // fps, blit=False)

    try:
        anim.save(out_path, writer="ffmpeg", fps=fps, dpi=140)
        print(f"Saved MP4 animation to: {out_path}")
    except Exception:
        gif_path = out_path.rsplit(".", 1).pop(0) + ".gif"
        anim.save(gif_path, writer=PillowWriter(fps=fps))
        print(f"ffmpeg not found; saved animated GIF to: {gif_path}")
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="uds_gluon_mass_jump.mp4")
    ap.add_argument("--fps", type=int, default=20)
    args = ap.parse_args()
    build_animation(args.out, args.fps)

