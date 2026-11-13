# CHANGES v3.3 r2 → v3.4 (DRAFT, 2026-11-12)

v3.3 r2 is unchanged at `../layered_plan_v3_3_r2_20261111/layered_plan_v3.3.md` (sha256 `89b3972a0af418bfcb260b978842e79dc73945c61ec2bd85fe3a5e7d1785aa39`). The exact diff is `plan_diff_v3.3_to_v3.4.txt`. v3.4 is a draft until Edmond signs it off, and no PDF has been built for it.

## Edmond's decisions applied (plan review B1–B4, 2026-11-12)

| Decision | Applied in |
|---|---|
| B1: `dirac4` gates L1.1; OP4's three extra nodes are a diagnostic finding | §2 (canonical rule), §1 L1 row, L1.1 setup, pass, status, decision; L1 exit gate; §8 row 3 |
| B2: all OP4-rule and OP4-bridge results are to be redone on `dirac4` | §2 consequence paragraph; §5 note; §6 note; §10 annotations; L1.5 status |
| B3: load-free carve-out for L1.1–L1.3 | §0.1 rule 1 exception |
| B4 (as clarified): the official V5 v2 census is accepted as the L1.1 census of `dirac4`; nothing is re-run; L1.1 is closed | L1.1 status; L1 exit gate; §8 row 3; §11 item 2 |

**Readings to confirm.** B2 "all to be redone" is read as: every result whose harness uses the OP4 rule or its continuum bridge (G1 0.970 and photon bending, the M3 generation split, the OP4 node findings, the held L1.5 design). Items that use neither OP4 nor the §6.2 node symbol (G3, M1, M2, C1–C4) are not changed. B4 had two readings in chat ("yes rerun is needed", then "you accepted L1.1"); the last message is taken as accepting the V5 v2 census with no re-run, which is what this draft says. If the first reading was meant, only the L1.1 status paragraph, the L1 exit gate, §8 row 3 and §11 item 2 change.

## Stale text fixed (no new decision)

- Frozen conventions: integer hops in units of a/2, one BCC orbit; the ℓ_P question is carried as open.
- L1.1: "Current result" paragraphs marked superseded or diagnostic; the decision paragraph replaced by the recorded decision; setup and pass updated; §10 V3 paragraph and `g(k)` repair marked superseded and withdrawn.
- §8 row 3 and §11 (sprint items 2 to 5, realistic L1 close) updated; the 4 to 6 week estimate is withdrawn.
- L1 exit gate rewritten to match.

## Results recorded

- L1.2: CLOSED (run `7e09b7c4`, PRs #5 and #6).
- L1.3: OPEN. Run `9ccf4855`, PR #8: R1 PASS, R2 FAIL / OPEN (recorded as open as written, Edmond 7:55 PM), S3 not run. The design prefactor error and the unscored follow-ups are stated. The corrected L1.3b is designed (PR #10) and awaits approval of its hash. The naming difference between ν_S and ν = cτ/a is added.
- L1.5: the 0.385κ prediction is labelled as an OP4 analysis; a `dirac4` hypothesis is stated as a hypothesis, not a result.

## Added (new sections)

- §0.5 and §0.6: **proposals awaiting Edmond's confirmation** (reproduction conventions; pilot-then-freeze, design dry-run, approval packet, stop rule, pre-registration governs).
- §0.7: decision log (factual).

## Not changed

L2 to L5 content, Appendix A, §9 interface contract, the §0.3 targets, and the README pointer (the README still names signed-off v3.3 r2 as the live plan until v3.4 is signed off).
