#!/usr/bin/env python3
"""Serverside Module 3: Zero-Metadata Client & Private Server Binding Table API."""

import itertools
import math
from typing import Dict, List, Optional, Tuple
import numpy as np

Coord3D = Tuple[int, int, int]
BCC_DIAGONALS_8: Tuple[Coord3D, ...] = tuple(itertools.product((-1, 1), repeat=3))


class ClientParticle:
    """Opaque client-space packet holding ZERO entanglement or server metadata."""

    __slots__ = ("pid", "pos")

    def __init__(self, pid: str, pos: Coord3D = (0, 0, 0)):
        self.pid = pid
        self.pos = pos


class SpacetimeKernelServer:
    """Backend server managing private entanglement tables carried during redraw()."""

    def __init__(self, vacuum_noise_prob: float = 0.0, seed: int = 42):
        self.rng = np.random.default_rng(seed)
        self.vacuum_noise_prob = vacuum_noise_prob
        self._next_eid = 1

        # Private server-side lookup tables (invisible to client objects)
        self._packet_to_eid: Dict[int, int] = {}
        self._groups: Dict[int, List[int]] = {}
        self._collapsed: Dict[int, bool] = {}
        self._anchor_angle: Dict[int, float] = {}
        self._anchor_outcome: Dict[int, int] = {}
        self._resolved_values: Dict[int, int] = {}

    # -------------------------------------------------------------------------
    # PRIMITIVE 1: x = entangle(a, a2, a3, ...)
    # -------------------------------------------------------------------------
    def entangle(self, *particles: ClientParticle) -> int:
        eid = self._next_eid
        self._next_eid += 1
        member_keys = [id(p) for p in particles]
        self._groups[eid] = member_keys
        self._collapsed[eid] = False

        for key in member_keys:
            self._packet_to_eid[key] = eid
            self._resolved_values.pop(key, None)
        return eid

    # -------------------------------------------------------------------------
    # PRIMITIVE 2: redraw(a, vector) [Server advances client pos & carries state]
    # -------------------------------------------------------------------------
    def redraw(self, particle: ClientParticle, vector: Coord3D) -> Coord3D:
        if vector not in BCC_DIAGONALS_8:
            raise ValueError(f"Invalid BCC vector {vector}; must be in (+-1, +-1, +-1).")
        px, py, pz = particle.pos
        dx, dy, dz = vector
        particle.pos = (px + dx, py + dy, pz + dz)

        # Server checks private binding table during redraw tick for vacuum noise
        key = id(particle)
        eid = self._packet_to_eid.get(key)
        if (
            eid is not None
            and not self._collapsed[eid]
            and self.vacuum_noise_prob > 0.0
            and self.rng.random() < self.vacuum_noise_prob
        ):
            self.decohere(particle)

        return particle.pos

    # -------------------------------------------------------------------------
    # PRIMITIVE 3 & 4: read(a, basis=...) and decohere() [no-arg vacuum random]
    # -------------------------------------------------------------------------
    def decohere(self, particle: Optional[ClientParticle] = None) -> int:
        """No-basis spontaneous vacuum fluctuation collapse (random())."""
        outcome = 1 if self.rng.random() < 0.5 else -1
        if particle is not None:
            eid = self._packet_to_eid.get(id(particle))
            if eid is not None and not self._collapsed[eid]:
                self._collapsed[eid] = True
                for member_key in self._groups[eid]:
                    self._resolved_values[member_key] = 1 if self.rng.random() < 0.5 else -1
        return outcome

    def read(self, particle: ClientParticle, basis_rad: Optional[float] = None) -> int:
        """Detector hit on opaque client particle 'a' resolved via private server table."""
        if basis_rad is None:
            return self.decohere(particle)

        key = id(particle)
        eid = self._packet_to_eid.get(key)
        if eid is None:
            return 1 if self.rng.random() < 0.5 else -1

        if self._collapsed[eid] and key in self._resolved_values:
            return self._resolved_values[key]

        if not self._collapsed[eid]:
            outcome = 1 if self.rng.random() < 0.5 else -1
            self._collapsed[eid] = True
            self._anchor_angle[eid] = basis_rad
            self._anchor_outcome[eid] = outcome
            self._resolved_values[key] = outcome
            return outcome

        delta = basis_rad - self._anchor_angle[eid]
        prob_opposite = math.cos(delta / 2.0) ** 2
        outcome = (
            -self._anchor_outcome[eid]
            if self.rng.random() < prob_opposite
            else self._anchor_outcome[eid]
        )
        self._resolved_values[key] = outcome
        return outcome

    def read_ghz_triplet(
        self,
        particles: Tuple[ClientParticle, ClientParticle, ClientParticle],
        bases: Tuple[str, str, str],
    ) -> Tuple[int, int, int]:
        """Resolve a 3-particle GHZ state via private server binding table."""
        keys = [id(p) for p in particles]
        eid = self._packet_to_eid.get(keys[0])
        if eid is None or self._groups.get(eid) != keys:
            raise ValueError("Particles do not match an active 3-particle server record.")

        if self._collapsed[eid]:
            return tuple(
                self._resolved_values.get(k, self.decohere()) for k in keys
            )  # type: ignore

        self._collapsed[eid] = True
        y_count = sum(1 for b in bases if b == "Y")
        target_product = -1 if y_count == 2 else 1

        r1 = 1 if self.rng.random() < 0.5 else -1
        r2 = 1 if self.rng.random() < 0.5 else -1
        r3 = target_product * r1 * r2

        for k, val in zip(keys, (r1, r2, r3)):
            self._resolved_values[k] = val
        return (r1, r2, r3)


def run_bell_sweep() -> None:
    print("=" * 74)
    print("PART 1: 2-Particle Bell CHSH Sweep [Zero-Metadata Client + redraw()]")
    print("=" * 74)
    print("Vacuum Noise/Hop | Bell CHSH |S| | Status (Classical Limit <= 2.0000)")
    print("-" * 74)

    a0, a1 = math.radians(0.0), math.radians(90.0)
    b0, b1 = math.radians(45.0), math.radians(135.0)
    settings = [(a0, b0, 1.0), (a0, b1, -1.0), (a1, b0, 1.0), (a1, b1, 1.0)]

    for noise in (0.0, 0.005, 0.015, 0.030, 0.060):
        srv = SpacetimeKernelServer(vacuum_noise_prob=noise, seed=42)
        s_total = 0.0
        trials = 2500

        for ang_a, ang_b, sign in settings:
            corr = 0
            for _ in range(trials):
                p1, p2 = ClientParticle("Signal"), ClientParticle("Idler")
                srv.entangle(p1, p2)
                for _ in range(12):
                    srv.redraw(p1, (1, 1, 1))
                    srv.redraw(p2, (-1, -1, -1))
                r1 = srv.read(p1, basis_rad=ang_a)
                r2 = srv.read(p2, basis_rad=ang_b)
                corr += r1 * r2
            s_total += sign * (corr / trials)

        s_val = abs(s_total)
        status = "QUANTUM NON-LOCAL (|S| > 2)" if s_val > 2.0 else "CLASSICAL / DECOHERED (|S| <= 2)"
        print(f"  {noise:>14.3f} | {s_val:>13.4f} | {status}")


def run_ghz_benchmark() -> None:
    print("\n" + "=" * 74)
    print("PART 2: 3-Particle GHZ Mermin Benchmark [Zero-Metadata Client + redraw()]")
    print("=" * 74)
    print("Vacuum Noise/Hop | <XXX>   | <XYY>   | Mermin M | Status (Classical <= 2.0)")
    print("-" * 74)

    ghz_vectors = ((1, 1, 1), (1, -1, -1), (-1, 1, -1))
    trials = 2500

    for noise in (0.0, 0.005, 0.015, 0.030, 0.060):
        srv = SpacetimeKernelServer(vacuum_noise_prob=noise, seed=108)
        means: Dict[Tuple[str, str, str], float] = {}

        for bases in (("X", "X", "X"), ("X", "Y", "Y"), ("Y", "X", "Y"), ("Y", "Y", "X")):
            prod_sum = 0
            for _ in range(trials):
                pa, pb, pc = ClientParticle("A"), ClientParticle("B"), ClientParticle("C")
                srv.entangle(pa, pb, pc)
                for _ in range(10):
                    srv.redraw(pa, ghz_vectors[0])
                    srv.redraw(pb, ghz_vectors[1])
                    srv.redraw(pc, ghz_vectors[2])
                ra, rb, rc = srv.read_ghz_triplet((pa, pb, pc), bases)
                prod_sum += ra * rb * rc
            means[bases] = prod_sum / trials

        mermin_m = (
            means[("X", "X", "X")]
            - means[("X", "Y", "Y")]
            - means[("Y", "X", "Y")]
            - means[("Y", "Y", "X")]
        )
        status = "GHZ NON-LOCAL (M > 2)" if mermin_m > 2.0 else "CLASSICAL / DECOHERED"
        print(
            f"  {noise:>14.3f} | {means[('X','X','X')]:>7.4f} | {means[('X','Y','Y')]:>7.4f} | "
            f"{mermin_m:>8.4f} | {status}"
        )


if __name__ == "__main__":
    run_bell_sweep()
    run_ghz_benchmark()
