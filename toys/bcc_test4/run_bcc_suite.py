#!/usr/bin/env python3
"""Master test & simulation runner for the 6-face Planck-cube grid suite (43 tests)."""

import argparse, io, json, os, subprocess, sys, time, unittest
from contextlib import redirect_stdout
import baryon_calculator, bcc_3d_gravity, bcc_3body_orbits, bcc_baryogenesis
import bcc_born_pascal, bcc_dark_matter, bcc_em_wave_sim, bcc_meson_sim
import bcc_unified_sim, bcc3dhorizonsim

TESTS = [
    "test_baryon_calculator", "test_bcc_unified_sim", "test_bcc_meson_sim",
    "test_bcc_em_wave_sim", "test_bcc_born_pascal", "test_bcc_3d_gravity",
    "test_bcc3dhorizonsim", "test_bcc_3body_orbits", "test_bcc_dark_matter",
    "test_bcc_baryogenesis",
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
    b_names = {"p", "Delta+", "Lambda", "Sigma0", "Xi0", "Omega-"}
    for line in outs["baryon"].splitlines():
        c = line.split()
        if len(c) >= 5:
            name, _b, _s, mod_s, pdg_s, *_ = c
            if name in b_names:
                baryons.append({"name": name, "model": float(mod_s), "pdg": float(pdg_s)})

    m_names = {"pi", "rho", "K", "K*", "phi", "D", "D*", "J/psi", "B", "B*", "Upsilon"}
    for line in outs["meson"].splitlines():
        c = line.split()
        if len(c) >= 8:
            name, qks, j_s, _bt, _rt, _st, mod_s, pdg_s, *_ = c
            if name in m_names:
                mesons.append({"name": name, "quarks": qks, "J": int(j_s),
                               "model": float(mod_s), "pdg": float(pdg_s)})
        elif len(c) >= 3:
            h_s, _tks, mev_s, *_ = c
            if h_s.isdigit():
                hops.append(int(h_s))
                stored.append(float(mev_s))

    in_p2 = False
    for line in outs["unified"].splitlines():
        if "PART 2:" in line: in_p2 = True
        elif "PART 3:" in line: in_p2 = False
        elif in_p2 and "Loop Links=" in line:
            left, right = line.split("Mass=", 1)
            lk = int(left.split("=").pop().strip(": "))
            mass_val = float(right.split("MeV").pop(0).strip())
            lbl = "0 (Vacuum)" if lk == 0 else ("4 (Mass Gap Δ)" if lk == 4 else f"{lk} Links")
            glue.append({"links": lbl, "mass_mev": mass_val})

    in_p6 = False
    for line in outs["gravity"].splitlines():
        if "PART 6:" in line: in_p6 = True
        elif in_p6 and line.strip().startswith("(") and ")" in line:
            m_str, rest = line.strip().split(")", 1)
            c = rest.split()
            if len(c) >= 7:
                ld_s, _tw, _cw, b0_s, _px0, b2_s, *_ = c
                lensing.append({"momentum": (m_str + ")").replace(" ", ""),
                                "load": int(ld_s), "lag_b0": int(b0_s), "lag_b2": int(b2_s)})

    for line in outs["horizon"].splitlines():
        c = line.split()
        if len(c) >= 6 and "(" in line and ")" in line:
            r_s, *_ = c
            if r_s.isdigit():
                radii.append(int(r_s))
                wk_s, *_ = line.split(")", 1).pop(1).split()
                work.append(float(wk_s))

    return {
        "architecture": {"grid": "6-face cubic", "tests_run": tests_run, "tests_ok": tests_ok},
        "baryon_spectrum": baryons, "meson_spectrum": mesons,
        "string_breaking": {"threshold_mev": 275.0, "hops": hops, "stored_mev": stored},
        "glueball_mass_gap": glue, "momentum_lensing": lensing,
        "radial_horizon": {"deadlock_cap": 100.0, "radii": radii, "workload": work},
        "three_body_orbits": [ln.strip() for ln in outs["three_body"].splitlines() if ln.strip()],
        "dark_matter": [ln.strip() for ln in outs["dark_matter"].splitlines() if ln.strip()],
        "baryogenesis": [ln.strip() for ln in outs["baryogenesis"].splitlines() if ln.strip()],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-tests", action="store_true")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()
    t0 = time.perf_counter()
    t_run, t_ok = (0, True) if args.skip_tests else run_tests()
    if not t_ok: sys.exit(1)
    outs = {
        "baryon": run_baryon(),
        "unified": run_mod(bcc_unified_sim, "bcc_unified_sim.py", ("run_unified_demo", "run_demo", "main")),
        "meson": run_mod(bcc_meson_sim, "bcc_meson_sim.py", ("run_meson_demo", "run_demo", "main")),
        "em": run_mod(bcc_em_wave_sim, "bcc_em_wave_sim.py", ("run_em_and_slit_demo", "run_demo", "main")),
        "pascal": run_mod(bcc_born_pascal, "bcc_born_pascal.py", ("run_born_pascal_demo", "run_demo", "main")),
        "gravity": run_mod(bcc_3d_gravity, "bcc_3d_gravity.py", ("run_3d_gravity_demo", "run_demo", "main")),
        "horizon": run_mod(bcc3dhorizonsim, "bcc3dhorizonsim.py", ("run_3d_horizon_demo", "run_demo", "main")),
        "three_body": run_mod(bcc_3body_orbits, "bcc_3body_orbits.py", ("run_3body_demo", "run_demo", "main")),
        "dark_matter": run_mod(bcc_dark_matter, "bcc_dark_matter.py", ("run_dark_matter_demo", "run_demo", "main")),
        "baryogenesis": run_mod(bcc_baryogenesis, "bcc_baryogenesis.py", ("run_baryogenesis_demo", "run_demo", "main")),
    }
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(parse_json(t_run, t_ok, outs), f, indent=2)
        print(f"\nExported JSON to: {os.path.abspath(args.json_out)}")
    print(f"Master suite completed cleanly in {time.perf_counter() - t0:.2f}s.")


if __name__ == "__main__":
    main()
