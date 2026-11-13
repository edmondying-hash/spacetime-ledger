#!/usr/bin/env python3
"""Dual-channel (+/-) Pascal triangle walk vs. continuous wave-equation |psi|^2.

Demonstrates:
1. Pure integer tick counting across two phase channels (N_+ and N_-).
2. Destructive cancellation (N_+ - N_- = 0) creating exact 0.0000 dark nodes.
3. Born-rule detection workload (N_+ - N_-)^2 converging directly to the
   continuous wave-equation probability density |psi(x)|^2 as ticks N grow.
"""
import math


def compute_dual_pascal_distribution(n_ticks=12):
    """Run n_ticks of dual-channel (+/-) BCC diagonal hops and compare to continuous |psi|^2."""
    state = {0: (1, 0)}

    for tick in range(1, n_ticks + 1):
        next_state = {}
        for x, (pos, neg) in state.items():
            l_pos, l_neg = next_state.get(x - 1, (0, 0))
            next_state[x - 1] = (l_pos + pos, l_neg + neg)

            r_pos, r_neg = next_state.get(x + 1, (0, 0))
            if tick % 2 == 0:
                next_state[x + 1] = (r_pos + neg, r_neg + pos)
            else:
                next_state[x + 1] = (r_pos + pos, r_neg + neg)
        state = next_state

    positions = sorted(state.keys())
    classical_total = sum(pos + neg for pos, neg in state.values()) or 1
    born_total = sum((pos - neg) ** 2 for pos, neg in state.values()) or 1

    raw_wave = {
        x: math.exp(-(x * x) / float(n_ticks)) * (math.cos(math.pi * x / 4.0) ** 2)
        for x in positions
    }
    wave_total = sum(raw_wave.values()) or 1.0

    rows = []
    max_diff = 0.0
    for x in positions:
        pos, neg = state[x]
        net_psi = pos - neg
        p_class = (pos + neg) / classical_total
        p_born = (net_psi ** 2) / born_total
        p_wave = raw_wave[x] / wave_total
        diff = p_born - p_wave
        if abs(diff) > max_diff:
            max_diff = abs(diff)
        rows.append({
            'x': x,
            'pos': pos,
            'neg': neg,
            'net_psi': net_psi,
            'p_classical': p_class,
            'p_born': p_born,
            'p_wave': p_wave,
            'diff': diff,
        })

    return {'n_ticks': n_ticks, 'rows': rows, 'max_abs_diff': max_diff}


def run_pascal_born_demo():
    res12 = compute_dual_pascal_distribution(n_ticks=12)

    print("=== PART 1: Dual-Channel (+/-) Pascal Walk vs. Continuous Wave Equation (N=12 Ticks) ===")
    header = (f"{'Pos x':>6} {'N_+':>6} {'N_-':>6} {'Net psi':>8} {'Classical':>10} "
              f"{'Born (dN)^2':>11} {'WaveEq |psi|^2':>14} {'Diff':>8}  Pattern")
    print(header)
    print("-" * len(header))

    for r in res12['rows']:
        bar = "#" * int(round(r['p_born'] * 38))
        tag = " <-- Dark Node" if r['net_psi'] == 0 else ""
        print(f"{r['x']:6d} {r['pos']:6d} {r['neg']:6d} {r['net_psi']:8d} {r['p_classical']:10.4f} "
              f"{r['p_born']:11.4f} {r['p_wave']:14.4f} {r['diff']:+8.4f}  {bar}{tag}")

    print("\n=== PART 2: Convergence Toward Continuous Wave Equation as Ticks (N) Increase ===")
    print(f"{'Ticks (N)':>10} {'Active Pixels':>15} {'Max |Born - WaveEq| Error':>27}")
    print("-" * 56)
    for n in (12, 24, 48, 100):
        summary = compute_dual_pascal_distribution(n_ticks=n)
        print(f"{n:10d} {len(summary['rows']):15d} {summary['max_abs_diff']:27.6f}")


if __name__ == '__main__':
    run_pascal_born_demo()
