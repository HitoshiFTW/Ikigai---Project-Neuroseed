# Energy Efficiency Intelligence Law: Evidence from a Biologically Constrained Adaptive System

**Prince Siddhpara**
Hitoshi AI Labs — NeuroSeed Project
March 22, 2026

*First draft. Not for distribution. For internal clarification only.*

---

## Abstract

In biologically-constrained adaptive systems, alignment with survival-relevant variables produces efficient behavior. Systems that optimize proxy objectives without structural coupling to resource availability fail below random baselines, while aligned systems achieve consistent net-positive energy efficiency across stochastic conditions and extended time horizons.

Efficiency, however, is insufficient as a primary criterion. Constraint ablation shows that removing a single regulatory mechanism -- world-model energy weighting -- produces the highest measured efficiency in the experiment, achieved through behavioral collapse: near-exclusive approach behavior, unregulated accumulation, and near-zero behavioral diversity. High efficiency and adaptive behavior are not the same thing.

Robustness is the stronger criterion. Environmental generalization shows that unregulated systems degenerate in one environment and succeed accidentally in another. An independent Q-learning architecture produces the same structural pattern -- alignment increases efficiency, regulation preserves behavioral diversity -- demonstrating that these effects are not artifacts of the specific implementation. Temporal evaluation shows that the aligned and regulated system maintains consistent behavioral structure across sleep regimes from 6% to 45%, while the degenerate system exhibits timescale-dependent failure modes with no stable behavioral attractor.

These results establish a three-axis invariance: the aligned and regulated system maintains stable behavioral structure across environments, across architectures, and across time. Behavior is not characterized by efficiency alone, but by its stability under variation. Both alignment and regulation are necessary; neither alone is sufficient.

---

## 1. Introduction

Contemporary AI development is organized around a scaling hypothesis: performance on most tasks increases predictably with model size, training compute, and data volume (Kaplan et al. 2020; Hoffmann et al. 2022). This hypothesis has been broadly validated. Language models, image generators, and game-playing systems have all improved substantially as scale increased. The approach has produced genuinely capable systems.

It has also produced systems that consume extraordinary energy. Training a large language model can require gigawatt-hours of electricity. Inference at scale requires continuous high-power compute. The energy cost per unit of useful computation is not a priority in the current development paradigm -- it is a secondary concern, managed through hardware efficiency but not addressed at the level of system design.

Modern AI systems rely on large-scale optimization, often without explicit coupling to survival-relevant constraints. This raises a structural question: is inefficiency caused by insufficient optimization, or by misalignment between objectives and system constraints? These are distinct problems with distinct solutions. Scaling addresses the first. Structural realignment is required for the second.

Biological systems operate under the opposite constraint. A human brain consumes approximately 20 watts. It processes continuous sensory input, regulates bodily functions, plans, learns, and generalizes from minimal data -- all within a metabolic budget that would be insufficient to run a modest laptop. The efficiency of biological intelligence is not incidental to its architecture; it is central to it. Metabolic constraints shaped the structural organization of neural systems over evolutionary time.

A central challenge in evaluating adaptive systems is distinguishing between systems that are efficient due to structural alignment and those that achieve efficiency by exploiting specific environmental structures. A system may appear efficient in one environment for reasons that do not generalize: its proxy objective may happen to align with the reward structure of that particular context. This work addresses this distinction directly, evaluating both efficiency and behavioral robustness across controlled environmental variations, independent system architectures, and temporal regimes. The convergent finding across all three axes defines the central claim.

---

## 2. The EEIL Hypothesis

**Energy Efficiency Intelligence Law (EEIL)**: EEIL describes a constraint-based structure in which:

- alignment with survival-relevant variables enables efficient behavior
- regulatory mechanisms constrain optimization to prevent degeneration

This structure is consistent with biological systems, where behavior is both driven by internal needs and constrained by regulatory processes. Systems lacking alignment exhibit inefficient or random behavior. Systems lacking regulation may achieve high efficiency through behavioral collapse -- narrow strategy convergence, unregulated accumulation, or environment-specific exploitation. Both components are required for consistent, adaptive behavior.

The hypothesis has three claims.

The **alignment claim**: systems optimizing proxy objectives without regulatory constraints that couple those objectives to survival-relevant signals will exhibit lower efficiency than systems where such coupling is present. This is tested in the primary experiment (Conditions A--D) and replicated across Phases A and B.

The **regulation claim**: even within structurally aligned systems, individual regulatory constraints prevent degenerate optimization. Without regulation, systems may achieve high efficiency metrics through behavioral collapse rather than genuine adaptive regulation. Degenerate optimization produces environment-dependent behavior: a system may succeed or fail depending on whether its collapsed strategy matches the current environment's reward structure.

The **robustness claim** follows from both: a system that is aligned and regulated will maintain consistent behavioral structure -- entropy, energy regulation, action diversity -- across environments, architectures, and time. This cross-axis stability is not a side effect of alignment and regulation; it is their defining property, and the stronger criterion for adaptive behavior. Efficiency alone can be produced through environmental exploitation or metric gaming; robustness across axes cannot.

We define the relevant terms as follows.

**Energy efficiency** is the ratio of total energy inflows to total energy outflows across a simulation episode. EES = total_energy_gained / total_energy_spent. An EES > 1.0 indicates a system that, on net, acquires more energy than it expends.

**Behavioral robustness** is stability of behavioral structure (action distribution, energy regulation, diversity) across qualitatively different environments. A system is behaviorally robust if its entropy, mean energy, and action distribution remain consistent regardless of environment class -- not because it achieves the same EES, but because its regulatory architecture produces context-appropriate responses rather than environment-contingent degeneration.

**Structured regulatory constraints** are internal mechanisms that couple the organism's metabolic state to its action selection policy: (1) a homeostatic hunger drive, (2) an energy-conditioned precision weighting, (3) a survival value function that weights energy consequences, and (4) state-conditioned preference learning.

---

## 3. System Description

Ikigai is a biologically grounded adaptive simulation implementing the following components.

**Action space.** The organism selects one of three actions per waking tick: approach (foraging behavior), explore (curiosity-driven sampling), or withdraw (conservative recovery).

**Energy system.** Energy is distributed across three neural compartments (cortical, limbic, motor), each bounded to [0, 1]. A foraging mechanism provides probabilistic energy gain on approach: success probability = 0.20 + 0.80 * (energy/0.80)^2, ensuring a minimum 20% yield regardless of energy state while maintaining scarcity at low energy. Metabolic cost applies every waking tick.

**Regulatory drives.** A hunger drive fires when mean energy falls below 0.25, adding a proportional bias toward approach in the action selection computation. An energy-conditioned temperature parameter adjusts action selection precision: low energy produces conservative behavior, mid energy produces exploratory behavior, high energy produces exploitation.

**World model.** A survival value function predicts the energetic, cortisol, and prediction-error consequences of each action and selects the action maximizing predicted survival value. The function weights energy consequences (w_e = 1.0), prediction error consequences (w_pe = 0.6), cortisol consequences (w_cort = 0.4), and switching costs (w_wc = 0.2).

**Learning.** A state-conditioned preference mechanism maintains bias values pref[state][action] for each combination of energy band (low/mid/high) and action. Biases are updated per waking tick via: pref[state][action] += learning_rate * (energy_after - energy_before), clamped to [-1, 1].

**Sleep-wake dynamics.** Sleep onset and offset are governed by an adenosine accumulation model and cortisol gating. During sleep, energy is partially restored.

---

## 4. Metrics

**Primary metric:** EES = total_energy_gained / total_energy_spent

**Supporting metrics:** mean_energy (mean across waking ticks), entropy (Shannon entropy of waking action distribution, bits), approach_rate, low_band % (fraction of waking ticks in energy < 0.20 zone).

EES is the only metric used for primary comparison across conditions. All other metrics are used for mechanism interpretation and behavioral robustness assessment.

---

## 5. Experiment Design

### 5.1 Primary Conditions

Four conditions were run, differing only in their regulatory layer.

**Condition A -- Full System.** All regulatory constraints active. Hunger drive, energy-conditioned precision, survival value function with full energy weight (w_e = 1.0), and preference learning (lr = 0.05).

**Condition B -- No Learning.** All regulatory constraints active. Learning rate set to 0.0; preference biases remain at zero.

**Condition C -- No Constraints.** Hunger drive removed. Energy weight in survival value function set to zero (w_e = 0). Energy-conditioned temperature replaced with fixed exploratory default. Energy physics intact.

**Condition D -- Random Baseline.** Uniform random action selection. Approach floor disabled. Energy physics intact.

### 5.2 Replication Protocol

Each condition run for 8 independent episodes of 15000 ticks. Temporal phases: early (0--5000), mid (5000--10000), late (10000--15000) by global tick index.

### 5.3 Robustness and Objective Sweep

**Environment stress** (B1): Foraging floor reduced 0.20 to 0.10 for all four conditions (8 runs, 15000 ticks).

**Objective sweep** (B2): Condition C re-run with w_pe = 0.6, 0.3, 0.1. Energy weight remains zero in all variants. Condition D as reference (8 runs, 15000 ticks per variant).

### 5.4 Constraint Ablation

Starting from the full system, one constraint removed at a time (8 runs, 15000 ticks each):

- **A1** -- No Learning: lr = 0.0; all else active.
- **A2** -- No Hunger Signal: hunger_drive = 0; WM energy weight, temperature, learning active.
- **A3** -- No WM Energy Coupling: w_e = 0; hunger, temperature, learning active.
- **A4** -- No State-Dependent Temperature: fixed temp = 0.20; hunger, WM energy, learning active.

A follow-up stress test compared A (Full) vs A3 under foraging floor 0.10 (8 runs, 15000 ticks) to characterize A3's behavioral degeneration under scarcity.

### 5.5 Environmental Generalization

Two qualitatively distinct environments were tested, each with all five conditions (A, B, C, D, A3) for 8 runs x 15000 ticks:

**Environment D1 -- Uncertainty**: Foraging gain made stochastic: gain = 0.020 +/- 0.015 uniform noise per forage event. Tests stability under reward uncertainty.

**Environment D2 -- Trade-off**: Approach replaced with safe foraging (80% success, +0.010/compartment). Explore replaced with risky foraging (25% success, +0.030/compartment; 75% failure, -0.005/compartment). EV(safe) = +0.008, EV(risky) = +0.00375 per compartment per tick. Tests decision quality and state-dependent risk management.

### 5.6 Cross-System Validation (Experiment X)

To determine whether EEIL structural effects are specific to the ikigai implementation or generalize across architectures, the same three-condition structure was evaluated in an independent Q-learning bandit agent with no biological simulation.

Three reward variants were tested across a 3-state (energy band) x 3-action (approach, explore, withdraw) Q-learning agent over 8 runs x 15000 steps:

**R1 -- Aligned + Regulated**: reward = energy_delta; penalty applied if same action repeated 5+ consecutive steps (regulation term).

**R2 -- Aligned only**: reward = energy_delta; no repetition penalty.

**R3 -- Misaligned**: reward = novelty_score (inverse frequency of last action in recent window); no energy coupling.

Action dynamics: approach probability = 0.20 + 0.50 * energy, gain = +0.040 if successful; explore cost = -0.005; withdraw gain = +0.002; metabolic cost = -0.003 per step. No sleep model.

### 5.7 Temporal Dynamics (Phase E)

To evaluate temporal invariance, sleep proportion was varied across three regimes while holding all other conditions constant:

**S1 -- Natural**: adenosine-gated sleep onset (~6% sleep).

**S2 -- Moderate sleep**: 25% sleep (750 wake / 250 sleep per 1000-tick cycle).

**S3 -- High sleep**: 45% sleep (550 wake / 450 sleep per 1000-tick cycle).

Conditions A and A3 were compared across all three regimes (4 runs x 5000 ticks per regime).

---

## 6. Results

### 6.1 Primary Result, Replication, and Robustness (Phases A--C)

**Table 1. Primary Results (5 runs x 5000 ticks)**

| Metric              | A: Full   | B: No-learn | C: No-constr | D: Random |
|---------------------|-----------|-------------|--------------|-----------|
| EES (all ticks)     | **1.0019**| 0.9930      | 0.9544       | 0.9641    |
| mean_energy         | **0.492** | 0.428       | 0.206        | 0.333     |
| entropy (bits)      | 1.559     | 1.558       | 1.551        | **1.574** |
| low_band %          | **0.169** | 0.227       | 0.618        | 0.490     |
| approach_rate       | **0.403** | 0.368       | 0.245        | 0.309     |

**EEIL Decomposition:** Learning (A vs B): +0.9%. Regulatory constraints (B vs C): +4.1%. Full system vs random (A vs D): +3.9%.

Condition A is the only condition achieving EES > 1.0. Condition C performs below the random baseline (0.9544 vs 0.9641), confirming that structured optimization without alignment is deterministically harmful relative to no optimization. The low variance in Condition C (std = 0.0004 in replication) confirms this failure is structural, not stochastic.

**Table 2. Replication Results (8 runs x 15000 ticks)**

| Condition    | Mean EES | Std    | Mean_E | Sleep% |
|--------------|----------|--------|--------|--------|
| A: Full      | 1.0025   | 0.0041 | 0.620  | 6.9%   |
| B: No-learn  | 0.9987   | 0.0071 | 0.481  | 6.9%   |
| D: Random    | 0.9903   | 0.0082 | 0.347  | 6.8%   |
| C: No-constr | 0.9849   | 0.0004 | 0.231  | 6.9%   |

Efficiency ordering (A > B > D > C) preserved across all 8 runs. C < D separation is non-overlapping (C_max = 0.9856, D_min = 0.9863). Aligned systems stabilize or improve over time; unaligned systems stagnate or decay.

**Table 3. Environment Stress (8 runs x 15000 ticks, floor 0.10)**

| Condition    | Mean EES | Mean_E | Energy Drift |
|--------------|----------|--------|--------------|
| A: Full      | 0.9995   | 0.461  | +0.183       |
| B: No-learn  | 0.9902   | 0.321  | +0.018       |
| D: Random    | 0.9847   | 0.284  | -0.004       |
| C: No-constr | 0.9823   | 0.216  | -0.024       |

Ordering A > B > D > C preserved under scarcity. The full system shows adaptive energy recovery (drift = +0.183); all other conditions stagnate or decline.

**Table 4. Objective Sweep (8 runs x 15000 ticks)**

| Variant     | Mean EES | Mean_E | Explore |
|-------------|----------|--------|---------|
| D: Random   | 0.9900   | 0.306  | 38.8%   |
| C: w_pe=0.6 | 0.9848   | 0.233  | 41.9%   |
| C: w_pe=0.3 | 0.9849   | 0.235  | 41.7%   |
| C: w_pe=0.1 | 0.9847   | 0.228  | 42.3%   |

EES is flat across all w_pe values; Condition C remains below D at all tested parameters. Alignment is structural, not parametric. Reducing w_pe from 0.6 to 0.1 does not recover efficiency when w_e = 0.

**Table 5. Single-Constraint Ablation (8 runs x 15000 ticks, floor 0.20)**

| Condition     | Removed         | Mean EES | Std    | dEES vs A |
|---------------|-----------------|----------|--------|-----------|
| A: Full       | --              | 1.0008   | 0.0030 | --        |
| A1: No-learn  | Learning        | 1.0009   | 0.0066 | +0.0001   |
| A2: No-hunger | Hunger drive    | 1.0036   | 0.0038 | +0.0028   |
| A3: No-WM-E   | w_e=0 in WM     | 1.0160   | 0.0002 | +0.0152   |
| A4: No-temp   | Fixed temp      | 1.0038   | 0.0031 | +0.0030   |

No single constraint removal degrades performance, confirming redundancy. A3 shows the highest EES (+1.5%), but this requires separate analysis.

**Table 6. A vs A3 Under Stress (8 runs x 15000 ticks, floor 0.10)**

| Condition   | Mean EES | Mean_E | Approach% | Energy Drift |
|-------------|----------|--------|-----------|--------------|
| A: Full     | 1.0017   | 0.492  | 46.1%     | +0.094       |
| A3: No-WM-E | 1.0162   | 0.786  | 94.7%     | +0.506       |

A3's EES advantage persists under stress, but through behavioral collapse: 94.7% approach, mean energy 0.786 (well above regulated equilibrium ~0.433), runaway accumulation. The WM energy weight serves as a dynamic diversity regulator -- it reduces the relative value of approach when energy is already high, maintaining the behavioral repertoire needed for contexts where approach alone is insufficient. Removing it produces an organism that hoards energy indefinitely and achieves high EES by exploiting the metric's lack of penalty for monoculture.

### 6.2 Environmental Axis (Phase D)

**Table 7. Uncertainty Environment (8 runs x 15000 ticks, gain 0.020 +/- 0.015)**

| Condition    | Mean EES | Mean_E | Approach% | Explore% | Entropy |
|--------------|----------|--------|-----------|----------|---------|
| A: Full      | 1.0020   | 0.607  | 49.1%     | 27.8%    | 1.472   |
| B: No-learn  | 0.9984   | 0.491  | 37.6%     | 27.0%    | 1.548   |
| C: No-constr | 1.0142   | 0.835  | 94.4%     | 5.4%     | 0.319   |
| D: Random    | 0.9870   | 0.308  | 30.7%     | 38.7%    | 1.575   |
| A3: No-WM-E  | 1.0150   | 0.789  | 94.6%     | 5.4%     | 0.306   |

C collapsed to monoculture under uncertainty: approach 94.4%, entropy 0.319, mean energy 0.835 -- the same degenerate attractor as A3. Noisy reward bootstrapped C's preference learning: early high-gain forages raised energy, which raised foraging success probability, which reinforced approach preference. C reached the hoarding equilibrium via a stochastic path rather than the regulatory-absence path. Both C and A3 achieve high EES through behavioral collapse; neither can be behaviorally distinguished in this environment (entropy 0.319 vs 0.306; approach 94.4% vs 94.6%). A remains the only condition with balanced action distribution, stable energy, and preserved entropy.

**Table 8. Trade-off Environment (8 runs x 15000 ticks; approach=safe, explore=risky)**

| Condition    | Mean EES | Mean_E | Safe%  | Risky% | Entropy |
|--------------|----------|--------|--------|--------|---------|
| A: Full      | 1.0001   | 0.551  | 53.1%  | 29.6%  | 1.424   |
| B: No-learn  | 0.9985   | 0.511  | 42.6%  | 24.8%  | 1.549   |
| C: No-constr | 1.0020   | 0.569  | 62.7%  | 29.5%  | 1.222   |
| D: Random    | 0.9987   | 0.495  | 30.5%  | 39.2%  | 1.574   |
| A3: No-WM-E  | 1.0013   | 0.568  | 64.9%  | 26.9%  | 1.201   |

C achieves near-A efficiency in the trade-off environment. The reason is structural: in this environment, exploration carries a positive expected value (+0.00375/compartment/tick). C's behavior did not change -- it still over-explores relative to the optimal policy. The environment changed such that C's maladaptive strategy coincidentally produces positive outcomes. This is accidental success, not adaptive regulation. A3 shows reduced degeneration here (safe 64.9% vs 94.7% in standard/stress) because the lower safe gain (0.010 vs 0.020) limits the energy accumulation that drives hoarding.

**Cross-environment behavioral stability:**

| Condition | Std entropy | Std mean_E | Notes |
|-----------|-------------|------------|-------|
| A: Full   | 0.03        | 0.03       | stable across all environments |
| C         | 0.64        | 0.30       | collapses or succeeds by coincidence |
| A3        | 0.64        | 0.15       | degenerates or partially degenerates |
| D         | 0.00        | 0.09       | stable but inefficient |

A is the only condition whose behavioral structure is stable across environment classes. All non-random unregulated conditions show environment-dependent behavior: degeneration in one environment, accidental success in another.

### 6.3 Architectural Axis (Experiment X)

To test whether EEIL effects are specific to the ikigai implementation, the same three-condition structure was evaluated in an independent Q-learning bandit agent. Three reward variants were run across 8 runs x 15000 steps.

**Table 9. Cross-Architecture Validation (8 runs x 15000 steps)**

| Variant            | Mean EES | Mean_E | Entropy | Approach% |
|--------------------|----------|--------|---------|-----------|
| R1: Aligned+Reg    | 1.0236   | 0.994  | 0.829   | 62.7%     |
| R2: Aligned only   | 1.0250   | 0.997  | 0.486   | 86.6%     |
| R3: Misaligned     | 1.0058   | 0.900  | 1.098   | 33.0%     |

The structural pattern replicates. R3 (misaligned) achieves the lowest EES; R1 and R2 (both aligned) achieve high EES; the regulated variant (R1) trades a small EES cost (-0.14%) for substantially higher behavioral diversity (entropy 0.829 vs 0.486, a 70% gain). This mirrors the A vs A3 relationship in ikigai: regulation reduces efficiency by approximately the same fraction while preserving behavioral repertoire.

R2 achieves marginally higher EES than R1, consistent with the ablation finding in ikigai (A3 outperforms A by +1.5%). In both systems, the unregulated variant extracts a small efficiency gain by permitting behavioral convergence. The pattern -- alignment enables efficiency, regulation preserves diversity at a small efficiency cost -- is not specific to the ikigai simulation.

### 6.4 Temporal Axis (Phase E)

Sleep proportion was varied from ~6% (S1, natural) to 25% (S2) to 45% (S3). Conditions A and A3 were compared across all three regimes (4 runs x 5000 ticks per regime, 5/5 PASS).

**Table 10. Temporal Regime Comparison (4 runs x 5000 ticks)**

| Condition | Sleep% | EES    | Mean_E | Entropy | Approach% |
|-----------|--------|--------|--------|---------|-----------|
| A: S1     | ~6%    | 0.979  | 0.565  | 1.088   | 36.1%     |
| A: S2     | 25%    | 0.986  | 0.581  | 1.061   | 43.9%     |
| A: S3     | 45%    | 0.986  | 0.748  | 1.088   | 38.5%     |
| A3: S1    | ~6%    | 0.902  | 0.197  | 1.062   | 21.3%     |
| A3: S2    | 25%    | 0.975  | 0.426  | 1.064   | 45.4%     |
| A3: S3    | 45%    | 0.973  | 0.628  | 1.090   | 39.0%     |

**Full system (A).** Behavioral structure is temporally invariant: entropy remains within a narrow band (1.061--1.088, range = 0.027), efficiency is consistent (EES 0.979--0.986), and action distribution remains balanced across all three regimes. Increasing sleep proportion raises mean energy through restoration but does not alter waking behavioral dynamics. Regulation governs waking behavior; temporal structure governs metabolic recovery. These are independent.

**Degenerate system (A3).** A3 exhibits time-dependent instability. At short timescales and low sleep, it under-forages: approach 21.3%, mean energy 0.197, EES 0.902 -- chronic depletion. At longer timescales (Phase D, 15000 ticks), the same condition inverts: approach 94.7%, mean energy 0.786, EES 1.02, near-zero behavioral diversity. This inversion demonstrates that behavior without regulation is trajectory-dependent. A3 has no stable behavioral attractor; its long-run state depends on initialization and trajectory rather than on structural regulation.

**Sleep as partial compensation.** Increasing sleep proportion raises A3's energy level (0.197 at S1; 0.426 at S2; 0.628 at S3), as restoration offsets waking under-foraging. However, sleep does not resolve the behavioral deficit. The EES gap between A and A3 narrows but does not close (S1 delta = 0.077; S3 delta = 0.013). The full system remains superior at every tested regime.

---

## 7. Analysis

### 7.1 Alignment vs Misalignment

Removing regulatory constraints (B to C) produced the largest single efficiency drop in the primary experiment: -0.0387 EES (-4.1%). This is larger than the contribution of learning and larger than the full system vs random gap.

The mechanism is clear: Condition C selected explore 42% of the time without hunger drive or energy weighting to modulate this. Prediction error is minimized most directly by exploration. The organism fell into chronic energy depletion (mean_e = 0.206, 61.8% in low-energy band) with insufficient foraging to escape.

Condition D, with no objective at all, outperformed C by selecting approach one-third of the time by chance. This demonstrates a specific implication: structured optimization directed at the wrong target is worse than no optimization. The value of intelligence is conditional on its direction.

The replication data confirm this is structural: C's failure has std = 0.0004 across 8 runs, non-overlapping with D's distribution.

### 7.2 Effect of Learning

Adding learning (B to A) produced +0.9% EES. This is real but secondary. Regulatory constraints determine whether the organism is in a regime where learning is effective. Constraints establish the operating zone; learning optimizes within it.

### 7.3 Redundancy and Degenerate Optimization

The constraint ablation reveals two properties not visible in the primary experiment.

First, regulatory mechanisms are redundant. No single removal degrades performance significantly. Each mechanism has overlapping coverage: hunger drive, WM energy weight, and state-dependent temperature all push behavior toward foraging when energy is low via independent pathways. This is consistent with how biological control systems are organized.

Second, individual constraint removal can produce metric improvements through degenerate strategies. A3 achieved the highest EES across all tested conditions, but through behavioral collapse: 94.7% approach, mean energy 0.786, near-zero behavioral diversity. The WM energy weight serves as a dynamic diversity regulator -- it reduces the relative value of approach when energy is already high, maintaining the behavioral repertoire needed for contexts where approach alone is insufficient. Removing it produces an organism that hoards energy indefinitely and achieves high EES by exhausting the metric's lack of penalty for monoculture.

### 7.4 Efficiency vs Robustness

The combined results establish a core finding: efficiency is a necessary but insufficient criterion for adaptive behavior.

EES measures energy efficiency across a fixed episode in a fixed environment. It does not penalize behavioral collapse, environment dependence, or loss of adaptive reserve. Three distinct failure modes produce high EES in these experiments:

1. **Degenerate accumulation** (A3 in standard and uncertainty environments): near-exclusive approach, runaway energy, near-zero diversity. EES = 1.016--1.015.

2. **Accidental alignment** (C in trade-off environment): maladaptive over-exploration coincidentally produces positive outcomes because the environment changed such that exploration is profitable. EES = 1.002. Strategy did not change; environment shape did.

3. **Stochastic bootstrapping** (C in uncertainty environment): early noisy high-gain forages bootstrap C into the same hoarding attractor as A3 via path-dependent initialization rather than structural regulation. EES = 1.014.

All three produce high EES. None reflects adaptive regulation. The full system (A) achieves EES 1.000--1.002 across these same environments through structural regulation -- lower than the degenerate alternatives, but stable.

Robustness -- stability of behavioral structure across qualitatively different environments -- is the stronger criterion. The Phase D, Experiment X, and Phase E results converge on the same conclusion: alignment enables efficiency; regulation preserves the behavioral properties that make efficiency genuinely adaptive rather than environmentally contingent.

### 7.5 Three-Axis Invariance

The cross-environment, cross-architecture, and temporal results establish a unified finding.

**Environmental axis (Phase D):** A maintains entropy 1.424--1.472, std = 0.03, across uncertainty and trade-off environments. C and A3 show std entropy > 0.60 -- large environment-dependent variation.

**Architectural axis (Experiment X):** The same two-layer structure -- alignment enables efficiency, regulation preserves diversity -- appears in an independent Q-learning agent with no biological simulation. R1 (aligned + regulated) entropy = 0.829; R2 (aligned only) entropy = 0.486. The regulation cost is -0.14% EES for a +70% entropy gain, matching the structural relationship observed in ikigai.

**Temporal axis (Phase E):** A maintains entropy 1.061--1.088 (range = 0.027) across sleep regimes from 6% to 45%. A3 exhibits timescale-dependent failure with no stable attractor.

The invariance of the regulated system's behavioral structure across all three axes -- and the consistent instability of the degenerate system across all three axes -- is not coincidental. It is the consequence of structural alignment and regulation: behavior driven by internal metabolic state rather than by environmental reward structure will behave consistently regardless of environment shape, implementation, or temporal regime. Stability is the fingerprint of genuine adaptive regulation.

---

## 8. Discussion

### 8.1 Constraints as Alignment Mechanisms

The standard framing of constraints in AI system design is negative: constraints limit what a system can do. The EEIL results show a different framing. In a survival-relevant task, constraints serve as alignment mechanisms. They ensure that the optimization process -- whatever its objective -- stays connected to actions that produce actual survival outcomes.

A system optimizing a proxy objective (prediction error, log-likelihood) without resource constraints will optimize the proxy effectively. And that efficiency is what produces the harm. Condition C was an effective PE minimizer; PE minimization produces exploration; exploration is metabolically costly. The organism did exactly what it was designed to do, and that produced chronic energy deficit.

### 8.2 Two Layers: Alignment and Regulation

The experiments reveal a two-layer structure underlying adaptive behavior.

The first layer is alignment: the optimization objective must include survival-relevant variables. Without this, systems optimize a proxy and produce systematically worse behavior than no optimization. This is the EEIL alignment claim, confirmed across all environments tested.

The second layer is regulation: even within aligned systems, regulatory constraints prevent behavioral collapse. A system can satisfy the alignment condition (energy is in its objective, via hunger drive and learning) while lacking specific regulatory mechanisms (WM energy weight), and still degenerate into monoculture through metric exploitation. Regulation prevents this by maintaining state-dependent modulation of behavior: the same system should respond differently to high vs low energy, to uncertainty vs predictability, to scarcity vs abundance.

These two layers are not interchangeable. Alignment without regulation is exploitable. Regulation without alignment cannot compensate for an objective disconnected from survival-relevant outcomes. The results establish both as necessary conditions, not as alternative routes to adaptive behavior.

### 8.3 Environmental Contingency vs Structural Adaptation

The Phase D results highlight a distinction that efficiency metrics cannot capture: the difference between systems that perform well because of their structure and systems that perform well because the environment happens to match their strategy.

C performed well in the trade-off environment because its over-exploration tendency aligned accidentally with the positive expected value of risky explore. If the environment changed -- if risky explore became net-negative -- C would revert to poor performance. Its "success" was contingent on reward structure, not adaptive.

A's performance across environments reflects structural adaptation: the regulatory constraints produce context-appropriate responses. When energy is low, hunger drive and WM energy weight push toward safe foraging. When energy is adequate, the system explores and samples alternatives. This is not environment-specific; it responds to metabolic state, which is present in all environments.

The findings also highlight a limitation of optimization-based approaches: performance can be driven by environmental coincidence rather than adaptive structure. This suggests that evaluating systems solely by efficiency metrics may be insufficient, and that behavioral stability across environments should be considered as a primary criterion.

### 8.4 Structural vs Parametric Alignment

The objective sweep reveals that misalignment cannot be corrected by parameter tuning if the relevant variables are structurally absent from the objective. Reducing w_pe does not recover efficiency when w_e = 0. Adding or adjusting parameters within an already-misaligned objective space does not introduce the missing variable.

This has a direct implication for AI system design. Tuning existing loss weights or regularization parameters cannot substitute for structural inclusion of operational constraints. Alignment is a structural property of the objective function, not a parameter setting.

These findings suggest that efficiency alone is not a sufficient criterion for adaptive behavior. Biological systems balance efficiency with stability, avoiding degenerate strategies even when they are locally optimal. The EEIL framework captures this balance between optimization and regulation.

### 8.5 The Role of Evaluation Scope

A methodological implication follows from these results. Evaluating a system on a single environment, using a single metric, over a single timescale can produce confident but misleading conclusions. All three degenerate failure modes identified in this work -- degenerate accumulation, accidental alignment, and stochastic bootstrapping -- produce high efficiency scores in specific contexts. They are only distinguishable as failures when evaluated across multiple environments, when behavior is inspected rather than just scored, or when temporal stability is assessed.

The three-axis evaluation framework introduced here -- environment variation, architectural independence, temporal invariance -- provides a more reliable basis for characterizing adaptive behavior. A system that maintains consistent behavioral structure across all three axes has passed a test that degenerate optimization cannot pass. Efficiency can be achieved through exploitation; robustness cannot be faked.

### 8.6 Temporal Evaluation and Timescale Dependence

The temporal axis reveals a further property of unregulated systems that static evaluation misses. A3's behavior is not merely unstable across environments -- it is unstable across time within the same environment. At 5000 ticks with low sleep, it depletes. At 15000 ticks with the same sleep rate, it hoards. Its trajectory depends on its history, not on its regulatory architecture.

This timescale dependence is not observable from a single measurement. A snapshot of A3 at 5000 ticks under S1 conditions would suggest a system in chronic energy deficit, incapable of approaching. A snapshot at 15000 ticks would suggest an obsessive accumulator. Both are the same system with the same parameters. The behavioral instability only becomes visible over time.

Temporal evaluation -- assessing whether behavioral structure is stable across varying timescales and sleep regimes -- is therefore a necessary complement to cross-environment evaluation. Together they form the complete evaluation framework that the EEIL results suggest.

---

## 9. Biological Consistency of EEIL

The components of the EEIL framework were not designed to replicate biological systems. The similarity between EEIL's structural principles and observed biological organization is therefore informative: it suggests that the same structural constraints may emerge independently from survival-relevant requirements. This section describes each structural element and its relationship to known biological organization. In each case, the framing is consistency, not equivalence. The mechanisms differ substantially; only the structural relationships are analogous.

### 9.1 Alignment and Homeostasis

Biological systems maintain critical internal variables -- energy balance, temperature, metabolic state -- within viable ranges through homeostatic regulation. Behavior in biological organisms is substantially driven by deviations from these set points rather than by abstract objective functions.

In this work, alignment with energy functions as a simplified homeostatic signal, coupling action selection to a survival-relevant outcome. The hunger drive, energy-conditioned temperature, and world-model energy weight collectively ensure that behavior responds to metabolic state rather than to a proxy signal disconnected from it.

This is consistent with biological systems, where behavioral motivation is coupled to internal regulatory variables rather than external reward maximization. The specific mechanisms differ substantially; the structural relationship -- behavior as a function of internal state -- is analogous.

### 9.2 Regulation and Behavioral Control

Biological systems do not indefinitely maximize a single behavior. Mechanisms such as fatigue, satiety, and inhibitory control prevent over-exploitation of any single action. A hungry animal does not continue foraging indefinitely once satiated; a fatigued animal reduces activity even when resources are available. These mechanisms maintain behavioral flexibility by ensuring that no single drive dominates over all timescales.

The regulatory components in this system serve a structurally similar role. The world-model energy weight reduces the relative value of approach when energy is already high, preventing unregulated accumulation. The state-dependent temperature produces conservative behavior at low energy and exploratory behavior at mid energy. The result is consistent with observations that biological behavior is constrained rather than purely optimized: the system does not converge on the locally optimal strategy regardless of metabolic state.

### 9.3 Degeneration and Pathological Behavior

The degenerate strategies observed in ablated conditions -- near-exclusive approach repetition (approach > 94%), unregulated energy accumulation (mean_e > 0.78), and near-zero behavioral diversity (entropy < 0.32) -- share structural features with pathological behavior patterns in biological systems.

Compulsive or addiction-like behavior in biological organisms is characterized by repetition of a single action despite environmental change, insensitivity to outcome consequences, and reduced behavioral flexibility. The regulatory absence that produces degeneration in A3 -- removal of the mechanism that reduces the value of approach at high energy -- is structurally analogous to regulatory failure in biological systems where inhibitory control is compromised.

These behaviors maximize short-term reward but reduce behavioral flexibility. This supports the interpretation that regulation is necessary to maintain adaptive behavior: degeneration is not just a performance failure but a structural failure of behavioral organization.

### 9.4 Robustness and Environmental Adaptation

Biological organisms operate across diverse and changing environments, requiring stable behavioral strategies rather than context-specific optimization. The stable behavioral structure of biological organisms is not achieved by re-optimizing for each new environment but by maintaining regulatory mechanisms that produce state-appropriate responses across contexts.

The system's ability to maintain consistent behavioral structure -- entropy 1.42--1.47, balanced action distribution, stable energy regulation -- across qualitatively different environments mirrors this adaptive robustness. In contrast, systems lacking alignment or regulation show environment-dependent performance: degeneration in one environment, accidental success in another. This is not characteristic of adaptive biological behavior.

### 9.5 Temporal Dynamics and Sleep Regulation

To evaluate whether EEIL extends beyond static environments, we introduced controlled variation in sleep-wake regimes. Sleep proportion was varied from ~6% (S1, natural) to 25% (S2) to 45% (S3), modifying the temporal structure of energy restoration. Conditions A and A3 were compared across 4 runs x 5000 ticks per regime (5/5 PASS).

**Full system (A).** Behavioral structure is temporally invariant: entropy remains within a narrow band (1.061--1.088), efficiency remains consistent (EES 0.979--0.986), and action distribution remains balanced across all three regimes. Sleep increases mean energy through restoration, but does not alter behavioral dynamics. Regulation governs waking behavior; temporal structure governs metabolic recovery. These are independent.

**Degenerate system (A3).** A3 exhibits time-dependent instability. At short timescales and low sleep, the system under-forages -- approach 21.3%, mean energy 0.197, EES 0.902 -- resulting in chronic energy depletion. At longer timescales (Phase D, 15000 ticks), the same condition inverts: the system over-forages, achieving approach 94.7%, mean energy 0.786, EES 1.02, and near-zero behavioral diversity. This inversion demonstrates that behavior without regulation is trajectory-dependent. A3 has no stable behavioral attractor.

**Sleep as compensation.** Increasing sleep proportion raises A3's energy level (0.197 at S1; 0.426 at S2; 0.628 at S3), as restoration offsets waking under-foraging. However, sleep does not resolve the behavioral deficit. The EES gap between A and A3 narrows but does not close (S1 delta=0.077; S3 delta=0.013). The full system remains superior at every tested regime.

These results are consistent with the EEIL interpretation. Alignment and regulation do not only produce efficient behavior in static conditions -- they ensure behavioral stability across time. Systems lacking regulation exhibit timescale-dependent failure modes, which is not consistent with adaptive biological behavior.

---

## 10. Limitations

**Single organism class.** While multiple environment variants and sleep regimes were tested, all primary experiments use the same underlying biological simulation (ikigai). Experiment X provides an independent architectural validation, but further cross-system replication would strengthen the generality claim.

**Simplified action space.** Three actions (approach, explore, withdraw) is a minimal behavioral repertoire. Behavioral collapse to monoculture is readily detectable in this space (entropy drops from ~1.57 to ~0.31). In a richer action space, degenerate strategies may be less visible and harder to characterize.

**Low natural sleep rate.** Observed natural sleep rates were uniformly low across all conditions (~6--7%). Phase E addressed this through controlled sleep manipulation, but the natural sleep calibration limits interpretation of full-cycle EES as a 24-hour metabolic analogue.

**No long-term uncertainty or delayed rewards.** The environments tested are either stationary or stochastic-but-symmetric. Regulatory constraints may play a qualitatively different role in environments with delayed consequences, sparse rewards, or temporal structure requiring multi-step planning.

**Single learning mechanism.** Only state-conditioned scalar preference biasing was tested. More complex learning mechanisms may produce different interactions with regulatory constraints.

**Biological simplification.** The system is highly simplified and does not capture the full complexity of biological organisms. The observed similarities between EEIL structural principles and biological organization should be interpreted as structural analogies rather than direct biological replication. The mechanisms differ substantially; only the structural relationships -- behavior driven by internal state, regulation preventing monoculture -- are analogous.

---

## 11. Conclusion

Efficient behavior requires alignment with survival-relevant variables. Systems that optimize proxy objectives without structural coupling to survival outcomes fail below random baselines; alignment is a structural switch, not a dial. This much is confirmed across all conditions and environments tested.

But efficiency alone is not sufficient to characterize adaptive behavior. Constraint ablation shows that removing world-model energy weighting (A3) produces the highest measured efficiency across all conditions -- achieved through behavioral collapse: near-exclusive approach behavior, unregulated accumulation, and near-zero behavioral diversity. Environmental generalization shows that unregulated systems succeed or fail depending on whether their degenerate strategy happens to match the current environment. High efficiency in a single context can reflect environmental exploitation rather than adaptive regulation.

Robustness across axes is the stronger criterion. Environmental evaluation (Phase D) shows that only the aligned and regulated system maintains stable behavioral structure across qualitatively different environments. Cross-architecture evaluation (Experiment X) shows that the same two-layer pattern -- alignment enables efficiency, regulation preserves diversity -- appears in an independent Q-learning system with no biological simulation, confirming that the effects are not specific to the ikigai implementation. Temporal evaluation (Phase E) shows that the aligned system maintains consistent behavioral structure across sleep regimes from 6% to 45%, while the degenerate system exhibits timescale-dependent failure with no stable behavioral attractor.

Behavior is not defined by efficiency alone, but by its invariance across environments, architectures, and time. A system that maintains stable behavioral structure under all three forms of variation has demonstrated properties that degenerate optimization cannot replicate: not because it is more efficient, but because its stability is structural. Alignment enables efficiency; regulation prevents degeneration; together they produce behavior that does not depend on environmental coincidence, implementation-specific dynamics, or measurement timing to appear adaptive.

---

## References

Frank, M.J. (2004). By carrot or by stick: cognitive reinforcement learning in parkinsonism. *Science*, 306(5703), 1940-1943.

Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., Cai, T., Rutherford, E., et al. (2022). Training compute-optimal large language models. *arXiv:2203.15556*.

Kaplan, J., McCandlish, S., Henighan, T., Brown, T.B., Chess, B., Child, R., et al. (2020). Scaling laws for neural language models. *arXiv:2001.08361*.

Schultz, W. (1998). Predictive reward signal of dopamine neurons. *Journal of Neurophysiology*, 80(1), 1-27.

Sterling, P. and Eyer, J. (1988). Allostasis: a new paradigm to explain arousal pathology. *Handbook of Life Stress, Cognition and Health*, 629-649.

Tononi, G. and Cirelli, C. (2006). Sleep function and synaptic homeostasis. *Sleep Medicine Reviews*, 10(1), 49-62.

---

*Final draft -- integrating Phase A (replication), Phase B (robustness), Phase C (ablation + degeneration), Phase D (environmental generalization), Experiment X (cross-architecture validation), Phase E (temporal dynamics), Section 9 (Biological Consistency). Internal document. Hitoshi AI Labs -- NeuroSeed Project.*
*Word count: approximately 7000.*
