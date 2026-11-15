# L0' definition of a "real problem" with the simple cubic (6-face) grid

Prepared by spacetime with helper's criteria, 2026-11-14. Source draft sha256 1ae63c1970aa5e6ada88f7fa2ccd9c658c63f2e5d453a549b9bee556c298a7fe; F2 worded per Edmond's 11:08 ET ruling on the checkerboard sign.

## Scope
Every candidate rule is scored against the same gates, including the baseline, BCC/dirac4 (8 corner hops) as recorded on main. The simple cubic candidates are Wilson, staggered, a 4-component dirac4 analogue, and split-step.

## Hard gates (failing any one disqualifies a candidate)
- F1 Species. At low energy there is exactly one light Dirac/Weyl species. Any extra species must be lifted to the Planck scale by a declared repair term, and every gated result must be insensitive to that term across a range stated before scoring.
- F2 Bias. One species is reached without a preferred sublattice or a fixed direction, and without any position-dependent sign pattern other than a checkerboard sign. A checkerboard (staggered) sign is not counted as a bias.
- F3 Reversibility. The rule is unitary and reversible.
- F4 Dispersion. There is no term linear in k. Any direction-dependent term goes as (k l)^2 or smaller and stays within the Fermi/LHAASO bounds.
- F5 Isotropy. A new pre-registered large-scale test must show anisotropy decaying as its gate requires. It measures how far a point-source front leaks outside the c0*n sphere, and the angular spread of the static load field as a function of r.

## Knob rule
A declared continuous knob is allowed only if every gated result is insensitive to it across the pre-stated range. Having to tune a knob to pass is a fail (checklist 1 and 7).

## Simplicity test
The baseline dirac4 has 4 components and 2 declared knobs (phi and the Wilson r). A simple cubic rule passes only if it has at most 4 components and at most 2 declared knobs.

## Trigger
The fallback to BCC/dirac4 applies if no simple cubic candidate passes F1-F5, the knob rule and the simplicity test. The outcome is to be read alongside how the BCC baseline itself scores on the same gates.

## Timebox
One census round over the four pre-listed candidates, plus at most one pre-registered repair round. Every failed run is kept on record.

## Not a real problem
- (k l)^2 anisotropy within bounds
- axis/diagonal ordering reversed relative to BCC
- no prior citation for the rule
- BCC numbers in the paper that need rewording
