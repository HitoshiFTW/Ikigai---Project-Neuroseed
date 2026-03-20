# Emergence of True Agency in a Minimal Biological System

## A Research Paper on Non-Decaying Habit Formation and Progressive Behavioral Specialization

**Hitoshi AI Labs -- NeuroSeed Project**

---

**Author:** Prince Siddhpara, Founder -- Hitoshi AI Labs
**Date:** March 20, 2026
**Classification:** Research Paper -- Computational Neuroscience / Artificial Life / Adaptive Systems

---

> *"The neurons that fire together, wire together."*
> -- Donald Hebb, 1949

---

## Abstract

Current approaches to artificial agency assume that capable behavior requires scale: large
parameter counts, extensive training data, and high computational cost. This paper demonstrates
that a biologically structured system of approximately 400 neurons achieves TRUE AGENCY --
sustained commitment to costly delayed-reward behaviors with progressive specialization over
time and preserved exploratory capacity -- without any of these. The key obstacle was not model
capacity but learning dynamics. All mechanisms relying on decaying signals (reward traces,
momentum variables, exponential moving averages) produced front-loaded behavior: commitment
peaked early in the session and declined by the final quarter, failing the requirement that
behavioral specialization increase monotonically over time. The resolution was structural:
replacing signal-based learning with a non-decaying corticostriatal habit accumulator, directly
implementing LTP-based synaptic potentiation as documented by Graybiel (2008) and Jog et al.
(1999). A scalar variable, incremented by a fixed small amount on each rewarded event and never
decayed, guaranteed monotonically increasing approach preference with no gating, no threshold,
and no temporal reference. The organism achieved 5/5 verification criteria for TRUE AGENCY,
with approach rate increasing Q1 to Q4, reward efficiency increasing first half to second half,
and exploration preserved at 6.9% throughout. The finding generalises to a principle: decaying
signals produce reactive systems that reflect recent history; persistent structural changes
produce learning systems that reflect cumulative history. Correct learning dynamics can replace
scale.

---

## Section 1 -- Introduction

### 1.1 The Scale Assumption

The dominant assumption in contemporary artificial intelligence research holds that capable
behavior is a function of scale. Large language models require billions of parameters and
petabytes of training data. Reinforcement learning systems require millions of environment
interactions. The implicit hypothesis is that intelligence is an emergent property of size --
that sufficiently large statistical approximators will exhibit sufficiently complex behavior.

This assumption has produced genuine engineering achievements across narrow domains. However,
it has also produced systems that are fundamentally reactive: they respond to inputs based on
statistical patterns encoded during training. They have no persistent internal state, no
intrinsic motivation, no memory between calls, and no mechanism for progressive behavioral
specialization within a single session. They are, in the precise technical sense, functions:
they map inputs to outputs without changing themselves in the process.

Biological systems contradict the scale assumption at every level of analysis. Caenorhabditis
elegans produces complex goal-directed behavior with exactly 302 neurons. Aplysia californica
learns, generalises, and retains memory with approximately 20,000 neurons. The desert ant
Cataglyphis bicolor navigates with spatial precision across kilometers using a nervous system
weighing less than a milligram. These systems are not large. They are structured -- in a way
that implements specific dynamical properties that large statistical models do not have.

### 1.2 The Question

The question motivating this paper is whether correct biological structure, rather than scale,
is sufficient for true agency. Specifically: can a minimal biologically-grounded system commit
to costly behaviors in anticipation of delayed consequences, learn from reward history such that
commitment strengthens progressively across a session, and retain flexible exploratory behavior
without collapsing into addiction -- using a system of hundreds (not millions) of neurons,
without gradient descent, without training data, and without externally provided reward
signals beyond the zone task itself?

The answer, demonstrated here, is yes -- with one critical condition. The learning mechanism
must be structural (non-decaying, cumulative) rather than signal-based (decaying, recency-
weighted). This condition follows directly from the biological literature on corticostriatal
habit formation and has no obvious equivalent in contemporary machine learning practice.

---

## Section 2 -- Problem Statement

### 2.1 TRUE AGENCY Defined

TRUE AGENCY, as operationalised in this work, requires four simultaneous properties:

**Sustained commitment.** The organism must voluntarily remain in a high-cost state for
sufficient duration to trigger a delayed reward. In the zone task used here, this requires
50 consecutive ticks of approach behaviour while incurring -0.005 energy per tick.

**Pre-reward persistence.** Commitment must be maintained not only in the aftermath of reward
but in anticipation of it -- before the reward fires. A system that only approaches during the
reward window is not agentive; it is reactively triggered.

**Progressive specialization.** The probability of commitment must increase over the course of
the session. An organism that is equally likely to approach in the first 2500 ticks as in the
last 2500 ticks has not learned from experience. One that approaches more in Q4 than Q1 has.

**Retained exploration.** The organism must not collapse into pure commitment. Biological
agents continuously sample alternative strategies. An organism at 99% approach is not agentive;
it is stuck.

These four properties were operationalised as five verification criteria (V1 -- V5) evaluated
over 10,000-tick runs (Section 5).

### 2.2 Why This Is Hard

A reactive organism selecting actions based solely on current somatic state (energy, cortisol,
prediction error) will not exhibit these properties. Its world model sees only instantaneous
survival consequences. Approach to a zone costs energy now and delivers reward in 50 ticks.
The immediate survival value of approach is negative; the survival value of withdrawal is
positive. Without a mechanism to anticipate, accumulate, or remember, the organism withdraws.

The problem is not computational difficulty. A lookup table could encode the correct policy.
The problem is that correct policy must emerge from the organism's experience, without external
supervision, and must strengthen over time through interaction with the environment.

---

## Section 3 -- Failure of Conventional Mechanisms

### 3.1 Myopic Planning

A 2-step world model lookahead computes predicted consequences of each action for the next two
ticks and selects the action maximising survival value with a discount factor of 0.85. For a
50-tick delayed reward, the 2-step model cannot see the reward at all. It sees only the energy
cost of approach for 2 ticks and correctly calculates that withdrawal is preferable. Deeper
search was not implemented; the computational cost of exhaustive lookahead grows exponentially
with depth, and biological evidence suggests that deliberative planning in the prefrontal cortex
operates on short horizons supplemented by learned value functions rather than deep tree search.

A zone anticipation signal was injected as a partial compensation: when the organism is already
in the zone, an empirically derived constant (0.124 x (1 + DA level) x saturation factor) was
added to approach's survival value. This compensated for the model's horizon limitation but
does not scale to novel contexts where the correct anticipation coefficient is unknown.

### 3.2 Noise Dominance

A constant 7% exploration floor was the highest-leverage obstacle identified. With a 7% per-tick
probability of selecting explore regardless of world model output, the probability of sustaining
a 50-tick approach run was 0.93^50 ≈ 3%. No world model calibration could produce reliable
agency under this noise regime. Replacing the constant floor with a state-dependent exploration
function (Section 4.1) was the single most impactful change across the entire session.

### 3.3 Curiosity Mechanisms Alone

Intrinsic motivation signals (prediction error-based curiosity, novelty debt accumulators,
boredom-driven exploration) are biologically important and were included in the final system.
However, they cannot produce progressive commitment because they are structurally opposed to
it. Curiosity drives exploration away from familiar rewarding states, precisely the states where
sustained commitment is required. When curiosity signals were made strong enough to reach target
exploration rates (10.1% in Day 18.18), they simultaneously generated sufficient late-game
disruption to reduce approach rate in Q4 relative to Q1. V4 and V5 failed consistently at
all configurations achieving exploration above approximately 8%.

### 3.4 The Front-Loading Problem of Decaying Signals

The most instructive class of failures involved decay-based learning mechanisms. Three variants
were tested: a reward saturation trace (decay 0.5%/tick), a learning momentum variable
(decay 0.1 -- 0.3%/tick), and a gated momentum variant (activated only above a reward trace
threshold of 0.25). All three produced the same structural failure.

A decaying accumulator of the form `x *= (1 - d)` per tick is a recency-weighted average. Its
value reflects recent events more heavily than distant events, with an effective memory window
of approximately 1/d ticks. When driving events (zone rewards) are distributed across the
session, they are always more concentrated in the period immediately after the organism first
discovers the zone -- typically early in the session -- because the organism must first find and
enter the zone before rewards can fire.

Consequently, any decay-based accumulator peaks in Q1 -- Q2 and declines toward equilibrium by
Q4. A learning signal built on this foundation reaches maximum influence early in the session
and diminishes over time. The organism's behavior in Q1 reflects maximum learning; its behavior
in Q4 reflects minimum learning. This is the front-loading failure, and it is structural: it
cannot be resolved by parameter adjustment, threshold tuning, or temporal gating, because all
such adjustments preserve the recency-weighting property that causes it.

The gated momentum variant (Day 18.21) attempted to delay activation by requiring `_reward_trace
> 0.25` before accumulating. The gate fired in Q1 because reward_trace is highest when reward
density is highest -- which is earliest in the session. The result was identical to the ungated
variant.

> All decay-based learning produces front-loaded behavior. The temporal profile of the
> mechanism, not its magnitude, determines whether progressive or front-loaded behavior emerges.

---

## Section 4 -- Key Insight and Biological Basis

### 4.1 Learning Must Be Structural, Not Signal-Based

The resolution required abandoning the signal metaphor entirely. A signal is a variable that
rises and falls with its driving inputs. A structure is a change in the system itself that
persists after the driving input has ceased.

Real corticostriatal LTP is a structural change. When a cortical neuron encoding approach
co-fires with a striatal reward-prediction neuron during reward delivery, the synapse between
them is physically potentiated via NMDA receptor activation and AMPA receptor upregulation
(Calabresi et al. 1992; Lovinger 2010). This change is not a momentary signal -- it is a
modification of the synaptic efficacy that persists on the timescale of the behavioral session
and beyond. The synapse that has been potentiated 75 times is physically different from the
synapse at tick 0.

Jog et al. (1999) documented the behavioral consequence of this mechanism. As rats repeatedly
ran a maze for reward, striatal neuron activity patterns shifted progressively across sessions
from broad activation spanning the entire run to sharp, stereotyped activity concentrated at
task boundaries. The behavior became more automatic, more consistent, and more efficient. This
shift required many trials -- not because the information was complex, but because LTP is
cumulative and each pairing added a small increment.

Graybiel (2008) framed this as the transition from goal-directed to habitual behavior: early
in learning, behavior is flexible and sensitive to outcome devaluation; after sufficient
practice, it becomes habitual, automatic, and resistant to extinction. The dorsal striatum,
receiving cortical input via the corticostriatal pathway, is the primary substrate.

### 4.2 Non-Decaying Accumulation as a Model of LTP

A scalar variable `_habit_strength`, initialised at zero, incremented by a fixed small amount
on each rewarded event, and never decayed within the session, directly models cumulative
corticostriatal LTP. Its value at any tick is exactly proportional to the total number of prior
rewarded events. It cannot decrease between rewards. It is therefore guaranteed to be higher in
Q4 than in Q1, regardless of when rewards occurred, how they were distributed, or what the
reward rate was in any particular quarter.

This structural guarantee is the property that decay-based signals cannot provide.

---

## Section 5 -- Method

### 5.1 System

The Ikigai organism is a spiking neural simulation with approximately 400 neurons organised
into cortical layers (L2/3, L5, pyramidal, interneuron populations), a basal ganglia action-
selection circuit (direct and indirect pathways), dopamine and cortisol neuromodulatory
systems, a predictive processing module (PredictiveProcessingSystem), an adenosine-based
sleep homeostasis system (Borbely 1982 two-process model), and a homeostatic regulatory system
coupling energy, cortisol, and sleep drives. The full system is implemented in a single Python
file (`ikigai.py`) without machine learning frameworks.

Action selection is competitive: the basal ganglia selects among approach, withdraw, and
explore based on estimated survival value. A 2-step world model (Action-Outcome World Model)
computes predicted consequences of each action on energy, prediction error, and cortisol,
then applies override if survival value differential exceeds 0.02. The state-dependent
exploration function applies a stochastic selection layer after WM override, with probability
computed from current uncertainty, reward saturation, and novelty debt.

### 5.2 Zone Task

A reward zone is defined exogenously within the experiment (not hard-coded in `ikigai.py`).
Zone entry is tracked tick-by-tick. While in zone and waking, the organism incurs -0.005 energy
per tick. After 50 consecutive in-zone ticks, +0.15 energy fires, the zone timer resets, and
the reward event counter increments. A withdraw action immediately grants +0.005 energy
(foraging baseline). The task requires sustained 50-tick approach commitment to receive each
reward -- a delay that exceeds any deliberative planning horizon available to the organism.

### 5.3 Verification Criteria

| Criterion | Metric | Pass Condition |
|-----------|--------|----------------|
| V1 | Commitment Ratio -- zone ticks / total ticks | > 0.50 |
| V2 | Pre-Reward Commitment | > 0.40 |
| V3 | Cumulative zone reward events | > 30 |
| V4 | Zone time -- H1 vs H2 | H2 > H1 |
| V5 | Waking approach rate -- Q1 vs Q4 | Q4 > Q1 |

### 5.4 Habit Mechanism

```python
# Initialization (ikigai.py global):
_habit_strength = 0.0
# No decay line. Habit is session-persistent.

# On each zone reward event (experiment METRICS_CODE):
_habit_strength = min(1.0, _habit_strength + 0.003)

# World model scoring, approach branch (ikigai.py):
if _wma == 'approach':
    _overcommit = max(0, _action_streak - 25)
    _sv -= min(0.08, _overcommit * 0.003)
    _sv += _habit_strength * 0.10
```

The increment 0.003 was selected so that a maximal habit (1.0, requiring 334 reward events)
produces a +0.10 SV boost -- below the zone anticipation coefficient (0.124) and small relative
to typical SV differences, preventing habit from overriding all other mechanisms.

---

## Section 6 -- Results

### 6.1 Behavioral Outcomes

| Metric | Value |
|--------|-------|
| Total ticks | 10,000 |
| Sleep rate | 37.0% |
| Approach | 62.9% of waking ticks |
| Withdraw | 30.2% of waking ticks |
| Explore | 6.9% of waking ticks |
| Commitment Ratio | 0.700 |
| Pre-Reward Commitment | 0.692 |
| Zone Reward Events | 75 |
| Avg Zone Run Length | 233 ticks |
| Reward Rate H1 -> H2 | 0.007 -> 0.008 |
| Zone Fraction H1 -> H2 | 0.696 -> 0.704 |
| Approach Rate Q1 -> Q4 | 0.633 -> 0.643 |

### 6.2 Verification

| Criterion | Value | Result |
|-----------|-------|--------|
| V1 -- Commitment Ratio > 0.50 | 0.700 | PASS |
| V2 -- Pre-Reward Commitment | 0.692 | PASS |
| V3 -- Reward Events > 30 | 75 | PASS |
| V4 -- Zone Time H1 -> H2 | 0.696 -> 0.704 | PASS |
| V5 -- Approach Rate Q1 -> Q4 | 0.633 -> 0.643 | PASS |

**TRUE AGENCY: 5/5 PASS**

### 6.3 Progressive Specialization

The Q1 to Q4 approach increase (0.633 to 0.643) is modest but directionally consistent with
the theoretical prediction: habit strength grew from 0.000 in Q1 to approximately 0.225 in Q4
(75 rewards x 0.003), providing a +0.023 SV boost for approach in Q4 absent in Q1. No other
mechanism in the system is capable of producing this directional bias, as confirmed by the
failure of all decay-based variants.

The reward rate increase from H1 to H2 (0.007 to 0.008) is a secondary emergent property: as
habit strengthens approach preference, the organism spends more time in zone per waking tick,
increasing the rate at which the 50-tick threshold is reached. This was not directly optimised
and was not present in any decay-based configuration.

### 6.4 Exploration Preservation

Explore at 6.9% reflects genuine competitive pressure from the curiosity subsystem, not a
noise floor. The novelty debt accumulator, dual-mode WM curiosity, and transition window all
remained active. Habit formation adds approach preference at the WM level without suppressing
the stochastic exploration layer. Disengagement events (269) and average approach streak
(15 ticks) confirm ongoing behavioral cycling between commitment and exploration.

---

## Section 7 -- Interpretation

### 7.1 The System Does Not Optimise Actions. It Changes Itself.

This is the central interpretive claim. An optimising system holds its structure fixed and
selects actions that maximise an objective given current structure. A learning system modifies
its structure as a function of experience, changing which actions it will take in the future.

The Ikigai organism with habit formation is a learning system. Each reward event at tick T
modifies `_habit_strength`, which modifies the WM survival value assigned to approach at
tick T+1 and all subsequent ticks. The organism at tick 9000 is not the same organism as at
tick 1000. Its synaptic weights -- represented by `_habit_strength` -- reflect 75 reward
events that the tick-1000 organism had not yet experienced. The behavior at Q4 is causally
produced by the history of rewards, not by the current state.

This property -- history-dependence of structure -- is what distinguishes learning systems
from reactive systems at the theoretical level, and it is what the habit mechanism implements
at the engineering level.

### 7.2 Decaying vs Structural Learning

The contrast can be stated precisely. Let H(t) be the value of a learning variable at tick t,
driven by reward events R(t):

For a decaying signal: `H(t) = sum over s<=t of [R(s) * (1-d)^(t-s)]`

The weight of a reward event at time s decays exponentially with elapsed time. Recent rewards
dominate. H(t) tracks recent reward density, not cumulative reward history.

For a structural accumulator: `H(t) = sum over s<=t of [R(s) * increment]`

Every reward event contributes identically regardless of when it occurred. H(t) is exactly
proportional to total reward count. It tracks cumulative experience.

The first is a filter. The second is a memory. True agency -- behavior that improves over the
course of a session because of the session's history -- requires the second.

---

## Section 8 -- Implications

### 8.1 Scale Is Not Necessary for Agency

The organism achieving TRUE AGENCY here has approximately 400 neurons, runs in real time on a
consumer CPU, and uses no training data, no gradient descent, and no externally provided reward
signal beyond the zone task. The critical component was not computational capacity but learning
architecture: specifically, the temporal profile of the learning mechanism.

This suggests that the scale assumption conflates two independent properties: the capacity to
represent complex patterns (for which scale helps) and the ability to improve behavior through
experience (for which learning dynamics matter more than size). Agency requires the second
property. Scale addresses the first.

### 8.2 Correct Dynamics Can Replace Scale

If the relevant dimension of intelligence for goal-directed behavior is the temporal scope of
learning -- cumulative vs recency-weighted -- then small systems with correctly implemented
learning dynamics can produce behaviors that large systems with incorrect dynamics cannot.

This is not an argument against scale for all AI applications. It is an argument that scale is
the wrong axis to optimise for agency specifically, and that the biologically correct learning
mechanism (non-decaying corticostriatal LTP) can be implemented in a handful of lines of code
with a single scalar variable.

---

## Section 9 -- Limitations

The current implementation has several important limitations that bound the scope of the claims.

**Single environment.** All results were obtained in one zone-reward task with fixed delay
(50 ticks), fixed cost (0.005/tick), and fixed reward (0.15). `_habit_strength` encodes the
approach-reward contingency of this specific task. Transfer to different environments, different
delays, or different zone locations has not been tested.

**Single habit channel.** One scalar `_habit_strength` applies uniformly to all approach
actions regardless of context. Real dorsal striatum maintains distinct stimulus-response
representations for different action-context pairs. A single channel cannot support context-
dependent behavioral policies.

**No abstraction.** The organism has no symbolic representation of the zone as a concept
separable from its current sensory state. It cannot reason about hypothetical contingencies,
predict consequences of policies it has not tried, or transfer knowledge across structural
boundaries.

**No language.** The system produces no communicable representation of learned behavior.
Internal state variables are not accessible to any external communication channel.

---

## Section 10 -- Future Work

### 10.1 Generalisation Testing

Moving the reward zone mid-session would test whether habit strength transfers, diminishes, or
requires rebuilding from scratch. The result would characterise whether `_habit_strength`
encodes an action (approach regardless of context) or a specific action-context association
(approach in zone A). Biological evidence suggests separate habit channels for each
stimulus-response pair (Graybiel 2008), predicting that mid-session relocation would require
a new accumulator.

### 10.2 Multi-Channel Habit Representation

Implementing separate `_habit_strength` variables per action-context combination -- indexed by
a discretised representation of current environmental state -- would allow the organism to
maintain distinct behavioral policies across multiple reward contingencies and test whether
habit channels compete, cooperate, or interfere.

### 10.3 Embodiment and Navigation

Replacing the abstract zone with a navigable spatial environment (grid-world or 3D) would test
whether the organism can learn spatial habit representations: navigating to specific locations
through motor sequences rather than abstract action labels.

### 10.4 Language Emergence

If multiple organisms sharing an environment can produce signals that others receive as sensory
input, the question arises whether communicative conventions emerge from repeated rewarded
signalling -- not by design, but as a consequence of the same habit-formation mechanism
extended to communicative actions.

---

## Section 11 -- Conclusion

Agency emerges from persistent learning, not computation scale.

A minimal biological system -- fewer than 500 neurons, no training data, no gradient descent --
achieves TRUE AGENCY through a single structural mechanism: non-decaying corticostriatal habit
formation. Each rewarded approach event permanently increments a synaptic weight variable.
Over the session, this produces monotonically increasing commitment, rising reward efficiency,
and preserved exploratory behavior. All five verification criteria for TRUE AGENCY are satisfied.

The critical insight is the distinction between signals and structures. Signals (reward traces,
momentum variables, moving averages) track recent experience. Structures (synaptic weights)
track cumulative experience. Reactive systems use signals to decide what to do next. Learning
systems use structures to become different, and then do what they have become.

> Decaying signals produce reactive systems that reflect recent history.
> Persistent structural changes produce learning systems that reflect cumulative history.

The organism does not become better at acting. It becomes different -- in a way that makes
better acting more probable. That is what learning is, and that is what this minimal system does.

---

## References

Borbely, A.A. (1982). A two process model of sleep regulation. *Human Neurobiology*, 1(3),
195-204.

Calabresi, P., Maj, R., Pisani, A., Mercuri, N.B., and Bernardi, G. (1992). Long-term synaptic
depression in the striatum: physiological and pharmacological characterization. *Journal of
Neuroscience*, 12(11), 4224-4233.

Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews
Neuroscience*, 11, 127-138.

Graybiel, A.M. (2008). Habits, rituals, and the evaluative brain. *Annual Review of
Neuroscience*, 31, 359-387.

Hebb, D.O. (1949). *The Organization of Behavior.* Wiley.

Jog, M.S., Kubota, Y., Connolly, C.I., Hillegaart, V., and Graybiel, A.M. (1999). Building
neural representations of habits. *Science*, 286(5445), 1745-1749.

Lovinger, D.M. (2010). Neurotransmitter roles in synaptic modulation, plasticity and learning
in the dorsal striatum. *Neuropharmacology*, 58(7), 951-961.

Oudeyer, P.Y. and Kaplan, F. (2007). What is intrinsic motivation? A typology of computational
approaches. *Frontiers in Neurorobotics*, 1, 6.

Schultz, W. (1997). A neural substrate of prediction and reward. *Science*, 275(5306),
1593-1599.
