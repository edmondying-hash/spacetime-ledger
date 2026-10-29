---
title: "The Quantized Space-Ledger: Locating Quantum Non-Locality in a Discrete Spacetime Substrate"
subtitle: "A speculative client–server framework for quantum foundations"
author: "Edmond"
date: "October 2026"
geometry: margin=1in
fontsize: 11pt
colorlinks: true
header-includes:
  - \usepackage{amsmath,amssymb,braket}
  - \usepackage{float}
  - \floatplacement{figure}{H}
---

## Abstract

Quantum foundations still wrestle with wave–particle duality, the measurement problem, Bell non-locality, and the apparent retrocausality of delayed-choice experiments. This paper proposes a speculative, information-theoretic framework in which these puzzles are reorganized around a single hypothesis: **spacetime itself is a discrete, entangled network of quantized nodes (a "Space-Ledger") that carries the quantum state.** We describe the framework with a client–server analogy. The observable universe of matter, signals and detectors is the *client side*: it is local, and propagation within it is bounded by the speed of light, with massive "apps" running slower than massless ones. Spacetime is the *server side*: the ledger, operating at a scale approaching zero length (the Planck regime), where the global state, including entanglement and Bell correlations, is held. In this picture non-locality is not eliminated; it is *located* in the substrate, while the client side keeps no-signaling. We show that the framework reproduces the standard, non-retrocausal account of the delayed-choice quantum eraser. We also identify a route to falsifiability: if the ledger is discrete at the Planck scale, it may produce energy-dependent photon dispersion, which current gamma-ray-burst observations already constrain tightly.

---

## 1. Introduction: Moving Superposition into Spacetime

For over a century the double-slit experiment has been the foundational puzzle of quantum mechanics. With no which-way measurement, single quanta build up an interference pattern on a screen; with a which-way measurement, the pattern becomes two classical bands.

Many interpretations place the burden of this behavior on the particle itself or on its wavefunction (e.g., collapse in Copenhagen-style accounts, or branching in Many-Worlds). This paper explores an alternative: **the wavefunction belongs to spacetime, not to the particle.** The quantum state is the state of the Space-Ledger, a network of space "pixels." What we call a "particle" is the localized excitation that is *returned by a read-out* to the client side when the ledger is queried by a measurement-like interaction.

Under this hypothesis spacetime is not an empty, continuous stage. It is a **quantized, highly entangled computational network**. Superposition, interference and decoherence are properties of the ledger state; the localized particle is how that state shows up to client-side observers.

A further working principle is that the model admits no physical infinities. A fixed node size sets a minimum distance (the Planck length), and a finite workload per node sets a maximum density and curvature. The ledger is therefore offered as a potential candidate for a framework without singularities, and possibly with a natural ultraviolet cutoff (Sec. 6).

### 1.1 The Client–Server Picture

We organize the framework around two layers:

| Layer | What lives there | Rules |
| :--- | :--- | :--- |
| **Server side** (spacetime / ledger) | The global quantum state, phases, entanglement, Bell correlations | Operates at a scale approaching zero length (Planck regime); state is global and not decomposable into local pieces |
| **Client side** (observable universe) | Matter, signals, detectors, records, observers | Local; nothing propagates faster than $c$; massive excitations propagate at $v < c$, massless ones at $c$ |

: The two layers of the client–server picture.

A useful analogy: the server holds a shared database; each client can only read what it queries locally, and can only talk to other clients through channels capped at $c$. This analogy is a guide to intuition, not a derivation. In this picture the client-side cap at $c$ is a potential candidate for the maximum propagation speed of the server network itself, one node spacing per update tick ($c = \ell_{\text{Planck}}/t_{\text{Planck}}$; Sec. 6.1).

---

### 1.2 Why Discreteness?

The ledger assumes spacetime is made of discrete nodes rather than a true continuum. This is a hypothesis, but three independent lines of physics hint in that direction.

1. **Black-hole entropy and the Bekenstein bound.** Bekenstein (1973) proposed that a black hole carries entropy proportional to its horizon area, and Hawking's (1975) discovery of black-hole radiation fixed the coefficient: $S = k_B A / (4 l_P^2)$, where $l_P$ is the Planck length. Read as a bound, the information that can be stored in a region is capped by its boundary area measured in Planck units. A finite cap on information suggests a finite number of degrees of freedom per region, which is what a discrete network would supply and a true continuum would not.
2. **Ultraviolet divergences.** In quantum field theory, many calculations diverge at arbitrarily short distances (high momenta). They are handled by imposing a cutoff and renormalizing. A physical minimum length would provide a natural cutoff instead of an artificial one.
3. **An operational limit.** To probe a distance $\Delta x$ requires a probe of energy roughly $\hbar c/\Delta x$. Below about $l_P$, that energy concentrated in that region would form a black hole and hide what it was trying to measure. Arguments of this kind, including generalized uncertainty principles, suggest a minimal measurable length near the Planck scale (reviewed by Garay, 1995, and Hossenfelder, 2013).

**The model's position.** Continuous coordinates are a large-scale approximation, like a smooth photograph that is actually made of pixels. Zooming in does not go on forever: it terminates at the Planck scale, and below that, "distance" has no physical meaning in the model.

**Refinement: an organized, rigid grid.** We take the nodes to form an organized, rigid, cube-like network: the body-centred cubic (BCC) grid with 8 links per node, used in the simulations of this paper. The nodes are fixed in place; they do not move or fluctuate. A regular grid has preferred directions and could in principle pick out a preferred frame. However, link-only path sums on this grid leave a direction dependence of $c$ only at order $(E/E_P)^2$ (Sec. 6.1), far below current bounds. A random, causal-set-like arrangement (Bombelli, Lee, Meyer and Sorkin, 1987; Bombelli, Henson and Sorkin, 2009) remains a fallback if boost invariance requires it (Sec. 7.3, open problem 13).

**Uncertainty at the node scale.** On a discrete network, position and momentum cannot both be resolved below the node scale: there is no finer position to assign, and no shorter wavelength the network can carry. This matches the minimal-length and generalized-uncertainty-principle arguments above (Garay, 1995; Hossenfelder, 2013), which add a Planck-scale correction to Heisenberg's relation. This is a resolution limit, not a fluctuation: the nodes themselves are rigid and fixed, and they do not jitter. Quantum uncertainty of particles remains the ordinary quantum mechanics of client states. At every scale accessible to experiment, the standard Heisenberg uncertainty relation $\Delta x\,\Delta p \ge \hbar/2$ holds unchanged, and the model does not alter it there.

**Discrete is not the same as finite in extent.** Whether spacetime is continuous and whether the universe is infinite are separate questions. Discreteness limits how *finely* spacetime can be divided. By itself it implies nothing about the universe's total size, and the model makes no claim about that here.

## 2. Mathematical Framework: A Tensor-Network Description

To formalize the picture we use discrete **graph theory** and **tensor networks** (in the spirit of Matrix Product States or MERA). The mathematics below is standard quantum mechanics written in a node-based language; the novel physical content of the proposal lies in the interpretation and in the discreteness hypothesis of Section 7.

```
     (Node A) ======= [Entanglement Bond] ======= (Node B)
        ||                                           ||
   [Phase State: phi_A]                        [Phase State: phi_B]
```

### 2.1 Node Definition and State Spaces

Let spacetime be modeled as an **undirected** graph $G = (V, E)$, where $V$ is the set of quantized spacetime nodes (pixels) and $E$ is the set of entanglement bonds between them. Bonds are undirected because entanglement is symmetric: if node $A$ is entangled with node $B$, then $B$ is equally entangled with $A$. (The direction of time enters only through the update rule of Sec. 2.2, not through the bonds.) Each node $v_i \in V$ carries a finite-dimensional Hilbert space $\mathcal{H}_i$.

The ledger state of a region of space lives in the tensor product of these local spaces and is specified by the **network tensor** $T$:

$$\ket{\Psi_{\text{space}}} = \sum_{j_1, j_2, \dots, j_n} T_{j_1 j_2 \dots j_n}\, \ket{j_1} \otimes \ket{j_2} \otimes \dots \otimes \ket{j_n}$$

where:

- $j_i$ is the discrete excitation or phase index of pixel $v_i$;
- $T_{j_1 j_2 \dots j_n}$ is the network tensor. Its factorization into smaller tensors contracted along the bonds in $E$ encodes the entanglement layout of the grid.

This $\ket{\Psi_{\text{space}}}$ *is* the wavefunction in this framework: a property of spacetime, held server-side.

### 2.2 Excitations and Their Propagation

A particle is not an autonomous object sliding across a continuous plane. It is a localized excitation of the ledger. Creating a particle at node $v_a$ is represented by a creation operator $\hat{\Phi}^\dagger_a$ acting on the ledger:

$$\ket{\Psi(t)} = \hat{\Phi}^\dagger_a \ket{\Psi_{\text{space}}}$$

Time advances in discrete network clock cycles, $\Delta\tau \approx t_{\text{Planck}}$. Each cycle applies a unitary network update operator $\hat{U}_{\text{net}}$:

$$\ket{\Psi(t + \Delta\tau)} = \hat{U}_{\text{net}} \ket{\Psi(t)}$$

Because $\hat{U}_{\text{net}}$ is built from local gates along the bonds of $T$, the *amplitude* for the excitation spreads along all open routes in $E$. To be clear about what spreads: it is the ledger state (the server-side wavefunction) that develops support on many routes. No client-side observer ever sees a "smeared" particle; a client only ever registers a localized excitation when it queries the ledger (Sec. 3.3).

Locality on the client side is built into this structure: $\hat{U}_{\text{net}}$ couples only neighboring nodes per cycle, so the light-cone has a maximum slope of one node per cycle, which we identify with $c$. Massive excitations, whose dispersion relation contains a rest-energy term, have group velocity $v < c$, matching the "app speed depends on mass" intuition.

---

## 3. The Double-Slit Protocol: Topological Routing

### 3.1 Unmeasured State: Open Topology

When a single excitation approaches two open slits with no which-way device, the node pathways through Slit 1 ($V_{\text{slit1}}$) and Slit 2 ($V_{\text{slit2}}$) both remain coherently bonded to the rest of the network.

1. **Distributed phase updates.** Successive applications of $\hat{U}_{\text{net}}$ give the ledger state support on both $V_{\text{slit1}}$ and $V_{\text{slit2}}$.
2. **Phase interference.** Beyond the slits the two contributions overlap. The probability that screen node $x$ registers the excitation is

   $$P(\text{detection at node } x) = \left| \bra{x} \hat{U}_{\text{net}} \tfrac{1}{\sqrt{2}}\left(\ket{V_{\text{slit1}}} + \ket{V_{\text{slit2}}}\right) \right|^2$$

   The cross term between the two paths produces the usual interference fringes, because the ledger sums the amplitudes for both pathways before any client-side read-out.

### 3.2 Measured State: The Which-Way Anchor

A which-way detector is a macroscopic system whose nodes are already strongly coupled to the environment. Placing one at Slit 2 couples the detector space $\mathcal{H}_{\text{det}}$ to the nodes $V_{\text{slit2}}$:

$$\ket{\Psi_{\text{interaction}}} = \alpha \ket{V_{\text{slit1}}}\ket{0}_{\text{det}} + \beta \ket{V_{\text{slit2}}}\ket{1}_{\text{det}}, \qquad |\alpha|^2 + |\beta|^2 = 1$$

Since $\braket{0|1}_{\text{det}} = 0$, the cross term at the screen vanishes, and the screen sees no fringes.

### 3.3 Collapse in the Ledger Picture: Decoherence plus Read-out

We split "collapse" into two steps, and we are explicit about which step is explained and which is postulated.

**Step 1: Decoherence (server side, explained).** The detector state does not stay isolated; it quickly becomes entangled with many environment nodes $\ket{E_0}, \ket{E_1}$:

$$\ket{\Psi} \to \alpha \ket{V_{\text{slit1}}}\ket{0}_{\text{det}}\ket{E_0} + \beta \ket{V_{\text{slit2}}}\ket{1}_{\text{det}}\ket{E_1}, \qquad \braket{E_0|E_1} \approx 0$$

The reduced state of the system and detector is then

$$\rho \approx |\alpha|^2 \ket{V_{\text{slit1}},0}\bra{V_{\text{slit1}},0} + |\beta|^2 \ket{V_{\text{slit2}},1}\bra{V_{\text{slit2}},1}$$

In ledger language, the phase correlation between the two routes has not been destroyed. It has *spread out into a huge number of environment nodes*, where no local client can practically gather it back. The off-diagonal terms vanish for every practical local query. This is standard decoherence theory, restated.

**Step 2: Read-out (server side, postulated).** Decoherence explains why the alternatives stop interfering. It does *not* by itself explain why one definite outcome occurs. The framework adds an explicit postulate, stated as a server-side read with three operations:

> **Read-out postulate.** When an irreversible, decohered record is created, the server performs one read: (i) *sample*: draw one outcome $k$ with weight $p_k = |c_k|^2$ from the decohered ledger state; (ii) *lock*: write $k$ into the ledger, so later reads of the same record return the same value; (iii) *return*: deliver $k$ to the client side.

Seen from the client side, the sample–lock–return sequence is the Born rule, and the returned outcome is what clients experience as a "particle at a place." We stress that this is a postulate, not a derivation: the squared-amplitude weights (equivalently the $\cos^2$ odds in the Bell tests of Sec. 5) are put in by hand. Whether they follow from the ledger is the subject of the energy-share test (open problem 27), which stores link amplitudes with energy $\propto$ amplitude$^2$ and reads by energy share without inserting $\cos^2$; until it reports, $\cos^2$ remains a postulate. Deriving the read-out rule from the structure of $T$ and $\hat{U}_{\text{net}}$ (for example via symmetry or envariance-type arguments, or a typicality argument over ledger microstates) is the main open problem of the framework.

**Measurement as interaction-triggered queries.** In this model, measurement does not require a conscious observer. Any physical interaction whose cascade of effects records information about a state in its environment acts as a query to the server and yields a definite client-side outcome. Stated more carefully: client-observable events correspond to measurement outcomes of server-side quantum evolution. This is the ledger reading of decoherence (Zurek, 2003) and quantum Darwinism (Zurek, 2009). An example is Einstein's question to Pais of whether the Moon exists only when someone looks at it (Pais, 1979). The Moon is continuously scattered by sunlight, cosmic microwave background photons and other particles, so in ledger terms it is queried continuously and remains definite whether or not anyone observes it. *Caveat:* decoherence accounts for the suppression of observable superpositions, but it does not by itself select a single outcome (Step 2 above). The paper remains neutral among interpretations, such as Copenhagen and many-worlds, on how that selection is understood.

#### Why the Read-out Is the Square

The read-out postulate uses the squared amplitude $|c_k|^2$. This subsection collects standard reasons for that choice and adds a small numerical check of alternatives. *It does not derive the rule from the ledger; it narrows what such a derivation has to supply.*

**A computing analogy.** In a neural network, an activation function such as softmax is applied once, in the final layer, to turn internal scores into output probabilities. Here the squared amplitude plays the analogous role: server-side amplitudes are added and evolved linearly, and the square is applied once, at client-side read-out. The question is then why this output layer is $|a|^2$ rather than some other function.

**(1) The Pythagoras picture.** Amplitudes add like arrows (complex numbers, or vectors in a Hilbert space). For arrows, the squared length is the quantity with two special properties.

- *It is invariant under rotations.* A change of measurement basis is a unitary transformation, a rotation of the arrow, and leaves $\sum_k |c_k|^2$ unchanged.
- *It adds over exclusive outcomes, as Pythagoras' theorem does over perpendicular sides.* If two detectors are merged, the merged probability is the sum of the two, $|c_1|^2 + |c_2|^2$. Totals stay at 100% however the detectors are split or merged.
- *Other powers lack these properties.* The sum of cubed (or first-power) components changes when the arrow is rotated, so its probabilities would depend on how the detector set is drawn rather than only on the state.
- *The square mixes paths only in pairs.* $|a_1 + a_2 + a_3|^2$ contains single-path terms and pairwise cross terms $2\,\mathrm{Re}(a_i a_j^*)$, but no genuinely three-path term. The square therefore predicts zero third-order interference: Sorkin's parameter $\kappa$ vanishes in a three-slit experiment (Sorkin, 1994).

**(2) Gleason's theorem.** Gleason (1957) proved that in a Hilbert space of dimension at least 3, every probability assignment to measurement outcomes (closed subspaces) that is additive over orthogonal outcomes has the trace form $p = \mathrm{Tr}(\rho P)$. For a pure state this is $|c_k|^2$. Busch (2003) extended the result to dimension 2 by allowing generalized measurements (POVMs). Historically, Born (1926) introduced the probability interpretation as a postulate in his treatment of collision processes. It was soon confirmed by experiment, and Gleason's theorem later showed that, once the Hilbert-space structure and additivity are assumed, no other rule is available. *Gleason's theorem assumes the Hilbert-space structure and non-contextual additivity; it does not explain where they come from.*

**(3) A numerical check of alternative read-outs.** We computed double- and triple-slit Fraunhofer patterns with illustrative parameters. The total photon number was held fixed and each candidate rule was normalized over the screen. Three tests were applied:

- *Three-slit interference.* Sorkin's $\kappa$ at the central maximum, compared with the measured bounds $|\kappa| < 0.01$ (Sinha et al., 2010) and $\tilde\kappa_3 = (0.6 \pm 1.8)\times10^{-3}$ for single photons (Kauten et al., 2017).
- *Detector merging.* Amplitudes $(0.6, 0.48, 0.64)$, with the last two detectors merged.
- *Entangled-pair signalling.* The state $\cos\tfrac{\pi}{6}\ket{00} + \sin\tfrac{\pi}{6}\ket{11}$; Bob's marginal is compared for Alice measuring in $Z$ or $X$.

The results are summarized in Table \ref{tab:readout} and Figures \ref{fig:readout} and \ref{fig:readoutexp}.

\begin{table}[htbp]
\centering
\small
\caption{Alternative read-out rules tested against the square (illustrative geometry). Only the squared amplitude passes all three tests.}
\label{tab:readout}
\begin{tabular}{lccc}
\hline
Rule & $\kappa$ (centre) & $P_1$: 3 vs 2 detectors & Bob $P(0)$: Alice $Z$ vs $X$ \\
\hline
$|a|^2$ (Born) & $3\times10^{-16}$ & 0.360 / 0.360 & 0.750 / 0.750 \\
$|a|^1$ & $-4.0\times10^{-2}$ & 0.349 / 0.429 & 0.634 / 0.634 \\
$|a|^{1.5}$ & $-1.1\times10^{-2}$ & 0.355 / 0.394 & 0.695 / 0.695 \\
$|a|^3$ & $-5.5\times10^{-3}$ & 0.367 / 0.297 & 0.839 / 0.839 \\
softmax $e^{5|a|}$ & $+0.52$ & 0.361 / 0.269 & 0.854 / 0.785 \\
$e^{|a|}-1$ & $+0.16$ & 0.352 / 0.402 & 0.680 / 0.666 \\
$e^{|a|^2}-1$ & $+0.65$ & 0.362 / 0.326 & 0.797 / 0.774 \\
$2^{|a|}-1$ & $+0.10$ & 0.351 / 0.410 & 0.665 / 0.656 \\
\hline
\end{tabular}
\end{table}

- *Power rules.* $|a|^p$ with $p = 1, 1.5, 3$ gives $|\kappa| \approx 5\times10^{-3}$ to $4\times10^{-2}$ at the centre and about 0.1 averaged over the screen. These values exceed both experimental bounds. The power rules also change one detector's probability when other detectors are merged. They did not signal in this particular two-qubit example, because the amplitudes factorize there.
- *Exponential rules.* Softmax and exponential rules fail all three tests.
- *A softmax that recovers Born.* Softmax with logits $z_k = \log|a_k|^2$ reproduces Born exactly: the square can be written as a softmax, but only with these logits.
- *Small-amplitude limit.* A rule that matches Born at small amplitude, such as $e^{\beta|a|^2} - 1 = \beta|a|^2 + \tfrac{1}{2}\beta^2|a|^4 + \dots$, still carries an $|a|^4$ term. That term produces three-path interference that grows with intensity: $\kappa \approx 0.5\,\beta$, crossing the Kauten and Sinha bounds at $\beta \approx 0.004$ and $0.02$ (Figure \ref{fig:readoutexp}, panel d).
- *Dependence on amplitude scale.* Such rules also depend on the overall scale of $|a|$. Amplitudes are defined only up to normalization, so that scale carries no physical meaning.
- *Signalling.* Non-linear read-outs generally permit signalling through entangled pairs (Gisin, 1990; Polchinski, 1991), as seen here in Bob's shifted marginals.

\begin{figure}[tp]
\centering
\includegraphics[width=\linewidth]{readout_kappa.png}
\caption{Sorkin third-order parameter for alternative read-out rules. (b) $|\kappa|$ at the central maximum of a three-slit pattern for the Born rule, power rules and softmax rules, against the Sinha et al. (2010) and Kauten et al. (2017) bounds; Born values are round-off. (c) Softmax $e^{\beta|a|^2}$ versus $\beta$: at small $\beta$ the fringes wash out, and at large $\beta$ $\kappa$ is too large.}
\label{fig:readout}
\end{figure}

\begin{figure}[tp]
\centering
\includegraphics[width=\linewidth]{readout_exp.png}
\caption{Exponential read-out rules. (d) For $P \propto e^{\beta|a|^2}-1$, the three-slit $\kappa$, the detector-merging error and the entangled-pair signal all grow in proportion to $\beta$, i.e.\ to beam brightness, and cross the experimental bounds near $\beta \sim 10^{-2}$. (e) $|\kappa|$ at the central peak for several exponential rules at $\beta = 1$; only the square passes.}
\label{fig:readoutexp}
\end{figure}

**Consequence for the ledger.** Taken together, the square is the read-out consistent with rotatable arrows, with additive outcomes, with the three-slit bounds and with no-signalling. Open problem 1 (Sec. 9) therefore narrows. The remaining question is why server-side amplitudes behave like rotatable arrows, i.e.\ why the ledger's state space carries a complex Hilbert-space structure with unitary evolution. Given that structure, Gleason's theorem fixes the read-out. *This narrowing assumes non-contextual additivity of the read-out, which a concrete ledger model would still have to justify.*

*Remark: the server side's quantum-level work is geometric. Between queries, the server side evolves the state by length-preserving rotations (unitary evolution), and the read-out takes the squared length. On this picture the server side's quantum-level work is predominantly geometric: it rotates state vectors, much as a GPU performs matrix multiplications, with one squaring step at the output. This geometry lives in the abstract complex state space, not in ordinary 3D space. How the server side stores or distributes the state, for example in a tensor-network-like distribution across nodes, is left open.*


---

### 3.4 Repeated Queries: Zeno Dynamics and Query-Rate Limits (Hypothesis)

This subsection extends the query picture of Sec. 3.3 to repeated queries. The quantum mechanics is standard; the ledger reading is offered as a potential candidate interpretation, not as a result.

**Evolution between queries.** After a query, the state resumes evolving immediately, but gradually. For short times the probability of still finding the system in its post-query state is
$$P(t) \approx 1 - \left(\frac{t}{\tau_Z}\right)^2, \qquad \tau_Z = \frac{\hbar}{\Delta E},$$
where $\Delta E$ is the energy *uncertainty* of the state, not its total energy. An energy eigenstate has $\Delta E = 0$ and does not drift. If $N$ equally spaced queries are made over a total time $T$, the survival probability is
$$P \approx \left[1 - \left(\frac{T}{N\tau_Z}\right)^2\right]^N \approx \exp\!\left(-\frac{T^2}{N\tau_Z^2}\right) \;\longrightarrow\; 1 \quad (N \to \infty).$$
This is the quantum Zeno effect (Misra and Sudarshan, 1977). For other query rates, particularly in decaying systems, repeated queries can instead accelerate the transition (the anti-Zeno effect). At each query the Born rule keeps the outcome probabilities normalized. In the ledger reading, server-side evolution proceeds by local update rules that are independent of client queries; a query only sets the state from which the next stretch of evolution starts.

**Experimental evidence.**

- Itano, Heinzen, Bollinger and Wineland (1990) drove a radio-frequency transition in trapped beryllium ions and interrupted it with short laser measurement pulses. The transition was inhibited as the number of measurement pulses increased, in agreement with the Zeno prediction.
- Fischer, Gutiérrez-Medina and Raizen (2001) reported the first observation of both the Zeno and anti-Zeno effects in an unstable system: cold sodium atoms tunneling out of an accelerated optical standing wave. Repeated measurements during the initial nonexponential decay period suppressed or enhanced the decay, depending on the measurement frequency.
- Streed et al. (2006) observed both pulsed and continuous Zeno effects in a $^{87}$Rb Bose–Einstein condensate. The continuous and pulsed suppression matched when $\gamma\,\delta t = 3.60(0.43)$, in agreement with the predicted value of 4, and increasing the measurement rate suppressed the transition rate down to $0.005\,\omega_R$.
- Signoles et al. (2014) observed quantum Zeno *dynamics* in the 51-dimensional Hilbert space of a Rydberg-atom angular momentum $J = 25$: continuous selective interrogation confined the evolution to an adjustable subspace, producing "Schrödinger cat" superpositions.

**Query-rate limits.** Three limits bound how often a state can be queried or changed. (i) Signals between separated regions, including the records that a query produces, travel no faster than $c$. (ii) The Margolus–Levitin bound (Margolus and Levitin, 1998) limits the number of mutually orthogonal states a system can pass through per second to at most $2E/(\pi\hbar)$, where $E$ is the mean energy above the ground state. (iii) As a model assumption, each node performs at most one update per Planck time, $t_P \approx 5.4\times10^{-44}$ s, i.e. about $10^{43}$ updates per second per node. This last limit is a postulate of the ledger model, not an established result.

**Agreement between queries.** Simultaneous or immediately repeated queries of the same property return the same result (repeatability). In the ledger reading, this is because the committed result is copied redundantly into many environment records (quantum Darwinism; Zurek, 2009). Later queries can differ only after the state has drifted on the $\tau_Z$ timescale, or when a non-commuting property is queried. Which events count as "the same moment" depends on the reference frame, but the correlations between spacelike-separated queries do not depend on their order, as Bell tests confirm (Sec. 5). In summary, the observed variety of outcomes arises on the client side from how, when and which property is queried; the state, its energy spread and its correlations reside on the server side.

*Caveats. The Zeno formulas above are textbook quantum mechanics; the ledger model reinterprets them and does not change any prediction. The Planck-time update limit is an assumption with no direct experimental support, and it may need modification to remain compatible with Lorentz invariance (Sec. 7.3). Real measurements are of finite duration and strength, so the idealized instantaneous-query picture is an approximation.*

### 3.5 The Arrow of Time

**Server side: reversible.** $\hat{U}_{\text{net}}$ is unitary and therefore reversible: any server-side evolution can, in principle, be run backward, so the server's dynamics by themselves have no preferred direction. This is consistent with the time-symmetry of the fundamental microscopic laws (apart from a small time-reversal violation in the weak interaction, which does not account for the everyday arrow). Reversible does not mean the server is outside time. It still steps through its update cycles in order, as discussed in Secs. 4.2 and 5.4.

**Client side: the forward arrow.** On the client side, the forward arrow would emerge from never-ending queries to the server. Not just deliberate measurements, but every environmental interaction (a stray photon, a collision with an air molecule) decoheres states and copies committed results into many environment nodes (Sec. 3.3; quantum Darwinism, Sec. 5.3). These records accumulate and entropy grows, so committed results cannot practically be undone: reversing one would require recollecting and reversing every copy spread through the environment.

**A low-entropy start.** This account needs a boundary condition: the universe must have begun in a state of very low entropy, so that records and entropy had room to grow. This is often called the *past hypothesis* (Albert, 2000). Zeh (1989) gives a detailed treatment of how decoherence and such initial conditions together underlie the direction of time. The model does not explain why the initial state had low entropy.

**No retrocausality.** Reversibility on the server side does not let anything reach the client's past. The safeguards of Sec. 5.3 still prevent any signal from being sent, and, as in the delayed-choice analysis of Sec. 4, no later choice changes an earlier client-side record.

**Status.** This matches the standard decoherence and thermodynamic account of the arrow of time. The model's contribution is only to locate the pieces: reversibility on the server, and irreversibility in the client-side records.

### 3.6 Matter–Antimatter Asymmetry (Hypothesis)

*This subsection is speculative.*

**The observation.** The observable universe is made almost entirely of matter, with no significant primordial antimatter. The asymmetry is usually expressed as the ratio of baryons to photons, which is of order $10^{-10}$ (Canetti, Drewes and Shaposhnikov, 2012). Sakharov (1967) showed that producing such an asymmetry from a symmetric start requires three conditions: baryon-number violation, C and CP violation, and a departure from thermal equilibrium.

**Link to the arrow of time.** By the CPT theorem, the small time-reversal (T) violation in the weak interaction mentioned in Sec. 3.5 is equivalent to CP violation. The caveat in the arrow-of-time discussion and the matter surplus therefore share a common root.

**The honest problem.** The CP violation in the Standard Model is far too small, by many orders of magnitude, to produce the observed asymmetry (Canetti, Drewes and Shaposhnikov, 2012). Where the rest comes from is an open question in physics.

**Ledger hypothesis.** We propose that the server's update rule carries a small fundamental bias in how it processes matter versus antimatter excitations. This is consistent with Sec. 3.5: a unitary, reversible rule need not be T- or CP-symmetric, so a biased server is still a reversible one. A CP-violating phase of this kind needs at least three fermion generations (Kobayashi and Maskawa, 1973); if the generations are overtone modes of one node excitation pattern (Sec. 6.8), the three modes supply the minimum structure in which a CP-violating update bias can appear.

**Motivation: a selection argument.** No intent or design is implied. Without such a bias, matter and antimatter would have annihilated almost entirely into radiation, and the network would host no lasting client apps: no atoms, no stars, and no observers. Any universe in which observers can ask the question must therefore run on a biased server. This explains why we observe *a* bias, but not its *size*. Selection (anthropic) arguments are also debated, and many physicists regard them as a last resort rather than an explanation. A quantitative account of the bias is an open problem (Sec. 9).

## 4. Delayed Choice Without Time Travel

The delayed-choice quantum eraser (e.g., Kim, Yu, Kulik, Shih and Scully, *Phys. Rev. Lett.* 84, 1, 2000) is often presented as evidence that a later choice changes an earlier event. Standard quantum mechanics already explains it without retrocausality. In this section we show that the ledger framework reproduces that standard account in its own language. We do not claim it is the only way to resolve the puzzle.

### 4.1 What the Experiment Actually Shows

In the experiment, each photon pair consists of a *signal* photon, which goes to a screen detector $D_0$, and an entangled *idler* photon, which carries the which-way information and is detected later at one of several detectors. Some idler detectors preserve the which-way information; others ("erasers") combine the paths so that information is lost.

The key facts are:

1. **The signal screen never shows interference on its own.** The full pattern at $D_0$ is always a smooth, fringe-free sum, whatever happens to the idlers.
2. **Fringes appear only in sorted subsets.** Using coincidence counting, the $D_0$ hits are sorted by which idler detector fired. The subsets paired with the two eraser detectors show fringes and anti-fringes (shifted by half a period), which add up exactly to the smooth total. The subsets paired with the which-way detectors show no fringes.
3. **The sorting needs classical information.** Nobody at $D_0$ can see any fringes without first receiving the idler records through an ordinary channel limited by $c$.

### 4.2 The Ledger Account

1. **Joint correlations live on the server side.** When the photon pair is created, the ledger holds one joint state for signal and idler, e.g.

   $$\ket{\Psi} = \tfrac{1}{\sqrt{2}}\left(\ket{A}_s\ket{A}_i + \ket{B}_s\ket{B}_i\right)$$

   where $A, B$ label the two source regions (paths). The relative phase between the two paths is stored in the *joint* signal–idler correlations, not in the signal alone.
2. **The signal render is fringe-free.** Tracing out the idler leaves the signal in an even mixture of $\ket{A}_s$ and $\ket{B}_s$, so the screen pattern at $D_0$ has no fringes, whatever is later done to the idler. Nothing the idler encounters later changes this client-side record.
3. **The eraser chooses a basis, not a past.** An eraser detector reads the idler in the basis $\ket{\pm}_i = (\ket{A}_i \pm \ket{B}_i)/\sqrt{2}$. Rewriting the same joint state,

   $$\ket{\Psi} = \tfrac{1}{\sqrt{2}}\left(\ket{+}_s\ket{+}_i + \ket{-}_s\ket{-}_i\right), \qquad \ket{\pm}_s = \tfrac{1}{\sqrt{2}}\left(\ket{A}_s \pm \ket{B}_s\right)$$

   so the signal hits paired with $\ket{+}_i$ form fringes and those paired with $\ket{-}_i$ form anti-fringes. The ledger already held these correlations; idler detection only selects which sub-ensemble a given signal hit belongs to.
4. **Fringes appear only after classical comparison.** The sub-ensemble fringes show up only when the two client-side records ($D_0$ hits and idler clicks) are brought together and compared, which itself happens at most at speed $c$.

**Independence from distance and detection order.** The joint signal–idler correlations are a property of the server-side ledger state $\ket{\Psi}$, not of any client-side channel between the detectors. Consequently, the coincidence statistics $P(x, k)$, for screen position $x$ and idler outcome $k$, are the same whether the idler detector sits beside $D_0$ or light-years away, and whether the idler click occurs before or after the signal photon registers. Each detection is a client-side query of the ledger; the definite outcome at that detector is fixed only when that query occurs (Sec. 3.3), and the marginal at $D_0$ is fringe-free in every case. This is consistent with the discrete clock-cycle dynamics of Sec. 2.2: the ledger evolves cycle by cycle under $\hat{U}_{\text{net}}$, and the proposal is only that the joint correlations, once established, persist in $\ket{\Psi}$ until they are read out. It does not place the server outside time. Whether the server's internal ordering of read-outs for spacelike-separated detections is physical but unobservable remains the open tension noted in Sec. 5.4. The claim matches standard quantum mechanics, in which measurements on spacelike-separated subsystems commute, so the joint statistics are invariant under any reordering of those measurements.

Figure \ref{fig:eraser} illustrates these points with a simple two-slit model of the Kim et al. (2000) arrangement.

\begin{figure}[tp]
\centering
\includegraphics[width=\linewidth]{eraser.png}
\caption{Delayed-choice quantum eraser. (a) Schematic after Kim et al. (2000): a laser pumps two regions A and B of a BBO crystal, producing signal--idler pairs; the signal goes to the scanned screen detector $D_0$, and the idler passes a prism and beam splitters BSA, BSB and BS to $D_3$, $D_4$ (which-path record kept) or $D_1$, $D_2$ (which-path erased). (b) Computed $D_0$ patterns from the joint state $(\ket{A}_s\ket{A}_i+\ket{B}_s\ket{B}_i)/\sqrt{2}$, with 40,000 simulated pairs (points) and theory curves (lines); parameters are illustrative. (b1) The full $D_0$ pattern has no fringes, and the four sorted subsets add back to it exactly. (b2) Hits coincident with $D_1$ show fringes and those with $D_2$ anti-fringes, shifted by $\pi$; together they are fringe-free. (b3) Hits coincident with $D_3$ or $D_4$ show no fringes. The screen is never fringed on its own: fringes appear only after the hits are sorted by later idler records. In the ledger picture, the server side holds the joint signal--idler correlations, and the later idler detection only selects which sub-ensemble a hit is read into, so no earlier client-side record changes. There is no retrocausality and no signalling.}
\label{fig:eraser}
\end{figure}

So no past event is rewritten. The ledger keeps the joint phase correlations, the screen record is fixed when it is made, and the "erasure" is a way of sorting records that already exist.

---

## 5. Bell Non-Locality: Server Side Non-Local, Client Side Local

### 5.1 What Bell's Theorem Rules Out

Bell's theorem shows that no theory in which outcomes are set by *local* hidden variables (variables carried along with each system and acting no faster than light) can reproduce the correlations quantum mechanics predicts for entangled pairs. Loophole-free Bell tests (e.g., Hensen et al., 2015; Giustina et al., 2015; Shalm et al., 2015) agree with quantum mechanics. Any framework that reproduces quantum predictions must therefore be non-local in Bell's sense somewhere.

### 5.2 Where the Ledger Puts the Non-Locality

The Space-Ledger accepts this. It does not claim to eliminate non-locality; it proposes to **locate** it:

- **Server side.** The entangled pair is one ledger state, $\ket{\Psi}_{AB}$, that is not the product of a state at $A$ and a state at $B$. Its correlations are a property of the substrate as a whole. In Bell's language the ledger is a non-local hidden-variable carrier: the "global" state is the thing that is non-local. Because the server operates at a scale approaching zero length, the correlation is not something that travels between $A$ and $B$ across client-side space; it is held in the structure of spacetime itself.
- **Client side.** Every client-side process is local and bounded by $c$. In particular, the **no-signaling theorem** holds: the local outcome statistics at $A$, $P(a \mid x)$, do not depend on the measurement setting $y$ chosen at $B$:

  $$\sum_b P(a, b \mid x, y) = P(a \mid x) \quad \text{for all } y$$

  A client at $A$ sees only random-looking results. The Bell correlation becomes visible only when the records from $A$ and $B$ are compared through an ordinary classical channel limited by $c$. Clients cannot read the server's joint correlations directly; they can only reconstruct them after the fact.

In the software analogy: two clients reading a shared server variable can find that their results are correlated, but neither can use the server to send a message faster than the network between them allows, because each one's local read looks random until they compare logs.

**Shared record and holistic read-out.** In this picture entangled particles do not carry two copies of a correlation; they share a single server-side record, $\ket{\Psi}_{AB}$, held once rather than duplicated. The server-side read-out of a shared record is holistic: it is not parametrised by client-side distance and is not bounded by $c$, so it is not a propagation speed at all, neither instantaneous nor slightly superluminal. This is consistent with experiments and theory that exclude hidden influences travelling at any finite speed (Salart et al., 2008; Bancal et al., 2012). The server side is taken to obey its own strict rules (reversible swaps, no wipes, holistic read-out), while the client-side constraints (no-cloning, no-signaling, the $c$ limit) act as an interface protection, comparable to a sandbox boundary, that seals server-side operations from client access. Bell-type tests exclude local hidden variables but not a non-local structure of this kind, for which Bohmian mechanics is a precedent (Bell, 1964; Bohm, 1952). The testable claim is that no server-side operation is detectable at the client interface beyond standard quantum statistics. *This is an interpretive restatement, not a derivation: it adds no predictions beyond quantum mechanics at present, and how a grid of local cores realises a holistic read-out is open (Sec. 9, item 23).*

### 5.3 Server-Side Safeguards

If the server holds non-local correlations, something must stop clients from exploiting them to signal faster than light. In the ledger picture this is done by three mechanisms, each of which is established physics rather than a new assumption. We present them as supporting the client/server architecture, not as proofs of it.

1. **Random read-out (Born-rule randomness).** Each client-side query of one half of an entangled pair returns a locally random outcome, and its marginal statistics are independent of the setting chosen at the distant site (the no-signaling condition of Sec. 5.2). The server-side correlations therefore cannot carry a message until the two records are compared over an ordinary channel limited by $c$. This is the primary no-signaling safeguard, and it holds even without decoherence.
2. **No-cloning.** The server never lets a client duplicate an unrendered state. Historically, Herbert's 1982 "FLASH" proposal tried to signal faster than light by making many copies of one half of an entangled pair, so that the distant setting could be read off the copies' statistics. Its refutation led directly to the no-cloning theorem: an unknown quantum state cannot be copied (Wootters and Zurek, 1982; Dieks, 1982). Random read-out and no-cloning together block faster-than-light signaling.
3. **Decoherence as the consistency mechanism.** Decoherence is not the light-speed safeguard; it is what keeps the client side *consistent*. In ledger terms it resembles the server committing a result and replicating it into many environment nodes, so that every client agrees on what was rendered and no single client can undo it (Sec. 3.3). This matches Zurek's "quantum Darwinism," in which the environment holds many redundant records of selected states, which is what makes them objective and robust (Zurek, 2009).

Taken together, the server holds the non-local correlations, while these mechanisms keep the client side local, causal, and consistent.

### 5.4 Remaining Tension

This division keeps the framework consistent with Bell tests and with relativity's no-signaling requirement, but it does not remove every tension. If the server-side read-out is a physical update, it needs a preferred ordering of space-like separated events, which sits uneasily with Lorentz invariance (as in Bohmian mechanics). Making the server's ordering unobservable from the client side is required for consistency and is an open problem of the model.

### 5.5 Entanglement as a Shared Server Record: A Pointer API (Hypothesis, toy-tested)

*Entanglement is a shared server record, not a signal.* We tested the Sec. 5.2 picture as a minimal server interface. The call `a = entangle(x1, x2)` opens one record; each daughter packet carries only a pointer to it, together with the pump's energy and momentum, which are split between the daughters and conserved. Relay nodes forward the packets as ordinary link phase; nothing marks them as entangled, and no probability is computed in flight. The call `read(a, i, basis, setting)` runs on the server in a fixed order: it computes the odds, locks the attribute read, and returns $\pm1$. The first read of an attribute settles it for the whole set, so a partner reading the same attribute gets the correlated value. The other three attributes reset, so a later read on another basis gets a fresh answer. No outcome is stored before the read; a pre-stored value would be a local hidden variable and would cap $S$ at 2. With standard CHSH angles, the shared record gives $S = 2.822 \pm 0.007$ (the quantum maximum is $2\sqrt2 \approx 2.828$). With 80% detector efficiency and 1% dark counts per detector it gives $2.800 \pm 0.009$, inside the range measured for SPDC sources. A control that gives each daughter its own copied record gives $S = 0.01 \pm 0.01$ (figure below). Each side alone is 50/50, A's marginal does not shift with B's setting (all differences under $2\sigma$), and a read on another basis after a lock is uncorrelated ($0.003 \pm 0.005$). The record is non-local, but no message exceeds $c$. *Caveat: the read uses the $\cos^2(\theta_A - \theta_B)$ odds by hand, so this checks that the interface is consistent and does not derive the Born rule (Sec. 3.3). How local cores realise the joint read remains open (Sec. 9, item 23).*

![Pointer-API Bell test. CHSH $S$ for the shared record (ideal and with detector noise) and for the copied-record control, against the local bound 2 and the quantum maximum $2\sqrt2$.](chsh.png){width=80%}

#### Lazy, stateless evaluation (Hypothesis, toy-tested)

The record need not be updated every tick. It holds the four attribute states and a version number. At read time a single call, `brute_force(x, version, Δticks)`, jumps straight to the state $\Delta t$ ticks after `entangle()` or the last lock, like a counter-based random-number generator (Philox-style) that computes step $N$ without stepping through the ones before it. The phase drifts in proportion to energy times $\Delta t$. Each lock bumps the version, so the reset attributes get fresh randomness. The collapse then makes one weighted draw from the odds, using both detectors' settings together; it never looks up a stored value. In simulation the lazy version gives $S = 2.837 \pm 0.010$. Calling it every tick instead gives identical odds and the same outcomes draw for draw, with phases differing by $3.6\times10^{-13}$ rad (float rounding). An energy–time (Franson-type) read follows $\cos^2(\Delta\phi/2)$ and gives $S = 2.821 \pm 0.010$. The cost stays flat at about 10–20 µs whatever $\Delta t$ is, while per-tick updating grows in proportion to $\Delta t$ (about 5 ms at $10^5$ ticks); the two break even near 100 ticks (figure below). In computing terms the server is lazy: it does the work only when a client asks. *Caveat: the phase drift cancels out of these statistics, as expected for a pump-locked source, so this test does not probe it. The Franson model leaves out timing-window losses, so its visibility is 1.0, where a real Franson setup without post-selection reaches 0.5. The $\cos^2$ odds are still put in by hand.*

![Lazy versus per-tick evaluation. CHSH and Franson-type fringe from a single read-time call, and compute cost versus elapsed ticks: constant for the read-time call, linear for per-tick updating.](v11.png){width=80%}

---

## 6. Mass, Propagation Speed, and Relativistic Consistency

**Finiteness Principle (Hypothesis).** The model is constructed so that no physical quantity becomes infinite. Two features bound it from both ends: (i) nodes have a fixed size of about one Planck length, so no physical distance is shorter than $l_P$; and (ii) each node carries a finite workload, with a cap whose recommended form is a frame-independent limiting curvature of order $1/l_P^4$ (about $10^{3}/l_P^4$ in the Kretschmann scalar in the toy of Sec. 6.17), so curvature, rest-frame density (about the Planck density) and collision energy per node ($\sqrt{s} \lesssim E_P$) have maximum values. Two consequences follow as potential candidates. First, the infinite curvature at the centre of a classical black hole is replaced by a finite, fully loaded core (Secs. 6.16–6.17). Second, the minimum distance supplies a natural cutoff for the ultraviolet divergences of quantum field theory, since no mode shorter than the node spacing exists on the network.

*Caveats. The cap value is a placeholder, not derived from the node update rules. A cutoff alone does not preserve Lorentz invariance: a preferred-frame lattice regulator can transmit grid anisotropy to low energies through virtual-particle loops, which is the radiative-correction challenge discussed in Sec. 6.15. Finiteness of the network also does not by itself fix the fate of a fully loaded core; bounce and white-hole outcomes are left open.*

### 6.1 The Client-Side Speed Limit

The ledger updates in discrete ticks of duration $\tau \approx t_{\text{Planck}}$, on a graph with characteristic node spacing $a \approx \ell_{\text{Planck}}$. Because $\hat{U}_{\text{net}}$ couples only neighboring nodes per tick (Sec. 2.2), no excitation can advance more than one node per tick. The client-side speed limit is therefore

$$c = \frac{a}{\tau} = \frac{\ell_{\text{Planck}}}{t_{\text{Planck}}},$$

which is consistent by construction, since $\ell_{\text{Planck}}/t_{\text{Planck}} = c$.\footnote{In the four-component candidate rule of Sec. 6.2 (\emph{Doubler-free four-component node}), the light speed realised by the rule is slightly below the hop limit (about 0.989 of it), so $c = \ell_P/t_P$ holds only approximately there; see that subsection.} A massless excitation hops one node per tick in a fixed direction, and so always travels at exactly $c$.

In this picture the speed of light is a potential candidate for the *propagation limit of the server network itself*: client-side apps (particles and signals) are capped at $c$ because no pattern can be replotted faster than one node per update tick. Numerically, with $\ell_{\text{Planck}} = \sqrt{\hbar G/c^3} \approx 1.616\times10^{-35}$ m and $t_{\text{Planck}} = \sqrt{\hbar G/c^5} \approx 5.391\times10^{-44}$ s, the ratio is $1.616\times10^{-35}/5.391\times10^{-44} \approx 2.998\times10^{8}$ m/s, i.e. $c$. The equality is exact by the definitions of the Planck units, so it is a consistency check rather than an independent prediction. Massive apps move slower because, in plain terms, part of each tick's update goes into their rest-mass workload (the direction-flip amplitude of Sec. 6.2) instead of net forward replotting; only a massless pattern spends every tick on forward motion.

If, in the server's hidden frame, the per-node cap is written as an energy budget, $\sqrt{(mc^2)^2+(pc)^2} \le m_P c^2$ (Sec. 6.17), the speed $v = pc^2/E$ reaches $c$ only for $m = 0$, and a massive app has a finite maximum Lorentz factor $\gamma_{\max} = E_P/(mc^2)$: about $2.4\times10^{22}$ for an electron, a top speed short of $c$ by about one part in $10^{45}$. *This is a heuristic valid only in the hidden server frame, not a frame-free prediction: energy is not Lorentz invariant, and the recommended frame-independent cap of Sec. 6.17 limits curvature and collision energy ($\sqrt{s} \le E_P$), not the speed of a single particle. A strict per-particle limit would require either a server frame observable at Planck energies or a doubly special relativity in which $E_P$ is itself invariant (Magueijo and Smolin, 2002; Amelino-Camelia, 2002).*

**Two readings of the speed limit.** In special and general relativity the limit acts as an energy barrier: a massive body approaches $c$ only as its energy grows without bound, so reaching $c$ would require infinite energy. In the ledger picture the limit is offered as a potential candidate for a *structural* one: $c$ is the network's maximum propagation rate, one node per tick, so no faster replotting exists for any app to reach. Massive apps stay below $c$ because part of each tick goes to rest-mass workload; in the hidden-frame heuristic above, they would also have a finite $\gamma_{\max}$. The barrier is not removed; it is located in the network's update structure rather than in an infinite energy cost.

*Caveat. At all observed energies the two readings give identical predictions, with the same relations between energy, momentum and speed. They differ only near $E_P$, far beyond any observation (the most energetic cosmic ray recorded is about $3\times10^{-8}\,E_P$; Sec. 6.17). The contrast is therefore a difference in explanation plus a Planck-scale prediction, not a currently testable departure from relativity.*

*Caveats. (a) Direction dependence of $c$ on a regular grid is treated in the next paragraph. (b) Replotting does not move the nodes: nodes stay fixed and do not jitter. (c) Server-side entanglement correlations carry no signal, so they allow no faster-than-$c$ messaging, consistent with the no-signalling theorem (Secs. 5 and 7.4).*

**Isotropy of $c$ on a link-only grid (Hypothesis).** In this model, load moves only from one node to an adjacent node along a link, never to a point in between. Rotating the whole grid changes nothing physically: only the angle between a signal's direction and the grid axes matters, so a cube "standing on a corner" is simply the body-diagonal ([111]) direction of the same grid. If a signal followed a single hop path, it would zigzag along the links (the Manhattan, or taxicab, metric) and travel about 29% slower along a face diagonal and 42% slower along a body diagonal than along an axis, which observation excludes. The observed signal, however, is offered as a potential candidate for a sum over *all* hidden hop paths, in line with the hidden-path picture (Sec. 6.15) and Feynman's path integral. Feynman's checkerboard (Feynman and Hibbs, 1965) is a 1+1-dimensional precedent: a particle that only ever hops at $\pm c$ reproduces the Dirac equation once all zigzag paths are summed. In three dimensions, the zigzags in different directions average out and the front becomes round. In a toy sum over link-only paths from one node of a cubic grid (Figure \ref{fig:paths}), the ratio of the front radius along the body diagonal to that along an axis is 0.76 after 4 ticks, 0.92 after 16, 0.98 after 64 and 0.997 after 120, compared with a fixed $1/\sqrt{3} \approx 0.58$ for a single path.

For the nearest-neighbour wave equation on a cubic grid (continuous time, spacing $l_P$), the speed is exactly $c$ in every direction in the long-wavelength limit; this is the Test 1 result of Sec. 6.15. A residual direction dependence appears only at order $(ka)^2 = (E/E_P)^2$. Axis signals are slowest and body-diagonal signals fastest, with an axis-to-body-diagonal difference in group speed of $(E/E_P)^2/12$:

| Signal | $E/E_P$ | Axis vs. diagonal speed difference |
|---|---|---|
| Visible light (500 nm) | $2.0\times10^{-28}$ | $3\times10^{-57}$ |
| 1 TeV gamma ray | $8.2\times10^{-17}$ | $6\times10^{-34}$ |
| 100 TeV gamma ray | $8.2\times10^{-15}$ | $6\times10^{-30}$ |
| Oh-My-God cosmic ray ($3.2\times10^{20}$ eV) | $2.6\times10^{-8}$ | $6\times10^{-17}$ |

: Axis-to-body-diagonal group-speed difference on a nearest-neighbour cubic grid, $(E/E_P)^2/12$.

This corresponds to $E_{\text{QG},2} \approx 4.2$–$7.3\times10^{19}$ GeV, about $10^{8}$ times above the GRB 090510 quadratic bound, so the effect lies far below current sensitivity (Sec. 7.1).

The leading coefficient depends on the layout. The axis-to-diagonal spread in units of $(ka)^2$ is about 0.083 for a simple cubic grid, 0.056 for body-centred cubic and diamond, and 0.021 for face-centred cubic (close packing), which is the most isotropic of the simple nearest-neighbour layouts. A cubic grid whose links also include the 12 face diagonals (weights 1/3 on axis links and 1/6 on diagonal links) cancels the $(ka)^2$ direction dependence entirely, leaving only order $(ka)^4$. Both remain link-only and are potential candidates for the node layout.

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{paths_roundness.png}
\caption{Sum over link-only hop paths from one node of a cubic grid (mid-plane slice, log scale) after 4, 16, 64 and 120 ticks. Cyan: contour at $e^{-2}$ of the peak. White dashed: the diamond-shaped front expected from a single zigzag path (Manhattan metric). The front becomes round as the hop count grows; the body-diagonal to axis radius ratio reaches 0.997 at 120 ticks.}
\label{fig:paths}
\end{figure}

*Caveats. The wave result uses continuous time; a discrete-tick version requires a time step of at most $t_P/\sqrt{3}$, or sub-steps, for stability in three dimensions. The path-sum demonstration is diffusive and illustrates only the averaging of link-only paths, not the light-speed front itself. Isotropy does not by itself hide a preferred rest frame, so the radiative-correction challenge of Sec. 6.15 remains open. Nodes stay fixed and do not jitter.*

### 6.2 Mass as Per-Hop Processing

In client–server language, mass is extra per-hop processing for the "app": at every tick, a massive excitation has some amplitude to flip its direction of travel (its chirality) instead of simply moving on. This is the structure of Feynman's checkerboard model (Feynman and Hibbs, 1965) and of the Dirac quantum walks and quantum cellular automata developed by Bialynicki-Birula (1994), Meyer (1996), Strauch (2006), Arrighi, Nesme and Forets (2014), and D'Ariano and Perinotti (2014).

In one spatial dimension, write the excitation as a two-component amplitude $(\psi_R, \psi_L)$ for right- and left-moving parts. One tick of the ledger is

$$\begin{aligned}
\psi_R(x + a,\, t + \tau) &= \cos\theta\, \psi_R(x, t) - i \sin\theta\, \psi_L(x, t), \\
\psi_L(x - a,\, t + \tau) &= \cos\theta\, \psi_L(x, t) - i \sin\theta\, \psi_R(x, t),
\end{aligned}
\qquad \sin\theta = \frac{mc^2 \tau}{\hbar}.$$

For $m = 0$ there is no flipping and each component moves at $c$. For $m > 0$ the excitation zigzags, which is a lattice version of *zitterbewegung*. Each individual hop is still at speed $c$, but the mean drift speed is less than $c$. The exact lattice dispersion relation is $\cos(\omega\tau) = \cos\theta\,\cos(ka)$. In the continuum limit $a, \tau \to 0$ with $c = a/\tau$ fixed, this becomes the Dirac equation,

$$i\hbar\, \partial_t \psi = -i\hbar c\, \sigma_z\, \partial_x \psi + mc^2\, \sigma_x\, \psi,$$

with $E^2 = p^2c^2 + m^2c^4$. The group velocity is then

$$v = \frac{\partial E}{\partial p} = \frac{pc^2}{E} = c\sqrt{1 - \left(\frac{mc^2}{E}\right)^2}.$$

So the propagation speed depends on mass *relative to energy*, not on mass alone. The more of an app's energy is spent on per-hop processing (rest energy $mc^2$), the slower it runs. As $E \gg mc^2$ the speed approaches $c$, and an app with $E = mc^2$ is at rest.

#### Candidate hardware picture (Hypothesis)

*This subsection offers one possible picture of how the server side might carry out the tick rule above. It is not a claim about how the server side is actually built.*

One potential candidate reads each node as an identical processing core:

- **Placement.** The cores sit rigidly on a body-centred-cubic (BCC) lattice, and each is linked to its 8 nearest neighbours. The cores never move or jitter; only the stored amplitudes are passed along.
- **Updates.** At every tick, all cores act at once on non-overlapping pairs in a checkerboard (Margolus) pattern (Margolus, 1984). Each pair applies a small reversible swap or mix, so an amplitude moves at most one core per tick and nothing is ever wiped or overwritten.
- **Entangled states.** Joint states are held as shared records, and only one pair-update writes each record in a given tick.
- **Read-out.** The squaring step of Sec. 3.3 is applied only when a result is read out.

Rules of this kind are quantum walks, or quantum cellular automata. In the long-wavelength limit they reproduce the Weyl and Dirac equations (Bialynicki-Birula, 1994; D'Ariano and Perinotti, 2014). The minimal three-dimensional automaton of D'Ariano and Perinotti lives on exactly this BCC lattice.

**Small simulations of the candidate.**

- **Light cone.** We ran the 1D tick rule above from a single core for 300 ticks (Figure \ref{fig:qcacone}). The probability outside $|x| \le ct$ is exactly zero at every tick. A massless excitation moves exactly one core per tick.
- **Dispersion.** Massive wave packets move more slowly, following $\cos\omega\tau = \sqrt{1-m^2}\cos ka$ (here $m = \sin\theta$). Across 32 packets the measured speeds agree with this formula to within 0.013, and the top speed is $\sqrt{1-m^2}$.
- **Exactness.** Over these runs, total probability is conserved to about $10^{-13}$, and running the rule backward restores the initial state to about $10^{-15}$. The overlap between two states is unchanged to $10^{-15}$, as no-cloning requires (Wootters and Zurek, 1982).
- **Entangled pair.** We created a pair at one core and carried it about 72 cores apart, hop by hop. The far party's position statistics changed by less than $10^{-16}$ whatever the near party measured. The correlation remained: the far particle was on the right with probability 0.72 given the near one on the left, and 0.27 given the near one on the right.
- **Roundness.** In a 2D massless version, a smooth packet spreads into a circle (diagonal/axis radius ratio 0.999–1.001), and the direction dependence of the speed falls as $(ka)^2$ (Figure \ref{fig:qcaround}). For the 3D BCC automaton, the dispersion relation gives a direction spread that falls as $ka$. Both are consistent with the isotropy discussion of Sec. 6.1.

**Why the checkerboard matters.** Table \ref{tab:race} and Figure \ref{fig:qcarace} compare the checkerboard with naive updates, in which each core holds a single register:

- Copying from a neighbour in place wipes the data.
- Averaging with a neighbour leaks probability.
- Updating pairs one after another in place keeps the total but lets an influence cross 26 cores in a single tick, which breaks the light cone.

Only simultaneous pairwise updates keep probability, reversibility and the one-hop limit together.

\begin{table}[htbp]
\centering
\small
\caption{Race-condition test on 64 cores with one register each (total probability 1 at start; rightmost non-zero core 11 at start).}
\label{tab:race}
\begin{tabular}{lccc}
\hline
Update rule & Total prob., 1 tick & Total prob., 40 ticks & Rightmost core after 1 tick \\
\hline
Checkerboard pairwise mix & 1.000000 & 1.000000 & 11 \\
Naive in-place copy & 0 (wiped) & 0 & -- \\
Naive averaging & 0.74 & 0.17 & 12 \\
Sequential in-place mixes & 1.000000 & 1.000000 & 37 \\
\hline
\end{tabular}
\end{table}

\begin{figure}[tp]
\centering
\includegraphics[width=\linewidth]{qca_lightcone.png}
\caption{Candidate hardware, 1D tick rule. (a) Point source with $\theta = 0.3$, $\log_{10}$ probability; no probability appears outside the dashed one-core-per-tick light cone. (b) Wave-packet speed versus wavenumber: lines from $\cos\omega\tau = \sqrt{1-m^2}\cos ka$, circles from simulation. (c) Root-mean-square spread of a point source.}
\label{fig:qcacone}
\end{figure}

\begin{figure}[tp]
\centering
\includegraphics[width=\linewidth]{qca_race.png}
\caption{Checkerboard versus naive updates. (a) Total probability: exact for the checkerboard (and for sequential mixes, dashed), wiped by in-place copying, leaking under averaging. (b) Rightmost non-zero core: sequential in-place updates jump far beyond the light cone (dotted).}
\label{fig:qcarace}
\end{figure}

\begin{figure}[tp]
\centering
\includegraphics[width=\linewidth]{qca_roundness.png}
\caption{Roundness of a 2D massless walk with nearest-neighbour hops, at tick 360. Left: smooth packet ($\sigma = 8$ cores). Middle: single-core point source. Right: diagonal-to-axis mean-radius ratio versus tick; inset: direction spread of the group speed versus $|k|$ for the 2D walk (simulated rule) and the 3D BCC automaton (from its published dispersion).}
\label{fig:qcaround}
\end{figure}

*Limits.*

- *Roundness holds only for features much larger than a node. A single-core point source keeps a lattice imprint (ratio 0.847 at every tick).*
- *Our naive 2D massive walk was clearly anisotropic, so how mass couples isotropically remains open.*
- *The 3D roundness is computed from D'Ariano and Perinotti's published dispersion relation, not simulated here.*
- *Gravity is not derived from this picture.*
- *These results are standard properties of local unitary rules, reproduced at small scale. The node-as-core reading is offered only as one candidate.*

**Doubler-free four-component node (Hypothesis).** A three-dimensional lattice walk generically carries extra low-energy copies of each particle ("doublers"), and the simplest BCC rules above do too. As one potential candidate fix, each core holds four amplitudes, a left-handed and a right-handed two-component Weyl pair, with the mass mixing the two (D'Ariano and Perinotti, 2014). One cycle has four ticks: a right-handed step, a Wilson layer, a left-handed step and a mirrored Wilson layer. The Wilson layer couples left and right with an angle $\varphi$ that is zero at long wavelength and of order one near every doubler, in the spirit of Wilson's lattice fermions (Wilson, 1977). Every layer uses only the 8 corner hops plus on-site mixing, so the rule stays exactly unitary.

- **Doublers.** A global numerical search over the Brillouin zone (several hundred random starts) finds no zero-frequency point other than the physical one for $0 < \varphi < \pi/2$. Without the Wilson layer, or without alternating the handedness, zero modes remain.
- **Gap versus speed.** The smallest doubler gap and the low-energy light speed trade off against each other (Table \ref{tab:dirac4}, Figure \ref{fig:dirac4}). At $\varphi \approx 1.4$ the gap is about $0.08\,E_P \approx 10^{18}$ GeV, roughly $10^{14}$ times the reach of the LHC.
- **Roundness.** The direction spread of the group speed falls as $(ka)^2$ (fitted slope 1.96–2.01 for masses 0, 0.3 and 0.6 in lattice units), with a spread of about $4\times10^{-4}$ to $6\times10^{-4}$ at $ka = 0.025$. Smooth packets are round to 0.7% at $\sigma = 8$ cores.
- **Exactness.** In real-space runs ($48^3$ cores, 24 ticks), unitarity holds to $7\times10^{-16}$, the probability outside the one-hop light cone is exactly zero, total probability is conserved to $10^{-15}$, and running backward restores the initial state to $4\times10^{-16}$. The largest group speed equals the low-energy light speed.

**Formal update rule (Hypothesis).** *State.* Each core $x$ on the BCC grid carries $\psi(x)=(\psi_R(x),\psi_L(x))^{T}\in\mathbb{C}^2\oplus\mathbb{C}^2$, a right- and a left-handed Weyl pair. The ledger Hilbert space is $\mathcal{H}=\ell^2(\mathrm{BCC})\otimes\mathbb{C}^4$. We use $\tau_a$ for Pauli matrices acting on the $(R,L)$ label and $\sigma_a$ for Pauli matrices acting inside each Weyl spinor. *Links.* The 8 corner links are $h\in\{(\pm1,\pm1,\pm1)\}$ in units of $a/2$, with $T_h\psi(x)=\psi(x-h)$. Since every layer is translation invariant, we give it at wavevector $k$ (the Fourier symbol of $\sum_h T_h\otimes M_h$).

*Hop symbols* (D'Ariano and Perinotti, 2014), $\epsilon=\pm1$, $c_i=\cos k_i$, $s_i=\sin k_i$:
$$A^{\epsilon}_k=u^{\epsilon}_k\,\sigma_0-i\,\mathbf n^{\epsilon}_k\cdot\boldsymbol\sigma,\qquad
u^{\epsilon}_k=c_xc_yc_z-\epsilon\,s_xs_ys_z,$$
$$\mathbf n^{\epsilon}_k=\big(s_xc_yc_z+\epsilon\,c_xs_ys_z,\;\;c_xs_yc_z-\epsilon\,s_xc_ys_z,\;\;c_xc_ys_z+\epsilon\,s_xs_yc_z\big),$$
with $(u^{\epsilon}_k)^2+|\mathbf n^{\epsilon}_k|^2=1$, so $A^{\epsilon}_k\in SU(2)$. In real space $A^{\epsilon}=\sum_h T_h\otimes A^{\epsilon}_h$ uses only the 8 corner links.

*Step 1 and step 3, directional hops with mass mixing* ($\nu^2+m^2=1$):
$$S^{\epsilon}_k=\begin{pmatrix}\nu A^{\epsilon}_k & i m\,\sigma_0\\ i m\,\sigma_0 & \nu A^{\epsilon\dagger}_k\end{pmatrix},\qquad S_1=S^{+},\;\;S_3=S^{-}.$$

*Step 2 and step 4, Wilson layers* at a fixed angle $\varphi$ ($\varphi=1.4$ by default):
$$V^{\epsilon}_k(\varphi)=e^{-i\varphi X^{\epsilon}_k}\,e^{+i\varphi\tau_x},\qquad X^{\epsilon}_k=u^{\epsilon}_k\,\tau_x+\tau_y\otimes(\mathbf n^{\epsilon}_k\cdot\boldsymbol\sigma).$$
Here $X^{\epsilon}_k$ is Hermitian with $(X^{\epsilon}_k)^2=1$ (the cross terms cancel because $\tau_x\tau_y=-\tau_y\tau_x$), so $e^{-i\varphi X}=\cos\varphi-i\sin\varphi\,X$. At $k=0$, $X=\tau_x$ and $V=1$. The effective L–R mixing therefore vanishes at long wavelength and is of order one near the doubler momenta. Step 2 is $V^{+}$. The mirrored step 4 is $V^{-}$.

*One cycle:*
$$\boxed{\;U_k=V^{-}_k(\varphi)\,S^{-}_k\,V^{+}_k(\varphi)\,S^{+}_k,\qquad \psi(t+4\tau)=U\,\psi(t)\;}$$

*Unitarity and light cone.* Each factor is unitary: $S^{\epsilon}$ because $A^{\epsilon}\in SU(2)$ and $\nu^2+m^2=1$, and $V^{\epsilon}$ as a product of two exponentials of Hermitian operators. Therefore $U$ is unitary. Each layer is a sum of on-site terms and single corner hops, so the support of $\psi$ grows by at most one link per layer and four per cycle.

*Low-energy limit.* With $\omega$ taken per layer ($e^{-4i\omega}$ = eigenvalue of $U_k$), the lowest band is $\omega^2\simeq\omega_0^2+c_0^2|k|^2$. This is the Dirac equation with $\omega_0=\tfrac12\arcsin m$ and $c_0(\varphi=1.4)=0.98911$, which is direction independent to $10^{-6}$ at this order. For $0<\varphi<\pi/2$ the only zero-frequency point is $k=0$.

*Chain extension (domain wall).* With $N_s$ internal copies $\psi_s$, $s=0\ldots N_s-1$, the code puts mass on-site and replaces step 4 by $R(b)\,M(m_0)\,V^{-}$. Here $M(m_0)=e^{+im_0\tau_x}$ acts on each copy, and
$$R(b)=\prod_{s=0}^{N_s-2}\exp\!\big[-i b\,(\psi_{L,s}^{\dagger}\psi_{R,s+1}+\mathrm{h.c.})\big],$$
with $S^{\pm}$ taken at $m=0$. This leaves one chiral mode at each end of the chain, and the residual mass falls as $(\tan m_0/\tan b)^{N_s}$.

\begin{table}[htbp]
\centering
\small
\caption{Four-component node with Wilson layer: smallest doubler gap and low-energy light speed versus the Wilson angle $\varphi$ (gap per tick in units of $E_P \approx 1.22\times10^{19}$ GeV; speed in units of the hop rate $\ell_P/t_P$).}
\label{tab:dirac4}
\begin{tabular}{lccc}
\hline
$\varphi$ & Smallest gap ($E_P$) & Gap (GeV) & Light speed / hop rate \\
\hline
0.5 & 0.217 & $2.6\times10^{18}$ & 0.650 \\
0.8 & 0.262 & $3.2\times10^{18}$ & 0.797 \\
1.0 & 0.232 & $2.8\times10^{18}$ & 0.884 \\
1.2 & 0.167 & $2.0\times10^{18}$ & 0.949 \\
1.4 & 0.082 & $1.0\times10^{18}$ & 0.989 \\
1.5 & 0.035 & $4.3\times10^{17}$ & 0.998 \\
$\pi/2$ & 0 (doublers return) & -- & 1.000 \\
\hline
\end{tabular}
\end{table}

\begin{figure}[tp]
\centering
\includegraphics[width=\linewidth]{dirac4.png}
\caption{Four-component node. Left: lowest frequency per tick ($m = 0$, units of $E_P$) along a path through the doubler points for single-step and alternating rules without a Wilson layer, a non-alternating rule with one, and the alternating rule with the mirrored Wilson layer at $\varphi = 0.8$ and $1.4$; only the last two stay away from zero everywhere except at $\Gamma$. Right: smallest doubler gap (global search) and low-energy light speed versus the Wilson angle $\varphi$.}
\label{fig:dirac4}
\end{figure}

**What $c$ means here.** The measured $c$ is the light speed realised by the rule, about 0.989 of the grid hop rate at $\varphi \approx 1.4$. The hop limit $\ell_P/t_P$ is then a hidden server-side bound about 1% above $c$, so $c = \ell_P/t_P$ (Sec. 6.1) holds only approximately, to within the chosen $\varphi$. This is consistent with the SI definition of $c$ (fixed exactly since 1983): that definition fixes the units, not the hidden hop rate.

*Limits of the four-component node.*

- *The low-energy particle is a non-chiral Dirac particle: both handednesses appear together, as the Nielsen–Ninomiya theorem requires for local lattice rules of this type (Nielsen and Ninomiya, 1981a, 1981b). A chiral weak sector or purely left-handed neutrinos would need further constructions, such as domain-wall (Kaplan, 1992) or Ginsparg–Wilson-type (Ginsparg and Wilson, 1982) rules; a domain-wall-type rule is tested below.*
- *Narrow packets ($\sigma = 4$ cores) remain about 6% non-round; roundness is good only for features much larger than a node.*
- *Interactions and gravity are not included.*

**Chiral modes from internal component chains (Hypothesis).** As one potential candidate route to chirality, each node holds $N_s$ copies of the four-component content above, i.e. $4N_s$ internal property states per node. The index $s = 1,\dots,N_s$ is an internal label, not a coordinate: there is no extra spatial dimension, and no hop ever changes $s$. In the fourth tick an on-site rotation of angle $b$ mixes $L_s$ with $R_{s+1}$ for $s = 1,\dots,N_s-1$, leaving $R_1$ and $L_{N_s}$ unpaired. This is the domain-wall construction of lattice field theory (Kaplan, 1992; Shamir, 1993), and the ledger offers one physical interpretation of its fifth coordinate as a chain of internal components within each node. All physical hops remain the 8 corner hops, one per tick, so the rule stays exactly unitary. The following were measured in 3+1 dimensions at $\varphi = 1.4$, $b = 0.2$ (Table \ref{tab:dw}, Figure \ref{fig:dw}).

- **Residual mass.** With a bare on-site mass $m_0$, the left- and right-handed end modes mix only through the chain, and their mass falls exponentially with $N_s$. For $m_0 = 0.05$ it is $2.9\times10^{-3}$, $1.8\times10^{-4}$, $7.0\times10^{-7}$ and $2.7\times10^{-9}$ per tick at $N_s = 2, 4, 8, 12$, reaching about $10^{-16}$ at $N_s = 24$. The fitted decay rate per copy is $-1.390$ against a predicted $\ln(\tan m_0/\tan b) = -1.399$; for $m_0 = 0.1$ it is $-0.698$ against $-0.703$. At $m_0 = 0$ the end modes are exactly massless.
- **Chirality and localisation.** At $m_0 = 0$, $N_s = 16$, the mode on $s = 1$ is right-handed and the mode on $s = N_s$ left-handed, with $|\gamma_5| = 1.0000, 0.9999, 0.9993, 0.9953, 0.954$ at $|k| = 0.01, 0.05, 0.1, 0.15, 0.2$ (lattice units). The localisation length grows from 0.12 to 0.64 components over that range; by $|k| \approx 0.3$ the mode has left the chain end ($|\gamma_5| \approx 0.47$).
- **Doublers and bulk.** By global search, the smallest doubler gap at $N_s = 16$ is 0.058, 0.046, 0.034 and 0.022 $E_P$ for $b = 0.1, 0.15, 0.2, 0.25$; at $b = 0.2$ this is about $4\times10^{17}$ GeV. The bulk (interior-component) gap at $b = 0.2$ is 0.033 $E_P$. For $b \geq 0.3$ a doubler end mode survives near $k = (\pi/2, \pi/2, \pm\pi/2)$ with a gap that falls exponentially with $N_s$, so the construction requires $b \lesssim 0.25$.
- **Roundness.** The end mode's speed spread over 13 directions scales as $k^{2.00}$ (about $5\times10^{-4}$ at $k = 0.05$), with speed 0.9855 of the hop rate.
- **Exactness.** In a real-space run ($40^3$ nodes, $N_s = 8$, 24 ticks), unitarity holds to $9\times10^{-16}$, the probability outside the one-hop light cone is exactly zero, probability is conserved to $2\times10^{-15}$, and reversal restores the initial state to $2\times10^{-15}$.
- **Cost.** At $N_s = 8$ a node holds 32 components (residual mass about $7\times10^{-7}$ per tick for $m_0 = 0.05$); $N_s = 16$ gives 64.

**No fifth dimension required (Hypothesis).** In Kaplan's construction the chiral modes live on the boundaries of a fifth spatial dimension, which is usually treated as a computational device without physical meaning, or else as a literal extra dimension. The results above suggest a third reading: the same mathematics is reproduced when the fifth coordinate is replaced by internal property states held within each node. Nothing ever hops along $s$; space stays three-dimensional, and the light cone, unitarity and isotropy measured above are unchanged. *If this reading holds, the domain-wall route to chirality would no longer require an extra dimension, only a richer per-node state. This does not yet solve the weak sector: the coupling of these modes to the weak gauge field remains open (Sec. 9, item 23).*

\begin{table}[htbp]
\centering
\small
\caption{Internal component chain ($\varphi = 1.4$, $b = 0.2$): residual end-mode mass for $m_0 = 0.05$ and node component count versus $N_s$, and end-mode chirality and localisation versus $|k|$ ($N_s = 16$, $m_0 = 0$). Units per tick, $E_P$.}
\label{tab:dw}
\begin{tabular}{lccc|lcc}
\hline
$N_s$ & Components & Residual mass & & $|k|$ & $|\gamma_5|$ & Loc. length \\
\hline
2 & 8 & $2.9\times10^{-3}$ & & 0.01 & 1.0000 & 0.12 \\
4 & 16 & $1.8\times10^{-4}$ & & 0.05 & 0.9999 & 0.20 \\
8 & 32 & $7.0\times10^{-7}$ & & 0.1 & 0.9993 & 0.29 \\
12 & 48 & $2.7\times10^{-9}$ & & 0.15 & 0.9953 & 0.40 \\
24 & 96 & $\sim10^{-16}$ & & 0.2 & 0.954 & 0.64 \\
\hline
\end{tabular}
\end{table}

\begin{figure}[tp]
\centering
\includegraphics[width=\linewidth]{domainwall.png}
\caption{Internal component chain. (a) Residual end-mode mass versus $N_s$ with the predicted $(\tan m_0/\tan b)^{N_s}$ (dashed). (b) Chirality $|\gamma_5|$ and end-component weight versus $|k|$. (c) Localisation length in components. (d) Smallest doubler gap versus $b$ (solid: global search; dashed: at the surviving special point only).}
\label{fig:dw}
\end{figure}

*Limits of the component chain.*

- *Coupling these chiral modes to the weak gauge field is not solved; consistent chiral lattice gauge theory remains an open problem.*
- *The chiral end mode holds only for $|k| \lesssim 0.25$, i.e. wavelengths above about 25 nodes; this covers all observed particles but not Planck-scale excitations.*
- *The doubler gap is reduced from about 0.082 to 0.034 $E_P$, and the light speed to 0.9855 of the hop rate.*
- *The construction reproduces known lattice methods rather than deriving chirality from the ledger.*

### 6.3 Special Relativity: Emergent Lorentz Invariance

The Dirac equation recovered above is Lorentz invariant, so in this model special relativity *emerges* at low energies ($E \ll E_{\text{Planck}}$, $ka \ll 1$). It is not built in exactly. The full lattice dispersion relation differs from $E^2 = p^2c^2 + m^2c^4$ at order $(E/E_{\text{Planck}})$ or higher, depending on the graph. D'Ariano and Perinotti (2014) note that in their automaton, Lorentz covariance is distorted in the ultra-relativistic regime. These deviations are exactly the Lorentz-violation signatures tested in Sec. 7. The Fermi and LHAASO bounds there already rule out an order-one linear deviation, which requires the linear term to be suppressed; on the BCC grid, link-only path sums leave a direction dependence only at order $(E/E_P)^2$ (Sec. 6.1), with a random, causal-set-like node arrangement kept as a fallback (Sec. 7.3).

### 6.4 General Relativity (Open Work)

The framework does not yet reproduce general relativity; this subsection is a sketch of directions, not a result. In the ledger picture, curvature would have to emerge from position-dependent structure of the graph: variations in node workload (with the nodes themselves rigid; Sec. 6.14) or in the entanglement pattern encoded in $T$.

**Proposal: mass loads the server.** **Energy is server workload; mass is the portion of that workload an app carries at rest ($E = mc^2$).** Massless photons still carry energy and therefore still add workload, which is why light also gravitates: in general relativity, energy, not only rest mass, sources curvature. (In standard physics, most visible mass is itself energy: the Higgs-given masses of a proton's three valence quarks account for only about 1% of its mass, and lattice QCD finds most of the rest comes from the energy of confined quarks and gluons; Yang et al., 2018.)

Two refinements follow:

- **Workload is not a single number.** In general relativity, the source of curvature is the full stress–energy tensor $T_{\mu\nu}$: energy density, momentum flow, pressure and stress. This is distinct from the network tensor $T$, as noted below. Pressure itself gravitates. In a collapsing stellar core, pressure adds to the gravitational pull, as in the Tolman–Oppenheimer–Volkoff equation (Sec. 6.5). The negative pressure of dark energy, with equation of state $w \approx -1$ (Planck Collaboration, 2020), drives accelerated expansion (Sec. 6.10). In ledger terms, the *kind* of workload matters, not only its amount.
- **Curvature can exist and propagate without local workload.** Einstein's vacuum equations admit curved solutions, such as the exterior of a Schwarzschild black hole and gravitational waves, carried by the Weyl (tidal) part of curvature. Gravitational waves were directly detected by LIGO in 2015 (Abbott et al., 2016). In ledger terms, we hypothesize that workload sources curvature locally and the network propagates it: gravitational waves would be ripples in the server's own state passing between nodes, with no client app riding along.

The working hypothesis of this paper is that the mass-energy of client-side apps is what produces gravity. An excitation with energy $E$ does not just run its own per-hop processing (Sec. 6.2); it also *loads* the server nodes around it. Two effects are proposed:

1. **Slower local updates (time dilation).** Loaded nodes complete fewer effective update cycles per unit of global ledger time. Clocks built from client-side processes near a mass therefore tick slower, which is the qualitative content of gravitational time dilation.
2. **Reshaped effective paths (curvature).** The load raises the effective cost of routing through loaded nodes (the nodes stay rigid; Sec. 6.14), so the fastest paths through the graph curve toward the mass. Free excitations following these paths trace curved trajectories, playing the role of geodesics.

This is a different role for mass than in Sec. 6.2. There, mass sets an app's *own* speed through the network, which is special relativity. Here, mass *acts back on the server*, changing the network that every other app runs on, which is gravity. Whether this sketch can be made quantitative is open. In particular, the load-to-geometry rule must reproduce Einstein's field equations, $G_{\mu\nu} = (8\pi G/c^4)\,T^{\mu\nu}_{\text{matter}}$ (the energy–momentum tensor, distinct from the network tensor $T$), not just the qualitative effects.

Several existing programs give precedent for this:

- **Entanglement builds geometry.** Van Raamsdonk (2010) argued, in a holographic setting, that classically connected spacetime is tied to entanglement between degrees of freedom, and that reducing entanglement between two regions pulls them apart.
- **Einstein's equation as an equation of state.** Jacobson (1995) derived the Einstein equation from the proportionality of entropy and horizon area together with $\delta Q = T\,dS$ on local Rindler horizons. If ledger entanglement entropy scales with area, a similar argument could apply.
- **Causal sets.** In causal set theory, geometry is recovered from the order and number of discrete elements, with volume counted by the number of nodes (Bombelli, Lee, Meyer and Sorkin, 1987).

Any such mechanism, including the load proposal above, must satisfy the **equivalence principle**: all excitations, massive or massless, must respond identically to the local graph geometry. In ledger language, gravity must change the "network" itself (effective routing cost and tick rate), not apply species-dependent per-hop processing. Otherwise different apps would fall differently, which experiments forbid to high precision. Showing that a specific $T$ and $\hat{U}_{\text{net}}$ produce Einstein's equation at large scales, and satisfy the equivalence principle, is an open problem.

### 6.5 Extreme Objects: Black Holes and Core-Collapse Supernovae (Hypothesis)

*This subsection is speculative. It reinterprets established physics in ledger language and adds no new quantitative prediction yet.*

**Black holes: maximum server load.** Under the load proposal of Sec. 6.4, a very large mass-energy concentrated in few nodes places extreme load on the server and drives the local effective update rate toward zero. This lines up with standard general relativity: for a non-rotating mass $M$, a static clock at radius $r$ runs slow relative to a distant clock by the factor $\sqrt{1 - r_s/r}$, with $r_s = 2GM/c^2$. That factor goes to zero at the horizon, so a distant observer sees processes at the horizon appear frozen. In ledger terms, the horizon is where loaded nodes effectively stop advancing relative to the rest of the network. 

**No singularities.** The model's position is that no physical singularity or infinity exists. A finite network has a maximum node load, set at Planck density, so a black-hole interior is a finite region of maximum load rather than a point of infinite density. General relativity does predict singularities: Penrose's 1965 theorem shows that, once a trapped surface forms and reasonable energy conditions hold, classical spacetime cannot be continued indefinitely (it is geodesically incomplete). A common view among physicists is that this signals the breakdown of the continuum equations in a regime where quantum gravity must take over, not that GR's mathematics is in error. The ledger model proposes to replace that regime with a finite, maximally loaded core. A related idea in loop quantum gravity is the "Planck star" of Rovelli and Vidotto (2014), in which collapsing matter is halted near Planck density and bounces. Whether a ledger core of this kind can be made consistent with the horizon, with evaporation, and with observations remains open.

**Information is preserved.** Because $\hat{U}_{\text{net}}$ is unitary, the ledger never deletes information. Everything that falls into a black hole stays encoded in the server state. Hawking (1975) showed that black holes radiate thermally and evaporate, which appeared to destroy information. Most physicists now expect information to be preserved, so that the entropy of the radiation follows the *Page curve*: it rises, then turns over at the "Page time" and falls back toward zero as the black hole evaporates (Page, 1993). Calculations from 2019 using quantum extremal surfaces ("islands") reproduced the Page curve in semiclassical gravity models (Penington, 2019/2020; Almheiri, Engelhardt, Marolf and Maxfield, 2019). The open problem for the ledger is to show *how* the server releases the encoded information into the Hawking radiation so that the emission follows the Page curve.

**Core-collapse supernovae: load shedding.** A supernova is not a black hole, but it shows the same load dynamics briefly reaching a limit and reversing. The standard mechanism (reviewed by Janka, 2012) is:

1. At the end of its life, a massive star has an iron core that can no longer release energy by fusion. Once the core grows too massive for electron degeneracy pressure to support it, it collapses within a fraction of a second.
2. The core reaches nuclear density, where matter becomes nearly incompressible. The infalling inner core stiffens and *bounces*, launching a shock wave outward.
3. The shock stalls, and heating by the enormous flood of neutrinos from the newborn proto-neutron star, aided by turbulent non-radial flows, helps revive it. The outer layers are then ejected.
4. The core remains as a neutron star or, if too much mass falls back or the remnant is too massive, collapses further to a black hole.

The neutrino burst is observed directly: Kamiokande-II and IMB detected neutrinos from SN 1987A hours before its optical discovery (Hirata et al., 1987; Bionta et al., 1987), in good agreement with this core-collapse picture.

In ledger language, Edmond proposes the following reading, which places the bounce on the **client side**. The collapsing core rapidly increases the load on the surrounding server nodes, but the limit it hits is not a server limit. It comes from the apps' own rules: the strong force and neutron degeneracy pressure make nuclear matter extremely stiff at separations of about $10^{-15}$ m. That scale is roughly 20 orders of magnitude above the Planck length, far from any node-level structure. The bounce is like water resisting compression: a property of what is being squeezed, not of the space it occupies. The core rebounds off this nuclear stiffness, and the neutrino flood sheds the load outward into the wider network.

Nuclear density is also not a hard wall. A core heavy enough overwhelms nuclear stiffness and keeps collapsing, forming a black hole. The **server-side** packing limit, if it exists, applies only far deeper, in black-hole interiors, where it may replace the singularity (an open question above). Compared like with like:

| | Length scale | Density |
|---|---|---|
| Client-side limit (nuclear stiffness) | $\sim 10^{-15}$ m (nucleon size) | $\sim 2.3\times10^{17}$ kg m$^{-3}$ (nuclear saturation) |
| Server-side cutoff (hypothetical) | $\ell_P \approx 1.6\times10^{-35}$ m | $\rho_P = c^5/(\hbar G^2) \approx 5.2\times10^{96}$ kg m$^{-3}$ |
| Ratio | $\sim 10^{20}$ | $\sim 10^{79}$ |

The nuclear limit is client-side, well understood, and can be exceeded; the Planck-density cutoff is server-side and hypothetical. The ledger model leaves the standard supernova mechanism, with its nuclear-matter bounce, neutrino heating and hydrodynamics, unchanged.

---

### 6.6 Virtual Particles as Internal Network Traffic (Interpretation)

*Caveat first.* In standard quantum field theory, "virtual particles" are internal lines in Feynman diagrams, that is, terms in a perturbative expansion of a scattering amplitude. They are *off-shell*: they do not satisfy $E^2 = p^2c^2 + m^2c^4$. They are never directly detected, and many physicists do not regard them as real objects at all. This paper does not claim otherwise. What follows is only an *interpretation* of the same mathematics, and it leaves every QFT prediction unchanged.

**The interpretation.** In ledger language, a virtual particle can be read as a *carrier signal*: internal traffic on the network. Force mediation, by photons for electromagnetism and gluons for the strong force, becomes client-to-client communication routed through the server ledger. The off-shell status fits this picture naturally. The traffic is internal to the server and is never rendered on the client side as a detectable particle, so it need not obey the client-side energy–momentum relation. Vacuum fluctuations would, in the same reading, be the server's background activity: fluctuations of the matter-field (client) states as described by standard QFT, not fluctuations of node positions, which stay fixed.

**Bound states.** The same reading extends to atoms. An electron in an atom is a standing wave, and its orbital shapes and discrete energy levels come from its Coulomb interaction with the nucleus, which QFT describes in terms of virtual-photon exchange. In ledger language, carrier-signal traffic between two client excitations sustains a standing-wave pattern between them, and this would be why bound states such as atoms have stable, discrete levels. This is again an interpretation only: the levels are still computed by the standard calculation, which is unchanged.

**Status.** This reading is interpretive and adds no new prediction yet. The measured effects that QFT computes using these terms, such as the Lamb shift in hydrogen (measured by Lamb and Retherford, 1947, and first estimated by Bethe, 1947), are reproduced by the standard calculation, not by the ledger. A similar caution applies to the Casimir effect: although it is often cited as evidence for vacuum fluctuations, Jaffe (2005) showed that Casimir forces can be computed without reference to zero-point energies, as forces between charges and currents. In the ledger picture the plate geometry would, like the atom, restrict which standing modes fit between the boundaries, but Jaffe's result means this too is one reading among several. Neither effect therefore singles out the ledger reading over others. In short, "virtual" means only that the carrier itself is never detected; the force it mediates is fully real and measured, as with the Casimir force, first measured precisely by Lamoreaux (1997). In ledger terms, server-side traffic is never rendered on the client side, but its effects are.

**A second test: cavity-modified atoms.** In the same reading, carrier traffic acts as the network's keep-alive signal: it cannot be switched off, but boundaries can thin it by restricting which carrier modes fit. A cavity around an atom removes some modes, and the atom's spontaneous emission rate and level shifts change measurably (Purcell, 1946; Kleppner, 1981; Goy et al., 1983; Heinzen & Feld, 1987). The ledger reading thus ties Casimir plates and cavity-modified atoms to one mechanism, mode thinning by boundaries, measured once with plates and once with an atom. As with the Casimir effect, standard QED already predicts these changes, so this is a consistency check rather than a test that singles out the ledger.

**Keep-alive traffic as the zero-point source (Hypothesis, toy-tested).** We postulate that the always-on keep-alive traffic supplies the zero-point jitter on which the entanglement value of G depends. On the 8-cable BCC grid with 16 fields per node, a purely mechanical (classical) server, uniform local damping plus independent local kicks leaves the normal modes uncorrelated, with mode energy set by the kick spectrum. Because the classical boundary correlation is unchanged by an overall rescaling, G depends only on the spectrum's shape, not its strength, so no ħ/2 level has to be chosen. Kicks whose power rises in proportion to frequency, cut off at the lattice's maximum frequency so the power per node stays finite, give $G \approx$ 1.00 along (100) and about 0.90 averaged over directions. They settle in about 500 cycles and stay steady for $10^5$ cycles. White-noise kicks act like heat and give $G \approx$ 0.46. A fixed per-node action floor and activity-scaled kicks fail ($G \approx$ 0.02 and 0.18). Each node needs a small memory, about eight internal filter variables, to shape its kicks. *Caveat: this moves the assumption from a hand-set jitter level to a hand-chosen kick spectrum, the same step taken in stochastic electrodynamics (Marshall, 1963; Boyer, 1975; de la Peña & Cetto, 1996); it holds for linear node rules only, and stochastic electrodynamics is known to fail for nonlinear systems.*

### 6.7 Spin, Exclusion, and Two Kinds of Client Apps

**Exclusion in standard physics.** The Pauli exclusion principle (Pauli, 1925) states that two identical fermions cannot occupy the same *complete* quantum state, and that state includes spin. It does not forbid them from sharing a region of space. The two electrons of helium both sit in the 1s orbital, with opposite spins. Each standing-wave pattern (mode, or orbital) can therefore hold at most two electrons, one per spin state. This rule is what builds up the shell structure of the periodic table, and it is a large part of why ordinary matter is rigid and resists compression.

**Ledger reading.** In the model, exclusion is a rule about the *occupancy of standing-wave states* on the server, not about nodes or locations. The server assigns each fermionic state at most one owner.

**Two kinds of client apps.** Bosons, such as photons, have no such limit: unlimited numbers can occupy the same state, which is what makes lasers and Bose–Einstein condensates possible. The server would then run two kinds of client apps: *exclusive* ones (fermions, which make up matter) and *shareable* ones (bosons, which carry forces).

**Relation to no-cloning.** Exclusion and no-cloning (Sec. 5.3) are distinct principles. No-cloning forbids making a copy of an *unknown* state. Exclusion forbids identical fermions from sharing *any* state. Bosons can pile into a known, shared state, as in a laser, without violating no-cloning. Both can still be read as server-side rules about the uniqueness of states.

**Standard origin and status.** In standard physics, exclusion follows from the antisymmetry of the joint wavefunction under exchange of identical fermions. The spin-statistics theorem (Pauli, 1940) connects this to spin: particles with half-integer spin are fermions, and particles with integer spin are bosons. The ledger model reinterprets these rules; it does not yet derive them. Deriving spin-statistics from the network structure is an open problem (Sec. 9).

### 6.8 Three Generations as Harmonics (Hypothesis)

*This subsection is speculative.*

**The observation.** Matter fermions come in three generations: the electron, muon and tau with their neutrinos, and the quark pairs up/down, charm/strange and top/bottom. Across generations, the particles have identical charges and interactions and differ only in mass. The heavier generations are unstable and play almost no role in ordinary matter. Precision measurements of the $Z$ boson's decay width at LEP give $N_\nu = 2.984 \pm 0.008$ light neutrino species (ALEPH et al., 2006), consistent with exactly three generations, at least for generations with a light neutrino. Why there are exactly three is unknown.

**Ledger hypothesis.** We propose that the three generations are three overtone modes of one node excitation pattern, much as one string supports a fundamental and its overtones. If so, the mode structure should fix the mass ratios between generations, which makes the idea testable. The test is the charged-lepton mass ratios, $m_\mu/m_e \approx 206.8$ and $m_\tau/m_\mu \approx 16.8$, and the empirical Koide relation, $m_e + m_\mu + m_\tau = \tfrac{2}{3}\left(\sqrt{m_e}+\sqrt{m_\mu}+\sqrt{m_\tau}\right)^2$, which holds to about $10^{-5}$ (Koide, 1983). That relation is empirical; neither the Standard Model nor this paper explains it.

*Caveat.* Plain overtones of a uniform pattern give evenly spaced frequencies ($f, 2f, 3f$), hence mass ratios near 2 and 1.5, not 207 and 17; a working mode rule needs strongly uneven spacing that is not yet identified. An earlier lattice version, in which the generations were read as the extra low-energy points ("doublers") along the three grid axes of the BCC rule, failed: it gives four species per Brillouin zone, not three, and its Wilson-split mass tiers give a Koide ratio of 0.33–0.50 instead of 2/3.

**Mass as frequency.** Rest mass sets a characteristic frequency through $E = mc^2 = h f_C$, the Compton frequency $f_C = mc^2/h$. In the ledger picture, distinct generations therefore correspond to distinct characteristic frequencies of the same excitation pattern. For the charged leptons, $m_\mu/m_e \approx 206.77$ and $m_\tau/m_e \approx 3477.2$ (CODATA 2022), so their Compton frequencies stand in the same ratios. Neutrinos show the frequency structure directly. Each flavor eigenstate $\nu_\alpha$ ($\alpha = e, \mu, \tau$) is a superposition of three mass eigenstates, $\nu_\alpha = \sum_i U_{\alpha i}\,\nu_i$, where $U$ is the Pontecorvo–Maki–Nakagawa–Sakata (PMNS) mixing matrix. The phases of the mass components advance at rates that differ in proportion to $\Delta m^2_{ij}$, so the flavor composition oscillates with baseline $L$ and energy $E$, with phase $\propto \Delta m^2_{ij} L / 4E$. This oscillation was established by Super-Kamiokande for atmospheric neutrinos (Fukuda et al., 1998) and by SNO for solar neutrinos (Ahmad et al., 2002), and it was recognized by the 2015 Nobel Prize in Physics (Kajita, McDonald).

*Caveat.* Everything in the preceding paragraph is standard physics. The harmonic picture reinterprets it and does not derive it. The model does not currently predict the mass-squared splittings $\Delta m^2_{ij}$, the PMNS mixing angles, or the absolute neutrino mass scale. It would gain real support only if those quantities followed from the network's mode structure.

**Link to Sec. 3.6.** Kobayashi and Maskawa (1973) showed that CP violation in the quark mixing matrix requires at least three generations; they shared the 2008 Nobel Prize in Physics for this work. Three generations are therefore the minimum structure that allows the kind of CP-violating bias Sec. 3.6 proposes. This is a structural requirement; it does not suggest that the generations exist for that reason.

**Status.** There is no derivation yet of the generation masses or of the number three. Deriving three modes and their mass ratios from the network is an open problem (Sec. 9).

### 6.9 Quantum Tunneling

In standard quantum mechanics, a particle's wavefunction does not stop at a barrier it classically cannot cross. Inside the barrier the amplitude decays exponentially, and if the barrier is thin enough, some amplitude survives on the far side. In ledger terms, the server-side wavefunction extends through and past the barrier with exponentially decaying amplitude, so a client render on the far side has a small but nonzero probability. This is a reinterpretation of well-established results: Gamow (1928) explained alpha decay as tunneling out of the nucleus, and the scanning tunneling microscope (Binnig, Rohrer, Gerber and Weibel, 1982) images surfaces atom by atom using the tunneling current. The ledger adds no new prediction here.

### 6.10 Vacuum Energy and the Cosmological Constant Problem (Target)

This is one of the largest open problems in physics, and the model does not claim to solve it. If the zero-point energy of quantum fields is summed up to a Planck-scale cutoff, the naive estimate of the vacuum energy density exceeds the observed dark-energy density by roughly 120 orders of magnitude (the exact figure depends on the cutoff assumed). Weinberg (1989) reviewed this mismatch and the proposed ways out.

In ledger terms, the vacuum is the server's idle traffic (Sec. 6.6). The problem then becomes a concrete target for the model. Either the ledger needs a mechanism by which idle server traffic does not gravitate at that level, or the network's finite number of degrees of freedom must reduce the estimate. The second option has precedent: Cohen, Kaplan and Nelson (1999) argued that if the entropy in a region is limited by its boundary area, as the Bekenstein bound suggests (Sec. 1.2), then effective field theory must cut off far earlier than the naive count assumes, which lowers the vacuum-energy estimate dramatically. A ledger with area-scaling degrees of freedom might realize this naturally. We list it as one of the most promising directions in Sec. 9, not as a result.

**Dark energy as a per-node cost (Hypothesis).** We postulate that dark energy is a server-side entry: a fixed energy $e$ per node. Expansion adds nodes everywhere, not at an edge, so total energy grows with node number while the density stays constant, giving $w = -1$ exactly. A Friedmann integration with this rule matches $\Lambda$CDM to machine precision ($2\times10^{-16}$ in $t(a)$). The fee must be $e \approx 1.1\times10^{-123}$ in Planck units; it is put in by hand, not derived. Area-limited capacity (Cohen, Kaplan & Nelson, 1999; Hsu, 2004; Li, 2004) does derive the $\sim10^{-122}$ scale, but only by letting a global horizon size set each node's amount: the Hubble-radius version gives $w = 0$, and the event-horizon version gives $w$ near $-1$ with a fitted constant $c$ of order one. Node allocation is treated as a server-side operation; only its effect is visible client-side. *Caveat: as stated, the per-node cost is a cosmological constant by construction, with a tuned value; it relabels $\Lambda$ rather than explaining it. Its one sharp consequence is that $w$ stays exactly $-1$ at all times (Sec. 7.7).*

**Where the expansion energy comes from: a balanced ledger (Hypothesis).** A finite network cannot draw on an infinite reserve, so we propose that expansion is booked double-entry, in the spirit of the zero-energy universe (Tryon, 1973). Each new node books a credit, its flat $w = -1$ fee, together with an equal negative gravitational debit. The net stays near zero, and the network converts gravitational binding into size rather than creating energy. This is consistent with the measured spatial flatness (curvature $|\Omega_k| \lesssim 0.002$ from CMB and BAO data), since a flat universe is the case usually associated with zero total energy. In general relativity gravitational energy has no local definition. The server can still book it node by node, while clients see only the global balance. Bound systems (atoms, planets, galaxies and galaxy groups) do not expand, so new nodes and the trade appear only in the unbound gaps between galaxy groups. An alternative, a finite pool that is drawn down so that dark energy weakens over time, is kept as a fallback in case future DESI results confirm a weakening trend. The flat fee with a balanced ledger remains the main line. *Caveat: "total energy" of the universe is not uniquely defined in general relativity, so the zero-energy picture is a bookkeeping interpretation, not a derived result; the per-node debit rule is postulated, and the fee's size remains open (open problem 24).*

**Early expansion as load-triggered node splitting (Hypothesis).** In the early hot phase, we postulate that a node splits when its load exceeds a threshold $E_*$. New nodes start in their own quantum ground state rather than copying the parent (consistent with no-cloning); their vacuum fluctuations are stretched by the growth and frozen, seeding structure. The split rate follows slot occupancy: internal slots fill at random, counted in log-load $x = \ln(E/E_*)$, and a split fires when one slot is filled, giving $H^2 \propto 1 - e^{-bx}$, i.e. $1 - E_*/E$ for $b = 1$. A toy calculation (quantum mode functions on the node-rule background, asynchronous splits) gives, at 55 e-folds, $n_s = 0.9658$, $r = 0.0022$ for $b = 1$ and $n_s = 0.9663$, $r = 0.0032$ for $b = \sqrt{2/3}$, with running $\approx -6\times10^{-4}$ and a graceful exit once the load falls below $E_*$. Requiring a filled pair instead squares the rule and reproduces the Starobinsky plateau form exactly (Starobinsky, 1980), with $n_s \approx 0.965$, $r \approx 0.003$, so the two rules are observationally close; compare Planck 2018, $n_s = 0.9649 \pm 0.0042$ (Planck Collaboration, 2020, paper X), and BICEP/Keck, $r < 0.036$ (BICEP/Keck Collaboration, 2021). Alternatives fail: occupancy counted in raw energy collapses abruptly; fixed split fractions and log rules give $r$ too high (the power-law and $\phi^2$ models); synchronized splits leave visible ripples in the spectrum. Testable: $r \approx 0.002$–$0.004$ and $n_s \approx 1 - 2/N$, within reach of LiteBIRD and CMB-S4. *Caveat: this restates known Starobinsky/$\alpha$-attractor physics in node language. The log-load counting, slot size $b$ and energy scale are chosen, not derived, and the calculation is quantum field theory on a background, not a lattice field simulation. The slot-pair idea arose in brainstorming with the Intuition assistant.*

### 6.11 Dark Matter as Unrendered Client Apps (Hypothesis)

*This subsection is speculative.*

**The evidence.** Several independent observations point to matter that gravitates but does not interact with light: the rotation curves of galaxies, gravitational lensing by galaxies and clusters, and the pattern of acoustic peaks in the cosmic microwave background. The Planck 2018 results give a cold dark matter density $\Omega_c h^2 = 0.120 \pm 0.001$ against a total matter density $\Omega_m h^2 \approx 0.143$, so dark matter makes up roughly 84% of all matter (Planck Collaboration, 2020).

**Ledger hypothesis.** We propose that dark matter is a third kind of client app, alongside the exclusive (fermion) and shareable (boson) apps of Sec. 6.7. It is an excitation that loads the server, and so gravitates under the load proposal of Sec. 6.4, but does not couple to the electromagnetic force carriers of Sec. 6.6. It is therefore never rendered as light. This fits the principle stated in Sec. 6.6: server-side effects can be fully real even when nothing is rendered on the client side.

**The Bullet Cluster constraint.** In the merging cluster 1E 0657–558, gravitational lensing shows that most of the mass follows the galaxies, while the hot X-ray gas, which holds most of the ordinary matter, has been slowed and left behind (Clowe et al., 2006). Dark matter therefore behaves like nearly collisionless particles that moved apart from the gas, so it cannot be a fixed, static property of the network. This is why the model treats it as moving excitations, which keeps it close to standard particle dark matter.

**Bootstrapping structure.** Because dark matter does not feel radiation pressure, it could begin clumping in the early universe before ordinary matter could. It formed gravitational potential wells into which ordinary matter later fell to build galaxies. In this sense dark matter bootstraps the visible client side; this describes the order of events, and no intent is implied.

**Contrast with emergent gravity.** Some proposals, such as Verlinde's emergent gravity (2017), aim to explain the phenomena attributed to dark matter with no dark matter at all, as an additional gravitational effect of the underlying microscopic degrees of freedom. Such approaches face difficulty with cluster observations, including the mass–gas offset in the Bullet Cluster. The ledger model does not take that route.

**Dark matter as a light scalar ripple (Hypothesis).** We postulate that dark matter and the Higgs are different things delivered by a similar server-side mechanism: a scalar field held as an internal state at every node, whose ripples are client-side apps. The Higgs is the heavy, short-lived setting; dark matter would be a very light, stable, symmetry-protected setting (axion-like, "fuzzy"; Hu, Barkana & Gruzinov, 2000; Hui et al., 2017) coupled to nothing visible. Its halos act as gravity wells, a scaffolding into which ordinary matter falls, and it bends light only through the nodes' load. A $128^3$ Schrödinger–Poisson toy (local per-node updates except the gravity solve) forms a halo whose soliton core matches the known ground-state profile within 3–6% (cf. Schive, Chiueh & Broadhurst, 2014), with persistent granules (density fluctuations of about 100% rms) and growth suppressed below the Jeans scale, the fuzzy signature. Mass is conserved to $3\times10^{-12}$ and energy to about 0.01%. *Caveat: the outer halo falls as about $r^{-2.3}$ rather than the NFW $r^{-3}$ in this isolated, non-expanding box, and more run time did not steepen it. A rerun on an expanding grid with ongoing infall gave the same settled slope (about $r^{-2.3}$, briefly near $r^{-3.3}$ during one infall burst), which we take as within range given the unresolved core and single seed. Lyman-alpha bounds push the particle mass above about $2\times10^{-21}$ eV (Iršič et al., 2017), in tension with kpc-sized cores.*

**Side note: an alternative reading as shared-hardware contention (speculative, not tested).** As an alternative only, dark matter could be the load of a second routine running on the same nodes: a background process that is never read, so its states are never locked into outcomes (Sec. 3.3) and it stays uncollapsed, with a high-entropy profile unlike the visible sector. Lacking any radiating channel (no photon-like links to the visible sector or within itself), the background load cannot shed kinetic energy, so it clusters into extended virialized halos but cannot cool and condense into stars or planets. Its work draws on the same node cycles, so it would slow the local update rate and raise routing cost by the load mechanism of Sec. 6.4, and would be felt through gravity only. With no gauge coupling to the visible sector it would be collisionless and dark. A simpler variant, in which the shared substrate acts as a low-pass filter that spatially blurs the visible load, is weaker: a blur would follow the visible gas and would fail the Bullet Cluster offset. A link to the matter–antimatter asymmetry (Sec. 3.6), with antimatter held in the background routine, is possible but not required and is not argued here. *Open problem:* the background load would have to be about 5.4 times the visible baryonic load (dark matter is about 84% of all matter), and nothing in this picture yet explains that ratio. We see no way to test this reading at present.

*The Bullet Cluster in this reading (qualitative, not simulated).* In a cluster merger the visible gas couples electromagnetically, so the two gas clouds meet under ram pressure, shock, and slow near the collision center. The background load has no electromagnetic coupling and, within observational limits, little self-interaction (a cross-section per unit mass below about 1 cm$^2$ g$^{-1}$; Randall et al., 2008), so it passes through largely unhindered with its own momentum. Its load footprint therefore ends up ahead of the slowed gas, and the lensing peaks would sit offset from the baryons, as observed.

**Status.** This reinterprets particle dark matter in ledger language. The light-scalar variant is tested only in a toy: its core, granules and small-scale suppression are reproduced, while the outer slope and the mass bound remain open (Sec. 9).

### 6.12 The Higgs Sector and a Toy Network (Hypothesis)

*This subsection reports exploratory calculations. The numbers are first-pass estimates, not a derivation of the Higgs sector.*

**Higgs field as server state, boson as client app.** In the ledger language, the Higgs vacuum value $v \approx 246$ GeV is a property of the network's ground state, held server-side at every node. The Higgs boson, observed at the LHC in 2012 (ATLAS Collaboration, 2012; CMS Collaboration, 2012) and now measured at $M_H \approx 125.2$ GeV, is a client-side excitation of that state. At tree level $m_H = \sqrt{2\lambda}\,v$, so $\lambda \approx 0.13$ and $m_H/v \approx 0.51$. The ratio measures how stiff the ground state is against small displacements.

**Mass as a fixed rate card (Hypothesis).** In ledger terms the Higgs setting acts as a fixed rate card held at every node: $v \approx 246$ GeV is the same everywhere and does not change with the number of particles present or with the load a node carries. Each particle type is billed at a fixed rate set by its Yukawa coupling $y$, with $m = y\,v/\sqrt{2}$: the electron at $0.511$ MeV ($y_e \approx 2.9\times10^{-6}$), the top quark at about $173$ GeV ($y_t \approx 1$). Photons and gluons have no Yukawa coupling and are not billed. The charge is booked to the network as load (slowed link timing), not to the Higgs setting, which is why mass gravitates; in the double-entry picture, rest mass and its gravitational load are matching entries. The charge is a standing one, re-applied at every hop through the left/right slot swap (the lattice counterpart of Zitterbewegung) rather than drained tick by tick, so setting $v = 0$ would make the electron massless at once. Most visible mass is not billed this way: the Higgs-given masses of a proton's valence quarks total about 9 MeV of its 938 MeV, and the rest is QCD binding energy, which here is internal link traffic booked directly as load with no Higgs entry (Yang et al., 2018). The Higgs setting does depend on temperature: above the electroweak crossover (about 160 GeV) $v$ falls to nearly zero and the rate card is cleared. *Caveat: this is a bookkeeping restatement of the Standard Model mass mechanism; it does not explain the values of the Yukawa couplings or of $v$.*

**The hierarchy problem.** Radiative corrections to the Higgs mass parameter grow with the square of the ultraviolet cutoff $\Lambda$, while $m_H/M_{\text{Pl}} \sim 10^{-17}$. A discrete network supplies a physical cutoff, so the corrections are finite, but this is shared by any lattice regularization and does not remove the fine-tuning: the bare parameters must still cancel to high precision. A related scale puzzle is the weakness of gravity, $(m_p/M_{\text{Pl}})^2 \sim 6\times10^{-39}$ for the gravitational coupling between protons, compared with $\alpha \approx 1/137$. The ledger model offers no explanation of either hierarchy at present; both are open problems (Sec. 9).

**Edge-of-stability precedent.** Froggatt and Nielsen (1996) proposed that the Standard Model effective potential has two degenerate minima, one near the Planck scale, and predicted $M_t = 173 \pm 5$ GeV and $M_H = 135 \pm 9$ GeV before either the Higgs was found or the top mass was precise. Shaposhnikov and Wetterich (2010) argued that asymptotically safe gravity drives $\lambda \to 0$ near the Planck scale, giving $m_H \approx 126$ GeV. Buttazzo et al. (2013) showed that the measured parameters place the SM vacuum close to the boundary between stability and metastability. Our independent rerun (two-loop SM RGEs with the Buttazzo et al. matching conditions) reproduced the Froggatt–Nielsen result, $M_t \approx 173.3$ GeV and $M_H \approx 131$ GeV for $\phi_2 = 10^{19}$ GeV. It also found a typographical error in their Eq. (1) (a $\phi^4$ that should read $\phi^3$), which does not affect their result. Imposing $\lambda(M_{\text{Pl}}) = 0$ gives $M_H \approx 128.8$ GeV against the measured 125.2 GeV, agreement within about 3%. Exact agreement would require $M_t \approx 171$ GeV, compared with the measured 172.6 GeV, where the translation from the measured top mass to the pole mass used here carries an interpretive uncertainty of roughly 1 GeV. With current inputs, $\lambda$ reaches a minimum of about $-0.011$ between $10^{17}$ and $10^{19}$ GeV: the vacuum sits near a critical point and is metastable. In ledger terms, this is a candidate statement that the network's ground state sits near a critical point; it is not yet a derivation.

**Toy network.** To check what this means for a discrete substrate, we studied a 4D hypercubic lattice at Planck spacing, with 8 nearest neighbours per node and one complex doublet $\phi_x$ per node. The doublet's content matches that of a qubit: 2 complex amplitudes, or 4 real components, the same as the Higgs doublet. The lattice action is

$$S = \sum_x \Big[-2\kappa \sum_{\mu=1}^{4} \phi_x\cdot\phi_{x+\hat\mu} + \phi_x^2 + \lambda_L(\phi_x^2 - 1)^2\Big],$$

with hopping parameter $\kappa$ and lattice self-coupling $\lambda_L$. The main findings are:

- At $\kappa = 0.49$ the network sits deep in the ordered phase, and $m_H$ comes out at the Planck scale.
- In the free theory, the critical point is exactly $\kappa_c = 1/8$, the inverse of the number of neighbours. Monte Carlo runs on $L = 8, 12, 16$ lattices (Binder-cumulant crossings, figure below) show that self-interaction shifts it upward: $\kappa_c = 0.1259 \pm 0.0005$ ($\lambda_L = 0.001$), $0.1288 \pm 0.0009$ ($\lambda_L = 0.01$) and $0.1442 \pm 0.0014$ ($\lambda_L = 0.05$). Mean-field theory places the critical point below $1/8$ for these couplings and misses this shift.
- Just past criticality the measured vacuum value follows $v^2 \propto \Delta\kappa = \kappa - \kappa_c$, as expected near a critical point.
- Obtaining $v = 246$ GeV with Planck spacing requires $|\kappa - \kappa_c| \sim 10^{-34}$. This is the hierarchy problem restated on the lattice, not a solution to it.
- Radiative symmetry breaking (Coleman and Weinberg, 1973) could in principle generate a small offset from a massless starting point. In the pure SM it does not, because the top-quark contribution dominates and has the wrong sign. Working radiative models add a hidden scalar or gauge sector (Gildener and Weinberg, 1976). In ledger terms, this would mean an extra server-side field.

![Binder cumulant versus hopping parameter $\kappa$ for $L = 8, 12, 16$ at several $\lambda_L$. The crossing of the curves estimates the interacting critical point $\kappa_c$, which lies above the free value $1/8$.](binder.png){width=80%}

**Self-tuning the knob by homing (Hypothesis, toy-tested).** A local rule can bring $\kappa$ close to $\kappa_c$ without hand tuning, provided it has a signal that peaks there. We use the anisotropy cost $C = -N\,\mathrm{Var}(a_n)$, where $a_n$ measures how far the field leans away from being symmetric across its four components. The rule works like CNC homing to a limit switch. The knob is dithered by $\pm\delta$, and it steps at a fixed full seek rate toward whichever side has the better cost, over at least half of the range $[0.10, 0.20]$. After that it keeps stepping at full rate and shrinks the step ($\times 0.7$) only when the up/down comparison flips sign *and* the difference exceeds twice its recent median absolute deviation, a confirmed signal from the stopper. The comparison is taken per patch over 8 octants and combined by median. On the O(4) $\phi^4$ toy ($\lambda_L = 0.05$, 8-link BCC grid, $\kappa_c \approx 0.1495$), all 12 runs locked, from hot ($\kappa_0 = 0.10$) and cold ($\kappa_0 = 0.20$) starts with 3 seeds each (figure below). They locked at $\kappa_f - \kappa_c = +0.0063 \pm 0.0018$ ($L = 8$) and $+0.0062 \pm 0.0008$ ($L = 12$), on the ordered side, in about $1.2\times10^5$ ticks. A variant that also held back the step until a signal appeared stalled in the flat part of the cost curve and locked in none of 18 runs: the seek must not slow before the stopper is sensed. *Caveat: the residual bias of about $+0.006$ does not shrink from $L = 8$ to $L = 12$, because the lock tracks the finite-size peak of the cost rather than $\kappa_c$ itself. The cold starts never completed the 50% seek stage and were carried in by the later full-rate steps. The toy uses a BCC grid, not the hypercubic lattice above, and the rule still has hand-set constants (dither size, period, the shrink factor and the 2·MAD threshold). Getting from $10^{-3}$ to the $10^{-34}$ required for $v = 246$ GeV is not addressed; the hierarchy problem remains open (Sec. 9).*

![Homing the Higgs knob. $\kappa$ versus ticks for hot ($\kappa_0 = 0.10$) and cold ($\kappa_0 = 0.20$) starts at $L = 8$ and $12$: a full-rate seek, then a step that shrinks only on confirmed flips. All 12 runs lock about $+0.006$ above $\kappa_c$.](seek50.png){width=80%}

*(Hypothesis)* We read the $\phi^4$ potential as an effective description rather than the mechanism itself. It is the smooth curve that summarizes how the node field behaves near the transition, which is why its weights are not uniquely fixed: a family of $(a_1, a_2)$ pairs reproduces the same $m/v$. The mechanism we propose is a homing loop, analogous to a CNC axis homing onto a limit switch. The coupling $\kappa$ moves at full seek rate until a confirmed anisotropy signal registers the transition, and then it creeps in with shrinking steps. In simulation, this loop locks $\kappa$ within about $+0.006$ of $\kappa_c$ in 12 of 12 runs.

**The Higgs boson as a ripple (Hypothesis).** Because the Higgs field is held at every node, a Higgs excitation can be produced at any location where sufficient energy ($\gtrsim 125$ GeV) is concentrated. It behaves as a resonance with three stages (request $\to$ response $\to$ close): incoming energy concentrates; the field rings as a standing $k=0$ oscillation, all nodes in step, at a pitch set by the field's own stiffness rather than by the input; and within $\sim 10^{-22}$ s it subsides, handing its energy to other fields (swapped, not wiped) as the ripple settles back to the ground state. A real-time toy (one boson coupled to a 1500-mode scalar bath, exact Schrödinger evolution) reproduces this: the absorption peak sits at $0.992\,m_H$, the fitted decay rate is $\Gamma = 0.0399$ against the golden-rule value $0.0394$, and the coherence of a "boson / no boson" superposition falls from $0.5$ to below $0.07$ as the decay products escape and leave a record. With a 12-mode bath the energy flows back and the coherence revives to $0.48$, so the closing step is irreversible only because the products spread into very many modes. *This is a toy, with a scalar bath standing in for the real decay channels; it does not address why $v = 246$ GeV.*

**Caveats.** The lattices are small and the error bars are sizable. Gauge fields and the top quark are not included on the lattice. A hypercubic lattice breaks rotational and Lorentz symmetry (see Sec. 7.3). The mean-field and Monte Carlo results disagree on the direction of the shift, and the conversion from lattice units to GeV is schematic. The near-zero $\lambda(M_{\text{Pl}})$ result is the strongest part of this subsection, and it was established in the earlier literature, not by the ledger model.

### 6.13 An Information Cap per Node (Hypothesis)

This subsection applies a known bound to the network geometry. It is offered as a potential candidate constraint on the model, not as a result.

**The bound.** The Bekenstein–Hawking entropy of a black hole is $S = A/(4 l_P^2)$ in natural units (nats), where $A$ is the horizon area (Bekenstein, 1973; Hawking, 1975). Converting to bits, this is about 1 bit per $4\ln 2 \approx 2.77$ Planck areas, or roughly 0.36 bits per Planck area. Under the holographic principle ('t Hooft, 1993; Susskind, 1995; reviewed by Bousso, 2002), no region can hold more information than a black hole of the same boundary area, so this is the maximum for any region.

**Applied to cubic Planck nodes.** Take the model's nodes as cubes of side $l_P$ carrying one qubit each, on a 4D grid with 6 spatial and 2 temporal links per node.

- *Single node.* A cube has 6 faces of one Planck area each, so the cap is $6/2.77 \approx 2.2$ bits. One qubit is within the cap.
- *Block of $N \times N \times N$ nodes.* With independent qubits the block holds $N^3$ bits, while the cap from its surface is $6N^2/2.77 \approx 2.2\,N^2$ bits. The volume count exceeds the cap for $N > 2.2$.
- *Independent bits per node.* Inside a block $N$ nodes wide, each node can carry at most about $2.2/N$ independent bits: about 0.2 for $N = 10$, and about $10^{-20}$ for a proton-sized region ($N \sim 10^{20}$).

**Interpretation.** Each node can still hold a qubit, but the node states within a region cannot all be independent. Nearly all of them must be entangled with one another or determined by the boundary, so the number of free degrees of freedom scales with surface area rather than volume. In ledger terms, the server stores a region largely through its boundary, with a tightly correlated interior. This is consistent with holography and with proposals that spacetime connectivity arises from entanglement (Van Raamsdonk, 2010; Maldacena and Susskind, 2013).

The bending of light near a mass, with deflection angle $4GM/(c^2 b)$ for impact parameter $b$, measures curvature. Its upper value is of order the Planck curvature, $\sim 1/l_P^2$. It describes how strongly nodes are loaded (an effective curvature on rigid nodes), not how many states they hold; the state count comes from the entropy bound above.

**Finite processing rate (Hypothesis).** The storage cap above has a companion cap on speed. The Margolus–Levitin theorem limits a system of mean energy $E$ above its ground state to at most $2E/(\pi\hbar)$ distinguishable state changes per second (Margolus & Levitin, 1998); read in ledger terms, each node has a finite clock rate set by its load. Quantum algorithms respect matching ceilings: Grover search gives only a square-root speedup over classical search, and this is provably optimal (Bennett, Bernstein, Brassard & Vazirani, 1997), while quantum computers are widely believed not to solve NP-complete problems efficiently. Present-day quantum-computer run times are not used as evidence here, since they reflect engineering limits (gate errors, noise, error correction) rather than limits of the underlying ledger. Together, finite bits per region and finite updates per second point to a server with large but finite capacity, consistent with the paper's exclusion of actual infinities.

**Information cap on the 8-cable grid (Hypothesis, toy-tested, partial).** On the 8-cable BCC grid with 16 fields at the zero-point jitter level, the classical mutual information a region shares with its outside is proportional to the number of crossing cables, not to the volume (linear fit $R^2 = 0.999$ against cable count versus $0.93$ against node count at $L = 11$; slabs of fixed cut and $2.4\times$ volume share identical information). Taking a cable's capacity as two fields, each a Gaussian channel with signal at most the jitter level, gives 1 bit per tick per cable; the observed sharing is 0.74–0.85 bits per crossing cable for cubes, spheres, slabs and rods, below this min-cut bound. With linear node rules, information injected inside a region reaches the outside at no more than 10% of the bound. The cap limits boundary-crossing information only; internal scrambling is unconstrained. The bound does not set $G$: a saturated cap would give $G \approx 0.72$, whereas the steady state gives $G \approx 0.95$, using about 75% of capacity. *Caveat: classical Gaussian mutual information only; the capacity depends on the SNR = 1 choice; the nonlinear (scrambling) case rests on the locality argument and was not confirmed numerically; small grids.*

**Caveats.** The argument assumes that the holographic bound applies to the lattice. This is the standard argument (any region could in principle collapse to a black hole), but it has not been proven for a discrete network. A simple cubic lattice is anisotropic, so the factor 2.2 depends on node shape and would change for a different cell geometry; the $N^2$ versus $N^3$ scaling does not. The model does not yet supply an update rule that produces area-law entanglement (open problem 14).

### 6.14 Toward General Relativity (Hypothesis)

This subsection outlines how the ledger might connect to general relativity (GR). None of the steps below has been carried out for this model; they are offered as potential candidate paths, building on Sec. 6.4. The subsection first states the model's primary picture (rigid nodes carrying a directional workload) and then lists the existing mathematical machinery that could make it quantitative.

**Primary picture: rigid nodes, varying workload.** In this model the nodes are *rigid*: mass does not stretch, shrink or bend them. Mass-energy instead changes the *workload* of the nodes it occupies and of those nearby. Curvature is then *effective*: what changes near a mass is the cost of routing a signal through loaded nodes and the rate at which local client-side clocks tick, not the shape of the nodes. Observers who can only measure paths and clock rates would describe these changes with a curved effective metric $g_{\mu\nu}$. The motivation for rigid nodes comes from how motion is represented. A moving object, even a massive one at high velocity, does not travel *through* the network: its pattern (its state) is re-plotted from node to node at each update, as an image moves across a screen of fixed pixels. Since no node is carried along, motion gives no reason for node shape to change. This picture has precedents. Zuse (1969; English translation 1970) proposed that physical processes could be computed by a cellular automaton, with particles represented as "digital particles", patterns propagating across fixed cells. 't Hooft (2016) developed a deterministic cellular-automaton interpretation of quantum mechanics, in which quantum mechanics is used as a tool to describe an underlying classical automaton.

*Caveat. A fixed grid of nodes defines a rest frame, so motion relative to the nodes would in principle be detectable. Experiments find no preferred frame for local physics (see the Lorentz-symmetry discussion under Key limitation below). The update rules must therefore make re-plotted motion indistinguishable from uniform motion in any inertial frame; whether they can is open.*

**Precedent: effective (optical and analogue) geometry.** Gordon (1923) showed that light in a moving dielectric medium propagates as if in an effective spacetime metric (the "optical metric"). The analogue-gravity programme, reviewed by Barceló, Liberati and Visser (2011), studies many systems in which perturbations of a flat-space medium obey wave equations in an effective curved metric; Unruh (1981) proposed that sound in a transonic fluid flow would show a sonic horizon emitting a thermal, Hawking-like spectrum. The weak-field Schwarzschild solution can be read in the same way. In isotropic coordinates, to first order in $GM/(rc^2)$, the metric is
$$ds^2 \approx -\Big(1-\tfrac{2GM}{rc^2}\Big)c^2dt^2 + \Big(1+\tfrac{2GM}{rc^2}\Big)(dx^2+dy^2+dz^2),$$
so the coordinate speed of light is $c/n(r)$ with an effective refractive index
$$n(r) \approx 1 + \frac{2GM}{rc^2}.$$
Ray optics in this medium gives, to the same order, the GR light deflection $4GM/(c^2 b)$ for impact parameter $b$ and the Shapiro time delay of signals passing the mass. Clock rates are a separate piece of the metric: static clocks run at $d\tau/dt \approx 1 - GM/(rc^2)$, the gravitational time dilation that the GPS system corrects for. In ledger terms, $n(r)$ is the extra routing cost through loaded nodes and $d\tau/dt$ is their reduced tick rate (Sec. 6.4). *This equivalence holds only for static, weak fields at first order; it is not a derivation from the node rules.*

**Why one number per node is not enough.** A scalar workload (one number per node) cannot reproduce GR. A static index $n(r)$ captures light paths around a non-rotating mass, but it contains no momentum-flow components, so it cannot produce frame dragging around a rotating mass, which Gravity Probe B measured (Everitt et al., 2011). Gravitational waves in GR carry two tensor polarizations; the three-detector observation of GW170814 allowed the first test of polarization content, and the LIGO–Virgo analysis found Bayes factors of more than 200 and 1000 for purely tensor polarization against purely vector and purely scalar polarization (Abbott et al., 2017). Historically, Nordström's scalar theory of gravity gave a conformally flat spacetime and therefore predicted no global bending of light (reviewed by Norton, 1992), which is one reason it was abandoned. The workload must therefore be directional: a tensor, not a number.

**Workload from apps: the 4-momentum.** Each client app carries its mass and its vector of propagation, combined in the 4-momentum $p^\mu = (E/c,\,p_x,\,p_y,\,p_z)$. For a point-like app ($c = 1$), its contribution to the workload is
$$W^{\mu\nu} = \frac{p^\mu p^\nu}{E}\,\delta^3\big(\mathbf{x}-\mathbf{x}_{\text{app}}(t)\big),$$
the standard stress–energy tensor of a point particle. It is symmetric $4\times4$, with 10 independent components. Summing the contributions of all apps on a node (divided by the node volume) gives the node's workload tensor, which is identified with the matter energy–momentum tensor $T^{\mu\nu}$: $T^{00}$ is energy density, $T^{0i}$ momentum density (energy flux), $T^{ii}$ pressure and $T^{ij}$ ($i\neq j$) shear stress. The effective metric $g_{\mu\nu}$, also with 10 components, is the network's response to this workload. The hypothesized link in the continuum limit is the Einstein equation $G_{\mu\nu} = 8\pi T_{\mu\nu}$ ($G = c = 1$). Massless apps ($E = |\mathbf{p}|c$) contribute as well, consistent with light gravitating (Sec. 6.4). *The response rule from workload to $g_{\mu\nu}$ is assumed here, not derived.*

**Mathematical machinery.** The routes below are existing frameworks that could supply the workload-to-metric rule. In each, the geometric language should be read as *effective*: it describes paths and clock rates on rigid nodes.

**The task: a continuum limit.** GR describes a smooth geometry. In the ledger, that geometry would have to arise as a continuum limit: node contributions are summed over regions much larger than the Planck spacing, and the averaged result is an effective smooth metric. The question is which node-level quantity, after averaging, behaves as curvature.

**Route A: thermodynamics of horizons.** Jacobson (1995) showed that if entropy is proportional to horizon area, and the Clausius relation $\delta Q = T\,dS$ holds on every local Rindler horizon, then the Einstein equations follow as an equation of state. The area-law cap of Sec. 6.13 supplies the first ingredient, provided the node entanglement actually obeys an area law.

**Route B: entanglement first law.** Lashkari, McDermott and Van Raamsdonk (2014) and Faulkner, Guica, Hartman, Myers and Van Raamsdonk (2014) showed that the first law of entanglement, $\delta S = \delta E$ for ball-shaped regions, implies the Einstein equations linearized about the background geometry. These results are derived within AdS/CFT (holographic conformal field theories), so they do not transfer directly to the ledger; they indicate that entanglement structure can carry gravitational dynamics.

**Route C: sum over geometries.** Causal dynamical triangulations (CDT) build spacetime from simple flat simplices glued with a fixed causal (time) structure and sum over all such gluings. Simulations report a macroscopic four-dimensional universe emerging (Ambjørn, Jurkiewicz and Loll, 2004), whose large-scale shape matches a de Sitter universe (Ambjørn, Görlich, Jurkiewicz and Loll, 2008), and whose spectral dimension is about 4 at large scales and about 2 at short scales (Ambjørn, Jurkiewicz and Loll, 2005). Evidence for a second-order transition line has been reported (Ambjørn, Jordan, Jurkiewicz and Loll, 2011). The physically acceptable phase appears only near such transition lines, which parallels the near-critical behaviour discussed for the Higgs sector in Sec. 6.12.

**Regge calculus: curvature from counting.** In Regge calculus (Regge, 1961), spacetime is assembled from identical flat blocks of fixed size. No block is curved. Curvature appears only at the hinges where blocks meet, as a *deficit angle* set by how many blocks meet there; smooth GR curvature is the large-scale average of these deficits. This is consistent with the ledger's assumption of no structure finer than one node. As an intuition: LEGO bricks look square up close but can form a smooth curve at a distance. In the ledger reading the blocks are not physically rearranged: the deficit angles are *effective*, describing how workload changes paths and clock rates around each hinge, rather than a geometric bending of rigid nodes.

**From deficit angles to the Einstein tensor.** In 4D Regge calculus the hinges are 2D triangles, and the Regge action is
$$S_{\text{R}} = \frac{1}{8\pi}\sum_h A_h\,\varepsilon_h \qquad (G = c = 1),$$
where $A_h$ is the area of hinge $h$ and $\varepsilon_h$ its deficit angle. For small simplices, $\varepsilon_h$ is approximately the curvature times the area around the hinge, so the deficit angles supply the curvature side of the field equations, $G_{\mu\nu}$. In the ledger reading, the node workload tensor supplies the other side, $T_{\mu\nu}$: concentrations of workload are associated with larger effective deficit angles nearby. Each flat simplex acts as a local tangent (locally flat) frame, and the deficit angles measure the mismatch between neighbouring frames. Curvature therefore resides on the hinges, not inside the blocks. A 4-simplex has 5 vertices, and every choice of 3 of them spans a triangle, giving $\binom{5}{3} = 10$ triangular hinges per simplex. This count matches the 10 independent components of the symmetric tensors $G_{\mu\nu}$, $g_{\mu\nu}$ and the workload tensor $T^{\mu\nu}$, and each hinge 2-plane in 4D is built from six basic orientations ($tx, ty, tz, xy, xz, yz$). *Whether this numerical match reflects more than a counting coincidence is open.* Technically, in Regge calculus the edge lengths (also 10 per 4-simplex) fix each block's flat shape and are the variables varied to make $S_{\text{R}}$ stationary, giving the Regge equations, whose continuum limit is the Einstein equation $G_{\mu\nu} = 8\pi T_{\mu\nu}$; in the fixed-block (dynamical triangulation) version the connectivity is varied instead. Cheeger, Müller and Schrader (1984) proved that the curvature of a piecewise-flat space converges to the smooth curvature, in the sense of measures, when the piecewise-flat space approximates the smooth one suitably. In SI units the coupling is $8\pi G/c^4 \approx 2.1\times10^{-43}\ \text{s}^2\,\text{kg}^{-1}\,\text{m}^{-1}$; in ledger terms this small number acts as the stiffness relating workload to the effective deficit it produces, which is why everyday masses produce only tiny deficits.

\begin{figure}[tp]
\centering
\includegraphics[width=\linewidth]{regge_convergence.png}
\caption{A 2D Regge-calculus test (unit sphere and ellipsoid built from flat triangles; subdivided icosahedron, levels 0–6). The total deficit angle equals $4\pi$ to rounding error at every level (Gauss–Bonnet). On the sphere, the vertex curvature $K_v = \varepsilon_v / A_v$ with Voronoi dual areas converges to the exact $K = 1$ at order $h^2$: the maximum error falls from 31\% (12 vertices) to $8.9\times10^{-5}$ (40,962 vertices). On an ellipsoid ($c = 0.6$), curvature summed over a region converges (error $5\times10^{-4}$), while the single-vertex error stalls near 9\% because the mesh is not regular. Left: level-2 sphere coloured by deficit angle. Right: error versus mean edge length $h$.}
\label{fig:regge}
\end{figure}

*Caveats. In 2D the Regge action is topological (Gauss–Bonnet), so this demonstration shows curvature emerging from deficit angles, not gravitational dynamics. Pointwise convergence depends on mesh quality; smooth curvature emerges reliably only as a large-scale average. A fixed cubic grid does not bend geometrically: every hinge has the same deficit. In the rigid-node picture, curvature must therefore be effective, carried by variations in workload rather than in connectivity or edge lengths.*

**Calibration against classical tests (rough estimate).** As a first rough estimate only, the node rule's free parameters could be fixed by requiring its large-scale averages to reproduce well-measured GR results:

- solar light deflection at the limb, 1.75 arcsec;
- Mercury's anomalous perihelion advance, about 43 arcsec per century;
- the Shapiro delay, where Cassini tracking gives $\gamma - 1 = (2.1 \pm 2.3)\times10^{-5}$ (Bertotti, Iess & Tortora, 2003);
- the net GPS satellite clock rate offset, about 38 µs per day;
- the orbital decay of the Hulse–Taylor pulsar PSR B1913+16, where the observed-to-GR ratio is $0.9983 \pm 0.0016$ (Weisberg & Huang, 2016).

Matching these would be a consistency estimate, not a derivation: a rule tuned to reproduce GR in the weak field says little by itself. The primary task is to derive the node logic so that these results follow without fitting. Outputs in the Planck regime would then become predictions rather than adjustable features.

The gap between tested scales and the node scale is large. The inverse-square law has been tested down to separations of 52 µm (Lee et al., 2020), about $3\times10^{30}$ Planck lengths. The smallest source mass whose gravitational coupling has been measured is about 90 mg (Westphal et al., 2021), roughly $4\times10^{3}$ Planck masses ($m_P \approx 2.18\times10^{-8}$ kg), spread over a region of about 1 mm. No current experiment probes gravity at the scale of a single node.

**Key limitation.** A rigid grid with a *scalar* workload fails: it cannot produce frame dragging or tensor gravitational-wave polarizations, as above. A rigid grid with a *tensor* (directional) workload built from app 4-momenta is a potential candidate. The remaining problem is symmetry: a rigid hypercubic grid has preferred directions, while Lorentz symmetry has been tested to very high precision across the matter, photon and gravity sectors (compiled by Kostelecký and Russell, 2011; see also Sec. 7). The rule that maps workload to the effective metric must therefore wash out lattice anisotropy at observable scales, possibly through averaging or through the entanglement pattern (Routes A and B). The model has not yet shown that it does.

*Caveats. Routes A and B assume an area-law entanglement that the ledger has not derived (open problem 14), and Route B is established only in AdS/CFT. CDT results are numerical and remain under active study, and CDT varies connectivity, whereas the ledger keeps nodes rigid; it is used here only as mathematical machinery. This subsection identifies candidate paths; it does not derive GR.*

#### Worked example: solar light deflection from summed node workloads (Hypothesis)

This example applies the optical-metric picture above to the Sun, keeping the bookkeeping in Planck units.

**Planck-unit bookkeeping.**

- The key identity is $GM/(rc^2) = (M/m_P)(l_P/r)$: the weak-field potential in units of $c^2$ equals the mass in Planck masses times the inverse distance in Planck lengths.
- For the Sun, $M_\odot \approx 9.14\times10^{37}\,m_P$ and $R_\odot \approx 4.30\times10^{43}\,l_P$. Its volume contains about $3.3\times10^{131}$ Planck-scale nodes.
- The mean workload is therefore about $2.7\times10^{-94}\,m_P$ per node. Each node's share is extremely small, and the measurable effect arises only from the sum.

**Simulation.**

- *Model.* The effective index is $n(\mathbf{x}) = 1 + 2\sum_i (m_i/m_P)(l_P/|\mathbf{x}-\mathbf{x}_i|)$, the isotropic weak-field optical metric.
- *Coarse-graining.* $3\times10^{131}$ nodes cannot be simulated, so the Sun was coarse-grained into $N$ equal-volume cubic cells. Cell masses follow an $n=3$ polytrope (Eddington's standard model; Eddington, 1926; Chandrasekhar, 1939) and sum to $M_\odot$.
- *Deflection.* For a ray grazing the limb ($b = R_\odot$), the deflection was computed by summing each cell's contribution along a straight line (Born approximation).
- *Cross-checks ($N \approx 10^3$).* Numerical quadrature along the line gave 1.751258 arcsec, and full integration of the bent ray gave 1.751263 arcsec. The Born sum gave 1.751257 arcsec.

| Cells $N$ | Deflection (arcsec) | Without factor 2 (arcsec) |
|---|---|---|
| 1,003 | 1.751257 | 0.875629 |
| 9,978 | 1.751243 | 0.875622 |
| 100,026 | 1.7512433 | 0.8756216 |
| 999,954 | 1.7512433 | 0.8756216 |
| GR, $4GM/(bc^2)$ | 1.7512433 | 0.8756 ($2GM/(bc^2)$) |

: Limb deflection from summed cell workloads.

**Results.**

- *Convergence.* The summed deflection converges to $4GM_\odot/(R_\odot c^2) = 1.751$ arcsec. The relative difference is about $10^{-9}$ at $N \approx 10^6$. Convergence is rapid because the cubic grid is nearly spherically symmetric; randomly placed cells would converge more slowly.
- *Same mass, smaller volume.* Compressing the same mass into $0.5\,R_\odot$ or $0.1\,R_\odot$ leaves the deflection at $b = R_\odot$ unchanged (1.751243 arcsec in all three cases).
- *Distance dependence.* For $b \ge R_\odot$ the deflection falls as $1/b$ (Figure \ref{fig:sun}).
- These results are expected by construction. Outside a spherically symmetric mass, only the total enclosed mass enters: this is the shell theorem, and in GR, Birkhoff's theorem. The example therefore checks the bookkeeping, not new physics.

\begin{figure}[tp]
\centering
\includegraphics[width=\linewidth]{sun_bend.png}
\caption{Solar light deflection from summed cell workloads, using $n = 1 + 2\sum_i (m_i/m_P)(l_P/|\mathbf{x}-\mathbf{x}_i|)$ with an $n=3$ polytrope density profile. (a) Deflection of a ray grazing the limb ($b = R_\odot$) versus the number of cells $N$, with the factor 2 (circles) and with the Newtonian part only (squares). Dashed and dotted lines mark $4GM/(bc^2) = 1.751$ arcsec and half that value. Inset: relative difference from $4GM/(bc^2)$. (b) Deflection versus $b/R_\odot$ for the same total mass contained within $1.0$, $0.5$ and $0.1\,R_\odot$ ($N \approx 10^5$), compared with $4GM/(bc^2)$.}
\label{fig:sun}
\end{figure}

**The factor of two.**

- *Half from the time part.* Without the factor 2, the sum gives 0.875 arcsec. This is the value obtained from Newtonian gravity by Soldner (1801) and from the equivalence principle by Einstein (1911); it corresponds to the time (clock-rate) part of the metric alone.
- *Full value.* The full 1.75 arcsec requires equal contributions from the time part and the space part of the metric, as in linearized GR. The 1919 eclipse expeditions framed this choice explicitly: about 0.87 arcsec for the Newtonian law versus 1.75 arcsec for Einstein's theory. Their results favoured the larger value (Dyson, Eddington & Davidson, 1920).
- *Why a scalar coupling fails.* The electromagnetic stress-energy tensor is traceless. A theory in which gravity couples only to the trace of $T^{\mu\nu}$, as in Nordström's scalar theory, therefore gives no light deflection (Norton, 1992).
- *What the model would need.* Equal space and time contributions follow if nodes carry the full ten-component workload tensor (Sec. 6.14) and couple tensor to tensor.

*Caveat. In this simulation the factor 2 in $n$ was inserted from linearized GR; it was not derived. The model's position is that the full-tensor workload, already part of its design, would supply the factor. Demonstrating this from an explicit node update rule remains open (open problem 20).*

*Independent check (Hypothesis).* A separate 2D ray and wave toy with load-dependent link timing gives deflection proportional to $1/b$: clock slowdown alone yields the Newtonian 0.875 arcsec, while clock slowdown plus an equal extra routing cost per hop yields 1.751 arcsec and the GR Shapiro delay (247 µs vs 124 µs for an Earth–Mars round trip). This is consistent with rigid nodes, where the extra cost is routing cost rather than stretching; *why the two contributions are equal is addressed, conditionally, below.*

*Why clock slowdown equals routing cost (Hypothesis).* We postulate a local server-side ledger balance at every patch boundary: the load crossing the boundary equals the change in the boundary's state count times the local tick rate. This is a node-level reading of Jacobson's derivation of the Einstein equation from $\delta Q = T\,dS$ on local horizons (Jacobson, 1995), treated as bookkeeping rather than client-side thermodynamics. Required in every direction at once, the balance forces the link cost $\Psi$ to equal the clock slowdown $\Phi$, since the direction-dependent term $\partial_n\partial_n(\Phi-\Psi)$ must vanish. A $28^3$ toy imposing the balance along 13 lattice directions gives $\Psi/\Phi = 1.0000000$, the Newtonian limit exactly, and light bending of exactly twice the clock-only value; imposing it in only one direction leaves $\Psi/\Phi$ undetermined ($\approx 0.41$ in the solver's choice). Jacobson's free constant $\Lambda$ fits the per-node fee of Sec. 6.10. The boundary state count is taken from the ground-state entanglement of node fields (Bombelli et al., 1986; Srednicki, 1993), with each link counted at half length; small-cluster toys give $G = 1$ for roughly 4 massless scalar types on the 6-link cubic grid, or about 7 on the 8-link body-centred cubic grid (about 3 per Planck area), so $G$ is set by the field count rather than by a hand-set per-link state count. *Caveat: weak static fields only; the isotropy of the balance, the temperature mapping, the half-length link counting and the field count (which together set $G$) are postulated; the steady state was found with a global solver rather than the local update loop; this reproduces known GR results in node language.*

*Light bending as a sum over paths (Hypothesis).* Light's amplitude covers every path through the nodes, each hop adding phase $k(1+|\Phi|+|\Psi|)$. Paths away from the classical bend cancel; those near it add up, and the stationary points are the two lensed images at the $2\times$ bend radius. In a wave toy with $\Psi = \Phi$, the far-field peak lies at 95 mrad against 48.8 mrad for clock-only phase, a ratio of 1.95, about $2\times$; the roughly 5% shortfall comes from the finite beam width. Two features exist only in the wave picture: a finite on-axis focus ($75\times$ the unlensed intensity) with rings, where rays give an infinite caustic, and an angular spread that shrinks with wavelength toward the ray limit. Detection follows the Born rule: about 78% of single-beam photons land within $\pm20\%$ of the $2\times$ bend, against about 0.2% near the clock-only angle, and the pattern builds up over about $10^3$–$10^5$ photons. *Caveat: this is standard wave optics in a weak gravitational field (Nakamura & Deguchi, 1999), in the thin-screen, small-angle limit, without polarization, with the Born rule assumed; the ledger adds only the reading of phase as clock plus link cost.*

![Wave toy of light bending with phase per hop set by clock plus link cost: the far-field peak lies near twice the clock-only angle, a plane wave forms a finite on-axis focus with rings, and Born-rule photon hits build up the pattern.](wave_lensing.png){width=80%}

#### Worked example: Mercury's perihelion advance from summed node workloads (Hypothesis)

This example applies the same node-summed solar field to Mercury's orbit ($a = 0.387098$ AU, $e = 0.205630$, period 87.9691 days, about 415.2 orbits per century).

**Planck-unit ratio and external field.**

- The relevant ratio is $GM_\odot/(ac^2) = (M_\odot/m_P)(l_P/a) = 9.1364\times10^{37} / 3.5829\times10^{45} \approx 2.550\times10^{-8}$.
- *Point-mass check.* The polytrope cells of the previous example (100,026 cells) were reused. At Mercury's closest, mean and farthest distances (20 directions each), the summed field equals that of a point mass to within $3.9\times10^{-12}$ (relative). The orbit can therefore be computed with a point-mass Sun, as the shell theorem predicts.

**Method.**

- *Equations of motion.* The orbit was integrated with the Newtonian acceleration plus the first post-Newtonian (1PN) correction in the parametrized post-Newtonian (PPN) form (Will, 2014). In this form, $\gamma$ measures how much space is curved per unit mass, and $\beta$ measures the nonlinearity of the field, i.e. how strongly the field's own energy contributes. General relativity has $\gamma = \beta = 1$. The predicted advance scales as $(2+2\gamma-\beta)/3$ times the GR value.
- *Integrator.* An eighth-order Runge–Kutta integrator (DOP853, relative tolerance $10^{-13}$) was run for 200 orbits (about 48 years). The advance was taken from a linear fit to the direction of the Runge–Lenz vector, which points to perihelion.
- *Energy checks.* In the Newtonian runs, energy is conserved to $2\times10^{-11}$. In the 1PN runs, the Newtonian energy oscillates within each orbit by up to $1.6\times10^{-7}$, of the order of $GM_\odot/(ac^2)$, as expected for the correction terms. No secular drift is apparent.

| Case | $\gamma$ | $\beta$ | Factor | Sim. | Analytic |
|---|---|---|---|---|---|
| Newtonian only | – | – | 0 | +0.0001 | 0 |
| GR-like | 1 | 1 | 1 | +42.984 | 42.982 |
| Time only | 0 | 1 | 1/3 | +14.329 | 14.327 |
| Nordström-like | $-1$ | 1/2 | $-1/6$ | $-7.164$ | $-7.164$ |
| No self-loading | 1 | 0 | 4/3 | +57.310 | 57.309 |
| GR-like + $J_2$ | 1 | 1 | – | +43.012 | 42.982 + 0.028 |

: Mercury's perihelion advance in arcsec per century ($''$/cy) for different post-Newtonian parameters; Factor $=(2+2\gamma-\beta)/3$; $J_2 = 2.2\times10^{-7}$ (Nordström-like values from Will, 2014).

**Observational budget.** Clemence (1947) gives the following values (arcsec per century):

- Observed total perihelion motion: 5599.74.
- General precession of the equinoxes: 5025.645.
- Newtonian perturbations by the other planets: 531.54 in total. The largest contributions are Venus (277.856), Jupiter (153.584) and Earth (90.038).
- Residual: 42.56 ± 0.94, compared with the relativistic prediction of 43.03 ± 0.03.
- The Newtonian pure-Sun run reproduces the first part of the classical problem: it gives no advance, so the residual is left unexplained.

\begin{figure}[tp]
\centering
\includegraphics[width=\linewidth]{mercury.png}
\caption{Mercury's perihelion advance with the node-summed solar field. (a) Change of the Runge--Lenz (perihelion) direction versus time over 200 orbits for the Newtonian, GR-like, time-only, Nordström-like and no-self-loading cases. (b) Simulated advance versus the PPN factor $(2+2\gamma-\beta)/3$; the dashed line is $42.98 \times (2+2\gamma-\beta)/3$ arcsec per century.}
\label{fig:mercury}
\end{figure}

**Interpretation.**

- *Light bending tests one parameter.* Light deflection is proportional to $(1+\gamma)/2$, so it tests only $\gamma$, the space part of the workload.
- *Mercury tests two.* The perihelion advance additionally depends on $\beta$, so it also probes the nonlinear part of the field.
- *Node-workload reading.* In the node picture, the full ten-component tensor is a natural description of a three-dimensional node's workload: an energy part, momentum parts, and stress parts. The space components of this tensor correspond to $\gamma = 1$. Mercury adds a second requirement, $\beta = 1$, which corresponds to self-loading: the workload associated with the gravitational field itself also loads nodes. In conventional terms, gravity gravitates.
- *Sensitivity.* A time-only workload (14.3 arcsec/century), a workload without self-loading (57.3), or a Nordström-like scalar workload ($-7.2$, a retrograde shift) would each disagree with the observed residual.
- *Solar flattening.* The solar quadrupole ($J_2 \approx 2.2\times10^{-7}$) contributes only about 0.03 arcsec per century.

*Caveat. Here $\gamma$ and $\beta$ were borrowed from the PPN/GR equations and inserted; they were not derived from a node rule. The agreement with 43 arcsec per century therefore shows only that the node-summed field reproduces the Sun's external field; the model must still produce $\gamma = 1$ and $\beta = 1$ from its own update rule (open problem 21).*

### 6.15 Hiding the Server Rest Frame: Two Toy Simulations (Hypothesis)

**Framing.** In the rigid-node picture (Sec. 6.14), the grid defines a rest frame, but that frame resides on the server side; client-side updates propagate at most at $c$. This is close to a Lorentz–Poincaré-type view, as presented by Bell (1976, reprinted 1987): physical laws are written in one frame, and if those laws are Lorentz invariant, observers in uniform motion are unable to detect their motion, so experiments cannot determine which frame is "really" at rest. In ledger terms, a preferred server frame may exist yet remain undetectable, provided all client dynamics are frame-independent at large scales. Whether a rigid grid of nodes permits this is a quantitative question. As a first check, we ran two toy simulations using standard textbook update rules (Python/NumPy). They test whether patterns re-plotted on a fixed grid show a dependence on direction or speed.

**Test 1: wave dispersion on a 3D cubic lattice.** We solved the discrete wave equation (second-order leapfrog in time, nearest-neighbour Laplacian, lattice spacing $a$, $c = 1$) and compared the analytic group velocity with the measured speed of Gaussian wave packets travelling along the lattice directions [100] (axis), [110] (face diagonal) and [111] (body diagonal). The packets were planar (constant on lattice planes normal to the direction of travel), which are exact solutions of the 3D scheme. Results:

- Short waves travel slower than $c$, and the shortfall depends on direction. To leading order, $1 - v_g/c \approx \tfrac{1}{8}(ka)^2\,\big|\sum_i n_i^4 - \lambda^2\big|$, where $\mathbf{n}$ is the direction of travel ($\sum_i n_i^4 = 1, \tfrac12, \tfrac13$ for [100], [110], [111]) and $\lambda = c\,\Delta t/a$ is the Courant number. The ordering is therefore [100] slowest, then [110], then [111].
- The measured packet speeds agree with the analytic formula to about $1\times10^{-4}$ at every wavenumber tested (see the table below and Figure \ref{fig:test1}).
- The anisotropy between axis and body diagonal is $\approx (ka)^2/12$, independent of the timestep, and vanishes for long wavelengths ($ka \to 0$).
- Timestep notes: a timestep equal to the spacing ($\lambda = 1$) makes propagation exact only on a 1D chain. In 3D the scheme is unstable for $\lambda > 1/\sqrt{3}$; at $\lambda = 1/\sqrt{3}$ the leading error cancels along [111] but not along the axes. No single choice makes all directions exact.

| $ka$ | $v_g/c$ [100] | $v_g/c$ [110] | $v_g/c$ [111] |
|---|---|---|---|
| 0.25 | 0.9940 | 0.9980 | 0.9993 |
| 1.0 | 0.9038 | 0.9676 | 0.9891 |
| 2.0 | 0.5955 | 0.8559 | 0.9508 |

: Measured wave-packet group velocities on the cubic lattice ($\lambda = 0.5$).

*Extrapolation to Planck spacing.* Setting $a = l_P$, so that $ka = E/E_P$ with $E_P \approx 1.22\times10^{19}$ GeV, and taking the timestep to zero, the fractional speed shortfall is $\tfrac18 (E/E_P)^2 \sum_i n_i^4$:

| Photon energy | $1 - v_g/c$ |
|---|---|
| 1 GeV | $8.4\times10^{-40}$ ([100]) to $2.8\times10^{-40}$ ([111]) |
| 30 GeV | $7.6\times10^{-37}$ ([100]) |
| 31 GeV (highest GRB 090510 photon) | $8.1\times10^{-37}$ ([100]) |
| 1 TeV | $8.4\times10^{-34}$ ([100]) |

: Lattice-induced photon speed shortfall for $a = l_P$.

Observations of GRB 090510, with photons up to about 31 GeV, found no evidence of Lorentz-invariance violation and set a lower limit of $1.2\,E_P$ on the scale of a *linear* energy dependence of the speed of light (Abdo et al., 2009). This lattice rule produces no linear term; its leading effect is quadratic. For quadratic dispersion, Vasileiou et al. (2013) report $E_{\text{QG},2} > 1.3\times10^{11}$ GeV (95% C.L., subluminal) from the same burst. In their convention ($\delta v/c = \tfrac32 (E/E_{\text{QG},2})^2$), the lattice corresponds to $E_{\text{QG},2} \approx 4.2$–$7.3\times10^{19}$ GeV, depending on direction. At 31 GeV the lattice effect is about $10^{17}$ times below the current bound.

\begin{figure}[tp]
\centering
\includegraphics[width=\linewidth]{replot_anisotropy.png}
\caption{Test 1: leapfrog wave equation on a 3D cubic lattice ($c = 1$, spacing $a$). (a) Analytic group velocity versus $ka$ for directions [100], [110], [111] at Courant number $\lambda = 0.5$ (lines), with measured speeds of planar Gaussian wave packets (dots). (b) Deviation $|1 - v_g/c|$ on log axes; dashed lines show the leading-order form $(ka)^2/8\,|\sum_i n_i^4 - \lambda^2|$. (c) Axis-versus-body-diagonal speed difference for $\lambda = 0.01, 0.5, 1/\sqrt{3}$, scaling as $(ka)^2$ and vanishing as $ka \to 0$.}
\label{fig:test1}
\end{figure}

\begin{figure}[tp]
\centering
\includegraphics[width=\linewidth]{replot_kink.png}
\caption{Test 2: discrete sine-Gordon (Frenkel–Kontorova) kinks launched at $v = 0$–$0.95c$ on 1D lattices of spacing $a = 0.05, 0.5, 1.0, 1.5$ (rest width 1, rest mass 8). (a) Measured kink width versus $\gamma$, compared with Lorentz contraction $1/\gamma$. (b) Energy divided by $\gamma m$. (c) Deviation of width$\,\times\gamma$ from 1 versus $a\gamma$ (spacing relative to the contracted width), growing steeply as the width approaches the spacing.}
\label{fig:test2}
\end{figure}

**Test 2: a moving kink on a 1D lattice.** We used the discrete sine-Gordon (Frenkel–Kontorova) chain, $\ddot\phi_j = (\phi_{j+1} - 2\phi_j + \phi_{j-1})/a^2 - \sin\phi_j$, whose continuum limit is Lorentz invariant and supports kinks: localized patterns of rest width 1 and rest energy (mass) $m = 8$ in these units. Kinks were launched from the boosted continuum profile at $v = 0, 0.3, 0.6, 0.8, 0.9, 0.95\,c$ on lattices with $a = 0.05, 0.5, 1.0, 1.5$, and the width (from a fit to the kink profile), energy and speed were measured. Discreteness is known to produce a periodic Peierls–Nabarro potential acting on the kink (reviewed by Braun and Kivshar, 1998).

| $a$ | $v$ | width $\times\gamma$ | $E/(\gamma m)$ | measured speed |
|---|---|---|---|---|
| 0.05 | 0 to 0.95 | 0.9999–1.0012 | 0.9996–1.0000 | 0.9489 (launched at 0.95) |
| 0.5 | 0.6 | 0.988 | 0.995 | 0.588 |
| 0.5 | 0.95 | 1.72 | 0.988 | 0.80 (slowed) |
| 1.0 | 0.95 | 2.45 | 1.16 | 0.51 |
| 1.5 | 0.95 | 2.8 | 0.57 | 0.08 (nearly pinned) |

: Kink width (1 = exact Lorentz contraction), energy and speed on lattices of spacing $a$.

- *Width much larger than $a$.* On the fine lattice the re-plotted kink contracts by exactly $1/\gamma$ and its energy equals $\gamma m$ to within 0.04%, up to $0.95c$. Relativistic behaviour emerges from re-plotting on fixed nodes.
- *Width approaching $a$.* Once the contracted width approaches the spacing, deviations grow steeply (Figure \ref{fig:test2}c). The kink radiates lattice waves, slows down (from 0.95 to about 0.80 at $a = 0.5$) and fits a broadened profile. At $a = 1.5$ it is nearly pinned to the lattice, a Peierls–Nabarro effect.
- Total energy was conserved to better than $3\times10^{-4}$ in all runs. Fitted widths on the coarsest lattices are rough, because only a few lattice points span the kink.

**Conclusion.** For these update rules, the grid's rest frame is unobservable to within the stated precision for patterns much larger than a node: direction dependence and departures from Lorentz contraction both fall off as (pattern size / spacing)$^{-2}$. This yields a new constraint for the model: physical particles must be much larger than one node. A proton, with charge radius of about 0.84 fm, spans of order $10^{20}$ Planck lengths, so in this picture it is a very large pattern.

**Hidden path, hidden frame.** Between recorded events, standard quantum mechanics assigns no definite trajectory. In Feynman's path-integral formulation, the amplitude for an event is a sum of contributions from all paths, each weighted by a phase equal to the classical action in units of $\hbar$ (Feynman, 1948), and only recorded events are client-visible. In this model, the intermediate path and the grid rest frame would both reside server-side. Hidden, however, is not the same as zero. For patterns much larger than a node, the grid effects in Sec. 6.15 scale roughly as (pattern size / spacing)$^{-2}$. For accessible particles this is below about $10^{-30}$: a proton spans about $5\times10^{19}$ Planck lengths, and an electron, at the collider bound on its size of roughly $10^{-18}$ m, spans about $10^{17}$. A residual quadratic-in-energy term could in principle appear for the highest-energy photons and electrons. Synchrotron radiation of about 100 MeV from the Crab Nebula constrains electron dispersion: Jacobson, Liberati & Mattingly (2003) rule out a subluminal cubic-order correction to the electron dispersion relation (a speed shift linear in energy) of Planck-scale size, placing it at least about $10^{7}$ times beyond the Planck scale. This is consistent with the update rule tested here, which has no linear term. A dedicated bound on quadratic electron dispersion would be a possible future test.

**No holographic jitter.** Some proposals for Planck-scale geometry predict a random, correlated jitter of macroscopic positions. Hogan (2012) proposed a "holographic noise" of transverse position, arising from non-commuting position operators in different directions, which would appear in a Michelson interferometer as a random Planckian walk of the beam splitter. The Fermilab Holometer, two co-located 39 m interferometers cross-correlated up to MHz frequencies, searched for this signal (Chou et al., 2016). Its final first-generation analysis found no correlated shear noise and constrained the model parameters below the level predicted by the Planck-scale holographic bound (Chou et al., 2017). A later configuration with bent arms found no rotational correlations either (Richardson et al., 2021).

In the present model the nodes are rigid and do not fluctuate in position, and replotting of patterns on the server grid is deterministic. The only grid effects on a large pattern are the suppressed corrections found in the two toy simulations above, which fall as the inverse square of the pattern size measured in node spacings: about $10^{-30}$ for a pattern of $10^{-20}$ m and far smaller for macroscopic mirrors. No measurable interferometer noise of Holometer type is therefore predicted.

*Caveat. This conclusion depends on the node rule being deterministic and the node positions being fixed. If node updates had stochastic components, Holometer-type bounds would apply to them directly.*

**Test 3: a Dirac walker on the BCC grid (Hypothesis, toy-tested).** We used the D'Ariano–Perinotti BCC Dirac automaton. A single-handed step leaves a linear, direction-odd term in the dispersion ($\xi_1 = \pm 0.19$, so $E_{QG,1} \approx 2.6\,E_P$), which fails the GRB bounds by about 3×. Alternating the two handednesses each tick (a four-component left plus right rule) cancels the linear term exactly in every direction. The leading deviation is then quadratic and subluminal ($|\xi_2| \le 0.23$, so $E_{QG,2} \gtrsim 1.8\times10^{19}$ GeV), about $10^8$ times above current quadratic bounds. A Wilson layer that removes the doubler modes keeps this cancellation. Moving-clock tests at $v = 0$–$0.8c$ along five directions show a direction-dependent deviation that falls as $(m a)^2$, the same order as the scalar test. Once the limiting speed is matched per mass, no residual floor remains. *Caveat: the limiting speed of a massive walker exceeds that of the massless one by $\Delta c/c \approx +0.043\, mc^2/E_P$. This shift is isotropic and vanishes as $m \to 0$, but it gives each species its own limiting speed: about $10^{-24}$ for the electron and $3\times10^{-21}$ for the proton. The proton value has not yet been checked against ultra-high-energy cosmic-ray limits.*

**The radiative-correction challenge.** The suppression estimates above treat particles as classical patterns. In quantum field theory, virtual-particle loops sample momenta up to the cutoff, here the grid scale. Collins, Perez, Sudarsky, Urrutia & Vucetich (2004) argued that, when known particle interactions are combined with a Planck-scale preferred frame, such loops generically produce Lorentz violation at low energies with no suppression by powers of $E/E_P$. The result would be different limiting speeds for different fields, with fractional differences of roughly 0.1% to 10%, unless the bare parameters are unnaturally finely tuned. Differences of this size are far above the limits compiled from precision tests (Kostelecký & Russell, 2011). Known mitigations exist. One is a protecting symmetry: Groot Nibbelink & Pospelov (2005) showed that in the supersymmetric Standard Model, Lorentz-violating operators start at dimension five, so they are suppressed by at least one power of the ultraviolet scale and are stable against radiative corrections. Another is an update rule whose structure prevents loop amplification of grid anisotropy. Whether the ledger's node rule has such a property is unknown. The toy simulations in this section are classical and do not address loops. This is likely the most serious challenge to the hidden-frame hypothesis.

*Caveats. Both simulations use a single scalar field; Test 2 is a 1D toy model. Neither involves photons as vector fields, gravity, or the ledger's actual node update rule, and the prefactors depend on the rule chosen. Other update rules (higher-order, random or entanglement-based) could give different prefactors, and some could produce a linear-in-energy term, which the GRB 090510 bound already excludes near $E_P$. A preferred frame still exists in principle; these results show only that, for these rules, its effects are suppressed for large patterns. Patterns near Planck size would behave like the coarse-lattice kinks and be distorted, slowed or pinned.*

### 6.16 Black Holes Without Singularities (Hypothesis)

This subsection develops the "No singularities" remark made earlier in Sec. 6 into a potential candidate picture of black-hole interiors. It does not follow from the node rules; it states what the ledger would have to reproduce and where it could differ from GR.

**Exterior: unchanged.** Far from the core, curvature is small compared with $1/l_P^2$, and the network is assumed to reduce to GR (Sec. 6.14). Horizons then form as in GR, and exterior observables are unchanged: the shadow images of the Event Horizon Telescope and the ringdown signals measured by LIGO/Virgo probe regions where any Planck-scale correction is expected to be negligible.

**Interior: a finite core.** With a minimum node size $l_P$, the effective deficit angle on a hinge of area $\sim l_P^2$ cannot exceed $2\pi$, so curvature is bounded at roughly $1/l_P^2$, and the energy density is bounded at roughly the Planck density ($\rho_P = c^5/(\hbar G^2) \approx 5\times10^{96}\ \text{kg m}^{-3}$). The central singularity of classical GR is therefore a candidate to be replaced by a finite, maximally loaded core. This is consistent with the information cap of Sec. 6.13: the horizon area still bounds the information the interior can hold, $S \le A/(4 l_P^2)$, whatever the core structure.

**Precedents.** Several approaches report non-singular behaviour of this kind:

- *Loop quantum cosmology.* Ashtekar, Pawlowski and Singh (2006) found, for homogeneous isotropic models with a scalar field, that the big-bang singularity is replaced by a "big bounce", with deterministic quantum evolution across the Planck regime. This concerns cosmology, not black holes, but it is the clearest precedent for discreteness removing a singularity.
- *Regular black holes.* Bardeen (1968) presented a modification of the Schwarzschild metric with a regular centre, often cited as the first regular black-hole metric. Hayward (2006) gave regular space-times describing the formation of a black hole from vacuum, a static Bardeen-like region with finite density that behaves as a cosmological constant at small radius, and evaporation back to vacuum.
- *Planck stars.* Rovelli and Vidotto (2014) proposed that quantum-gravitational pressure halts collapse at Planck-scale energy density and produces a bounce that is very short in the star's proper time but very long as seen from outside, because of gravitational time dilation.

**Possible tests.** Abedi, Dykaar and Afshordi (2017) searched public LIGO data for repeating, damped "echoes" after black-hole mergers, which Planck-scale structure near horizons could produce, and reported tentative evidence at about $2.5\sigma$. Later searches, including the LIGO–Virgo–KAGRA tests of GR with the GWTC-3 catalogue (Abbott et al., 2021/2025), found no significant evidence for echoes. Delayed-bounce or Planck-star signals remain speculative. Note that echoes probe near-horizon structure; a ledger core deep inside the horizon need not produce them at all.

*Caveats. The finite core is not derived from the model's node rules; it is assumed from the existence of a minimum node size. Regular-core models face their own problems: Carballo-Rubio et al. (2018) showed that generic regular black holes with a non-zero inner-horizon surface gravity suffer a mass-inflation instability at the inner horizon, so a ledger core would have to avoid or resolve this. There is no experimental evidence for non-singular black-hole interiors at present.*

### 6.17 Node Saturation: Finite Curvature Where GR Diverges (Hypothesis)

This subsection turns the finite-core remark of Sec. 6.16 into a rough numerical estimate. The rule used is a *placeholder*, chosen as the simplest way to express a working cap of about one Planck mass of workload per node; it is not derived from the node update rules.

**Cap rule used.** A mass $M$ compressed to radius $R$ is spread over about $(4\pi/3)(R/l_P)^3$ nodes. If no node carries more than about $m_P$, the mass cannot occupy fewer than $M/m_P$ nodes, so it cannot be packed below
$$R_{\min} = l_P\left(\frac{3M}{4\pi m_P}\right)^{1/3}.$$
In the toy, the GR formulas are evaluated at an effective radius $R_{\text{eff}} = (R^3 + R_{\min}^3)^{1/3}$, which equals $R$ when the load per node is small and levels off at $R_{\min}$ when the nodes saturate. The curvature measure is the Kretschmann scalar at the surface, $K = 48G^2M^2/(c^4 R^6)$, which in GR grows without limit as $R \to 0$.

**Hidden-frame heuristic: a per-node energy budget.** The rule above counts only rest mass. A more general but frame-dependent placeholder caps the total energy carried by one node:
$$\sqrt{(mc^2)^2 + (pc)^2} \;\le\; m_P c^2 = E_P \approx 1.956\times10^{9}\ \text{J} \;(\approx 1.22\times10^{28}\ \text{eV}).$$
At rest the whole budget is rest mass, $m \le m_P \approx 21.8\ \mu\text{g}$, which is the $R_{\min}$ rule above. For a massless app the whole budget is momentum, $p \le p_P = m_P c \approx 6.52\ \text{kg m s}^{-1}$. Since $v = pc^2/E \le c$, with equality only for $m = 0$, only massless apps reach $c$; in plain terms, each tick's update is shared between rest mass and forward motion, and the forward share tops out at one node per tick (Sec. 6.1).

Within this heuristic, a consequence that differs from GR and special relativity: there, the energy of a massive body grows without bound as $v \to c$. Under the budget, a massive app has a finite maximum Lorentz factor $\gamma_{\max} = E_P/(mc^2)$. For an electron, $\gamma_{\max} \approx 2.39\times10^{22}$ and $1 - v_{\max}/c \approx 1/(2\gamma_{\max}^2) \approx 8.8\times10^{-46}$; for a proton, $\gamma_{\max} \approx 1.30\times10^{19}$ and $1 - v_{\max}/c \approx 3.0\times10^{-39}$. This is the Finiteness Principle (Sec. 6) applied to kinetic energy: no app carries infinite energy in the server frame. As noted below, this per-particle limit does not survive in the frame-independent form.

*Caveats. As written, the energy cap holds in the hidden server frame. Energy is frame-dependent, so a boosted observer would see a different value; the recommended form below caps a frame-independent quantity instead, so that the server frame stays hidden (Sec. 6.15). The highest-energy cosmic ray observed, the Fly's Eye "Oh-My-God" event of 1991 at $(3.2\pm0.9)\times10^{20}$ eV, about 51 J (Bird et al., 1995), is about $3\times10^{-8}$ of $E_P$, so there is no conflict with observation. Nodes stay fixed and do not jitter; the budget limits load, not node position.*

**Recommended form: a frame-independent limiting curvature (Hypothesis).** Both rules above refer to one frame. A potential candidate that every observer agrees on is a bound on curvature invariants built from the full tensor, the Kretschmann scalar $R_{abcd}R^{abcd}$ and the Ricci invariants $R^2$ and $R_{\mu\nu}R^{\mu\nu}$, each of order $1/l_P^4$ per node (the toy above gives $K_{\max} \approx 842/l_P^4$). This is a discrete counterpart of Markov's limiting density (1982) and of the limiting-curvature hypothesis developed by Frolov, Markov and Mukhanov (1989), Mukhanov and Brandenberger (1992) and Brandenberger (1995). Through Einstein's equations, the Ricci part bounds the local workload tensor, giving a rest-frame density of at most about $\rho_P$ and a collision energy $\sqrt{s}$ of at most about $E_P$ per node; the Weyl (tidal) part is bounded through the Kretschmann scalar. The rest-mass rule is kept as the toy that sets the numbers, and the energy budget as a hidden-frame heuristic.

- *Why curvature, not energy or density.* A black-hole interior is vacuum: the workload tensor vanishes there, and only tidal (Weyl) curvature grows toward the centre. Caps on the trace, on $T_{\mu\nu}T^{\mu\nu}$, or on rest-frame density are zero inside the horizon and cannot remove the singularity. Only a curvature cap reaches it, so the finite core above rests on this form.
- *The lone photon.* A single light pulse can carry arbitrarily high energy in some frame, but that is a Doppler shift of the observer, not a property of the pulse; its trace, $T_{\mu\nu}T^{\mu\nu}$ and invariant mass are all zero, and it produces no invariant curvature by itself. Nothing is capped. Two interacting pulses have invariant mass $\sqrt{s}$, which all observers agree on, and that is capped at about $E_P$. For comparison, the LHC reaches $\sqrt{s} = 13.6$ TeV, about $10^{-15}\,E_P$.
- *Checks.* At the solar surface $K/K_{\max} \approx 7\times10^{-188}$, at Mercury's orbit $\approx 2\times10^{-199}$, and the Sun's central density is $\approx 3\times10^{-92}\,\rho_P$; the Sun-bending and Mercury examples are unchanged. The saturated core (about $\rho_P$, $K_{\max} \sim 10^{142}\ \text{m}^{-4}$) is unchanged.

*Caveats. The cap is postulated, not derived from the node update rule. All scalar curvature invariants vanish for plane gravitational waves, so a complete rule may need non-scalar conditions. The value $K_{\max}$ and the minimum horizon mass of about $0.17\,m_P$ come from the placeholder toy. An invariant cap does not limit the speed of a single particle (Sec. 6.1). The fate of a saturated core, including bounce or white-hole outcomes, is left open. Nodes stay fixed and do not jitter.*

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{node_cap.png}
\caption{Node-saturation toy. (a) Kretschmann scalar at the surface of a mass compressed to radius $r$ (in units of $l_P^{-4}$) for the Sun, 1 kg and one Planck mass. Dashed: GR, diverging as $r^{-6}$. Solid: placeholder node cap, levelling off at $\approx 842\,l_P^{-4}$ for every mass (dotted line). (b) Compactness $GM/(rc^2)$; the dotted line marks the horizon value $1/2$.}
\label{fig:nodecap}
\end{figure}

**Results.**

- *Maximum curvature.* With the cap, $K_{\max} = 48(4\pi/3)^2/l_P^4 \approx 842/l_P^4 \approx 1.2\times10^{142}\ \text{m}^{-4}$. It is the same for every mass, because the saturated density is always about the Planck density.
- *Saturated radius.* $R_{\min} \approx 0.62\,l_P$ for one Planck mass, $\approx 222\,l_P$ ($3.6\times10^{-33}$ m) for 1 kg, $\approx 4.5\times10^{-23}$ m for the Sun, $\approx 9.7\times10^{-23}$ m for 10 solar masses and $\approx 7\times10^{-21}$ m for Sgr A*. All are far inside the corresponding horizons (3 km for the Sun, about $1.3\times10^{10}$ m for Sgr A*).
- *GR is recovered where the load is small.* The fractional change in curvature is about twice the mean load per node. For the Sun as it is, the mean load is $\approx 3\times10^{-94}\,m_P$ per node, so the change is $\sim 10^{-93}$; the Sun-bending and Mercury worked examples of Sec. 6.14 are therefore unchanged.
- *Smallest black hole in this toy.* A horizon forms only if $R_{\min}$ lies inside $2GM/c^2$, which gives $M \gtrsim 0.17\,m_P \approx 4\times10^{-9}$ kg. Below this, the toy produces a saturated Planck-density object with no horizon. This sits at the same Planck-mass crossover noted in open problem 19.
- *Finite interior.* For every black hole above that mass, the toy replaces the central singularity with a saturated core of radius $R_{\min}$ and finite curvature, as in the regular-core models listed in Sec. 6.16.

In plain terms: GR's curvature formula divides by a radius that can go to zero. In the ledger picture the radius stops shrinking once every node is fully loaded, so the curvature stops rising. For anything less dense than the Planck density, which includes every star, planet and laboratory object, the two descriptions agree to far beyond any measurable precision.

The idea of a universal upper bound is not new. Markov (1982) proposed that the density of matter never exceeds a limiting value built from $c$, $G$ and $\hbar$ (of order the Planck density), with modified field equations that reduce to Einstein's at low density and give a de Sitter core at the limit; this was later developed into a limiting-curvature hypothesis. Rovelli and Vidotto (2014) argued that the onset of quantum-gravity effects in collapse is governed by energy density rather than size, so a "Planck star" core can be much larger than the Planck length, consistent with the $R_{\min} \propto M^{1/3}$ scaling found above (their $n = 1/3$ case).

**Spin–torsion as a possible ceiling (Interpretation).** In Einstein–Cartan (Einstein–Cartan–Sciama–Kibble) gravity, spin density sources torsion (Kibble, 1961; Sciama, 1964; Hehl et al., 1976). Torsion is fixed algebraically by the local spin density, so it vanishes outside matter and all vacuum tests of GR are unchanged. For Dirac matter it adds an effective axial four-fermion contact term that becomes important near the Cartan density $\rho_C \sim m^2c^4/(G\hbar^2)$, and the resulting spin–spin repulsion can halt collapse and replace the singularity with a bounce (Kopczyński, 1972; Trautman, 1973; Popławski, 2010). If nodes hold four-component Dirac amplitudes (Sec. 6.2; $4N_s$ components with an internal component chain), their axial spin current would add four torsion components to the node workload beyond the 10 of the symmetric tensor, so a term of this kind would arise from the node content rather than be added by hand.

*Caveat. For nucleons $\rho_C \sim 3\times10^{58}$ kg m$^{-3}$, about 39 orders of magnitude below the Planck density (about 45 for electrons). If spin–torsion repulsion is real, ordinary collapse would bounce long before the node cap is reached, and the ceiling would be particle-mass dependent rather than universal. The repulsive sign also depends on how spins are averaged and on non-minimal couplings. Einstein–Cartan therefore motivates a finite density but does not reproduce the Planck-scale cap, which remains a postulate.*

*Caveats. The cap rule is a hypothesis and a placeholder; a different saturation rule would change the numerical factors (842, 0.17 $m_P$) though probably not the existence of a ceiling. The toy uses static surface formulas, not a collapse calculation, and does not address the inner-horizon instability noted in Sec. 6.16, evaporation, or what happens to a saturated core over time; white-hole or bounce outcomes are left open. Saturated nodes are a statement about maximum load, not about node motion: nodes stay fixed and the network is not grainy or jittery at accessible scales. This regime is not lab-testable. Laboratory tests remain the gravity-mediated entanglement test (Sec. 7.4), small-source tests (Sec. 7.5) and the energy-squared grid effect (Sec. 7.1–7.3).*

### 6.18 Mercury's Perihelion from Clock Relay (Hypothesis)

In the ledger, a node's clock rate is relayed from neighbour to neighbour. If each hop *compounds* the slowdown (multiplies it) instead of adding to it, the time part of the metric comes out as $g_{00} = e^{-2U}$. Expanded to second order, that gives the post-Newtonian parameter $\beta = 1$; with $\gamma = 1$ from the space part, the perihelion advance, which scales as $(2 + 2\gamma - \beta)/3$, matches general relativity. In simulation, the compounding relay gave $\beta = 1.00$, $\gamma = 1.000$ and 42.91$''$ per century, against the observed $\approx 43''$. An additive relay gave $\beta = 0.5$ and 50.1$''$, so it is ruled out. Letting a node's own load also slow its clock double-counts the effect (46.3$''$).

*Caveat: In simulation, a strictly neighbour-relayed clock (no global time) yields compounding without it being imposed. $\beta$ converges to 1 as the hop size shrinks (0.9992 on the finest grid), with the remaining gap shrinking in proportion to hop size, while a global-clock control stays at $\beta = 0.5$. We hypothesize that the per-hop ratio comes from workload: a node busy with its share of the workload tensor relays fewer ticks per tick, and each neighbour counts them in its own slowed ticks, so that the slowdown relayed from neighbour to neighbour composes multiplicatively, giving $g_{00} \approx e^{-2U}$. Like a self-organizing map, each node adjusts only to its neighbours and a global clock gradient emerges with no central reference; unlike a SOM, it settles at once from the current workload rather than learning over many passes. That link length follows the local clock ($\gamma = 1$) is still assumed, not derived (open problem #21).*

## 7. Testable Predictions: Planck-Scale Discreteness

A framework that only restates quantum mechanics cannot be tested. The ledger's distinct physical claim is that spacetime is **discrete** at roughly the Planck scale ($\ell_{\text{Planck}} \approx 1.6 \times 10^{-35}$ m, $E_{\text{Planck}} \approx 1.22 \times 10^{19}$ GeV). That claim can, in principle, be tested.

### 7.1 Energy-Dependent Photon Dispersion

On a regular lattice, waves whose wavelength approaches the lattice spacing feel the grid: the dispersion relation deviates from $E = pc$. A generic first-order (linear) modification is

$$E^2 \approx p^2c^2\left(1 \pm \xi\, \frac{E}{E_{\text{Planck}}}\right) \quad\Rightarrow\quad v(E) \approx c\left(1 \pm \xi\, \frac{E}{E_{\text{Planck}}}\right)$$

with $\xi$ a dimensionless parameter of order one if the effect is set by the Planck scale. Two photons emitted together at distance $D$ with energy difference $\Delta E$ would then arrive separated by

$$\Delta t \approx \xi\, \frac{\Delta E}{E_{\text{Planck}}}\,\frac{D}{c}$$

(with corrections for cosmological expansion at large redshift). Over cosmological distances this tiny effect adds up, so gamma-ray bursts (GRBs) with sharp, high-energy light curves are sensitive probes. Equivalently, one writes $E_{\text{QG},1} = E_{\text{Planck}}/\xi$ and bounds $E_{\text{QG},1}$ from below.

### 7.2 Existing Constraints

Observations already constrain linear dispersion strongly:

- **Fermi GRB 090510.** The Fermi LAT/GBM collaborations detected emission up to about 31 GeV from this short burst and found no evidence of Lorentz-invariance violation. They placed a lower limit of $E_{\text{QG},1} > 1.2\,E_{\text{Planck}}$ on a linear energy dependence, under reasonable assumptions about emission times, and reported $|\Delta t/\Delta E| < 30$ ms/GeV at 99% confidence (Abdo et al., *Nature* 462, 331, 2009).
- **LHAASO GRB 221009A.** Using TeV photons from the brightest GRB ever recorded, the LHAASO collaboration set 95% confidence limits of $E_{\text{QG},1} > 1.0 \times 10^{20}$ GeV (subluminal) and $> 1.1 \times 10^{20}$ GeV (superluminal), roughly ten times the Planck energy (Cao et al., *Phys. Rev. Lett.* 133, 071501, 2024).

**Implication for the Space-Ledger.** A naive regular Planck-scale grid with an order-one linear dispersion coefficient ($\xi \sim 1$) is already **disfavored**: the data require $\xi \lesssim 0.1$. A viable ledger must therefore either (a) suppress the linear term, so the leading effect is quadratic, $\propto (E/E_{\text{Planck}})^2$, which is much less constrained, or (b), as a fallback, arrange its nodes so that discreteness does not single out a preferred frame at all (Sec. 7.3). Either way, the framework makes a concrete commitment that future GRB, blazar, and neutrino timing data can test further.

### 7.3 Keeping Approximate Lorentz Invariance on a Discrete Network

A regular cubic grid picks out a preferred rest frame and preferred directions, which is why it tends to predict Lorentz violation. Discreteness does not have to work this way. In causal set theory, spacetime points are scattered *randomly* (via a Poisson process) with a density of about one per Planck volume, and the only structure is the causal order between them. Bombelli, Henson and Sorkin (*Mod. Phys. Lett. A* 24, 2579, 2009) argued that such a random discrete structure need not pick out a preferred frame, so discreteness and Lorentz invariance can coexist. On the BCC grid used here the anisotropy is pushed to order $(E/E_P)^2$ (Sec. 6.1); whether boosts are also hidden is open.

This paper keeps the organized BCC grid (Sec. 1.2), where link-only path sums leave a direction dependence of $c$ only at order $(E/E_P)^2$ (Sec. 6.1). A random, causal-set-like network whose large-scale statistics are Lorentz invariant remains a fallback if boost invariance, or the radiative-correction challenge (Sec. 6.15), requires it. Under that fallback the first-order dispersion of Sec. 7.1 is expected to vanish, consistent with Fermi and LHAASO. Residual signatures would then have to be sought elsewhere, for example in tiny non-local corrections to wave propagation or in "swerving" (momentum diffusion) of particles over very long baselines, as discussed in the causal set literature. In that literature swerving arises from stochastic dynamics; with the deterministic replotting assumed here, it would appear only if the node rule contained stochastic elements. Quantifying these for a specific choice of $T$ and $\hat{U}_{\text{net}}$ is future work.


### 7.4 Most Accessible Test: Gravity-Mediated Entanglement (Hypothesis)

Bose et al. (2017) and Marletto and Vedral (2017) proposed placing two small masses, each in a superposition of two locations, close enough that only gravity couples them, and then testing whether the masses become entangled. Their argument is that a purely classical mediator cannot create entanglement, so observing it would indicate that gravity has quantum features. The inference relies on assumptions about locality of the mediator.

In this model, correlations are held server-side and gravity arises from the workload of quantum (client) states. Each branch of a superposed mass therefore loads the nodes differently, and the two masses' joint state would acquire branch-dependent phases. The expectation is that such an experiment would observe gravity-generated entanglement, as standard quantum mechanics with a quantum gravitational interaction predicts. A null result, with the experiment performing as designed, would count against the model.

*Caveat. This is an expectation, not a derivation: the ledger's node rule has not been used to compute the entanglement rate, and the prediction coincides with that of other quantum treatments of gravity, so a positive result would not single out this model.*


### 7.5 Small-Source Relativistic Tests (Hypothesis)

Relativistic effects of a gravitational source, such as clock-rate shifts and the curvature-related effects of Sec. 6.14, have so far been measured only for astronomical or planetary sources. For laboratory-scale sources only the Newtonian attraction has been measured, down to a source mass of about 90 mg (Westphal et al., 2021).

**Node-sum estimates.** With $GM/(rc^2) = (M/m_P)(l_P/r)$, the fractional clock-rate shift at distance $r$ from a small source can be estimated directly in Planck units:

| Source | Mass | Distance $r$ | $GM/(rc^2)$ |
|---|---|---|---|
| Baseball | 145 g | 3.7 cm (surface) | $\approx 3\times10^{-27}$ |
| Tungsten block | 1 tonne | 0.231 m (surface of equal-mass sphere) | $\approx 3.2\times10^{-24}$ |
| Great Pyramid (own mass) | $\approx 6\times10^{9}$ kg | apex | $\approx 4\times10^{-20}$ |

: Fractional clock-rate shift produced by small sources (point-mass or uniform-density estimates).

- For the tungsten block, a shift of $3.2\times10^{-24}$ corresponds to about $3\times10^{-19}$ s per day.
- The pyramid value is computed for a uniform solid pyramid (base 230 m, height 147 m) and refers to the potential of its own mass at the apex, not to the height difference in Earth's field.
- For comparison, transportable optical clocks have reached uncertainties near $10^{-18}$ and have measured Earth's gravitational redshift over height differences in the field (Grotti et al., 2018; Takamoto et al., 2020). All three estimates lie below that level; the pyramid value, the largest, is about 25 times smaller.
- *Closest existing probe.* An atom-interferometer measurement detected the gravitational Aharonov–Bohm phase shift produced by a 1.25 kg tungsten source mass (Overstreet et al., 2022). This is a quantum phase arising from the source's potential, at the Newtonian level, rather than a test of its relativistic corrections.

**What such tests would show.** At every accessible scale, the node sum reproduces the predictions of general relativity. A small-source relativistic measurement would therefore extend tests of GR into a new regime and check the model's consistency jointly with GR. It would not distinguish the two. That would require a prediction from an explicit node rule that departs from GR for small sources.

*Caveat. The estimates are order-of-magnitude values from point-mass or uniform-density formulas; real experiments would face gradients, shielding and environmental effects not considered here.*

---

### 7.6 A Hard Frequency Ceiling (Hypothesis)

If space is sampled at one node per Planck length and one update per Planck time, the ledger has a fixed clock rate $f_{\text{tick}} = 1/t_P = c/\ell_P \approx 1.85\times10^{43}$ Hz. By the sampling theorem (Nyquist, 1928; Shannon, 1949), a wave needs at least two nodes per wavelength, so the highest frequency the network can carry is about half of this:
$$ f_{\max} \approx \frac{1}{2t_P} \approx 9\times10^{42}\ \text{Hz}, \qquad E_{\max} = h f_{\max} \sim E_P \approx 10^{19}\ \text{GeV}. $$
The ledger therefore predicts that no physical wave or particle exceeds this ceiling, and that energies, momenta and loop integrals stay finite (Sec. 1.2), with no ultraviolet divergence to remove. The exact factor depends on the lattice geometry (for the BCC grid of Sec. 6.2 the zone boundary is direction-dependent, so the ceiling is of order, not exactly, $1/2t_P$), and the top of the band is occupied by the gapped doubler modes, so ordinary smooth physics ends well below it. *The ceiling holds in the server's own frame; since that frame is hidden from clients (Sec. 6.15), how a boosted client observer sees it is tied to the open question of Lorentz invariance (Sec. 7.3). The highest observed energies (cosmic rays near $3\times10^{11}$ GeV) lie about eight orders of magnitude below it, so this is a consistency statement rather than a near-term test.*

### 7.7 Constant Dark Energy (Hypothesis)

The flat per-node cost of Sec. 6.10 predicts $w = -1$ exactly at all times. *A confirmed time-varying dark energy, as hinted by DESI's first-year BAO results combined with CMB and supernova data (DESI Collaboration, 2025), would rule it out.*

## 8. Open Framework Objectives

### 8.1 The Quantum Mechanics of Ledger Extraction

The primary objective of the framework is to eliminate the ad-hoc application of the Born Rule during client-side read-out. Future work must demonstrate how a local projection on a Tensor Network State (TNS) substrate naturally enforces an operational trace form $p = \mathrm{Tr}(\rho P)$ across space-like separated nodes without explicit non-local message routing.

### 8.2 Radiative Lorentz Invariance and Ultraviolet Regularization

While link-only path sums on the BCC grid suppress directional anisotropy to order $(E/E_P)^2$ at tree level, the model must be tested against radiative corrections in virtual loops. We must formalize either:

1. An exact counter-term mechanism within the node's internal component chain that blocks grid-anisotropy leakage to low energies.
2. A transition from a rigid BCC lattice to a discrete Causal Set background generated via a coordinate-free Poisson distribution.

### 8.3 Chiral Lattice Gauge Theory Integration

While the internal component chain successfully achieves domain-wall isolation for free chiral Dirac fermions, coupling these end-modes to a localized gauge field remains an open bottleneck. We must formulate an explicit, anomaly-free implementation of a left-handed weak gauge sector that avoids the constraints of the Nielsen-Ninomiya theorem without re-introducing doubler excitations into the bulk ledger.

## 9. Summary and Next Steps

The Space-Ledger framework restates quantum phenomena in terms of a quantized spacetime network, with a clear split between a non-local server-side state and a local client-side world:

| Phenomenon | Common Interpretation | Quantized Space-Ledger Proposal |
| :--- | :--- | :--- |
| **Wave–Particle Duality** | The quantum object shows wave or particle aspects depending on the experimental arrangement (complementarity). | The wavefunction belongs to spacetime (the ledger). The "particle" is the localized excitation rendered on the client side when the ledger is queried. |
| **Measurement Collapse** | Copenhagen: measurement is an irreversible interaction with a classical apparatus. (Collapse by *conscious* observation is the separate von Neumann–Wigner view, not Copenhagen.) | Environmental coupling spreads server-side phase correlations into many environment nodes (decoherence); one outcome is sampled, locked and returned to the client side by the postulated server-side read-out (Born rule). |
| **Delayed-Choice "Retrocausality"** | Popular accounts suggest erasure changes how the particle moved in the past; standard QM shows it does not. | The ledger holds joint signal–idler correlations; the screen is never fringed on its own; sorting by idler outcome reveals sub-ensemble fringes. No past is rewritten. |
| **Bell Non-Locality** | Entangled correlations violate local hidden-variable bounds. | Non-locality lives on the server side (the spacetime substrate); the client side stays local and no-signaling. |

: Summary of standard interpretations and the Space-Ledger proposal.

**Open problems and next steps:**

1. Derive the Born read-out rule from the structure of the ledger, rather than postulating it. Given a complex Hilbert-space structure and additive outcomes, Gleason's theorem fixes the rule as the square, and the simulations of Sec. 3.3 show that softmax, power and exponential alternatives fail three-slit, detector-merging or no-signalling tests. The problem therefore narrows to why server-side amplitudes behave like rotatable arrows (complex Hilbert-space structure with unitary updates). How the server side stores joint (entangled) states is also left open.
2. Specify a concrete $T$ and $\hat{U}_{\text{net}}$ and show they reproduce relativistic quantum field theory in the continuum limit.
3. Show how the server-side ordering of updates remains unobservable to clients, preserving relativity.
4. Make the "mass loads the server" proposal quantitative: show how curvature, time dilation, and Einstein's field equations at large scales emerge from variations in the ledger's node workload or entanglement structure, with all excitations coupling identically to that geometry (equivalence principle).
5. For black holes (Sec. 6.5): show that a server-side maximum node load at Planck density consistently replaces the GR singularity, and show how the unitary ledger releases information from the interior into Hawking radiation so that the emission follows the Page curve. (The supernova bounce is a client-side, nuclear-matter effect and needs no server-side explanation.)
6. Derive the spin-statistics connection and Pauli exclusion from the structure of the ledger network (Sec. 6.7), rather than importing them from standard quantum field theory.
7. Vacuum energy (Sec. 6.10): find a mechanism by which the server's idle traffic does not gravitate at the naive QFT level, or show that the ledger's finite, area-scaling degrees of freedom reduce the vacuum energy toward the observed value. We regard this as one of the most promising directions for the model.
8. Matter–antimatter asymmetry (Sec. 3.6): specify the CP-violating bias in the server's update rule and show that it yields the observed baryon-to-photon ratio while satisfying Sakharov's conditions.
9. Dark matter (Sec. 6.11): identify which network excitation dark matter is, why it loads the server but does not couple to the electromagnetic carriers, and what sets its abundance.
10. Three generations (Sec. 6.8): derive from the network why there are three resonance modes of the fermion excitation pattern, and their mass ratios, including whether the Koide relation follows, and likewise the neutrino mass-squared splittings, PMNS mixing angles and absolute neutrino mass scale.
11. Higgs sector (Sec. 6.12): find a local network rule that settles at the *interacting* critical point without tuning (a form of self-organized criticality), rather than at the free value $\kappa_c = 1/8$.
12. Derive $\lambda(M_{\text{Pl}}) \approx 0$ and the $10^{-17}$ ratio $m_H/M_{\text{Pl}}$ from the network, and determine whether an extra hidden server-side field (scalar or gauge) is required to generate the electroweak scale.
13. Compute the dispersion and diffusion signatures of a random, causal-set-like ledger and compare them against Fermi, LHAASO and future data. For regular grids, isotropy of $c$ at observable energies is resolved as a potential candidate (Sec. 6.1): link-only path sums give a residual of order $(E/E_P)^2$; the grid-versus-random choice now turns mainly on boost invariance and the radiative-correction challenge (open problem 18).
14. Information cap (Sec. 6.13): derive area-law entanglement of node states from the node update rule, so that the holographic bound follows from the network rather than being imposed.
15. General relativity (Sec. 6.14): derive the rule mapping the node workload tensor (summed app 4-momenta) to the effective metric from the node update rules, show that it reproduces the Einstein equation in the continuum limit, and show the absence of observable lattice anisotropy.
16. Black-hole cores (Sec. 6.16): compute the core structure from the node rules, including its maximum load, whether an inner horizon forms, and whether it is stable.
17. Hiding the server frame (Sec. 6.15): repeat the dispersion and moving-pattern tests with vector and tensor fields and with the actual node update rule, and determine whether any linear-in-energy dispersion arises.
18. Radiative transmission of grid anisotropy (Sec. 6.15): determine whether the node update rule suppresses the transmission of grid anisotropy to low-energy physics through virtual-particle loops (Collins et al., 2004), for example through a protecting symmetry, without fine tuning.
19. Planck-mass load on one node (Sec. 6.14): determine the node rule's behaviour when a single node carries a workload of about one Planck mass ($m_P \approx 2.18\times10^{-8}$ kg), and show that GR is recovered when the same load is spread over many nodes. The Planck mass is the crossover at which a black hole's Schwarzschild radius ($2Gm/c^2$) reaches about one Planck length (exactly $2\,l_P$ for $m = m_P$).
20. Factor of two in light deflection (Sec. 6.14, worked example): derive, from an explicit node update rule with a tensor workload, equal time and space contributions to the effective metric, so that the solar deflection is $4GM/(bc^2)$ without inserting the factor 2 by hand. Partly addressed (Sec. 6.14): an isotropic local ledger balance forces equal contributions; the remaining aim is to derive that isotropy and the per-link state count from the node rules.
21. Self-loading and the perihelion advance (Sec. 6.14, Mercury worked example): derive $\beta = 1$ (the gravitational field's own workload loading nodes) together with $\gamma = 1$ from the same explicit tensor node rule, so that Mercury's 43 arcsec per century follows without borrowing PPN parameters.
22. Node saturation (Sec. 6.17): derive from the node update rule a frame-independent cap (candidate: a limiting curvature on tensor invariants, equivalently $\sqrt{s} \lesssim E_P$ per cell); add conditions for cases where scalar invariants vanish, such as plane gravitational waves; determine the cap value and the minimum black-hole mass (about $0.17\,m_P$ in the toy), both of which are toy-dependent; compute the saturated core dynamically during collapse and the fate of sub-threshold saturated objects; and decide whether any per-particle speed limit below $c$ exists (hidden-frame or doubly-special-relativity form).
23. Candidate hardware (Sec. 6.2): fermion doubling is resolved in the four-component construction with a Wilson layer. Chirality is partly addressed by the internal component chain ($4N_s$ components per node; Sec. 6.2), which reinterprets Kaplan's fifth dimension as internal per-node states rather than an extra spatial dimension; still open: coupling chiral modes to the weak gauge field (chiral lattice gauge theory), the exact relation between $c$ and the hop rate $\ell_P/t_P$, interactions, how single-writer shared records hold many-particle joint states, and whether the rule can carry the node workload needed for gravity, and how a grid of local cores realises the holistic read-out of a shared record (Sec. 5.2) without client-detectable signaling.
24. Per-node fee (Sec. 6.10): derive the size $e \approx 1.1\times10^{-123}$ in Planck units from purely local node rules, without a global horizon input.
25. Outer halo slope (Sec. 6.11): rerun the light-scalar toy on an expanding grid with ongoing infall and test whether the outer profile steepens to $r^{-3}$.
26. Early splitting (Sec. 6.10): derive the log-load counting and the slot size $b$ from the node rules, rather than choosing them.
27. Born-rule odds (Sec. 5.5): derive the $\cos^2$ read-out odds of Sec. 5.5 from the node rules rather than inserting them.

**Methodological note.** To keep the model falsifiable, server-side explanations are reserved for regimes where known physics fails or is silent: quantum correlations and measurement, Planck-scale structure, and black-hole interiors. Where established client-side physics (nuclear forces, degeneracy pressure, hydrodynamics) already explains a phenomenon, as in supernova bounces, the ledger reinterprets it but does not replace it. A framework that can attribute anything to the server would predict nothing.

This draft offers a foundation for modeling the universe not as particles in a void, but as a self-updating computational substrate whose local, light-speed-limited "client" world is rendered from a global spacetime ledger.

---

## References

- Born, M. "Zur Quantenmechanik der Stoßvorgänge." *Z. Phys.* 37, 863–867 (1926).
- Boyer, T. H. "Random electrodynamics: the theory of classical electrodynamics with classical electromagnetic zero-point radiation." *Phys. Rev. D* 11, 790 (1975).
- de la Peña, L., Cetto, A. M. *The Quantum Dice: An Introduction to Stochastic Electrodynamics.* Kluwer, Dordrecht (1996).
- Gleason, A. M. "Measures on the closed subspaces of a Hilbert space." *J. Math. Mech.* 6, 885–893 (1957).
- Busch, P. "Quantum states and generalized observables: a simple proof of Gleason's theorem." *Phys. Rev. Lett.* 91, 120403 (2003).
- Goy, P., Raimond, J. M., Gross, M. & Haroche, S. "Observation of cavity-enhanced single-atom spontaneous emission." *Phys. Rev. Lett.* 50, 1903 (1983).
- Heinzen, D. J. & Feld, M. S. "Vacuum radiative level shift and spontaneous-emission linewidth of an atom in an optical resonator." *Phys. Rev. Lett.* 58, 2343 (1987).
- Kleppner, D. "Inhibited spontaneous emission." *Phys. Rev. Lett.* 47, 233 (1981).
- Marshall, T. W. "Random electrodynamics." *Proc. R. Soc. Lond. A* 276, 475 (1963).
- Purcell, E. M. "Spontaneous emission probabilities at radio frequencies." *Phys. Rev.* 69, 681 (1946).
- Sorkin, R. D. "Quantum mechanics as quantum measure theory." *Mod. Phys. Lett. A* 9, 3119–3128 (1994).
- Sinha, U., Couteau, C., Jennewein, T., Laflamme, R., Weihs, G. "Ruling out multi-order interference in quantum mechanics." *Science* 329, 418–421 (2010).
- Kauten, T., Keil, R., Kaufmann, T., Pressl, B., Brukner, Č., Weihs, G. "Obtaining tight bounds on higher-order interferences with a 5-path interferometer." *New J. Phys.* 19, 033017 (2017).
- Gisin, N. "Weinberg's non-linear quantum mechanics and supraluminal communications." *Phys. Lett. A* 143, 1–2 (1990).
- Polchinski, J. "Weinberg's nonlinear quantum mechanics and the Einstein-Podolsky-Rosen paradox." *Phys. Rev. Lett.* 66, 397–400 (1991).
- Abdo, A. A. et al. (Fermi LAT and GBM Collaborations). "A limit on the variation of the speed of light arising from quantum gravity effects." *Nature* 462, 331–334 (2009).
- Cao, Z. et al. (LHAASO Collaboration). "Stringent Tests of Lorentz Invariance Violation from LHAASO Observations of GRB 221009A." *Phys. Rev. Lett.* 133, 071501 (2024). arXiv:2402.06009.
- Kim, Y.-H., Yu, R., Kulik, S. P., Shih, Y., Scully, M. O. "Delayed 'Choice' Quantum Eraser." *Phys. Rev. Lett.* 84, 1 (2000).
- Bell, J. S. "On the Einstein Podolsky Rosen paradox." *Physics* 1, 195 (1964).
- Bancal, J.-D., Pironio, S., Acín, A., Liang, Y.-C., Scarani, V., Gisin, N. "Quantum non-locality based on finite-speed causal influences leads to superluminal signalling." *Nature Physics* 8, 867–870 (2012).
- Bohm, D. "A suggested interpretation of the quantum theory in terms of 'hidden' variables. I." *Physical Review* 85, 166–179 (1952).
- Salart, D., Baas, A., Branciard, C., Gisin, N., Zbinden, H. "Testing the speed of 'spooky action at a distance'." *Nature* 454, 861–864 (2008).
- Hensen, B. et al. "Loophole-free Bell inequality violation using electron spins separated by 1.3 kilometres." *Nature* 526, 682 (2015).
- Bird, D. J. et al. "Detection of a cosmic ray with measured energy well beyond the expected spectral cutoff due to cosmic microwave radiation." *Astrophys. J.* 441, 144 (1995).
- Bombelli, L., Henson, J., Sorkin, R. D. "Discreteness without symmetry breaking: a theorem." *Mod. Phys. Lett. A* 24, 2579 (2009).
- Tryon, E. P. "Is the universe a vacuum fluctuation?" *Nature* 246, 396 (1973).
- Zurek, W. H. "Decoherence, einselection, and the quantum origins of the classical." *Rev. Mod. Phys.* 75, 715 (2003).
- Feynman, R. P., Hibbs, A. R. *Quantum Mechanics and Path Integrals.* McGraw-Hill (1965).
- Bialynicki-Birula, I. "Weyl, Dirac, and Maxwell equations on a lattice as unitary cellular automata." *Phys. Rev. D* 49, 6920 (1994).
- Meyer, D. A. "From quantum cellular automata to quantum lattice gases." *J. Stat. Phys.* 85, 551 (1996).
- Strauch, F. W. "Relativistic quantum walks." *Phys. Rev. A* 73, 054302 (2006).
- Arrighi, P., Nesme, V., Forets, M. "The Dirac equation as a quantum walk: higher dimensions, observational convergence." *J. Phys. A* 47, 465302 (2014).
- D'Ariano, G. M., Perinotti, P. "Derivation of the Dirac equation from principles of information processing." *Phys. Rev. A* 90, 062106 (2014).
- Van Raamsdonk, M. "Building up spacetime with quantum entanglement." *Gen. Relativ. Gravit.* 42, 2323 (2010).
- Jacobson, T. "Thermodynamics of spacetime: the Einstein equation of state." *Phys. Rev. Lett.* 75, 1260 (1995). arXiv:gr-qc/9504004.
- Bombelli, L., Koul, R. K., Lee, J., Sorkin, R. D. "Quantum source of entropy for black holes." *Phys. Rev. D* 34, 373 (1986).
- Srednicki, M. "Entropy and area." *Phys. Rev. Lett.* 71, 666 (1993).
- Nakamura, T. T., Deguchi, S. "Wave optics in gravitational lensing." *Prog. Theor. Phys. Suppl.* 133, 137 (1999). doi:10.1143/PTPS.133.137.
- Bombelli, L., Lee, J., Meyer, D., Sorkin, R. D. "Space-time as a causal set." *Phys. Rev. Lett.* 59, 521 (1987).
- Janka, H.-T. "Explosion mechanisms of core-collapse supernovae." *Annu. Rev. Nucl. Part. Sci.* 62, 407 (2012).
- Hirata, K. et al. (Kamiokande-II). "Observation of a neutrino burst from the supernova SN1987A." *Phys. Rev. Lett.* 58, 1490 (1987).
- Bionta, R. M. et al. (IMB). "Observation of a neutrino burst in coincidence with supernova 1987A in the Large Magellanic Cloud." *Phys. Rev. Lett.* 58, 1494 (1987).
- Penrose, R. "Gravitational collapse and space-time singularities." *Phys. Rev. Lett.* 14, 57 (1965).
- Frolov, V. P., Markov, M. A., Mukhanov, V. F. "Through a black hole into a new universe?" *Phys. Lett. B* 216, 272 (1989).
- Mukhanov, V., Brandenberger, R. "A nonsingular universe." *Phys. Rev. Lett.* 68, 1969 (1992).
- Brandenberger, R. H. "Implementing Markov's limiting curvature hypothesis." arXiv:gr-qc/9509059 (1995).
- Magueijo, J., Smolin, L. "Lorentz invariance with an invariant energy scale." *Phys. Rev. Lett.* 88, 190403 (2002).
- Amelino-Camelia, G. "Doubly-special relativity: first results and key open problems." *Int. J. Mod. Phys. D* 11, 1643 (2002).
- Markov, M. A. "Limiting density of matter as a universal law of nature." *JETP Lett.* 36, 265 (1982).
- Rovelli, C., Vidotto, F. "Planck stars." *Int. J. Mod. Phys. D* 23, 1442026 (2014).
- Hawking, S. W. "Particle creation by black holes." *Commun. Math. Phys.* 43, 199 (1975).
- Page, D. N. "Information in black hole radiation." *Phys. Rev. Lett.* 71, 3743 (1993).
- Penington, G. "Entanglement wedge reconstruction and the information paradox." *JHEP* 09 (2020) 002; arXiv:1905.08255 (2019).
- Almheiri, A., Engelhardt, N., Marolf, D., Maxfield, H. "The entropy of bulk quantum fields and the entanglement wedge of an evaporating black hole." *JHEP* 12 (2019) 063.
- Bekenstein, J. D. "Black holes and entropy." *Phys. Rev. D* 7, 2333 (1973).
- Garay, L. J. "Quantum gravity and minimum length." *Int. J. Mod. Phys. A* 10, 145 (1995).
- Hossenfelder, S. "Minimal length scale scenarios for quantum gravity." *Living Rev. Relativ.* 16, 2 (2013).
- Lamb, W. E., Retherford, R. C. "Fine structure of the hydrogen atom by a microwave method." *Phys. Rev.* 72, 241 (1947).
- Bethe, H. A. "The electromagnetic shift of energy levels." *Phys. Rev.* 72, 339 (1947).
- Jaffe, R. L. "The Casimir effect and the quantum vacuum." *Phys. Rev. D* 72, 021301 (2005).
- Lamoreaux, S. K. "Demonstration of the Casimir force in the 0.6 to 6 $\mu$m range." *Phys. Rev. Lett.* 78, 5 (1997).
- Bennett, C. H., Bernstein, E., Brassard, G. & Vazirani, U. "Strengths and weaknesses of quantum computing." *SIAM J. Comput.* 26, 1510 (1997).
- Herbert, N. "FLASH—A superluminal communicator based upon a new kind of quantum measurement." *Found. Phys.* 12, 1171 (1982).
- Wootters, W. K., Zurek, W. H. "A single quantum cannot be cloned." *Nature* 299, 802–803 (1982).
- Dieks, D. "Communication by EPR devices." *Phys. Lett. A* 92, 271 (1982).
- Zurek, W. H. "Quantum Darwinism." *Nature Phys.* 5, 181 (2009).
- Pauli, W. "Über den Zusammenhang des Abschlusses der Elektronengruppen im Atom mit der Komplexstruktur der Spektren." *Z. Phys.* 31, 765 (1925).
- Pauli, W. "The connection between spin and statistics." *Phys. Rev.* 58, 716 (1940).
- Misra, B., Sudarshan, E. C. G. "The Zeno's paradox in quantum theory." *J. Math. Phys.* 18, 756 (1977).
- Itano, W. M., Heinzen, D. J., Bollinger, J. J., Wineland, D. J. "Quantum Zeno effect." *Phys. Rev. A* 41, 2295 (1990).
- Gamow, G. "Zur Quantentheorie des Atomkernes." *Z. Phys.* 51, 204 (1928).
- Binnig, G., Rohrer, H., Gerber, Ch., Weibel, E. "Surface studies by scanning tunneling microscopy." *Phys. Rev. Lett.* 49, 57 (1982).
- Weinberg, S. "The cosmological constant problem." *Rev. Mod. Phys.* 61, 1 (1989).
- Cohen, A. G., Kaplan, D. B., Nelson, A. E. "Effective field theory, black holes, and the cosmological constant." *Phys. Rev. Lett.* 82, 4971 (1999).
- Albert, D. Z. *Time and Chance.* Harvard University Press (2000).
- Zeh, H. D. *The Physical Basis of the Direction of Time.* Springer (1989).
- Sakharov, A. D. "Violation of CP invariance, C asymmetry, and baryon asymmetry of the universe." *JETP Lett.* 5, 24 (1967).
- Canetti, L., Drewes, M., Shaposhnikov, M. "Matter and antimatter in the universe." *New J. Phys.* 14, 095012 (2012).
- Planck Collaboration (Aghanim, N., et al.). "Planck 2018 results. VI. Cosmological parameters." *Astron. Astrophys.* 641, A6 (2020).
- Planck Collaboration (Akrami, Y., et al.). "Planck 2018 results. X. Constraints on inflation." *Astron. Astrophys.* 641, A10 (2020).
- Starobinsky, A. A. "A new type of isotropic cosmological models without singularity." *Phys. Lett. B* 91, 99 (1980).
- BICEP/Keck Collaboration (Ade, P. A. R., et al.). "Improved constraints on primordial gravitational waves using Planck, WMAP, and BICEP/Keck observations through the 2018 observing season." *Phys. Rev. Lett.* 127, 151301 (2021).
- Clowe, D., et al. "A direct empirical proof of the existence of dark matter." *Astrophys. J. Lett.* 648, L109 (2006).
- Randall, S. W., Markevitch, M., Clowe, D., Gonzalez, A. H., Bradač, M. "Constraints on the self-interaction cross section of dark matter from numerical simulations of the merging galaxy cluster 1E 0657-56." *Astrophys. J.* 679, 1173 (2008).
- Verlinde, E. P. "Emergent gravity and the dark universe." *SciPost Phys.* 2, 016 (2017).
- Yang, Y.-B., et al. "Proton mass decomposition from the QCD energy momentum tensor." *Phys. Rev. Lett.* 121, 212001 (2018).
- Abbott, B. P., et al. (LIGO Scientific and Virgo Collaborations). "Observation of gravitational waves from a binary black hole merger." *Phys. Rev. Lett.* 116, 061102 (2016).
- ALEPH, DELPHI, L3, OPAL, SLD Collaborations, et al. "Precision electroweak measurements on the Z resonance." *Phys. Rept.* 427, 257 (2006).
- Koide, Y. "A fermion-boson composite model of quarks and leptons." *Phys. Lett. B* 120, 161 (1983).
- Fukuda, Y. et al. (Super-Kamiokande Collaboration). "Evidence for oscillation of atmospheric neutrinos." *Phys. Rev. Lett.* 81, 1562 (1998).
- Ahmad, Q. R. et al. (SNO Collaboration). "Direct evidence for neutrino flavor transformation from neutral-current interactions in the Sudbury Neutrino Observatory." *Phys. Rev. Lett.* 89, 011301 (2002).
- Mohr, P. J. et al. "CODATA recommended values of the fundamental physical constants: 2022." NIST SP 961 (2024).
- Kobayashi, M., Maskawa, T. "CP-violation in the renormalizable theory of weak interaction." *Prog. Theor. Phys.* 49, 652 (1973).
- Aad, G. et al. (ATLAS Collaboration). "Observation of a new particle in the search for the Standard Model Higgs boson with the ATLAS detector at the LHC." *Phys. Lett. B* 716, 1 (2012).
- Chatrchyan, S. et al. (CMS Collaboration). "Observation of a new boson at a mass of 125 GeV with the CMS experiment at the LHC." *Phys. Lett. B* 716, 30 (2012). arXiv:1207.7235.
- Froggatt, C. D., Nielsen, H. B. "Standard Model criticality prediction: top mass 173 ± 5 GeV and Higgs mass 135 ± 9 GeV." *Phys. Lett. B* 368, 96 (1996). arXiv:hep-ph/9511371.
- Shaposhnikov, M., Wetterich, C. "Asymptotic safety of gravity and the Higgs boson mass." *Phys. Lett. B* 683, 196 (2010). arXiv:0912.0208.
- Buttazzo, D. et al. "Investigating the near-criticality of the Higgs boson." *JHEP* 12 (2013) 089. arXiv:1307.3536.
- Coleman, S., Weinberg, E. "Radiative corrections as the origin of spontaneous symmetry breaking." *Phys. Rev. D* 7, 1888 (1973).
- Gildener, E., Weinberg, S. "Symmetry breaking and scalar bosons." *Phys. Rev. D* 13, 3333 (1976).
- 't Hooft, G. "Dimensional reduction in quantum gravity." arXiv:gr-qc/9310026 (1993).
- Susskind, L. "The world as a hologram." *J. Math. Phys.* 36, 6377 (1995).
- Bousso, R. "The holographic principle." *Rev. Mod. Phys.* 74, 825 (2002).
- Maldacena, J. and Susskind, L. "Cool horizons for entangled black holes." *Fortsch. Phys.* 61, 781 (2013).
- Pais, A. "Einstein and the quantum theory." *Rev. Mod. Phys.* 51, 863 (1979).
- Fischer, M. C., Gutiérrez-Medina, B., Raizen, M. G. "Observation of the quantum Zeno and anti-Zeno effects in an unstable system." *Phys. Rev. Lett.* 87, 040402 (2001).
- Streed, E. W. et al. "Continuous and pulsed quantum Zeno effect." *Phys. Rev. Lett.* 97, 260402 (2006).
- Signoles, A. et al. "Confined quantum Zeno dynamics of a watched atomic arrow." *Nature Phys.* 10, 715 (2014).
- Nielsen, H. B., Ninomiya, M. "Absence of neutrinos on a lattice: (I). Proof by homotopy theory." *Nucl. Phys. B* 185, 20–40 (1981); erratum *Nucl. Phys. B* 195, 541 (1982).
- Nielsen, H. B., Ninomiya, M. "Absence of neutrinos on a lattice: (II). Intuitive topological proof." *Nucl. Phys. B* 193, 173–194 (1981).
- Wilson, K. G. "Quarks and strings on a lattice." In A. Zichichi (ed.), *New Phenomena in Subnuclear Physics*, Part A, 69–142. Plenum, New York (1977).
- Ginsparg, P. H., Wilson, K. G. "A remnant of chiral symmetry on the lattice." *Phys. Rev. D* 25, 2649–2657 (1982).
- Kaplan, D. B. "A method for simulating chiral fermions on the lattice." *Phys. Lett. B* 288, 342–347 (1992).
- Shamir, Y. "Chiral fermions from lattice boundaries." *Nucl. Phys. B* 406, 90–106 (1993).
- Kibble, T. W. B. "Lorentz invariance and the gravitational field." *J. Math. Phys.* 2, 212–221 (1961).
- Sciama, D. W. "The physical structure of general relativity." *Rev. Mod. Phys.* 36, 463–469 (1964).
- Hehl, F. W., von der Heyde, P., Kerlick, G. D., Nester, J. M. "General relativity with spin and torsion: Foundations and prospects." *Rev. Mod. Phys.* 48, 393–416 (1976).
- Kopczyński, W. "A non-singular universe with torsion." *Phys. Lett. A* 39, 219–220 (1972).
- Trautman, A. "Spin and torsion may avert gravitational singularities." *Nature Phys. Sci.* 242, 7–8 (1973).
- Popławski, N. J. "Cosmology with torsion: An alternative to cosmic inflation." *Phys. Lett. B* 694, 181–185 (2010); erratum *Phys. Lett. B* 701, 672 (2011).
- Margolus, N. "Physics-like models of computation." *Physica D* 10, 81–95 (1984).
- Margolus, N., Levitin, L. B. "The maximum speed of dynamical evolution." *Physica D* 120, 188 (1998).
- Lashkari, N., McDermott, M. B., Van Raamsdonk, M. "Gravitational dynamics from entanglement 'thermodynamics'." *JHEP* 04 (2014) 195.
- Faulkner, T., Guica, M., Hartman, T., Myers, R. C., Van Raamsdonk, M. "Gravitation from entanglement in holographic CFTs." *JHEP* 03 (2014) 051.
- Ambjørn, J., Jurkiewicz, J., Loll, R. "Emergence of a 4D world from causal quantum gravity." *Phys. Rev. Lett.* 93, 131301 (2004).
- Ambjørn, J., Jurkiewicz, J., Loll, R. "The spectral dimension of the universe is scale dependent." *Phys. Rev. Lett.* 95, 171301 (2005).
- Ambjørn, J., Görlich, A., Jurkiewicz, J., Loll, R. "Planckian birth of the quantum de Sitter universe." *Phys. Rev. Lett.* 100, 091304 (2008).
- Ambjørn, J., Jordan, S., Jurkiewicz, J., Loll, R. "A second-order phase transition in causal dynamical triangulations." *Phys. Rev. Lett.* 107, 211303 (2011).
- Regge, T. "General relativity without coordinates." *Nuovo Cimento* 19, 558 (1961).
- Cheeger, J., Müller, W., Schrader, R. "On the curvature of piecewise flat spaces." *Commun. Math. Phys.* 92, 405–454 (1984).
- Ashtekar, A., Pawlowski, T., Singh, P. "Quantum nature of the big bang." *Phys. Rev. Lett.* 96, 141301 (2006).
- Hayward, S. A. "Formation and evaporation of nonsingular black holes." *Phys. Rev. Lett.* 96, 031103 (2006).
- Bardeen, J. M. "Non-singular general-relativistic gravitational collapse." In *Proceedings of the International Conference GR5*, Tbilisi, USSR, p. 174 (1968).
- Abedi, J., Dykaar, H., Afshordi, N. "Echoes from the abyss: Tentative evidence for Planck-scale structure at black hole horizons." *Phys. Rev. D* 96, 082004 (2017).
- Abbott, R. et al. (LIGO Scientific, Virgo and KAGRA Collaborations). "Tests of general relativity with GWTC-3." arXiv:2112.06861 (2021); *Phys. Rev. D* 112, 084080 (2025).
- Carballo-Rubio, R., Di Filippo, F., Liberati, S., Pacilio, C., Visser, M. "On the viability of regular black holes." *J. High Energy Phys.* 07 (2018) 023.
- Gordon, W. "Zur Lichtfortpflanzung nach der Relativitätstheorie." *Ann. Phys.* 72 (377), 421–456 (1923).
- Barceló, C., Liberati, S., Visser, M. "Analogue gravity." *Living Rev. Relativ.* 14, 3 (2011).
- Unruh, W. G. "Experimental black-hole evaporation?" *Phys. Rev. Lett.* 46, 1351 (1981).
- Everitt, C. W. F. et al. "Gravity Probe B: Final results of a space experiment to test general relativity." *Phys. Rev. Lett.* 106, 221101 (2011).
- Abbott, B. P. et al. (LIGO Scientific and Virgo Collaborations). "GW170814: A three-detector observation of gravitational waves from a binary black hole coalescence." *Phys. Rev. Lett.* 119, 141101 (2017).
- Norton, J. D. "Einstein, Nordström and the early demise of scalar, Lorentz-covariant theories of gravitation." *Arch. Hist. Exact Sci.* 45, 17–94 (1992).
- Kostelecký, V. A., Russell, N. "Data tables for Lorentz and CPT violation." *Rev. Mod. Phys.* 83, 11 (2011).
- Zuse, K. *Rechnender Raum.* Schriften zur Datenverarbeitung, Vol. 1. Friedr. Vieweg & Sohn, Braunschweig (1969). English translation: *Calculating Space*, MIT Technical Translation AZT-70-164-GEMIT, Project MAC, Cambridge, MA (1970).
- 't Hooft, G. *The Cellular Automaton Interpretation of Quantum Mechanics.* Fundamental Theories of Physics, Vol. 185. Springer, Cham (2016).
- Vasileiou, V. et al. "Constraints on Lorentz invariance violation from Fermi-Large Area Telescope observations of gamma-ray bursts." *Phys. Rev. D* 87, 122001 (2013).
- Bell, J. S. "How to teach special relativity." *Progress in Scientific Culture* 1 (1976); reprinted in *Speakable and Unspeakable in Quantum Mechanics*, Cambridge University Press, Cambridge (1987), pp. 67–80.
- Braun, O. M., Kivshar, Y. S. "Nonlinear dynamics of the Frenkel–Kontorova model." *Phys. Rep.* 306, 1–108 (1998).
- Feynman, R. P. "Space-time approach to non-relativistic quantum mechanics." *Rev. Mod. Phys.* 20, 367–387 (1948).
- Jacobson, T., Liberati, S., Mattingly, D. "A strong astrophysical constraint on the violation of special relativity by quantum gravity." *Nature* 424, 1019 (2003).
- Collins, J., Perez, A., Sudarsky, D., Urrutia, L., Vucetich, H. "Lorentz invariance and quantum gravity: an additional fine-tuning problem?" *Phys. Rev. Lett.* 93, 191301 (2004).
- Groot Nibbelink, S., Pospelov, M. "Lorentz violation in supersymmetric field theories." *Phys. Rev. Lett.* 94, 081601 (2005).
- Bertotti, B., Iess, L., Tortora, P. "A test of general relativity using radio links with the Cassini spacecraft." *Nature* 425, 374 (2003).
- Weisberg, J. M., Huang, Y. "Relativistic measurements from timing the binary pulsar PSR B1913+16." *Astrophys. J.* 829, 55 (2016).
- Lee, J. G., Adelberger, E. G., Cook, T. S., Fleischer, S. M., Heckel, B. R. "New test of the gravitational 1/r² law at separations down to 52 µm." *Phys. Rev. Lett.* 124, 101101 (2020).
- Westphal, T., Hepach, H., Pfaff, J., Aspelmeyer, M. "Measurement of gravitational coupling between millimetre-sized masses." *Nature* 591, 225–228 (2021).
- Eddington, A. S. *The Internal Constitution of the Stars.* Cambridge University Press, Cambridge (1926).
- Chandrasekhar, S. *An Introduction to the Study of Stellar Structure.* University of Chicago Press, Chicago (1939).
- Soldner, J. G. von. "Ueber die Ablenkung eines Lichtstrals von seiner geradlinigen Bewegung, durch die Attraktion eines Weltkörpers, an welchem er nahe vorbei geht." *Berliner Astronomisches Jahrbuch für 1804*, 161–172 (1801).
- Einstein, A. "Über den Einfluß der Schwerkraft auf die Ausbreitung des Lichtes." *Ann. Phys.* (4) 35, 898–908 (1911).
- Dyson, F. W., Eddington, A. S., Davidson, C. "A determination of the deflection of light by the sun's gravitational field, from observations made at the total eclipse of May 29, 1919." *Phil. Trans. R. Soc. A* 220, 291–333 (1920).
- Clemence, G. M. "The relativity effect in planetary motions." *Rev. Mod. Phys.* 19, 361–364 (1947).
- Will, C. M. "The Confrontation between General Relativity and Experiment." *Living Rev. Relativ.* 17, 4 (2014). doi:10.12942/lrr-2014-4
- Hogan, C. J. "Interferometers as probes of Planckian quantum geometry." *Phys. Rev. D* 85, 064007 (2012).
- Chou, A. S., et al. (Holometer Collaboration). "First measurements of high frequency cross-spectra from a pair of large Michelson interferometers." *Phys. Rev. Lett.* 117, 111102 (2016).
- Chou, A., et al. (Holometer Collaboration). "Interferometric constraints on quantum geometrical shear noise correlations." *Class. Quantum Grav.* 34, 165005 (2017).
- Richardson, J. W., et al. "Interferometric constraints on spacelike coherent rotational fluctuations." *Phys. Rev. Lett.* 126, 241301 (2021).
- Bose, S., et al. "Spin entanglement witness for quantum gravity." *Phys. Rev. Lett.* 119, 240401 (2017).
- Marletto, C., Vedral, V. "Gravitationally induced entanglement between two massive particles is sufficient evidence of quantum effects in gravity." *Phys. Rev. Lett.* 119, 240402 (2017).
- Grotti, J., et al. "Geodesy and metrology with a transportable optical clock." *Nat. Phys.* 14, 437–441 (2018).
- Takamoto, M., et al. "Test of general relativity by a pair of transportable optical lattice clocks." *Nat. Photon.* 14, 411–415 (2020).
- Overstreet, C., Asenbaum, P., Curti, J., Kim, M., Kasevich, M. A. "Observation of a gravitational Aharonov–Bohm effect." *Science* 375, 226–229 (2022).
- Nyquist, H. "Certain topics in telegraph transmission theory." *Trans. AIEE* 47, 617–644 (1928).
- Shannon, C. E. "Communication in the presence of noise." *Proc. IRE* 37, 10–21 (1949).
- Hsu, S. D. H. "Entropy bounds and dark energy." *Phys. Lett. B* 594, 13 (2004).
- Li, M. "A model of holographic dark energy." *Phys. Lett. B* 603, 1 (2004).
- DESI Collaboration (Adame, A. G., et al.). "DESI 2024 VI: Cosmological constraints from the measurements of baryon acoustic oscillations." *JCAP* 02, 021 (2025).
- Hu, W., Barkana, R., Gruzinov, A. "Cold and fuzzy dark matter." *Phys. Rev. Lett.* 85, 1158 (2000).
- Schive, H.-Y., Chiueh, T., Broadhurst, T. "Cosmic structure as the quantum interference of a coherent dark wave." *Nat. Phys.* 10, 496 (2014).
- Hui, L., Ostriker, J. P., Tremaine, S., Witten, E. "Ultralight scalars as cosmological dark matter." *Phys. Rev. D* 95, 043541 (2017).
- Iršič, V., et al. "First constraints on fuzzy dark matter from Lyman-$\alpha$ forest data and hydrodynamical simulations." *Phys. Rev. Lett.* 119, 031302 (2017).
