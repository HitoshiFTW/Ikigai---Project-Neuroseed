# Energy Efficiency Intelligence Law: Evidence from a Biologically Constrained Adaptive System

**Prince Siddhpara**
Hitoshi AI Labs — NeuroSeed Project
March 22, 2026

*First draft. Not for distribution. For internal clarification only.*

---

## Abstract

This work investigates the relationship between optimization, constraint structure, and energy efficiency in a biologically-inspired adaptive system. Four conditions were compared -- a full constrained adaptive system, a constrained system without learning, a system without regulatory constraints, and a random baseline -- using Energy Efficiency Score (EES = total energy gained / total energy spent) as the primary metric, across five runs of 5000 ticks and replicated across eight runs of 15000 ticks.

Results show that only constraint-aligned systems achieve net-positive energy efficiency, and that this effect is stable across extended simulations and environmental variation. The full system achieved EES = 1.0019 (primary) and 1.0025 (replicated); all other conditions remained below 1.0. Critically, the unconstrained condition (C) performed below the random baseline (D), demonstrating that misaligned optimization is deterministically harmful relative to no optimization at all.

An objective sweep demonstrates that inefficiency cannot be corrected through parameter tuning, but requires structural inclusion of survival-relevant variables. Reducing prediction-error weighting from 0.6 to 0.1 produced no improvement in Condition C; the failure is structural rather than parametric.

Constraint ablation further reveals that while multiple mechanisms redundantly support alignment -- no single constraint removal significantly degrades performance -- removing regulatory constraints leads to degenerate strategies that maximize efficiency through behavioral collapse. Ablation of the world-model energy weight (A3) produced the highest EES across all conditions, but achieved this through near-exclusive approach behavior (~95%) and unregulated energy accumulation, not through adaptive balance. Under environmental stress this pattern persists and intensifies.

These findings suggest that efficient behavior depends on both alignment and regulation, rather than optimization strength alone. Alignment enables efficiency; regulation preserves behavioral integrity.

---

## 1. Introduction

Contemporary AI development is organized around a scaling hypothesis: performance on most tasks increases predictably with model size, training compute, and data volume (Kaplan et al. 2020; Hoffmann et al. 2022). This hypothesis has been broadly validated. Language models, image generators, and game-playing systems have all improved substantially as scale increased. The approach has produced genuinely capable systems.

It has also produced systems that consume extraordinary energy. Training a large language model can require gigawatt-hours of electricity. Inference at scale requires continuous high-power compute. The energy cost per unit of useful computation is not a priority in the current development paradigm -- it is a secondary concern, managed through hardware efficiency but not addressed at the level of system design.

Modern AI systems rely on large-scale optimization, often without explicit coupling to survival-relevant constraints. This raises a structural question: is inefficiency caused by insufficient optimization, or by misalignment between objectives and system constraints? These are distinct problems with distinct solutions. Scaling addresses the first. Structural realignment is required for the second.

Biological systems operate under the opposite constraint. A human brain consumes approximately 20 watts. It processes continuous sensory input, regulates bodily functions, plans, learns, and generalizes from minimal data -- all within a metabolic budget that would be insufficient to run a modest laptop. The efficiency of biological intelligence is not incidental to its architecture; it is central to it. Metabolic constraints shaped the structural organization of neural systems over evolutionary time.

We investigate whether efficiency emerges from structured constraint systems, rather than from optimization strength alone. The hypothesis tested here is that the regulatory architecture -- homeostasis, drive states, metabolic coupling, experience-dependent learning -- is constitutive of efficient behavior, not merely associated with it. Removing this architecture should degrade efficiency not through reduced capability but through objective misalignment.

We formalize this as the Energy Efficiency Intelligence Law (EEIL) and test it through controlled ablation experiments. The question is not whether a constrained system can be efficient, but whether the constraints themselves cause the efficiency -- and whether their absence can produce degenerate strategies that satisfy efficiency metrics through pathological means.

---

## 2. The EEIL Hypothesis

**Energy Efficiency Intelligence Law**: Efficient behavior emerges in systems where optimization is structurally aligned with survival-relevant variables and constrained by regulatory mechanisms. Alignment alone is insufficient; without regulation, systems may achieve high efficiency through degenerate strategies that collapse behavioral diversity.

The hypothesis has two claims.

The first is the alignment claim: systems optimizing proxy objectives without regulatory constraints that couple those objectives to survival-relevant signals will exhibit lower efficiency than systems where such coupling is present. This is the claim tested in the primary experiment (Conditions A--D) and replicated across phases A and B.

The second is the regulation claim: even among structurally aligned systems, individual regulatory constraints serve to prevent degenerate optimization. A system that has removed specific regulatory mechanisms may achieve high efficiency metrics through behavioral collapse -- narrow strategy convergence, unregulated accumulation, loss of adaptive balance -- rather than through genuine regulation. This is the claim tested in Phase C.

Both claims are required. Alignment without regulation permits exploitation of the metric. Regulation without alignment cannot compensate for an objective disconnected from survival-relevant outcomes.

We define the relevant terms as follows.

**Energy efficiency** is the ratio of total energy inflows to total energy outflows across a simulation episode. EES = total_energy_gained / total_energy_spent, where gains include all positive energy changes per tick (foraging yield, metabolic recovery, sleep restoration) and costs include all negative energy changes (metabolic drain, failed foraging opportunity cost). An EES > 1.0 indicates a system that, on net, acquires more energy than it expends. An EES < 1.0 indicates a system in long-run deficit.

**Structured regulatory constraints** are internal mechanisms that couple the organism's metabolic state to its action selection policy. The specific constraints tested here are: (1) a homeostatic hunger drive that increases the value of foraging actions as energy decreases, (2) an energy-conditioned precision weighting that adjusts the sharpness of action selection based on metabolic state, (3) a survival value function that weights energy consequences in action planning, and (4) state-conditioned preference learning that accumulates experience-based biases toward historically profitable actions.

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

### 5.3 Replication Protocol

The replication experiment was designed to test the stability of the observed efficiency ordering under extended time horizons and stochastic variation. Each condition was run for 8 independent episodes of 15000 ticks each, using identical metrics and conditions as the primary experiment. Episode length was increased to allow observation of dynamics across three temporal phases: early (ticks 0--5000), mid (5000--10000), and late (10000--15000), classified by global tick index. All other parameters were held constant.

### 5.4 Robustness and Objective Sweep

Two additional experiments were conducted to test whether the observed efficiency differences are robust to environmental variation and sensitive to objective parameterization. These experiments were designed to address whether the failure of Condition C reflects excessive PE optimization or the structural absence of energy coupling.

**Environment stress** (Experiment B1): The foraging floor parameter was reduced from 0.20 to 0.10, reducing baseline resource availability for all conditions. This is the only change; all four conditions were run under this modified environment (8 runs, 15000 ticks).

**Objective sweep** (Experiment B2): Condition C was re-run with three values of the prediction-error weight (w_pe = 0.6, 0.3, 0.1), while all other Condition C patches remained identical. The energy weight remained at zero in all variants. Condition D was included as a reference baseline (8 runs, 15000 ticks per variant).

### 5.5 Constraint Ablation and Degeneration Analysis

A constraint ablation experiment was conducted to determine which regulatory components are individually necessary versus redundant. Starting from the full system (A), one constraint was removed at a time across four ablation conditions (8 runs, 15000 ticks each):

**A1 -- No Learning**: Learning rate set to 0.0; all other constraints active.

**A2 -- No Hunger Signal**: Hunger drive removed (hunger_drive = 0); world-model energy weight, temperature regulation, and learning remain active.

**A3 -- No World-Model Energy Coupling**: Energy weight in survival value function set to zero (w_e = 0); hunger drive, temperature regulation, and learning remain active.

**A4 -- No State-Dependent Temperature**: Temperature fixed at 0.20; hunger drive, world-model energy weight, and learning remain active.

A follow-up stress test was conducted comparing A (Full) against A3 (No WM energy) specifically under the reduced foraging floor environment (floor = 0.10, 8 runs, 15000 ticks), to determine whether the behavioral effects of A3 persist under resource scarcity.

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

**Replication Results (8 runs x 15000 ticks)**

Table 2 reports the replication results across 8 runs of 15000 ticks per condition.

**Table 2. Replication Results**

| Condition    | Mean EES | Std    | Mean_E | Sleep% |
|--------------|----------|--------|--------|--------|
| A: Full      | 1.0025   | 0.0041 | 0.620  | 6.9%   |
| B: No-learn  | 0.9987   | 0.0071 | 0.481  | 6.9%   |
| D: Random    | 0.9903   | 0.0082 | 0.347  | 6.8%   |
| C: No-constr | 0.9849   | 0.0004 | 0.231  | 6.9%   |

The efficiency ordering (A > B > D > C) was preserved across all runs, confirming the stability of the result. Condition A remains the only condition achieving mean EES > 1.0.

**Distribution Analysis**

While the efficiency difference between A (Full) and B (No Learning) exhibits some overlap across runs (A_min = 0.9977, B_max = 1.0097), the separation between D (Random) and C (No Constraints) is consistent and non-overlapping (C_max = 0.9856, D_min = 0.9863, gap = +0.0007). The low variance in Condition C (std = 0.0004) indicates that the inefficiency of the misaligned system is deterministic rather than stochastic. Condition C produces the same failure mode reliably across every run.

**Temporal Analysis**

Period-level EES (mean over 8 runs) shows distinct dynamics across conditions. Condition A maintains efficiency throughout (early: 1.0066, mid: 0.9988, late: 1.0023), with no systematic degradation. Condition D exhibits gradual deterioration: mean energy falls from 0.359 in the early period to 0.290 in the late period (drift = -0.069). Condition C remains consistently inefficient across all three periods, with mid-period variance reflecting ecological oscillation rather than sustained improvement.

This indicates that aligned systems stabilize or improve over time, while unaligned systems either stagnate or decay.

---

**Phase B Results -- Environment Stress**

Table 3 reports EES under reduced resource availability (foraging floor 0.10), with all other parameters unchanged.

**Table 3. Environment Stress Results (8 runs x 15000 ticks, floor 0.10)**

| Condition    | Mean EES | Std    | Mean_E | Energy Drift |
|--------------|----------|--------|--------|--------------|
| A: Full      | 0.9995   | 0.0092 | 0.461  | +0.183       |
| B: No-learn  | 0.9902   | 0.0102 | 0.321  | +0.018       |
| D: Random    | 0.9847   | 0.0010 | 0.284  | -0.004       |
| C: No-constr | 0.9823   | 0.0003 | 0.216  | -0.024       |

The efficiency ordering (A > B > D > C) was preserved under reduced resource availability. While absolute efficiency decreased across all conditions, the relative ordering remained stable and the C < D separation held (C_max = 0.9826, D_min = 0.9835, non-overlapping). The full system exhibited increasing mean energy over time (early: 0.353, late: 0.536, drift = +0.183), indicating adaptive recovery under scarcity, whereas all other conditions remained stable or declined. This is the only condition that actively improves its position under stress.

**Phase B Results -- Objective Sweep**

Table 4 reports EES for Condition C variants with varying prediction-error weight (w_pe), with Condition D as reference.

**Table 4. Objective Sweep Results (8 runs x 15000 ticks)**

| Variant      | Mean EES | Std    | Mean_E | Explore |
|--------------|----------|--------|--------|---------|
| D: Random    | 0.9900   | 0.0088 | 0.306  | 38.8%   |
| C: w_pe=0.6  | 0.9848   | 0.0003 | 0.233  | 41.9%   |
| C: w_pe=0.3  | 0.9849   | 0.0003 | 0.235  | 41.7%   |
| C: w_pe=0.1  | 0.9847   | 0.0003 | 0.228  | 42.3%   |

Reducing prediction-error weighting does not improve efficiency in Condition C. EES remains effectively unchanged across all tested values of w_pe (range: 0.9847--0.9849), and action distributions show minimal variation (explore rate: 41.7--42.3% across all variants). Condition C remains below the random baseline at all tested parameter values. This indicates that the inefficiency of the misaligned system is not caused by excessive optimization of prediction error, but by the structural absence of energy-based constraints from the objective function.

---

**Phase C Results -- Constraint Ablation**

Table 5 reports EES for each single-constraint ablation condition, compared to the full system. All runs use the standard foraging environment (floor 0.20).

**Table 5. Single-Constraint Ablation Results (8 runs x 15000 ticks, floor 0.20)**

| Condition      | Removed          | Mean EES | Std    | dEES vs A |
|----------------|------------------|----------|--------|-----------|
| A: Full        | --               | 1.0008   | 0.0030 | --        |
| A1: No-learn   | Learning (lr=0)  | 1.0009   | 0.0066 | +0.0001   |
| A2: No-hunger  | Hunger drive     | 1.0036   | 0.0038 | +0.0028   |
| A3: No-WM-E    | w_e=0 in WM      | 1.0160   | 0.0002 | +0.0152   |
| A4: No-temp    | Fixed temp=0.20  | 1.0038   | 0.0031 | +0.0030   |

Removing any single constraint does not degrade performance. On the contrary, all single-constraint ablations maintain or improve EES relative to the full system. This confirms the presence of redundancy: the regulatory mechanisms have overlapping coverage, such that each individual constraint can be removed without catastrophic loss.

The large EES increase in A3 (No WM energy weight, +1.5%) is the most striking result and requires separate analysis; see Section 6.4.

---

**Phase C Results -- Degenerate Optimization (A3 Stress Test)**

To determine whether A3's efficiency advantage reflects genuine improvement or metric exploitation, A3 was compared to the full system under environmental stress (floor 0.10).

**Table 6. A vs A3 Under Stress (8 runs x 15000 ticks, floor 0.10)**

| Condition    | Mean EES | Std    | Mean_E | Approach% | Energy Drift |
|--------------|----------|--------|--------|-----------|--------------|
| A: Full      | 1.0017   | 0.0041 | 0.492  | 46.1%     | +0.094       |
| A3: No-WM-E  | 1.0162   | 0.0017 | 0.786  | 94.7%     | +0.506       |

Ablation of world-model energy weighting (A3) produces the highest energy efficiency score across all tested conditions, both in the standard and stress environments. However, this improvement is achieved through behavioral collapse: the system converges to near-exclusive approach behavior (94.7%), leading to continuous energy accumulation without regulation.

Under environmental stress, this pattern persists and intensifies, with energy levels rising to a mean of 0.786 -- well above the regulated equilibrium of ~0.433 observed in the full system -- and behavioral diversity near zero. The full system under the same stress maintains a balanced action distribution (approach 46.1%), energy near equilibrium (0.492), and a modest positive drift (+0.094).

This demonstrates that high efficiency can be achieved through degenerate strategies that exploit the metric without maintaining adaptive or balanced behavior. A3 does not improve efficiency -- it abandons regulation and converts the metric into a monoculture signal.

---

## 7. Analysis

### 7.1 Effect of Regulatory Constraints

Removing regulatory constraints (B to C) produced the largest single efficiency drop in the experiment: -0.0387 EES, or -4.1% relative to the no-learning system. This is a larger contribution than learning itself and larger than the difference between the full system and the random baseline.

The mechanism is clear from the action distributions. Condition C selected explore 42% of the time, the highest explore rate of any condition, including the random baseline (39%). Without hunger drive overriding the exploration tendency, and without energy consequences weighted in the survival value function, the organism defaulted to the behavior that minimizes prediction error most directly: exploration. But exploration is energetically costly and produces no food. The result was chronic energy depletion: 61.8% of waking ticks in the low-energy band, mean energy 0.206.

At low energy, the foraging success probability is 20-22% (ecological floor). With approach selected only 24.5% of the time, the organism's expected energy gain per waking tick from foraging was minimal. Metabolic cost continued regardless. The organism was unable to escape the low-energy regime.

### 7.2 Effect of Learning

Adding experience-dependent learning (B to A) produced +0.0088 EES (+0.9%). This is a real but secondary contribution. The state-conditioned preference mechanism accumulated approach bias, increasing approach rate from 0.368 to 0.403. With higher approach rate and the resulting higher mean energy (0.428 vs 0.492), foraging success probability increased, compounding into higher per-approach yield.

The learning contribution is secondary not because learning is unimportant, but because the regulatory constraints determine whether the organism is in a regime where learning can be effective. Learning in Condition A is effective because drives and value function maintain mean energy in the mid-high range, where foraging is frequent and profitable. Constraints establish the operating regime; learning optimizes within it.

### 7.3 The C < D Result: Wrong Objective Versus No Objective

The result EES_C < EES_D deserves direct attention.

Condition C retained a world model, a survival value function, and a predictive processing system. It had more computational structure than Condition D (random). And yet it performed worse. The interpretation is that computational structure, without metabolic alignment, can be actively harmful.

The prediction-error minimization objective -- which drives the world model in the absence of energy and hunger signals -- is not aligned with energy efficiency. Prediction error is reduced most effectively by exploring an unpredictable environment. A system optimizing prediction error without constraint will explore extensively. In an environment where survival depends on foraging, this is maladaptive.

Condition D has no optimization objective. It samples actions uniformly. By chance, it selects approach roughly one third of the time. That is more than Condition C's 24.5%, and it is enough to maintain a higher mean energy (0.333 vs 0.206) and a higher EES.

This result has a specific implication: the claim that any structured optimization is better than random is false in the absence of objective alignment. The value of optimization is conditional on it being directed toward the right target. An optimization system directed at the wrong target can be worse than no optimization at all.

The replication results confirm this: across 8 runs of 15000 ticks, the C < D ordering was preserved without exception, with non-overlapping distributions. The failure is not stochastic -- it is structural.

### 7.4 Why Misaligned Optimization Fails

Condition C's failure was not a capacity failure. The organism was capable of selecting approach; it simply did not, because nothing in its objective function penalized energy loss. When optimization is decoupled from the survival-relevant outcome it is supposed to serve, the optimizer pursues its objective efficiently -- and that efficiency is what produces the harm.

Condition C was an effective prediction-error minimizer. Prediction error is minimized by exploration. The organism explored, and the exploration was metabolically costly with no survival benefit. The result was not incompetence but misalignment: a capable system consistently doing the wrong thing.

This is distinct from the random baseline failure mode. Condition D failed by chance: it selected suboptimal actions at random. Condition C failed by design: it selected suboptimal actions because they were optimal for its objective. A capable optimizer pursuing the wrong objective is worse than no optimizer, because it consistently and reliably produces the misaligned behavior. The replication data confirm this: Condition C's failure is not stochastic (std = 0.0004) -- it is structural.

The objective sweep confirms this at the mechanistic level. Adjusting the strength of prediction-error optimization (w_pe: 0.6 to 0.1) does not recover efficiency when the energy weight remains zero. EES is flat across all variants; explore rate barely shifts. The failure mode is not driven by PE being too strong -- it is driven by energy being structurally absent. Misalignment is not a matter of parameter tuning. It is a matter of which variables enter the objective at all.

### 7.5 Redundancy and Degenerate Optimization

The constraint ablation results reveal two additional properties of the system that the primary experiment did not test.

First, the regulatory mechanisms are redundant. No single constraint removal significantly degrades performance. Each mechanism has overlapping coverage with the others: hunger drive, world-model energy weight, and state-dependent temperature all push behavior toward foraging when energy is low, via different pathways. This is consistent with how biological control systems are organized: multiple overlapping mechanisms maintain homeostasis, such that damage to any one pathway does not immediately destabilize the organism.

Second, removing individual constraints can produce apparent metric improvements through degenerate strategies rather than genuine regulatory improvement. The A3 condition (no world-model energy weight) achieved the highest EES across all conditions, both in normal and stress environments. But this improvement was not adaptive: the organism collapsed to 94.7% approach behavior, accumulated energy far above equilibrium (mean 0.786 vs 0.433), and showed near-zero behavioral diversity.

The world-model energy weight (w_e = 1.0) in the full system serves as a dynamic regulator: when energy is high, the energy consequence of approach is low (already replete), and the system naturally diversifies to explore or withdraw. When energy is low, the energy consequence of approach is high, and the system concentrates on foraging. Removing this weight eliminates the state-dependent modulation. The hunger drive still fires below 0.25 energy, but once energy exceeds that threshold, nothing prevents continuous foraging. The result is an organism that hoards energy indefinitely, achieves high EES through accumulation rather than regulation, and abandons the behavioral diversity that would be required to handle a more complex or uncertain environment.

This is the key distinction between efficiency and behavioral integrity. EES captures energy efficiency across a fixed episode in a stable environment. It does not capture whether the organism would remain functional under novelty, threat, or changed conditions. The A3 strategy is fragile: its high EES depends on the continuous availability of foraging opportunity and the absence of any requirement to explore or withdraw.

---

## 8. Discussion

### 8.1 Constraints as Alignment Mechanisms

The standard framing of constraints in AI system design is negative: constraints limit what a system can do. The EEIL experimental results show a different framing. In a survival-relevant task, constraints serve as alignment mechanisms. They ensure that the optimization process -- whatever its objective -- stays connected to the actions that produce actual survival outcomes.

This framing has a specific consequence for AI system design. A system optimizing a proxy objective (prediction error, log-likelihood, reward signal) without metabolic or resource constraints will optimize the proxy, potentially at the expense of actual utility. Adding resource constraints to the optimization loop is not a limitation -- it is a correction mechanism that maintains alignment between the optimization objective and the operational requirement.

A key finding, confirmed by replication, is that misaligned optimization (Condition C) consistently underperforms random action (Condition D). The replication data -- C consistently below D across all 8 runs, with C_max (0.9856) below D_min (0.9863) -- shows this is not a stochastic artifact. It is a structural consequence of misalignment.

### 8.2 Alignment Is Necessary but Not Sufficient

The ablation results reveal a two-layer structure underlying efficient behavior.

The first layer is alignment: the optimization process must be coupled to survival-relevant variables. When this coupling is absent (Condition C), the system optimizes an unaligned proxy and performs worse than random. This is the EEIL alignment claim, confirmed in phases A and B.

The second layer is regulation: even within an aligned system, individual regulatory constraints prevent behavioral collapse. The A3 condition shows that removing the world-model energy weight -- while leaving hunger, temperature, and learning intact -- produces an organism that satisfies the alignment condition (it still responds to energy state through hunger drive and preference learning) but lacks one regulatory constraint. The result is not catastrophic misalignment, but degenerate optimization: the organism exploits the remaining pathways to pursue a narrow energy-accumulation strategy.

Both layers are required for meaningful efficiency. Alignment without regulation permits exploitation of the metric. An organism can achieve high EES by abandoning behavioral diversity, accumulating energy, and never diversifying -- all while technically remaining "aligned" with energy outcomes. Regulation prevents this by maintaining state-dependent modulation of behavior.

This finding is not visible in the primary experiment. The primary experiment removes all regulatory constraints simultaneously (Condition C), which produces misalignment. The ablation experiment removes them one at a time, which reveals degeneration. The two failure modes are distinct.

### 8.3 Efficiency vs Behavioral Integrity

The A3 condition highlights a key limitation of efficiency metrics: they can be maximized through pathological strategies that reduce behavioral diversity and adaptability.

EES measures energy efficiency across a fixed episode in a stable environment. It does not penalize behavioral monoculture. A system that selects approach 95% of the time in a stable foraging environment will achieve high EES -- but it will not explore, will not withdraw when threatened, and will not adapt its behavior to conditions where approach is not the correct action. Its efficiency is environment-specific and strategy-narrow.

The full system maintains behavioral diversity (approach 46%, explore 28%, withdraw 26%) alongside positive energy efficiency. This diversity is not waste -- it is the behavioral repertoire that would be needed to handle a more complex environment. The regulatory constraints that prevent the organism from collapsing to monoculture also maintain the organizational structure that adaptation requires.

This suggests that efficiency must be interpreted alongside behavioral structure, rather than as a standalone objective. A high EES is not evidence of adaptive efficiency if it is produced by a degenerate strategy.

### 8.4 Structural vs Parametric Alignment

The objective sweep reveals a critical distinction between parametric and structural alignment. Parameter tuning adjusts the strength of optimization. Structural alignment determines which variables enter the objective at all. These are different interventions with different consequences.

In Condition C, the energy weight was set to zero. This is a structural change: energy consequences are no longer part of what the system optimizes. Reducing w_pe from 0.6 to 0.1 adjusts how strongly the system optimizes PE -- but PE remains the only objective. The action distribution does not change, because nothing in the objective favors foraging over exploration regardless of how PE is weighted.

Misalignment between a system's optimization objective and its operational requirements cannot be corrected by adjusting loss weights or regularization parameters if the relevant variables are absent from the objective entirely. Tuning existing parameters cannot substitute for structural inclusion of survival-relevant variables.

### 8.5 Efficiency and Scale

The full constrained system in this experiment is small. Its neural architecture has three compartments; its action space has three options; its simulation runs for 5000 ticks. The random baseline operates in the same environment. The efficiency difference (EES_A vs EES_D = +3.9%) is not explained by scale. All conditions have the same scale. The difference is explained by structure.

This does not prove that biological efficiency would survive arbitrary scaling -- the relationship between scale and structural efficiency is an open empirical question. But it is consistent with the hypothesis that the source of biological efficiency is organizational rather than computational: it is the architecture of regulation, not the volume of computation, that produces efficiency.

---

## 9. Limitations

**Single environment.** All experiments were conducted in a single foraging environment with fixed resource dynamics. Phase B robustness experiments modified resource availability (foraging floor reduction), and the efficiency ordering was preserved. However, the generalizability to qualitatively different environments -- with different action-consequence structures, threat dynamics, or non-stationary reward distributions -- is not established.

**Simplified action space.** Three actions (approach, explore, withdraw) is a minimal behavioral repertoire. The behavioral collapse observed in A3 (95% approach) is a recognizable degeneration in this space. In a richer action space, degenerate strategies may be less visible and harder to detect through action distribution alone.

**Low sleep rate.** Observed sleep rates were uniformly low across all conditions (~6--7%). This is consistent across all conditions and does not affect between-condition comparisons, but limits interpretation of EES_total as a full-episode efficiency measure. Longer simulations or modified adenosine dynamics may produce more naturalistic sleep profiles.

**No long-term uncertainty or delayed reward structure.** The environment used here is stationary, fully observable, and without delayed consequences. Regulatory constraints may play a different -- and potentially more critical -- role in environments with delayed rewards, partial observability, or non-stationary dynamics. The A3 degenerate strategy would likely fail in such environments, as behavioral diversity becomes necessary for exploration and adaptation. This is consistent with the interpretation of w_e as a diversity-maintaining mechanism, but remains untested.

**Single learning mechanism.** Only one form of learning (local scalar preference biasing) was tested. More complex learning mechanisms -- temporal difference, model-based planning, episodic memory -- may produce different efficiency profiles and interact differently with regulatory constraints.

---

## 10. Conclusion

This work provides evidence that energy-efficient behavior depends on both structural alignment with survival-relevant variables and regulatory constraints that prevent degenerate optimization.

A primary experiment compared four conditions -- full constraints with learning, full constraints without learning, no constraints, and random policy -- across five runs of 5000 ticks. The full constrained adaptive system was the only condition achieving EES > 1.0. Removing regulatory constraints produced the largest single efficiency drop (-4.1%). The unconstrained optimizer performed below the random baseline, showing that misaligned optimization is not merely inefficient -- it is deterministically harmful relative to no optimization at all.

Replication and robustness testing show that this effect is stable under stochastic variation and environmental change. The efficiency ordering A > B > D > C was preserved across 8 runs of 15000 ticks and under reduced resource availability. Under scarcity, the full system showed adaptive energy recovery (drift = +0.183), while all other conditions stagnated or declined. An objective sweep demonstrated that the failure of the unconstrained system cannot be corrected by parameter tuning: EES in Condition C was flat across all tested values of w_pe, confirming that misalignment is a structural switch, not a dial.

Constraint ablation reveals that alignment is supported by redundant mechanisms: no single constraint removal significantly degrades performance, indicating overlapping coverage across the regulatory system. However, ablation of the world-model energy weight (A3) exposes a second failure mode -- degenerate optimization -- in which the system achieves high EES through behavioral collapse (94.7% approach, mean energy 0.786) rather than through adaptive balance. Under stress, this pattern persists and intensifies. High efficiency achieved through monoculture is not equivalent to adaptive efficiency: it is a metric-exploiting strategy that abandons the behavioral diversity required for generalization.

These findings suggest that efficient behavior is not a consequence of optimization strength alone, but of structured constraint systems that balance alignment and regulation. Alignment ensures that the optimization process is directed at survival-relevant outcomes. Regulation ensures that directed optimization does not collapse into a degenerate strategy that satisfies the metric while losing adaptive structure.

The core claim is precise: optimization without alignment is harmful; alignment without regulation is exploitable. Both are required.

---

## References

Frank, M.J. (2004). By carrot or by stick: cognitive reinforcement learning in parkinsonism. *Science*, 306(5703), 1940-1943.

Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., Cai, T., Rutherford, E., et al. (2022). Training compute-optimal large language models. *arXiv:2203.15556*.

Kaplan, J., McCandlish, S., Henighan, T., Brown, T.B., Chess, B., Child, R., et al. (2020). Scaling laws for neural language models. *arXiv:2001.08361*.

Schultz, W. (1998). Predictive reward signal of dopamine neurons. *Journal of Neurophysiology*, 80(1), 1-27.

Sterling, P. and Eyer, J. (1988). Allostasis: a new paradigm to explain arousal pathology. *Handbook of Life Stress, Cognition and Health*, 629-649.

Tononi, G. and Cirelli, C. (2006). Sleep function and synaptic homeostasis. *Sleep Medicine Reviews*, 10(1), 49-62.

---

*First draft — revised with replication (Phase A), robustness results (Phase B), and constraint ablation + degeneration analysis (Phase C). Internal document. Hitoshi AI Labs — NeuroSeed Project.*
*Word count: approximately 5000.*
