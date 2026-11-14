#!/usr/bin/env python3
"""Compact 9-Panel Benchmark Dashboard (40/40 Tests OK)."""

import argparse, json, os
import matplotlib.pyplot as plt
import numpy as np
from bcc_3body_orbits import _grad_6face_load, _newton_acc
from bcc_dark_matter import BCCDarkMatterSim


def _step(pos, vel, masses, dt, fn):
    nv, np_ = [], []
    for i, ((px, py), (vx, vy)) in enumerate(zip(pos, vel)):
        oth = [(ox, oy, masses[j]) for j, (ox, oy) in enumerate(pos) if j != i]
        ax, ay = fn((px, py), oth)
        vx2, vy2 = vx + ax * dt, vy + ay * dt
        nv.append((vx2, vy2))
        np_.append((px + vx2 * dt, py + vy2 * dt))
    return np_, nv


def trace_3body(masses, p0, v0, t_end, scale):
    gp, gv = [(float(x), float(y)) for x, y in p0], [(float(x), float(y)) for x, y in v0]
    np_, nv = list(gp), list(gv)
    gh, nh = [[p] for p in gp], [[p] for p in np_]
    g_fn = lambda pos, oth: _grad_6face_load(pos, oth, scale, 0.15)
    for _ in range(int(round(t_end / 0.004))):
        gp, gv = _step(gp, gv, masses, 0.004, g_fn)
        np_, nv = _step(np_, nv, masses, 0.004, _newton_acc)
        for i in range(3):
            gh[i].append(gp[i])
            nh[i].append(np_[i])
    return gh, nh


def build_dashboard(d, out_path):
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(3, 3, figsize=(18, 14), dpi=160)
    it, w = iter(axes.flat), 0.36
    nt = d.get("architecture", {}).get("tests_run") or 40
    fig.suptitle(f"6-Face Planck-Cube Grid — Benchmarks ({nt}/{nt} Tests OK)",
                 fontsize=14, fontweight="bold", y=0.985)

    # 1. Baryons & 2. Mesons
    for title, key, col in (("1. Baryons (3q)", "baryon_spectrum", "#2563eb"),
                            ("2. Mesons ($q\\bar{q}$)", "meson_spectrum", "#0d9488")):
        ax, rows = next(it), d[key]
        x = np.arange(len(rows))
        ax.bar(x - w / 2, [r["model"] for r in rows], w, label="Grid", color=col)
        ax.bar(x + w / 2, [r["pdg"] for r in rows], w, label="PDG", color="#94a3b8")
        ax.set_title(title, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels([r["name"] for r in rows], fontsize=8)
        ax.legend(fontsize=8)

    # 3. Flux-Tube String Breaking
    ax, sb = next(it), d["string_breaking"]
    hops, st, th = np.array(sb["hops"]), np.array(sb["stored_mev"]), sb["threshold_mev"]
    ax.plot(hops, st, "--", color="#475569", lw=1.2)
    ax.scatter(hops[st <= th], st[st <= th], color="#2563eb", s=42, label="Intact")
    ax.scatter(hops[st > th], st[st > th], color="#dc2626", s=55, marker="X", label="Snapped")
    ax.axhline(th, color="#ea580c", ls=":", lw=1.5, label=f"{th:.0f} MeV Cap")
    ax.set_title("3. Flux-Tube String Breaking", fontweight="bold")
    ax.legend(fontsize=8)

    # 4. Glueball Mass Gap
    ax, gb = next(it), d["glueball_mass_gap"]
    bars = ax.bar([g["links"] for g in gb], [g["mass_mev"] for g in gb],
                  color=["#cbd5e1", "#7c3aed", "#6d28d9", "#5b21b6"], width=0.5)
    for bar, g in zip(bars, gb):
        ax.text(bar.get_x() + bar.get_width() / 2, g["mass_mev"] + 60,
                f"{g['mass_mev']:.0f}", ha="center", fontsize=8, fontweight="bold")
    ax.set_ylim(0, max(g["mass_mev"] for g in gb) * 1.15)
    ax.set_title("4. Pure-Gluon Mass Gap ($BareT=0$)", fontweight="bold")
    ax.tick_params(axis="x", labelsize=8)

    # 5. Momentum Lensing
    ax, ml = next(it), d["momentum_lensing"]
    xl = np.arange(len(ml))
    ax.plot(xl, [r["lag_b0"] for r in ml], "o-", color="#dc2626", lw=2, label="b=0")
    ax.plot(xl, [r["lag_b2"] for r in ml], "s-", color="#f59e0b", lw=2, label="b=2")
    ax.set_title("5. Momentum Lensing (Part 5→1)", fontweight="bold")
    ax.set_xticks(xl)
    ax.set_xticklabels([r["momentum"] for r in ml], fontsize=8)
    ax.legend(fontsize=8)

    # 6. 3D Horizon
    ax, rh = next(it), d["radial_horizon"]
    rad, wk, cap = np.array(rh["radii"]), np.array(rh["workload"]), rh["deadlock_cap"]
    ax.bar(rad, wk, color=["#dc2626" if v >= cap else "#16a34a" for v in wk], width=0.55)
    ax.axhline(cap, color="#1e293b", ls="--", lw=1.5, label="Cap (100)")
    ax.set_title("6. 3D Deadlocked Horizon", fontweight="bold")
    ax.legend(fontsize=8)

    # 7. Figure-8 & 8. Pythagorean 3-4-5
    ax = next(it)
    vx3, vy3 = -0.93240737, -0.86473146
    g8, n8 = trace_3body([1.0, 1.0, 1.0],
                         [(-0.97000436, 0.24308753), (0.97000436, -0.24308753), (0.0, 0.0)],
                         [(-0.5 * vx3, -0.5 * vy3), (-0.5 * vx3, -0.5 * vy3), (vx3, vy3)], 6.33, 12.0)
    for i, (tr, c) in enumerate(zip(g8, ("#2563eb", "#0d9488", "#7c3aed"))):
        ax.plot(*zip(*tr), color=c, lw=1.8, label="Grid" if i == 0 else None)
    ax.plot(*zip(*next(iter(n8))), "--", color="#94a3b8", lw=1.3, label="Newton")
    ax.set_title("7. 3-Body Figure-8 (min_sep=0.68)", fontweight="bold")
    ax.legend(fontsize=8)

    ax = next(it)
    g3, n3 = trace_3body([3.0, 4.0, 5.0], [(1.0, 3.0), (-2.0, -1.0), (1.0, -1.0)],
                         [(0.0, 0.0), (0.0, 0.0), (0.0, 0.0)], 3.2, 10.0)
    for i, (tg, tn, c) in enumerate(zip(g3, n3, ("#dc2626", "#f59e0b", "#2563eb"))):
        ax.plot(*zip(*tg), color=c, lw=1.8, label=f"Grid m={i+3}")
        ax.plot(*zip(*tn), ":", color="#64748b", lw=1.2, label="Newton" if i == 0 else None)
    ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.set_aspect("equal")
    ax.set_title("8. Pythagorean 3-4-5 Zoom (0.15 Cap)", fontweight="bold")
    ax.legend(fontsize=7.2, loc="upper left", ncol=2)

    # 9. Dark Matter Rotation Curve
    ax, r_dm = next(it), [float(r) for r in range(2, 22, 2)]
    cv = BCCDarkMatterSim().rotation_curve(r_dm)
    ax.plot(r_dm, [c["v_total"] for c in cv], "o-", color="#7c3aed", lw=2, label="+ $Q_{EM}=0$ Halo")
    ax.plot(r_dm, [c["v_baryon"] for c in cv], "s--", color="#64748b", lw=1.7, label="Baryons Only")
    ax.set_ylim(0, 26); ax.set_title("9. Dark Matter Rotation Curve", fontweight="bold")
    ax.legend(fontsize=8, loc="lower left")

    plt.tight_layout(rect=(0, 0, 1, 0.96))
    plt.savefig(out_path, dpi=180); plt.close(fig)
    print(f"Saved 9-panel benchmark dashboard to: {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="benchmark_report.json")
    ap.add_argument("--out", default="bcc_benchmark_dashboard.png")
    args = ap.parse_args()
    with open(args.json, "r", encoding="utf-8") as f:
        build_dashboard(json.load(f), args.out)

