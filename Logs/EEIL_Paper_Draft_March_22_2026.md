# Energy Efficiency Intelligence Law: Evidence from a Biologically Constrained Adaptive System

**Prince Siddhpara**
Hitoshi AI Labs — NeuroSeed Project
March 22, 2026

*First draft. Not for distribution. For internal clarification only.*

---

## Abstract

Current machine learning systems achieve performance through scale: larger models trained on larger datasets with greater computational resources. This approach produces capable systems but at substantial energy cost, and with no formal mechanism to ensure that optimization objectives remain aligned with operational constraints. Biological intelligence, by contrast, operates under severe metabolic limits and exhibits behavior organized around survival efficiency rather than raw task performance.

We propose the Energy Efficiency Intelligence Law (EEIL): systems with structured regulatory constraints achieve higher energy efficiency than systems without such constraints, independent of computational scale. We test this hypothesis through controlled ablation experiments in Ikigai, a biologically grounded adaptive simulation implementing homeostasis, metabolic drives, predictive processing, and experience-dependent learning. Four conditions were compared across five independent runs of 5000 ticks each: a full constrained adaptive system (A), a constrained system without learning (B), a system retaining energy physics but without regulatory drives (C), and a random baseline (D).

The primary metric, Energy Efficiency Score (EES = total energy gained / total energy spent), produced the following result: only Condition A achieved EES > 1.0 (A: 1.0019, B: 0.9930, C: 0.9544, D: 0.9641). Critically, Condition C performed below the random baseline, a result not initially predicted. Post-hoc analysis revealed that a prediction-error-minimizing system without energy constraints consistently chose exploration over foraging, falling into chronic energy depletion with mean energy 0.206 and 61.8% of time in the low-energy band. A random policy, by allocating roughly equal probability to all actions including foraging, outperformed the unconstrained optimizer.

These results support the EEIL hypothesis within this system. Regulatory constraints contributed +4.1% efficiency over the unconstrained condition. Learning contributed an additional +0.9%. The full system exceeded the random baseline by +3.9%. More significantly, the C < D result demonstrates that constraints are necessary to maintain alignment between optimization objectives and survival-relevant outcomes. A system optimizing an unaligned proxy objective -- here, prediction-error minimization without metabolic coupling -- performs worse than one with no objective at all.

---

## 1. Introduction

Contemporary AI development is organized around a scaling hypothesis: performance on most tasks increases predictably with model size, training compute, and data volume (Kaplan et al. 2020; Hoffmann et al. 2022). This hypothesis has been broadly validated. Language models, image generators, and game-playing systems have all improved substantially as scale increased. The approach has produced genuinely capable systems.

It has also produced systems that consume extraordinary energy. Training a large language model can require gigawatt-hours of electricity. Inference at scale requires continuous high-power compute. The energy cost per unit of useful computation is not a priority in the current development paradigm -- it is a secondary concern, managed through hardware efficiency but not addressed at the level of system design.

Biological systems operate under the opposite constraint. A human brain consumes approximately 20 watts. It processes continuous sensory input, regulates bodily functions, plans, learns, and generalizes from minimal data -- all within a metabolic budget that would be insufficient to run a modest laptop. The efficiency of biological intelligence is not incidental to its architecture; it is central to it. Metabolic constraints shaped the structural organization of neural systems over evolutionary time.

This observation motivates a hypothesis about the relationship between constraints and intelligence. If biological intelligence is efficient because it evolved under metabolic constraint, then the structural features that enforce efficiency -- homeostasis, drive states, predictive processing, sleep-wake regulation -- may be constitutive of intelligent behavior rather than separate from it. Intelligence may not simply coexist with metabolic efficiency; it may require it.

We formalize this intuition as the Energy Efficiency Intelligence Law (EEIL) and test it in a controlled computational environment. The environment allows precise manipulation of regulatory constraints while holding all other system properties constant. The question is not whether a constrained system can be efficient, but whether the constraints themselves cause the efficiency.

---

## 2. The EEIL Hypothesis

**Energy Efficiency Intelligence Law**: Systems optimizing proxy objectives without regulatory constraints that couple those objectives to survival-relevant signals exhibit lower energy efficiency than systems where such coupling is present, independent of computational scale.

The critical distinction from a weaker efficiency claim is the following: the hypothesis does not merely predict that constraints help. It predicts a specific failure mode. When a system's optimization objective is decoupled from its metabolic requirements, it will optimize the proxy effectively while degrading survival-relevant outcomes -- and may perform worse than an unoptimized baseline.

We define the relevant terms as follows.

**Energy efficiency** is the ratio of total energy inflows to total energy outflows across a simulation episode. EES = total_energy_gained / total_energy_spent, where gains include all positive energy changes per tick (foraging yield, metabolic recovery, sleep restoration) and costs include all negative energy changes (metabolic drain, failed foraging opportunity cost). An EES > 1.0 indicates a system that, on net, acquires more energy than it expends. An EES < 1.0 indicates a system in long-run deficit.

**Structured regulatory constraints** are internal mechanisms that couple the organism's metabolic state to its action selection policy. The specific constraints tested here are: (1) a homeostatic hunger drive that increases the value of foraging actions as energy decreases, (2) an energy-conditioned precision weighting that adjusts the sharpness of action selection based on metabolic state, (3) a survival value function that weights energy consequences in action planning, and (4) state-conditioned preference learning that accumulates experience-based biases toward historically profitable actions.

The hypothesis predicts that removing these constraints will reduce energy efficiency. The stronger prediction -- and the one that distinguishes the EEIL hypothesis from a weaker claim that constraints merely help -- is that removing constraints produces not just reduced efficiency but qualitatively different failure modes.

---

## 3. System Description

Ikigai is a biologically grounded adaptive simulation implementing the following components.

**Action space.** The organism selects one of three actions per waking tick: approach (foraging behavior), explore (curiosity-driven sampling), or withdraw (conservative recovery). Each action has energy consequences that depend on ecological conditions.

**Energy system.** Energy is distributed across three neural compartments (cortical, limbic, motor), each bounded to [0, 1]. Mean energy is computed as the average across compartments. A foraging mechanism provides probabilistic energy gain on approach: success probability = 0.20 + 0.80 * (energy/0.80)^2, ensuring a minimum 20% yield regardless of energy state (ecological floor) while maintaining scarcity at low energy. Metabolic cost applies every waking tick. A mild efficiency bonus (+0.001 per compartment per tick) applies when energy is in the mid-range (0.20 -- 0.50), creating a preferred operating band without eliminating resource pressure.

**Regulatory drives.** A hunger drive fires when mean energy falls below 0.25, adding a proportional bias toward approach in the action selection computation. An energy-conditioned temperature parameter adjusts action selection precision: low energy produces conservative behavior, mid energy produces exploratory behavior, high energy produces exploitation.

**World model.** A survival value function predicts the energetic, cortisol, and prediction-error consequences of each action and selects the action maximizing predicted survival value. The function weights energy consequences (w_e = 1.0), prediction error consequences (w_pe = 0.6), cortisol consequences (w_cort = 0.4), and switching costs (w_wc = 0.2).

**Learning.** A state-conditioned preference mechanism maintains scalar bias values pref[state][action] for each combination of energy band (low/mid/high) and action. Biases are updated per waking tick via: pref[state][action] += learning_rate * (energy_after - energy_before), clamped to [-1, 1]. Biases are injected into the survival value computation before action selection, implementing an approximation of dopamine-mediated corticostriatal plasticity.

**Sleep-wake dynamics.** Sleep onset and offset are governed by an adenosine accumulation model and cortisol gating. During sleep, energy is partially restored.

---

## 4. Metrics

**Primary metric:**
EES = total_energy_gained / total_energy_spent

where gains and costs are summed over all ticks (waking and sleeping). A secondary metric, EES_waking, restricts the computation to waking ticks only, isolating behavioral efficiency from sleep recovery.

**Supporting metrics:**
- mean_energy: mean energy across all waking ticks
- entropy: Shannon entropy of the waking action distribution (bits)
- low_band %: fraction of waking ticks spent in the low-energy band (energy < 0.20)
- approach_rate: fraction of waking ticks selecting approach
- delta_e|action: mean energy change per tick conditioned on action

EES is the only metric used for primary comparison across conditions. All other metrics are used for interpretation of mechanism.

---

## 5. Experiment Design

Four conditions were run, each using the same simulation environment, action space, energy physics, and neural architecture. The conditions differed only in their regulatory layer.

**Condition A -- Full System (Structured + Adaptive).** All regulatory constraints active. Hunger drive, energy-conditioned precision, survival value function with full energy weight, and state-conditioned preference learning with learning rate 0.05. This is the reference condition.

**Condition B -- No Learning (Structured + Non-adaptive).** All regulatory constraints active. Learning rate set to 0.0; preference biases remain at zero throughout. The organism uses drives and the survival value function but does not accumulate experience-based biases.

**Condition C -- No Constraints (Weakly Structured).** Hunger drive removed (set to zero). Energy weight in survival value function set to zero (action selection considers only prediction error and cortisol, not energy consequences). Energy-conditioned temperature replaced with a fixed exploratory default. The organism retains the energy physics (foraging still produces energy; metabolic cost still applies) but does not use energy state to guide action selection.

**Condition D -- Random Baseline (Unstructured).** Action selection replaced with uniform random choice among the three actions. The approach floor (a 2% minimum action initiation rate) was disabled to maintain a truly uniform policy. Energy physics intact.

Each condition was run for 5 independent episodes of 5000 ticks each. Initial conditions were identical across conditions (no saved state, energy initialized at default). All conditions operated with identical computational structure -- same neural architecture, same action space, same environmental physics -- differing only in their regulatory constraints. All conditions used the same simulation executable with condition-specific patches applied via in-memory source modification.

---

## 6. Results

Table 1 reports the primary and supporting metrics for all four conditions, averaged across five runs.

**Table 1. EEIL Experimental Results**

| Metric              | A: Full   | B: No-learn | C: No-constr | D: Random |
|---------------------|-----------|-------------|--------------|-----------|
| EES (all ticks)     | **1.0019**| 0.9930      | 0.9544       | 0.9641    |
| EES (waking only)   | **0.8248**| 0.7889      | 0.5486       | 0.6850    |
| mean_energy         | **0.492** | 0.428       | 0.206        | 0.333     |
| entropy (bits)      | 1.559     | 1.558       | 1.551        | **1.574** |
| low_band %          | **0.169** | 0.227       | 0.618        | 0.490     |
| approach_rate       | **0.403** | 0.368       | 0.245        | 0.309     |
| explore_rate        | 0.276     | 0.253       | **0.420**    | 0.390     |
| delta_e\|approach   | **+0.00518** | +0.00466 | +0.00359   | +0.00489  |

**EEIL Decomposition:**

| Component                         | Delta EES | % over baseline |
|-----------------------------------|-----------|-----------------|
| Learning (A vs B)                 | +0.0088   | +0.9%           |
| Regulatory constraints (B vs C)   | +0.0387   | +4.1%           |
| Full system vs random (A vs D)    | +0.0378   | +3.9%           |

Three results are notable.

First, Condition A is the only condition achieving EES > 1.0. This means the full constrained adaptive system is the only one that, across all ticks including sleep, gains more energy than it expends. All other conditions are in net energy deficit.

Second, Condition C performs below the random baseline (EES: 0.9544 vs 0.9641). This result was not predicted by the initial hypothesis and is examined in detail in the Analysis section.

Third, the energy delta per approach action is highest in Condition A (+0.00518 per tick) and decreases monotonically through B, D, and C. This ordering follows mean_energy directly: the full system maintains higher energy, achieving higher foraging success probabilities, compounding into a higher per-approach yield. Efficiency generates further efficiency.

---

## 7. Analysis

### 7.1 Effect of Regulatory Constraints

Removing regulatory constraints (B to C) produced the largest single efficiency drop in the experiment: -0.0387 EES, or -4.1% relative to the no-learning system. This is a larger contribution than learning itself and larger than the difference between the full system and the random baseline.

The mechanism is clear from the action distributions. Condition C selected explore 42% of the time, the highest explore rate of any condition, including the random baseline (39%). Without hunger drive overriding the exploration tendency, and without energy consequences weighted in the survival value function, the organism defaulted to the behavior that minimizes prediction error most directly: exploration. But exploration is energetically costly and produces no food. The result was chronic energy depletion: 61.8% of waking ticks in the low-energy band, mean energy 0.206.

At low energy, the foraging success probability is 20-22% (ecological floor). With approach selected only 24.5% of the time, the organism's expected energy gain per waking tick from foraging was: 0.245 * 0.21 * gain_per_success ≈ minimal. Metabolic cost continued regardless. The organism was unable to escape the low-energy regime.

### 7.2 Effect of Learning

Adding experience-dependent learning (B to A) produced +0.0088 EES (+0.9%). This is a real but secondary contribution. The state-conditioned preference mechanism accumulated approach bias, increasing approach rate from 0.368 to 0.403. With higher approach rate and the resulting higher mean energy (0.428 vs 0.492), foraging success probability increased, compounding into higher per-approach yield.

The learning contribution is secondary not because learning is unimportant, but because the regulatory constraints determine whether the organism is in a regime where learning can be effective. Learning in Condition A is effective because drives and value function maintain mean energy in the mid-high range, where foraging is frequent and profitable. If the regulatory constraints were absent, learning would accumulate evidence in a low-energy chronic-depletion regime, producing a different and less useful set of preferences.

Constraints and learning are therefore not independent contributors. Constraints establish the operating regime; learning optimizes within it.

### 7.3 The C < D Result: Wrong Objective Versus No Objective

The result EES_C < EES_D deserves direct attention.

Condition C retained a world model, a survival value function, and a predictive processing system. It had more computational structure than Condition D (random). And yet it performed worse. The interpretation is that computational structure, without metabolic alignment, can be actively harmful.

The prediction-error minimization objective -- which drives the world model in the absence of energy and hunger signals -- is not aligned with energy efficiency. Prediction error is reduced most effectively by exploring an unpredictable environment, because exploration produces diverse sensory input that updates the model. A system optimizing prediction error without constraint will explore extensively. In an environment where survival depends on foraging, this is maladaptive.

Condition D has no optimization objective. It samples actions uniformly. By chance, it selects approach roughly one third of the time. That is more than Condition C's 24.5%, and it is enough to maintain a higher mean energy (0.333 vs 0.206) and a higher EES.

This result has a specific implication: the claim that any structured optimization is better than random is false in the absence of objective alignment. The value of intelligence is conditional on the intelligence being directed toward the right target. An optimization system directed at the wrong target can be worse than no optimization at all.

This is not a novel theoretical observation -- it is related to the Goodhart's Law failure mode and the AI alignment problem more generally. What this experiment provides is a concrete quantitative demonstration in a minimal system: -0.97% EES penalty for misaligned optimization versus random policy.

---

## 8. Discussion

### 8.1 Constraints as Alignment Mechanisms

The standard framing of constraints in AI system design is negative: constraints limit what a system can do. A system with no constraints can explore a larger hypothesis space and potentially find better solutions.

The EEIL experimental results suggest a different framing. In a survival-relevant task, constraints serve as alignment mechanisms. They ensure that the optimization process -- whatever its objective -- stays connected to the actions that produce actual survival outcomes. The hunger drive does not limit the organism's intelligence; it redirects that intelligence toward foraging when foraging is needed.

This framing has a specific consequence for AI system design. A system optimizing a proxy objective (prediction error, log-likelihood, reward signal) without metabolic or resource constraints will optimize the proxy, potentially at the expense of actual utility. Adding resource constraints to the optimization loop is not a limitation -- it is a correction mechanism that maintains alignment between the optimization objective and the operational requirement.

The experimental results sharpen this claim. Efficiency is not a property of optimization alone; it is a property of alignment between the optimization target and the system's survival constraints. Condition C had more optimization structure than Condition D. It had a world model, a value function, and predictive processing. And it was less efficient, because the optimization was not directed at survival-relevant outcomes. The efficiency gap between C and D is not explained by capability; it is explained by objective misalignment. A capable system solving the wrong problem is worse than an incapable one solving no problem.

### 8.2 Efficiency and Scale

The full constrained system in this experiment is small. Its neural architecture has three compartments; its action space has three options; its simulation runs for 5000 ticks. The random baseline operates in the same environment. The efficiency difference (EES_A vs EES_D = +3.9%) is not explained by scale. All conditions have the same scale. The difference is explained by structure.

This does not prove that biological efficiency would survive arbitrary scaling -- the relationship between scale and structural efficiency is an open empirical question. But it is consistent with the hypothesis that the source of biological efficiency is organizational rather than computational: it is the architecture of regulation, not the volume of computation, that produces efficiency.

---

## 9. Limitations

**Single environment.** All experiments were conducted in a single foraging environment with fixed resource dynamics. The generalizability of the EEIL result to other environments -- particularly those with different action-consequence relationships -- is not established.

**Small system.** The simulated organism has three neural compartments, three actions, and operates on timescales of thousands of ticks. Biological neural systems have billions of neurons, thousands of distinct cell types, and operate over a lifetime. The degree to which findings from this system generalize to biological or large-scale artificial systems is unknown.

**No language or abstract reasoning.** The organism tested here engages in low-level sensorimotor behavior in a resource environment. Claims about cognitive efficiency in language, planning, or abstract reasoning cannot be derived from these results.

**Short simulation horizon.** 5000 ticks is sufficient to observe ecological dynamics and early learning effects, but not to observe long-run adaptation, developmental change, or multi-generational selection effects.

**Single learning mechanism.** Only one form of learning (local scalar preference biasing) was tested. More complex learning mechanisms -- temporal difference, model-based planning, episodic memory -- may produce different efficiency profiles.

**Sleep rate.** Observed sleep rates were uniformly low across all conditions (~5.9%). Because this pattern was consistent across all four conditions, EES differences between conditions are attributable to waking behavior rather than differential sleep recovery. The low rate relative to previous experiments with the same system (~34%) may reflect shorter episode length (5000 vs 8000+ ticks); the organism may not accumulate sufficient adenosine for multiple sleep bouts within the measurement window. This does not affect condition comparisons but limits interpretation of EES_total as a full-episode efficiency measure.

---

## 10. Conclusion

We tested the Energy Efficiency Intelligence Law (EEIL) through controlled ablation experiments in a biologically grounded adaptive system. Four conditions -- full constraints with learning, full constraints without learning, no constraints, and random policy -- were compared using EES as the primary metric across five runs of 5000 ticks.

Results support the EEIL hypothesis within this system. The full constrained adaptive system achieved EES = 1.0019, the only condition exceeding 1.0. Removing regulatory constraints produced a -4.1% efficiency drop, the largest contribution of any component tested. Adding experience-dependent learning produced an additional +0.9% efficiency. The full system outperformed the random baseline by +3.9%.

The most informative result was not in the expected ordering but in its violation: the unconstrained system (C) performed below the random baseline (D). A prediction-error optimizer without metabolic alignment devoted 42% of its behavior to exploration, fell into chronic energy depletion, and achieved lower efficiency than a system with no strategy at all. This result supports the claim that misaligned optimization is not merely inefficient but actively harmful relative to no optimization.

These results suggest that regulatory constraints in biological systems are not incidental to intelligence but constitutive of it: they are the mechanism by which optimization is kept aligned with survival. The implication for artificial system design is that resource constraints and metabolic signals are not limitations to be designed around but structural requirements for maintaining alignment between optimization objectives and operational outcomes.

Further work is required to determine whether these findings generalize across environments, scales, and learning mechanisms. The current results establish experimental support within a specific, controlled context.

---

## References

Frank, M.J. (2004). By carrot or by stick: cognitive reinforcement learning in parkinsonism. *Science*, 306(5703), 1940-1943.

Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., Cai, T., Rutherford, E., et al. (2022). Training compute-optimal large language models. *arXiv:2203.15556*.

Kaplan, J., McCandlish, S., Henighan, T., Brown, T.B., Chess, B., Child, R., et al. (2020). Scaling laws for neural language models. *arXiv:2001.08361*.

Schultz, W. (1998). Predictive reward signal of dopamine neurons. *Journal of Neurophysiology*, 80(1), 1-27.

Sterling, P. and Eyer, J. (1988). Allostasis: a new paradigm to explain arousal pathology. *Handbook of Life Stress, Cognition and Health*, 629-649.

Tononi, G. and Cirelli, C. (2006). Sleep function and synaptic homeostasis. *Sleep Medicine Reviews*, 10(1), 49-62.

---

*First draft. Internal document. Hitoshi AI Labs — NeuroSeed Project.*
*Word count: approximately 2400.*
