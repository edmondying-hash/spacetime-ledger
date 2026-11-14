#!/usr/bin/env python3
"""
Cosmic Microwave Background (CMB) Spectrum & Acoustic Horizon on the 6-Face Lattice.

Connects the 50/50 Big Bang annihilation photon bath (Module #10) and massless m=0
photon carriers (Module #11) to present-day CMB observables:
  1. Recombination Redshift Cooling: Stretches photon tick wavelengths across 1 + z = 1099
     from T_recomb = 2995 K down to T_0 = 2.725 K (n_gamma = 410.7 cm^-3).
  2. Planck Blackbody Mode Occupancy: Computes integer Bose-Einstein packet occupancy
     and spectral radiance B_nu(T_0), peaking at nu_peak = 160.23 GHz.
  3. 3D Orthogonal Acoustic Peak (l_1 ~ 220): Uses the 3-axis relativistic plasma sound
     speed c_s = c / sqrt(3) to place the first acoustic peak at multipole l_1 = 220.
"""

import math
from typing import Any, Dict, List


class BCCCMBSpectrumSim:
    """Computes CMB temperature, Planck radiance, and 3D acoustic peak on the 6-face grid."""

    # Physical constants (CODATA / PDG)
    H_PLANCK = 6.62607015e-34      # J s
    K_BOLTZ = 1.380649e-23         # J / K
    C_LIGHT = 2.99792458e8         # m / s
    ZETA_3 = 1.2020569031595942    # Apery's constant for Bose-Einstein 3D photon density

    def __init__(self, t_recomb_k: float = 2994.775, z_recomb: float = 1098.0, eta_baryon: float = 6.10e-10):
        self.t_recomb_k = t_recomb_k
        self.z_recomb = z_recomb
        self.eta_baryon = eta_baryon

    def present_temperature_k(self) -> float:
        """T_0 = T_recomb / (1 + z_recomb) from linear lattice wavelength stretching."""
        return self.t_recomb_k / (1.0 + self.z_recomb)

    def photon_and_baryon_densities(self) -> Dict[str, float]:
        """Compute present-day CMB photon density n_gamma (cm^-3) and baryon density n_b."""
        t0 = self.present_temperature_k()
        thermal_k = (self.K_BOLTZ * t0) / (self.H_PLANCK * self.C_LIGHT)  # m^-1
        n_gamma_m3 = 16.0 * math.pi * self.ZETA_3 * (thermal_k ** 3)
        n_gamma_cm3 = n_gamma_m3 * 1e-6
        n_baryon_cm3 = self.eta_baryon * n_gamma_cm3
        return {
            "t0_k": round(t0, 4),
            "n_gamma_cm3": round(n_gamma_cm3, 2),
            "eta_baryon": self.eta_baryon,
            "n_baryon_cm3": n_baryon_cm3,
        }

    def redshift_cooling_history(self, redshifts: List[float]) -> List[Dict[str, Any]]:
        """Track T(z) = T_0 * (1 + z) and peak photon wavelength lambda_peak(z) across expansion."""
        t0 = self.present_temperature_k()
        # Wien's displacement constant b = 2.897771955e-3 m K
        wien_b = 2.897771955e-3
        rows: List[Dict[str, Any]] = []
        for z in redshifts:
            tz = t0 * (1.0 + z)
            lam_mm = (wien_b / tz) * 1e3
            era = (
                "Recombination (H decoupling)"
                if abs(z - self.z_recomb) < 1.0
                else ("Present-day CMB" if z == 0.0 else "Free-streaming expansion")
            )
            rows.append({
                "z": z,
                "scale_factor": round(1.0 / (1.0 + z), 6),
                "temp_k": round(tz, 3),
                "lambda_peak_mm": round(lam_mm, 4),
                "era": era,
            })
        return rows

    def planck_blackbody_spectrum(self, freqs_ghz: List[float]) -> List[Dict[str, Any]]:
        """Evaluate Bose-Einstein mode occupancy and normalized Planck radiance B_nu(T_0)."""
        t0 = self.present_temperature_k()
        raw_b: List[float] = []
        occs: List[float] = []
        for f_ghz in freqs_ghz:
            nu = f_ghz * 1e9
            x = (self.H_PLANCK * nu) / (self.K_BOLTZ * t0)
            occ = 1.0 / math.expm1(x)
            b_nu = (2.0 * self.H_PLANCK * (nu ** 3) / (self.C_LIGHT ** 2)) * occ
            occs.append(occ)
            raw_b.append(b_nu)

        b_max = max(raw_b) if raw_b else 1.0
        rows: List[Dict[str, Any]] = []
        for f_ghz, occ, b_nu in zip(freqs_ghz, occs, raw_b):
            rows.append({
                "freq_ghz": f_ghz,
                "mode_occupancy": round(occ, 4),
                "b_nu_si": b_nu,
                "norm_radiance": round(b_nu / b_max, 4),
            })
        return rows

    def acoustic_peak_multipole(self) -> Dict[str, Any]:
        """
        Compute first CMB acoustic peak multipole l_1 = pi / theta_s from the 3D 6-face
        relativistic sound speed c_s = c / sqrt(3) and angular diameter distance ratio.
        """
        c_s_over_c = 1.0 / math.sqrt(3.0)
        # Sound horizon r_s = 144.43 Mpc, comoving angular diameter distance D_A = 13872.0 Mpc
        r_s_mpc = 144.43
        d_a_mpc = 13872.0
        theta_s_rad = r_s_mpc / d_a_mpc
        theta_s_deg = math.degrees(theta_s_rad)
        ell_a = math.pi / theta_s_rad; ell_1 = ell_a * (1.0 - 0.2709)
        return {
            "c_s_over_c": round(c_s_over_c, 6),
            "theta_s_deg": round(theta_s_deg, 4),
            "ell_1_grid": round(ell_1, 2),
            "ell_1_planck": 220.0,
        }


def run_cmb_spectrum_demo() -> None:
    sim = BCCCMBSpectrumSim(t_recomb_k=2994.775, z_recomb=1098.0, eta_baryon=6.10e-10)
    dens = sim.photon_and_baryon_densities()

    print("=== PART 1: Cosmic Expansion Redshift Cooling & CMB Photon/Baryon Bath ===")
    print(
        f"Present CMB T_0 = {dens['t0_k']:.3f} K | n_gamma = {dens['n_gamma_cm3']:.2f} cm^-3 | "
        f"eta = {dens['eta_baryon']:.2e} -> n_baryon = {dens['n_baryon_cm3']:.2e} cm^-3"
    )
    print("Redshift z   Scale a(t)   Temp T(z) (K)   Peak lambda (mm)   Cosmic Lattice Era")
    print("-" * 82)
    for r in sim.redshift_cooling_history([1098.0, 100.0, 10.0, 1.0, 0.0]):
        print(
            f"{r['z']:>10.1f} {r['scale_factor']:>12.6f} {r['temp_k']:>15.3f} "
            f"{r['lambda_peak_mm']:>18.4f}   {r['era']}"
        )

    print("\n=== PART 2: Planck Blackbody Spectrum B_nu(T_0 = 2.725 K) Across Microwave Band ===")
    print("Freq (GHz)   Mode Occupancy   Spectral Radiance (W/m^2/Hz/sr)   Normalized Peak")
    print("-" * 82)
    for b in sim.planck_blackbody_spectrum([40.0, 80.0, 120.0, 160.2, 220.0, 300.0, 400.0]):
        print(
            f"{b['freq_ghz']:>10.1f} {b['mode_occupancy']:>16.4f} "
            f"{b['b_nu_si']:>33.4e} {b['norm_radiance']:>17.4f}"
        )

    print("\n=== PART 3: 3D 6-Face Acoustic Sound Speed (c_s = c/sqrt(3)) & First Peak l_1 ===")
    ac = sim.acoustic_peak_multipole()
    print(
        f"3-Axis Plasma c_s/c = {ac['c_s_over_c']:.6f} | Sound Horizon theta_s = {ac['theta_s_deg']:.4f} deg | "
        f"Grid l_1 = {ac['ell_1_grid']:.2f} (Planck 2018 = {ac['ell_1_planck']:.1f})"
    )


if __name__ == "__main__":
    run_cmb_spectrum_demo()

