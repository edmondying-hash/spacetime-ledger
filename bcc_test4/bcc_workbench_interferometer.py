#!/usr/bin/env python3
"""
BCC Workbench Torsion-Pendulum & 976 nm Laser Interferometer Experiment (`bcc_test4`).

Models a tabletop vacuum experiment using your spacecraft's 976 nm GaAs diode + FAC lens +
99.7% dielectric mirror hardware as a precision lab instrument:
  1. Measures open-boundary photon recoil (F = P_opt / c) vs. closed-absorber null test (F = 0).
  2. Converts nanonewton torsion fiber twist into optical interferometer fringe shifts
     (lambda = 976 nm, nanometer path resolution) and wall optical-lever deflection.
  3. Compares workbench energy density against Dielectric Damage, Schwinger Pair Production,
     and 100% Planck-Cube Congestion Saturation limits.
"""

import math
from typing import Any, Dict


class BCCWorkbenchInterferometerSim:
    """Tabletop vacuum torsion pendulum + 976 nm laser interferometer simulator."""

    def __init__(
        self,
        laser_optical_watts: float = 5.0,
        wavelength_nm: float = 976.0,
        mirror_reflectivity: float = 0.997,
        arm_radius_m: float = 0.15,          # 30 cm balanced crossbar (15 cm lever arm)
        fiber_length_m: float = 0.40,        # 40 cm tungsten suspension fiber
        fiber_diameter_um: float = 75.0,     # 25 micron tungsten wire
        beam_waist_mm: float = 1.0,          # 1 mm collimated FAC laser spot
    ):
        self.p_opt = laser_optical_watts
        self.wavelength_m = wavelength_nm * 1e-9
        self.refl = mirror_reflectivity
        self.r_arm = arm_radius_m
        self.L_fiber = fiber_length_m
        self.r_fiber = (fiber_diameter_um * 1e-6) / 2.0
        self.spot_area_m2 = math.pi * ((beam_waist_mm * 1e-3) / 2.0) ** 2

        self.c = 299_792_458.0
        self.G_tungsten = 160.0e9  # Shear modulus of tungsten (Pa)
        self.planck_saturation_w_cm2 = 4.63e113
        self.schwinger_limit_w_cm2 = 4.65e29
        self.mirror_damage_w_cm2 = 5.0e6  # CW dielectric coating thermal limit (~5 MW/cm^2)

    def torsion_spring_constant_nm_rad(self) -> float:
        """Torsional stiffness kappa = (pi * G * r^4) / (2 * L) in N*m/rad."""
        return (math.pi * self.G_tungsten * (self.r_fiber ** 4)) / (2.0 * self.L_fiber)

    def run_workbench_trial(
        self, open_exhaust: bool = True, wall_distance_m: float = 4.0
    ) -> Dict[str, Any]:
        """Compute steady-state torsion twist, interferometer fringe shift, and saturation regime."""
        # Open boundary: collimated beam exits mirror (F = R * P / c); Closed absorber: F_net = 0
        eff_power = self.p_opt * self.refl if open_exhaust else 0.0
        thrust_n = eff_power / self.c
        torque_nm = thrust_n * self.r_arm

        kappa = self.torsion_spring_constant_nm_rad()
        theta_rad = torque_nm / kappa
        theta_mrad = theta_rad * 1e3

        # Optical path shift at the interferometer mirror arm: dL = r_arm * theta
        path_shift_m = self.r_arm * theta_rad
        fringe_shifts = (2.0 * path_shift_m) / self.wavelength_m

        # Wall optical lever deflection (beam angle doubles on mirror reflection: 2 * theta)
        wall_deflection_mm = (2.0 * theta_rad * wall_distance_m) * 1e3

        # Intensity vs. Saturation Regimes (W/cm^2)
        spot_area_cm2 = self.spot_area_m2 * 1e4
        intensity_w_cm2 = self.p_opt / spot_area_cm2
        congestion_fraction = intensity_w_cm2 / self.planck_saturation_w_cm2

        return {
            "mode": "OPEN_EXHAUST" if open_exhaust else "CLOSED_ABSORBER_NULL",
            "optical_watts": self.p_opt,
            "thrust_nn": round(thrust_n * 1e9, 3),
            "twist_mrad": round(theta_mrad, 4),
            "path_shift_nm": round(path_shift_m * 1e9, 2),
            "interferometer_fringes": round(fringe_shifts, 3),
            "wall_spot_shift_mm": round(wall_deflection_mm, 2),
            "intensity_w_cm2": round(intensity_w_cm2, 2),
            "planck_congestion_ratio": congestion_fraction,
            "below_mirror_damage": intensity_w_cm2 < self.mirror_damage_w_cm2,
        }


def run_workbench_demo() -> None:
    sim = BCCWorkbenchInterferometerSim(
        laser_optical_watts=5.0,
        wavelength_nm=976.0,
        arm_radius_m=0.15,
        fiber_length_m=0.40,
        fiber_diameter_um=75.0,
    )
    open_res = sim.run_workbench_trial(open_exhaust=True, wall_distance_m=4.0)
    null_res = sim.run_workbench_trial(open_exhaust=False, wall_distance_m=4.0)

    print("=== BCC WORKBENCH TORSION + 976 nm INTERFEROMETER EXPERIMENT ===")
    print(f"Hardware: 5.0 W 976 nm GaAs Diode + FAC Lens + 99.7% Mirror | 75 um x 40 cm Tungsten Fiber")
    print(f"1. Open-Boundary Exhaust:   F = {open_res['thrust_nn']:6.3f} nN | Path Shift = {open_res['path_shift_nm']:6.2f} nm ({open_res['interferometer_fringes']:.2f} fringes) | Wall Lever = {open_res['wall_spot_shift_mm']:.2f} mm")
    print(f"2. Closed-Absorber Null:    F = {null_res['thrust_nn']:6.3f} nN | Path Shift = {null_res['path_shift_nm']:6.2f} nm ({null_res['interferometer_fringes']:.2f} fringes) | Wall Lever = {null_res['wall_spot_shift_mm']:.2f} mm")
    print(f"3. Spot Intensity Check:    {open_res['intensity_w_cm2']:.2f} W/cm^2 (Safe below 5e6 W/cm^2 mirror limit | Planck Grid Load: {open_res['planck_congestion_ratio']:.2e})")


if __name__ == "__main__":
    run_workbench_demo()
