#!/usr/bin/env python3
"""Visualize exported JSON reports from bcc_unified_engine.py."""

import argparse
import json
from pathlib import Path
from typing import Any, Dict
import matplotlib.pyplot as plt
import numpy as np


def load_report(json_path: str) -> Dict[str, Any]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def plot_dashboard(report: Dict[str, Any], out_path: str = "bcc_dashboard.png") -> None:
    modules = report.get("modules", {})
    panels = []
    if "module_1_baryons" in modules:
        panels.append("m1")
    if "module_2_lensing" in modules:
        panels.append("m2")
    if "module_4_double_slit" in modules:
        panels.append("m4")
    if "module_5_isotropy_sweep" in modules or "module_5_isotropy" in modules:
        panels.append("m5")

    if not panels:
        raise ValueError("No plottable module data found in JSON report.")

    n_panels = len(panels)
    cols = 2 if n_panels > 1 else 1
    rows = (n_panels + 1) // 2

    plt.style.use("seaborn-v0_8-darkgrid")
    fig, axes = plt.subplots(rows, cols, figsize=(7 * cols, 5 * rows), squeeze=False)
    ax_list = axes.flatten()

    idx = 0

    # Panel 1: Module 1 Baryon Mass Breakdown
    if "m1" in panels:
        ax = ax_list[idx]
        idx += 1
        m1 = modules["module_1_baryons"]
        fams = m1["families"]
        names = [f["Family"] for f in fams]
        bare = np.array([f["BareT"] for f in fams])
        route = np.array([f["RouteT"] for f in fams])
        spin = np.array([f["SpinT"] for f in fams])

        x = np.arange(len(names))
        ax.bar(x, route, label="Gluon RouteT (BCC Links)", color="#2b5c8f")
        ax.bar(x, bare, bottom=route, label="Quark BareT", color="#e07a5f")
        ax.bar(x, spin, bottom=route + bare, label="SpinT", color="#81b29a")

        gb_mass = m1.get("glueball_4link_mev", 0)
        if gb_mass > 0:
            ax.axhline(
                gb_mass,
                color="#d90429",
                linestyle="--",
                linewidth=1.5,
                label=f"4-Link Glueball ({gb_mass:.0f} MeV)",
            )

        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=30, ha="right")
        ax.set_ylabel("Mass / Workload (MeV)")
        ax.set_title("Module 1: 3D BCC Baryon Workload & Glueball Gap")
        ax.legend(loc="upper left", fontsize=8)

    # Panel 2: Module 2 Coupled Radial Lensing
    if "m2" in panels:
        ax = ax_list[idx]
        idx += 1
        m2 = modules["module_2_lensing"]
        for key, color, label in [
            ("N", "#1d3557", "Nucleon Cluster (N)"),
            ("Omega", "#e63946", "Heavy Strange Cluster (Omega)"),
        ]:
            if key in m2:
                b_vals = [r["impact_b"] for r in m2[key]]
                c_vals = [r["eff_c_ratio"] for r in m2[key]]
                ax.plot(b_vals, c_vals, marker="o", linewidth=2, color=color, label=label)

        ax.axhline(1.0, color="gray", linestyle=":", label="Vacuum Speed (1.000c)")
        ax.set_xlabel("Impact Parameter b (BCC Diagonal Units)")
        ax.set_ylabel("Effective Signal Speed (c_eff / c)")
        ax.set_title("Module 2: Coupled Radial Wavefront Lensing")
        ax.legend(fontsize=8)

    # Panel 3: Module 4 Double-Slit Interference vs Which-Path Decoherence
    if "m4" in panels:
        ax = ax_list[idx]
        idx += 1
        m4 = modules["module_4_double_slit"]
        coh = m4["coherent_counts"]
        wp = m4["which_path_counts"]
        y_sorted = sorted(int(k) for k in coh.keys())
        coh_vals = [coh[str(y)] if str(y) in coh else coh[y] for y in y_sorted]
        wp_vals = [wp[str(y)] if str(y) in wp else wp[y] for y in y_sorted]

        ax.plot(
            y_sorted,
            coh_vals,
            marker="o",
            linewidth=2.2,
            color="#2a9d8f",
            label="Coherent (No Sensor - Interference)",
        )
        ax.plot(
            y_sorted,
            wp_vals,
            marker="s",
            linestyle="--",
            linewidth=1.8,
            color="#f4a261",
            label="Which-Path Sensor at y=-6 (Decohered)",
        )
        ax.axvline(-12, color="#e63946", linestyle=":", alpha=0.6, label="Dark Fringes (y=±12)")
        ax.axvline(12, color="#e63946", linestyle=":", alpha=0.6)
        ax.set_xlabel("Detector Screen Position y")
        ax.set_ylabel(f"Single-Dot Clicks (Total = {m4['clicks']})")
        ax.set_title("Module 4: Double-Slit Interference & Which-Path Washout")
        ax.legend(fontsize=8)

    # Panel 4: Module 5 Radial Scaling Sweep (Isotropy Error & Shapiro Delay)
    if "m5" in panels:
        ax = ax_list[idx]
        idx += 1
        sweep = modules.get("module_5_isotropy_sweep")
        if sweep is None:
            iso = modules["module_5_isotropy"]
            sweep = [{
                "radius": report.get("parameters", {}).get("radius", 60),
                "mean_shapiro_lag": np.mean([r["shapiro_lag"] for r in iso["rows"]]),
                "mean_isotropy_err_pct": iso["mean_anisotropy_err"],
            }]

        radii = [s["radius"] for s in sweep]
        errs = [s["mean_isotropy_err_pct"] for s in sweep]
        lags = [s["mean_shapiro_lag"] for s in sweep]

        l1 = ax.plot(
            radii,
            errs,
            marker="o",
            linewidth=2.2,
            color="#d62828",
            label="Mean Isotropy Error (%)",
        )
        ax.set_xlabel("Wavefront Radius R (BCC Lattice Units)")
        ax.set_ylabel("Spherical Anisotropy Error (%)", color="#d62828")
        ax.tick_params(axis="y", labelcolor="#d62828")

        ax2 = ax.twinx()
        l2 = ax2.plot(
            radii,
            lags,
            marker="^",
            linestyle="--",
            linewidth=2.0,
            color="#003049",
            label="Mean 1/r Shapiro Delay (Ticks)",
        )
        ax2.set_ylabel("Gravitational Shapiro Delay (Ticks)", color="#003049")
        ax2.tick_params(axis="y", labelcolor="#003049")

        lines = l1 + l2
        labels = [l.get_label() for l in lines]
        ax.legend(lines, labels, loc="center right", fontsize=8)
        ax.set_title("Module 5: Continuum Isotropy Convergence & Shapiro Lag")

    for empty_idx in range(idx, len(ax_list)):
        ax_list[empty_idx].set_visible(False)

    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    print(f"[Saved dashboard plot -> {out_path}]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot 3D BCC Unified Engine JSON output")
    parser.add_argument("json_file", type=str, help="Input JSON file from bcc_unified_engine.py")
    parser.add_argument(
        "--out",
        type=str,
        default="bcc_dashboard.png",
        help="Output PNG filename (default: bcc_dashboard.png)",
    )
    args = parser.parse_args()
    if not Path(args.json_file).exists():
        raise FileNotFoundError(f"JSON report not found: {args.json_file}")
    report = load_report(args.json_file)
    plot_dashboard(report, out_path=args.out)


if __name__ == "__main__":
    main()
