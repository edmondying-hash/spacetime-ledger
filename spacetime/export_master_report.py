#!/usr/bin/env python3
"""Root Master JSON Exporter: Collects benchmarks across all 6 subdirectories."""

import json
import math
from pathlib import Path
import sys
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent
if not (ROOT / "bcc").exists():
    ROOT = ROOT.parent

for sub in ("bcc", "serverside", "sr", "gr", "cosmo", "elements"):
    sys.path.insert(0, str(ROOT / sub))

from bcc_meson_sim import BCCMesonSim
from bcc_orbital_sim import BCCOrbitalEngine
from bcc_virtual_carriers import BCCVirtualCarrierSim
from spacetime_server_api import ClientParticle, SpacetimeKernelServer
from bcc_sr_emergence import BCCSREmergenceSim
from bcc_gr_emergence import BCCGREmergenceSim
from bcc_dark_matter import BCCDarkMatterSim
from bcc_halo_solver import BCCHaloSolver
from bcc_dark_energy import BCCDarkEnergySim
from bcc_cmb_spectrum import BCCCMBSpectrumSim
from bcc_hydrogen_atom import BCCHydrogenAtomSim
from bcc_nuclear_fusion import BCCNuclearFusionSim
from bcc_nuclear_fission import BCCNuclearFissionSim
from bcc_molecular_chemistry import BCCMolecularChemistrySim

try:
    from bcc_frame_dragging import BCCFrameDraggingSim
    HAS_FRAME_DRAG = True
except ImportError:
    HAS_FRAME_DRAG = False


def collect_master_report() -> Dict[str, Any]:
    report: Dict[str, Any] = {"project": "Client-Server 3D BCC Spacetime Network", "pillars": {}}

    # 1. BCC Pillar: Meson Spectrum, Orbital Precession & Virtual Carriers (Compton + FFT Green's)
    meson_sim = BCCMesonSim()
    orb_sim = BCCOrbitalEngine(core_mass_mev=1218.3, cluster_count=18)
    ellipse = orb_sim.trace_trajectory(r0=24.0, v_tan_ratio=0.84, ticks=1600)
    vc_sim = BCCVirtualCarrierSim()

    report["pillars"]["bcc"] = {
        "mesons": meson_sim.run_spectrum(),
        "precessing_orbit_xy": ellipse["points"][:, :2].tolist(),
        "horizon_radius": orb_sim.horizon_radius,
        "photon_carriers": vc_sim.simulate_carrier_range(max_hops=8, mass_mev=0.0),
        "weak_carriers": vc_sim.simulate_carrier_range(max_hops=8, mass_mev=80379.0),
        "gluon_bundling": vc_sim.gluon_carrier_bundling(max_hops=8),
        "lattice_green_mu0": vc_sim.lattice_green_function(n=96, mu=0.0),
        "lattice_green_yukawa": vc_sim.lattice_green_function(n=96, mu=1.0 / 3.0),
    }

    # 2. Serverside Pillar: Bell CHSH & 3-Particle GHZ Decoherence Sweep
    noises = [0.0, 0.005, 0.015, 0.030, 0.060]
    bell_s_vals, ghz_m_vals = [], []
    a0, a1 = math.radians(0.0), math.radians(90.0)
    b0, b1 = math.radians(45.0), math.radians(135.0)
    settings = [(a0, b0, 1.0), (a0, b1, -1.0), (a1, b0, 1.0), (a1, b1, 1.0)]
    v_a, v_b, v_c = ((1, 1, 1), (1, -1, -1), (-1, 1, -1))

    for noise in noises:
        srv_b = SpacetimeKernelServer(vacuum_noise_prob=noise, seed=42)
        s_tot = 0.0
        for ang_a, ang_b, sign in settings:
            corr = 0
            for _ in range(1000):
                p1, p2 = ClientParticle("S"), ClientParticle("I")
                srv_b.entangle(p1, p2)
                for _ in range(12):
                    srv_b.redraw(p1, (1, 1, 1))
                    srv_b.redraw(p2, (-1, -1, -1))
                corr += srv_b.read(p1, ang_a) * srv_b.read(p2, ang_b)
            s_tot += sign * (corr / 1000.0)
        bell_s_vals.append(round(abs(s_tot), 4))

        srv_g = SpacetimeKernelServer(vacuum_noise_prob=noise, seed=108)
        means = {}
        for bases in (("X", "X", "X"), ("X", "Y", "Y"), ("Y", "X", "Y"), ("Y", "Y", "X")):
            psum = 0
            for _ in range(1000):
                pa, pb, pc = ClientParticle("A"), ClientParticle("B"), ClientParticle("C")
                srv_g.entangle(pa, pb, pc)
                for _ in range(10):
                    srv_g.redraw(pa, v_a)
                    srv_g.redraw(pb, v_b)
                    srv_g.redraw(pc, v_c)
                ra, rb, rc = srv_g.read_ghz_triplet((pa, pb, pc), bases)
                psum += ra * rb * rc
            means[bases] = psum / 1000.0
        m_val = means[("X", "X", "X")] - means[("X", "Y", "Y")] - means[("Y", "X", "Y")] - means[("Y", "Y", "X")]
        ghz_m_vals.append(round(m_val, 4))

    report["pillars"]["serverside"] = {
        "noise_per_hop": noises,
        "bell_chsh_S": bell_s_vals,
        "ghz_mermin_M": ghz_m_vals,
    }

    # 3. SR Pillar: Zigzag Clock Gamma & Energy-Momentum Dispersion
    sr_sim = BCCSREmergenceSim(c_bcc=1.0, rest_mass_mev=927.3)
    betas = [0.0, 0.25, 0.50, 0.70, 0.80, 0.90, 0.95, 0.99]
    report["pillars"]["sr"] = {
        "kinematics": sr_sim.kinematics_profile(betas),
        "dispersion": sr_sim.energy_momentum_table(betas),
    }

    # 4. GR Pillar: 3D BCC Poisson Time Dilation, 2x Light Deflection & Frame Dragging
    gr_sim = BCCGREmergenceSim(node_cap=100.0, r_s=3.0)
    fd_rows = []
    if HAS_FRAME_DRAG:
        fd_sim = BCCFrameDraggingSim(r_s=3.0, spin_j=1.8)
        fd_rows = fd_sim.radial_lense_thirring_sweep([12.0, 15.0, 18.0, 22.0, 28.0])
    report["pillars"]["gr"] = {
        "time_dilation": gr_sim.time_dilation_profile([3.0, 4.0, 6.0, 10.0, 14.0, 20.0]),
        "light_deflection": gr_sim.light_deflection_2x_test([6.0, 8.0, 10.0, 15.0, 20.0, 25.0]),
        "frame_dragging": fd_rows,
    }

    # 5. Cosmo Pillar: Rotation Curve, Cored Halo, Dark Energy & CMB Spectrum
    dm_sim = BCCDarkMatterSim()
    halo_sim = BCCHaloSolver()
    de_sim = BCCDarkEnergySim()
    cmb_sim = BCCCMBSpectrumSim()

    rot_rows = dm_sim.rotation_curve([2.0, 4.0, 6.0, 8.0, 11.0, 14.0, 17.0, 20.0])
    freqs = [float(f) for f in range(20, 421, 20)]
    report["pillars"]["cosmo"] = {
        "rotation_curve": rot_rows,
        "cusp_vs_core": halo_sim.cored_vs_cusp_profile([0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0]),
        "dark_energy_history": de_sim.cosmic_acceleration_history([2.5, 1.8, 1.2, 0.8, 0.632, 0.4, 0.2, 0.0]),
        "cmb_spectrum": cmb_sim.planck_blackbody_spectrum(freqs),
    }

    # 6. Elements Pillar: Hydrogen Orbitals, Fusion Tunneling, Binding Curve & Fission Chain
    h_sim = BCCHydrogenAtomSim()
    fus_sim = BCCNuclearFusionSim()
    fis_sim = BCCNuclearFissionSim()
    mol_sim = BCCMolecularChemistrySim()

    report["pillars"]["elements"] = {
        "hydrogen_orbitals": h_sim.standing_wave_orbitals(max_n=5),
        "fusion_tunneling": fus_sim.thermal_tunneling_sweep([15.0, 30.0, 60.0, 100.0, 150.0, 200.0]),
        "binding_curve": fis_sim.binding_curve_comparison(),
        "fission_chain": fis_sim.chain_reaction_generations(generations=8, initial_neutrons=100),
        "molecular_cohesion": mol_sim.intermolecular_cohesion_table(),
    }

    return report


def main() -> None:
    out_file = ROOT / "master_report.json"
    data = collect_master_report()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[Saved unified 6-pillar JSON report -> {out_file}]")


if __name__ == "__main__":
    main()
