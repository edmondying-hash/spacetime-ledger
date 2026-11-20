#!/usr/bin/env python3
"""Root Master Dashboard: Renders a 15-panel (5x3) unified overview from master_report.json."""

import json
import matplotlib.pyplot as plt
import numpy as np


def render_master_dashboard(json_path: str = "master_report.json", out_png: str = "master_dashboard.png") -> None:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pillars = data["pillars"]
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, axes = plt.subplots(5, 3, figsize=(18, 24.5))
    ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14 = axes.flatten()

    # 1. [bcc/] Ground-State Meson Spectrum (Model vs PDG)
    mesons = pillars["bcc"]["mesons"]
    names = [m["name"] for m in mesons]
    x = np.arange(len(names))
    ax0.bar(x - 0.18, [m["ModelMeV"] for m in mesons], width=0.36, color="#1d3557", label="3D BCC Model")
    ax0.bar(x + 0.18, [m["PDGMeV"] for m in mesons], width=0.36, color="#e07a5f", label="PDG Experiment")
    ax0.set_yscale("log")
    ax0.set_xticks(x)
    ax0.set_xticklabels(names, rotation=35, ha="right", fontsize=8)
    ax0.set_ylabel("Mass (MeV, log)")
    ax0.set_title("1. [bcc/] Ground-State Meson Spectrum", fontweight="bold")
    ax0.legend(fontsize=8)

    # 2. [bcc/] Virtual Force Carriers: Photon (1/r) vs Weak (Yukawa)
    ph = pillars["bcc"]["photon_carriers"]
    wk = pillars["bcc"]["weak_carriers"]
    hops = [row["hops"] for row in ph]
    ax1.plot(hops, [row["potential"] for row in ph], marker="o", linewidth=2.2, color="#219ebc", label="Massless Photon V(r) = 1/r")
    ax1.plot(hops, [row["potential"] for row in wk], marker="s", linestyle="--", linewidth=2.2, color="#e63946", label="Weak W/Z Yukawa exp(-r/r0)/r")
    ax1.set_xlabel("BCC Diagonal Hops")
    ax1.set_ylabel("Carrier Potential V(r)")
    ax1.set_title("2. [bcc/] Virtual Carriers: EM vs. Weak Yukawa", fontweight="bold")
    ax1.legend(fontsize=8)

    # 3. [bcc/] Self-Interacting Gluon Flux-Tube Bundling (4-Hop Snap)
    gl = pillars["bcc"]["gluon_bundling"]
    g_hops = [row["hops"] for row in gl]
    g_mev = [row["tube_mev"] for row in gl]
    colors_gl = ["#d62828" if row["snapped"] else "#2a9d8f" for row in gl]
    ax2.bar(g_hops, g_mev, color=colors_gl, edgecolor="black")
    ax2.axhline(275.0, color="#1d1e2c", linestyle="--", linewidth=1.5, label="String Break Threshold (275 MeV)")
    ax2.set_xlabel("BCC Diagonal Hops")
    ax2.set_ylabel("Stored Tube Energy (MeV)")
    ax2.set_title("3. [bcc/] Gluon Bundling & 4-Hop Snap", fontweight="bold")
    ax2.legend(fontsize=8)

    # 4. [bcc/] Refractive Orbital Rosette
    pts = np.array(pillars["bcc"]["precessing_orbit_xy"])
    h_rad = pillars["bcc"]["horizon_radius"]
    ax3.add_patch(plt.Circle((0, 0), h_rad, color="#1d1e2c", label=f"Horizon (r={h_rad})"))
    ax3.plot(pts[:, 0], pts[:, 1], color="#f77f00", linewidth=1.4, label="Precessing Ellipse")
    ax3.set_aspect("equal")
    ax3.set_xlim(-27, 27)
    ax3.set_ylim(-27, 27)
    ax3.set_xlabel("X (BCC Units)")
    ax3.set_ylabel("Y (BCC Units)")
    ax3.set_title("4. [bcc/] Refractive Perihelion Rosette", fontweight="bold")
    ax3.legend(loc="upper right", fontsize=8)

    # 5. [serverside/] Bell & GHZ Decoherence
    srv = pillars["serverside"]
    noise = srv["noise_per_hop"]
    ax4.plot(noise, srv["ghz_mermin_M"], marker="s", linewidth=2.2, color="#7209b7", label="3-Particle GHZ (Mermin M)")
    ax4.plot(noise, srv["bell_chsh_S"], marker="o", linewidth=2.2, color="#2a9d8f", label="2-Particle Bell (CHSH |S|)")
    ax4.axhline(2.0, color="#d62828", linestyle="--", linewidth=1.4, label="Classical Local Limit (2.0)")
    ax4.set_xlabel("Vacuum Fluctuation Noise / Hop")
    ax4.set_ylabel("Non-Locality Parameter")
    ax4.set_title("5. [serverside/] Bell & GHZ Decoherence", fontweight="bold")
    ax4.legend(fontsize=8)

    # 6. [sr/] Zigzag Clock Lorentz Dilation & Contraction
    kin = pillars["sr"]["kinematics"]
    betas = [row["beta"] for row in kin]
    ax5.plot(betas, [row["zigzag_gamma"] for row in kin], marker="o", linewidth=2.2, color="#1d3557", label="Lorentz γ (Time Dilation)")
    ax5.plot(betas, [row["clock_rate"] for row in kin], marker="s", linestyle="--", color="#e63946", label="Internal Clock Rate (1/γ)")
    ax5.set_xlabel("Velocity Fraction β = v / c")
    ax5.set_ylabel("Dimensionless Factor")
    ax5.set_title("6. [sr/] BCC Zigzag Clock Dilation", fontweight="bold")
    ax5.legend(fontsize=8)

    # 7. [gr/] 3D BCC Poisson Time Dilation vs Schwarzschild
    td = pillars["gr"]["time_dilation"]
    r_td = [row["r"] for row in td]
    ax6.plot(r_td, [row["gr_dtau_dt"] for row in td], color="#1d3557", linewidth=2.3, label="Schwarzschild GR g_00")
    ax6.plot(r_td, [row["bcc_dtau_dt"] for row in td], marker="o", linestyle="--", color="#e63946", label="3D BCC Poisson Clock")
    ax6.set_xlabel("Radius r (BCC Units)")
    ax6.set_ylabel("Clock Rate dτ / dt")
    ax6.set_title("7. [gr/] BCC Poisson Time Dilation & Horizon", fontweight="bold")
    ax6.legend(fontsize=8)

    # 8. [gr/] 2x Einstein Photon Deflection (g_00 + g_rr)
    ld = pillars["gr"]["light_deflection"]
    b_vals = [row["b"] for row in ld]
    ax7.plot(b_vals, [row["bcc_rad"] for row in ld], marker="o", linewidth=2.3, color="#2a9d8f", label="3D BCC Total (2.00x Newton)")
    ax7.plot(b_vals, [row["newton_rad"] for row in ld], marker="^", linestyle="--", color="#f4a261", label="Newtonian (1.00x g_00 only)")
    ax7.set_xlabel("Impact Parameter b (BCC Units)")
    ax7.set_ylabel("Deflection Angle α (rad)")
    ax7.set_title("8. [gr/] 2x Einstein Light Deflection", fontweight="bold")
    ax7.legend(fontsize=8)

    # 9. [cosmo/] Flat Galaxy Rotation Curve
    rc = pillars["cosmo"]["rotation_curve"]
    r_rc = [row["r"] for row in rc]
    ax8.plot(r_rc, [row["v_total"] for row in rc], marker="o", linewidth=2.3, color="#2a9d8f", label="Total (Baryons + Q_EM=0 Halo)")
    ax8.plot(r_rc, [row["v_baryon"] for row in rc], marker="s", linestyle="--", color="#f4a261", label="Baryons Only (Keplerian)")
    ax8.set_xlabel("Galactic Radius r")
    ax8.set_ylabel("Orbital Speed v(r)")
    ax8.set_title("9. [cosmo/] Flat Rotation Curve (84.6% Dark)", fontweight="bold")
    ax8.legend(fontsize=8)

    # 10. [cosmo/] NFW Cusp vs. 100-Tick BCC Core Saturation
    cc = pillars["cosmo"]["cusp_vs_core"]
    r_cc = [row["r"] for row in cc]
    ax9.plot(r_cc, [row["nfw_cusp_ticks"] for row in cc], marker="^", linestyle="--", color="#e63946", label="Divergent NFW Cusp (1/r)")
    ax9.plot(r_cc, [row["grid_core_ticks"] for row in cc], marker="o", linewidth=2.3, color="#1d3557", label="3D BCC Cored Halo (<100 Cap)")
    ax9.axhline(100.0, color="#1d1e2c", linestyle=":", linewidth=1.4, label="Node Cap (100 ticks/cycle)")
    ax9.set_xlabel("Core Radius r (BCC Units)")
    ax9.set_ylabel("Halo Density (ticks/cycle)")
    ax9.set_title("10. [cosmo/] Cusp-to-Core Saturation", fontweight="bold")
    ax9.legend(fontsize=8)

    # 11. [cosmo/] Congestion-Gated Dark Energy Transition
    de = pillars["cosmo"]["dark_energy_history"]
    z_vals = [row["z"] for row in de]
    ax10.plot(z_vals, [row["omega_m_z"] for row in de], marker="o", color="#e07a5f", label="Matter Fraction Ω_m(z)")
    ax10.plot(z_vals, [row["omega_l_z"] for row in de], marker="^", color="#3d5a80", label="Idle Vacuum Ω_Λ(z)")
    ax10.axvline(0.632, color="#2a9d8f", linestyle=":", linewidth=1.6, label="Acceleration Flip (z=0.632)")
    ax10.invert_xaxis()
    ax10.set_xlabel("Redshift z (Past -> Present)")
    ax10.set_ylabel("Cosmic Volume Fraction")
    ax10.set_title("11. [cosmo/] Congestion-Gated Dark Energy", fontweight="bold")
    ax10.legend(fontsize=8)

    # 12. [cosmo/] Planck CMB Blackbody Spectrum (T_0 = 2.725 K)
    cmb = pillars["cosmo"]["cmb_spectrum"]
    freqs = [row["freq_ghz"] for row in cmb]
    ax11.plot(freqs, [row["norm_radiance"] for row in cmb], marker="o", markersize=4, linewidth=2.2, color="#7209b7", label="BCC Bose-Einstein Radiance")
    ax11.axvline(160.2, color="#e63946", linestyle="--", linewidth=1.4, label="Peak Frequency (160.2 GHz)")
    ax11.set_xlabel("Frequency ν (GHz)")
    ax11.set_ylabel("Normalized Spectral Radiance")
    ax11.set_title("12. [cosmo/] CMB Blackbody Spectrum (2.725 K)", fontweight="bold")
    ax11.legend(fontsize=8)

    # 13. [elements/] Nuclear Binding Curve (Fusion -> Fe-56 Peak -> Fission)
    bc = pillars["elements"]["binding_curve"]
    iso_labels = [row["isotope"].split("(")[-1].rstrip(")") for row in bc]
    b_vals_nuc = [row["binding_per_nuc"] for row in bc]
    ax12.plot(iso_labels, b_vals_nuc, marker="D", linewidth=2.3, color="#1d3557", label="Binding Energy / Nucleon")
    ax12.axvline("56Fe", color="#2a9d8f", linestyle="--", linewidth=1.5, label="56Fe Peak Stability (8.79 MeV)")
    ax12.set_xlabel("Nuclear Isotope (Light -> Heavy)")
    ax12.set_ylabel("Binding / Nucleon (MeV)")
    ax12.set_title("13. [elements/] Nuclear Binding Curve (Fusion & Fission)", fontweight="bold")
    ax12.legend(fontsize=8)

    # 14. [elements/] D-T Fusion Quantum Tunneling Reactivity
    ft = pillars["elements"]["fusion_tunneling"]
    t_mk = [row["temp_mk"] for row in ft]
    ax13.plot(t_mk, [row["norm_reactivity"] for row in ft], marker="o", linewidth=2.3, color="#f77f00", label="Gamow Tunneling Reactivity")
    ax13.axvline(15.0, color="#219ebc", linestyle=":", linewidth=1.5, label="Solar Core (15M K)")
    ax13.axvline(150.0, color="#d62828", linestyle="--", linewidth=1.5, label="Tokamak Ignition (150M K)")
    ax13.set_xlabel("Plasma Temperature (Million K)")
    ax13.set_ylabel("Normalized Reactivity")
    ax13.set_title("14. [elements/] D-T Fusion Quantum Tunneling", fontweight="bold")
    ax13.legend(fontsize=8)

    # 15. [elements/] U-235 Neutron Chain Reaction (k_eff)
    fc = pillars["elements"]["fission_chain"]
    gens = [row["gen"] for row in fc]
    ax14.plot(gens, [row["supercritical_k118"] for row in fc], marker="^", linewidth=2.2, color="#d62828", label="Supercritical (k=1.18)")
    ax14.plot(gens, [row["critical_k100"] for row in fc], marker="s", linewidth=2.2, color="#2a9d8f", label="Critical Reactor (k=1.00)")
    ax14.plot(gens, [row["subcritical_k085"] for row in fc], marker="o", linestyle="--", linewidth=2.0, color="#8d99ae", label="Subcritical Shutdown (k=0.85)")
    ax14.set_xlabel("Fission Generation")
    ax14.set_ylabel("Neutron Population")
    ax14.set_title("15. [elements/] U-235 Fission Chain Reaction", fontweight="bold")
    ax14.legend(fontsize=8)

    fig.suptitle(
        "Client-Server 3D BCC Spacetime Network: Unified 15-Panel (6-Pillar) Benchmark Dashboard",
        fontsize=16,
        fontweight="bold",
    )
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.savefig(out_png, dpi=180)
    print(f"[Saved unified 15-panel master dashboard -> {out_png}]")


if __name__ == "__main__":
    render_master_dashboard()
