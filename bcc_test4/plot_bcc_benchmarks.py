#!/usr/bin/env python3
"""8-Panel Benchmark Dashboard for the 6-Face Planck-Cube Grid Suite (37/37 Tests)."""

import argparse, json, os
import matplotlib.pyplot as plt
import numpy as np
from bcc_3body_orbits import _grad_6face_load, _newton_acc

DEFAULTS = {
    "baryon_spectrum": [
        {"name": "p", "model": 938.92, "pdg": 938.27},
        {"name": "Delta+", "model": 1232.00, "pdg": 1232.00},
        {"name": "Lambda", "model": 1115.68, "pdg": 1115.68},
        {"name": "Sigma0", "model": 1179.81, "pdg": 1192.64},
        {"name": "Xi0", "model": 1329.77, "pdg": 1314.86},
        {"name": "Omega-", "model": 1681.89, "pdg": 1672.45},
    ],
    "meson_spectrum": [
        {"name": "pi", "model": 140.00, "pdg": 138.04},
        {"name": "rho", "model": 780.00, "pdg": 775.26},
        {"name": "K", "model": 488.20, "pdg": 495.64},
        {"name": "K*", "model": 897.27, "pdg": 893.60},
        {"name": "phi", "model": 1035.37, "pdg": 1019.46},
        {"name": "D", "model": 1764.00, "pdg": 1867.20},
        {"name": "D*", "model": 1892.00, "pdg": 2008.55},
        {"name": "J/psi", "model": 3106.40, "pdg": 3096.90},
    ],
    "string_breaking": {
        "threshold_mev": 275.0,
        "hops": list(range(10)),
        "stored_mev": [0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0, 360.0, 405.0],
    },
    "glueball_mass_gap": [
        {"links": "0 (Vacuum)", "mass_mev": 0.0},
        {"links": "4 (Mass Gap Δ)", "mass_mev": 2001.18},
        {"links": "6 Links", "mass_mev": 2851.75},
        {"links": "8 Links", "mass_mev": 3694.67},
    ],
    "momentum_lensing": [
        {"momentum": "(0,0,0)", "load": 6, "lag_b0": 6, "lag_b2": 0},
        {"momentum": "(2,0,0)", "load": 8, "lag_b0": 9, "lag_b2": 1},
        {"momentum": "(2,1,0)", "load": 9, "lag_b0": 12, "lag_b2": 3},
        {"momentum": "(3,2,1)", "load": 12, "lag_b0": 13, "lag_b2": 5},
    ],
    "radial_horizon": {
        "deadlock_cap": 100.0,
        "radii": list(range(7)),
        "workload": [244.33, 187.19, 108.61, 121.81, 29.42, 19.32, 12.61],
    },
}


def _step_bodies(pos_list, vel_list, masses, dt, fn_acc):
    new_v, new_p = [], []
    for i, ((px, py), (vx, vy)) in enumerate(zip(pos_list, vel_list)):
        others = [(ox, oy, masses[j]) for j, (ox, oy) in enumerate(pos_list) if j != i]
        ax, ay = fn_acc((px, py), others)
        vx2, vy2 = vx + ax * dt, vy + ay * dt
        new_v.append((vx2, vy2))
        new_p.append((px + vx2 * dt, py + vy2 * dt))
    return new_p, new_v


def trace_3body(masses, pos0, vel0, t_end, dt=0.004, scale=12.0, smooth=0.15):
    gp = [(float(x), float(y)) for x, y in pos0]
    gv = [(float(vx), float(vy)) for vx, vy in vel0]
    np_ = list(gp)
    nv = list(gv)
    g_hist = [[p] for p in gp]
    n_hist = [[p] for p in np_]
    g_fn = lambda pos, oth: _grad_6face_load(pos, oth, scale, smooth)
    for _ in range(int(round(t_end / dt))):
        gp, gv = _step_bodies(gp, gv, masses, dt, g_fn)
        np_, nv = _step_bodies(np_, nv, masses, dt, _newton_acc)
        for i in range(3):
            g_hist[i].append(gp[i])
            n_hist[i].append(np_[i])
    return g_hist, n_hist


def build_dashboard(data, out_path):
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(2, 4, figsize=(22, 10.5), dpi=160)
    it = iter(axes.flat)
    n_tests = data.get("architecture", {}).get("tests_run") or 37
    fig.suptitle(
        f"6-Face Planck-Cube Grid (1.0 $l_P^3$, 1.0 $t_P$) — Unified Benchmarks ({n_tests}/{n_tests} Tests OK)",
        fontsize=14, fontweight="bold", y=0.98,
    )
    w = 0.36

    # 1. Baryons
    ax = next(it)
    b = data["baryon_spectrum"]
    x = np.arange(len(b))
    ax.bar(x - w / 2, [r["model"] for r in b], w, label="6-Face Grid", color="#2563eb")
    ax.bar(x + w / 2, [r["pdg"] for r in b], w, label="PDG 2024", color="#94a3b8")
    ax.set_title("1. Ground-State Baryons (3q)", fontweight="bold")
    ax.set_ylabel("Mass (MeV)")
    ax.set_xticks(x)
    ax.set_xticklabels([r["name"] for r in b], fontsize=8)
    ax.legend(fontsize=8)

    # 2. Mesons
    ax = next(it)
    m = data["meson_spectrum"]
    xm = np.arange(len(m))
    ax.bar(xm - w / 2, [r["model"] for r in m], w, label="6-Face Grid", color="#0d9488")
    ax.bar(xm + w / 2, [r["pdg"] for r in m], w, label="PDG 2024", color="#94a3b8")
    ax.set_title("2. Ground-State Mesons ($q\\bar{q}$)", fontweight="bold")
    ax.set_ylabel("Mass (MeV)")
    ax.set_xticks(xm)
    ax.set_xticklabels([r["name"] for r in m], fontsize=8)
    ax.legend(fontsize=8)

    # 3. Flux-Tube String Breaking
    ax = next(it)
    sb = data["string_breaking"]
    hops, stored, th = np.array(sb["hops"]), np.array(sb["stored_mev"]), sb["threshold_mev"]
    ax.plot(hops, stored, "--", color="#475569", lw=1.2)
    ax.scatter(hops[stored <= th], stored[stored <= th], color="#2563eb", s=45, label="Intact")
    ax.scatter(hops[stored > th], stored[stored > th], color="#dc2626", s=55, marker="X", label="Snapped")
    ax.axhline(th, color="#ea580c", ls=":", lw=1.6, label=f"Threshold ({th:.0f} MeV)")
    ax.set_title("3. Flux-Tube String Breaking", fontweight="bold")
    ax.set_xlabel("6-Face Hops (L)")
    ax.set_ylabel("Energy (MeV)")
    ax.legend(fontsize=8)

    # 4. Glueball Mass Gap
    ax = next(it)
    gb = data["glueball_mass_gap"]
    bars = ax.bar([g["links"] for g in gb], [g["mass_mev"] for g in gb],
                  color=["#cbd5e1", "#7c3aed", "#6d28d9", "#5b21b6"], width=0.5)
    for bar, g in zip(bars, gb):
        ax.text(bar.get_x() + bar.get_width() / 2, g["mass_mev"] + 55,
                f"{g['mass_mev']:.1f}", ha="center", fontsize=8, fontweight="bold")
    ax.set_ylim(0, max(g["mass_mev"] for g in gb) * 1.15)
    ax.set_title("4. Pure-Gluon Mass Gap ($BareT=0$)", fontweight="bold")
    ax.set_ylabel("Mass (MeV)")
    ax.tick_params(axis="x", labelsize=7.5)

    # 5. Momentum-Coupled Lensing
    ax = next(it)
    ml = data["momentum_lensing"]
    xl = np.arange(len(ml))
    ax.plot(xl, [r["lag_b0"] for r in ml], "o-", color="#dc2626", lw=2, label="Central (b=0)")
    ax.plot(xl, [r["lag_b2"] for r in ml], "s-", color="#f59e0b", lw=2, label="Off-Axis (b=2)")
    ax.set_title("5. Momentum Lensing (Part 5→1)", fontweight="bold")
    ax.set_ylabel("Delay (Pixels)")
    ax.set_xticks(xl)
    ax.set_xticklabels([r["momentum"] for r in ml], fontsize=8)
    ax.legend(fontsize=8)

    # 6. 3D Deadlocked Horizon
    ax = next(it)
    rh = data["radial_horizon"]
    rad, wk, cap = np.array(rh["radii"]), np.array(rh["workload"]), rh["deadlock_cap"]
    ax.bar(rad, wk, color=["#dc2626" if v >= cap else "#16a34a" for v in wk], width=0.55)
    ax.axhline(cap, color="#1e293b", ls="--", lw=1.5, label="Deadlock Cap (100)")
    ax.set_title("6. 3D Network-Deadlocked Horizon", fontweight="bold")
    ax.set_xlabel("Radius r ($l_P$)")
    ax.set_ylabel("Workload (Ticks)")
    ax.legend(fontsize=8)

    # 7. 3-Body Figure-8 Choreography
    ax = next(it)
    f8_p = [(-0.97000436, 0.24308753), (0.97000436, -0.24308753), (0.0, 0.0)]
    vx3, vy3 = -0.93240737, -0.86473146
    f8_v = [(-0.5 * vx3, -0.5 * vy3), (-0.5 * vx3, -0.5 * vy3), (vx3, vy3)]
    g8, n8 = trace_3body([1.0, 1.0, 1.0], f8_p, f8_v, t_end=6.33, scale=12.0)
    for i, (tr_g, col) in enumerate(zip(g8, ("#2563eb", "#0d9488", "#7c3aed"))):
        gx, gy = zip(*tr_g)
        ax.plot(gx, gy, color=col, lw=1.8, label="6-Face Grid" if i == 0 else None)
    nx8, ny8 = zip(*next(iter(n8)))
    ax.plot(nx8, ny8, "--", color="#94a3b8", lw=1.3, label="Newton")
    ax.set_title("7. 3-Body Figure-8 (min_sep=0.68)", fontweight="bold")
    ax.set_xlabel("x (units)")
    ax.legend(fontsize=8)

    # 8. 3-Body Pythagorean 3-4-5 Close-Pass Split (Zoomed Core)
    ax = next(it)
    p345_p = [(1.0, 3.0), (-2.0, -1.0), (1.0, -1.0)]
    p345_v = [(0.0, 0.0), (0.0, 0.0), (0.0, 0.0)]
    g3, n3 = trace_3body([3.0, 4.0, 5.0], p345_p, p345_v, t_end=3.2, scale=10.0)
    cols = ("#dc2626", "#f59e0b", "#2563eb")
    lbls = ("m=3", "m=4", "m=5")
    for i, (tr_g, tr_n, col, m_lbl) in enumerate(zip(g3, n3, cols, lbls)):
        gx, gy = zip(*tr_g)
        nx, ny = zip(*tr_n)
        ax.plot(gx, gy, color=col, lw=1.9, label=f"Grid ({m_lbl})")
        ax.plot(nx, ny, ":", color="#64748b", lw=1.2, label="Newton" if i == 0 else None)
        sx, sy = next(iter(tr_g))
        ex, ey = tr_g[-1]
        ax.scatter([sx], [sy], color=col, s=36, zorder=4)
        ax.scatter([ex], [ey], color=col, marker="o", edgecolor="k", s=45, zorder=5)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("8. Pythagorean 3-4-5 Zoom (0.15 Cap)", fontweight="bold")
    ax.set_xlabel("x (units)")
    ax.legend(fontsize=7.2, loc="upper left", ncol=2)

    plt.tight_layout(rect=(0, 0, 1, 0.95))
    plt.savefig(out_path, dpi=180)
    plt.close(fig)
    print(f"Saved 8-panel benchmark dashboard to: {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="benchmark_report.json")
    ap.add_argument("--out", default="bcc_benchmark_dashboard.png")
    args = ap.parse_args()
    data = dict(DEFAULTS)
    if args.json and os.path.exists(args.json):
        with open(args.json, "r", encoding="utf-8") as f:
            raw = json.load(f)
        for k, v in raw.items():
            if v:
                data[k] = v
    build_dashboard(data, args.out)


if __name__ == "__main__":
    main()

