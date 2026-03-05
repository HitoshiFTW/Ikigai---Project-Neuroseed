# Ikigai -- Full System Biological Audit

**Project NeuroSeed -- Hitoshi AI Labs**

**Date:** March 5, 2026
**Classification:** Internal Technical Audit -- Computational Neuroscience
**Author:** Automated audit generated from codebase analysis of `ikigai.py`

---

## 1. System Overview

Ikigai is a single-file Python simulation (~4,400 lines) implementing a spiking neural network coupled with neuromodulatory, endocrine, cognitive, and social subsystems. It runs in discrete timesteps ("ticks") of 1000 ticks per session. The system persists state to disk between sessions via JSON serialization.

### Architecture Summary

| Component | Count |
|---|---|
| Core neurons | 40 (named, hand-wired) |
| Layer 23R neurons | 60 (regional populations) |
| Total neurons | 100 |
| Inhibitory interneurons | 2 |
| Excitatory synapses | ~170 |
| Inhibitory synapses | 2 |
| Neuromodulator systems | 7 |
| Brain region models | 6 |
| Cognitive subsystems | ~25 |

### What It Represents

Ikigai is presented as a "digital organism" -- a minimal agent with spiking neurons, emotional states, personality, memory, sleep, language, social cognition, and dreams. Conceptually, it attempts to model a single developing mind from neural dynamics up through higher cognition.

The system does not simulate any specific biological organism. It is a hybrid architecture: a small spiking network at the bottom, with scripted cognitive systems layered on top.

---

## 2. Neural Model

### Neuron Dynamics

The `Neuron` class implements a **leaky integrate-and-fire (LIF)** model with the following dynamics:

```
v(t+1) = v(t) * leak + input * gain
if v >= threshold: fire, reset v=0
```

| Property | Implementation | Biological Analogue | Accuracy |
|---|---|---|---|
| Membrane potential | Single scalar voltage | Aggregate dendritic depolarization | Low -- no ion channels, no reversal potentials |
| Leak | Multiplicative decay (0.9-0.98) | Passive membrane conductance | Functional approximation |
| Threshold | Adaptive (0.3-1.5 range) | Sodium channel activation threshold | Functional approximation |
| Refractory period | Integer timer (1-3 ticks) | Absolute + relative refractory | Correct concept, coarse timing |
| Intrinsic noise | Gaussian (sigma=0.005) | Ion channel stochasticity | Correct principle (Faisal 2008) |
| Calcium fatigue | Accumulates on spike, decays 0.95/tick | Calcium-dependent adaptation | Functional -- missing calcium dynamics |
| Intrinsic plasticity | Threshold adapts toward target rate | Turrigiano 1998 homeostatic | Correct concept, simplified implementation |

### Assessment

The neuron model is a standard LIF with biologically motivated additions (calcium fatigue, intrinsic plasticity, noise). It is **not** a conductance-based model. There are no ion channel dynamics, no dendritic compartments, no synaptic reversal potentials, no action potential waveform. The voltage is unitless and has no biophysical correspondence.

This is typical of computational neuroscience at the "network-level" abstraction. The model is biologically inspired but not biologically accurate at the single-neuron level.

**Realism: 3/10.** Functional approximation of spiking. Missing all biophysical detail.

---

## 3. Network Architecture

### Topology

The network is **hand-wired** with named neurons representing specific brain regions:

- **Input/Hidden/Output**: ni, nh, no (core feedforward pathway)
- **Inhibitory**: Ih1, Ih2 (2 interneurons)
- **Sensory**: Sens-001 to 003
- **Association**: Assoc-001 to 003
- **Motor**: Motor-001, Motor-002
- **Prefrontal**: PFC-001 to 005
- **ACC**: ACC-001 to 003
- **Insula**: Insula-001 to 003
- **VTA/NAc**: VTA-001/002, NAc-001/002
- **Hippocampal**: CA3-001/002, CA1-001/002
- **Language**: Wernicke-001 to 003, Broca-001 to 003
- **Bridge**: Bridge-001, Bridge-002
- **Layer 23R populations**: OFC(5), aIns(4), BG(6), lPFC(5), PPC(4), TP(4), CB(6), SMA(4), NB(3), RH(9), CL(5), MC(5)

### EI Ratio

| Property | Value | Biological Target |
|---|---|---|
| Excitatory neurons | 98 | ~80% of cortical neurons |
| Inhibitory neurons | 2 | ~20% of cortical neurons |
| EI neuron ratio | 49:1 | 4:1 |

The EI neuron ratio is **biologically incorrect by an order of magnitude**. The system compensates through a "population compression factor" (`population_scale = 3.0 + 0.5/scale`) that treats each inhibitory neuron as representing ~3.5 biological interneurons. This is a mathematical workaround, not a structural solution.

### Connectivity

- Connections are **sparse and hand-wired** between named neurons
- L23R neurons are connected in fan-in/fan-out patterns (each population receives input from one core neuron, projects to one downstream neuron)
- No random connectivity, no distance-dependent wiring, no cortical columns
- Connection probability is effectively deterministic (each synapse is placed manually)

### Assessment

The architecture does not resemble biological cortex. Real cortex has:
- ~20% inhibitory neurons with diverse subtypes (PV, SST, VIP)
- Random sparse connectivity (~10% connection probability)
- Columnar organization with layer-specific connections
- Distance-dependent falloff of connection probability
- Recurrent excitatory-inhibitory microcircuits

The hand-wired topology is closer to a "concept map" than a neural network -- each neuron represents a region, not a cell.

**Realism: 2/10.** Named neurons function as symbolic nodes, not as biological populations.

---

## 4. Plasticity and Learning

### STDP (Spike-Timing-Dependent Plasticity)

```python
dt = pre.last_spike_tick - post.last_spike_tick
td = exp(-|dt|/20) if dt > 0 else -exp(-|dt|/20)
eligibility_trace += td
```

| Property | Implementation | Biological Evidence | Accuracy |
|---|---|---|---|
| STDP window | Exponential, tau=20 ticks | Bi et al. 1998, Song et al. 2000 | Correct functional form |
| Pre-before-post | Positive (LTP) | Standard STDP | Correct |
| Post-before-pre | Negative (LTD) | Standard STDP | Correct |
| Eligibility trace | Accumulates STDP, decays with tau=25 | Izhikevich 2007 three-factor | Correct concept |
| Inhibitory plasticity | Excluded from STDP | Vogels et al. 2011 iSTDP | Inaccurate -- inhibitory STDP exists and is important |

### Three-Factor Learning

```python
dw = eligibility * da_level * 0.01 * modifiers
```

The weight update combines:
1. Eligibility trace (STDP timing)
2. Dopamine level (reward signal)
3. Serotonin, myelination, adenosine modifiers

This implements the three-factor learning rule (Izhikevich 2007): STDP + neuromodulatory gating. The biological concept is valid. However:

- Weight changes are **accumulated during waking** but **applied only during sleep** (`consolidate()`). This enforces sleep-dependent consolidation (correct concept) but is implemented as a hard gate rather than gradual process.
- No homeostatic normalization of total synaptic weight per neuron
- No metaplasticity (BCM-style sliding threshold)

### Homeostatic Plasticity

1. **Intrinsic threshold plasticity**: Neurons track their firing rate and adjust threshold. Target rate: 10%. Time constant: ~20 ticks, learning rate eta=0.001/scale. This correctly implements Turrigiano (1999) homeostatic plasticity.
2. **Synaptic scaling in consolidate()**: Slow pull toward initial weight (tau=5000 ticks). Correct concept (Turrigiano 2008) but applied only during sleep consolidation call.
3. **PI controller for EI balance**: Adjusts inhibitory synaptic weights based on EI ratio error. This is functionally analogous to inhibitory STDP (Vogels et al. 2011) but implemented as an explicit control loop, not as a learning rule.

### Myelination

Synapses track usage count and progressively reduce transmission delay (2 -> 1 -> 0 ticks). Based on Fields 2008. The concept is biologically valid -- activity-dependent myelination is real. However, real myelination changes conduction velocity continuously, not in discrete steps.

### Assessment

The plasticity system has the right qualitative structure: STDP for associative learning, three-factor for reinforcement learning, homeostatic plasticity for stability, myelination for speed. The approximation level is coarse but conceptually sound.

**Realism: 4/10.** Correct principles, highly simplified implementations.

---

## 5. Neuromodulators and Emotion

Ikigai implements 7 neuromodulator/hormone systems:

### DopamineSystem

| Property | Implementation | Biological System |
|---|---|---|
| Tonic level | Baseline 0.5, slow drift | VTA tonic DA (Grace 1991) |
| Phasic burst | Positive RPE: +0.03/tick | Burst firing on unexpected reward (Schultz 1997) |
| Phasic dip | Negative RPE: -0.02/tick | Pause on omitted reward |
| Prediction error | da.update(output_fired) | Temporal difference-like |
| Cooldown | Phasic cooldown timer | Reuptake delay |

Assessment: The tonic/phasic separation and RPE signal are biologically correct in concept. The values are arbitrary and the prediction error computation is simplified (no explicit value function or temporal difference).

### SerotoninSystem

Tracks average firing rate over a 20-tick window. Level moves toward 0.6 setpoint. The implementation is minimal -- serotonin in biology affects mood, appetite, and sleep through 14 receptor subtypes. Here it is a single scalar "population activity average." **Very simplified.**

### NorepinephrineSystem

Responds to signal magnitude changes (surprise detection). Elevates on large input changes (delta > 0.3), decays when stable. Tracks "elevated_ticks" for sustained arousal. This correctly captures the phasic NE response to novel/salient stimuli (Aston-Jones & Cohen 2005). Missing: tonic NE modulation of signal-to-noise ratio, LC dynamics.

### AcetylcholineSystem

Responds to novelty, modulates synaptic gain. Single scalar. In biology, ACh has distinct functions in cortex (attention, gain modulation) vs hippocampus (encoding vs retrieval). Here it is one value.

### CortisolSystem

| Property | Implementation | Biological System |
|---|---|---|
| Stress response | Rises on novelty output failure, NE elevation | HPA axis cortisol release |
| Chronic stress | Accumulates over sustained high levels | Allostatic load |
| Synaptic atrophy | High cortisol degrades target synapse weights | McEwen 2007 dendritic remodeling |
| Circadian decay | Higher decay during REM sleep | Cortisol circadian rhythm |
| Oxytocin buffering | Reduced cortisol when oxytocin high | Social buffering |

This is one of the more developed neuromodulator systems. The cortisol-oxytocin interaction and stress-recovery dynamics capture real HPA axis behavior at a functional level.

### AdenosineSystem

Sleep pressure accumulator. Builds with cortical activity, clears during sleep. Models the adenosine sleep drive (Porkka-Heiskanen et al. 1997). Functional and biologically appropriate.

### OxytocinSystem

Rises on positive social interaction (output fired + DA high + cortisol low). Modulates trust, synaptic pruning. Based on Kosfeld et al. 2005. Simplified but conceptually valid.

### Assessment

The neuromodulatory systems capture the right qualitative frameworks: dopamine RPE, cortisol stress, adenosine fatigue, oxytocin trust. They interact correctly (cortisol-oxytocin buffering, dopamine-serotonin balance). However, each is a single scalar value rather than a spatially distributed system with receptor subtypes.

**Realism: 4/10.** Correct functional roles, drastically simplified dynamics.

---

## 6. Cognitive Systems

The system contains approximately 25 higher-level cognitive subsystems. Critical evaluation:

### Episodic Memory (EpisodicMemorySystem)

- Stores events as dictionaries with environment vector, neuromodulator state, valence, and active assemblies
- Encodes based on significance threshold
- Retrieval uses manual matching, not neural pattern completion
- **Verdict: Scripted.** Memory is a Python list with manual encode/retrieve logic. No neural mechanism drives storage or recall -- hippocampal neurons (CA3, CA1) exist but memory operations bypass them entirely.

### Hippocampus (HippocampusSystem)

- Computes novelty by cosine distance between current input pattern and stored patterns
- "Process" function decides ENCODE or MATCH based on similarity threshold
- **Verdict: Scripted.** The hippocampal neurons fire based on synaptic input, but the HippocampusSystem class operates independently, using its own internal pattern list.

### Working Memory (WorkingMemorySystem)

- Fixed-slot buffer (capacity 5) with TTL-based decay
- Items are text labels, not neural activity patterns
- Adenosine reduces capacity; dlPFC activity extends TTL
- **Verdict: Scripted.** Goldman-Rakic 1995 concept implemented as a fixed-size Python list, not as persistent neural activity.

### Predictive Processing (PredictiveProcessingSystem)

- Maintains a running prediction (exponential average) and computes prediction error
- Generates learning boost from large errors
- **Verdict: Scripted.** Friston 2010 free energy principle referenced but implemented as a simple rolling average predictor. No hierarchical generative model.

### Cell Assemblies (CellAssemblySystem)

- Dictionary of named assemblies (THREAT, SAFETY, CURIOSITY, etc.) with activation thresholds
- Activated by neuromodulator conditions (e.g., high cortisol -> THREAT active)
- **Verdict: Scripted.** Assemblies are hard-coded labels activated by if-then rules on neuromodulator levels. They are not neural ensembles that form through Hebbian learning. The name "cell assembly" references Hebb 1949 but the implementation has no relation to Hebbian assembly formation.

### Dream System (DreamSystem)

- During REM: randomly selects 2 episodic memories, recombines attributes
- 40% chance per REM tick of generating a dream
- Processes emotional memories (reduces valence by ~15%)
- Generates prospective simulations
- **Verdict: Scripted.** Dreams are template-based text generation from randomly recombined memory attributes. There is no replay of neural activity patterns. The concept (Hobson & McCarley 1977 activation-synthesis) is referenced but not implemented neurally.

### Metacognition (MetacognitionSystem)

- Confidence scoring for retrieved memories
- Uncertainty detection from conflicting motor commands
- Second-order statement generation ("I think I know this")
- **Verdict: Scripted.** No second-order neural representations. Metacognitive statements are generated by if-then rules on confidence thresholds.

### Emotional Regulation (EmotionalRegulationSystem)

- Two strategies: cognitive reappraisal (PFC-mediated) and expressive suppression
- Wisdom computed from fear-recovery memory patterns
- Dysregulation tracking from sustained high cortisol
- **Verdict: Scripted.** Gross 1998 process model implemented as explicit strategy selection logic. Regulation is not emergent from PFC-amygdala neural dynamics.

### Language / Grammar (GrammarEmergenceSystem, SemanticEmergenceSystem)

- Sentence generation from templates and active assemblies
- Construction grammar patterns detected from assembly co-activation sequences
- Core vocabulary is hard-coded
- **Verdict: Scripted.** Language is template-based text generation. The word "emergence" in the class name is aspirational. Vocabulary is predefined. Sentences are constructed by pattern matching on system state.

### Social Cognition (AttachmentSystem, EmpathySystem, TheoryOfMindSystem)

- Attachment score tracks presence responsiveness
- Empathy detects presence state changes
- Theory of Mind processes intention/belief attribution
- **Verdict: Scripted.** All social systems operate on explicit if-then logic using presence entity state variables. No neural mechanism for social representation.

### Personality / Big Five

- Big Five traits (O, C, E, A, N) updated every 10 ticks
- Mapped to regional activity averages (claustrum -> O, PFC -> C, etc.)
- Day 11 modifications: A uses oxytocin-coupled drift, N uses two-timescale integration
- **Verdict: Mixed.** Traits are derived from actual neural firing rates in some regions, so there is a partial connection to neural dynamics. However, the mapping itself (regional -> trait) is hard-coded and the trait update formulas are scripted.

### Assessment

The overwhelming majority of cognitive systems are **scripted**, not emergent. They are Python classes that implement psychological theories as explicit if-then logic on system state variables. The neural network at the bottom produces firing patterns, but the cognitive systems do not read those patterns through neural mechanisms. Instead, they operate through direct variable inspection.

**Realism: 2/10.** Psychological concepts implemented as code, not as neural computation.

---

## 7. Scaling Laws

Day 11 introduced several population-scaling mechanisms:

| Mechanism | Formula | Biological Analogue |
|---|---|---|
| PI controller | delta = k_p*error + k_i*integral | Inhibitory STDP (Vogels 2011) |
| Rate-based normalization | pop_scale = mean_rate / baseline | Divisive normalization (Carandini 2012) |
| Adaptive population scale | 3.0 + 0.5/sqrt(N/100) | Interneuron compression |
| Intrinsic plasticity scaling | eta = 0.001/scale | N-dependent homeostasis |
| Motor noise scaling | sigma = 0.025 + 0.008/scale | Stochastic decision circuits |
| EI homeostasis scaling | k1, k2 / scale | Gain adaptation |

### Assessment

These scaling laws produce stable EI ratio, firing rate, and conflict density across N=50 to N=400. The PI controller and divisive normalization are biologically grounded concepts. However:

- Real cortex scales through structural mechanisms (connectivity patterns, inhibitory subtypes, columnar organization), not through parametric tuning of controller gains
- The scaling laws are tuned to this specific architecture (2 inhibitory neurons, hand-wired topology) and would not generalize to arbitrary network structures
- The "conflict density" and "trait variance" metrics are artifacts of the scripted cognitive systems, not natural neural observables

**Realism: 5/10.** Mathematically sound scaling, biologically motivated but architecturally specific.

---

## 8. Emergent vs Scripted Behavior

### Emergent Behaviors

Behaviors arising from neural dynamics without explicit programming:

- Spike patterns across neurons from synaptic input summation
- Firing rate adaptation from intrinsic plasticity
- EI balance from PI controller feedback
- Synaptic weight consolidation through STDP + three-factor learning
- Myelination of frequently used pathways
- Motor competition from WTA inhibitory feedback
- Activity-dependent threshold adaptation
- Fatigue from calcium accumulation
- Adenosine-driven changes to leak and synaptic failure

### Scripted Behaviors

Logic explicitly programmed as if-then rules in Python:

- All language generation (vocabulary, sentences, grammar, questions, narratives)
- All memory operations (hippocampal encoding, retrieval, episodic storage)
- All cell assembly activation (hard-coded thresholds on neuromodulator levels)
- Dream generation (random memory recombination with templates)
- Metacognitive statement generation
- Emotional regulation strategy selection
- Social awareness, empathy, and theory of mind
- Attachment style classification
- Personality trait mapping (regional activity -> Big Five)
- Somatic marker mode selection (APPROACH, AVOID, ANXIOUS, NEUTRAL)
- Conflict resolution
- Executive function evaluation
- Curiosity drive classification (epistemic vs anxiety)
- Working memory slot management
- Predictive processing (rolling average predictor)
- Sensory environment event generation
- Presence entity behavior
- Compassion, gratitude, self-compassion, mission detection
- Narrative self-model and autobiography
- Self-improvement awareness
- Learning awareness

### Ratio

Approximately **10-15% of system behavior is emergent** from neural dynamics. The remaining **85-90% is explicit procedural logic** operating on system state variables.

---

## 9. Biological Accuracy Score

| Dimension | Score (0-10) | Justification |
|---|---|---|
| Neuron realism | 3 | LIF with calcium fatigue and noise. No biophysics. |
| Network architecture | 2 | Hand-wired named nodes, 2 inhibitory neurons. Not cortical. |
| Plasticity | 4 | STDP + three-factor + homeostatic. Correct principles, coarse. |
| Neuromodulation | 4 | 7 systems with correct functional roles. Single scalars. |
| Cognitive systems | 2 | Scripted implementations of psychological theories. |
| Scaling | 5 | PI controller and divisive normalization are sound. |
| Sleep/dream | 3 | Sleep stages correctly sequenced. Dreams are text templates. |
| Social cognition | 1 | Entirely scripted if-then logic. |
| **Overall** | **3.0** | Biologically inspired simulation with scripted cognition. |

---

## 10. Major Biological Gaps

### Missing Neural Mechanisms

| Mechanism | Biological Importance | Current Status |
|---|---|---|
| Cortical columns/layers | Fundamental unit of cortical computation | Absent. Neurons are flat. |
| Inhibitory interneuron subtypes | PV, SST, VIP serve different computational roles | Only 2 generic inhibitory neurons |
| Synaptic delays (realistic) | Axonal conduction takes 1-20ms | Fixed 2-tick delay for all |
| Dendritic computation | Nonlinear integration, local plasticity | No dendrites |
| Gap junctions | Fast synchronization, especially in interneurons | Absent |
| Glial cells | Metabolic support, synaptic modulation, pruning | Absent |
| Cortical oscillations | Gamma, theta, alpha rhythms for binding and communication | No oscillatory dynamics |
| Ion channel diversity | Na, K, Ca, HCN channels shape dynamics | No ion channels |
| Synaptic vesicle dynamics | Short-term facilitation and depression | Only failure probability |
| Conductance-based synapses | Reversal potentials determine E/I interaction | Absent. Current-based only. |

### Missing Cognitive Mechanisms

| Mechanism | Importance | Current Status |
|---|---|---|
| Recurrent attractor dynamics | Basis of working memory, pattern completion | No attractor networks |
| Neural pattern completion | How hippocampal recall actually works | Memory retrieval is list search |
| Spike sequence replay | Sleep consolidation mechanism | No replay. Dreams are random recombination. |
| Population coding | Neural basis of representation | Individual named neurons, not populations |
| Phase-amplitude coupling | Cross-frequency communication | No oscillations |
| Predictive coding hierarchy | Cortical information processing | Single-level rolling average |
| Developmental plasticity | Brain development, critical periods | CriticalPeriodSystem exists but is scripted |
| Reward circuit dynamics | Basal ganglia Go/NoGo pathways | Partially present (Motor competition), mostly scripted |

---

## 11. What Ikigai Already Does Well

### Neuromodulator Interaction

The seven neuromodulator systems interact in biologically plausible ways:
- Cortisol-oxytocin buffering (social safety reduces stress)
- Dopamine RPE with tonic/phasic separation
- Adenosine sleep pressure coupling to cognition
- Serotonin stabilization of activity levels
- Norepinephrine surprise detection

These interactions create emergent dynamics where, for example, social presence reduces cortisol, which increases oxytocin, which improves trust and attachment. This kind of neuromodulatory crosstalk is real and the functional approximation is reasonable.

### EI Balance and Homeostasis

The PI controller, divisive normalization, intrinsic plasticity, and synaptic scaling create a multi-layered homeostatic system that maintains stable dynamics across network sizes. This mirrors real cortical homeostasis, which employs multiple timescale mechanisms (Turrigiano & Nelson 2004).

### Three-Factor Learning Rule

The combination of STDP timing + dopamine gating + eligibility traces is one of the better-implemented mechanisms. This follows the theoretical framework of Izhikevich (2007) and recent experimental validation of eligibility traces in cortex (Gerstner et al. 2018).

### Sleep Architecture

The sleep state machine correctly sequences SWS -> SWR -> REM with appropriate neuromodulatory changes. Weight consolidation during sleep, cortisol circadian variation, and adenosine clearance are all biologically appropriate design choices.

### Scaling Laws

The Day 11 scaling laws demonstrate thoughtful engineering. The rate-based normalization and PI controller produce genuine population invariance, which is a real property of balanced cortical networks (Renart et al. 2010). The spike correlation metric detects pathological synchrony.

### Persistence and Development

Cross-session state persistence with backup saves allows the system to develop over multiple sessions. This creates a trajectory of plasticity changes, memory accumulation, and trait evolution that loosely parallels biological development.

---

## 12. Final Verdict

### What Ikigai Is

Ikigai is closest to a **cognitive experiment with neural substrate** -- a hybrid system where:

1. A small spiking neural network provides dynamical substrate (firing patterns, plasticity, homeostasis)
2. Scripted cognitive modules read system state and generate psychological behavior (language, memory, emotion, social cognition)

It is **not** a neural simulation in the computational neuroscience sense (cf. NEURON, Brian2, NEST). Those tools simulate biophysically detailed neurons and let behavior emerge from network dynamics. Ikigai's neurons are functional placeholders, and its behavior is primarily scripted.

It is **not** a conventional AI system. It does not learn from data, optimize an objective function, or generalize to new tasks. It produces pre-scripted behavioral patterns modulated by neural state.

It is best described as a **digital organism prototype** -- an engineering framework that combines biologically inspired dynamics with programmatic cognition. The neural layer provides genuine dynamical stability (EI balance, homeostasis, plasticity). The cognitive layer provides behavioral richness (language, memory, social interaction) that would take orders of magnitude more neurons to produce emergently.

### Honest Assessment

| Question | Answer |
|---|---|
| Is the neuron model biologically accurate? | No. Functional LIF approximation. |
| Is the network architecture realistic? | No. Hand-wired named nodes, not cortical. |
| Do cognitive behaviors emerge from neural dynamics? | ~10-15% emergent, ~85-90% scripted. |
| Does the system learn? | Yes, through STDP and three-factor plasticity. Learning is real but slow. |
| Is the neuromodulator system reasonable? | Yes, qualitatively. Single scalars, not spatial. |
| Does the system scale biologically? | PI controller and normalization are sound. Architecture-specific. |
| Is "digital organism" an accurate description? | Partially. It has persistence, development, sleep, memory. But cognitive behavior is programmatic. |

### Path Forward

For Ikigai to advance from "cognitive experiment" toward "digital organism," the primary gap to close is the **cognitive scripting**. The key architectural change would be replacing scripted cognitive systems with emergent computation. This would require:

1. **Population coding**: Replace named neurons with neuron populations that represent information through firing rate patterns
2. **Attractor networks**: Working memory, pattern completion, and decision making from recurrent dynamics
3. **Spike replay**: Dream consolidation from actual replay of spike patterns, not text template recombination
4. **Hierarchical processing**: Multiple cortical layers with feedforward/feedback connections
5. **Scale**: 10,000-100,000 neurons minimum for non-trivial emergent cognition

Until then, Ikigai is an interesting proof-of-concept that demonstrates how biological principles can be assembled into a coherent framework, even if the cognition is not yet emerging from the neural dynamics themselves.

---

*This audit was generated from analysis of `ikigai.py` (4,362 lines, 361 code items, 100 neurons, ~175 synapses) on March 5, 2026.*
*Project NeuroSeed -- Hitoshi AI Labs*
