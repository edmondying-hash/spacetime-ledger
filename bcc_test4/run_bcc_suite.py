#!/usr/bin/env python3
"""Master test & simulation runner for the 6-face Planck-cube grid suite."""

import argparse, io, json, os, subprocess, sys, time, unittest
from contextlib import redirect_stdout
import baryon_calculator, bcc_3d_gravity, bcc_3body_orbits, bcc_born_pascal
import bcc_em_wave_sim, bcc_meson_sim, bcc_unified_sim, bcc3dhorizonsim

TESTS = [
    "test_baryon_calculator", "test_bcc_unified_sim", "test_bcc_meson_sim",
    "test_bcc_em_wave_sim", "test_bcc_born_pascal", "test_bcc_3d_gravity",
    "test_bcc3dhorizonsim", "test_bcc_3body_orbits",
]


def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for name in TESTS:
        suite.addTests(loader.loadTestsFromName(name))
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    return res.testsRun, res.wasSuccessful()


def run_baryon():
    saved, buf = list(sys.argv), io.StringIO()
    try:
        sys.argv = ["baryon_calculator.py"]
        with redirect_stdout(buf):
            baryon_calculator.main()
    finally:
        sys.argv = saved
    out = buf.getvalue()
    print(out, end="")
    return out


def run_mod(mod, script, funcs):
    for fn_name in funcs:
        fn = getattr(mod, fn_name, None)
        if callable(fn):
            buf = io.StringIO()
            with redirect_stdout(buf):
                fn()
            out = buf.getvalue()
            print(out, end="")
            return out
    p = subprocess.run([sys.executable, script], capture_output=True, text=True, check=True)
    print(p.stdout, end="")
    return p.stdout


def parse_json(tests_run, tests_ok, outs):
    baryons, mesons, hops, stored, glue, lensing, radii, work = [], [], [], [], [], [], [], []
    for line in outs["baryon"].splitlines():
        c = line.split()
        if len(c) >= 5 and c[0] in {"p", "Delta+", "Lambda", "Sigma0", "Xi0", "Omega-"}:
            baryons.append({"name": c[0], "model": float(c[3]), "pdg": float(c[4])})

    for line in outs["meson"].splitlines():
        c = line.split()
        if len(c) >= 8 and c[0] in {"pi", "rho", "K", "K*", "phi", "D", "D*", "J/psi"}:
            mesons.append({"name": c[0], "quarks": c[1], "J": int(c[2]),
                           "model": float(c[6]), "pdg": float(c[7])})
        elif len(c) >= 3 and c[0].isdigit():
            hops.append(int(c[0]))
            stored.append(float(c[2]))

    in_p2 = False
    for line in outs["unified"].splitlines():
        if "PART 2:" in line: in_p2 = True
        elif "PART 3:" in line: in_p2 = False
        elif in_p2 and line.split() and line.split()[0].isdigit():
            c = line.split()
            lk = int(c[0])
            lbl = "0 (Vacuum)" if lk == 0 else ("4 (Mass Gap Δ)" if lk == 4 else f"{lk} Links")
            glue.append({"links": lbl, "mass_mev": float(c[5])})

    in_p6 = False
    for line in outs["gravity"].splitlines():
        if "PART 6:" in line: in_p6 = True
        elif in_p6 and line.strip().startswith("(") and ")" in line:
            m_str, rest = line.strip().split(")", 1)
            c = rest.split()
            if len(c) >= 7:
                lensing.append({"momentum": (m_str + ")").replace(" ", ""),
                                "load": int(c[0]), "lag_b0": int(c[3]), "lag_b2": int(c[5])})

    for line in outs["horizon"].splitlines():
        c = line.split()
        if len(c) >= 6 and c[0].isdigit() and "(" in line and ")" in line:
            radii.append(int(c[0]))
            after_coord = line.split(")", 1)[1].split()
            work.append(float(after_coord[0]))

    three_body = [ln.strip() for ln in outs["three_body"].splitlines() if ln.strip()]

    return {
        "architecture": {"grid": "6-face cubic", "tests_run": tests_run, "tests_ok": tests_ok},
        "baryon_spectrum": baryons,
        "meson_spectrum": mesons,
        "string_breaking": {"threshold_mev": 275.0, "hops": hops, "stored_mev": stored},
        "glueball_mass_gap": glue,
        "momentum_lensing": lensing,
        "radial_horizon": {"deadlock_cap": 100.0, "radii": radii, "workload": work},
        "three_body_orbits": three_body,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-tests", action="store_true")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()
    t0 = time.perf_counter()

    t_run, t_ok = (0, True) if args.skip_tests else run_tests()
    if not t_ok:
        sys.exit(1)

    outs = {
        "baryon": run_baryon(),
        "unified": run_mod(bcc_unified_sim, "bcc_unified_sim.py", ("run_unified_demo", "run_demo", "main")),
        "meson": run_mod(bcc_meson_sim, "bcc_meson_sim.py", ("run_meson_demo", "run_demo", "main")),
        "em": run_mod(bcc_em_wave_sim, "bcc_em_wave_sim.py", ("run_em_and_slit_demo", "run_demo", "main")),
        "pascal": run_mod(bcc_born_pascal, "bcc_born_pascal.py", ("run_born_pascal_demo", "run_demo", "main")),
        "gravity": run_mod(bcc_3d_gravity, "bcc_3d_gravity.py", ("run_3d_gravity_demo", "run_demo", "main")),
        "horizon": run_mod(bcc3dhorizonsim, "bcc3dhorizonsim.py", ("run_3d_horizon_demo", "run_demo", "main")),
        "three_body": run_mod(bcc_3body_orbits, "bcc_3body_orbits.py", ("run_3body_demo", "run_demo", "main")),
    }
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(parse_json(t_run, t_ok, outs), f, indent=2)
        print(f"\nExported JSON to: {os.path.abspath(args.json_out)}")
    print(f"Master suite completed cleanly in {time.perf_counter() - t0:.2f}s.")


if __name__ == "__main__":
    main()
