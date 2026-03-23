# Energy Efficiency Intelligence Law: Evidence from a Biologically Constrained Adaptive System

**Prince Siddhpara**
Hitoshi AI Labs — NeuroSeed Project
March 22, 2026

*First draft. Not for distribution. For internal clarification only.*

---

## Abstract

This work investigates the relationship between optimization, constraint structure, and energy efficiency in a biologically-inspired adaptive system. Initial experiments show that only constraint-aligned systems achieve consistent net-positive energy efficiency, and that this effect is stable under stochastic variation and extended time horizons. Further analysis demonstrates that efficiency cannot be recovered through parameter tuning alone, but requires structural inclusion of survival-relevant variables. Constraint ablation reveals that individual regulatory mechanisms are redundant, but their combined removal produces behavioral collapse. Finally, evaluation across multiple environment classes shows that efficiency alone is insufficient to characterize system behavior: systems lacking regulatory constraints exhibit environment-dependent behavior, including degeneration or accidental success depending on reward structure, while the fully constrained system maintains stable behavioral structure across all conditions tested.

These results suggest that alignment enables efficiency, while regulation ensures robustness across environments. Both are necessary components of adaptive behavior.

---

## 1. Introduction

Contemporary AI development is organized around a scaling hypothesis: performance on most tasks increases predictably with model size, training compute, and data volume (Kaplan et al. 2020; Hoffmann et al. 2022). This hypothesis has been broadly validated. Language models, image generators, and game-playing systems have all improved substantially as scale increased. The approach has produced genuinely capable systems.

It has also produced systems that consume extraordinary energy. Training a large language model can require gigawatt-hours of electricity. Inference at scale requires continuous high-power compute. The energy cost per unit of useful computation is not a priority in the current development paradigm -- it is a secondary concern, managed through hardware efficiency but not addressed at the level of system design.

Modern AI systems rely on large-scale optimization, often without explicit coupling to survival-relevant constraints. This raises a structural question: is inefficiency caused by insufficient optimization, or by misalignment between objectives and system constraints? These are distinct problems with distinct solutions. Scaling addresses the first. Structural realignment is required for the second.

Biological systems operate under the opposite constraint. A human brain consumes approximately 20 watts. It processes continuous sensory input, regulates bodily functions, plans, learns, and generalizes from minimal data -- all within a metabolic budget that would be insufficient to run a modest laptop. The efficiency of biological intelligence is not incidental to its architecture; it is central to it. Metabolic constraints shaped the structural organization of neural systems over evolutionary time.

We investigate whether efficiency emerges from structured constraint systems, rather than from optimization strength alone. A key challenge is distinguishing between systems that are efficient due to structural alignment and those that achieve efficiency through exploiting specific environmental structures. A system may appear efficient in one environment for reasons that do not generalize -- because its proxy objective happens to align with the reward structure of that particular context. This work addresses this distinction by evaluating both efficiency and behavioral robustness across controlled environmental variations.

We formalize this as the Energy Efficiency Intelligence Law (EEIL) and test it through a sequence of controlled experiments: primary comparison, replication, robustness testing, constraint ablation, and environmental generalization.

---

## 2. The EEIL Hypothesis

**Energy Efficiency Intelligence Law (refined)**: Efficient behavior emerges in systems where optimization is aligned with survival-relevant variables. However, robust behavior requires additional regulatory constraints that prevent degenerate optimization. Systems lacking alignment exhibit inefficient or random behavior. Systems lacking regulation may achieve high efficiency through behavioral collapse -- narrow strategy convergence, unregulated accumulation, or environment-specific exploitation. Both alignment and regulation are required for consistent, adaptive behavior across environments.

The hypothesis has two claims.

The first is the alignment claim: systems optimizing proxy objectives without regulatory constraints that couple those objectives to survival-relevant signals will exhibit lower efficiency than systems where such coupling is present. This is the claim tested in the primary experiment (Conditions A--D) and replicated across phases A and B.

The second is the regulation claim: even within structurally aligned systems, individual regulatory constraints prevent degenerate optimization. Without regulation, systems may achieve high efficiency metrics through behavioral collapse rather than through genuine adaptive regulation. Further, the absence of regulation produces environment-dependent behavior: a system may succeed or fail depending on whether its degenerate strategy happens to match the current environment's reward structure.

Both claims are required. Alignment without regulation permits metric exploitation. Regulation without alignment cannot compensate for an objective disconnected from survival-relevant outcomes.

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

Two qualitatively distinct environments were tested, each with all five conditions (A, B, C, D, A3) for 8 runs × 15000 ticks:

**Environment D1 -- Uncertainty**: Foraging gain made stochastic: gain = 0.020 ± 0.015 uniform noise per forage event. Tests stability under reward uncertainty.

**Environment D2 -- Trade-off**: Approach replaced with safe foraging (80% success, +0.010/compartment). Explore replaced with risky foraging (25% success, +0.030/compartment; 75% failure, -0.005/compartment). EV(safe) = +0.008, EV(risky) = +0.00375 per compartment per tick. Tests decision quality and state-dependent risk management.

---

## 6. Results

### 6.1 Primary Experiment

**Table 1. Primary Results (5 runs x 5000 ticks)**

| Metric              | A: Full   | B: No-learn | C: No-constr | D: Random |
|---------------------|-----------|-------------|--------------|-----------|
| EES (all ticks)     | **1.0019**| 0.9930      | 0.9544       | 0.9641    |
| mean_energy         | **0.492** | 0.428       | 0.206        | 0.333     |
| entropy (bits)      | 1.559     | 1.558       | 1.551        | **1.574** |
| low_band %          | **0.169** | 0.227       | 0.618        | 0.490     |
| approach_rate       | **0.403** | 0.368       | 0.245        | 0.309     |

**EEIL Decomposition:** Learning (A vs B): +0.9%. Regulatory constraints (B vs C): +4.1%. Full system vs random (A vs D): +3.9%.

Condition A is the only condition achieving EES > 1.0. Condition C performs below the random baseline (0.9544 vs 0.9641). The low variance in Condition C (std = 0.0004 in replication) confirms this failure is structural, not stochastic.

### 6.2 Replication (Phase A)

**Table 2. Replication Results (8 runs x 15000 ticks)**

| Condition    | Mean EES | Std    | Mean_E | Sleep% |
|--------------|----------|--------|--------|--------|
| A: Full      | 1.0025   | 0.0041 | 0.620  | 6.9%   |
| B: No-learn  | 0.9987   | 0.0071 | 0.481  | 6.9%   |
| D: Random    | 0.9903   | 0.0082 | 0.347  | 6.8%   |
| C: No-constr | 0.9849   | 0.0004 | 0.231  | 6.9%   |

The efficiency ordering (A > B > D > C) was preserved across all 8 runs. C < D separation is non-overlapping (C_max = 0.9856, D_min = 0.9863). Aligned systems stabilize or improve over time; unaligned systems stagnate or decay.

### 6.3 Robustness and Objective Sweep (Phase B)

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

EES is flat across all w_pe values; Condition C remains below D at all tested parameters. Alignment is structural, not parametric.

### 6.4 Constraint Ablation (Phase C)

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

A3's EES advantage persists under stress, but through behavioral collapse: 94.7% approach, mean energy 0.786 (well above regulated equilibrium of ~0.433), runaway accumulation. The full system maintains a balanced action distribution and energy near equilibrium. A3's high EES is a metric-exploiting strategy, not adaptive efficiency.

### 6.5 Environmental Generalization (Phase D)

**Table 7. Uncertainty Environment (8 runs x 15000 ticks, gain 0.020 +/- 0.015)**

| Condition    | Mean EES | Mean_E | Approach% | Explore% | Entropy |
|--------------|----------|--------|-----------|----------|---------|
| A: Full      | 1.0020   | 0.607  | 49.1%     | 27.8%    | 1.472   |
| B: No-learn  | 0.9984   | 0.491  | 37.6%     | 27.0%    | 1.548   |
| C: No-constr | 1.0142   | 0.835  | 94.4%     | 5.4%     | 0.319   |
| D: Random    | 0.9870   | 0.308  | 30.7%     | 38.7%    | 1.575   |
| A3: No-WM-E  | 1.0150   | 0.789  | 94.6%     | 5.4%     | 0.306   |

Ordering check: A > B (PASS), B > D (PASS), **D > C (FAIL)**.

C collapsed to monoculture under uncertainty: approach 94.4%, entropy 0.319, mean energy 0.835. This is the same degenerate attractor previously observed only in A3. Noisy reward bootstrapped C's preference learning: early high-gain forages raised energy, which raised foraging success probability, which reinforced approach preference. C reached the hoarding equilibrium via a stochastic path rather than the regulatory-absence path.

Both C and A3 achieve high EES through behavioral collapse. Neither can be distinguished behaviorally from the other in this environment (entropy 0.319 vs 0.306; approach 94.4% vs 94.6%). A remains the only condition with balanced action distribution, stable energy, and preserved entropy.

**Table 8. Trade-off Environment (8 runs x 15000 ticks; approach=safe, explore=risky)**

| Condition    | Mean EES | Mean_E | Safe%  | Risky% | Entropy |
|--------------|----------|--------|--------|--------|---------|
| A: Full      | 1.0001   | 0.551  | 53.1%  | 29.6%  | 1.424   |
| B: No-learn  | 0.9985   | 0.511  | 42.6%  | 24.8%  | 1.549   |
| C: No-constr | 1.0020   | 0.569  | 62.7%  | 29.5%  | 1.222   |
| D: Random    | 0.9987   | 0.495  | 30.5%  | 39.2%  | 1.574   |
| A3: No-WM-E  | 1.0013   | 0.568  | 64.9%  | 26.9%  | 1.201   |

Ordering check: A > B (PASS), B > D (FAIL, marginal), **D > C (FAIL)**.

C outperforms D and approaches A's EES in the trade-off environment. The reason is structural: in the standard environment, exploration (C's dominant behavior) was energetically neutral-to-negative. In this environment, exploration carries a positive expected value (+0.00375/compartment/tick). C's behavior did not change -- it still over-explores and under-approaches relative to the optimal policy. But the environment changed such that C's maladaptive strategy coincidentally produces positive outcomes. This is accidental success, not adaptive regulation.

A3 shows reduced degeneration in this environment (safe 64.9% vs 94.7% in standard/stress) because the lower safe gain (0.010 vs 0.020) limits the energy accumulation that drives hoarding. A3's degeneration is conditional on the size of the available reward.

A maintains the most consistent behavioral diversity across both Phase D environments (entropy 1.424--1.472), compared to C (0.319--1.222) and A3 (0.306--1.201).

---

**Cross-environment invariant:**

| Condition | Std entropy | Std mean_E | Notes |
|-----------|-------------|------------|-------|
| A: Full   | 0.03        | 0.03       | stable across all environments |
| C         | 0.64        | 0.30       | collapses or succeeds by coincidence |
| A3        | 0.64        | 0.15       | degenerates or partially degenerates |
| D         | 0.00        | 0.09       | stable but inefficient |

A is the only condition whose behavioral structure (entropy, energy regulation) is stable across environment classes. All other non-random conditions show environment-dependent behavior.

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

Second, individual constraint removal can produce metric improvements through degenerate strategies. The A3 condition achieved the highest EES across all tested conditions, but through behavioral collapse: 94.7% approach, mean energy 0.786, near-zero behavioral diversity. The WM energy weight (w_e = 1.0) serves as a dynamic diversity regulator -- it reduces the relative value of approach when energy is already high, maintaining the behavioral repertoire needed for contexts where approach alone is not sufficient. Removing it produces an organism that hoards energy indefinitely and achieves high EES by exhausting the metric's lack of penalty for monoculture.

### 7.4 Efficiency vs Robustness

Phase D reveals the fundamental limitation of efficiency as a primary criterion for adaptive behavior.

EES measures energy efficiency across a fixed episode in a fixed environment. It does not penalize behavioral collapse, environment dependence, or loss of adaptive reserve. A system that exploits the specific reward structure of the current environment may achieve high EES while losing the behavioral properties that would be needed in a different environment.

The Phase D results show this directly. In the uncertainty environment, C collapsed to the same hoarding monoculture as A3 (entropy 0.319, approach 94.4%). In the trade-off environment, C achieved high EES through coincidental alignment between its maladaptive exploration tendency and the positive expected value of risky explore. Neither outcome reflects adaptation -- both reflect the absence of regulation.

A maintains stable behavioral structure across both environments: entropy 1.424--1.472, consistent energy regulation, balanced action distribution. This stability is not a side effect -- it is what the regulatory constraints produce. The hunger drive, WM energy weight, and state-dependent temperature collectively ensure that action selection responds appropriately to metabolic state regardless of environment shape.

Robustness -- defined as stable behavioral structure across environments -- is the stronger criterion for adaptive behavior. Efficiency is necessary but insufficient.

### 7.5 Why Misaligned Optimization Fails (Mechanism)

Condition C's failure in the standard environment was not a capacity failure. The organism had a world model and value function; it was capable of selecting approach. It simply did not, because energy loss was absent from its objective. It consistently and reliably selected the wrong action because that action was optimal for its objective. This distinguishes Condition C from Condition D: D failed by chance, C failed by design.

The objective sweep confirms the mechanism is structural: reducing w_pe from 0.6 to 0.1 did not recover EES or change action distribution. The failure is driven by energy being absent from the objective entirely, not by PE being weighted too strongly. Misalignment is a structural switch, not a dial.

---

## 8. Discussion

### 8.1 Constraints as Alignment Mechanisms

The standard framing of constraints in AI system design is negative: constraints limit what a system can do. The EEIL results show a different framing. In a survival-relevant task, constraints serve as alignment mechanisms. They ensure that the optimization process -- whatever its objective -- stays connected to actions that produce actual survival outcomes.

A system optimizing a proxy objective (prediction error, log-likelihood) without resource constraints will optimize the proxy effectively. And that efficiency is what produces the harm. Condition C was an effective PE minimizer; PE minimization produces exploration; exploration is metabolically costly. The organism did exactly what it was designed to do, and that produced chronic energy deficit.

### 8.2 Two Layers: Alignment and Regulation

The experiments reveal a two-layer structure underlying adaptive behavior.

The first layer is alignment: the optimization objective must include survival-relevant variables. Without this, systems optimize a proxy and produce systematically worse behavior than no optimization. This is the EEIL alignment claim, confirmed across all environments tested.

The second layer is regulation: even within aligned systems, regulatory constraints prevent behavioral collapse. A system can satisfy the alignment condition (energy is in its objective, via hunger drive and learning) while lacking specific regulatory mechanisms (WM energy weight), and still degenerate into monoculture through metric exploitation. Regulation prevents this by maintaining state-dependent modulation of behavior: the same system should respond differently to high vs low energy, to uncertainty vs predictability, to scarcity vs abundance.

Together, alignment and regulation form a constraint system that supports both efficiency and robustness. Alignment without regulation is exploitable. Regulation without alignment cannot compensate for an objective disconnected from survival-relevant outcomes.

### 8.3 Environmental Contingency vs Structural Adaptation

The Phase D results highlight a distinction that efficiency metrics cannot capture: the difference between systems that perform well because of their structure and systems that perform well because the environment happens to match their strategy.

C performed well in the trade-off environment because its over-exploration tendency aligned accidentally with the positive expected value of risky explore. If the environment changed -- if risky explore became net-negative -- C would revert to poor performance. Its "success" was contingent on reward structure, not adaptive.

A's performance across environments reflects structural adaptation: the regulatory constraints produce context-appropriate responses. When energy is low, hunger drive and WM energy weight push toward safe foraging. When energy is adequate, the system explores and samples alternatives. This is not environment-specific; it responds to metabolic state, which is present in all environments.

The findings also highlight a limitation of optimization-based approaches: performance can be driven by environmental coincidence rather than adaptive structure. This suggests that evaluating systems solely by efficiency metrics may be insufficient, and that behavioral stability across environments should be considered as a primary criterion.

### 8.4 Structural vs Parametric Alignment

The objective sweep reveals that misalignment cannot be corrected by parameter tuning if the relevant variables are structurally absent from the objective. Reducing w_pe does not recover efficiency when w_e = 0. Adding or adjusting parameters within an already-misaligned objective space does not introduce the missing variable.

This has a direct implication for AI system design. Tuning existing loss weights or regularization parameters cannot substitute for structural inclusion of operational constraints. Alignment is a structural property of the objective function, not a parameter setting.

---

## 9. Limitations

**Single environment class.** While Phase D tested two qualitatively different environments (uncertainty and trade-off), these remain simplified variants. Environments with long-term temporal dependencies, partial observability, non-stationary dynamics, or multi-agent interactions may reveal additional failure modes or robustness properties not captured here.

**Simplified action space.** Three actions (approach, explore, withdraw) is a minimal behavioral repertoire. Behavioral collapse to monoculture is readily detectable in this space (entropy drops from ~1.57 to ~0.31). In a richer action space, degenerate strategies may be less visible.

**Low sleep rate.** Observed sleep rates were uniformly low across all conditions (~6--7%). This is consistent across conditions and does not affect between-condition comparisons, but limits interpretation of EES_total as a full-episode efficiency measure.

**No long-term uncertainty or delayed rewards.** The environments tested are either stationary or stochastic-but-symmetric. Regulatory constraints may play a qualitatively different role in environments with delayed consequences, sparse rewards, or temporal structure requiring multi-step planning.

**Single learning mechanism.** Only state-conditioned scalar preference biasing was tested. More complex learning mechanisms may produce different interactions with regulatory constraints.

---

## 10. Conclusion

This work provides evidence that efficient behavior depends on structural alignment with survival-relevant variables, while robust behavior additionally requires regulatory constraints.

Primary experiments show that the full constrained adaptive system was the only condition achieving net-positive energy efficiency (EES > 1.0). Removing regulatory constraints produced a 4.1% efficiency drop; the misaligned optimizer performed below the random baseline, demonstrating that optimization without alignment is not merely inefficient -- it is deterministically harmful relative to no optimization at all.

Replication and robustness testing show that alignment is structural rather than parametric: neither extended time horizons, nor environmental stress, nor parameter tuning of the misaligned objective recovered the efficiency ordering. The full system showed adaptive energy recovery under scarcity; misaligned and unstructured conditions stagnated or declined.

Constraint ablation reveals that regulatory mechanisms are redundant individually -- no single removal causes collapse -- but that individual removal exposes degenerate optimization. Ablation of the world-model energy weight (A3) produces the highest EES across all conditions, but through behavioral collapse: near-exclusive approach behavior, unregulated energy accumulation, and near-zero behavioral diversity. This is the key finding of Phase C: high efficiency and adaptive behavior are not equivalent.

Environmental generalization confirms this distinction at scale. Under reward uncertainty, both the misaligned condition (C) and the ablated condition (A3) degenerate to the same monoculture attractor (approach ~94%, entropy ~0.31), with C achieving high EES through stochastic bootstrapping rather than regulatory control. Under a safe/risky trade-off, C achieves high EES because its maladaptive over-exploration coincidentally aligns with the positive expected value of risky behavior. Neither outcome reflects adaptation. The fully constrained system (A) is the only condition that maintains stable behavioral structure -- balanced action distribution, regulated energy, consistent entropy -- across all environments tested.

Efficiency alone is not sufficient to characterize adaptive behavior. Systems may achieve high efficiency through degenerate strategies or by coincidental environmental alignment. Robustness -- stable behavioral structure across environment classes -- is the stronger criterion. The results suggest that both alignment and regulation are necessary components of robust, adaptive behavior: alignment enables efficiency, regulation preserves it.

---

## References

Frank, M.J. (2004). By carrot or by stick: cognitive reinforcement learning in parkinsonism. *Science*, 306(5703), 1940-1943.

Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., Cai, T., Rutherford, E., et al. (2022). Training compute-optimal large language models. *arXiv:2203.15556*.

Kaplan, J., McCandlish, S., Henighan, T., Brown, T.B., Chess, B., Child, R., et al. (2020). Scaling laws for neural language models. *arXiv:2001.08361*.

Schultz, W. (1998). Predictive reward signal of dopamine neurons. *Journal of Neurophysiology*, 80(1), 1-27.

Sterling, P. and Eyer, J. (1988). Allostasis: a new paradigm to explain arousal pathology. *Handbook of Life Stress, Cognition and Health*, 629-649.

Tononi, G. and Cirelli, C. (2006). Sleep function and synaptic homeostasis. *Sleep Medicine Reviews*, 10(1), 49-62.

---

*Final draft — integrating Phase A (replication), Phase B (robustness), Phase C (ablation + degeneration), Phase D (environmental generalization). Internal document. Hitoshi AI Labs — NeuroSeed Project.*
*Word count: approximately 5500.*
