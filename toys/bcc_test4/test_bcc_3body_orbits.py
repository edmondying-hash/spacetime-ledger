#!/usr/bin/env python3
"""Unit tests for 3-body ledger-grid orbits on the 6-face Planck-cube lattice."""

import unittest
from bcc_3body_orbits import simulate_3body


class TestBCC3BodyOrbits(unittest.TestCase):
    def test_figure8_stays_outside_smoothing_cap_and_tracks_newton(self):
        """Figure-8 choreography stays bound outside 0.15 smoothing radius with low drift."""
        f8_pos = [(-0.97000436, 0.24308753), (0.97000436, -0.24308753), (0.0, 0.0)]
        vx3, vy3 = -0.93240737, -0.86473146
        f8_vel = [(-0.5 * vx3, -0.5 * vy3), (-0.5 * vx3, -0.5 * vy3), (vx3, vy3)]

        res = simulate_3body(
            [1.0, 1.0, 1.0],
            f8_pos,
            f8_vel,
            t_end=6.33,
            dt=0.002,
            cell_scale=12.0,
            smoothing_units=0.15,
        )
        self.assertGreater(res["min_sep"], 0.15)
        self.assertLess(res["max_drift"], 0.15)

    def test_pythagorean_345_close_pass_triggers_grid_smoothing_split(self):
        """Pythagorean 3-4-5 matches Newton pre-pass, then diverges inside 0.15 cell cap."""
        p345_pos = [(1.0, 3.0), (-2.0, -1.0), (1.0, -1.0)]
        p345_vel = [(0.0, 0.0), (0.0, 0.0), (0.0, 0.0)]

        pre = simulate_3body(
            [3.0, 4.0, 5.0],
            p345_pos,
            p345_vel,
            t_end=1.80,
            dt=0.002,
            cell_scale=10.0,
            smoothing_units=0.15,
        )
        post = simulate_3body(
            [3.0, 4.0, 5.0],
            p345_pos,
            p345_vel,
            t_end=10.0,
            dt=0.002,
            cell_scale=10.0,
            smoothing_units=0.15,
        )
        self.assertLess(pre["max_drift"], 0.08)
        self.assertLess(post["min_sep"], 0.15)
        self.assertGreater(post["max_drift"], pre["max_drift"])

    def test_finite_c_retarded_load_introduces_measurable_phase_shift(self):
        """Finite-speed (c) congestion propagation differs from instantaneous load spread."""
        f8_pos = [(-0.97000436, 0.24308753), (0.97000436, -0.24308753), (0.0, 0.0)]
        vx3, vy3 = -0.93240737, -0.86473146
        f8_vel = [(-0.5 * vx3, -0.5 * vy3), (-0.5 * vx3, -0.5 * vy3), (vx3, vy3)]

        r_inst = simulate_3body(
            [1.0, 1.0, 1.0], f8_pos, f8_vel, t_end=3.0, dt=0.002, retarded_c=0.0
        )
        r_ret = simulate_3body(
            [1.0, 1.0, 1.0], f8_pos, f8_vel, t_end=3.0, dt=0.002, retarded_c=15.0
        )
        self.assertNotAlmostEqual(r_inst["max_drift"], r_ret["max_drift"], places=4)


if __name__ == "__main__":
    unittest.main()

