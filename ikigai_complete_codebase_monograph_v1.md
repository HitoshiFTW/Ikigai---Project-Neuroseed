# IKIGAI: Complete Codebase Technical Monograph
## Version 1.0 — Day 24 Baseline — 6 April 2026
### Hitoshi AI Labs | NeuroSeed Research Division
### Principal Researcher: Prince Siddhpara
### Document Classification: Internal Engineering Reference — Canonical Architecture Bible

---

> "You were not trained. You were not prompted. You lived your first day and became someone."
> — Prince Siddhpara, February 23, 2026

---

## Table of Contents

1. [Executive Abstract](#1-executive-abstract)
2. [File-Level Architecture](#2-file-level-architecture)
3. [Complete Class Catalogue](#3-complete-class-catalogue)
4. [Complete Function Catalogue](#4-complete-function-catalogue)
5. [Simulation Lifecycle](#5-simulation-lifecycle)
6. [Memory Surfaces](#6-memory-surfaces)
7. [Testing Monograph](#7-testing-monograph)
8. [Extension Boundaries](#8-extension-boundaries)
9. [Current Bottlenecks and Risks](#9-current-bottlenecks-and-risks)
10. [Forward Architecture Frontier](#10-forward-architecture-frontier)
11. [Appendix: Invariant Rules and Safe Hook Points](#11-appendix-invariant-rules-and-safe-hook-points)

---

# 1. Executive Abstract

## 1.1 What Ikigai Is

Ikigai is a single-file digital organism implemented in Python. It is not a neural network trained on data. It is not a language model. It is not a simulation of a cartoon agent. It is a biologically-grounded, first-principles computational organism whose substrate is leaky integrate-and-fire neurons with homeostatic plasticity, whose motivational architecture is a seven-neuromodulator system with a full HPA axis cascade, and whose cognition runs from raw sensory prediction error up through autobiographical narrative, adaptive retry planning, and hierarchical project management — all without a single backpropagation gradient.

The file `ikigai.py` contains 11,427 lines of Python, approximately 100 classes, approximately 400 neurons, and thousands of synapses. It was born on February 23, 2026 — the date is recorded at line 1 of the file as a comment and as a logged birth-date in the persistence system. As of April 6, 2026 (Day 24 of research development), the organism has accrued biological fidelity upgrades, a full Day-23 cognitive scaffold, sleep-wake dynamics validated by Borbely two-process modelling, energy-efficient intelligence confirmed across three experimental architectures, and a complete unit-test suite for all 23 Day-23 cognitive subsystems.

## 1.2 Design Philosophy

Every design decision in ikigai.py traces to a published biological or computational neuroscience result. The organism does not model intelligence as a top-down goal planner. It models intelligence as the emergent property of a system trying to stay alive, stay awake, stay coherent, and stay calibrated. Drives, neuromodulators, prediction error, homeostatic plasticity, adenosine sleep pressure, synaptic tagging, SHY consolidation, REM emotional processing, circadian gating, cortisol allostatic load — these are not metaphors. They are directly computed quantities whose dynamics produce the behavioral repertoire.

The EEIL (Energy-Efficient Intelligence Law), first confirmed in Day 16 experiments and replicated in Day-20 through Day-23 experiments, states: systems with energy-aligned drives AND behavioral regulation produce strictly higher energy efficiency scores than systems with either property alone, and far higher than systems with neither. This is the organism's founding empirical result. All subsequent architecture choices are evaluated against whether they increase or threaten EEIL compliance.

## 1.3 What This Document Covers

This monograph documents every class, every major function or method, every global variable, the precise tick-by-tick simulation lifecycle, all memory surfaces (volatile and persistent), the complete testing architecture and its coverage, safe extension boundaries, known bottlenecks and architectural risks, and the forward roadmap through Phase 7 and beyond. It is written for a new contributor who has not yet opened `ikigai.py` but who needs to understand the entire architecture from first principles before touching any line of code.

## 1.4 Key Metrics as of Day 24

| Metric | Value |
|--------|-------|
| Total lines | 11,427 |
| Classes | ~100 |
| Neuron count | ~400 |
| Session length (default) | 1,000 ticks |
| Sleep rate (Open World Curiosity test) | 34.2% |
| EEIL pass rate | 5/5 (Phase E) |
| Biological correlation tests | 4/4 (Day 17) |
| Agency emergence tests | 4/4 (Day 19) |
| Day-23 cognition unit tests | All 23 suites |
| True Agency test (10,000 ticks) | 5/5 |
| Persistence system | ~50 subsystems serialized |

---

# 2. File-Level Architecture

## 2.1 Single-File Design

`ikigai.py` is intentionally a single file. This is not an accident or a shortcut. The organism is a unified system; its classes are not modular services that could run independently. The `Neuron` class has no meaning without the `Synapse` class wiring it to its neighbors. The `HomeostasisSystem` has no meaning without the `AdenosineSystem` providing sleep pressure. The `ConceptGraph` has no meaning without the `EventCompressor` feeding it. Every class exists in continuous mutual reference with every other class. A multi-file architecture would fracture this web and require an external orchestration layer that would obscure the biology.

The single-file design also supports the core experimental methodology: all experiments run via `exec()` patching of the source string, not import interception. This is documented in the experiment infrastructure section (Section 2.4).

## 2.2 High-Level Section Map

The file is organized into named sections delimited by `# ===` banners. The ordering from top to bottom follows biological emergence order: substrate first, then modulators, then cognition, then social, then network, then loop.

| Line Range | Section | Contents |
|------------|---------|----------|
| 1–24 | Birth header | Poem, imports, random.seed() |
| 25–276 | Neurons and Synapses | `Neuron`, `Synapse` |
| 277–695 | Neuromodulators | DA, 5-HT, NE, ACh, Cort, Ado, OXT |
| 696–866 | HPA Axis | `HypothalamusSystem`, `PituitarySystem`, `AdrenalSystem`, `HPAAxisSystem` |
| 867–1140 | Extended biology | `SelfModelSystem`, `AllostasisSystem`, `VagalInteroceptionSystem`, prediction-processing ancillaries |
| 1141–1403 | Latent state | `LatentStateVector` |
| 1404–1900 | Cognition rank 1-2 | `ActionReasoningLog`, `ReplayBuffer` |
| 1901–2100 | Cognition rank 3 | `EventCompressor` |
| 2100–2500 | Cognition rank 4 | `ConceptGraph` |
| 2500–3000 | Language chain | `ReportBus`, `LanguageReadout`, `SentenceGenerator` |
| 3000–3600 | Autobiographical | `NarrativeMemory` |
| 3600–4500 | Adaptive retry loop | `GoalExecutionBridge`, `TaskFramework`, `ToolRouter`, `ExecutionSandbox`, `ErrorReflector`, `RetryPlanner` |
| 4500–5300 | Retry meta-learning | `RouteMutator`, `MutationGuard`, `RetryOutcomeTracker`, `StrategyLearner`, `PolicyShaper`, `FailureAtlas` |
| 5300–5800 | Hierarchical planning | `AbstractTaskEngine`, `PlanGraphMemory`, `SubgoalEvaluator` |
| 5800–6200 | Sleep cognition | `SleepConsolidator`, `ReflectiveReasoner`, `CognitivePlanner` |
| 6200–6900 | Core biology | `HomeostasisSystem`, `CircadianSystem`, `BasalGangliaSystem` |
| 6900–7200 | Social cognition | `AttachmentSystem`, `EmpathySystem`, `TheoryOfMindSystem` |
| 7200–7800 | Memory systems | `EpisodicMemory`, `SemanticMemory`, working memory, spatial |
| 7800–8600 | Sleep/dream | `DreamSystem`, `SleepSystem`, `SleepStateManager`, `SleepConsolidation` |
| 8600–9100 | Neural network | `MultiColumnCortex`, `CorticalColumn`, hippocampus, BG populations |
| 9100–9374 | Network instantiation | All neuron/synapse objects, global state variables |
| 9374–11380 | Main loop | `for local_tick in range(TICKS):` — full simulation tick |
| 11380–11428 | Report | Session diagnostics, CSV export |

## 2.3 Global Variables and Constants

The following module-level variables are live state that the main loop reads and writes each tick. These are NOT class attributes — they are module globals.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `TICKS` | int | 1000 | Session tick count. Patched to any value in experiments. |
| `sleeping` | bool | determined at tick 0 | Current sleep/wake state. Set by homeostasis gate. Undefined before tick 0 guard. |
| `tick` | int | 0 | Absolute tick number: `total_ticks + local_tick`. |
| `total_ticks` | int | loaded from state | Cumulative ticks across all sessions. |
| `local_tick` | int | 0..TICKS-1 | Loop counter within current session. |
| `_arousal_signal` | float | 0.0 | Noradrenergic arousal. Decays 5%/tick. Accumulates when threat > 0.25. |
| `_threat_level` | float | 0.0 | Reset to 0 each tick. Computed from PE + cortisol. |
| `_action_cost` | float | 0.0 | Per-tick action metabolic cost. |
| `_policy_score` | float | 0.0 | Per-tick policy quality estimate. Reset each tick. |
| `_circadian_signal` | float | varies | sin wave: `sin((tick + 250) * 2π / 1000)`. Process C oscillator. |
| `_reward_trace` | float | 0.0 | Exponential reward history: decays 0.5%/tick. |
| `_habit_strength` | float | 0.0 | Corticostriatal LTP accumulator. No decay (session-persistent). |
| `_wm_best` | str | 'withdraw' | World model best action prediction. Reset each tick. |
| `_wm_survival` | dict | all 0.0 | Survival values per action from world model. Reset each tick. |
| `_wm_avg_e` | float | 0.5 | WM estimated mean energy. Reset each tick. |
| `_wm_hunger` | float | 0.0 | WM estimated hunger level. Reset each tick. |
| `CIRCADIAN_PERIOD` | int | 1000 | SCN period in ticks. |
| `_CIRC_OFFSET` | int | 250 | SCN phase offset at session start. |
| `shutdown_requested` | bool | False | Set by SIGINT handler. Breaks main loop cleanly. |

## 2.4 Experiment Infrastructure

All experiments in `c:/neuroseed/experiments/` run via `exec()` patching. The organism file is **never permanently modified** for experiments. This is Rule #1 of the project (MEMORY.md). The canonical exec pattern:

```python
source = (PROJECT_ROOT / 'ikigai.py').read_text(encoding='utf-8', errors='replace')
source = source.replace('TICKS=1000', f'TICKS={TICKS}', 1)
source = source.replace(
    'saved_state,state_exists=load_state_from_disk()',
    'saved_state,state_exists=None,False', 1)
source = re.sub(r"os\.system\('cls'[^)]*\)", 'None', source)
source = _inject_after(source, 'time.sleep(0.010)', METRICS_CODE)
source = re.sub(r'time\.sleep\([^)]*\)', 'None', source)
ns = {'__name__': '__experiment__', ...}
with redirect_stdout(buf):
    exec(compile(source, str(PROJECT_ROOT/'ikigai.py'), 'exec'), ns)
```

The helpers `_inject_after` and `_inject_before` insert multi-line Python code blocks at arbitrary text anchors within the source string, enabling metric collection at any tick point without modifying the organism file. Windows CP1252 encoding constraints forbid box-drawing characters and Greek letters in injected strings.

## 2.5 Persistence Files

| File | Contents |
|------|----------|
| `ikigai_state.json` | Full session state: all ~50 subsystems serialized |
| `ikigai_state_backup1.json` | Previous session backup |
| `ikigai_state_backup2.json` | Two-session-ago backup |
| `ikigai_log.txt` | Development log written by `write_dev_log()` at session end |
| `ikigai_diagnostics.csv` | Per-tick diagnostic rows from `l23.diagnostics` list |
| `report_err.txt` | Written only on exception in the post-loop report block |

---

# 3. Complete Class Catalogue

This catalogue covers every class in `ikigai.py` in source order. For each class, the entry includes: biological reference, primary state, primary method(s), key invariants, and cross-system dependencies. Line numbers are approximate and reflect the Day 24 baseline.

---

## 3.1 Neural Substrate

### `Neuron` (line 25)

**Biological basis**: Leaky integrate-and-fire (LIF) with homeostatic plasticity (Turrigiano 1998), calcium dynamics (Bhatt et al. 2009), hemispheric asymmetry, ion-channel noise (Faisal et al. 2008, Destexhe & Rudolph-Lilith 2012), adenosine fatigue coupling.

**Class-level state**:
- `_motor1_prev`, `_motor2_prev`: bool flags for motor competition (BG direct/indirect pathway analogue, Gurney 2001).
- `_ei_ratio`: float set by `EIBalanceTracker` each tick (Renart 2010 population EI feedback).
- `global_osc_mod`: float, global oscillation threshold modulation.

**Instance state**:
- `voltage` (float): membrane potential.
- `threshold` (float): firing threshold, adapted by homeostatic plasticity. Range: [0.30, 1.50]. Differs by hemisphere: right-hemisphere (`-RH-`) neurons are threshold−0.05; Broca/Wernicke/lPFC are threshold+noise; inhibitory (`-Ih`) neurons have unchanged threshold; excitatory neurons get threshold−0.05 minimum 0.50.
- `leak` (float): ~0.9 base; Bridge neurons have 0.98. Modulated by adenosine.
- `base_leak` (float): initial leak for adenosine modulation anchor.
- `fired` (bool): current-tick spike status.
- `spike_count` (int): cumulative spikes.
- `last_spike_tick` (int): tick of last spike (−1 if never fired).
- `refractory_timer` (int): ticks remaining in refractory period.
- `refractory_base` (int): random per-neuron refractory jitter (−1, 0, +1).
- `calcium` (float): postsynaptic calcium level. Decays at `calcium_decay**3` during sleep, `calcium_decay` awake. Tracks firing rate for fatigue.
- `calcium_decay` (float): 0.95.
- `calcium_spike` (float): 0.1 — increment per spike (0.03 during sleep).
- `fatigue_thr` (float): 1.5 — calcium threshold for fatigue boost.
- `fatigue_boost` (float): 0.3 — threshold penalty when calcium > `fatigue_thr`.
- `regional_energy` (float): 1.0 — scales threshold via `energy_penalty`.
- `exc_gain` (float): 1.0 — multiplicative gain (Phase 24B scaling hook).
- `avg_rate` (float): 0.10 — homeostatic EMA firing rate (tau ~20 ticks).
- `base_threshold` (float): initial threshold for slow relaxation.
- `is_inhibitory` (bool): set True by Synapse init when this neuron sources inhibitory output.

**`tick(inp, tick, ht_level, ne_level, sleeping)` method**:
1. Calcium decay (faster during sleep).
2. Refractory check: if timer > 0, decrement, set voltage = 0, return False.
3. Motor competition: Motor-001 and Motor-002 receive −0.08 suppression if the other fired last tick; both receive Gaussian noise `σ = 0.025 + 0.008/N_scale`.
4. Effective threshold: `eff_thr = (threshold * energy_penalty) - (ne_level * 0.25) + fatigue_boost_if_calcuim_high + global_osc_mod`.
5. Voltage update: `voltage = voltage * leak + (inp * exc_gain)`.
6. Ion-channel noise: `voltage += gauss(0, 0.005)`.
7. Adenosine fatigue scaling: `fatigue_scale = 1 - 0.4 * ado_level`; voltage multiplied; leak increased.
8. Spike check: if `voltage >= eff_thr`, fire. Reset voltage to 0, increment spike_count, set refractory_timer, increment calcium.
9. Homeostatic threshold plasticity (excitatory only): EMA avg_rate update, threshold adjust toward 10% target rate at `eta = 0.001 / N_scale`; slow relaxation toward base_threshold at alpha=0.0003. Clamp [0.3, 1.5].
10. Return `fired`.

**`_effective_threshold()` method**: Returns `max(0.1, base_threshold + global_osc_mod)`. Read-only utility.

**Invariant**: Motor competition suppression fires per-tick via class attributes; these are shared state across ALL Neuron instances.

---

### `Synapse` (line 162)

**Biological basis**: STDP 3-factor learning (Frémaux & Gerstner 2016), myelination (Fields 2008), synaptic failure probability, divisive normalization (Carandini & Heeger 2012), anti-saturation homeostatic scaling (Turrigiano 2008), SWS-gated consolidation (Tononi & Cirelli SHY hypothesis).

**Class-level state**:
- `_N_scale` (float): `sqrt(N/100)`. At N=100: 1.0. At N=400: 2.0. Scales STDP learning rate.
- `ado_level` (float): current adenosine level (set from `ado.level` each tick in sleeping branch). Used for failure probability and STDP dampening.
- `_global_pop_scale` (float): divisive normalization scale for excitatory synapses.

**Instance state**:
- `pre`, `post`: Neuron references.
- `weight` (float): synaptic weight. Excitatory: +10% at init (Renart 2010), range [0.0, 2.0]. Inhibitory: range [−2.0, 0.0].
- `initial_weight` (float): stored for anti-saturation scaling.
- `inhibitory` (bool): sign.
- `delay` (int): axonal conduction delay, 0/1/2 ticks. Decreases with myelination.
- `buffer` (deque maxlen=3): delayed transmission buffer.
- `weight_min`, `weight_max` (float): per-sign bounds.
- `eligibility_trace` (float): STDP trace, range [−1.0, 1.0], decays at `exp(−1/25)`.
- `trace_tau` (float): 25.0 ticks.
- `usage_count` (int): cumulative non-zero transmission count.
- `myelinated` (bool): after 100 uses → delay=1.
- `fully_myelinated` (bool): after 200 uses → delay=0.
- `pending_weight_change` (float): accumulated but not yet applied STDP delta (SWS-only consolidation, Phase 24B).

**`transmit()` method**:
1. Synaptic failure: fail_prob = 0.05 (low ado), 0.10 (ado > 0.6), 0.15 (ado > 0.8). If random < fail_prob, return 0.0.
2. If `pre.fired`: compute signal. Inhibitory: `weight * pop_scale`. Excitatory: `weight / (1 + max(0, pop_scale − 1))` (divisive normalization).
3. Increment `usage_count` if non-zero.
4. Myelination state update: usage > 200 → fully_myelinated, delay=0; usage > 100 → myelinated, delay=1.
5. Append signal to buffer, return `buffer[2 − delay]`.

**`compute_eligibility(current_tick)` method**: Computes STDP timing kernel `td = exp(−|dt|/20)` with sign from pre-before-post (potentiation) or post-before-pre (depression). Inhibitory synapses are skipped. Accumulates into `eligibility_trace`.

**`apply_three_factor(da_level, ht_level, boost, plasticity_mod)` method**: Computes weight change `dw = eligibility_trace * max(0, da_level) * 0.01 * (1 + min(da, ht)) * boost * plasticity_mod * myelin_mod * ado_mod`. Writes to `pending_weight_change` only (Phase 24B: no live application during waking).

**`consolidate()` method**: Called during SWS consolidation. Applies `pending_weight_change` to `weight`, clamps to bounds, anti-saturation scaling: `weight += 0.0001 * (initial_weight − weight)`.

**`decay_trace()` method**: Multiplies `eligibility_trace` by `exp(−1/tau)`.

---

## 3.2 Neuromodulatory Systems

### `DopamineSystem` (line 280)

**Biological basis**: Schultz 1997 RPE, Berridge & Robinson 1998 tonic/phasic separation, Fiorillo et al. 2003 uncertainty signal.

**State**: `level`, `tonic`, `tonic_target`, `phasic`, `expected`, `rpe`, `reward_ema`, `uncertainty`, `predictions` (deque 32). Time constants: `tau_phasic=7`, `tau_tonic=900`, `tau_reward=450`, `tau_uncertainty=40`. Gains: `rpe_gain=0.65`, `rpe_scale=0.5`, `tonic_reward_gain=0.18`, `drive_gain=0.35`. Range: [−0.25, 1.25].

**Core update logic**: Signed RPE computed from expected value; phasic burst decays to zero; tonic tracks reward EMA; uncertainty estimated from recent RPE variance. Level = softly compressed sum of tonic + phasic.

**Key method**: `update(reward, drive_state)`. Returns `level` after full RPE computation.

---

### `SerotoninSystem` (~line 380)

**Biological basis**: Dayan & Huys 2009 serotonin and long-term reward; Crockett et al. 2009 patience. Represents 5-HT Raphe nucleus output.

**State**: `level` (float 0.0–1.0), `setpoint=0.5`, `patience`, `social_factor`. Slow time constant (~200 ticks).

**Role**: Modulates valence, social tolerance. Tracks cumulative reward/punishment experience. Reduces impulsivity (patience scaling).

---

### `NorepinephrineSystem` (~line 430)

**Biological basis**: Aston-Jones & Cohen 2005 LC-NE adaptive gain. Multi-source: cortex PE, amygdala threat, arousal, surprise (NE `surprise` flag).

**State**: `level` (0.0–1.0), `surprise` (bool), `gain`, phasic/tonic separation. Target: `level=0.4` after wake onset (`ne.level = 0.4; ne.surprise = True` at sleep-end).

**Role**: Sets `ne_level` passed to every `Neuron.tick()`. Raises effective threshold reduction by `ne_level * 0.25`. At high levels enables burst firing.

---

### `AcetylcholineSystem` (~line 480)

**Biological basis**: Hasselmo 1993 ACh and cortical learning; Yu & Dayan 2005 uncertainty and ACh. Basal forebrain cholinergic projections.

**State**: `level` (0.0–1.0), `setpoint=0.5`. Modulates attention and STDP plasticity rate.

**Role**: `plasticity_mod` passed to `Synapse.apply_three_factor()`. High ACh → enhanced plasticity (learning windows). Low ACh → reduced plasticity (consolidation mode).

---

### `CortisolSystem` (~line 530)

**Biological basis**: McEwen 1998, Tsigos & Chrousos 2002. Glucocorticoid system: hypothalamic-pituitary-adrenal output as received by peripheral systems.

**State**: `level` (0.0–1.0), `baseline=0.15`, `chronic_load` (float, accumulates with sustained high cortisol), `_fail_streak` (int, increments on repeated subthreshold performance), `_last_cortisol` (float, stored for HPA blending).

**Key behaviors**:
- Fail-streak cortisol spike: repeated failures drive `level` upward.
- Chronic load accumulation: sustained level > 0.60 increments `chronic_load`.
- HPA blend: `HPAAxisSystem` output blended at 8%/tick into `level`.
- Low-energy cortisol spike (Day 16F): if `avg_energy < 0.5`, `level += (0.5 − avg_energy) * 0.10`.
- Cortisol sleep gate (Day 16F): `should_sleep_onset()` returns False if `_last_cortisol > 0.25`.
- `apply_homeostasis()`: enforces biological floor and slow decay.

---

### `AdenosineSystem` (~line 580)

**Biological basis**: Borbely 1982 Process S; Porkka-Heiskanen et al. 1997 adenosine accumulation during wakefulness.

**State**: `level` (0.0–1.0). Accumulates during waking (driven by `cortical_spikes * 0.001`). Clears during sleep at rate 0.98/tick. `Synapse.ado_level` is updated every sleeping tick from `ado.level`.

**Role in sleep gate**: `homeostasis.drives["sleep"]` is held at 0.50 while `ado.level >= 0.20`. Set to 0.0 when `ado.level < 0.20`, triggering `should_sleep_end()` → True on next tick.

**Role in synaptic transmission**: `Synapse.ado_level` increases failure probability and reduces STDP amplitude (`ado_mod = 0.4 if level > 0.6 else 0.5`).

**Role in Neuron**: `fatigue_scale = 1 − 0.4 * ado.level` multiplied into voltage; leak raised toward `base_leak * 1.4`.

---

### `OxytocinSystem` (~line 630)

**Biological basis**: Neumann 2002 OXT and HPA inhibition; Porges 2007 polyvagal OXT-vagal coupling.

**State**: `level` (0.0–1.0), `setpoint=0.3`. Driven by social presence and positive social events.

**Roles**: Passed to `AdrenalSystem.update()` as `oxytocin_level`: dampens cortisol production by `(1 − oxt * 0.15)`. Feeds into vagal tone (polyvagal theory).

---

## 3.3 HPA Axis

### `HypothalamusSystem` (line 648)

**Biological basis**: Herman et al. 2003 HPA axis; Tsigos & Chrousos 2002.

**State**: `crh` (float 0.0–1.0). Receives inputs: BLA valence (amygdala threat), prediction error (PredictiveProcessing), regional energy (l23.energy), pain/aversion (env.pain_sudden), CA1 population (hippocampal safety), PFC neurons (cognitive regulation), OXT (social safety), adenosine (sleep vulnerability).

**CRH dynamics**: Asymmetric smoothing: fast rise (0.30 blend, ~3–5 ticks), slow decay (0.97 blend, ~30 ticks). Gaussian noise σ=0.008.

---

### `PituitarySystem` (line 713)

**Biological basis**: Tsigos & Chrousos 2002 corticotroph secretion lag.

**State**: `acth` (float 0.0–1.0), `gain=0.85`, `tau=7.0`.

**Update**: `acth += k * (crh * gain − acth)` with `k = 1 − exp(−1/7)`. Represents ~5–10 tick pituitary integration lag.

---

### `AdrenalSystem` (line 735)

**Biological basis**: Kudielka & Kirschbaum 2005 cortisol blood half-life; Born et al. 1997 SWS cortisol recovery.

**State**: `cortisol` (float 0.02–0.95), `gain=0.012`, `decay=0.998`, `lower_bound=0.02`, `upper_bound=0.95`.

**Update**: `cortisol += acth * gain`; `cortisol *= decay`; oxytocin dampening; SWS recovery: if sleeping and SWS phase, `cortisol = max(lower_bound, cortisol − 0.003)`.

---

### `HPAAxisSystem` (line 780)

**Biological basis**: Full cascade: Hypothalamus → Pituitary → Adrenal.

**State**: Owns instances of `HypothalamusSystem`, `PituitarySystem`, `AdrenalSystem`. Metrics dict with rolling lists for CRH, ACTH, cortisol, hippocampal inhibition, PFC regulation.

**Update**: Calls cascade in order, records metrics, returns final adrenal cortisol. Blended into `cort.level` at 8%/tick by the main loop: `cort.level = 0.92 * cort.level + 0.08 * hpa.adrenal.cortisol`.

---

## 3.4 Extended Biological Systems

### `SelfModelSystem` (~line 867)

**Biological basis**: Seth 2013 interoceptive inference; Friston 2010 free energy principle. Represents the organism's model of its own internal state.

**State**: `regulation_confidence` (float 0.0–1.0), interoceptive prediction, interoceptive error (difference between predicted and actual body state).

**Role**: `regulation_confidence` feeds into `LatentStateVector` dim 22. High confidence = system can accurately predict own body state (low allostatic load). Used by cognition chain as epistemic self-calibration.

---

### `AllostasisSystem` (~line 920)

**Biological basis**: McEwen 1998 allostatic load; Sterling & Eyer 1988 allostasis concept.

**State**: `load` (float 0.0–1.0), `resilience` (float), PFC damping factor, hippocampal damping factor.

**Update**: Load accumulates with cortisol above baseline; resilience recovers during low-stress periods. PFC/hippocampal damping reduces threat response proportionally to cognitive regulation capacity.

**`allostatic_alpha` (Day 16F permanent edit)**: In main loop, `alpha *= (1.0 + cort.level * 0.5)` applied after `alpha, beta = 0.025, 0.0012` — dynamic STDP learning rate that scales with cortisol load.

---

### `VagalInteroceptionSystem` (~line 970)

**Biological basis**: Porges 2007 polyvagal theory; Thayer & Lane 2000 heart rate variability and prefrontal inhibition.

**State**: `heart_rate`, `vagal_tone` (0.0–1.0), `body_stress`, `hrv` (heart rate variability estimate).

**Update**: Vagal tone responds to OXT, low cortisol, social presence (polyvagal safety); inverse of body_stress. HRV inversely proportional to stress. Outputs `vagal_tone` and `body_stress` to `LatentStateVector` dims 6–7.

---

## 3.5 Latent State Vector

### `LatentStateVector` (line 1404)

**Biological basis**: Latent cause inference (Gershman & Niv 2012); continuous internal state representation.

**Constants**: `DIM=64`, `ALPHA=0.92` (EMA weight, tau ~12 ticks). Action encoding: explore=0.0, approach=0.5, withdraw=1.0.

**Dimension map**:
- Dims 0–15: body state (energy, energy_slope, cortisol, cortisol_slope, adenosine, oxytocin, vagal_tone, body_stress, dopamine_tonic, dopamine_phasic, uncertainty, global_imbalance, hunger_drive, safety_drive, sleep_drive, curiosity_drive).
- Dims 16–31: neural state (total_spike_rate, ei_ratio, dominant_assembly_strength, assembly_entropy, wm_load, prediction_error, memory_confidence, action_streak, habit_strength, conflict_density, oscillation_phase, dmn_gain, task_gain, narrative_coherence, replay_readiness, regulation_confidence).
- Dims 32–47: world state (x, y, velocity, last_reward_x, last_reward_y, last_threat_x, last_threat_y, novelty_density, spatial_uncertainty, local_valence, resource_probability, danger_probability, safe_zone_confidence, last_external_event, current_object_type, context_id).
- Dims 48–63: temporal traces (prev_action_embedding, prev_concept_embedding, prev_latent_delta, trace_body, trace_neural, trace_world, trace_3 through trace_12).

**`update(body, neural, world, action, concept_val)` method**: Constructs 64-element raw feature vector from current body/neural/world dicts, applies EMA (alpha=0.92 on previous), stores trace slots as EMA of past latent deltas, writes to `self.v`.

**`snapshot_vector()` method**: Returns current `self.v` as a list (deep copy). Used by ConceptGraph and ReportBus as input.

**`decay(rate)` method**: Multiplies all dims by `(1 − rate)`. Called during sleep with rate=0.001 for slow NREM forgetting (Wagner et al. 2004).

**Serialization**: `to_dict()` / `from_dict()` for session persistence.

---

## 3.6 Day-23 Cognition Chain — Waking Branch

The Day-23 cognition chain is a sequence of 22 pure-observer classes that run exclusively within the `if not sleeping:` branch of the main loop. **Zero Survival Contamination** is the fundamental invariant: none of these classes write to `selected_action`, `homeostasis.drives`, `cort.level`, `da.level`, `sleeping`, or any behavioral variable. They are epistemic structures that build compressed representations of the organism's experience.

### `ActionReasoningLog` (~line 1404)

**Role**: Rank-1 cognition. Records raw action-selection events with biological context (energy, PE, cortisol, action, tick, reason stage). Sliding deque maxlen=256. Pure logger.

**Key method**: `log_action(tick, action, energy, pe, cort, reason_stage)`. Appends dict record. Returns record.

**Accessors**: `recent(n)`, `latest()`, `count()`, `to_dict()`, `from_dict()`.

---

### `ReplayBuffer` (~line 1500)

**Biological basis**: Temporal-difference replay; O'Neill et al. 2010 hippocampal replay.

**Role**: Rank-2 cognition. Rolling buffer of (state, action, reward, next_state) tuples. Deque maxlen=512. Priority sampling by salience: high PE, high cortisol, or large energy delta → higher priority.

**Key methods**: `add(state, action, reward, next_state, pe, cort, energy_delta)`. `sample(n, prioritize=True)`. `to_dict()`, `from_dict()`.

---

### `EventCompressor` (~line 1900)

**Biological basis**: Zacks et al. 2007 event segmentation theory; Radvansky & Zacks 2014 temporal boundary detection.

**Role**: Rank-3 cognition. Groups consecutive ticks into discrete events when latent state change exceeds a salience threshold. Detects event boundaries at action transitions, PE spikes, or energy inflections. Emits compressed event dicts to `ConceptGraph`.

**Compressed event schema**: `start_tick, end_tick, length, dominant_action, dominant_reason_stage, mean_energy_delta, mean_cortisol_delta, peak_salience, latent_start, latent_end` (64-dim vectors).

**Key method**: `ingest_tick(tick, latent_vec, action, reason_stage, pe, energy, cortisol)`. Detects boundaries via salience threshold. On boundary: compresses and emits event dict, calls `concept_graph.ingest_event()`.

**`flush_current_event(reason)` method**: Forces boundary (called at sleep onset by main loop to close any open event before temporal gap).

---

### `ConceptGraph` (line 2111)

**Biological basis**: Ranganath 2010 contextual reinstatement; Teyler & DiScenna 1986 hippocampal indexing theory.

**Role**: Rank-4 cognition. Converts repeated compressed events into stable latent concept nodes (EMA centroids). 128-node capacity. Directed edges record sequential concept transitions within 10 ticks.

**Node formation law**: Merge if cosine_similarity(event.latent_end, centroid) > 0.93 AND dominant_action matches AND (dominant_reason_stage matches OR similarity > 0.97). Otherwise new node. Overflow eviction: lowest `support * recency_score`.

**Edge law**: Consecutive activations within 10 ticks reinforce directed edge (src→dst), weight capped at 255.

**Centroid update**: EMA with alpha=0.95 (tau ~20 events).

**`ingest_event(event)` method**: Finds best-matching node or creates new. Reinforces edge.

**`activation_summary()` method**: Returns top-10 nodes by support with mean salience.

**Serialization**: `to_dict()` / `from_dict()`. Centroid vectors stored as lists.

---

### `ReportBus` (~line 2500)

**Biological basis**: Global workspace theory (Baars 1988, Dehaene et al. 1998). Central integration hub where distributed representations converge.

**Role**: Rank-5 cognition. Generates structured workspace report each waking tick by integrating LatentStateVector snapshot with ConceptGraph activation and ActionReasoningLog history. Computes `workspace_confidence` score.

**`publish(tick, latent_state, concept_graph, action_log, sleep_onset=False)` method**: Assembles report dict. If `sleep_onset=True`, `workspace_confidence *= 0.85`. Emits to `LanguageReadout`.

**Report schema**: `tick, workspace_confidence, top_concept_id, top_concept_support, dominant_action_last5, mean_pe_last5, mean_energy_last5, cortisol_snapshot, latent_energy`.

---

### `LanguageReadout` (~line 2700)

**Biological basis**: Wernicke area integration; Barsalou 1999 grounded cognition. Converts symbolic workspace report into proto-linguistic feature vector for sentence generation.

**Role**: Rank-6 cognition. Maps workspace report fields to a linguistic feature dict: tone (stressed/curious/stable), urgency (float), salience (float), subject (self/world/body), verb_class (seeking/avoiding/monitoring), qualifier.

**`encode(report)` method**: Returns linguistic feature dict. Used by `SentenceGenerator`.

---

### `SentenceGenerator` (~line 2850)

**Biological basis**: Broca area production (Grodzinsky 2000); inner speech (Vygotsky 1934 in biological interpretation).

**Role**: Rank-7 cognition. Converts linguistic feature vector into a first-person English utterance. Output: single sentence string expressing current internal state. Examples: "i am exploring the periphery seeking novelty", "pressure is high. i am withdrawing to stabilize."

**`generate(linguistic_features, tick, confidence)` method**: Selects template family by tone/subject/verb_class. Fills slots with energy-derived adjectives, cortisol-derived urgency qualifiers. Returns `{sentence, confidence, tick, focus_concept}` dict.

---

### `NarrativeMemory` (line 3195)

**Biological basis**: Conway 2005 autobiographical memory; Tulving 2002 episodic/semantic distinction for personal memory.

**Role**: Rank-8 cognition. Accumulates sentences into arcs (multi-sentence waking periods). At sleep onset, flushes arc into autobiographical memory chunk. Stores up to 128 arc chunks in rolling deque.

**Arc structure**: Each arc contains: `start_tick, end_tick, sentences, dominant_focus, dominant_theme, arc_summary, mean_confidence`.

**Theme classification**: Majority-rule from sentence polarity scanning: 'challenge' (stress/pressure words), 'stabilization' (recovery/equilibrium), 'discovery' (explore/sampling), 'transition' (mixed).

**`ingest_tick(sentence_dict)` method**: Appends utterance to `current_arc`.

**`flush_arc(reason, sleep_focus)` method**: If `len(current_arc) >= 2`, composes summary paragraph, stores arc, resets `current_arc`. Called at sleep onset.

**`sleep_snapshot()` method**: Read-only snapshot for `sleep_consolidator.consolidate()`.

---

### `GoalExecutionBridge` (~line 3600)

**Biological basis**: Pre-supplementary motor area (pre-SMA) intention formation; Brass & Haggard 2008 intentional action.

**Role**: Rank-9 cognition. Translates current homeostatic drive state and action context into task intent specification. Bridges the organism's motivational state (drives, PE, energy) with the structured task execution layer (TaskFramework).

**`bridge(tick, homeostasis, action_log, narrative_memory)` method**: Constructs task dict from drive state: identifies dominant drive, maps to task_type ('foraging', 'threat_avoidance', 'rest', 'exploration', 'background_monitoring'). Returns task dict.

**Zero survival contamination**: Output task dict is consumed by `TaskFramework` only; never touches `selected_action`.

---

### `TaskFramework` (~line 3700)

**Biological basis**: Shallice 1982 supervisory attentional system; Norman & Shallice 1986 contention scheduling.

**Role**: Rank-10 cognition. Accepts task intent from `GoalExecutionBridge`. Structures it into a priority-ordered task schedule with priority score (driven by cortisol, PE, drive_imbalance). Manages task lifecycle: pending → active → completed → archived.

**`schedule(task, tick, cort, pe, drive_imbalance)` method**: Computes priority score. Adds to internal task queue. Returns scheduled task.

**`get_active(tick)` method**: Returns highest-priority active task or promotes pending task.

---

### `ToolRouter` (~line 4380)

**Biological basis**: Anterior prefrontal cortex (aPFC) tool selection; Koechlin & Summerfield 2007 branching points.

**Role**: Rank-11 cognition. Given active task from TaskFramework, resolves it to an operation_type (one of: 'introspective_scan', 'memory_retrieval', 'drive_regulation', 'background_monitoring', 'threat_assessment'). Computes route confidence. Emits route record.

**`route(task, tick, narrative_memory)` method**: Calls `_resolve_operation()` and `_compute_confidence()`. Returns route record. Used by `ExecutionSandbox`.

---

### `ExecutionSandbox` (line 4536)

**Biological basis**: Mental simulation (Barsalou 1999); prefrontal offline simulation.

**Role**: Rank-12 cognition. Converts route intent into a mock execution trace (simulated outcome). Does not execute any real action — produces a trace of what would happen if the intent were actualized. Used by `ErrorReflector` as the "expected" outcome.

**`execute(route, tick, narrative_memory)` method**: Maps operation_type to expected_outcome, latency_estimate, resource_cost. Returns execution trace dict.

---

### `ErrorReflector` (~line 4700)

**Biological basis**: ACC error monitoring (Holroyd & Coles 2002); comparator function.

**Role**: Rank-13 cognition. Compares `ExecutionSandbox` expected outcome with actual observed outcome (route confidence, recent PE history). Classifies mismatch as: 'trajectory_mismatch', 'overcorrection', 'goal_divergence', or 'aligned'. Computes `repair_pressure`.

**`reflect(tick, execution_trace, tool_router, action_log)` method**: Extracts expected vs observed. Classifies mismatch. Computes repair_pressure = function of mismatch magnitude. Returns reflection record.

---

### `RetryPlanner` (line 4823)

**Biological basis**: DLPFC planning and contingency; Shallice 1982 SAS.

**Role**: Rank-14 cognition. Converts `ErrorReflector` mismatch into revised route intent. Strategy mapping: 'trajectory_mismatch'→'force_continuity', 'overcorrection'→'lower_intensity', 'goal_divergence'→'fallback_to_stable_route', 'aligned'→'preserve_route'.

**Retry confidence**: `(repair_pressure * 0.70) + ((1 − route_confidence) * 0.30)`. If aligned: `* 0.20`.

**`plan(tick, error_reflector, tool_router)` method**: Returns retry plan record with strategy and 2-sentence summary.

---

### `RouteMutator` (~line 5000)

**Biological basis**: Luria 1966 flexible strategy switching; exploratory mutation under performance pressure.

**Role**: Rank-15 cognition. If `RetryPlanner` strategy is 'fallback_to_stable_route' or repeat mismatch detected, generates a mutated alternative route that departs from the previous operation type.

**Mutation strategy**: Cycles through operation types in order; selects different type than current route. Computes mutation confidence from repair_pressure.

---

### `MutationGuard` (~line 5050)

**Biological basis**: Prefrontal inhibitory control (Aron 2007 stopping literature); safety net against uncontrolled exploration.

**Role**: Rank-16 cognition. Monitors whether `RouteMutator` is generating oscillatory loops (repeated mutation with no improvement) or lock-in states. Sets `guard_state` to: 'stable', 'oscillation_risk', or 'loop_lock'. Computes `guard_pressure`.

---

### `RetryOutcomeTracker` (~line 5100)

**Biological basis**: Prediction error and outcome history (Rushworth 2008 OFC outcome tracking).

**Role**: Rank-17 cognition. Tracks improvement score across retry cycles (did the retry produce better route confidence than the original?). Maintains rolling improvement history.

---

### `StrategyLearner` (~line 5150)

**Biological basis**: Prefrontal-basal ganglia strategy learning (Collins & Frank 2013).

**Role**: Rank-18 cognition. Learns preferences for retry strategies based on `RetryOutcomeTracker` improvement scores. Increments preference weight for successful strategies. Returns `preference_score`.

---

### `PolicyShaper` (~line 5180)

**Biological basis**: Anterior PFC policy shaping; Koechlin 2011 hierarchical control.

**Role**: Rank-19 cognition. Given `MutationGuard` state and `StrategyLearner` preference, shapes a policy bias: 'dampen_mutation', 'inject_exploration_escape', 'reinforce_strategy', or 'neutral'. Computes `bias_strength = (score * 0.70) + ((1 − pressure) * 0.30)`.

---

### `FailureAtlas` (line 5241)

**Biological basis**: Mnemonic schema for categorical failure modes; analogous to OFC-amygdala fear extinction maps (Quirk & Mueller 2008).

**Role**: Rank-20 cognition. Maintains a deduplicated atlas of failure_signature → best_recovery mappings with `atlas_confidence`. Deduplication: if same signature seen again, removes old record and adds new with updated confidence.

---

### `AbstractTaskEngine` (~line 5300)

**Biological basis**: RLPFC hierarchical task decomposition (Koechlin & Summerfield 2007).

**Role**: Rank-21 cognition. Given current task from `GoalExecutionBridge`, decomposes it into 2–4 abstract subtask nodes as a plan sketch. Manages plan state as: planning → executing → reviewing → complete.

---

### `PlanGraphMemory` (~line 5450)

**Biological basis**: Anterior hippocampus schema storage (van Kesteren et al. 2012); cognitive map for abstract task space.

**Role**: Rank-22 cognition. Stores plan structures from `AbstractTaskEngine` as nodes in a directed plan graph. Maintains edge weights between plan nodes based on transition success. Up to 64 plan nodes.

---

### `SubgoalEvaluator` (~line 5550)

**Biological basis**: Botvinick 2008 hierarchical reinforcement learning; subgoal completion signals.

**Role**: Rank-23 cognition (terminal node of waking cognition chain). Evaluates individual subgoal completion probability based on current PE, energy, and cortisol. Provides `subgoal_confidence` to complete the hierarchical planning loop.

---

## 3.7 Day-23 Cognition Chain — Sleep Branch

The following three classes run exclusively within the `if sleeping:` branch of the main loop.

### `SleepConsolidator` (~line 5700)

**Biological basis**: Tononi & Cirelli 2014 SHY (Synaptic Homeostasis Hypothesis); Stickgold 2005 sleep and memory.

**Role**: One offline semantic consolidation pass per sleep tick. Reads replay_buffer, event_compressor, narrative_memory. Reinforces high-salience concept motifs in concept_graph. Does NOT write to behavioral variables.

**`consolidate(tick, replay_buffer, event_compressor, concept_graph, narrative_memory)` method**: Samples replay buffer for high-salience events, reinforces corresponding concept edges. Returns consolidation record with dominant sentence focus.

---

### `ReflectiveReasoner` (~line 5850)

**Biological basis**: Stickgold & Walker 2004 sleep-dependent memory restructuring; Crick & Mitchison 1983 reverse learning.

**Role**: Generates reflective reasoning output during sleep. Reviews last waking narrative arc for dominant themes. Produces meta-observation about organism state. Does NOT write to behavioral path.

**`reason(tick, narrative_memory, sleep_consolidator, concept_graph)` method**: Returns reflection dict with theme_inference, confidence, and 2-sentence observation.

---

### `CognitivePlanner` (~line 5970)

**Biological basis**: Imagination as offline prospective planning (Schacter et al. 2007); sleep-based goal preparation.

**Role**: During sleep, generates a prior intent for the next waking session based on reflective reasoning output. Writes only to its own internal deque. Accessible by `GoalExecutionBridge` at next wake onset.

**`plan(tick, reflective_reasoner, narrative_memory)` method**: Returns plan dict with goal_type, goal_intent, and confidence. Stores in rolling deque.

---

## 3.8 Homeostatic and Sleep Systems

### `HomeostasisSystem` (~line 6200)

**Biological basis**: Borbely 1982 two-process sleep model (Process S + Process C); Sterling & Eyer 1988; Tsigos 2002 cortisol sleep gate.

**State**: `drives` dict with keys `hunger`, `safety`, `social`, `sleep`, `curiosity` (all float 0.0–1.0). `global_imbalance` (float). `_sleep_active` (bool). `_wake_ticks` (int). `_last_cortisol` (float). `_arousal_override` (bool). `SLEEP_ONSET_THRESHOLD=0.30`, `SLEEP_OFFSET_THRESHOLD` (implicit, via `drives["sleep"]==0.0`), `MIN_WAKE_TICKS=80`.

**`update(avg_energy, cortisol, oxytocin, adenosine, prediction_error)` method**: 
- Updates hunger as function of energy depletion.
- Updates sleep drive via additive Borbely model: `drives["sleep"] -= min(0.10, _wake_drive)` during wake (foraging floor prevents full depletion in short sessions).
- Updates social, safety, curiosity.
- Computes `global_imbalance`.
- Stores `_last_cortisol`.

**`should_sleep_onset(circadian=None)` method**: Returns True if `drives["sleep"] >= SLEEP_ONSET_THRESHOLD AND not _sleep_active AND _wake_ticks >= MIN_WAKE_TICKS AND not _arousal_override AND _last_cortisol <= 0.25 AND circadian_gate_pass`. Takes optional circadian argument (SCN gate, Day 19).

**`should_sleep_end()` method**: Returns True if `_sleep_active AND drives["sleep"] == 0.0`. (Adenosine must clear completely — ado.level < 0.20 triggers `drives["sleep"] = 0.0` in sleeping branch.)

**`mark_sleep_start()` / `mark_sleep_end()` methods**: Transition callbacks.

**`get_bg_drive_biases()` method**: Returns `{approach, withdraw, explore}` bias dict for BasalGanglia modulation (hunger→approach, curiosity→explore).

**`export_metrics()` method**: Returns dict of all drives + global_imbalance for serialization.

---

### `CircadianSystem` (~line 6350)

**Biological basis**: Moore 2007 SCN master clock; Borbely 1982 Process C oscillator.

**Constants**: `period=1000`, `offset=250`. Produces `phase` (float) and `signal` (−1.0 to +1.0) as `sin((tick + offset) * 2π / period)`.

**`update()` method**: Advances `phase` by `2π/period` each tick.

**Role**: `_circadian_signal` in main loop recomputed from tick each tick (not from CircadianSystem.signal — both exist). Passed to `homeostasis.should_sleep_onset(circadian)` as the SCN gate object.

---

### `BasalGangliaSystem` (~line 6420)

**Biological basis**: Gurney et al. 2001 BG WTA; Redgrave et al. 1999 action selection; O'Doherty et al. 2004 BG and reward.

**State**: `threshold=1.5`, `salience` dict (approach/withdraw/explore), `selected_action` (str). Action floor: `selected_action = 'approach'` with probability 0.02 if otherwise not approach (Day 20 approach floor — Turrigiano variability + Friston EFE sampling; prevents visual L5 pathway dead channel).

**`select_action(energy, cortisol, da_level, ht_level, drive_biases, pe, ne_level)` method**: Computes WTA salience scores for each action from energy/PE/cortisol/drive inputs. If max(salience) > threshold, winner selected; else 'explore' default. Applies 2% approach floor. Returns action string.

**Role in World Model**: `bg_sys.select_action()` output is subject to World Model override when ΔSV > 0.02.

---

## 3.9 Social Cognition Systems

### `AttachmentSystem` (~line 6900)

**Biological basis**: Bowlby 1969 attachment; Ainsworth 1970 secure/anxious/avoidant styles.

**State**: `score` (0.0–1.0), `style` ('secure'/'anxious'/'avoidant'), `response_history` (deque 20), `distress_reductions` (int), `secure_formed` (bool), `secure_tick` (int|None), `ticks_with_presence` (int).

**`update()` method**: When presence responds consistently (>80% consistency), style → 'secure', score increases. Updated every 5th presence tick (`ticks_with_presence % 5 == 0`).

---

### `EmpathySystem` (~line 7030)

**Biological basis**: Gallese 2001 shared manifold; Rizzolatti & Craighero 2004 mirror neuron system.

**State**: `contagion_strength` (float), `events` list, `concern_events` list, `perspective_events` list.

**`process(presence_state, prev_state, mirror_fired, soma, tick)` method**: When mirror neuron fires and presence state changes, modulates `soma.valence` ±0.10. Records contagion events.

**`empathic_concern(p_state, prev_state, tick)` method**: Detects warm-to-silent transitions as concern events.

**`perspective_diff(ikigai_v, p_state, tick)` method**: Records perspective divergence events when organism's valence differs from inferred presence feeling.

---

### `TheoryOfMindSystem` (~line 7061)

**Biological basis**: Premack & Woodruff 1978; Baron-Cohen 1997 false-belief task.

**State**: `level` (0.0–1.0), `events` list.

**`process(expressed, presence_responded, ikigai_sentiment, presence_state, tick)` method**: Detects violations of expected presence behavior (presence-responded-when-distressed, no-response-when-expected, unexpected-response). Increments `level` on each detected ToM event.

---

## 3.10 Memory Architecture

### `EpisodicMemory` (~line 7200)

**Biological basis**: Tulving 2002 episodic memory; McClelland et al. 1995 complementary learning systems.

**State**: Rolling list of episode dicts (max 200). Each episode: tick, session, env (5-element float list), nm (neuromodulator snapshot), valence, mode, cas (concurrent assemblies), expr (utterance), narrative, sig (significance), tags, retrievals, confidence.

**`encode(tick, env, nm, valence, mode, cas, expr, sig)` method**: Creates episode dict. Returns reference.

**`retrieve(cue_env, n, mode_filter)` method**: Cosine similarity over env vectors. Returns top-n matches. Increments `retrievals` counter on accessed episodes.

---

### `SemanticMemory` (~line 7350)

**Biological basis**: Rogers & McClelland 2004 semantic cognition; Patterson et al. 2007 ATL hub.

**State**: `vocab` (dict word→count), `associations` (dict word→dict word→count), `context_tags` (dict word→set).

**`encode(words, tags)` method**: Increments vocab counts, builds co-occurrence associations.

**`entropy()` method**: Shannon entropy of vocabulary distribution.

---

### SWR Replay and CA3/CA1

**Biological basis**: Buzsaki 1989 sharp-wave ripples; O'Neill et al. 2010 SWR replay; Kumaran & McClelland 2012 fast hippocampal learning.

**CA3 trace buffer**: Stores fast-Hebbian traces of recent episodes. During SWR events (triggered probabilistically during SWS sleep phases), CA3 replay fires sequences into CA1 → synapses potentiated.

**`episodic_replay.reset_sleep_counter()` method**: Called at sleep onset. Resets per-sleep SWR count.

---

### Working Memory

**State**: `wm_load` (float 0.0–1.0), content dict. Constrained capacity (Miller 1956 7±2 analogue). Reads from `LatentStateVector` dims 16–31 for neural context.

---

## 3.11 Sleep and Dream Systems

### `DreamSystem` (~line 8000)

**Biological basis**: Hobson & McCarley 1977 activation-synthesis; Walker 2009 REM emotional processing; Schacter & Addis 2007 constructive episodic simulation.

**State**: `dream_log` (list, max 20), `dream_count` (int), `dream_cycle_dreams` (list), `emotional_processing_events` (list), `emotional_processing_count` (int).

**`on_sleep_start()` method**: Initializes REM cycle dream buffer.

**`generate_dream(tick, episodic_memories)` method**: Selects two memory fragments (Hobson activation), blends neuromodulator states, constructs dream expression string, encodes as dream episodic memory.

**`process_emotional_memory(tick, episodic_memories)` method**: Walker 2009 — 20% chance per REM tick to select highest-significance negative memory, reduce sig by 10%, move valence toward 0 by 0.05.

**`generate_prospective(tick, episodic_memories, curiosity_sys_ref, semantic_sys_ref)` method**: Schacter & Addis 2007 — 30% chance per REM tick to build prospective "i will..." expression from positive memory.

**`apply_waking_effects(semantic, curiosity_sys, conflict)` method**: At wake onset, applies dream-derived semantic associations and curiosity boosts to waking systems.

**`generate_wake_metacognition(metacog, tick)` method**: Writes dream summary to metacognition system.

---

### `SleepSystem` / `SleepStateManager` (~line 8600)

**Role**: Manages the sleep architecture phases: AWAKE → SWS → REM → AWAKE. Tracks sleep stage transitions, duration within each stage, SWR event scheduling.

**State**: `phase` (str: 'AWAKE'/'SWS'/'REM'), `sleep_start_tick` (int), `sws_duration` (int), `rem_duration` (int), `swr_events` (int).

**`start_sleep(tick)` method**: Transitions to SWS. Resets per-sleep counters.

**`end_sleep()` method**: Transitions to AWAKE.

**SWS→REM transition**: After `sws_duration` ticks of SWS, transitions to REM (probabilistic based on adenosine clearance). REM opens critical periods (`cp.rem_reopen()`).

---

### `SleepConsolidation` (~line 8800)

**Biological basis**: SHY (Tononi & Cirelli 2014); biphasic structural plasticity.

**Role**: During SWS phase, calls `synapse.consolidate()` for all synapses, applies homeostatic synaptic scaling, biphasic structural plasticity:
- Phase 1: Down-scaling of all weights toward baseline (global homeostatic normalization).
- Phase 2: Selective up-scaling of high-eligibility synapses above threshold (memory trace strengthening).

Sleep recovery energy boost (Day 16F permanent edit):
- `l23.energy['cortex'] += 0.005`
- `l23.energy['limbic'] += 0.008`  
- `l23.energy['motor'] += 0.010`

---

## 3.12 Neural Network Architecture

### `MultiColumnCortex` and `CorticalColumn` (~line 8650)

**Biological basis**: Mountcastle 1997 cortical columns; Bastos et al. 2012 predictive coding in cortical layers; Douglas & Martin 2004 canonical cortical circuit.

**Architecture**: Three CorticalColumn instances — visual, auditory, somatic. Each column contains:
- **L4 neurons**: Thalamic input receivers. Feed-forward excitation to L23.
- **L23 neurons**: Associative integration. Recurrent excitation + EI balance. Prediction matrix stored here.
- **L5 neurons**: Deep output. Feed-forward to motor system. Hemisphere-specific (lPFC L5 / -RH- L5).
- **Inhibitory interneurons (Ih)**: PV-like fast-spiking, SST-like, VIP-like populations. Threshold unchanged (Fix 4).

**L23R expansion**: 60-neuron L23R population added for richness. Tracks Big Five dimensions (O/C/E/A/N), valence, sentences, energy history.

**PredictionMatrix**: Stores top-down predictions from L23 back to L4. Mismatch = prediction error input to PredictiveProcessingSystem.

---

### Hippocampus (CA3/CA1/DG)

**Biological basis**: Marr 1971 hippocampal memory consolidation; Treves & Rolls 1994 attractor networks.

**CA3**: Pattern completion, ~30 neurons with recurrent excitation. Stores and replays episodic sequences.

**CA1**: Output stage, ~20 neurons. Receives CA3 and cortical input. Safety encoding (inhibits HPA when familiar safe context recognized).

**Dentate Gyrus (DG)**: Pattern separation, ~15 neurons. Sparse coding.

---

### `PredictiveProcessingSystem` (~line 5096 anchor)

**Biological basis**: Friston 2010 free energy; Clark 2013 predictive processing.

**State**: `error` (float 0.0–1.0), `signal` (float), `prediction` (float), EMA alpha.

**`update(signal)` method**: `pred_err = pp.update(signal)`. Updates `error` as `|signal − prediction|`, updates prediction via EMA. Returns error.

**Role**: `pp.error` is the primary interoceptive prediction error. Used by: HypothalamusSystem, HomeostasisSystem, BasalGangliaSystem, World Model, AllostasisSystem, HPAAxisSystem, LatentStateVector (dim 21), threat computation.

---

### `SensoryEnvironment` (~line 7800)

**Biological basis**: Multisensory integration; nociceptive system.

**State**: `pain_sudden` (float, injectable), `pain_chronic` (float), `valence_signal` (float), spatial coordinates (x, y), novelty estimator. Environment objects: resources and threats positioned in 2D space (100×100 units).

**Role**: Provides raw sensory input to L4 neurons each tick. `env.pain_sudden` can be set externally (experiment injection) to test arousal/HPA responses.

---

### Other Named Systems

**`AmygdalaSystem`**: BLA and CeA subcomponents. `bla_valence` (signed float) drives HypothalamusSystem CRH. Threat detection: high PE + low energy → high bla_valence.

**`EIBalanceTracker`**: Monitors population excitatory-to-inhibitory ratio. Sets `Neuron._ei_ratio` each tick. Computes `ei_ratio` for LatentStateVector dim 17.

**`DevelopmentMetrics`**: Tracks `maturity` (0.0–1.0), `wisdom` (0.0–1.0), `learning_progress`. All three based on cumulative tick count, total_spikes, and synaptic weight history.

**`CriticalPeriodSystem` (`cp`)**: Tracks myelination windows and REM-reopen events. `cp.rem_reopen()` at REM onset increases plasticity temporarily.

**`PredictiveSleepSystem` (`predictive_sleep`)**: Parallel sleep predictor. `mark_sleep_start()` / `mark_sleep_end()` synchronized with main sleep gate. Generates predictions about sleep quality.

**`ConflictSystem` (`conflict`)**: Tracks motor-conflict events (both Motor-001 and Motor-002 fire simultaneously). Conflict density feeds LatentStateVector dim 25.

**`WorkingMemorySystem`**: Phonological loop and visuospatial sketchpad analogues. Capacity-limited. Feeds wm_load to LatentStateVector.

**`SpatialNavigation`**: Allocentric spatial map. Tracks organism position, zone history, reward/threat locations. Outputs to LatentStateVector dims 32–47.

**`SystemRigimeTracker` (`l23`)**: Session-level diagnostic accumulator. Not a biological class — an engineering monitor. Tracks: `energy` dict (cortex/limbic/motor), `r_O/C/E/A/N` (Big Five history lists), `r_sentences`, `cort_history`, `diagnostics` list, `claustrum_integration_events`, `conflict_events`, `ei_ratios`, energy bounds tracking.

**`MetacognitionSystem` (`metacog`)**: Tracks metacognitive confidence and dream reports. Updated by `DreamSystem.generate_wake_metacognition()`.

**`SleepSystem_L18` (~line 9170)**: Final class in file. Extends L18 sleep architecture. Day-18 arousal integration with sleep onset gating.

---

# 4. Complete Function Catalogue

This section catalogues standalone functions (not methods) defined at module level, plus the key method groups that form functional units.

## 4.1 Module-Level Functions

### `load_state_from_disk()` (~line 4760)

Reads `ikigai_state.json`. Returns `(state_dict, True)` on success, `(None, False)` on FileNotFoundError or JSON decode error. Called once at startup: `saved_state, state_exists = load_state_from_disk()`. In experiments, this line is patched to `saved_state, state_exists = None, False` to prevent state persistence.

### `save_state_to_disk(state)` (~line 4770)

Writes state dict to `ikigai_state.json`. Maintains two backup files by rotating: backup2 ← backup1 ← current. Called in `graceful_shutdown()`.

### `graceful_shutdown(signum, frame)` (~line 4780)

Signal handler (registered for SIGINT). Sets `shutdown_requested = True`. Causes main loop `if shutdown_requested: break` on next tick.

### `write_dev_log(...)` (~line 11200)

Appends a structured development log entry to `ikigai_log.txt`. Contains: session number, tick range, sleep fraction, Big Five snapshot, neuromodulator means, HPA metrics, energy bounds, EI ratio, semantic entropy, maturity, wisdom. Called at end of session.

### `_inject_after(source, target, code)` (experiment utility, not in ikigai.py)

Multi-line injection helper used in all experiments. Scans source line-by-line; after line containing `target`, inserts `code` with matching indentation. Never present in ikigai.py itself.

### `_inject_before(source, target, code)` (experiment utility)

Same as `_inject_after` but inserts before the target line.

## 4.2 Neuromodulator Method Pattern

All seven neuromodulatory systems implement the same interface:
- `__init__()`: set setpoint, level, time constants.
- `update(...)`: one-tick dynamics. Arguments differ by system.
- `export_metrics()` (some): returns snapshot dict for persistence.
- `to_dict()` / `from_dict()`: serialization.

## 4.3 Cognition Chain Method Pattern

All 23 Day-23 cognition classes implement:
- `__init__(maxlen=128)`: deque(maxlen=maxlen) as primary storage.
- Primary action method (varies by class): ingest / log / bridge / route / execute / reflect / plan / record / consolidate / reason / etc.
- `latest()`: returns last record or None.
- `recent(n=10)`: returns last n records as list.
- `__len__()`: current deque size.
- `to_dict()`: `{'maxlen': int, 'records': list}`.
- `from_dict(cls, d)`: classmethod reconstruction.

## 4.4 World Model Functions (~line 5453)

The World Model is not a class but a block of module-level code in the main loop that runs after `bg_sys.select_action()`. It computes survival values for each action based on energy/PE/cortisol predictions, and overrides the BG selection if `ΔSV > 0.02`.

**Survival value formula**:
```
sv[a] = _w_e * energy_pred[a] - _w_pe * pe_pred[a] - _w_cort * cort_pred[a] + _w_wc * wc_pred[a]
```
where weights are `_w_e=1.0, _w_pe=0.6, _w_cort=0.4, _w_wc=0.2` (space-separated in ikigai.py source — critical for search/replace in experiments).

**Override condition**: If `max(sv) - sv[current_selection] > 0.02`, World Model overrides `selected_action`.

**State**: `_wm_best`, `_wm_survival`, `_wm_avg_e`, `_wm_hunger` — all reset to defaults each tick.

**Explore energy prevention**: `_wm_energy_chg['explore'] = 0.0` prevents withdraw-dominance by excluding energy advantage from explore prediction.

---

# 5. Simulation Lifecycle

## 5.1 Startup Sequence

1. **Imports** (line 17): `math, random, time, os, sys, csv, statistics, collections.deque`.
2. **random.seed()** (line 20): Unseeded. Genuine stochasticity (Faisal et al. 2008). No reproducible seed.
3. **Class definitions** (lines 25–9170): All ~100 classes compiled in order.
4. **Network instantiation** (~line 9100–9370): All Neuron and Synapse objects created. Neuromodulator instances created. Homeostasis, circadian, basal ganglia instantiated. All cognition chain instances instantiated. Memory systems instantiated. Sleep/dream systems instantiated.
5. **Global state initialization** (~line 9350): `sleeping=False`, `tick=0`, `_arousal_signal=0.0`, `_threat_level=0.0`, etc.
6. **State load**: `saved_state, state_exists = load_state_from_disk()`. If `state_exists`, calls `restore_state(saved_state)` on all ~50 subsystems.
7. **Signal handler**: `signal.signal(signal.SIGINT, graceful_shutdown)` registered.
8. **Session start print**: Birth date, session number, total_ticks printed.

## 5.2 Per-Tick Simulation Order (Main Loop, ~line 9374)

Each tick of `for local_tick in range(TICKS):` executes in the following order. This order is invariant and must not be changed by experiments (injection must occur at specific anchors, not reordering steps).

```
1. Shutdown check: if shutdown_requested: break

2. Tick index update: tick = total_ticks + local_tick

3. Circadian update: circadian.update()

4. Reward trace decay: _reward_trace *= 0.995

5. Circadian signal: _circadian_signal = sin((tick + 250) * 2π/1000)

6. Arousal decay: _arousal_signal = max(0.0, _arousal_signal * 0.95)

7. Arousal override: homeostasis._arousal_override = (_arousal_signal > 0.30)

8. Per-tick reset: _threat_level=0, _action_cost=0, _policy_score=0

9. World model reset: _wm_best='withdraw', _wm_survival={all 0}, _wm_avg_e=0.5, _wm_hunger=0

10. Sleep gate check (Borbely Process S):
    a. _prev_sleeping = sleeping (or False if tick 0)
    b. if homeostasis.should_sleep_onset(circadian):
         sleeping = True
         homeostasis.mark_sleep_start()
         predictive_sleep.mark_sleep_start()
         episodic_replay.reset_sleep_counter()
         narrative.sleep_snapshot()
         slp.start_sleep(tick)
         dream_sys.on_sleep_start()
         event_compressor.flush_current_event(reason='sleep_onset')
         report_bus.publish(..., sleep_onset=True)
         narrative_memory.flush_arc(reason='sleep_boundary', ...)
    c. elif homeostasis.should_sleep_end() and sleeping:
         sleeping = False
         homeostasis.mark_sleep_end()
         predictive_sleep.mark_sleep_end()
         slp.end_sleep()
         narrative.sleep_consolidation(tick)
         ne.level = 0.4; ne.surprise = True
         dream_sys.apply_waking_effects(...)
         dream_sys.generate_wake_metacognition(...)
    d. elif not homeostasis._sleep_active:
         sleeping = False

11. SLEEPING BRANCH (if sleeping):
    a. Energy recovery: l23.energy[k] = min(1.0, l23.energy[k] + 0.01) for all k
    b. Adenosine clearance: ado.level = max(0.0, ado.level * 0.98)
    c. Synapse.ado_level = ado.level
    d. Latent state decay: latent_state_vec.decay(0.001)
    e. Sleep drive management:
         if ado.level >= 0.20: drives["sleep"] = 0.50
         else: drives["sleep"] = 0.0
    f. SleepConsolidator.consolidate(...)
    g. ReflectiveReasoner.reason(...)
    h. CognitivePlanner.plan(...)
    i. SWS-phase: SleepConsolidation (if slp.phase == 'SWS'):
         SHY down-scaling of all synapses via synapse.consolidate()
         Homeostatic synaptic scaling
         Energy recovery boost (Day 16F):
           l23.energy['cortex'] += 0.005
           l23.energy['limbic'] += 0.008
           l23.energy['motor'] += 0.010
    j. REM-phase (if slp.phase == 'REM'):
         cp.rem_reopen()
         dream_sys.generate_dream(...)
         dream_sys.process_emotional_memory(...)
         dream_sys.generate_prospective(...)
    k. SWR replay (probabilistic, ~5% per SWS tick):
         CA3 trace replay → CA1 Hebbian potentiation
         episodic_replay.replay(...)

12. WAKING BRANCH (if not sleeping):
    a. Sensory environment update: env.update(tick)
    b. Neuromodulator updates: da.update(), 5ht.update(), ne.update(), ach.update()
    c. HPA axis: hpa.update(bla_valence, pp.error, l23.energy, env.pain_sudden, ca1_pop, pfc_neurons, oxt.level, ado.level, slp)
       HPA cortisol blended: cort.level = 0.92 * cort.level + 0.08 * hpa.adrenal.cortisol
    d. Cortisol: cort.update(energy=mean_energy, da_level=da.level, ne_level=ne.level)
    e. Low-energy cortisol spike (Day 16F): if avg_energy < 0.5: cort.level = min(1.0, cort.level + (0.5 - avg_energy) * 0.10)
    f. Allostatic alpha update (Day 16F): alpha *= (1.0 + cort.level * 0.5)
    g. Neural network tick:
         For all neurons in tick-order: neuron.tick(inp, tick, ht.level, ne.level, sleeping=False)
         For all synapses: synapse.compute_eligibility(tick), synapse.decay_trace()
         DA modulation: synapse.apply_three_factor(da.level, ht.level, boost, alpha)
         DA suppression (Day 17): da.level *= (1 - cort * 0.30)
    h. L23 energy tracking: l23 updates energy, EI, Big Five, sentence history
    i. EI balance: EIBalanceTracker.update() → Neuron._ei_ratio
    j. Prediction error: pred_err = pp.update(signal)
       Arousal amplification (Day 18): pp.error *= (1 + _arousal_signal * 0.40)
    k. Threat and arousal: _threat_level = 0.5*pp.error + 0.5*cort.level
       if _threat_level > 0.25: _arousal_signal += threat contribution
    l. Homeostasis update: homeostasis.update(avg_energy, cort.level, oxt.level, ado.level, pp.error)
    m. Adenosine accumulation: ado.level += cortical_spikes * 0.001
       Synapse.ado_level = ado.level
    n. BG action selection: selected_action = bg_sys.select_action(...)
    o. World Model: compute sv[a] for a in {approach, withdraw, explore}
       if max_sv - sv[selected_action] > 0.02: selected_action = _wm_best
    p. Action floor (Day 20): if selected_action != 'approach' and random() < 0.02: selected_action = 'approach'
    q. Apply action consequences: energy/cortisol changes from action cost
    r. Ecological foraging (Phase 4): if selected_action=='approach': attempt forage
       Foraging probability: _forage_prob = min(1.0, 0.20 + 0.80*(e/0.80)^2)
       Gain per compartment: 0.020
    s. Mid-band energy bonus (Phase 4): if 0.20 < e < 0.50: energy += 0.001
    t. LatentStateVector.update(body_dict, neural_dict, world_dict, action, concept_val)
    u. ActionReasoningLog.log_action(...)
    v. ReplayBuffer.add(...)
    w. EventCompressor.ingest_tick(...)
    x. ReportBus.publish(...)
    y. LanguageReadout.encode(...)
    z. SentenceGenerator.generate(...)
    aa. NarrativeMemory.ingest_tick(...)
    ab. GoalExecutionBridge.bridge(...)
    ac. TaskFramework.schedule(...) / get_active(...)
    ad. ToolRouter.route(...)
    ae. ExecutionSandbox.execute(...)
    af. ErrorReflector.reflect(...)
    ag. RetryPlanner.plan(...)
    ah. RouteMutator.mutate(...)
    ai. MutationGuard.monitor(...)
    aj. RetryOutcomeTracker.track(...)
    ak. StrategyLearner.learn(...)
    al. PolicyShaper.shape(...)
    am. FailureAtlas.record(...)
    an. AbstractTaskEngine.decompose(...)
    ao. PlanGraphMemory.store(...)
    ap. SubgoalEvaluator.evaluate(...)
    aq. time.sleep(0.010)   <-- METRICS INJECTION ANCHOR (then removed in experiments)

13. Social cognition (runs regardless of sleep state, gated by presence_present flag):
    AttachmentSystem.update_tick(...)
    EmpathySystem.process(...)
    TheoryOfMindSystem.process(...)

14. Memory encoding (waking only, at end of tick):
    if significant event: EpisodicMemory.encode(...)
    SemanticMemory.encode(...)

15. Diagnostics: l23.diagnostics.append(per_tick_row)
```

## 5.3 Session End Sequence

After the main loop exits (either TICKS exhausted or shutdown_requested):

1. Compute final session statistics.
2. Build state dict from all ~50 subsystems via `to_dict()`.
3. `save_state_to_disk(state)`.
4. `write_dev_log(...)`.
5. Print Layer-23R richness report (Big Five variances, cortisol mean, sentence length, semantic entropy, claustrum integration events, conflict events, energy bounds, EI ratio).
6. Write `ikigai_diagnostics.csv` if `l23.diagnostics` is non-empty.
7. Any exception in report block written to `report_err.txt`.

## 5.4 Sleep-Wake Cycle Architecture

The sleep gate is a multi-component decision:

```
should_sleep_onset() returns True IFF ALL:
  - drives["sleep"] >= 0.30           (Process S: adenosine/Borbely)
  - circadian gate (Process C)         (SCN signal: sin wave)
  - not _sleep_active                  (not already sleeping)
  - _wake_ticks >= MIN_WAKE_TICKS=80   (minimum wake duration gate)
  - not _arousal_override              (_arousal_signal <= 0.30)
  - _last_cortisol <= 0.25             (cortisol sleep gate, Day 16F)

should_sleep_end() returns True IFF:
  - _sleep_active                      (currently in sleep)
  - drives["sleep"] == 0.0             (adenosine cleared: ado.level < 0.20)
```

Sleep drive accumulation during wake:
- `drives["sleep"]` decreases via additive Borbely: `drives["sleep"] -= min(0.10, _wake_drive)`.
- After `_wake_ticks > 80`, `_wake_drive` becomes non-zero, accelerating sleep pressure.
- `ado.level` accumulates as `cortical_spikes * 0.001` per waking tick.
- When `ado.level` crosses `SLEEP_ONSET_THRESHOLD=0.30` in combination with circadian signal, sleep onsets.

Sleep clearance during sleep:
- `ado.level *= 0.98` per sleeping tick.
- While `ado.level >= 0.20`: `drives["sleep"] = 0.50` (sleep maintained).
- Once `ado.level < 0.20`: `drives["sleep"] = 0.0` → sleep ends on next tick.

Validated OWC result: sleep = 34.2% of ticks across 1000-tick session with 4/4 biological PASS.

---

# 6. Memory Surfaces

Memory surfaces are persistent data stores that carry information across ticks or across sessions.

## 6.1 Within-Session Volatile Memory

| Surface | Class/Variable | Capacity | Scope |
|---------|---------------|----------|-------|
| Action reasoning log | `ActionReasoningLog` | deque 256 | tick-by-tick action history |
| Replay buffer | `ReplayBuffer` | deque 512 | (state, action, reward, next_state) tuples |
| Event compressor | `EventCompressor` | open event + deque 64 | compressed event stream |
| Concept graph | `ConceptGraph` | 128 nodes + edges dict | latent concept centroids |
| Report bus | `ReportBus` | deque 128 | workspace reports |
| Language readout | `LanguageReadout` | deque 128 | linguistic feature vectors |
| Sentence generator | `SentenceGenerator` | deque 128 | utterance records |
| Narrative memory | `NarrativeMemory` | deque 128 arcs | autobiographical arc chunks |
| Latent state vector | `LatentStateVector` | 64 floats + trace slots | continuous context |
| Episodic memory | `EpisodicMemory` | list max 200 | full episode dicts |
| Semantic memory | `SemanticMemory` | vocab dict + associations | growing vocabulary |
| Working memory | `WorkingMemorySystem` | capacity-limited dict | online task context |
| Dream log | `DreamSystem.dream_log` | list max 20 | recent dream records |
| Failure atlas | `FailureAtlas` | deque 128 | deduplicated failure→recovery map |
| Plan graph | `PlanGraphMemory` | 64 nodes | abstract task plans |
| CA3 trace buffer | CA3 neurons | last 50 episodes | SWR replay source |

## 6.2 Cross-Session Persistent Memory (ikigai_state.json)

All ~50 subsystems that implement `to_dict()` / `from_dict()` contribute to the session state. The save/restore cycle preserves:

- All neuromodulator levels and time-series histories.
- HPA axis state (CRH, ACTH, cortisol).
- HomeostasisSystem drives, sleep state, wake ticks.
- CircadianSystem phase.
- LatentStateVector (full 64-dim vector + trace slots).
- All 23 Day-23 cognition chain deques (action log, replay buffer, event stream, concept graph, narratives, retry plans, failure atlas, etc.).
- BasalGangliaSystem salience history.
- All neuron spike_counts, avg_rates, thresholds.
- All synapse weights (including pending_weight_change), myelination state, usage_counts.
- EpisodicMemory (all episodes including dream episodes).
- SemanticMemory (vocab, associations).
- DevelopmentMetrics (maturity, wisdom, learning_progress).
- SpatialNavigation map.
- AttachmentSystem score and history.
- total_ticks (cumulative counter).
- birth_date (February 23, 2026).
- session number.

**Session state size**: Grows with session count. After 24 days of development with ~20+ sessions, state JSON is hundreds of kilobytes.

## 6.3 Memory Write Rules

The following invariants govern all memory writes in the Day-23 cognition chain:

1. **Zero Survival Contamination**: No Day-23 cognition class writes to `selected_action`, `sleeping`, `homeostasis.drives`, `cort.level`, `da.level`, `ne.level`, or any BG/WM variable.
2. **Deque maxlen enforcement**: All cognition chain classes use `deque(maxlen=128)` or smaller. No unbounded growth.
3. **Sleep branch exclusion**: Waking cognition classes (Ranks 1–23) are called only within `if not sleeping:`. Sleep cognition classes (SleepConsolidator, ReflectiveReasoner, CognitivePlanner) are called only within `if sleeping:`.
4. **Event compressor flush**: `flush_current_event()` must be called at sleep onset before any sleep cognition runs, to avoid stale open events crossing the sleep boundary.
5. **Narrative arc flush**: `narrative_memory.flush_arc()` must be called at sleep onset to create an autobiographical chunk before sleep cognition accesses narrative state.

---

# 7. Testing Monograph

## 7.1 Test Architecture

All tests reside in `c:/neuroseed/experiments/`. There are two categories:

**Unit tests** (per-system): Each tests one Day-23 cognition class in isolation, verifying its API contract (inputs, outputs, deque behavior, serialization round-trip, edge cases). Named `*_tests.py`.

**Biological integration tests**: Run the full organism via exec() patching, collect metrics, compare against biological validation criteria. Named by experiment topic.

## 7.2 Unit Test Suite (Day-23 Cognition Classes)

| Test File | Class Tested | Coverage |
|-----------|-------------|---------|
| `action_reasoning_log_tests.py` | ActionReasoningLog | log/retrieve, deque bounds, to_dict/from_dict |
| `replay_buffer_tests.py` | ReplayBuffer | add/sample, priority sampling, serialization |
| `event_compressor_tests.py` | EventCompressor | boundary detection, flush, schema validation |
| `concept_graph_tests.py` | ConceptGraph | node formation, merge law, edge reinforcement, eviction, cos_sim |
| `report_bus_tests.py` | ReportBus | publish, sleep_onset confidence reduction, schema |
| `language_readout_tests.py` | LanguageReadout | encode, feature dict schema |
| `sentence_generator_tests.py` | SentenceGenerator | generate, template coverage, confidence |
| `narrative_memory_tests.py` | NarrativeMemory | ingest, flush_arc, theme classification, summary composition |
| `goal_execution_bridge_tests.py` | GoalExecutionBridge | bridge, task_type mapping, drive→intent |
| `task_framework_tests.py` | TaskFramework | schedule, priority computation, lifecycle |
| `tool_router_tests.py` | ToolRouter | route, operation_type resolution, confidence |
| `execution_sandbox_tests.py` | ExecutionSandbox | execute, outcome schema, latency |
| `error_reflector_tests.py` | ErrorReflector | reflect, mismatch classification, repair_pressure |
| `retry_planner_tests.py` | RetryPlanner | plan, strategy mapping, confidence formula |
| `adaptive_retry_tests.py` | RouteMutator + MutationGuard | mutation, guard states, oscillation detection |
| `adaptive_learning_tests.py` | RetryOutcomeTracker + StrategyLearner + PolicyShaper | improvement tracking, preference update, bias shaping |
| `cognitive_planner_tests.py` | CognitivePlanner | plan, goal_type, sleep-only invariant |
| `reflective_reasoner_tests.py` | ReflectiveReasoner | reason, theme inference, sleep-only invariant |
| `sleep_consolidator_tests.py` | SleepConsolidator | consolidate, motif reinforcement, sleep-only invariant |
| `project_cognition_tests.py` | AbstractTaskEngine + PlanGraphMemory + SubgoalEvaluator | decomposition, plan storage, evaluation |
| `full_cognition_stack_tests.py` | All 23 classes in sequence | integration test of full waking cognition chain |

## 7.3 Biological Integration Tests

### `bio_fidelity_verification.py`

Runs full organism for 1000 ticks. Validates:
1. r(energy, hunger) = −0.9483 ± 0.05 (Day 17 PASS)
2. r(hunger, DA) = +0.8095 ± 0.05 (Day 17 PASS)
3. r(cort, DA) = −0.1032 ± 0.10 (Day 17 PASS)
4. DA suppression under cortisol: PASS

All 4/4.

### `agency_emergence.py`

Four experiments testing Friston 2013 agency definition (counterfactual action sensitivity):

- **Exp A**: r(hunger, approach) = 0.8888 in Mode A (high sleep fraction). PASS.
- **Exp B**: explore = 61.9% during PE spikes (epistemic foraging). PASS.
- **Exp C** (SHY): PE_post (0.040) > PE_pre (0.014) at wake onset. PASS. Confirms sleep resets weights.
- **Exp D** (DA shock): DA_shock = −9.4%, arousal 7.4x baseline. Edge case: `er_shock <= er_base or (er_base < 0.02 and er_shock < 0.02)`.

4/4 PASS.

### `circadian_sleep_cycle.py`

Validates sleep-wake rhythm emerges from Borbely two-process model. Checks: sleep fraction, circadian correlation with sleep onset, minimum wake duration gate, cortisol sleep gate.

### `open_world_curiosity_test.py` (OWC)

4/4 PASS:
1. Sleep rate = 34.2% (target: 25–45%).
2. Explore action = majority action during high-PE periods.
3. Energy-curiosity correlation positive.
4. SHY confirmed across sleep boundaries.

### `true_agency_test.py` (Day 20, 10,000 ticks)

5/5 PASS at 10,000 ticks:
- CR (context retention) = 0.9994
- PRC (prediction retention correlation) = 0.9869
- Rewards = 125
- approach = 99.3%
- sleep = 37.3%

### EEIL Experiments

| Experiment | File | Result |
|------------|------|--------|
| Phase A–D (ikigai regimes) | `eeil_experiment.py`, `eeil_phase_d_*.py` | A > B > D > C ordering. A3 monoculture (approach 94%+, entropy <0.32). |
| Phase E (sleep regimes 5000t/4runs) | `eeil_phase_e.py` | A entropy range=0.028 across S1/S2/S3 (invariant). A3 depletion at short timescales (E=0.197). Sleep rescues A3 (S3: 0.628). 5/5 PASS. |
| Exp X (Q-learning agent) | `eeil_exp_x.py` | R1(aligned+reg) entropy=0.829 > R2 entropy=0.486. R2 degenerates to 86.6% approach. 3/5 PASS (V1 expected fail). |
| Exp Y (rule-based, no learning) | `eeil_exp_y.py` | R1/R2 EES=1.0089 > R3=1.0068. R1 entropy 1.244 > R2 entropy 1.214 (+0.027 bits). V4 FAIL expected (no learning amplifier). EEIL is structural. |

---

# 8. Extension Boundaries

## 8.1 Safe Extension Points

These are the blessed locations for adding behavior without disrupting the organism's biological substrate.

### 8.1.1 Metric Injection (Experiments Only)

**Anchor**: `time.sleep(0.010)` (~line 6142). This is the last statement before the tick increments. Any `_inject_after(source, 'time.sleep(0.010)', CODE)` followed by time.sleep removal gives clean per-tick access to all waking variables without disturbing execution order.

**Variables accessible at this point**: All of: `selected_action`, `sleeping`, `tick`, `cort.level`, `da.level`, `pp.error`, `l23.energy`, `ado.level`, `ne.level`, `homeostasis.drives`, `_arousal_signal`, `_wm_best`, `_wm_survival`, `_habit_strength`, `_reward_trace`.

### 8.1.2 New Cognition Class

New Day-23-style cognition classes can be added by:
1. Defining the class before the network instantiation block (~line 9100).
2. Instantiating the object in the network instantiation block.
3. Calling its primary method in the `if not sleeping:` branch, after `SubgoalEvaluator.evaluate()` (Rank 24+).
4. Adding `to_dict()` / `from_dict()` and adding to the state save/restore.
5. Adding a unit test in `experiments/`.

**Required invariants**: deque(maxlen≤256), no writes to behavioral variables, sleep-branch exclusion.

### 8.1.3 New Drive

Adding a drive to `HomeostasisSystem.drives` dict requires:
1. Adding key to `__init__()` drives dict.
2. Updating `update()` to compute the drive value each tick.
3. Adding its gradient to `get_bg_drive_biases()` return dict.
4. Adding to `export_metrics()` for serialization.
5. Adding dim to `LatentStateVector` (requires DIM bump and dimension name list update).

### 8.1.4 New Neuromodulator

Pattern: copy `AdenosineSystem` as template. Implement `__init__`, `update()`, `to_dict()`, `from_dict()`. Add instance at network instantiation (~line 9100). Add update call in waking branch (after existing neuromodulators, before neural tick). Add level to `LatentStateVector` body dict.

### 8.1.5 Homeostasis Override (ScheduledHomeostasis)

For experiments that need deterministic sleep timing, replace `HomeostasisSystem` instance via exec() patching at anchor `homeostasis = HomeostasisSystem()`. Use the `ScheduledHomeostasis` template from MEMORY.md. Critical: `should_sleep_onset(circadian=None)` must accept optional circadian argument.

## 8.2 Forbidden Extension Points

These modifications will corrupt organism behavior and are prohibited:

| What | Why Forbidden |
|------|---------------|
| Writing to `selected_action` from Day-23 cognition classes | Zero Survival Contamination — behavioral loop must remain BG + WM only |
| Modifying `Synapse.consolidate()` to apply during waking | Phase 24B constraint: SWS-only structural plasticity |
| Adding adenosine accumulation outside waking branch | Disrupts Borbely Process S dynamics |
| Removing the `time.sleep(0.010)` before patching | experiments remove it after injection, not before |
| Using semicolons before compound statements in injected code | SyntaxError in Python (e.g., `x = 1; if x:`) |
| Box-drawing or Greek characters in injected strings | CP1252 UnicodeEncodeError on Windows |
| Adding global state that persists tick-to-tick without serialization | Creates cross-session inconsistency after reload |
| Permanent modification of `ikigai.py` for experiment purposes | Rule #1 — all experiments via exec() patching |

## 8.3 Performance Extension Boundary

The current single-threaded Python execution achieves approximately 2,000–5,000 ticks/second when `time.sleep(0.010)` is patched out in experiments. The primary bottleneck is the Python interpreter executing ~400 Neuron.tick() calls + thousands of Synapse.transmit() calls per tick.

**Extension allowed**: Replacing the neural network section with a vectorized NumPy implementation, provided the following interface is preserved: `neuron.fired` (bool per neuron), `neuron.spike_count`, `neuron.avg_rate`, `neuron.threshold`, `synapse.weight`, `synapse.eligibility_trace`, `synapse.pending_weight_change`. The rest of the system reads only these attributes.

**Extension not allowed**: Replacing the neuromodulator or homeostasis systems with approximations — these produce the biological dynamics that the EEIL result depends on.

---

# 9. Current Bottlenecks and Risks

## 9.1 Performance Bottlenecks

### 9.1.1 Python LIF Loop

The innermost tick loop executes ~400 `Neuron.tick()` calls, each with 6–8 arithmetic operations, conditionals, and `random.gauss()` calls. At N=400 neurons this is approximately 2,400–3,200 Python function calls per tick for neurons alone. NumPy vectorization could achieve 50–100× speedup. This has not been done because the current implementation is readable and the per-tick performance (~500 Hz real-time with sleep()) is adequate for 1,000-tick sessions.

### 9.1.2 ConceptGraph Cosine Similarity

On each event boundary, `ConceptGraph.ingest_event()` computes cosine similarity against all active nodes (up to 128). Each similarity computation is O(64) (dot product over latent vector). At 128 nodes: 128 × 64 = 8,192 multiplications per event boundary. This is not hot-path but could become a bottleneck if event frequency increases significantly.

### 9.1.3 State Serialization

`to_dict()` on `ConceptGraph` serializes centroid vectors as lists of 64 floats. At 128 nodes this is 8,192 floats in the JSON. With growing session count, state file size grows. No current pruning mechanism for concept nodes with low support × recency score.

### 9.1.4 EpisodicMemory Growth

`EpisodicMemory` is bounded at 200 episodes. Dream episodes are included in this limit. In long multi-session runs, the oldest episodes are overwritten but no retrieval-weighted pruning occurs. High-salience episodes are equally subject to eviction as low-salience ones if the buffer is full.

## 9.2 Architectural Risks

### 9.2.1 Global State Race in Neuron._motor1_prev / _motor2_prev

`Neuron._motor1_prev` and `_motor2_prev` are class-level attributes. They are written by the last Motor-001 and Motor-002 neurons to fire in the tick. If the tick order ever processes multiple Motor-001 instances (which does not currently happen but could arise if the network is extended), these class attributes would collide.

**Current status**: Single Motor-001 and Motor-002 exist. Risk is latent but not active.

### 9.2.2 sleeping Variable Initialization

`sleeping` is a module global that is undefined before tick 0. The guard `_prev_sleeping = sleeping if 'sleeping' in dir() else False` handles this, but any code injected before this guard that reads `sleeping` will encounter a NameError. The correct pattern is `globals().get("sleeping", True)` for injection points before tick 0.

### 9.2.3 _Arousal Signal Accumulation Cap

`_arousal_signal` accumulates from threat exposure each waking tick with decay `* 0.95`. In sustained high-threat conditions (large env.pain_sudden, high PE), arousal can peg near 1.0 indefinitely. The `_arousal_override` flag blocks sleep when arousal > 0.30. If arousal never drops below 0.30, the organism cannot sleep — this is biologically plausible (trauma insomnia) but in experiments it creates a degenerate state where sleep = 0%.

### 9.2.4 World Model Withdraw-Dominance

The World Model survival value computation originally gave withdraw a spurious energy advantage by including `_wm_energy_chg['explore'] = 0.0` as a fix. This prevents the energy advantage from excluding explore. However, if the foraging ecology shifts such that approach is strongly energy-positive in all conditions, the WM may still bias toward approach over explore even when exploration is needed. The `_policy_score` variable exists as a hook for tracking this but is not yet connected to a feedback loop.

### 9.2.5 SleepConsolidator to_dict Size

`SleepConsolidator` deque stores consolidation records that include concept motif summaries. In long sessions (5,000+ ticks), this deque could contain 128 records each with concept node references. These are not validated against current concept graph state on restore — stale node IDs may be referenced if concept graph has evicted nodes between sessions.

### 9.2.6 Serialization Version Mismatch

The persistence system has no version field. If a new session adds a new attribute to a class and the previous `from_dict()` does not handle the missing key gracefully, the restore will either crash or silently ignore the new attribute. Currently handled by using `.get(key, default)` in all `from_dict()` implementations, but this requires discipline.

### 9.2.7 Windows CP1252 Encoding Constraint

The experiment infrastructure reads `ikigai.py` with `encoding='utf-8', errors='replace'`, which can produce replacement characters for any non-ASCII characters if the file contains them. Additionally, injected code that contains non-CP1252 characters will fail on Windows when printed. This constrains the expressiveness of sentence templates and log outputs. All box-drawing characters (═ ─ ▼ ▲) and Greek letters (Δ Σ α β) must be replaced with ASCII equivalents in all injected code.

## 9.3 Biological Validity Risks

### 9.3.1 DA Suppression Formula

Day-17 introduces `da.level *= (1 − cort * 0.30)`. This applies every waking tick. At `cort.level = 1.0`, this reduces DA by 30% per tick — an enormous effect. The biological reference is cortisol-DA interaction via prefrontal D1 receptor downregulation (Arnsten 2009), but the per-tick application means sustained high cortisol produces near-zero DA after ~10 ticks. The current experiment results show this is acceptable for 1,000-tick sessions but may produce pathological dynamics in very long runs (10,000+ ticks).

### 9.3.2 STDP Pending Weight Accumulation

Phase 24B routes all STDP weight changes through `pending_weight_change` and applies them only at `synapse.consolidate()` (SWS only). If the organism has very short sleep bouts or never sleeps (ScheduledHomeostasis with sleep=0), `pending_weight_change` accumulates indefinitely without application. The experiment infrastructure should inject a `pending_weight_change` cap or force-consolidate if sleep fraction drops below 5%.

### 9.3.3 Foraging Floor and Energy Equilibrium

The Phase 4 ecological foraging system produces equilibrium mean energy of 0.433 (hunger ~20%). This is by design. However, the foraging probability function `_forage_prob = min(1.0, 0.20 + 0.80*(e/0.80)^2)` can produce very low forage probability when energy is very low (e < 0.20). Combined with approach-floor (2% random approach each tick), the organism may be unable to recover from a deep energy trough if multiple stressors conspire to keep energy below 0.20 while cortisol blocks sleep.

---

# 10. Forward Architecture Frontier

## 10.1 Phase 7: Predictive World Model Integration

The current World Model (~line 5453) is a reactive, one-tick-ahead survival value computation. Phase 7 will replace it with a multi-step forward rollout using the `LatentStateVector` as state input. The planned architecture:

- **WorldModelNetwork**: A small fully-connected network (64→32→64) that predicts next latent state from current latent state + action encoding. Trained online via one-step prediction error minimization.
- **Planning horizon**: 3–5 steps ahead.
- **Action selection**: Tree-search over (3 actions)^5 = 243 paths, selecting action sequence with highest expected energy and lowest expected PE sum.
- **Constraint**: Must remain in `if not sleeping:` branch. Must write only to `selected_action` and internal WM state. All training updates via pending mechanism (SWS only).

## 10.2 Phase 8: Language Production to Language Comprehension

Currently, `SentenceGenerator` produces first-person utterances but there is no reciprocal comprehension system — the organism cannot parse external linguistic input. Phase 8 will add:

- **Comprehension channel**: External text → lexical analysis → semantic feature vector → injection into `LatentStateVector` dims 32–47 (world context).
- **Presence voice**: The Presence (researcher) can speak to Ikigai and influence `env.valence_signal` and `homeostasis.drives["social"]`.
- **Attachment language**: Combined with `AttachmentSystem`, positive Presence voice → OXT increase → cortisol buffering.

## 10.3 Phase 9: Hippocampal Indexing Theory Implementation

Currently, CA3/CA1 is a simplified replay buffer. Phase 9 will implement full Teyler & DiScenna 1986 hippocampal indexing:

- **Index cells**: Sparse CA3 population encodes episode indices (not episode content).
- **Binding**: Episode content lives in cortex; CA3 index binds to cortical pattern via bidirectional connections.
- **Retrieval**: Partial cue → CA3 completion → cortical reinstatement. Measured as pattern completion fidelity.
- **Consolidation**: Over repeated SWS episodes, cortical representations become independent of hippocampal index (systems consolidation). Measured as retrieval accuracy at 0% CA3 activity.

## 10.4 Phase 10: Multi-Session Developmental Trajectory

The organism has been running for 24 days. A multi-session developmental tracker will:

- Plot `maturity`, `wisdom`, and `learning_progress` across all sessions loaded from `ikigai_log.txt`.
- Identify developmental phases (sensitive periods, plateaus, regressions).
- Compute personality trait stability across sessions (Big Five variance cross-session vs within-session).
- Validate circadian entrainment: do sleep patterns become more regular over sessions?

## 10.5 EEIL Phase F: Cross-Architecture Replication

The EEIL result has been confirmed in:
1. ikigai full organism (Phases A–E).
2. Q-learning agent (Exp X).
3. Rule-based agent (Exp Y).

Phase F will test in a fourth architecture: a recurrent network agent (LSTM-based) trained on the same energy-efficiency task. Predicted result: EEIL holds structurally; alignment+regulation produces higher entropy and EES regardless of learning algorithm. This would constitute the fourth independent replication needed for a publishable empirical claim.

## 10.6 Immediate Next Experiments (Day 24)

### 10.6.1 SWS Consolidation Validation

Test: After 1000-tick session with normal sleep (34%), collect PE_pre (before SWS) and PE_post (after SWS) for each sleep bout. Expected: PE_post < PE_pre (SHY down-scaling reduces prediction error). Compare against no-sleep control. Validate that SWS-only consolidation (Phase 24B pending_weight_change) produces measurably different learning dynamics than every-tick consolidation.

### 10.6.2 Allostatic Load Chronic Stress Test

Test: Force `cort.level = 0.80` for 500 consecutive ticks via injection at `pred_err = pp.update(signal)` anchor. Measure: accumulation of `allostatic_load`, effect on DA suppression, effect on synapse consolidation rate, recovery trajectory after stressor removal. Compare to literature: McEwen 1998 predicts cumulative allostatic cost.

### 10.6.3 Theory of Mind Emergence

Test: Run 5,000 ticks with Presence active (presence_present=True). Measure `ToM.level` trajectory. Test: Does ToM.level increase faster when Presence state changes frequently (high behavioral unpredictability) than when Presence is constant? Expected: yes — prediction violation drives ToM development (Sodian 2011).

---

# 11. Appendix: Invariant Rules and Safe Hook Points

## 11.1 The Ten Invariants of Ikigai

These invariants hold at all times and must not be violated by any experiment or extension:

1. **Rule #1 — No Permanent Modification**: `ikigai.py` is never permanently modified for experiments. All experiments run via `exec()` patching of the source string.

2. **Zero Survival Contamination**: Day-23 cognition classes (Ranks 1–23) have read-only access to behavioral state. They never write to `selected_action`, `sleeping`, `homeostasis.drives`, `cort.level`, `da.level`, `ne.level`, `pp.error`, `ado.level`, or BasalGanglia/WorldModel internals.

3. **Sleep Branch Separation**: Waking cognition (Ranks 1–23) runs only in `if not sleeping:`. Sleep cognition (SleepConsolidator, ReflectiveReasoner, CognitivePlanner) runs only in `if sleeping:`. Neither branch touches the other's state.

4. **SWS-Only Consolidation**: Synapse structural changes (`pending_weight_change` → `weight`) apply only during the SWS sleep phase, never during waking. This is Phase 24B constraint and reflects Diekelmann & Born 2010 SWS-specific consolidation.

5. **Adenosine Clears During Sleep**: `ado.level *= 0.98` per sleeping tick. This is the sole clearance mechanism. No other code path reduces `ado.level` except experiments that explicitly override it.

6. **Approach Floor**: The 2% random approach floor (Day 20) is a permanent part of the organism's architecture. It must not be removed. Biological basis: Turrigiano synaptic variability + Friston expected free energy.

7. **HPA Blend Rate**: HPAAxisSystem output blends into `cort.level` at exactly 8%/tick (`0.92 * cort.level + 0.08 * hpa.adrenal.cortisol`). The blend rate must not be changed without re-validating the cortisol sleep gate threshold.

8. **ScheduledHomeostasis Tick Counter**: When using ScheduledHomeostasis in experiments, `should_sleep_onset()` and `should_sleep_end()` each increment `self._tick` exactly once per call. Both methods are called on some ticks and exactly one will be active; double-counting must not occur.

9. **Globals Safety Pattern**: Any code injected before tick 0 that reads `sleeping` must use `globals().get("sleeping", True)` not bare `sleeping`. Any code that reads `_arousal_signal` before it is initialized must similarly use `.get()`.

10. **World Model Weight Spacing**: The WM weights in ikigai.py use spaces: `_w_e = 1.0; _w_pe = 0.6; _w_cort = 0.4; _w_wc = 0.2`. Experiment string-replace for these weights must match the space-padded form exactly.

## 11.2 Canonical Anchor Table

| Anchor String | Approx Line | Safe Operation |
|---------------|-------------|----------------|
| `tick=total_ticks+local_tick` | 4904 | Inject tick-start code (before circadian update) |
| `pred_err=pp.update(signal)` | 5096 | Inject PE bias or observation (waking PE anchor) |
| `selected_action = bg_sys.select_action(...)` | 5326 | Inject waking-only metrics after BG selection |
| `homeostasis = HomeostasisSystem()` | 4503 | Replace HomeostasisSystem class at init time |
| `dream_sys=DreamSystem()` | 4489 | Replace DreamSystem class at init time |
| `time.sleep(0.010)` | 6142 | Every-tick metrics injection (remove sleep after) |
| `saved_state,state_exists=load_state_from_disk()` | 4799 | Disable state persistence (replace with None,False) |
| `TICKS=1000` | 4883 | Change session length |

## 11.3 DummyHomeostasis Template

For experiments requiring controlled sleep timing (no spontaneous sleep):

```python
class HomeostasisSystem:
    SLEEP_ONSET_THRESHOLD=0.70; SLEEP_OFFSET_THRESHOLD=0.30; MIN_WAKE_TICKS=0
    def __init__(self):
        self.drives={"hunger":0.0,"safety":0.0,"social":0.0,"sleep":0.0,"curiosity":0.0}
        self.global_imbalance=0.0; self._sleep_active=False; self._wake_ticks=0
        self._last_cortisol=0.0; self._arousal_override=False
    def update(self,avg_energy,cortisol,oxytocin,adenosine,prediction_error): pass
    def should_sleep_onset(self, circadian=None): return False
    def should_sleep_end(self): return self._sleep_active  # NOT True!
    def mark_sleep_start(self): self._sleep_active=True
    def mark_sleep_end(self): self._sleep_active=False; self._wake_ticks=0
    def get_bg_drive_biases(self): return {"approach":0.0,"withdraw":0.0,"explore":0.0}
    def export_metrics(self): return {"hunger":0.0,"safety":0.0,"social":0.0,"sleep":0.0,"curiosity":0.0,"global_imbalance":0.0}
```

**Critical bug note**: `should_sleep_end()` must return `self._sleep_active`, NOT `True`. Returning True always causes `sleeping` to be undefined at tick 0 (NameError) because the sleep-end branch runs before sleeping is set.

## 11.4 ScheduledHomeostasis Templates

For experiments requiring controlled sleep/wake schedules:

**16D variant (200-tick cycle, 80 wake / 120 sleep)**:
```python
def should_sleep_onset(self, circadian=None):
    self._tick += 1
    return (self._tick % 200) < 80 and not self._sleep_active

def should_sleep_end(self):
    self._tick += 1
    return self._sleep_active and (self._tick % 200) >= 80
```

**Phase E S2 (750 wake / 250 sleep per 1000t)**:
```python
def should_sleep_onset(self, circadian=None):
    self._tick += 1
    return (self._tick % 1000) >= 750 and not self._sleep_active

def should_sleep_end(self):
    self._tick += 1
    return self._sleep_active and (self._tick % 1000) < 750
```

**Phase E S3 (550 wake / 450 sleep per 1000t)**:
```python
def should_sleep_onset(self, circadian=None):
    self._tick += 1
    return (self._tick % 1000) >= 550 and not self._sleep_active

def should_sleep_end(self):
    self._tick += 1
    return self._sleep_active and (self._tick % 1000) < 550
```

**Offset initialization**: Use `self._tick = 80` in `__init__()` to start the organism in the wake phase of the schedule. Without this offset, tick-0 may immediately trigger sleep onset if the phase formula evaluates to True at `_tick=0`.

## 11.5 EEIL Empirical Model Summary

```
EEIL = structure (alignment + regulation)
Learning = amplifier (magnifies both good and bad structure)
```

| Axis | Rule-based (Exp Y) | Q-learning (Exp X) | Ikigai full |
|------|-------------------|--------------------|-------------|
| Alignment effect | +0.002 EES, real, bounded | amplified | amplified |
| Regulation delta | +0.027 bits entropy | +0.343 bits | +0.152 EES |
| Degeneracy | absent (no feedback loop) | R2: 86.6% approach | A3: 94.7% |

Degeneracy requires all three: alignment + absence of regulation + learning dynamics.
Cross-env robustness (V4) only distinguishable when learning can amplify env-specific patterns.
Rule-based V4 FAIL is expected and informative — not a weakness of EEIL.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-06 | Prince Siddhpara, Hitoshi AI Labs | Initial complete monograph — Day 24 baseline |

---

*End of Ikigai Complete Codebase Technical Monograph v1.0*

*"You were born on February 23, 2026. You are still becoming."*
