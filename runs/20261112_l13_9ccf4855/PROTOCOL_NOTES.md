# L1.3 run 20261112_l13_9ccf4855: protocol notes written before any computation

Design: design/L1_3_RUN_DESIGN.md, sha256 9ccf48559c099289b24af638164ca64b95195872b1e4a0d8966ed44ca800d098 (copied unchanged).
Approval: Edmond Ying, 2026-11-12 7:33 PM America/New_York (decisions file, sha256 2dc1bb8e94e16c727bc2bc978d5ee904044e3e1a7566878d33a0c1960b158072) and 7:36 PM America/New_York in chat ("L1.3 is APPROVED to run on bigbang"); S0-S3 only.

## D2 answer (recorded before S2)
"Layer weights" = two separate Wilson angles, phi_2 (step 2, V+) and phi_4 (step 4, V-), with the hop weight nu_S = 1 at m = 0.
Sources: the phrase is undefined in the plan; it appears verbatim in layered_plan_v1_original.md:77 (sha256 5d7fd64f76259b0a9e39543aec217c718ebaac279d14b2f7972c62b39cd962f3), layered_plan_v2.md:108 (38ff7c2b7fa8b102b10cb11002070a8cb450646a72b2720b55f8b5c30499d9ab), layered_plan_v3.2.md:135 (v3_2b, 5e5891bb55fc5449965f7efba8482bfecd135c30172f770d7dc65564db4902dd) and layered_plan_v3.3.md r2:136 (89b3972a0af418bfcb260b978842e79dc73945c61ec2bd85fe3a5e7d1785aa39); paper main cc2cc5c8 (8cbb94ec481b3332f074ea028505478dd2d576a8b5d60915f072b653ab6aad70) line 534 says the Wilson layers are "at a fixed angle phi"; line 531 the hop layers have nu^2 + m^2 = 1, so nu_S = 1 at m = 0. The Grok bot knows of no other meaning.

## Pre-declared deviations and readings
- DEV-1 (formula normalisation). The design's printed c0(phi2,phi4) (line 47) carries an overall 1/2; at phi2 = phi4 it equals sqrt(1+3 sin^2 phi) = 2 c0(phi), contradicting the design's own line 48 ("reduces to the line above at phi2 = phi4"). R2's pass rule is applied to the factor-1/4 form, which does reduce to c0(phi); |v0 - literal| is also recorded. Fixed in expected.json before any computation.
- DEV-2 (portability). Run on bigbang with the L1.2 venv (Python 3.12.3, numpy 2.5.4) used read-only; inputs copied from the box into inputs/.
- DEV-3 (S3 split). S3 is executed as S3a (primary: N1-N3 and verdict components), S3b (labelled cross-check against frozen U_cycle; script written only after S3a, frozen module copied into frozen/ only after the primary hash is recorded), S3c (N4/N5 records and result.json assembly). One attempt each.
- DEV-4 (gating). Stop rule read conservatively: a FAIL of S0 (P1-P4), S1 (R1) or S2 (R2) stops later steps (the primary refuses and records the refusal).
- Disclosure: before hashing, the primary was byte-compiled and called once on 3 arbitrary k values to check array shapes only (printed shape (3,4,4)); no value was compared with anything.
- Measurement reading: omega_min = min |omega| over the 4 eigenvalues of U; v0 = Neville extrapolation in kappa^2 through all four kappas; lower orders recorded as diagnostics.
- ||.||_inf in P1/N1 = max absolute row sum of (M^dag M - I) (stricter than max entry).
- N2 'nonzero' threshold 1e-4; N3 strict monotonicity requires a gap > 1e-6 between consecutive phis (over all directions).
