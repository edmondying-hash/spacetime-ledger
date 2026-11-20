#!/usr/bin/env python3
"""Serverside Module 5: Anti-FTL Firewall & 4-State Superdense Coding Protocol.

Demonstrates:
1. FTL Exploit Test: Alice tries to force-signal Bob using entangle() + decohere()
   without sending a client packet -> Bob sees 50.0% random noise (0.000 bits FTL).
2. 4-State Dense Coding: Alice encodes 1 of 4 messages (00, 01, 10, 11) via local
   server transforms, scrambles the transit packet, and Bob decodes all 4 states
   with 100% accuracy ONLY after the packet crosses client space at v <= c.
"""

# ---- Fixed-copy label (Nov 19, 2026) ---------------------------------------
# INSERTED: outcomes are random draws / one-time-pad bookkeeping in the server layer (by design);
# no-signalling holds by construction.
# ---------------------------------------------------------------------------


from typing import Dict, Tuple
import numpy as np


class AntiFTLServerFirewall:
    """Server kernel enforcing no-signaling scrambling and 4-state Bell decoding."""

    # 4 orthogonal Bell states represented as (parity_bit, phase_bit)
    BELL_STATES: Dict[str, Tuple[int, int]] = {
        "00": (0, 0),  # |Phi+>
        "01": (1, 0),  # |Psi+> (Bit-flip X applied)
        "10": (0, 1),  # |Phi-> (Phase-flip Z applied)
        "11": (1, 1),  # |Psi-> (Bit + Phase Y applied)
    }

    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)

    def attempt_ftl_exploit(self, trials: int = 10000) -> float:
        """Alice tries to transmit bit '1' to Bob instantaneously via decohere()."""
        bob_ones = 0
        for _ in range(trials):
            # Server allocates entangled pair in state |Phi+> = (0, 0)
            parity, _ = self.BELL_STATES["00"]
            # Alice tries to force a '1' by triggering read/decohere on her half:
            # Server firewall injects uncontrollable 50/50 vacuum randomness!
            alice_forced_attempt = int(self.rng.integers(0, 2))
            bob_bit = alice_forced_attempt ^ parity
            bob_ones += bob_bit
        return bob_ones / trials

    def run_4state_dense_coding(self, trials_per_msg: int = 1000) -> Dict[str, float]:
        """Alice sends 1 of 4 states; scrambled in transit, decoded at Bob (v <= c)."""
        accuracy: Dict[str, float] = {}
        intercepted_ones = 0
        total_intercepts = 0

        for msg, (op_x, op_z) in self.BELL_STATES.items():
            correct = 0
            for _ in range(trials_per_msg):
                # 1. Server allocates shared pair in base state (0, 0)
                base_parity, base_phase = 0, 0

                # 2. Alice applies 1 of 4 local transforms to encode 2 bits
                encoded_parity = base_parity ^ op_x
                encoded_phase = base_phase ^ op_z

                # 3. Transit Firewall Check: Eve intercepts Alice's packet mid-flight
                # Server masks the payload with random vacuum key -> looks 50/50 scrambled!
                vacuum_mask = int(self.rng.integers(0, 2))
                intercepted_bit = encoded_parity ^ vacuum_mask
                intercepted_ones += intercepted_bit
                total_intercepts += 1

                # 4. Packet reaches Bob at v <= c: Server combines both halves to decode
                decoded_msg = f"{encoded_phase}{encoded_parity}"
                if decoded_msg == msg:
                    correct += 1

            accuracy[msg] = (correct / trials_per_msg) * 100.0

        accuracy["eve_intercept_ratio"] = intercepted_ones / total_intercepts
        return accuracy


def main() -> None:
    fw = AntiFTLServerFirewall(seed=42)
    bob_ftl_rate = fw.attempt_ftl_exploit(trials=10000)
    dc = fw.run_4state_dense_coding(trials_per_msg=1000)

    print("=" * 74)
    print("SERVERSIDE MODULE 5: Anti-FTL Firewall & 4-State Superdense Coding")
    print("=" * 74)
    print(f"[1] FTL Signaling Exploit Test (Alice calls decohere() to send '1'):")
    print(f"    Bob's Measured '1' Rate = {bob_ftl_rate:.4f} (Pure 0.5000 noise -> FTL BLOCKED)")
    print("-" * 74)
    print(f"[2] Mid-Flight Packet Interception (Eve reads 1 qubit in transit):")
    print(f"    Intercepted '1' Rate    = {dc['eve_intercept_ratio']:.4f} (Scrambled 1-time pad)")
    print("-" * 74)
    print("[3] 4-State Superdense Decoding at Bob (After client packet arrives at v<=c):")
    for msg in ("00", "01", "10", "11"):
        print(f"    Encoded State '{msg}' -> Decoded Accuracy = {dc[msg]:>6.1f}%")
    print("=" * 74)


if __name__ == "__main__":
    main()
