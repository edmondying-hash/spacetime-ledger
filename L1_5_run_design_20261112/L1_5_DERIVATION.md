# L1.5 hand derivation for the canonical rule `dirac4`: the linear term

Status: **derivation, not a run result.** It supports the design in `L1_5_RUN_DESIGN.md` and is part of the same hashed folder. Every numerical statement here comes from the unscored dry-run in `dryrun/` (outputs sit beside the scripts). Nothing here counts toward a gate.

Rule: paper §6.2 (Table `dirac4`), equal Wilson angle φ on both Wilson layers, massless unless said otherwise. Frozen module: `dryrun/frozen/dirac4.py`, sha256 `f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff` (the module used in the L1.3b run). k is in radians per a/2 and κ = |k|, as in L1.3 and L1.3b; kℓ = √3 κ. e^{−4iω} is an eigenvalue of U(k), ω per layer.

Proof status marks: **[P]** proved by hand below and also checked on random inputs in dry-run A; **[C]** computed numerically only; **[F]** closed form found from the numbers and checked, not proved.

## 1. Notation

With u, n the real functions of the paper (u = cx cy cz − ε sx sy sz and the three components of n), A^ε = u − i n·σ ∈ SU(2), S^ε = diag(A^ε, A^ε†) at m = 0, T = σ_x ⊗ 1, X^ε = u T + σ_y ⊗ (n·σ) with (X^ε)² = 1, V^ε = (cos φ − i sin φ X^ε)(cos φ + i sin φ T), and U = V⁻ S⁻ V⁺ S⁺. Write X = V⁻S⁻ and Y = V⁺S⁺, so U = X Y.

## 2. Two exact identities

**(I1) Reflection k → −k [P].** Under k → −k the cosines are even and each sine is odd, so u^ε(−k) = u^{−ε}(k) and n^ε(−k) = −n^{−ε}(k). Hence

- A^ε(−k) = A^{−ε}(k)†;
- S^ε(−k) = T S^{−ε}(k) T (T swaps the two blocks of S; this also holds at m ≠ 0, because the mass block is symmetric under the swap);
- X^ε(−k) = T X^{−ε}(k) T (σ_x σ_y σ_x = −σ_y), and T commutes with (cos φ + i sin φ T), so V^ε(−k) = T V^{−ε}(k) T.

Therefore U(−k) = (V⁻S⁻)(−k)(V⁺S⁺)(−k) = T (V⁺S⁺)(V⁻S⁻) T = T Y X T. Since Y X = X⁻¹(X Y)X,

  **U(−k) = (T X⁻¹) U(k) (T X⁻¹)⁻¹.**

So U(k) and U(−k) have the same spectrum, for every k, every m and every φ, provided the two Wilson layers carry the same angle. The step "V⁺ and V⁻ interchange under k → −k" is exactly where equal angles are used; with two angles (φ⁺ ≠ φ⁻) it fails (§6).

**(I2) Reality [P].** Let Q = σ_z ⊗ σ_y. For any SU(2) matrix B, B* = σ_y B σ_y. Hence Q S^ε Q⁻¹ = (S^ε)* (the block-diagonal part gets σ_y B σ_y, and at m ≠ 0 the off-diagonal mass block flips sign under σ_z exactly as its complex conjugate flips i). Also Q T Q⁻¹ = −T and Q X^ε Q⁻¹ = −(X^ε)*, so Q V^ε Q⁻¹ = (V^ε)*. Therefore

  **Q U(k) Q⁻¹ = U(k)\*,** with Q constant, for every k, m and φ (no equal-angle condition needed).

The eigenvalues of U(k) are therefore closed under complex conjugation: the eigenphases come in pairs ±θ. At k with the four phases (−θ₂, −θ₁, θ₁, θ₂) this is the pairing seen in every census.

Dry-run A checks all of these on 200 random (k, φ), both ε, to 4.5e-16 (identities) and 1.3e-15 (spectra), and shows that the frozen module and the analytic construction used here agree exactly.

## 3. Consequences for the dispersion relation

Near k = 0, U(0) = 1 (each factor reduces to the identity) and U(k) = e^{−4iH(k)} with H(k) Hermitian and analytic. Along a line k = κ n̂ the four eigenvalues of H(κ n̂) are analytic functions of κ (Rellich), also through κ = 0. At first order the eigenvalues of H₁ are ±c₀κ, each twice, with c₀(φ) = ½√(1+3 sin²φ) (L1.3b). Call the two positive branches p₁, p₂ and the two negative branches n₁, n₂.

**(C1) [P]** The band set at κ n̂ equals the set at −κ n̂ (I1) and is closed under ω → −ω (I2). Take the analytic continuation of a positive branch to −κ: p_j(−κ) = −c₀κ + … lies in the negative family at κ, and by (I2) the negative family is {−p₁, −p₂}. So p_j(−κ) = −p_{σ(j)}(κ) for a permutation σ of {1,2}. Two cases:

- σ = identity: each branch is an odd function of κ, ω_j = c₀κ + d_j κ³ + e_j κ⁵ + …;
- σ = swap: p₁(−κ) = −p₂(κ), and the branches can differ by ±β κ², ±γ κ³ …, i.e. a split by a term of even degree.

In both cases the **band mean** ω̄ = ½(p₁ + p₂) is an odd function of κ:

  **ω̄(κ n̂) = c₀κ + a₂ κ³ + a₄ κ⁵ + …, no term of even degree in κ, to all orders.**

In terms of the group velocity: no term of the form v = c₀(1 + ξ₁' κ), and none of any odd power of κ, in the mean over the two branches. This is the linear-term cancellation that §7.8 Test 3 of the paper describes ("alternating the two handednesses cancels the linear term exactly in every direction"), now with its mechanism: it is a symmetry of the alternating rule, and it needs the same angle φ on both Wilson layers. A "Wilson layer that removes the doubler modes keeps this cancellation" holds because V⁺ and V⁻ carry the same φ.

**(C2) [C] What the symmetry alone leaves open.** In the swap case the two branches could split at O(κ²) with opposite signs, ±β κ² (a helicity-dependent linear term, which the mean does not see). The symmetry does not exclude that, so it is checked directly:

- Second-order degenerate perturbation theory: the O(κ²) shifts of the +c₀κ pair are the eigenvalues of P₊H₂P₊. Dry-run C extracts H₂ from the analytic symbol (FFT on a circle in complex κ, matrix logarithm as a series) and finds both eigenvalues zero, max 2.9e-15, in 32 signed directions at φ = 1.4 and φ = 0.8.
- Dry-run B (50 digits, 26 signed directions, six φ): the coefficient of κ² in ω̄ is below 5e-22, and the splitting between the two branches is zero on [100] and [110] and grows as κ⁵ elsewhere (fitted exponent 5.0 at two directions). So the branches differ only at O(κ⁵).

Consequence: for the massless `dirac4` excitation at equal angles, the leak coefficient ξ₁ is zero (not merely small) in every direction. This agrees with the L1.3b R2c record (|b| ≤ 1.7e-10 at equal angles).

## 4. The quadratic term and its direction dependence

**Form of the κ³ term [P, symmetry argument].** ω̄ = c₀κ[1 + ξ₂'(n̂) κ² + O(κ⁴)]. ω̄² agrees with the analytic mean ½(p₁² + p₂²) up to O(κ¹⁰) (the branches differ at O(κ⁵) at most), so its κ⁴ part is a homogeneous quartic polynomial in k, invariant under the cubic group with inversion. The only such forms are α + β q, where q = n_x⁴ + n_y⁴ + n_z⁴ (with |n̂| = 1). Hence ξ₂'(n̂) = α(φ) + β(φ) q.

**Closed form [F].** Dry-run B finds, at six values of φ and 13 directions (50 digits),

  ξ₂'(n̂, φ) = −(1 − q)/3 − (3/8) sin²φ cos²φ / (1 + 3 sin²φ),

matching the extracted coefficients to 3e-19 (the limit of the 12-point fit), i.e. β/c₀ = 1/3 for every φ and α(φ) = −1/3 − (3/8) sin²φ cos²φ/(1+3 sin²φ). I found this form by inspecting the pilot numbers and then checking it at all 78 (φ, direction) points; it is a conjecture until a proof is written, and the design treats it as a pre-registered prediction, not an established result. Consequences:

- on [100] (q = 1) the coefficient is −(3/8) sin²φ cos²φ/(1+3 sin²φ) (0.0027 at φ = 1.4), on [110] (q = 1/2) it is −1/6 plus that, on [111] (q = 1/3) it is −2/9 plus that;
- the axis-to-body-diagonal difference ξ₂'(100) − ξ₂'(111) is exactly 2/9 for every φ, so the speed difference between axis and body diagonal is 3 × 2/9 κ² = (2/3) κ² = (2/9)(kℓ)²;
- the largest |ξ₂'| over directions and over the six tabulated φ is 0.2615 (φ = 0.5, [111]); at φ = 1.4 it is 0.2249. The paper's Test 3 quotes |ξ₂| ≤ 0.23 in the convention E/E_P = κ; the φ = 1.4 value 0.2249 is consistent with that, and the E_QG,2 implied by it is 1.8×10¹⁹ GeV, the paper's quoted ≳ 1.8×10¹⁹ GeV.

**A finding about the paper text.** Open-problem and limitations text (paper line 1253) says that for the wave rule and for the layer-alternating Dirac rule the direction dependence is "(E/E_P)²/18". 1/18 is the axis-to-body-diagonal difference of the scalar wave rule in (kℓ)² (1/24, 1/12, 7/72). For `dirac4` the difference measured here is 2/9 in (kℓ)² (equivalently 2/3 in κ²). The factor 4 in (kℓ)² (12 in κ²) is not explained by any convention I can identify without the open ℓ_P item; this is recorded for the paper-conventions item, not decided here.

## 5. What this derivation does not show

- It is about the massless `dirac4` excitation. The paper's photon is not a rule of this lattice model; §7.8 Test 3 uses the massless Dirac walker as the proxy, and so do I. A genuine vector or tensor field built on this rule is not defined and is not covered.
- It is about equal Wilson angles, the canonical rule. The L1.3b observation of a linear term for φ⁺ ≠ φ⁻ is consistent with (I1) failing there, §6.
- It does not use a load term. With a uniform load U₀ the paper's load-first rule rescales time, ω → e^{−U₀}ω, which multiplies c₀ and leaves the dimensionless coefficients ξ₁', ξ₂' unchanged. Load that varies in space is not part of the free spectrum.
- The O(κ⁵) branch splitting and the ξ₂' closed form are numerical.
- Whether the E/E_P ↔ κ identification is right is the open ℓ_P item. The design reports the result in four conventions.
- It says nothing about the OP4 rule. The 0.385κ leak and the "ℓ ≲ 0.26 ℓ_P" scale in the plan belong to the OP4 diagnostic branch and were not re-derived here.

## 6. Contrast: two Wilson angles

For φ⁺ ≠ φ⁻ the identity (I1) fails: the eigenphase sets of U(k) and U(−k) differ (dry-run A6: 0.66 rad at (0.5, 1.3) and 0.086 rad at (0.9, 1.0); 1.3e-15 at equal angles). (I2) still holds, because V* = (cos φ + i sin φ X*)(cos φ − i sin φ T) for any φ. This is the mechanism behind the linear term the L1.3 follow-up and the L1.3b record (R2c) found at unequal angles on [110] and [111] and not on [100]. It only matters for L1.5 as the statement that the cancellation is conditional on equal angles.

## 7. Files

`dryrun/` holds `l15_lib.py`, four scripts, their outputs, and `expected_pilot.json` (pilot values, 20 digits). `dryrun/frozen/dirac4.py` is the frozen module. These scripts are the reviewing agent's own, written for this derivation; the run is to use its own measurement code (design §6).
