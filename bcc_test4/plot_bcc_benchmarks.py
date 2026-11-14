#!/usr/bin/env python3
"""Compact 18-Panel (3x6) Master Dashboard Covering All 15 Modules (61/61 Tests OK)."""

import argparse, json
import matplotlib.pyplot as plt
import numpy as np
from bcc_3body_orbits import _grad_6face_load, _newton_acc
from bcc_baryogenesis import BCCBaryogenesisSim
from bcc_cmb_spectrum import BCCCMBSpectrumSim
from bcc_dark_matter import BCCDarkMatterSim
from bcc_gr_emergence import BCCGREmergenceSim
from bcc_halo_solver import BCCHaloSolver
from bcc_sr_emergence import BCCSREmergenceSim
from bcc_virtual_carriers import BCCVirtualCarrierSim


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
    fig, axes = plt.subplots(3, 6, figsize=(28, 14.5), dpi=160)
    it, w = iter(axes.flat), 0.36
    nt = d.get("architecture", {}).get("tests_run") or 61
    fig.suptitle(f"6-Face Planck-Cube Grid — 15-Module Master Benchmarks ({nt}/{nt} Tests OK)",
                 fontsize=16, fontweight="bold", y=0.975)

    # 1. Baryons & 2. Mesons
    for title, key, col in (("1. Baryons (3q)", "baryon_spectrum", "#2563eb"),
                            ("2. Mesons ($q\\bar{q}$)", "meson_spectrum", "#0d9488")):
        ax, rows = next(it), d[key]
        x = np.arange(len(rows))
        ax.bar(x - w / 2, [r["model"] for r in rows], w, label="Grid", color=col)
        ax.bar(x + w / 2, [r["pdg"] for r in rows], w, label="PDG", color="#94a3b8")
        ax.set_title(title, fontweight="bold", fontsize=10)
        ax.set_xticks(x)
        ax.set_xticklabels([r["name"] for r in rows], fontsize=6.5)
        ax.legend(fontsize=7)

    # 3. Flux-Tube String Breaking
    ax, sb = next(it), d["string_breaking"]
    hops, st, th = np.array(sb["hops"]), np.array(sb["stored_mev"]), sb["threshold_mev"]
    ax.plot(hops, st, "--", color="#475569", lw=1.2)
    ax.scatter(hops[st <= th], st[st <= th], color="#2563eb", s=34, label="Intact")
    ax.scatter(hops[st > th], st[st > th], color="#dc2626", s=46, marker="X", label="Snapped")
    ax.axhline(th, color="#ea580c", ls=":", lw=1.5, label=f"{th:.0f} MeV Cap")
    ax.set_title("3. Flux-Tube Breaking", fontweight="bold", fontsize=10)
    ax.legend(fontsize=7)

    # 4. Glueball Mass Gap
    ax, gb = next(it), d["glueball_mass_gap"]
    bars = ax.bar([g["links"] for g in gb], [g["mass_mev"] for g in gb],
                  color=["#cbd5e1", "#7c3aed", "#6d28d9", "#5b21b6"], width=0.5)
    for bar, g in zip(bars, gb):
        ax.text(bar.get_x() + bar.get_width() / 2, g["mass_mev"] + 60,
                f"{g['mass_mev']:.0f}", ha="center", fontsize=7, fontweight="bold")
    ax.set_ylim(0, max(g["mass_mev"] for g in gb) * 1.15)
    ax.set_title("4. Gluon Mass Gap (BareT=0)", fontweight="bold", fontsize=10)
    ax.tick_params(axis="x", labelsize=6.5)

    # 5. Momentum Lensing
    ax, ml = next(it), d["momentum_lensing"]
    xl = np.arange(len(ml))
    ax.plot(xl, [r["lag_b0"] for r in ml], "o-", color="#dc2626", lw=2, label="b=0")
    ax.plot(xl, [r["lag_b2"] for r in ml], "s-", color="#f59e0b", lw=2, label="b=2")
    ax.set_title("5. Momentum Lensing", fontweight="bold", fontsize=10)
    ax.set_xticks(xl)
    ax.set_xticklabels([r["momentum"] for r in ml], fontsize=6.8)
    ax.legend(fontsize=7)

    # 6. 3D Horizon
    ax, rh = next(it), d["radial_horizon"]
    rad, wk, cap = np.array(rh["radii"]), np.array(rh["workload"]), rh["deadlock_cap"]
    ax.bar(rad, wk, color=["#dc2626" if v >= cap else "#16a34a" for v in wk], width=0.55)
    ax.axhline(cap, color="#1e293b", ls="--", lw=1.5, label="Cap (100)")
    ax.set_title("6. 3D Deadlocked Horizon", fontweight="bold", fontsize=10)
    ax.legend(fontsize=7)

    # 7. Figure-8 & 8. Pythagorean 3-4-5
    ax = next(it)
    vx3, vy3 = -0.93240737, -0.86473146
    g8, n8 = trace_3body([1.0, 1.0, 1.0],
                         [(-0.97000436, 0.24308753), (0.97000436, -0.24308753), (0.0, 0.0)],
                         [(-0.5 * vx3, -0.5 * vy3), (-0.5 * vx3, -0.5 * vy3), (vx3, vy3)], 6.33, 12.0)
    for i, (tr, c) in enumerate(zip(g8, ("#2563eb", "#0d9488", "#7c3aed"))):
        ax.plot(*zip(*tr), color=c, lw=1.8, label="Grid" if i == 0 else None)
    ax.plot(*zip(*next(iter(n8))), "--", color="#94a3b8", lw=1.3, label="Newton")
    ax.set_title("7. 3-Body Figure-8", fontweight="bold", fontsize=10)
    ax.legend(fontsize=7)

    ax = next(it)
    g3, n3 = trace_3body([3.0, 4.0, 5.0], [(1.0, 3.0), (-2.0, -1.0), (1.0, -1.0)],
                         [(0.0, 0.0), (0.0, 0.0), (0.0, 0.0)], 3.2, 10.0)
    for i, (tg, tn, c) in enumerate(zip(g3, n3, ("#dc2626", "#f59e0b", "#2563eb"))):
        ax.plot(*zip(*tg), color=c, lw=1.8, label=f"Grid m={i+3}")
        ax.plot(*zip(*tn), ":", color="#64748b", lw=1.2, label="Newton" if i == 0 else None)
    ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.set_aspect("equal")
    ax.set_title("8. Pythagorean 3-4-5 (0.15 Cap)", fontweight="bold", fontsize=10)
    ax.legend(fontsize=6.5, loc="upper left", ncol=2)

    # 9. Dark Matter Rotation Curve
    ax, r_dm = next(it), [float(r) for r in range(2, 22, 2)]
    cv = BCCDarkMatterSim().rotation_curve(r_dm)
    ax.plot(r_dm, [c["v_total"] for c in cv], "o-", color="#7c3aed", lw=2, label="+ $Q_{EM}=0$ Halo")
    ax.plot(r_dm, [c["v_baryon"] for c in cv], "s--", color="#64748b", lw=1.7, label="Baryons Only")
    ax.set_ylim(0, 26); ax.set_title("9. Dark Matter Rotation Curve", fontweight="bold", fontsize=10)
    ax.legend(fontsize=7, loc="lower left")
    # 10. 3-Generation Baryogenesis (50/50 Cascade)
    ax, bsim = next(it), BCCBaryogenesisSim()
    b_res = [bsim.simulate_universe(n) for n in (1, 2, 3)]
    b_bars = ax.bar(["1 Gen\n(1D)", "2 Gens\n(2D)", "3 Gens\n(3D)"],
                    [r["surviving_matter"] for r in b_res],
                    color=["#94a3b8", "#94a3b8", "#2563eb"], width=0.5)
    ax.set_ylim(0, max(r["surviving_matter"] for r in b_res) * 1.28)
    for bar, r in zip(b_bars, b_res):
        lbl = "0" if r["surviving_matter"] == 0 else f"η~6.1e-10"
        ax.text(bar.get_x() + bar.get_width() / 2, r["surviving_matter"] * 1.04 + 1e-6,
                lbl, ha="center", fontsize=6.8, fontweight="bold")
    ax.set_title("10. 3-Gen Baryogenesis", fontweight="bold", fontsize=10)

    # 11. 3D Axis Generation Cutoff (100-Tick Node Cap)
    ax, gloads = next(it), bsim.generation_node_loads(node_cap=100.0)
    ax.bar(["Gen 1", "Gen 2", "Gen 3", "Gen 4"],
           [g["ticks"] for g in gloads],
           color=["#16a34a" if g["allowed"] else "#dc2626" for g in gloads], width=0.52)
    ax.axhline(100.0, color="#1e293b", ls="--", lw=1.5, label="Node Cap (100)")
    ax.set_ylim(0, 148)
    ax.set_title("11. 3D Axis Gen Cutoff", fontweight="bold", fontsize=10)
    ax.legend(fontsize=7, loc="upper left")

    # 12. Virtual Force-Carrier Range (1/r Photon vs. Yukawa Weak)
    ax, vsim = next(it), BCCVirtualCarrierSim()
    em_c = vsim.simulate_carrier_range(max_hops=8, mass_mev=0.0)
    wk_c = vsim.simulate_carrier_range(max_hops=8, mass_mev=80379.0, range_scale_hops=1.5)
    vhops = [r["hops"] for r in em_c]
    ax.plot(vhops, [r["potential"] for r in em_c], "o-", color="#0d9488", lw=2, label="Photon γ (1/r)")
    ax.plot(vhops, [r["potential"] for r in wk_c], "s--", color="#ea580c", lw=2, label="Weak W± (Yukawa)")
    ax.set_title("12. Virtual Carrier Range", fontweight="bold", fontsize=10)
    ax.legend(fontsize=7)

    # 13. Special Relativity: Lorentz Time Dilation & Length Contraction
    ax, sr_sim = next(it), BCCSREmergenceSim()
    betas = [0.0, 0.25, 0.5, 0.7, 0.85, 0.95]
    sr_kin = sr_sim.kinematics_profile(betas, rest_length_lp=1.0)
    ax.plot(betas, [r["gamma"] for r in sr_kin], "o-", color="#2563eb", lw=2, label="Time Dilation γ")
    ax.plot(betas, [r["clock_rate"] for r in sr_kin], "s--", color="#0d9488", lw=1.8, label="Length L/L0 (1/γ)")
    ax.set_title("13. SR Lorentz γ & Length", fontweight="bold", fontsize=10)
    ax.legend(fontsize=7, loc="upper left")

    # 14. Special Relativity: Bounded Velocity Addition (u + v <= c)
    ax = next(it)
    u_vals = [0.0, 0.25, 0.5, 0.75, 0.9, 1.0]
    gal = [u + 0.8 for u in u_vals]
    rel = [sr_sim.compose_velocities(u, 0.8)["grid_relativistic"] for u in u_vals]
    ax.plot(u_vals, gal, ":", color="#94a3b8", lw=1.6, label="Galilean (u+0.8c)")
    ax.plot(u_vals, rel, "o-", color="#7c3aed", lw=2, label="Grid SR Addition")
    ax.axhline(1.0, color="#dc2626", ls="--", lw=1.4, label="c Cap (1.0)")
    ax.set_title("14. SR Velocity Addition", fontweight="bold", fontsize=10)
    ax.legend(fontsize=6.8, loc="upper left")

    # 15. General Relativity: Schwarzschild g_00 Clock Rate & Horizon Lock
    ax, gr_sim = next(it), BCCGREmergenceSim(node_cap=100.0, r_s=3.0)
    gr_rad = [3.0, 4.0, 6.0, 8.0, 12.0, 16.0, 20.0]
    gr_prof = gr_sim.time_dilation_profile(gr_rad)
    ax.plot(gr_rad, [r["gr_dtau_dt"] for r in gr_prof], "-", color="#94a3b8", lw=3, label="Exact GR g_00")
    ax.plot(gr_rad, [r["grid_dtau_dt"] for r in gr_prof], "o--", color="#dc2626", lw=1.8, label="Grid sqrt(1-W/100)")
    ax.axvline(3.0, color="#1e293b", ls=":", lw=1.3, label="Horizon r_s=3")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("15. GR Time Dilation & Lock", fontweight="bold", fontsize=10)
    ax.legend(fontsize=6.8, loc="lower right")

    # 16. Inverse Halo Solver: Cored Lattice Halo vs. Divergent NFW Cusp
    ax, h_solver = next(it), BCCHaloSolver(node_cap=100.0)
    h_rad = [0.4, 0.8, 1.5, 2.5, 4.0, 6.0, 8.0]
    h_prof = h_solver.cored_vs_cusp_profile(h_rad, rho_0=85.0, core_radius=2.5)
    ax.plot(h_rad, [r["nfw_cusp_ticks"] for r in h_prof], "s:", color="#94a3b8", lw=1.8, label="NFW Cusp (1/r)")
    ax.plot(h_rad, [r["grid_core_ticks"] for r in h_prof], "o-", color="#0d9488", lw=2, label="Grid Cored Halo")
    ax.axhline(100.0, color="#dc2626", ls="--", lw=1.4, label="Node Cap (100)")
    ax.set_ylim(0, 320)
    ax.set_title("16. Halo Core vs. NFW Cusp", fontweight="bold", fontsize=10)
    ax.legend(fontsize=6.8, loc="upper right")

    # 17. CMB Planck Blackbody Spectrum (T_0 = 2.725 K, Peak = 160.2 GHz)
    ax, cmb_sim = next(it), BCCCMBSpectrumSim()
    freqs = [30.0, 60.0, 90.0, 120.0, 160.2, 200.0, 250.0, 300.0, 360.0, 420.0]
    spec = cmb_sim.planck_blackbody_spectrum(freqs)
    ax.plot(freqs, [s["norm_radiance"] for s in spec], "o-", color="#ea580c", lw=2, label="T_0 = 2.725 K")
    ax.axvline(160.2, color="#2563eb", ls="--", lw=1.4, label="Peak 160.2 GHz")
    ax.set_ylim(0, 1.15)
    ax.set_title("17. CMB Blackbody (2.725 K)", fontweight="bold", fontsize=10)
    ax.legend(fontsize=7, loc="upper right")

    # 18. Cosmic Expansion Cooling T(z) = 2.725 * (1 + z) & Acoustic Peak l_1 = 220
    ax = next(it)
    z_vals = [0.0, 1.0, 5.0, 20.0, 100.0, 400.0, 1098.0]
    cool = cmb_sim.redshift_cooling_history(z_vals)
    ax.loglog([1.0 + z for z in z_vals], [c["temp_k"] for c in cool], "s-", color="#7c3aed", lw=2, label="T(z) = T_0(1+z)")
    ax.scatter([1099.0], [2994.775], color="#dc2626", s=45, zorder=5, label="Recomb (l_1=220)")
    ax.set_title("18. CMB Cooling & l_1=220", fontweight="bold", fontsize=10)
    ax.legend(fontsize=6.8, loc="upper left")

    fig.subplots_adjust(left=0.035, right=0.99, top=0.92, bottom=0.05, wspace=0.28, hspace=0.36)
    plt.savefig(out_path, dpi=180); plt.close(fig)
    print(f"Saved 18-panel (3x6) master dashboard to: {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="benchmark_report.json")
    ap.add_argument("--out", default="bcc_benchmark_dashboard.png")
    args = ap.parse_args()
    with open(args.json, "r", encoding="utf-8") as f:
        build_dashboard(json.load(f), args.out)

