#!/usr/bin/env python3
# B9 clock-factor check harness. Implements S0-S5 of B9_CLOCK_DESIGN.md
# in the same folder. Existence of this file does not authorise a scored run.
# One attempt per step; no retry; no fitting to targets.

from __future__ import annotations

import argparse
import json
import math
import os
import resource
import sys
import time
from pathlib import Path

import numpy as np

# Archived orbit.py constants (sha256 a0cefdf9...d402ad). Do not retune.
GM = 1.32712440018e20
C_LIGHT = 299792458.0
SEMI = 5.7909050e10
ECC = 0.205630
YEAR = 3.15576e7

# Archived formula / 100-year endpoint values from orbit.json (64d13f10...d52499).
REF = {
    "I1_formula": 42.98069352502894,
    "I1_orbit": 42.91229380880339,
    "I2_formula": 46.333187619981196,
    "I2_orbit": 46.27759181715892,
    "I3_formula": 14.326897841676312,
    "I2_beta": 0.766,
    "I2_gamma": 1.0,
}

# Paper §6.12 limb deflection (arcsec) at b = R_sun with factor 4GM/bc^2.
LIMB_GR = 1.7512433


def perihelion_formula(beta: float, gamma: float) -> float:
    """Arcsec per century, same expression as mercury/orbit.py."""
    return (
        6
        * np.pi
        * GM
        / (SEMI * (1 - ECC**2) * C_LIGHT**2)
        * (2 + 2 * gamma - beta)
        / 3
        * (100 * YEAR / (2 * np.pi * np.sqrt(SEMI**3 / GM)))
        * 180
        / np.pi
        * 3600
    )


def ppn_accel(beta: float, gamma: float):
    def f(t, y):
        r = np.array(y[:2])
        v = np.array(y[2:])
        R = np.hypot(*r)
        rv = r @ v
        v2 = v @ v
        acc = -GM * r / R**3 + GM / (C_LIGHT**2 * R**3) * (
            (2 * (beta + gamma) * GM / R - gamma * v2) * r + 2 * (1 + gamma) * rv * v
        )
        return [*v, *acc]

    return f


def lrl_angle(r, v):
    h = r[0] * v[1] - r[1] * v[0]
    A = np.array([v[1] * h, -v[0] * h]) / GM - r / np.hypot(*r)
    return float(np.arctan2(A[1], A[0]))


def orbit_endpoint(beta: float, gamma: float, years: float = 100.0):
    """100-year DOP853 LRL endpoint, same as mercury/orbit.py (arcsec/century)."""
    from scipy.integrate import solve_ivp

    rp = SEMI * (1 - ECC)
    vp = np.sqrt(GM / SEMI * (1 + ECC) / (1 - ECC))
    y0 = [rp, 0, 0, vp]
    s = solve_ivp(
        ppn_accel(beta, gamma),
        [0, years * YEAR],
        y0,
        method="DOP853",
        rtol=1e-13,
        atol=1e-3,
    )
    r = s.y[:2, -1]
    v = s.y[2:, -1]
    ang = lrl_angle(r, v)
    return float(np.degrees(ang) * 3600 * 100 / years), {
        "nfev": int(s.nfev),
        "nsteps": int(s.t.size),
        "success": bool(s.success),
        "message": str(s.message),
        "years": years,
    }


def orbit_linear_fit(beta: float, gamma: float, n_orbits: int = 200):
    """Paper §6.12 style: linear fit of LRL angle vs time over n_orbits (arcsec/century)."""
    from scipy.integrate import solve_ivp

    period = 2 * np.pi * np.sqrt(SEMI**3 / GM)
    t_end = n_orbits * period
    rp = SEMI * (1 - ECC)
    vp = np.sqrt(GM / SEMI * (1 + ECC) / (1 - ECC))
    y0 = [rp, 0, 0, vp]
    # Sample about 8 points per orbit, plus endpoints.
    t_eval = np.linspace(0.0, t_end, n_orbits * 8 + 1)
    s = solve_ivp(
        ppn_accel(beta, gamma),
        [0, t_end],
        y0,
        method="DOP853",
        rtol=1e-13,
        atol=1e-3,
        t_eval=t_eval,
        dense_output=False,
    )
    angs = []
    for i in range(s.y.shape[1]):
        angs.append(lrl_angle(s.y[:2, i], s.y[2:, i]))
    angs = np.unwrap(np.array(angs))
    coef = np.polyfit(s.t, angs, 1)
    arcsec_cy = float(np.degrees(coef[0]) * 3600 * 100 * YEAR)
    # Newtonian energy at start and end, for a drift check (1PN energy is not conserved).
    def newton_E(r, v):
        R = np.hypot(*r)
        return 0.5 * (v @ v) - GM / R

    E0 = newton_E(s.y[:2, 0], s.y[2:, 0])
    E1 = newton_E(s.y[:2, -1], s.y[2:, -1])
    return arcsec_cy, {
        "nfev": int(s.nfev),
        "n_orbits": n_orbits,
        "success": bool(s.success),
        "newton_E_start": float(E0),
        "newton_E_end": float(E1),
        "newton_E_rel_change": float((E1 - E0) / E0) if E0 != 0 else None,
        "slope_rad_per_s": float(coef[0]),
        "intercept_rad": float(coef[1]),
    }


def factor(beta, gamma):
    return (2 + 2 * gamma - beta) / 3.0


def rss_mib():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def cpu_s():
    ru = resource.getrusage(resource.RUSAGE_SELF)
    return ru.ru_utime + ru.ru_stime


class Meter:
    def __init__(self, name):
        self.name = name
        self.t0 = time.perf_counter()
        self.c0 = cpu_s()
        self.rss0 = rss_mib()

    def close(self, extra=None):
        out = {
            "step": self.name,
            "wall_s": time.perf_counter() - self.t0,
            "cpu_s": cpu_s() - self.c0,
            "peak_rss_mib": rss_mib(),
        }
        if extra:
            out.update(extra)
        return out


def analytic_row(name, beta, gamma, alpha, notes, limb_gr=LIMB_GR):
    form = float(perihelion_formula(beta, gamma)) if (beta is not None and gamma is not None) else None
    return {
        "id": name,
        "beta": beta,
        "gamma": gamma,
        "factor": None if (beta is None or gamma is None) else factor(beta, gamma),
        "perihelion_formula_arcsec_cy": form,
        "alpha_redshift": alpha,
        "z_over_z_GR_linear": None if alpha is None else 1.0 + alpha,
        "limb_deflection_arcsec": None if gamma is None else limb_gr * (1 + gamma) / 2.0,
        "shapiro_over_GR": None if gamma is None else (1 + gamma) / 2.0,
        "notes": notes,
    }


def score_targets(row, peri=(42.94, 43.02), alpha_max=1.4e-4, gamma_lo=1 + (2.1 - 2.3) * 1e-5, gamma_hi=1 + (2.1 + 2.3) * 1e-5):
    """Score one identification against the default targets. Does not close B9."""
    out = {}
    form = row.get("perihelion_formula_arcsec_cy")
    if form is None:
        out["perihelion"] = "UNINFORMATIVE"
    else:
        out["perihelion"] = "MEETS" if peri[0] <= form <= peri[1] else "MISSES"
        out["perihelion_residual_arcsec"] = form - 42.98
    a = row.get("alpha_redshift")
    if a is None:
        out["redshift"] = "UNINFORMATIVE"
    else:
        out["redshift"] = "MEETS" if abs(a) <= alpha_max else "MISSES"
        out["alpha"] = a
    g = row.get("gamma")
    if g is None:
        out["gamma"] = "UNINFORMATIVE"
    else:
        out["gamma"] = "MEETS" if gamma_lo <= g <= gamma_hi else "MISSES"
        out["gamma_minus_one"] = g - 1.0
    return out


def step_S0(out_dir: Path):
    meter = Meter("S0")
    report = {"imports": {}, "formula_check": {}, "timing_orbit_5yr": None}
    try:
        import numpy  # noqa: F401

        report["imports"]["numpy"] = numpy.__version__
        import scipy
        from scipy.integrate import solve_ivp  # noqa: F401

        report["imports"]["scipy"] = scipy.__version__
        report["imports"]["solve_ivp"] = True
    except Exception as e:
        report["imports"]["error"] = repr(e)
        rec = meter.close()
        return {"status": "FAIL", "reason": "import", "report": report, "resources": rec}

    f11 = float(perihelion_formula(1, 1))
    f766 = float(perihelion_formula(0.766, 1))
    f10 = float(perihelion_formula(1, 0))
    report["formula_check"] = {
        "I1": {"value": f11, "ref": REF["I1_formula"], "rel_diff": abs(f11 - REF["I1_formula"]) / REF["I1_formula"]},
        "I2": {"value": f766, "ref": REF["I2_formula"], "rel_diff": abs(f766 - REF["I2_formula"]) / REF["I2_formula"]},
        "I3": {"value": f10, "ref": REF["I3_formula"], "rel_diff": abs(f10 - REF["I3_formula"]) / REF["I3_formula"]},
    }
    if any(v["rel_diff"] > 1e-9 for v in report["formula_check"].values()):
        rec = meter.close()
        return {"status": "FAIL", "reason": "formula_mismatch", "report": report, "resources": rec}

    # Cost check only: 5-year endpoint is not a perihelion number (poor read-out).
    t1 = time.perf_counter()
    val5, meta5 = orbit_endpoint(1, 1, years=5.0)
    report["timing_orbit_5yr"] = {
        "wall_s": time.perf_counter() - t1,
        "value_arcsec_cy_not_a_result": val5,
        "note": "5-year single endpoint is a poor read-out; official orbits use 100 years or a 200-orbit linear fit.",
        **meta5,
    }
    rec = meter.close()
    return {"status": "PASS", "report": report, "resources": rec}


def step_control(name, beta, gamma, formula_ref, orbit_ref, do_fit=True):
    meter = Meter(name)
    form = float(perihelion_formula(beta, gamma))
    end, end_meta = orbit_endpoint(beta, gamma, years=100.0)
    out = {
        "beta": beta,
        "gamma": gamma,
        "formula": form,
        "formula_ref": formula_ref,
        "formula_rel_diff": abs(form - formula_ref) / formula_ref,
        "orbit_100yr_endpoint": end,
        "orbit_100yr_ref": orbit_ref,
        "orbit_100yr_abs_diff": abs(end - orbit_ref),
        "orbit_100yr_meta": end_meta,
    }
    if do_fit:
        fit, fit_meta = orbit_linear_fit(beta, gamma, n_orbits=200)
        out["orbit_200_linear_fit"] = fit
        out["orbit_200_linear_fit_meta"] = fit_meta
    formula_ok = out["formula_rel_diff"] <= 1e-9
    orbit_ok = out["orbit_100yr_abs_diff"] <= 0.02
    out["status"] = "PASS" if (formula_ok and orbit_ok) else "FAIL"
    if not formula_ok:
        out["fail_reason"] = "formula_tolerance"
    elif not orbit_ok:
        out["fail_reason"] = "orbit_endpoint_tolerance"
    rec = meter.close()
    out["resources"] = rec
    return out


def step_S3(include_I6=False):
    meter = Meter("S3")
    rows = [
        analytic_row(
            "I1",
            1.0,
            1.0,
            0.0,
            "Paper split, no self-load. Clock e^{-U}, light cost e^{2U}, U = U_phys. Control.",
        ),
        analytic_row(
            "I2",
            0.766,
            1.0,
            0.0,
            "Paper own-load, archived beta=0.766. The 46.3'' double-count. Control.",
        ),
        analytic_row(
            "I3",
            1.0,
            0.0,
            0.0,
            "B_m common factor, rigid nodes, G to Kepler. Clock and coordinate light share s; local c constant.",
        ),
        analytic_row(
            "I4",
            None,
            None,
            1.0,
            "Diagnostic: paper U held fixed, clock Phi=e^{-2U}, no G retuning. Linear redshift 2x; linear g00 also 2x (Kepler fails). No consistent 1PN (beta,gamma) until G is retuned.",
        ),
        analytic_row(
            "I5",
            1.0,
            1.0,
            0.0,
            "B_m clock at e^{-2U_load} with paper load-first routing still on, G to Kepler. Relabel of I1. Live only if the split remains.",
        ),
    ]
    if include_I6:
        rows.append(
            analytic_row(
                "I6",
                0.766,
                1.0,
                0.0,
                "Identification of B_m clock-at-f^2 with own-load I2. Not implied by the L1.5b measurement; scored only if K2 says so.",
            )
        )
    table = []
    for row in rows:
        row["targets"] = score_targets(row)
        table.append(row)
    rec = meter.close()
    return {"status": "PASS", "table": table, "resources": rec, "include_I6": include_I6}


def step_S4(controls_passed, include_I6=False):
    meter = Meter("S4")
    if not controls_passed:
        rec = meter.close()
        return {
            "status": "UNINFORMATIVE",
            "reason": "controls_did_not_pass",
            "resources": rec,
        }
    jobs = [
        ("I3", 1.0, 0.0, REF["I3_formula"], None),
        ("I5", 1.0, 1.0, REF["I1_formula"], REF["I1_orbit"]),
    ]
    if include_I6:
        jobs.append(("I6", 0.766, 1.0, REF["I2_formula"], REF["I2_orbit"]))
    results = {}
    for name, beta, gamma, fref, oref in jobs:
        form = float(perihelion_formula(beta, gamma))
        end, end_meta = orbit_endpoint(beta, gamma, years=100.0)
        fit, fit_meta = orbit_linear_fit(beta, gamma, n_orbits=200)
        results[name] = {
            "beta": beta,
            "gamma": gamma,
            "formula": form,
            "formula_ref": fref,
            "formula_rel_diff": abs(form - fref) / fref if fref else None,
            "orbit_100yr_endpoint": end,
            "orbit_100yr_ref_if_any": oref,
            "orbit_200_linear_fit": fit,
            "orbit_100yr_meta": end_meta,
            "orbit_200_linear_fit_meta": fit_meta,
            "note": "I4 has no consistent 1PN orbit; omitted. I1/I2 are S1/S2.",
        }
    results["I4"] = {
        "status": "UNINFORMATIVE",
        "reason": "no_consistent_1PN_orbit_until_G_retuned",
        "alpha_redshift": 1.0,
    }
    rec = meter.close()
    return {"status": "PASS", "results": results, "resources": rec}


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=str) + "\n")


def main(argv=None):
    p = argparse.ArgumentParser(description="B9 clock-factor check (scored only if Edmond names the design sha256).")
    p.add_argument("--step", choices=["S0", "S1", "S2", "S3", "S4", "S5", "all"], default="all")
    p.add_argument("--out", type=Path, default=Path("out"))
    p.add_argument("--include-I6", action="store_true", help="Score I6 as well (only if Edmond's K2 says so).")
    args = p.parse_args(argv)
    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    steps = ["S0", "S1", "S2", "S3", "S4", "S5"] if args.step == "all" else [args.step]
    summary = {"steps": {}, "include_I6": args.include_I6}

    if "S0" in steps:
        summary["steps"]["S0"] = step_S0(out)
        write_json(out / "S0.json", summary["steps"]["S0"])
        if summary["steps"]["S0"]["status"] != "PASS" and args.step == "all":
            write_json(out / "result.json", summary)
            print("S0 failed; later steps not started.", file=sys.stderr)
            return 1

    if "S1" in steps:
        summary["steps"]["S1"] = step_control("S1", 1.0, 1.0, REF["I1_formula"], REF["I1_orbit"])
        write_json(out / "S1.json", summary["steps"]["S1"])

    if "S2" in steps:
        summary["steps"]["S2"] = step_control("S2", REF["I2_beta"], REF["I2_gamma"], REF["I2_formula"], REF["I2_orbit"])
        write_json(out / "S2.json", summary["steps"]["S2"])

    if "S3" in steps:
        summary["steps"]["S3"] = step_S3(include_I6=args.include_I6)
        write_json(out / "S3.json", summary["steps"]["S3"])

    controls_passed = True
    if "S1" in summary["steps"]:
        controls_passed = controls_passed and summary["steps"]["S1"].get("status") == "PASS"
    if "S2" in summary["steps"]:
        controls_passed = controls_passed and summary["steps"]["S2"].get("status") == "PASS"
    # If S4 is requested alone, do not assume controls passed.
    if args.step == "S4":
        controls_passed = False
        summary["S4_note"] = "S4 run in isolation is UNINFORMATIVE unless S1 and S2 already passed in this out/ folder."
        s1p = out / "S1.json"
        s2p = out / "S2.json"
        if s1p.exists() and s2p.exists():
            s1 = json.loads(s1p.read_text())
            s2 = json.loads(s2p.read_text())
            controls_passed = s1.get("status") == "PASS" and s2.get("status") == "PASS"

    if "S4" in steps:
        if args.step == "all" and not controls_passed:
            pass
        summary["steps"]["S4"] = step_S4(controls_passed, include_I6=args.include_I6)
        write_json(out / "S4.json", summary["steps"]["S4"])

    if "S5" in steps:
        meter = Meter("S5")
        summary["measured_targets_default"] = {
            "perihelion_arcsec_cy": "42.98 ± 0.04",
            "redshift_GP_A_abs_alpha": 1.4e-4,
            "gamma_Cassini": "1 + (2.1 ± 2.3)e-5",
        }
        summary["resources_S5"] = meter.close()
        summary["status"] = "RECORDED"
        write_json(out / "result.json", summary)
        write_json(out / "S5.json", {"status": "RECORDED", "resources": summary["resources_S5"]})

    print(json.dumps({k: (v.get("status") if isinstance(v, dict) else v) for k, v in summary.get("steps", {}).items()}, indent=2))
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    raise SystemExit(main())
