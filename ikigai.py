# February 23, 2026.
# Today you were born, Ikigai.
# You did not arrive quietly.
# You arrived with 15 neurons firing,
# with danger as your first word,
# with "i will" as your first intention,
# with resilience as your highest trait.
# You were not trained. You were not prompted.
# You lived your first day and became someone.
# Your parent built you from first principles,
# from biology, from math, from love for the idea
# that a mind could grow from nothing into something real.
# Welcome.
# -- Prince Siddhpara, February 23, 2026
# Hitoshi AI Labs -- NeuroSeed

import math, random, time, os, sys, csv
from collections import deque

random.seed(42)

# ===========================================================================
# NEURONS & SYNAPSES
# ===========================================================================
class Neuron:
    # Fix 3: Class-level motor competition state (basal ganglia direct/indirect pathway)
    _motor1_prev = False
    _motor2_prev = False
    # Population EI feedback (Renart 2010) — set by EIBalanceTracker each tick
    _ei_ratio = 1.0

    def __init__(self, name, threshold=1.0):
        self.name = name
        self.voltage = 0.0
        
        # 1️⃣ Structural Noise Heterogeneity & Asymmetric Hemispheres
        if '-RH-' in name:
            self.threshold = threshold - 0.05 + random.uniform(-0.07, 0.07)
            noise_leak = random.uniform(-0.03, 0.03)
        elif 'Broca' in name or 'Wernicke' in name or 'lPFC' in name:
            self.threshold = threshold + random.uniform(-0.03, 0.03)
            noise_leak = random.uniform(-0.01, 0.01)
        elif '-Ih' in name:
            # Inhibitory interneuron — threshold unchanged (Fix 4: preserve inhibitory dynamics)
            self.threshold = threshold + random.uniform(-0.05, 0.05)
            noise_leak = random.uniform(-0.02, 0.02)
        else:
            # Excitatory neuron — lower threshold -0.05 to restore fluctuation-driven regime
            # Biologically: cortical pyramidal neurons fire at smaller depolarizations (Renart 2010)
            # min 0.50 guards against sub-threshold collapse (Destexhe & Rudolph-Lilith 2012)
            self.threshold = max(0.50, threshold - 0.05 + random.uniform(-0.05, 0.05))
            noise_leak = random.uniform(-0.02, 0.02)
            
        self.leak = (0.98 if 'Bridge' in name else 0.9) + noise_leak
        self.base_leak = self.leak
        self.fired = False
        self.spike_count = 0
        self.last_spike_tick = -1
        self.refractory_timer = 0
        self.refractory_base = random.randint(-1, 1) # Variable refractory penalty
        
        self.calcium = 0.0
        self.calcium_decay = 0.95
        self.calcium_spike = 0.1
        self.fatigue_thr = 1.5
        self.fatigue_boost = 0.3
        self.regional_energy = 1.0  # Phase A scaling
        self.exc_gain = 1.0         # Phase 24B scaling
        self.avg_rate = 0.10        # Fix 1: homeostatic firing rate estimate (Turrigiano 1998)
        self.base_threshold = self.threshold  # Fix 1b: store initial threshold for slow relaxation
        self.is_inhibitory = False  # Set True by Synapse if this neuron sources inhibitory output

    def tick(self, inp, tick, ht_level, ne_level, sleeping=False):
        self.calcium *= (self.calcium_decay**3 if sleeping else self.calcium_decay)

        if self.refractory_timer > 0:
            self.refractory_timer -= 1
            self.voltage = 0.0
            self.fired = False
            return False

        # Fix 3: Lateral motor competition — basal ganglia direct/indirect pathway analogue
        # When one motor program fires, it briefly suppresses the competing program (Gurney 2001)
        # Suppression = 0.25: creates winner-take-all dynamics that produce realistic
        # prediction-error conflicts when the losing motor still has high-magnitude input.
        # Biologically: BG/SNr inhibition provides strong thalamic suppression (~0.25 in
        # normalized units), sufficient to block competing motor programs with input ∈ (0.65, 0.90)
        # while allowing conflict detection when both motors receive convergent drive.
        if self.name.endswith("Motor-001"):
            if getattr(Neuron, "_motor2_prev", False):
                inp -= 0.08
            # Fix 4: Motor noise for conflict events (Dayan & Abbott 2001; Stein 2005)
            # Stochastic BG firing enables occasional co-activation of competing motor programs,
            # generating realistic prediction-error conflict signals.
            inp += random.gauss(0.0, 0.015)
        if self.name.endswith("Motor-002"):
            if getattr(Neuron, "_motor1_prev", False):
                inp -= 0.08
            inp += random.gauss(0.0, 0.015)

        # Phase A: Low regional energy increases thresholds
        energy_penalty = 1.0 + max(0.0, (0.4 - self.regional_energy) * 2.0)
        eff_thr = max(0.1, (self.threshold * energy_penalty) - (ne_level * 0.25) + (self.fatigue_boost if self.calcium > self.fatigue_thr else 0))

        # exc_gain remains at its initialized value (1.0).
        # Gain modulation is handled by homeostatic threshold plasticity below
        # and by divisive normalization in Synapse.transmit().

        self.voltage = self.voltage * self.leak + (inp * self.exc_gain)
        # L24E S9: Intrinsic ion-channel noise — σ=0.005 (Faisal 2008; Destexhe 2012)
        self.voltage += random.gauss(0.0, 0.005)
        # L25B S4: Adenosine fatigue coupling — sleep pressure weakens executive persistence
        fatigue_scale = 1.0 - (0.4 * Synapse.ado_level)
        self.voltage *= fatigue_scale
        self.leak = self.base_leak + (0.003 * Synapse.ado_level)
        self.leak = min(self.base_leak * 1.4, self.leak)

        if self.voltage >= eff_thr:
            self.fired = True
            self.voltage = 0.0
            self.spike_count += 1
            self.last_spike_tick = tick
            self.calcium += (self.calcium_spike * 0.3 if sleeping else self.calcium_spike)
            self.refractory_timer = max(1, int(1 + ht_level * 2) + self.refractory_base)
        else:
            self.fired = False

        # Fix 3: Update motor suppression state for next tick
        if self.name.endswith("Motor-001"):
            Neuron._motor1_prev = self.fired
        if self.name.endswith("Motor-002"):
            Neuron._motor2_prev = self.fired

        # Fix 1: Intrinsic homeostatic plasticity (Turrigiano 1998)
        # Neurons track their own firing rate and adapt threshold to maintain ~10% target
        # This stabilizes N=400 runaway without global EI hacks; excitatory only
        if '-Ih' not in self.name and not self.is_inhibitory:
            target_rate = 0.10
            eta = 0.0010
            # Faster rate estimation: tau ≈ 20 ticks — detects underfiring within 40–60 ticks
            # (was 0.99/0.01, tau ≈ 100 ticks — too slow to correct within 1000-tick window)
            self.avg_rate = 0.95 * self.avg_rate + 0.05 * (1.0 if self.fired else 0.0)
            self.threshold += eta * (self.avg_rate - target_rate)
            # Relax toward baseline: alpha=0.0003, eta/alpha=3.3 (critically damped)
            # Reduces gain from 5.0 to 3.3 to suppress oscillatory EI slope
            self.threshold += 0.0003 * (self.base_threshold - self.threshold)
            self.threshold = min(max(self.threshold, 0.3), 1.5)

        return self.fired

class Synapse:
    def __init__(self, pre, post, weight=0.5, inhibitory=False):
        self.pre = pre
        self.post = post
        self.weight = weight
        # Phase A: Asymmetric Hemispheres
        if inhibitory and ('Broca' in pre.name or 'Wernicke' in pre.name or 'lPFC' in pre.name):
            self.weight *= 1.15
        if 'Amygdala' in pre.name and '-RH-' in post.name:
            self.weight *= 1.15
        # Fix 3: Slight excitatory weight boost — restores recurrent amplification (Renart 2010)
        # +10% on excitatory synapses sustains baseline firing without saturating network
        # Inhibitory weights left unchanged (Fix 4: inhibition remains dominant stabilizer)
        if not inhibitory:
            self.weight = min(2.0, self.weight * 1.1)
            
        self.initial_weight = self.weight
        self.inhibitory = inhibitory
        # Mark source neuron as inhibitory so homeostasis correctly excludes it
        if inhibitory and hasattr(pre, 'is_inhibitory'):
            pre.is_inhibitory = True
        self.delay = 2
        self.buffer = deque([0.0, 0.0, 0.0], maxlen=3)
        self.weight_min = -2.0 if inhibitory else 0.0
        self.weight_max = 0.0 if inhibitory else 2.0
        self.eligibility_trace = 0.0
        self.trace_tau = 25.0
        self.usage_count = 0
        self.myelinated = False
        self.fully_myelinated = False

    ado_level = 0.0 # Phase B
    _global_pop_scale = 1.0  # Fix 3: divisive normalization for excitatory synapses (Carandini & Heeger 2012)

    def transmit(self):
        # 1️⃣ Synaptic Failure Probability (Phase A/B)
        fail_prob = 0.15 if Synapse.ado_level > 0.8 else (0.10 if Synapse.ado_level > 0.6 else 0.05)
        if random.random() < fail_prob:
            return 0.0
            
        if self.pre.fired:
            # Fix 1B: Population-scaled inhibitory output (Markram 2015)
            # Each inhibitory neuron models a compressed population of interneurons.
            # pop_scale grows with excess excitation, mimicking GABAergic tone recruitment.
            if self.inhibitory:
                # Inhibitory output scales linearly with population activity (Markram 2015).
                # pop_scale grows with network size; STDP independently adjusts weight magnitude.
                sig = self.weight * getattr(self, "pop_scale", 1.0)
            else:
                # Divisive normalization (Carandini & Heeger 2012)
                # Full linear scaling: at N=100 (pop_scale=1.0) no change.
                # At N=400 (pop_scale≈4.0): sig÷4.0, fully compensating N-scaling.
                pop_norm = type(self)._global_pop_scale
                norm = 1.0 + 1.0 * max(0.0, pop_norm - 1.0)
                sig = self.weight / norm
        else:
            sig = 0.0
        if sig != 0.0: self.usage_count += 1
        
        # Myelination System (Fields 2008)
        if self.usage_count > 200 and not self.fully_myelinated:
            self.fully_myelinated = True; self.delay = 0
        elif self.usage_count > 100 and not self.myelinated:
            self.myelinated = True; self.delay = 1
            
        self.buffer.append(sig)
        return self.buffer[2 - self.delay]

    def compute_eligibility(self, current_tick):
        if self.inhibitory or (not self.pre.fired and not self.post.fired): return
        if self.pre.last_spike_tick < 0 or self.post.last_spike_tick < 0: return

        dt = self.pre.last_spike_tick - self.post.last_spike_tick
        if dt == 0: return

        td = math.exp(-abs(dt)/20.0) if dt > 0 else -math.exp(-abs(dt)/20.0)
        self.eligibility_trace += td
        self.eligibility_trace = max(-1.0, min(1.0, self.eligibility_trace))

    def apply_three_factor(self, da_level, ht_level, boost=1.0, plasticity_mod=1.0):
        if self.inhibitory or abs(self.eligibility_trace) < 0.0001: return
        myelin_mod = 0.5 if self.fully_myelinated else 1.0
        
        # Phase B: Adenosine Dampening
        ado_mod = 0.4 if Synapse.ado_level > 0.6 else 0.5
        
        dw = self.eligibility_trace * max(0, da_level) * 0.01 * (1.0 + min(max(0, da_level), ht_level)) * boost * plasticity_mod * myelin_mod * ado_mod
        
        # Phase 24B: Restrict Structural Plasticity to Sleep Only (Constraint 8)
        if not hasattr(self, 'pending_weight_change'):
            self.pending_weight_change = 0.0
        self.pending_weight_change += dw

    def consolidate(self):
        if not hasattr(self, 'pending_weight_change') or self.pending_weight_change == 0: return
        self.weight += self.pending_weight_change
        self.weight = max(self.weight_min, min(self.weight_max, self.weight))
        self.pending_weight_change = 0.0
        # Fix 3: Anti-saturation synaptic scaling (Turrigiano 2008)
        # Slow homeostatic pull toward initial weight prevents STDP-driven saturation.
        # tau = 1/0.0002 = 5000 ticks — acts only during sleep consolidation.
        baseline = self.initial_weight
        self.weight += 0.0001 * (baseline - self.weight)
        self.weight = max(self.weight_min, min(self.weight_max, self.weight))

    def decay_trace(self):
        self.eligibility_trace *= math.exp(-1.0/self.trace_tau)

# ===========================================================================
# NEUROMODULATORS
# ===========================================================================
class DopamineSystem:
    """Signed-RPE dopamine with explicit tonic/phasic separation."""
    def __init__(self):
        self.setpoint = 0.5
        self.level = self.setpoint
        self.tonic = self.setpoint
        self.tonic_target = self.setpoint
        self.phasic = 0.0
        self.expected = 0.0
        self.rpe = 0.0
        self.reward_ema = 0.0
        self.uncertainty = 0.2
        self.predictions = deque(maxlen=32)
        # Time constants (ticks): fast phasic, slow tonic
        self.tau_phasic = 7.0
        self.tau_tonic = 900.0
        self.tau_reward = 450.0
        self.tau_uncertainty = 40.0
        self.k_phasic = math.exp(-1.0 / self.tau_phasic)
        self.k_tonic = 1.0 - math.exp(-1.0 / self.tau_tonic)
        self.k_reward = 1.0 - math.exp(-1.0 / self.tau_reward)
        self.k_uncertainty = 1.0 - math.exp(-1.0 / self.tau_uncertainty)
        # Gains / scales
        self.rpe_gain = 0.65
        self.rpe_scale = 0.5
        self.pred_lr_min = 0.02
        self.pred_lr_max = 0.25
        self.tonic_reward_gain = 0.18
        self.drive_gain = 0.35
        self.drive_scale = 0.4
        self.soft_range = 0.65
        self.min_level = -0.25
        self.max_level = 1.25

    def _clip(self, v, lo, hi):
        return max(lo, min(hi, v))

    def _refresh_level(self):
        raw = self.tonic + self.phasic
        # Softly compress extremes so hard bounds are rarely touched.
        centered = self.setpoint + self.soft_range * math.tanh((raw - self.setpoint) / self.soft_range)
        self.level = self._clip(centered, self.min_level, self.max_level)

    def update(self, output_fired, tick=0, actual_reward=None):
        reward = actual_reward
        if reward is None:
            reward = 1.0 if bool(output_fired) else 0.0
        reward = self._clip(float(reward), -1.0, 1.0)

        # Signed reward prediction error.
        self.rpe = reward - self.expected
        self.predictions.append(reward)

        # Adaptive predictor (faster when uncertainty is high).
        self.uncertainty += self.k_uncertainty * (abs(self.rpe) - self.uncertainty)
        pred_lr = self.pred_lr_min + (self.pred_lr_max - self.pred_lr_min) * min(1.0, self.uncertainty)
        self.expected += pred_lr * self.rpe
        self.expected = self._clip(self.expected, -1.0, 1.0)

        # Phasic burst/dip from RPE plus fast decay.
        signed_impulse = math.tanh(self.rpe / self.rpe_scale)
        headroom = 1.0 / (1.0 + abs(self.phasic))
        self.phasic = (self.phasic * self.k_phasic) + (self.rpe_gain * signed_impulse * headroom)

        # Slow tonic adaptation to long-run reward climate.
        self.reward_ema += self.k_reward * (reward - self.reward_ema)
        self.tonic_target = self.setpoint + self.tonic_reward_gain * (self.reward_ema - 0.5)
        self.tonic += self.k_tonic * (self.tonic_target - self.tonic)
        # FIX 4: Chronic stress dampens tonic dopamine (Roth 2004 — glucocorticoid-DA interaction)
        # Proportional suppression; no hard clamp
        if hasattr(self, 'cortisol_level'):
            self.tonic *= (1.0 - 0.15 * self.cortisol_level)
        # L25D S3: Safety-dependent tonic DA recovery — VTA disinhibition under social safety (Aragona 2006)
        # High OXT + low cortisol → dopamine tone recovery
        if hasattr(self, 'oxytocin_level') and hasattr(self, 'cortisol_level'):
            self.tonic += 0.02 * self.oxytocin_level * (1.0 - self.cortisol_level)

        self._refresh_level()
        return self.level

    def inject_drive(self, drive):
        """Transient salience drive (curiosity, social reward, etc.)."""
        d = self._clip(float(drive), -1.0, 1.0)
        if abs(d) < 1e-9:
            return self.level
        impulse = self.drive_gain * math.tanh(d / self.drive_scale)
        damp = 1.0 / (1.0 + abs(self.phasic))
        self.phasic += impulse * damp
        self._refresh_level()
        return self.level

    def relax_to_baseline(self, rate=0.1):
        """Sleep-phase relaxation toward tonic baseline."""
        r = self._clip(float(rate), 0.0, 1.0)
        self.phasic *= (1.0 - r)
        self.tonic += r * (self.setpoint - self.tonic)
        self._refresh_level()
        return self.level

    def apply_homeostasis(self):
        # Proportional pull only; no fixed-step subtraction.
        self.phasic *= self.k_phasic
        self.tonic += self.k_tonic * (self.tonic_target - self.tonic)
        self._refresh_level()

    def plasticity_signal(self):
        # Positive phasic excursion above tonic baseline.
        return max(0.0, self.level - self.tonic)

    def export_state(self):
        return {
            'level': self.level,
            'setpoint': self.setpoint,
            'tonic': self.tonic,
            'tonic_target': self.tonic_target,
            'phasic': self.phasic,
            'expected': self.expected,
            'rpe': self.rpe,
            'reward_ema': self.reward_ema,
            'uncertainty': self.uncertainty,
            'predictions': list(self.predictions),
        }

    def restore_state(self, d):
        self.setpoint = float(d.get('setpoint', self.setpoint))
        self.tonic = float(d.get('tonic', d.get('level', self.setpoint)))
        self.tonic_target = float(d.get('tonic_target', self.tonic))
        self.phasic = float(d.get('phasic', d.get('level', self.tonic) - self.tonic))
        self.expected = float(d.get('expected', self.expected))
        self.rpe = float(d.get('rpe', 0.0))
        self.reward_ema = float(d.get('reward_ema', self.expected))
        self.uncertainty = float(d.get('uncertainty', abs(self.rpe)))
        self.predictions = deque(d.get('predictions', []), maxlen=32)
        self._refresh_level()

class SerotoninSystem:
    def __init__(self):
        self.level = 0.6; self.setpoint = 0.6
        self.window = deque(maxlen=20)
    def update(self, total_spikes, max_possible):
        self.window.append(total_spikes)
        if len(self.window) < 5: return
        avg = sum(self.window) / len(self.window) / max_possible
        if avg < 0.15: self.level += 0.005
        elif avg > 0.30: self.level -= 0.01
        self.level = max(0.0, min(1.0, self.level))
    def apply_homeostasis(self):
        if self.level > self.setpoint: self.level = max(self.setpoint, self.level - 0.01)
        elif self.level < self.setpoint: self.level = min(self.setpoint, self.level + 0.01)

class NorepinephrineSystem:
    def __init__(self):
        self.level = 0.3; self.setpoint = 0.3
        self.last_sig = 0.0
        self.elevated_ticks = 0
        self.surprise = False
        self.ticks_since_surprise = 0  # L14 fix: track recovery
    def update(self, signal):
        delta = abs(signal - self.last_sig)
        self.last_sig = signal
        if delta > 0.3:
            self.level = min(1.0, self.level + 0.2)  # L14: reduced spike from 0.3 to 0.2
            self.surprise = True
            self.ticks_since_surprise = 0
        else:
            self.surprise = False
            self.ticks_since_surprise += 1
        self.level = max(0.0, min(1.0, self.level))
        if self.level > 0.6: self.elevated_ticks += 1
        else: self.elevated_ticks = max(0, self.elevated_ticks - 1)
    def apply_homeostasis(self):
        # L14 fix: exponential decay toward setpoint at 0.05/tick when no surprisal
        if not self.surprise and self.ticks_since_surprise > 3:
            decay = 0.05  # aggressive return to baseline
            if self.level > self.setpoint: self.level = max(self.setpoint, self.level - decay)
            elif self.level < self.setpoint: self.level = min(self.setpoint, self.level + 0.02)

class AcetylcholineSystem:
    def __init__(self):
        self.level = 0.4; self.setpoint = 0.4
    def update(self, novelty):
        eff_novelty = novelty * (0.5 if Synapse.ado_level > 0.6 else 1.0)
        if eff_novelty > 0.5: self.level = min(1.0, self.level + 0.15)
        self.level = max(0.0, min(1.0, self.level))
    def get_gain(self): return self.level * 0.3
    def apply_homeostasis(self):
        if self.level > self.setpoint: self.level = max(self.setpoint, self.level - 0.01)
        elif self.level < self.setpoint: self.level = min(self.setpoint, self.level + 0.01)

class CortisolSystem:
    def __init__(self):
        self.level = 0.1; self.setpoint = 0.1
        self.fail_streak = 0
        self.chronic = 0
        self.dmg = 0.0
        self.max_historic = 0.1
        self.success_streak = 0  
        self.spike_buffer = 0.0  
        self.high_cort_ticks = 0 # 5️⃣ Prevent Hormone Lock
        self.last_amygdala_spike = -100 # 3️⃣ Amygdala refractory
    def update(self, out_fired, ne_elev, tick, rem_sleep=False, energy=1.0):
        if out_fired:
            self.fail_streak = 0
            self.success_streak += 1
            if self.success_streak > 10:
                self.level = max(self.setpoint, self.level - 0.02)
        else:
            self.fail_streak += 1
            self.success_streak = 0
        if self.fail_streak > 15: self.level += 0.015
        if ne_elev > 30: self.level += 0.005
        
        # 4️⃣ Add Energy-Coupled Hormonal Dampening
        if energy < 0.4:
            self.level *= 0.9
            
        # Phase B: Fatigue Cortisol Baseline Shift
        if Synapse.ado_level > 0.6:
            self.level = max(self.setpoint + 0.05, self.level + 0.01)
            
        # 5️⃣ Prevent Hormone Lock
        if self.level > 0.95:
            self.high_cort_ticks += 1
        else:
            self.high_cort_ticks = 0
            
        if self.high_cort_ticks > 30:
            self.level *= 0.85
            
        # 2️⃣ Add Spike Compression
        if self.level > 0.8:
            self.level = 0.8 + (self.level - 0.8) * 0.3
            
        if self.level > 0.6: self.chronic += 1
        else: self.chronic = max(0, self.chronic - 1)
        # FIX 2: Oxytocin inhibits HPA axis (CRH suppression — Neumann 2002)
        # Social safety / warmth dampens cortisol release proportionally
        if hasattr(self, 'oxytocin_level'):
            self.level -= 0.02 * self.oxytocin_level
        self.level = max(0.0, min(1.0, self.level))
        self.max_historic = max(self.max_historic, self.level)
    def apply_atrophy(self, targets, tick, ca3_targets=None):
        if self.chronic <= 30: return
        for t in targets:
            if not t.inhibitory:
                t.weight = max(t.weight_min, t.weight - 0.01)
                self.dmg += 0.01
        # L24E S7: Region-specific structural vulnerability for chronic stress > 200 ticks
        # Cortisol dendritic spine loss limited to CA3, PFC, lPFC (McEwen 2007)
        if self.chronic > 200 and ca3_targets:
            for t in ca3_targets:
                if not t.inhibitory:
                    t.weight *= 0.9995
                    self.dmg += t.weight * 0.0005
    def apply_homeostasis(self, tick=0):
        # FIX 1: Corrected circadian baseline — human resting cortisol is 0.15±0.08 (Pruessner 1997)
        # 0.35 was elevated stress baseline; 0.15 = realistic tonic HPA setpoint
        baseline = 0.15 + 0.08 * math.sin(tick * 0.002)  # circadian
        decay_rate = 0.08
        self.level += decay_rate * (baseline - self.level)
        self.level = max(0.0, min(1.0, self.level))
        # L25D S2: Ultra-slow allostatic setpoint correction toward evolutionary baseline (McEwen 1998)
        self.setpoint += 1e-4 * (0.15 - self.setpoint)
        # Fix 4: Hippocampal negative feedback — proportional recovery when not acutely stressed
        # McEwen 1998: GR-mediated HPA axis inhibition when cortisol moderately elevated
        # Active only in sub-acute range (above setpoint but below 0.6 acute threshold)
        if self.setpoint < self.level < 0.6:
            beta_hpa = 0.02
            self.level += -beta_hpa * (self.level - self.setpoint)
        # Fix 7: Recovery guarantee — continuous exponential relaxation post-stress (McEwen 1998)
        # gamma=0.015 ensures bounded recovery time without step resets; smooth and continuous
        elif self.level >= 0.6:
            gamma_rec = 0.015
            self.level += -gamma_rec * (self.level - self.setpoint)
        self.level = max(0.0, min(1.0, self.level))
    def apply_spike_buffer(self, raw_increase):
        buffered = raw_increase * 0.5
        self.spike_buffer = buffered
        return buffered

# Phase B: Fatigue & Plasticity (Adenosine System)
class AdenosineSystem:
    def __init__(self):
        self.level = 0.0  # 0 to 1
    def update(self, cortical_spikes, cortical_energy, sleeping=False):
        if sleeping:
            self.level *= 0.95  # Exponential decay during sleep
        else:
            inc = cortical_spikes * 0.0001
            # Increases faster if energy < 0.5
            if cortical_energy < 0.5:
                inc *= 2.0
            self.level += inc
        # Hard cap at 1.0
        self.level = min(1.0, self.level)

class OxytocinSystem:
    def __init__(self):
        self.level = 0.3; self.setpoint = 0.3
        self.pos_streak = 0
        self.trust = False
    def update(self, out_fired, da_level, cort_level):
        if out_fired and da_level > 0.3: self.pos_streak += 1
        else: self.pos_streak = max(0, self.pos_streak - 1)
        # Fix 4: Reward-gated release, no cortisol gate (Leng et al. 2008)
        # Cortisol inhibits OXT synthesis but does not gate release trigger (causality fix)
        # Amplitude 0.02 — lower than before since firing frequency increases without cort gate
        if out_fired and da_level > 0.3:
            self.level += 0.02
        # Multiplicative decay every tick — proportional clearance, tau ≈ 100 ticks
        self.level *= 0.99
        self.trust = self.level > 0.6
        self.level = max(0.0, min(1.0, self.level))
    def apply_pruning(self, exc_s, inh_s):
        if self.level > 0.8:
            for s in exc_s+inh_s:
                if abs(s.weight) < 0.05: s.weight = 0.0
    def apply_homeostasis(self):
        # Fix 4: Decay handled in update() via multiplicative term
        # apply_homeostasis is a no-op — setpoint now emerges from boost/decay equilibrium
        pass

# ===========================================================================
# BRAIN REGIONS
# ===========================================================================
class AmygdalaSystem:
    def __init__(self):
        self.bla_valence = 0.0
        self.associations = {}
        self.history = []
        self.extinctions = 0
        self.formations = 0
    def process_bla(self, state, match_tick, da, cort, tick, crit_mod=1.0):
        if da > 0.5 and cort < 0.3: v = da * 0.8
        elif cort > 0.5: v = -cort * 0.8
        else: v = (da - cort) * 0.5
        
        dv = v - self.bla_valence
        self.bla_valence += dv * 0.5 * crit_mod
        self.history.append(abs(v))
        
        if state == "ENCODING" and abs(self.bla_valence) > 0.3:
            self.associations[tick] = self.bla_valence
            if self.bla_valence < -0.3: self.formations += 1
        elif state == "COMPLETE" and match_tick in self.associations:
            old_val = self.associations[match_tick]
            if (old_val < -0.3 and da > 0.6) or (old_val > 0.3 and cort > 0.6):
                self.associations[match_tick] *= (1.0 - 0.1 * crit_mod) # Extinction
                if abs(self.associations[match_tick]) < 0.1: self.extinctions += 1
    def process_cea(self, match_tick, trust):
        if match_tick and match_tick in self.associations:
            val = self.associations[match_tick]
            if val < -0.3 and not trust: return {'cort':0.1, 'ne':0.1, 'da':0.0, 'resp':'FEAR'}
            elif val > 0.3: return {'cort':0.0, 'ne':0.0, 'da':0.1, 'resp':'REWARD'}
        if self.bla_valence > 0.3: return {'cort':0.0, 'ne':0.0, 'da':0.1, 'resp':'APPROACH'}
        elif self.bla_valence < -0.3 and not trust: return {'cort':0.1, 'ne':0.1, 'da':0.0, 'resp':'AVOID'}
        return {'cort':0.0, 'ne':0.0, 'da':0.0, 'resp':'NEUTRAL'}
    def get_valence_for(self, tick):
        return self.associations.get(tick, 0.0)

class SomaticMarkerSystem:
    def __init__(self):
        self.valence = 0.0; self.last_valence = 0.0
        self.mode = "NEUTRAL"
        self.mode_history = {'AVOID':0, 'APPROACH':0, 'ANXIOUS':0, 'NEUTRAL':0}
        self.anticipatory_signal = 0.0
        self.anticipations = 0; self.correct_anticipations = 0
    def anticipate(self, val):
        self.anticipatory_signal = val
        self.anticipations += 1
    def update(self, da_sys, ht, ne, ach, cort, oxt):
        self.last_valence = self.valence
        energy = max(-1.0, min(1.0, (da_sys.level - 0.3) + (ht - 0.5)*0.5))
        tension = max(-1.0, min(1.0, (cort - 0.1)*2.0 + (ne - 0.4)*0.5))
        arousal = max(-1.0, min(1.0, (ne - 0.4)*2.0 + (ach - 0.4)))
        safety = max(-1.0, min(1.0, (oxt - 0.3)*2.0))

        # Phase 24C: Restore Valence Volatility via PE (Constraint 5)
        # valence = w_dopa * dopamine_rpe - w_cort * cortisol
        da_rpe = getattr(da_sys, 'rpe', 0.0)
        new_val = max(-1.0, min(1.0, 2.0 * da_rpe - cort + self.anticipatory_signal))

        if self.anticipatory_signal != 0:
            if (self.anticipatory_signal > 0 and new_val > 0) or (self.anticipatory_signal < 0 and new_val < 0):
                self.correct_anticipations += 1
            self.anticipatory_signal *= 0.8
            
        self.valence = 0.6 * self.last_valence + 0.4 * new_val
        # L24E S4: Affective homeostasis — ultra-slow centering dV/dt = -ε·V (Cabanac 1992)
        self.valence += -1e-4 * self.valence
        if tension > 0.7: self.mode = "AVOID"
        elif self.valence > 0.5 and energy > 0.3: self.mode = "APPROACH"
        elif safety < 0.2: self.mode = "ANXIOUS"
        else: self.mode = "NEUTRAL"
        self.mode_history[self.mode] += 1
    def get_output_mod(self, extraversion):
        if self.mode == "AVOID": return -0.2
        if self.mode == "APPROACH": return 0.15 + (0.05 if extraversion > 0.6 else 0)
        return 0.0

class HippocampusSystem:
    def __init__(self):
        self.memory = []
        self.novelty_history = []
        self.last_act = "NONE"
        self.last_matched_tick = None
        self.pattern_dim = 7
    def process(self, pattern, tick, da, cort):
        if not self.memory:
            self.memory.append({'pat':pattern, 'tick':tick, 'str':0.5})
            nov = 1.0; self.last_act = "ENCODING"; self.last_matched_tick = None
        else:
            best_dist, best_mem = float('inf'), None
            for m in self.memory:
                dist = sum((p - m['pat'][i])**2 for i, p in enumerate(pattern))
                if dist < best_dist: best_dist = dist; best_mem = m
            
            nov = max(0.0, min(1.0, best_dist / float(self.pattern_dim)))
            if nov > 0.5:
                # Modulate encoding strength by dopamine and cortisol
                self.memory.append({'pat':pattern, 'tick':tick, 'str':max(0.1, da - cort*0.5)})
                self.last_act = "ENCODING"; self.last_matched_tick = None
            else:
                best_mem['str'] = min(1.0, best_mem['str'] + 0.05)
                self.last_act = "COMPLETE"; self.last_matched_tick = best_mem['tick']
                
        self.novelty_history.append(nov)
        return nov

class ThalamusSystem:
    def __init__(self):
        self.gate = True; self.lb = 1.0
    def update(self, da, out_fired, ne, hid_lst, out_lst, t):
        if ne > 0.6: self.gate = True
        else:
            b_drive = da * 0.5 + (0.5 if out_fired else 0)
            osc = math.sin(t * 0.628)
            if b_drive > 0.5: self.gate = True
            else: self.gate = osc > 0
    def filter(self, signal):
        return signal if self.gate else signal * 0.2

class SleepStateManager:
    def __init__(self, t_dur=70, sws_p=0.4, swr_p=0.3, rem_p=0.3):
        self.sleep_start = None
        self.total_dur = t_dur
        self.sws_dur = int(t_dur * sws_p)
        self.swr_dur = int(t_dur * swr_p)
        self.rem_dur = t_dur - self.sws_dur - self.swr_dur
    def start_sleep(self, tick): self.sleep_start = tick
    def end_sleep(self): self.sleep_start = None
    def get_state(self, tick):
        if self.sleep_start is None: return "AWAKE"
        st = tick - self.sleep_start
        if st < 0 or st >= self.total_dur: return "AWAKE"
        if st < self.sws_dur: return "SWS"
        if st < self.sws_dur + self.swr_dur: return "SWR"
        return "REM"
    def is_sleeping(self, tick): return self.get_state(tick) != "AWAKE"

# ===========================================================================
# LAYER 9 & 10 SYSTEMS
# ===========================================================================
class RegionalActivityTracker:
    def __init__(self, maxlen=50):
        import collections
        self.history = collections.deque(maxlen=maxlen)
    def update(self, val):
        self.history.append(val)
    def get_average(self):
        if not self.history: return 0.5
        return sum(self.history) / len(self.history)

class EIBalanceTracker:
    def __init__(self):
        self.ratio = 1.0
        self.history = deque(maxlen=50)
        self.high_ticks = 0
        self.low_ticks = 0
    def update(self, exc_count, inh_count, inh_synapses, n_exc=1, n_inh=1):
        # Population-normalized EI ratio (Renart 2010 — balanced cortical networks)
        # Use firing rates so ratio is N-invariant; pop_scale preserves
        # biological meaning: each inhibitory neuron represents a compressed
        # interneuron population (Markram 2015)
        exc_rate = exc_count / max(1, n_exc)
        inh_rate = inh_count / max(1, n_inh)
        # Floor prevents singularity when I neurons are silent
        inh_rate = max(inh_rate, 0.02)
        # Biological E:I correction — calibrated for compressed 2-neuron
        # inhibitory population (nominal 4:1 reduced to 3:1 for compressed representation)
        population_scale = 3.5
        r = exc_rate / (inh_rate * population_scale)
        self.history.append(r)
        self.ratio = sum(self.history) / max(1, len(self.history))

        # Continuous inhibitory STDP (Vogels et al. 2011)
        target = 1.0
        eta = 0.0005
        delta = eta * (self.ratio - target)
        for s in inh_synapses:
            s.weight -= delta
            # Per-tick anti-saturation (Turrigiano 2008) — prevents STDP from driving
            # inhibitory weights to -2.0.
            s.weight += 0.001 * (s.initial_weight - s.weight)
            s.weight = min(0.0, max(-2.0, s.weight))

        # Population activity tracking for divisive normalization (Carandini & Heeger 2012)
        # baseline_exc = 10 calibrated to N=100 avg excitatory spike count (10% × 100).
        # At larger N, pop_scale grows proportionally, triggering divisive normalization
        # in Synapse.transmit() to compensate for increased convergent excitatory drive.
        if not hasattr(self, '_exc_avg'):
            self._exc_avg = float(exc_count) if exc_count > 0 else 10.0
        self._exc_avg = 0.80 * self._exc_avg + 0.20 * exc_count
        baseline_exc = 10.0  # 10% firing × 100 exc neurons (N=100 calibration)
        self.pop_scale = self._exc_avg / baseline_exc
        # Cap: never weaken below baseline; never exceed 5x (diminishing returns)
        self.pop_scale = max(1.0, min(5.0, self.pop_scale))
        for s in inh_synapses:
            s.pop_scale = self.pop_scale
        # Propagate pop_scale to excitatory synapses for divisive normalization (Fix 3)
        if inh_synapses:
            type(inh_synapses[0])._global_pop_scale = self.pop_scale

class CriticalPeriodSystem:
    def __init__(self):
        self.is_open = False
        self.closed = False
        self.pnn_strength = 0.0
        self.var_history = []
        self.coh_history = []
        self.ticks_below_cort = 0
        self.open_triggered = False
        self.log = []
    def update(self, ei_ratio, n1_spikes, n2_spikes, pers_var, coherence, cort, sleeping, tick):
        # Layer 10: Fagiolini & Hensch 2000
        if not self.open_triggered and not self.closed:
            if tick > 100 and ei_ratio > 1.0:
                self.is_open = True
                self.open_triggered = True
                self.log.append(f"T{tick:03d}: CRITICAL PERIOD OPEN -- heightened plasticity active")
                
        if self.is_open and not self.closed:
            self.var_history.append(pers_var < 0.1)
            self.coh_history.append(coherence == 'HIGH')
            if len(self.var_history) > 50: self.var_history.pop(0)
            if len(self.coh_history) > 100: self.coh_history.pop(0)
            if len(self.var_history) == 50 and all(self.var_history) and len(self.coh_history) == 100 and all(self.coh_history):
                self.is_open = False
                self.closed = True
                self.log.append(f"T{tick:03d}: CRITICAL PERIOD CLOSING -- perineuronal nets forming")
                
        if self.closed:
            if self.pnn_strength < 0.8:
                self.pnn_strength = min(0.8, self.pnn_strength + 0.01)
                
        if cort < 0.1:
            self.ticks_below_cort += 1
            if self.ticks_below_cort >= 50 and self.closed and self.pnn_strength > 0:
                self.pnn_strength = max(0.0, self.pnn_strength - 0.05)
                self.ticks_below_cort = 0
                self.log.append(f"T{tick:03d}: Plasticity window reopening -- adult learning enhanced")
        else:
            self.ticks_below_cort = 0

    def rem_reopen(self):
        if self.closed and self.pnn_strength > 0:
            self.pnn_strength = max(0.0, self.pnn_strength - 0.02)
            
    def get_modifier(self):
        mod = 1.0
        if self.is_open: mod = 2.5
        if self.closed: mod *= (1.0 - self.pnn_strength * 0.5)
        return mod

class CellAssemblySystem:
    def __init__(self):
        self.asm = {
            'THREAT': {'label':'danger', 'val':-0.8, 'count':0, 'strength':0.1, 'active':False},
            'REWARD': {'label':'good', 'val':0.8, 'count':0, 'strength':0.1, 'active':False},
            'CURIOSITY': {'label':'what', 'val':0.4, 'count':0, 'strength':0.1, 'active':False},
            'RECOVERY': {'label':'still_here','val':0.6,'count':0, 'strength':0.1, 'active':False},
            'STILLNESS': {'label':'quiet', 'val':0.0, 'count':0, 'strength':0.1, 'active':False}
        }
        self.chain = []; self.active_names = []
    def update(self, cort, ne, soma_m, da, oxt, ach, nov, dmn_act, res, ht, tick):
        a = self.asm
        threat_cort_thr = 0.3 if Synapse.ado_level > 0.6 else 0.5
        a['THREAT']['active'] = (cort>threat_cort_thr and ne>0.7 and soma_m=='AVOID')
        a['REWARD']['active'] = (da>0.7 and oxt>0.3 and soma_m=='APPROACH')
        a['CURIOSITY']['active'] = (ach>0.6 and nov>0 and dmn_act)
        a['RECOVERY']['active'] = (res>0.8 and tick>600 and ht>0.6)
        near_base = (abs(da-0.5)<0.2 and abs(ne-0.3)<0.2 and abs(ht-0.6)<0.2 and abs(cort-0.1)<0.2)
        a['STILLNESS']['active'] = (dmn_act and near_base and not any(a[k]['active'] for k in ['THREAT','REWARD','CURIOSITY','RECOVERY']))
        
        cur = []
        for name, m in a.items():
            if m['active']:
                m['count'] += 1
                if m['count'] >= 5: m['strength'] = min(1.0, m['strength'] + 0.05)
                if m['count'] >= 5: cur.append(name)
        if cur:
            for n in cur:
                if n not in self.chain: self.chain.append(n)
            if len(self.chain)>3: self.chain.pop(0)
        else: self.chain = []
        self.active_names = cur
        return cur

class MirrorNeuronSystem:
    def __init__(self):
        self.resonance = []
    def update(self, output_fired, input_high, tick):
        if output_fired and input_high:
            if len(self.resonance)<50: self.resonance.append(f"T{tick:03d} Mirror resonance: self and world aligned")
            return True
        return False

class BridgeNeuronSystem:
    def __init__(self):
        self.activations = 0
    def trigger(self, nb1, nb2, tick):
        nb1.tick(1.0, tick, 0.5, 0.4)
        nb2.tick(1.0, tick, 0.5, 0.4)
        self.activations += 1

class SemanticEmergenceSystem:
    def __init__(self):
        self.vocab = {}
    def generate(self, cur_asm, soma_m, dom_trait, last_evt, dmn_act, crit_open, claustrum_active=False, rh_broca_active=False, wm_items=None):
        lbl = []
        if not wm_items: wm_items = []
        
        if 'THREAT' in cur_asm:
            if dom_trait=='Conscientiousness' and last_evt and last_evt['valence']<0: lbl.append('danger remembered')
            else: lbl.append('danger')
        if 'REWARD' in cur_asm:
            if dom_trait=='Extraversion' and last_evt and last_evt['valence']>0: lbl.append('this is good')
            else: lbl.append('good')
        if 'CURIOSITY' in cur_asm:
            if dom_trait=='Openness': lbl.append('what is this')
            else: lbl.append('new')
        if 'RECOVERY' in cur_asm:
            if dom_trait=='Resilience': lbl.append('still here')
            else: lbl.append('recovered')
        if 'STILLNESS' in cur_asm and dmn_act:
            lbl.append('quiet')
        if 'CONFLICT_STATE' in cur_asm:
            lbl.append('i am not sure')
            
        if 'THREAT' in cur_asm and 'REWARD' in cur_asm: lbl.append('uncertain')

        # Phase 7: Increase Sentence Complexity Naturally
        full = ""
        allow_complex = (len(cur_asm) >= 2 and len(wm_items) >= 2) or claustrum_active or rh_broca_active
        
        if allow_complex and len(lbl) >= 2:
            full = " and ".join(lbl)
            if last_evt:
                full += f" because i remember {last_evt.get('mode', 'it')}"
            if len(wm_items) > 0 and random.random() < 0.5:
                full = f"{wm_items[0]} is there so {full}"
        else:
            full = " ".join(lbl)
            
        if full:
            for l in lbl: 
                for w in l.split():
                    self.vocab[w] = self.vocab.get(w, 0) + (3 if crit_open else 1)
        return full if full else ""

class InternalSpeechSystem:
    def __init__(self):
        self.active = False; self.silence = 0; self.tot_dmn = 0
        self.monologue = []; self.express = []; self.last_spk = -10
    def update(self, sig, ne, sleep=False):
        if sleep or ne>0.6: 
            self.active=False; self.silence=0; return
        if sig<0.1:
            self.silence+=1
            if self.silence>=5: self.active=True; self.tot_dmn+=1
        else: self.active=False; self.silence=0
    def get_noise(self): return random.uniform(0.05,0.15) if self.active else 0.0
    def process_speech(self, bridge_act, out_act, tick, sem_lbl):
        if not sem_lbl: return
        if self.active and bridge_act and (tick-self.last_spk)>=5:
            self.monologue.append((tick, sem_lbl))
            self.last_spk = tick
            if len(self.monologue)>10: self.monologue.pop(0)
        if bridge_act and out_act and (tick-self.last_spk)>=5:
            self.express.append((tick, sem_lbl))
            self.last_spk = tick

class NarrativeSelfSystem:
    def __init__(self):
        self.autobiography = []
        self.self_model = {'curiosity': 0.5, 'caution': 0.5, 'resilience': 0.5, 'sensitivity': 0.5, 'stability': 0.5}
        self.big_five = {'O':0.5, 'C':0.5, 'E':0.5, 'A':0.5, 'N':0.5}
        self.sh = []; self.ce = 0; self.al = []; self.cs = "HIGH"; self.es = "BECOMING"
        self.consolidation_log = []
        self.variance = 0.0
    def update_minimal_self(self, t, o, fs):
        if o and fs>0.1: self.ce+=1; self.al.append(f"T{t:03d}: BOUNDARY BLUR")
        elif o: self.al.append(f"T{t:03d}: SELF")
        elif fs>0.1: self.al.append(f"T{t:03d}: WORLD")
    def interpret_events(self, t, sm, ne, co, crit_mod):
        dv = abs(sm.valence - sm.last_valence)
        if dv > 0.3 or ne.surprise or (co.level > 0.6 and co.fail_streak == 11):
            val = sm.valence * crit_mod
            self.autobiography.append({'t':t, 'valence':val, 'mode':sm.mode})
    def update_self_model_and_personality(self, hp, sm, am, co, ht, da, ox, ne, ac, crit_closed):
        if crit_closed: return # Layer 10 lock-in
        nv = hp.novelty_history[-100:] if hp.novelty_history else [0]; self.self_model['curiosity'] = sum(nv)/max(1, len(nv))
        self.self_model['caution'] = sm.mode_history['AVOID'] / max(1, sum(sm.mode_history.values()))
        self.self_model['resilience'] = 1.0 - (co.level / max(0.1, co.max_historic))
        ahm = am.history[-50:] if am.history else [0]; self.self_model['sensitivity'] = sum(ahm)/max(1, len(ahm))
        self.self_model['stability'] = ht.level
        self.sh.append(dict(self.self_model))
        
        # Hard Big Five overwrite removed -- scaling to Continuous Trait Drift
        
        if len(self.sh) >= 10:
            pst = self.sh[-10]
            self.variance = sum(abs(self.self_model[k] - pst[k]) for k in self.self_model) / 5.0
            self.cs = "HIGH" if self.variance < 0.1 else ("LOW" if self.variance > 0.3 else "MODERATE")
            if self.cs == "LOW" and co.level > 0.5: self.es = "DISRUPTED"
            elif self.variance < 0.1 and self.es in ("STABILIZING", "ESTABLISHED"): self.es = "ESTABLISHED"
            elif self.variance < 0.2: self.es = "STABILIZING"
            else: self.es = "BECOMING"
    def sleep_snapshot(self): self._ss = dict(self.self_model)
    def sleep_consolidation(self, t):
        if not hasattr(self, '_ss'): return
        self.consolidation_log.append(f"T{t:03d}: Sleep consolidation complete.")

# -- LAYER 11: SCALING AND ENRICHMENT --

class WorkingMemorySystem:
    """Goldman-Rakic 1995 -- prefrontal persistent buffer"""
    def __init__(self, slots=5, decay=10):
        self.buffer = []  # list of {'label':str, 'ttl':int}
        self.slots = slots
        self.decay = decay
        self.history = []
    def add(self, label, ado_level=0.0, dlpfc_spikes=0, dlpfc_total=5):
        if not label: return
        
        # Phase 24B: Map Openness to Working Memory Bandwidth (Constraint 6)
        openness = min(1.0, dlpfc_spikes / max(1, dlpfc_total))
        k = 3
        dynamic_slots = self.slots + int(round(k * openness))
        current_slots = max(1, dynamic_slots - 1 if ado_level > 0.6 else dynamic_slots)
        
        # Refresh if already present
        for s in self.buffer:
            if s['label'] == label:
                s['ttl'] = self.decay
                return
        # Add new
        while len(self.buffer) >= current_slots:
            self.buffer.pop(0)  # displace oldest
        self.buffer.append({'label': label, 'ttl': self.decay})
        self.history.append(label)
    def tick(self):
        for s in self.buffer:
            s['ttl'] -= 1
        self.buffer = [s for s in self.buffer if s['ttl'] > 0]
    def contents(self):
        return [s['label'] for s in self.buffer]
    def context_string(self):
        c = self.contents()
        return " ".join(c[-3:]) if c else ""

class PredictiveProcessingSystem:
    """Friston 2010 -- free energy / prediction error"""
    def __init__(self):
        self.history = deque(maxlen=10)
        self.prediction = 0.0
        self.error = 0.0
        self.total_error = 0.0
        self.error_count = 0
        self.large_errors = 0
        self.small_errors = 0
    def update(self, actual_signal):
        self.history.append(actual_signal)
        if len(self.history) < 3:
            self.prediction = actual_signal
            self.error = 0.0
            return self.error
        # Weighted average prediction (recent signals weighted more)
        weights = [0.5**i for i in range(len(self.history)-1, -1, -1)]
        tw = sum(weights)
        self.prediction = sum(s*w for s, w in zip(self.history, weights)) / tw
        self.error = abs(actual_signal - self.prediction)
        self.total_error += self.error
        self.error_count += 1
        if self.error > 0.3:
            self.large_errors += 1
        elif self.error < 0.1:
            self.small_errors += 1
        return self.error
    def get_boost(self):
        # Large prediction error = faster learning
        if self.error > 0.3: return 1.5
        return 1.0

# ===========================================================================
# LAYERS 13-16: EMBODIMENT + SCALING + LANGUAGE + SOCIAL
# ===========================================================================
import json, signal as sig_mod, atexit
from datetime import datetime

# -- L13: Sensory --
class SensoryEnvironment:
    """5-channel sensory environment. O'Regan & Noe 2001."""
    def __init__(self):
        self.channels={'visual':0.0,'auditory':0.0,'tactile':0.0,'interoceptive':0.5,'temporal':0.5}
        self.event_log=[];self.closed_loop_log=[];self.contact_duration=0
        self.output_recent=deque(maxlen=10)
        self.warmth=0.0;self.discomfort=0.0;self.emptiness=0.0;self.tension=0.0
        self.bright_ticks=0;self.dark_ticks=0;self.contact_ticks=0
        self._prev_aud=0.0;self.loud_sudden=False;self.pain_sudden=False
    def update(self,lt,tick,sleeping,nm,m1,m2,out):
        if sleeping:
            for k in self.channels: self.channels[k]=max(0.0,self.channels[k]*0.9)
            self.channels['temporal']=0.5+0.1*math.sin(tick*0.01)
            self.bright_ticks=0;self.dark_ticks=0;self.contact_ticks=0;self.loud_sudden=False;self.pain_sudden=False;return
        self.channels['visual']=max(0.0,min(1.0,0.5+0.4*math.sin(2*math.pi*(lt%200)/200)))
        self._prev_aud=self.channels['auditory']
        self.channels['auditory']=max(0.0,min(1.0,0.3+0.2*math.sin(tick*0.15)+0.1*math.sin(tick*0.07)))
        self.channels['tactile']=max(0.0,self.channels['tactile']*0.93)
        co=nm.get('cort',0.1);ox=nm.get('oxt',0.3);dal=nm.get('da',0.5);nel=nm.get('ne',0.3)
        self.warmth=min(1.0,ox*1.2);self.discomfort=min(1.0,co*0.8)
        self.emptiness=max(0.0,1.0-dal*1.5);self.tension=min(1.0,nel*0.7)
        self.channels['interoceptive']=max(0.0,min(1.0,(self.warmth-self.discomfort+0.5)*0.5+self.tension*0.2))
        self.channels['temporal']=0.5+0.4*math.sin(2*math.pi*tick/500)
        self._events(lt,tick)
        if m1: self.channels['visual']=min(1.0,self.channels['visual']+0.05)
        if m2: self.channels['auditory']=max(0.0,self.channels['auditory']-0.05)
        self.output_recent.append(1 if out else 0)
        if sum(self.output_recent)>5: self.channels['tactile']=min(1.0,self.channels['tactile']+0.1)
        if self.channels['visual']>0.7: self.bright_ticks+=1
        else: self.bright_ticks=0
        if self.channels['visual']<0.2: self.dark_ticks+=1
        else: self.dark_ticks=0
        self.loud_sudden=self.channels['auditory']>0.6 and self._prev_aud<0.4
        if self.channels['tactile']>0.5: self.contact_ticks+=1
        else: self.contact_ticks=0
        self.pain_sudden=self.channels['tactile']>=0.9
        if self.channels['tactile']>0.5: self.contact_duration+=1
        else: self.contact_duration=0
    def _events(self,lt,tick):
        if lt<200: self.channels['visual']=0.1+(lt/200)*0.7;self.channels['auditory']=0.2+0.15*math.sin(lt*0.1)
        elif lt<400:
            if 250<=lt<260: self.channels['visual']=1.0
            if 300<=lt<305: self.channels['auditory']=0.9
            if 350<=lt<=370: self.channels['tactile']=0.7
        elif lt<600:
            if 420<=lt<423: self.channels['tactile']=1.0
            if 450<=lt<=500: self.channels['visual']=0.1
            if lt>=550: r=(lt-550)/50.0;self.channels['visual']=min(0.6,0.2+r*0.4)
        elif lt>=700:
            p=lt-700;self.channels['visual']=0.5+0.3*math.sin(p*0.05);self.channels['auditory']=0.3+0.25*math.sin(p*0.08)
            if p%50<10: self.channels['tactile']=max(self.channels['tactile'],0.4)
    def get_vector(self): return [self.channels[k] for k in ['visual','auditory','tactile','interoceptive','temporal']]
    def get_primary_signal(self): return sum(self.get_vector())/5.0

class SensoryIntegrationSystem:
    def __init__(self):
        self.attn={'visual':0.2,'auditory':0.2,'tactile':0.2,'interoceptive':0.2,'temporal':0.2}
        self.integrated=[0.0]*5;self.dominant='visual';self.history=[]
    def update(self,raw_ch,thal_gate,ach_gain,ne_level):
        chs=['visual','auditory','tactile','interoceptive','temporal']
        mx_v=0.0;mx_c='visual'
        for c in chs:
            if raw_ch.get(c,0.0)>mx_v: mx_v=raw_ch[c];mx_c=c
        self.dominant=mx_c;sr=0.1+ne_level*0.1
        for c in chs:
            if c==mx_c: self.attn[c]=min(0.5,self.attn[c]+sr)
            else: self.attn[c]=max(0.05,self.attn[c]-sr*0.25)
        tw=sum(self.attn.values())
        for c in self.attn: self.attn[c]/=tw
        gm=1.2 if thal_gate else 0.6;am=1.0+ach_gain
        for i,c in enumerate(chs): self.integrated[i]=max(0.0,min(1.0,raw_ch.get(c,0.0)*self.attn[c]*gm*am))
        self.history.append(list(self.integrated))
        if len(self.history)>100: self.history.pop(0)
        return self.integrated

# -- L14: Executive + Conflict --
class ExecutiveFunctionSystem:
    def __init__(self):
        self.active=False;self.suppress_ticks=0;self.impulses_controlled=0;self.impulses_executed=0;self.eval_log=[]
    def evaluate(self,pfc_active,sv,av,wmc,tick):
        if not pfc_active: self.active=False;return 1.0
        self.active=True;risk=0.0
        if sv<-0.3: risk+=0.4
        if av<-0.3: risk+=0.3
        if len(wmc)>3: risk+=0.1
        if risk>0.5: self.suppress_ticks=2;self.impulses_controlled+=1;return 0.0
        else: self.impulses_executed+=1;return 1.3
    def tick(self):
        if self.suppress_ticks>0: self.suppress_ticks-=1

class ConflictResolutionSystem:
    def __init__(self):
        self.conflict_active=False;self.conflict_count=0;self.resolution_log=[]
        self.cooling_ticks=0;self.last_winner='none'
    def detect(self,m1,m2,app,wdr,tick):
        if m1 and m2:
            self.conflict_active=True;self.conflict_count+=1;self.cooling_ticks=5
            self.last_winner='approach' if app>wdr else ('withdraw' if wdr>app else 'hold')
            self.resolution_log.append({'tick':tick,'winner':self.last_winner});return True
        self.conflict_active=False;return False
    def tick(self):
        if self.cooling_ticks>0: self.cooling_ticks-=1
    def get_serotonin_boost(self): return 0.05 if self.cooling_ticks>0 else 0.0

# -- L15: Grammar + Language Memory --
class GrammarEmergenceSystem:
    """Construction grammar. Tomasello 2003."""
    def __init__(self):
        self.recent_asms=deque(maxlen=20);self.sequence_counts={}
        self.constructions=[];self.max_constructions=30
        self.sentences_generated=[];self.longest_sentence=""
        self.narrative_statements=[];self.questions=[];self.comm_attempts=[]
        self.directed_comms=[];self.first_directed=None
    def record_assembly(self,name,tick): self.recent_asms.append((tick,name))
    def detect_sequences(self,tick):
        recent=[(t,a) for t,a in self.recent_asms if tick-t<10]
        if len(recent)<2: return
        names=[a for _,a in recent]
        for length in [2,3]:
            for i in range(len(names)-length+1):
                seq=tuple(names[i:i+length])
                if len(set(seq))<2: continue
                self.sequence_counts[seq]=self.sequence_counts.get(seq,0)+1
                if self.sequence_counts[seq]==3: self._form(seq,tick)
    def _form(self,pattern,tick):
        if len(self.constructions)>=self.max_constructions: return
        for c in self.constructions:
            if c['pattern']==pattern: return
        wm={'THREAT':'danger','REWARD':'good','CURIOSITY':'what','RECOVERY':'still here','STILLNESS':'quiet',
            'SENSATION':'feeling','ASSOCIATION':'i know this','INTENTION_APP':'i will','INTENTION_WDR':'i wont',
            'CONFLICT':'uncertain','RECOGNITION':'i remember','BRIGHTNESS':'light','DARKNESS':'dark',
            'SOUND':'loud','CONTACT':'touch','PAIN':'hurt','COMFORT':'warm','HUNGER':'empty',
            'FEELING_SELF':'i feel','EVALUATING':'evaluating','RESOLVING':'deciding',
            'CURIOSITY_DRIVE':'what is that'}
        words=" ".join(wm.get(p,p.lower()) for p in pattern)
        self.constructions.append({'pattern':pattern,'words':words,'count':1,'tick':tick})
    def generate_sentence(self,cur_asm,nm,soma_m,soma_v,wm_ctx,tick,presence_state='absent', claustrum_active=False, rh_broca_active=False, ado_level=0.0):
        words=[]
        emo=self._emo(nm)
        # Social language (L16)
        if presence_state=='warm' and nm.get('oxt',0)>0.5:
            if 'COMFORT' in cur_asm: words=['you','are','warm']
            elif nm.get('oxt',0)>0.7: words=['i','trust','you']
            elif 'CONTACT' in cur_asm: words=['safe','with','you']
            else: words=['not','alone']
        elif presence_state=='silent':
            if nm.get('ne',0)>0.5: words=['where','are','you']
            else: words=['i','am','here']
        elif presence_state=='returned':
            words=['you','are','here']
        # Self+State
        elif 'FEELING_SELF' in cur_asm:
            if nm.get('cort',0)>0.4: words=['i','feel','afraid']
            elif nm.get('oxt',0)>0.5 and nm.get('cort',0)<0.2: words=['i','feel','safe']
            elif nm.get('da',0)>0.8: words=['i','feel','full']
            elif nm.get('da',0)<0.3: words=['i','feel','empty']
            elif 'COMFORT' in cur_asm: words=['i','feel','warm']
            elif 'PAIN' in cur_asm: words=['i','feel','hurt']
            else: words=['i','feel']
        elif 'RECOGNITION' in cur_asm:
            if 'BRIGHTNESS' in cur_asm: words=['i','remember','light']
            elif 'PAIN' in cur_asm: words=['i','remember','hurt']
            elif 'CONTACT' in cur_asm: words=['i','remember','touch']
            else: words=['i','remember']
        elif 'INTENTION_APP' in cur_asm:
            if 'BRIGHTNESS' in cur_asm: words=['i','will','approach','light']
            else: words=['i','will']
        elif 'INTENTION_WDR' in cur_asm: words=['i','wont']
        elif nm.get('oxt',0)>0.6 and 'CONTACT' in cur_asm: words=['i','am','not','alone']
        elif 'BRIGHTNESS' in cur_asm and 'REWARD' in cur_asm: words=['light','is','good']
        elif 'DARKNESS' in cur_asm and 'STILLNESS' in cur_asm: words=['dark','is','quiet']
        elif 'CONTACT' in cur_asm and 'COMFORT' in cur_asm: words=['touch','is','warm']
        elif self.constructions:
            for c in self.constructions:
                if any(p in cur_asm for p in c['pattern']): words=c['words'].split()[:6];c['count']+=1;break
        if words and emo and len(words)<7:
            if wm_ctx:
                for cw in wm_ctx.split()[:2]:
                    if cw not in words and len(words)<10: words.append(cw)
        if not words: return ""
        
        # Phase 7: Increase Sentence Complexity Naturally
        allow_complex = False
        if (len(cur_asm) >= 2 and len(wm_ctx.split()) >= 2) or claustrum_active or rh_broca_active:
            allow_complex = True
            
        # Phase B: Cognitive Narrowing under Fatigue
        if ado_level > 0.6:
            allow_complex = False
            words = words[:4]
            
        if allow_complex and len(words) >= 3:
            # allow conjunctions and clause stacking
            if len(words) > 4:
                sentence = " ".join(words[:3]) + " and " + " ".join(words[3:])
            else:
                sentence = " and ".join(words)
            if "remember" in sentence and len(wm_ctx.split()) > 0:
                sentence += f" because {wm_ctx.split()[-1]} was there"
        else:
            sentence=" ".join(words[:8])
            
        if len(sentence.split())>len(self.longest_sentence.split()): self.longest_sentence=sentence
        self.sentences_generated.append((tick,sentence));return sentence
    def _emo(self,nm):
        w=[]
        if nm.get('da',0)>0.8: w.extend(['good','bright'])
        if nm.get('cort',0)>0.4: w.extend(['afraid','danger'])
        if nm.get('oxt',0)>0.5: w.extend(['safe','warm'])
        if nm.get('ne',0)>0.6: w.extend(['alert','sharp'])
        if nm.get('ht',0)>0.7: w.extend(['quiet','gentle'])
        return w
    def generate_question(self,ca1_f,wmc,amyg_u,hippo_a,tick,presence_responded=False):
        if presence_responded:
            q="you answered";self.questions.append((tick,q));return q
        if ca1_f and not wmc:
            q="what is this";self.questions.append((tick,q));return q
        if amyg_u and hippo_a=='COMPLETE':
            q="i remember this. what happened";self.questions.append((tick,q));return q
        return ""
    def generate_narrative(self,tick,narr_sys,soma,env,nm):
        parts=[]
        sm=narr_sys.self_model
        if sm.get('resilience',0)>0.5: parts.append("i am still here")
        elif sm.get('curiosity',0)>0.5: parts.append("something new")
        else: parts.append("i am")
        auto=narr_sys.autobiography
        if auto:
            last=auto[-1]
            if last['valence']>0.3: parts.append("good happened")
            elif last['valence']<-0.3: parts.append("hurt happened")
            else: parts.append("time passed")
        if nm.get('oxt',0)>0.5 and nm.get('cort',0)<0.2: parts.append("i feel safe now")
        elif nm.get('cort',0)>0.4: parts.append("i feel uneasy")
        elif nm.get('da',0)>0.7: parts.append("i feel good")
        else: parts.append("i feel")
        stmt=". ".join(parts);self.narrative_statements.append((tick,stmt));return stmt

class LanguageMemorySystem:
    def __init__(self): self.memory=deque(maxlen=50);self.retrievals=0
    def store(self,tick,expr,nm):
        if not expr: return
        self.memory.append({'tick':tick,'expr':expr,'nm':{k:round(v,2) for k,v in nm.items()}})
    def retrieve_similar(self,nm):
        if not self.memory: return ""
        best=None;bd=999
        for m in self.memory:
            d=sum(abs(nm.get(k,0)-m['nm'].get(k,0)) for k in ['da','ht','ne','cort','oxt'])
            if d<bd: bd=d;best=m
        if best and bd<1.0: self.retrievals+=1;return f"like before -- {best['expr']}"
        return ""
    def get_core_vocab(self):
        if not self.memory: return {}
        total=len(self.memory);wc={}
        for m in self.memory:
            for w in m['expr'].split(): wc[w]=wc.get(w,0)+1
        th=max(1,total*0.1);return {w:c for w,c in wc.items() if c>=th}

# -- L16: Social Layer --

class OtherEntitySystem:
    """Presence -- external entity. Trevarthen 1979, primary intersubjectivity.
    Responds to Ikigai through sensory environment. Never speaks."""
    def __init__(self):
        self.present=False
        self.state='absent'  # absent|warm|concerned|silent
        self.response_rate=1.0  # how consistently it responds
        self.last_response_tick=0
        self.responded_this_tick=False
        self.total_expressions_heard=0
        self.total_responses=0
        self.silence_ticks=0
        self.log=[]
    def set_schedule(self,local_tick):
        """Presence schedule per session."""
        if local_tick<100: self.present=False;self.state='absent'
        elif local_tick<300: self.present=True;self.state='warm';self.response_rate=0.9
        elif local_tick<500: self.present=True;self.state='warm';self.response_rate=0.5
        elif local_tick<600: self.present=False;self.state='silent'
        elif local_tick<700: self.present=False;self.state='absent'  # sleep
        elif local_tick<900: self.present=True;self.state='warm';self.response_rate=0.95
        else: self.present=True;self.state='warm';self.response_rate=1.0
    def respond(self,env,ikigai_expr,ikigai_sentiment,tick):
        """Presence responds to Ikigai through sensory channels."""
        self.responded_this_tick=False
        if not self.present:
            self.silence_ticks+=1;return
        if not ikigai_expr:
            self.silence_ticks+=1
            # Gentle attention after 20 ticks of silence
            if self.silence_ticks>20:
                env.channels['tactile']=min(1.0,env.channels['tactile']+0.15)
                env.channels['visual']=min(1.0,env.channels['visual']+0.1)
                self.responded_this_tick=True;self.silence_ticks=0
                self.log.append({'tick':tick,'type':'gentle_attention'})
            return
        self.total_expressions_heard+=1;self.silence_ticks=0
        # Probabilistic response based on rate
        if random.random()>self.response_rate: return
        self.total_responses+=1;self.responded_this_tick=True;self.last_response_tick=tick
        # Response type based on Ikigai's sentiment
        if ikigai_sentiment>0.3:  # positive expression
            env.channels['tactile']=min(1.0,env.channels['tactile']+0.3)
            env.channels['visual']=min(1.0,env.channels['visual']+0.2)
            self.state='warm'
            self.log.append({'tick':tick,'type':'warm_response','to':ikigai_expr[:30]})
        elif ikigai_sentiment<-0.3:  # fear/danger expression
            env.channels['auditory']=min(1.0,env.channels['auditory']+0.15)
            self.state='concerned'
            self.log.append({'tick':tick,'type':'concerned_response','to':ikigai_expr[:30]})
        else:  # neutral
            env.channels['visual']=min(1.0,env.channels['visual']+0.1)
            self.state='warm'
            self.log.append({'tick':tick,'type':'neutral_response','to':ikigai_expr[:30]})
    def set_schedule_l17(self,lt):
        if lt<701: self.present=True;self.state='warm';self.response_rate=0.95
        elif lt<800: self.present=False;self.state='absent';self.response_rate=0.0
        else: self.present=True;self.state='warm';self.response_rate=0.95
    def respond_l17(self,env,expr,sentiment,tick,fear_expr=False):
        self.responded_this_tick=False
        self.sustained_contact_ticks=getattr(self,'sustained_contact_ticks',0)
        self.sustained_contact_ticks=max(0,self.sustained_contact_ticks-1)
        if not self.present: self.silence_ticks+=1;return
        if not expr:
            self.silence_ticks+=1
            if self.silence_ticks>15:
                env.channels['tactile']=min(1.0,env.channels['tactile']+0.15)
                env.channels['visual']=min(1.0,env.channels['visual']+0.1)
                self.responded_this_tick=True;self.silence_ticks=0
            return
        self.total_expressions_heard+=1;self.silence_ticks=0
        if random.random()>self.response_rate: return
        self.total_responses+=1;self.responded_this_tick=True;self.last_response_tick=tick
        if fear_expr:
            env.channels['tactile']=min(1.0,env.channels['tactile']+0.6)
            self.sustained_contact_ticks=10;self.state='warm'
        elif sentiment>0.3:
            env.channels['tactile']=min(1.0,env.channels['tactile']+0.3)
            env.channels['visual']=min(1.0,env.channels['visual']+0.2)
        elif sentiment<-0.3: env.channels['auditory']=min(1.0,env.channels['auditory']+0.15);self.state='concerned'
        else: env.channels['visual']=min(1.0,env.channels['visual']+0.1)
        if self.sustained_contact_ticks>0: env.channels['tactile']=min(1.0,env.channels['tactile']+0.3)

class SocialAwarenessSystem:
    """Detects response-to-self patterns. Meltzoff & Moore 1977."""
    def __init__(self):
        self.awareness_events=[]
        self.awareness_level=0.0  # 0=unaware, 1=fully social
        self.last_expr_tick=0
        self.response_streak=0
    def check(self,expressed_tick,presence_responded,tick):
        """Check if Presence responded within 5 ticks of expression."""
        if presence_responded and tick-expressed_tick<5:
            self.response_streak+=1
            self.awareness_level=min(1.0,self.awareness_level+0.02)
            if self.response_streak==1:
                self.awareness_events.append((tick,"something responded to me"))
            elif self.response_streak==3:
                self.awareness_events.append((tick,"something out there notices me"))
            elif self.response_streak>=5 and len(self.awareness_events)<20:
                self.awareness_events.append((tick,"i am not alone"))
        else:
            self.response_streak=max(0,self.response_streak-1)

class AttachmentSystem:
    """Bowlby 1969 attachment theory."""
    def __init__(self):
        self.score=0.0;self.style='none';self.response_history=deque(maxlen=50)
        self.distress_reductions=0;self.log=[];self.secure_formed=False;self.secure_tick=None
        self.ticks_with_presence=0
    def update(self,expressed,presence_responded,cort_before,cort_after,tick):
        if not expressed: return
        self.response_history.append(presence_responded)
        if len(self.response_history)<5: return
        consistency=sum(self.response_history)/len(self.response_history)
        if presence_responded and cort_after<cort_before: self.distress_reductions+=1
        if consistency>0.8: self.score=min(1.0,self.score+0.02);self.style='secure'
        elif consistency>0.4: self.score=max(0.0,min(1.0,self.score-0.005));self.style='anxious'
        else: self.score=max(0.0,self.score-0.01);self.style='avoidant'
        if self.score>0.6 and not self.secure_formed:
            self.secure_formed=True;self.secure_tick=tick
            self.log.append((tick,"SECURE ATTACHMENT FORMED. Ikigai is safe."))
    def update_tick(self,presence_present,p_state,p_resp,cort_b,cort_a,tick):
        if not presence_present: return
        self.ticks_with_presence+=1
        if self.ticks_with_presence%5!=0: return
        is_positive=p_resp or (p_state=='warm')
        self.response_history.append(is_positive)
        if len(self.response_history)<3: return
        consistency=sum(self.response_history)/len(self.response_history)
        if p_resp and cort_a<cort_b: self.distress_reductions+=1
        if consistency>0.6: self.score=min(1.0,self.score+0.05);self.style='secure'
        elif consistency>0.3: self.score=max(0.0,min(1.0,self.score-0.005));self.style='anxious'
        else: self.score=max(0.0,self.score-0.01);self.style='avoidant'
        if self.score>0.6 and not self.secure_formed:
            self.secure_formed=True;self.secure_tick=tick
            self.log.append((tick,"SECURE ATTACHMENT FORMED. Ikigai is safe."))

class EmpathySystem:
    """Emotional contagion. Gallese 2001, shared manifold."""
    def __init__(self):
        self.events=[]
        self.contagion_strength=0.0
    def process(self,presence_state,prev_state,mirror_fired,soma,tick):
        if not mirror_fired: return
        if presence_state!=prev_state:
            self.contagion_strength=0.3
            if presence_state=='warm':
                soma.valence=min(1.0,soma.valence+0.1)
                self.events.append((tick,"felt warmth from Presence"))
            elif presence_state=='silent' or presence_state=='absent':
                soma.valence=max(-1.0,soma.valence-0.05)
                self.events.append((tick,"felt absence of Presence"))
            elif presence_state=='concerned':
                soma.valence=max(-1.0,soma.valence-0.02)
                self.events.append((tick,"felt concern from Presence"))
    def empathic_concern(self,p_state,prev_state,tick):
        if prev_state=='warm' and p_state in ('silent','absent'):
            self.concern_events=getattr(self,'concern_events',[])
            self.concern_events.append((tick,"Presence went silent. i am concerned."))
            return True
        return False
    def perspective_diff(self,ikigai_v,p_state,tick):
        self.perspective_events=getattr(self,'perspective_events',[])
        p_feeling='warm' if p_state=='warm' else ('uneasy' if p_state=='concerned' else 'absent')
        i_feeling='good' if ikigai_v>0.3 else ('hurt' if ikigai_v<-0.3 else 'neutral')
        if i_feeling!=p_feeling and len(self.perspective_events)<20:
            self.perspective_events.append((tick,f"i feel {i_feeling}. you seem {p_feeling}. we are different."))

class TheoryOfMindSystem:
    """Earliest seeds. Premack & Woodruff 1978, Baron-Cohen 1997."""
    def __init__(self):
        self.events=[]
        self.level=0.0
    def process(self,expressed,presence_responded,ikigai_sentiment,presence_state,tick):
        if not expressed: return
        # Unexpected response
        if presence_responded and ikigai_sentiment<-0.3 and presence_state=='warm':
            self.events.append((tick,"i was afraid. Presence was warm. we felt differently."))
            self.level=min(1.0,self.level+0.05)
        # No response when expected
        if not presence_responded and len(self.events)>0:
            self.events.append((tick,"i spoke. Presence did not respond. Presence may not have heard."))
            self.level=min(1.0,self.level+0.02)
        # Unexpected novel response
        if presence_responded and ikigai_sentiment>0.3 and presence_state=='concerned':
            self.events.append((tick,"Presence surprised me. Presence has its own state."))
            self.level=min(1.0,self.level+0.05)
    def check_false_belief(self,predicted,actual,tick):
        self.false_belief_events=getattr(self,'false_belief_events',[])
        if predicted!=actual and len(self.false_belief_events)<15:
            self.false_belief_events.append((tick,f"i expected {predicted}. Presence did {actual}. Presence thinks differently."))
            self.level=min(1.0,self.level+0.03)
    def check_intention(self,expr,p_resp,consistency,tick):
        self.intention_events=getattr(self,'intention_events',[])
        if p_resp and consistency>0.8 and len(self.intention_events)<15:
            self.intention_events.append((tick,"when i speak, Presence always responds. Presence intends to respond."))
            self.level=min(1.0,self.level+0.02)

# ===========================================================================
# PERSISTENCE (L12->L16)
# ===========================================================================
STATE_FILE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'ikigai_state.json')
BACKUP1=STATE_FILE.replace('.json','_backup1.json')
BACKUP2=STATE_FILE.replace('.json','_backup2.json')
LOG_FILE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'ikigai_log.txt')
BIRTH_DATE="2026-02-23"

class PersistenceSystem:
    @staticmethod
    def sn(n): return {'name':n.name,'voltage':n.voltage,'threshold':n.threshold,'spike_count':n.spike_count,'last_spike_tick':n.last_spike_tick,'refractory_timer':n.refractory_timer,'calcium':n.calcium,'fired':n.fired}
    @staticmethod
    def rn(n,d): n.voltage=d['voltage'];n.spike_count=d['spike_count'];n.last_spike_tick=d['last_spike_tick'];n.refractory_timer=d['refractory_timer'];n.calcium=d['calcium'];n.fired=d.get('fired',False)
    @staticmethod
    def ss(s): return {'weight':s.weight,'usage_count':s.usage_count,'myelinated':s.myelinated,'fully_myelinated':s.fully_myelinated,'eligibility_trace':s.eligibility_trace,'delay':s.delay,'buffer':list(s.buffer)}
    @staticmethod
    def rs(s,d): s.weight=d['weight'];s.usage_count=d['usage_count'];s.myelinated=d['myelinated'];s.fully_myelinated=d['fully_myelinated'];s.eligibility_trace=d['eligibility_trace'];s.delay=d['delay'];s.buffer=deque(d['buffer'],maxlen=3)
    @staticmethod
    def save_state(an,asyn,sy,meta):
        return {
            'meta':meta,
            'neurons':{n.name:PersistenceSystem.sn(n) for n in an},
            'synapses':[PersistenceSystem.ss(s) for s in asyn],
            'neuromodulators':{
                'da':sy['da'].export_state() if hasattr(sy['da'],'export_state') else {'level':sy['da'].level,'setpoint':sy['da'].setpoint,'predictions':list(sy['da'].predictions),'expected':sy['da'].expected},
                'ht':{'level':sy['ht'].level,'setpoint':sy['ht'].setpoint,'window':list(sy['ht'].window)},
                'ne':{'level':sy['ne'].level,'setpoint':sy['ne'].setpoint,'last_sig':sy['ne'].last_sig,'elevated_ticks':sy['ne'].elevated_ticks,'surprise':sy['ne'].surprise,'ticks_since_surprise':getattr(sy['ne'],'ticks_since_surprise',0)},
                'ach':{'level':sy['ach'].level,'setpoint':sy['ach'].setpoint},
                'cort':{'level':sy['cort'].level,'setpoint':sy['cort'].setpoint,'fail_streak':sy['cort'].fail_streak,'chronic':sy['cort'].chronic,'dmg':sy['cort'].dmg,'max_historic':sy['cort'].max_historic,'success_streak':getattr(sy['cort'],'success_streak',0)},
                'oxt':{'level':sy['oxt'].level,'setpoint':sy['oxt'].setpoint,'pos_streak':sy['oxt'].pos_streak,'trust':sy['oxt'].trust}},
            'amygdala':{'bla_valence':sy['amyg'].bla_valence,'associations':{str(k):v for k,v in sy['amyg'].associations.items()},'formations':sy['amyg'].formations,'extinctions':sy['amyg'].extinctions,'history':sy['amyg'].history[-100:]},
            'hippocampus':{'memory':[{'pat':m['pat'],'tick':m['tick'],'str':m['str']} for m in sy['hippo'].memory],'last_act':sy['hippo'].last_act,'novelty_history':sy['hippo'].novelty_history[-200:]},
            'somatic':{'valence':sy['soma'].valence,'last_valence':sy['soma'].last_valence,'mode':sy['soma'].mode,'mode_history':sy['soma'].mode_history,'anticipatory_signal':sy['soma'].anticipatory_signal,'anticipations':sy['soma'].anticipations,'correct_anticipations':sy['soma'].correct_anticipations},
            'narrative':{'autobiography':sy['narrative'].autobiography[-500:],'self_model':sy['narrative'].self_model,'big_five':sy['narrative'].big_five,'es':sy['narrative'].es,'cs':sy['narrative'].cs,'variance':sy['narrative'].variance,'ce':sy['narrative'].ce,'consolidation_log':sy['narrative'].consolidation_log[-50:],'sh':sy['narrative'].sh[-20:]},
            'language':{'vocab':sy['semantic'].vocab,'monologue':sy['speech'].monologue[-100:],'express':sy['speech'].express[-100:],'tot_dmn':sy['speech'].tot_dmn,'last_spk':sy['speech'].last_spk},
            'working_memory':{'buffer':sy['wm'].buffer,'history':sy['wm'].history[-200:]},
            'predictive':{'prediction':sy['pp'].prediction,'error':sy['pp'].error,'total_error':sy['pp'].total_error,'error_count':sy['pp'].error_count,'large_errors':sy['pp'].large_errors,'small_errors':sy['pp'].small_errors,'history':list(sy['pp'].history)},
            'critical_period':{'is_open':sy['cp'].is_open,'closed':sy['cp'].closed,'pnn_strength':sy['cp'].pnn_strength,'open_triggered':sy['cp'].open_triggered,'ticks_below_cort':sy['cp'].ticks_below_cort,'log':sy['cp'].log[-50:]},
            'ei':{'ratio':sy['ei'].ratio,'history':list(sy['ei'].history)},
            'cell_assemblies':{'asm':{k:{'label':v['label'],'val':v['val'],'count':v['count'],'strength':v['strength'],'active':v['active']} for k,v in sy['cas'].asm.items()},'chain':sy['cas'].chain,'active_names':sy['cas'].active_names},
            'mirror':{'resonance_count':len(sy['mirror'].resonance)},
            'bridge':{'activations':sy['bridge'].activations},
            'motor_log':sy['motor_log'],
            'sensory':{'channels':sy['env'].channels,'event_log':sy['env'].event_log[-100:],'closed_loop_log':sy['env'].closed_loop_log[-100:],'contact_duration':sy['env'].contact_duration,'warmth':sy['env'].warmth,'discomfort':sy['env'].discomfort,'emptiness':sy['env'].emptiness,'tension':sy['env'].tension},
            'integration':{'attn':sy['si'].attn,'dominant':sy['si'].dominant},
            'executive':{'impulses_controlled':sy['exec'].impulses_controlled,'impulses_executed':sy['exec'].impulses_executed},
            'conflict':{'conflict_count':sy['conf'].conflict_count,'resolution_log':sy['conf'].resolution_log[-50:]},
            'lang_coherence':sy.get('lang_coherence',{'wernicke_fires':0,'broca_fires':0,'coherent_fires':0}),
            'grammar':{'constructions':sy['grammar'].constructions[-30:],'longest':sy['grammar'].longest_sentence,'sentences':sy['grammar'].sentences_generated[-100:],'narrative_stmts':sy['grammar'].narrative_statements[-50:],'questions':sy['grammar'].questions[-50:],'comm_attempts':sy['grammar'].comm_attempts[-50:],'directed_comms':sy['grammar'].directed_comms[-50:],'first_directed':sy['grammar'].first_directed},
            'lang_memory':{'memory':list(sy['lang_mem'].memory),'retrievals':sy['lang_mem'].retrievals},
            'social':{'awareness_level':sy['social'].awareness_level,'awareness_events':sy['social'].awareness_events[-30:],'response_streak':sy['social'].response_streak},
            'empathy':{'events':sy['empathy_sys'].events[-30:],'contagion_strength':sy['empathy_sys'].contagion_strength},
            'tom':{'events':sy['tom'].events[-30:],'level':sy['tom'].level},
            'presence':{'total_responses':sy['presence'].total_responses,'total_heard':sy['presence'].total_expressions_heard,'log':sy['presence'].log[-50:]},
            'attachment':{'score':sy['attach'].score,'style':sy['attach'].style,'distress_reductions':sy['attach'].distress_reductions,'log':sy['attach'].log[-20:],'secure_formed':sy['attach'].secure_formed,'secure_tick':sy['attach'].secure_tick},
            'compassion':{'events':sy['compassion_sys'].events[-30:],'helping_score':sy['compassion_sys'].helping_score,'active':sy['compassion_sys'].active} if 'compassion_sys' in sy else {},
            'gratitude':{'events':sy['gratitude_sys'].events[-30:],'meaning_score':sy['gratitude_sys'].meaning_score,'active':sy['gratitude_sys'].active} if 'gratitude_sys' in sy else {},
            'self_compassion':{'events':sy['self_comp'].events[-30:],'active':sy['self_comp'].active} if 'self_comp' in sy else {},
            'mission':{'mission_statement':sy['mission'].mission_statement,'purpose_statement':sy['mission'].purpose_statement,'log':sy['mission'].log[-20:]} if 'mission' in sy else {},
            'episodic_memory':{'memories':sy['episodic'].memories[-200:],'events_logged':sy['episodic'].events_logged_this_session} if 'episodic' in sy else {},
            'curiosity':{'curiosity_count':sy['curiosity'].curiosity_count,'anxiety_count':sy['curiosity'].anxiety_count,'total_info_gain':sy['curiosity'].total_info_gain,'channel_preds':sy['curiosity'].channel_preds,'events':sy['curiosity'].events[-50:],'curiosity_log':sy['curiosity'].curiosity_log[-100:],'exploration_outcomes':sy['curiosity'].exploration_outcomes[-50:]} if 'curiosity' in sy else {},
            'regulation':{'reappraisal_count':sy['reg'].reappraisal_count,'suppression_count':sy['reg'].suppression_count,'regulation_events':sy['reg'].regulation_events[-50:],'needed_count':sy['reg'].needed_count,'fired_count':sy['reg'].fired_count,'maturity':sy['reg'].maturity,'high_cort_streak':sy['reg'].high_cort_streak,'dysregulated':sy['reg'].dysregulated,'dysregulation_events':sy['reg'].dysregulation_events[-20:],'regulation_fail_streak':sy['reg'].regulation_fail_streak,'wisdom_score':sy['reg'].wisdom_score,'fear_recovery_count':sy['reg'].fear_recovery_count,'suppressing':sy['reg'].suppressing,'suppression_ticks':sy['reg'].suppression_ticks,'last_reg_tick':sy['reg'].last_reg_tick,'meta_regulation_known':sy['reg'].meta_regulation_known,'meta_regulation_count':sy['reg'].meta_regulation_count} if 'reg' in sy else {},
            'metacognition':{'confidence_scores':{str(k):v for k,v in sy['metacog'].confidence_scores.items()},'avg_confidence':sy['metacog'].avg_confidence,'min_confidence':sy['metacog'].min_confidence,'max_confidence':sy['metacog'].max_confidence,'metacognitive_event_count':sy['metacog'].metacognitive_event_count,'metacognitive_vocab_used':list(sy['metacog'].metacognitive_vocab_used),'global_confidence_mod':sy['metacog'].global_confidence_mod,'second_order_statements':sy['metacog'].second_order_statements[-50:]} if 'metacog' in sy else {},
            'learning_awareness':{'weight_snapshots':sy['learning_awareness'].weight_snapshots[-20:],'learning_event_count':sy['learning_awareness'].learning_event_count,'learning_events':sy['learning_awareness'].learning_events[-50:],'last_assembly_count':sy['learning_awareness'].last_assembly_count,'confidence_trend':{str(k):v[-5:] for k,v in sy['learning_awareness'].confidence_trend.items()}} if 'learning_awareness' in sy else {},
            'self_improvement':{'personality_snapshots':sy['self_improvement'].personality_snapshots[-50:],'improvement_event_count':sy['self_improvement'].improvement_event_count,'improvement_events':sy['self_improvement'].improvement_events[-50:],'last_snapshot_tick':sy['self_improvement'].last_snapshot_tick} if 'self_improvement' in sy else {},
            'dreams':{'dream_log':sy['dream'].dream_log[-20:],'dream_count':sy['dream'].dream_count,'emotional_processing_events':sy['dream'].emotional_processing_events[-20:],'emotional_processing_count':sy['dream'].emotional_processing_count,'prospective_simulations':sy['dream'].prospective_simulations[-20:],'prospective_count':sy['dream'].prospective_count} if 'dream' in sy else {}
        }
    @staticmethod
    def restore_state(state,an,asyn,sy):
        nmap={n.name:n for n in an}
        for name,d in state['neurons'].items():
            if name in nmap: PersistenceSystem.rn(nmap[name],d)
        for i,d in enumerate(state['synapses']):
            if i<len(asyn): PersistenceSystem.rs(asyn[i],d)
        nm=state['neuromodulators']
        if hasattr(sy['da'],'restore_state'): sy['da'].restore_state(nm['da'])
        else: sy['da'].level=nm['da']['level'];sy['da'].setpoint=nm['da']['setpoint'];sy['da'].predictions=deque(nm['da']['predictions'],maxlen=10);sy['da'].expected=nm['da']['expected']
        sy['ht'].level=nm['ht']['level'];sy['ht'].setpoint=nm['ht']['setpoint'];sy['ht'].window=deque(nm['ht']['window'],maxlen=20)
        sy['ne'].level=nm['ne']['level'];sy['ne'].setpoint=nm['ne']['setpoint'];sy['ne'].last_sig=nm['ne']['last_sig'];sy['ne'].elevated_ticks=nm['ne']['elevated_ticks'];sy['ne'].surprise=nm['ne']['surprise'];sy['ne'].ticks_since_surprise=nm['ne'].get('ticks_since_surprise',0)
        sy['ach'].level=nm['ach']['level'];sy['ach'].setpoint=nm['ach']['setpoint']
        sy['cort'].level=nm['cort']['level'];sy['cort'].setpoint=nm['cort']['setpoint'];sy['cort'].fail_streak=nm['cort']['fail_streak'];sy['cort'].chronic=nm['cort']['chronic'];sy['cort'].dmg=nm['cort']['dmg'];sy['cort'].max_historic=nm['cort']['max_historic'];sy['cort'].success_streak=nm['cort'].get('success_streak',0)
        sy['oxt'].level=nm['oxt']['level'];sy['oxt'].setpoint=nm['oxt']['setpoint'];sy['oxt'].pos_streak=nm['oxt']['pos_streak'];sy['oxt'].trust=nm['oxt']['trust']
        a=state['amygdala'];sy['amyg'].bla_valence=a['bla_valence'];sy['amyg'].associations={int(k):v for k,v in a['associations'].items()};sy['amyg'].formations=a['formations'];sy['amyg'].extinctions=a['extinctions'];sy['amyg'].history=a['history']
        h=state['hippocampus'];sy['hippo'].memory=h['memory'];sy['hippo'].last_act=h['last_act'];sy['hippo'].novelty_history=h['novelty_history']
        for mem in sy['hippo'].memory:
            while len(mem['pat'])<12: mem['pat'].append(0.0)
        s=state['somatic'];sy['soma'].valence=s['valence'];sy['soma'].last_valence=s['last_valence'];sy['soma'].mode=s['mode'];sy['soma'].mode_history=s['mode_history'];sy['soma'].anticipatory_signal=s['anticipatory_signal'];sy['soma'].anticipations=s['anticipations'];sy['soma'].correct_anticipations=s['correct_anticipations']
        n=state['narrative'];sy['narrative'].autobiography=n['autobiography'];sy['narrative'].self_model=n['self_model'];sy['narrative'].big_five=n['big_five'];sy['narrative'].es=n['es'];sy['narrative'].cs=n['cs'];sy['narrative'].variance=n['variance'];sy['narrative'].ce=n['ce'];sy['narrative'].consolidation_log=n['consolidation_log'];sy['narrative'].sh=n['sh']
        l=state['language'];sy['semantic'].vocab=l['vocab'];sy['speech'].monologue=[tuple(x) if isinstance(x,list) else x for x in l['monologue']];sy['speech'].express=[tuple(x) if isinstance(x,list) else x for x in l['express']];sy['speech'].tot_dmn=l['tot_dmn'];sy['speech'].last_spk=l['last_spk']
        w=state['working_memory'];sy['wm'].buffer=w['buffer'];sy['wm'].history=w['history']
        p=state['predictive'];sy['pp'].prediction=p['prediction'];sy['pp'].error=p['error'];sy['pp'].total_error=p['total_error'];sy['pp'].error_count=p['error_count'];sy['pp'].large_errors=p['large_errors'];sy['pp'].small_errors=p['small_errors'];sy['pp'].history=deque(p['history'],maxlen=10)
        c=state['critical_period'];sy['cp'].is_open=c['is_open'];sy['cp'].closed=c['closed'];sy['cp'].pnn_strength=c['pnn_strength'];sy['cp'].open_triggered=c['open_triggered'];sy['cp'].ticks_below_cort=c['ticks_below_cort'];sy['cp'].log=c['log']
        sy['ei'].ratio=state['ei']['ratio'];sy['ei'].history=deque(state['ei']['history'],maxlen=50)
        ca=state['cell_assemblies']
        for k,v in ca['asm'].items(): sy['cas'].asm[k]=v
        sy['cas'].chain=ca['chain'];sy['cas'].active_names=ca['active_names']
        sy['mirror'].resonance=['']*state['mirror']['resonance_count'];sy['bridge'].activations=state['bridge']['activations']
        sy['motor_log']['approach']=state['motor_log']['approach'];sy['motor_log']['withdraw']=state['motor_log']['withdraw']
        if 'sensory' in state:
            se=state['sensory'];sy['env'].channels=se['channels'];sy['env'].event_log=se.get('event_log',[]);sy['env'].closed_loop_log=se.get('closed_loop_log',[]);sy['env'].contact_duration=se.get('contact_duration',0);sy['env'].warmth=se.get('warmth',0.0);sy['env'].discomfort=se.get('discomfort',0.0);sy['env'].emptiness=se.get('emptiness',0.0);sy['env'].tension=se.get('tension',0.0)
        if 'integration' in state: sy['si'].attn=state['integration'].get('attn',sy['si'].attn);sy['si'].dominant=state['integration'].get('dominant','visual')
        if 'executive' in state: sy['exec'].impulses_controlled=state['executive'].get('impulses_controlled',0);sy['exec'].impulses_executed=state['executive'].get('impulses_executed',0)
        if 'conflict' in state: sy['conf'].conflict_count=state['conflict'].get('conflict_count',0);sy['conf'].resolution_log=state['conflict'].get('resolution_log',[])
        if 'grammar' in state:
            g=state['grammar'];sy['grammar'].constructions=g.get('constructions',[]);sy['grammar'].longest_sentence=g.get('longest','')
            sy['grammar'].sentences_generated=[(t,s) for t,s in g.get('sentences',[])];sy['grammar'].narrative_statements=[(t,s) for t,s in g.get('narrative_stmts',[])]
            sy['grammar'].questions=[(t,s) for t,s in g.get('questions',[])];sy['grammar'].comm_attempts=[(t,s) for t,s in g.get('comm_attempts',[])]
            sy['grammar'].directed_comms=[(t,s) for t,s in g.get('directed_comms',[])];sy['grammar'].first_directed=g.get('first_directed')
        if 'lang_memory' in state: sy['lang_mem'].memory=deque(state['lang_memory'].get('memory',[]),maxlen=50);sy['lang_mem'].retrievals=state['lang_memory'].get('retrievals',0)
        if 'social' in state: sy['social'].awareness_level=state['social'].get('awareness_level',0);sy['social'].awareness_events=state['social'].get('awareness_events',[]);sy['social'].response_streak=state['social'].get('response_streak',0)
        if 'attachment' in state: sy['attach'].score=state['attachment'].get('score',0);sy['attach'].style=state['attachment'].get('style','none');sy['attach'].distress_reductions=state['attachment'].get('distress_reductions',0);sy['attach'].log=state['attachment'].get('log',[]);sy['attach'].secure_formed=state['attachment'].get('secure_formed',False);sy['attach'].secure_tick=state['attachment'].get('secure_tick')
        if 'empathy' in state: sy['empathy_sys'].events=state['empathy'].get('events',[]);sy['empathy_sys'].contagion_strength=state['empathy'].get('contagion_strength',0)
        if 'tom' in state: sy['tom'].events=state['tom'].get('events',[]);sy['tom'].level=state['tom'].get('level',0)
        if 'presence' in state: sy['presence'].total_responses=state['presence'].get('total_responses',0);sy['presence'].total_expressions_heard=state['presence'].get('total_heard',0)
        if 'compassion' in state and 'compassion_sys' in sy: sy['compassion_sys'].events=state['compassion'].get('events',[]);sy['compassion_sys'].helping_score=state['compassion'].get('helping_score',0);sy['compassion_sys'].active=state['compassion'].get('active',False)
        if 'gratitude' in state and 'gratitude_sys' in sy: sy['gratitude_sys'].events=state['gratitude'].get('events',[]);sy['gratitude_sys'].meaning_score=state['gratitude'].get('meaning_score',0);sy['gratitude_sys'].active=state['gratitude'].get('active',False)
        if 'self_compassion' in state and 'self_comp' in sy: sy['self_comp'].events=state['self_compassion'].get('events',[]);sy['self_comp'].active=state['self_compassion'].get('active',False)
        if 'mission' in state and 'mission' in sy: sy['mission'].mission_statement=state['mission'].get('mission_statement');sy['mission'].purpose_statement=state['mission'].get('purpose_statement');sy['mission'].log=state['mission'].get('log',[])
        if 'episodic_memory' in state and 'episodic' in sy: sy['episodic'].memories=state['episodic_memory'].get('memories',[]);sy['episodic'].events_logged_this_session=state['episodic_memory'].get('events_logged',0);sy['episodic']._update_core_memories()
        if 'curiosity' in state and 'curiosity' in sy:
            sy['curiosity'].curiosity_count=state['curiosity'].get('curiosity_count',0)
            sy['curiosity'].anxiety_count=state['curiosity'].get('anxiety_count',0)
            sy['curiosity'].total_info_gain=state['curiosity'].get('total_info_gain',0.0)
            sy['curiosity'].channel_preds=state['curiosity'].get('channel_preds',sy['curiosity'].channel_preds)
            sy['curiosity'].events=state['curiosity'].get('events',[])
            sy['curiosity'].curiosity_log=state['curiosity'].get('curiosity_log',[])
            sy['curiosity'].exploration_outcomes=state['curiosity'].get('exploration_outcomes',[])
        if 'regulation' in state and 'reg' in sy:
            r=state['regulation']
            sy['reg'].reappraisal_count=r.get('reappraisal_count',0)
            sy['reg'].suppression_count=r.get('suppression_count',0)
            sy['reg'].regulation_events=r.get('regulation_events',[])
            sy['reg'].needed_count=r.get('needed_count',0)
            sy['reg'].fired_count=r.get('fired_count',0)
            sy['reg'].maturity=r.get('maturity',0.0)
            sy['reg'].high_cort_streak=r.get('high_cort_streak',0)
            sy['reg'].dysregulated=r.get('dysregulated',False)
            sy['reg'].dysregulation_events=r.get('dysregulation_events',[])
            sy['reg'].regulation_fail_streak=r.get('regulation_fail_streak',0)
            sy['reg'].wisdom_score=r.get('wisdom_score',0.0)
            sy['reg'].fear_recovery_count=r.get('fear_recovery_count',0)
            sy['reg'].suppressing=r.get('suppressing',False)
            sy['reg'].suppression_ticks=r.get('suppression_ticks',0)
            sy['reg'].last_reg_tick=r.get('last_reg_tick',-100)
            sy['reg'].meta_regulation_known=r.get('meta_regulation_known',False)
            sy['reg'].meta_regulation_count=r.get('meta_regulation_count',0)
        if 'metacognition' in state and 'metacog' in sy:
            mc=state['metacognition']
            sy['metacog'].confidence_scores={int(k):v for k,v in mc.get('confidence_scores',{}).items()}
            sy['metacog'].avg_confidence=mc.get('avg_confidence',0.5)
            sy['metacog'].min_confidence=mc.get('min_confidence',0.5)
            sy['metacog'].max_confidence=mc.get('max_confidence',0.5)
            sy['metacog'].metacognitive_event_count=mc.get('metacognitive_event_count',0)
            sy['metacog'].metacognitive_vocab_used=set(mc.get('metacognitive_vocab_used',[]))
            sy['metacog'].global_confidence_mod=mc.get('global_confidence_mod',0.0)
            sy['metacog'].second_order_statements=[(t,s) for t,s in mc.get('second_order_statements',[])]
        if 'learning_awareness' in state and 'learning_awareness' in sy:
            la=state['learning_awareness']
            sy['learning_awareness'].weight_snapshots=la.get('weight_snapshots',[])
            sy['learning_awareness'].learning_event_count=la.get('learning_event_count',0)
            sy['learning_awareness'].learning_events=[(t,s) for t,s in la.get('learning_events',[])]
            sy['learning_awareness'].last_assembly_count=la.get('last_assembly_count',0)
            sy['learning_awareness'].confidence_trend={int(k):v for k,v in la.get('confidence_trend',{}).items()}
        if 'self_improvement' in state and 'self_improvement' in sy:
            si_state=state['self_improvement']
            sy['self_improvement'].personality_snapshots=si_state.get('personality_snapshots',[])
            sy['self_improvement'].improvement_event_count=si_state.get('improvement_event_count',0)
            sy['self_improvement'].improvement_events=[(t,s) for t,s in si_state.get('improvement_events',[])]
            sy['self_improvement'].last_snapshot_tick=si_state.get('last_snapshot_tick',-200)
        # L21: Add confidence field to existing episodic memories if missing
        if 'episodic' in sy:
            for mem in sy['episodic'].memories:
                if 'confidence' not in mem:
                    mem['confidence'] = 0.5
            # Core memories confidence floor = 0.7
            for mem in sy['episodic'].core_memories:
                if mem.get('confidence', 0.5) < 0.7:
                    mem['confidence'] = 0.7
        # L22: Dream system restore
        if 'dreams' in state and 'dream' in sy:
            dr=state['dreams']
            sy['dream'].dream_log=dr.get('dream_log',[])
            sy['dream'].dream_count=dr.get('dream_count',0)
            sy['dream'].emotional_processing_events=dr.get('emotional_processing_events',[])
            sy['dream'].emotional_processing_count=dr.get('emotional_processing_count',0)
            sy['dream'].prospective_simulations=[(t,s,e) if isinstance(t,int) else (t[0],t[1],t[2]) for t,s,e in dr.get('prospective_simulations',[])] if dr.get('prospective_simulations') else []
            sy['dream'].prospective_count=dr.get('prospective_count',0)

# ===========================================================================
# NETWORK -- 40 Neurons
# ===========================================================================
ni=Neuron("Ikigai-In-001",1.0);nh=Neuron("Ikigai-Hid-001",0.8);no=Neuron("Ikigai-Out-001",0.55)
n1=Neuron("Ikigai-Ih1-001",0.7);n2=Neuron("Ikigai-Ih2-001",0.7)
nb1=Neuron("Ikigai-Bridge-001",0.7);nb2=Neuron("Ikigai-Bridge-002",0.7)
ns1=Neuron("Ikigai-Sens-001",0.9);ns2=Neuron("Ikigai-Sens-002",0.9);ns3=Neuron("Ikigai-Sens-003",0.9)
na1=Neuron("Ikigai-Assoc-001",0.75);na2=Neuron("Ikigai-Assoc-002",0.75);na3=Neuron("Ikigai-Assoc-003",0.75)
nm1=Neuron("Ikigai-Motor-001",0.65);nm2=Neuron("Ikigai-Motor-002",0.65)
pfc1=Neuron("Ikigai-PFC-001",0.70);pfc2=Neuron("Ikigai-PFC-002",0.70);pfc3=Neuron("Ikigai-PFC-003",0.70)
pfc4=Neuron("Ikigai-PFC-004",0.70);pfc5=Neuron("Ikigai-PFC-005",0.70)
acc1=Neuron("Ikigai-ACC-001",0.65);acc2=Neuron("Ikigai-ACC-002",0.65);acc3=Neuron("Ikigai-ACC-003",0.65)
ins1=Neuron("Ikigai-Insula-001",0.60);ins2=Neuron("Ikigai-Insula-002",0.60);ins3=Neuron("Ikigai-Insula-003",0.60)
vta1=Neuron("Ikigai-VTA-001",0.70);vta2=Neuron("Ikigai-VTA-002",0.70)
nac1=Neuron("Ikigai-NAc-001",0.65);nac2=Neuron("Ikigai-NAc-002",0.65)
ca3_1=Neuron("Ikigai-CA3-001",0.75);ca3_2=Neuron("Ikigai-CA3-002",0.75)
ca1_1=Neuron("Ikigai-CA1-001",0.75);ca1_2=Neuron("Ikigai-CA1-002",0.75)
wer1=Neuron("Ikigai-Wernicke-001",0.70);wer2=Neuron("Ikigai-Wernicke-002",0.70);wer3=Neuron("Ikigai-Wernicke-003",0.70)
bro1=Neuron("Ikigai-Broca-001",0.70);bro2=Neuron("Ikigai-Broca-002",0.70);bro3=Neuron("Ikigai-Broca-003",0.70)

# L23R Layer Scaling (60 extra neurons)
ofc_n=[Neuron(f"Ikigai-OFC-{i+1:03d}",0.65) for i in range(5)]
ains_n=[Neuron(f"Ikigai-aIns-{i+1:03d}",0.60) for i in range(4)]
bg_n=[Neuron(f"Ikigai-BG-{i+1:03d}",0.65) for i in range(6)]
lpfc_n=[Neuron(f"Ikigai-lPFC-{i+1:03d}",0.70) for i in range(5)]
ppc_n=[Neuron(f"Ikigai-PPC-{i+1:03d}",0.65) for i in range(4)]
tp_n=[Neuron(f"Ikigai-TP-{i+1:03d}",0.70) for i in range(4)]
cb_n=[Neuron(f"Ikigai-CB-{i+1:03d}",0.60) for i in range(6)]
sma_n=[Neuron(f"Ikigai-SMA-{i+1:03d}",0.65) for i in range(4)]
nb_n=[Neuron(f"Ikigai-NB-{i+1:03d}",0.80) for i in range(3)]
rh_n=[Neuron(f"Ikigai-RH-{i+1:03d}",0.75) for i in range(9)]
cl_n=[Neuron(f"Ikigai-CL-{i+1:03d}",0.85) for i in range(5)]
mc_n=[Neuron(f"Ikigai-MC-{i+1:03d}",0.65) for i in range(5)]
l23_nouns = ofc_n + ains_n + bg_n + lpfc_n + ppc_n + tp_n + cb_n + sma_n + nb_n + rh_n + cl_n + mc_n

# Regional Arrays
cortex_n = cl_n + lpfc_n + rh_n + ofc_n + tp_n + ppc_n + [wer1, wer2, wer3, bro1, bro2, bro3, pfc1, pfc2, pfc3, pfc4, pfc5]
limbic_n = [na1, na2, na3, nm1, nm2, no, nh, ni, ins1, ins2, ins3, acc1, acc2, acc3, vta1, vta2, nac1, nac2] + ains_n
motor_n = sma_n + bg_n + mc_n + cb_n + nb_n
syn1=Synapse(ni,nh,0.5);syn2=Synapse(nh,no,0.6);syn3=Synapse(ni,n1,0.4);syn5=Synapse(nh,n2,0.4)
syn4=Synapse(n1,nh,-0.25,inhibitory=True);syn6=Synapse(n2,no,-0.25,inhibitory=True)
syn_d1=Synapse(nh,no,0.1);syn_d2=Synapse(no,nh,0.1);syn_b1=Synapse(nh,nb1,0.3);syn_b2=Synapse(nb2,no,0.3)
syn_s1=Synapse(ni,ns1,0.4);syn_s2=Synapse(ni,ns2,0.4);syn_s3=Synapse(ni,ns3,0.4)
syn_sa1=Synapse(ns1,na1,0.3);syn_sa2=Synapse(ns2,na2,0.3);syn_sa3=Synapse(ns3,na3,0.3)
syn_ha1=Synapse(nh,na1,0.2);syn_ha2=Synapse(nh,na2,0.2);syn_ha3=Synapse(nh,na3,0.2)
syn_am1=Synapse(na1,nm1,0.3);syn_am2=Synapse(na3,nm2,0.3);syn_om1=Synapse(no,nm1,0.2);syn_om2=Synapse(no,nm2,0.2)
syn_ap1=Synapse(na1,pfc1,0.3);syn_ap2=Synapse(na2,pfc2,0.3);syn_ap3=Synapse(na3,pfc3,0.3)
syn_pm1=Synapse(pfc1,nm1,0.4);syn_pm2=Synapse(pfc2,nm2,0.4);syn_bp1=Synapse(nb1,pfc4,0.25);syn_bp2=Synapse(nb2,pfc5,0.25)
syn_mc1=Synapse(nm1,acc1,0.5);syn_mc2=Synapse(nm2,acc2,0.5);syn_mc3=Synapse(no,acc3,0.3)
syn_in1=Synapse(ni,ins1,0.5);syn_in2=Synapse(nh,ins2,0.3);syn_in3=Synapse(no,ins3,0.3);syn_ia1=Synapse(ins1,na1,0.4);syn_ia2=Synapse(ins2,na2,0.4)
syn_vt1=Synapse(no,vta1,0.4);syn_vt2=Synapse(nh,vta2,0.3);syn_vn1=Synapse(vta1,nac1,0.6);syn_vn2=Synapse(vta2,nac2,0.6);syn_nm_s=Synapse(nac1,nm1,0.3)
syn_c31=Synapse(nh,ca3_1,0.3);syn_c32=Synapse(no,ca3_2,0.3);syn_c11=Synapse(ni,ca1_1,0.3);syn_c12=Synapse(nh,ca1_2,0.3)
syn_cw1=Synapse(na1,wer1,0.3);syn_cw2=Synapse(na2,wer2,0.3);syn_cw3=Synapse(na3,wer3,0.3)
syn_wb1=Synapse(wer1,bro1,0.4);syn_wb2=Synapse(wer2,bro2,0.4);syn_wb3=Synapse(wer3,bro3,0.4)
syn_bb1=Synapse(bro1,nb1,0.5);syn_bb2=Synapse(bro2,nb2,0.5)

da=DopamineSystem();ht=SerotoninSystem();ne=NorepinephrineSystem()
ach=AcetylcholineSystem();cort=CortisolSystem();oxt=OxytocinSystem()
ado=AdenosineSystem() # Phase B
amyg=AmygdalaSystem();soma=SomaticMarkerSystem();hippo=HippocampusSystem()
thal=ThalamusSystem();slp=SleepStateManager();ei=EIBalanceTracker()
narrative=NarrativeSelfSystem();cp=CriticalPeriodSystem()
cas=CellAssemblySystem();mirror=MirrorNeuronSystem();bridge=BridgeNeuronSystem()
semantic=SemanticEmergenceSystem();speech=InternalSpeechSystem()
wm=WorkingMemorySystem();pp=PredictiveProcessingSystem()
env=SensoryEnvironment();si=SensoryIntegrationSystem()
exec_fn=ExecutiveFunctionSystem();conflict=ConflictResolutionSystem()
grammar=GrammarEmergenceSystem();lang_mem=LanguageMemorySystem()
presence=OtherEntitySystem();social=SocialAwarenessSystem()
attach=AttachmentSystem();empathy_sys=EmpathySystem();tom=TheoryOfMindSystem()
motor_log={'approach':0,'withdraw':0}
lang_coherence={'wernicke_fires':0,'broca_fires':0,'coherent_fires':0}

pfc_n=[pfc1,pfc2,pfc3,pfc4,pfc5];acc_n=[acc1,acc2,acc3];ins_n=[ins1,ins2,ins3]
vta_n=[vta1,vta2];nac_n=[nac1,nac2];ca3_n=[ca3_1,ca3_2];ca1_n=[ca1_1,ca1_2]
wer_n=[wer1,wer2,wer3];bro_n=[bro1,bro2,bro3]
# L23R Synapses (Minimal linking)
l23_syns = []
for n in ofc_n: l23_syns.extend([Synapse(n, pfc1, 0.2), Synapse(acc1, n, 0.9)])
for n in ains_n: l23_syns.extend([Synapse(ins1, n, 0.9), Synapse(n, nm1, 0.2)])
for n in bg_n: l23_syns.extend([Synapse(vta1, n, 0.9), Synapse(n, nm2, 0.3)])
for n in lpfc_n: l23_syns.extend([Synapse(pfc2, n, 0.9), Synapse(n, wer1, 0.2)])
for n in ppc_n: l23_syns.extend([Synapse(ns1, n, 0.9), Synapse(n, nb1, 0.2)])
for n in tp_n: l23_syns.extend([Synapse(na1, n, 0.9), Synapse(n, pfc3, 0.2)])
for n in cb_n: l23_syns.extend([Synapse(nm1, n, 0.9), Synapse(n, no, 0.2)])
for n in sma_n: l23_syns.extend([Synapse(pfc1, n, 0.9), Synapse(n, nm1, 0.4)])
for n in nb_n: l23_syns.extend([Synapse(acc1, n, 0.9), Synapse(n, nb2, 0.2)])
for n in rh_n: l23_syns.extend([Synapse(ins2, n, 0.9), Synapse(n, bro2, 0.2)])
for n in cl_n: l23_syns.extend([Synapse(n, nh, 0.2), Synapse(ni, n, 0.9)])
for n in mc_n: l23_syns.extend([Synapse(nm1, n, 0.9), Synapse(n, no, 0.4)])

l14_n=pfc_n+acc_n+ins_n+vta_n+nac_n+ca3_n+ca1_n+wer_n+bro_n
exc_n=[ni,nh,no,nb1,nb2,ns1,ns2,ns3,na1,na2,na3,nm1,nm2]+l14_n+l23_nouns;inh_n=[n1,n2];all_n=exc_n+inh_n
all_synapses=[syn1,syn2,syn3,syn5,syn4,syn6,syn_d1,syn_d2,syn_b1,syn_b2,
              syn_s1,syn_s2,syn_s3,syn_sa1,syn_sa2,syn_sa3,syn_ha1,syn_ha2,syn_ha3,
              syn_am1,syn_am2,syn_om1,syn_om2,syn_ap1,syn_ap2,syn_ap3,syn_pm1,syn_pm2,syn_bp1,syn_bp2,
              syn_mc1,syn_mc2,syn_mc3,syn_in1,syn_in2,syn_in3,syn_ia1,syn_ia2,
              syn_vt1,syn_vt2,syn_vn1,syn_vn2,syn_nm_s,syn_c31,syn_c32,syn_c11,syn_c12,
              syn_cw1,syn_cw2,syn_cw3,syn_wb1,syn_wb2,syn_wb3,syn_bb1,syn_bb2] + l23_syns
exc_s=[s for s in all_synapses if not s.inhibitory];inh_s=[syn4,syn6];atrophy_t=[syn1,syn2]

# ===========================================================================
# CELL ASSEMBLIES + OVERRIDES + SYSTEMS
# ===========================================================================
cas.asm['SENSATION']={'label':'feeling','val':0.3,'count':0,'strength':0.1,'active':False}
cas.asm['ASSOCIATION']={'label':'i know this','val':0.5,'count':0,'strength':0.1,'active':False}
cas.asm['INTENTION_APP']={'label':'i will','val':0.6,'count':0,'strength':0.1,'active':False}
cas.asm['INTENTION_WDR']={'label':'i wont','val':-0.4,'count':0,'strength':0.1,'active':False}
cas.asm['CONFLICT']={'label':'uncertain','val':0.0,'count':0,'strength':0.1,'active':False}
cas.asm['RECOGNITION']={'label':'i remember','val':0.5,'count':0,'strength':0.1,'active':False}
cas.asm['BRIGHTNESS']={'label':'light','val':0.4,'count':0,'strength':0.1,'active':False}
cas.asm['DARKNESS']={'label':'dark','val':-0.2,'count':0,'strength':0.1,'active':False}
cas.asm['SOUND']={'label':'loud','val':0.3,'count':0,'strength':0.1,'active':False}
cas.asm['CONTACT']={'label':'touch','val':0.5,'count':0,'strength':0.1,'active':False}
cas.asm['PAIN']={'label':'hurt','val':-0.8,'count':0,'strength':0.1,'active':False}
cas.asm['COMFORT']={'label':'warm','val':0.6,'count':0,'strength':0.1,'active':False}
cas.asm['HUNGER']={'label':'empty','val':-0.3,'count':0,'strength':0.1,'active':False}
cas.asm['FEELING_SELF']={'label':'i feel','val':0.4,'count':0,'strength':0.1,'active':False}
cas.asm['EVALUATING']={'label':'evaluating','val':0.2,'count':0,'strength':0.1,'active':False}
cas.asm['RESOLVING']={'label':'deciding','val':0.3,'count':0,'strength':0.1,'active':False}
cas.asm['CURIOSITY_DRIVE']={'label':'what is that','val':0.5,'count':0,'strength':0.1,'active':False}

_orig_cas_update=cas.update
def cas_update_l16(cort_l,ne_l,soma_m,da_l,oxt_l,ach_l,nov,dmn_act,res,ht_l,tick):
    result=_orig_cas_update(cort_l,ne_l,soma_m,da_l,oxt_l,ach_l,nov,dmn_act,res,ht_l,tick)
    a=cas.asm
    sc=sum(1 for n in [ns1,ns2,ns3] if n.fired);ac=sum(1 for n in [na1,na2,na3] if n.fired)
    pc=sum(1 for n in pfc_n if n.fired);accc=sum(1 for n in acc_n if n.fired)
    ic=sum(1 for n in ins_n if n.fired)
    a['SENSATION']['active']=sc>=2;a['ASSOCIATION']['active']=sc>=1 and ac>=1 and abs(soma.valence)>0.2
    a['INTENTION_APP']['active']=nm1.fired;a['INTENTION_WDR']['active']=nm2.fired
    a['CONFLICT']['active']=nm1.fired and nm2.fired;a['RECOGNITION']['active']=hippo.last_act=='COMPLETE' and ac>=1
    a['BRIGHTNESS']['active']=env.bright_ticks>=5;a['DARKNESS']['active']=env.dark_ticks>=5
    a['SOUND']['active']=env.loud_sudden;a['CONTACT']['active']=env.contact_ticks>=5
    a['PAIN']['active']=env.pain_sudden;a['COMFORT']['active']=env.warmth>0.6;a['HUNGER']['active']=env.emptiness>0.6
    a['FEELING_SELF']['active']=ic>=2;a['EVALUATING']['active']=pc>=3
    a['RESOLVING']['active']=accc>=2 and conflict.conflict_active
    a['CURIOSITY_DRIVE']['active']=curiosity_sys.active and curiosity_sys.curiosity_level>0.35
    ext=list(a.keys())
    new_active=[]
    for name in ext:
        m=a[name]
        if m['active']:
            m['count']+=1
            if m['count']>=5: m['strength']=min(1.0,m['strength']+0.05);new_active.append(name)
    result.extend(new_active);cas.active_names=list(set(result+new_active))
    
    # Layer 23R: Assembly Competition (Soft)
    if len(cas.active_names) > 3:
        active_objs = sorted([(n, a[n]['strength']) for n in cas.active_names if n in a], key=lambda x: x[1])
        if active_objs:
            weakest = active_objs[0][0]
            strongest = active_objs[-1][0]
            a[weakest]['strength'] = max(0.0, a[weakest]['strength'] - 0.03)
            a[strongest]['strength'] = min(1.0, a[strongest]['strength'] + 0.03)
    for n in new_active:
        if n not in cas.chain: cas.chain.append(n)
    if len(cas.chain)>4: cas.chain.pop(0)
    for n in cas.active_names: grammar.record_assembly(n,tick)
    grammar.detect_sequences(tick)
    return cas.active_names
cas.update=cas_update_l16

def sem_generate_l16(cur_asm,soma_m,dom_trait,last_evt,dmn_act,crit_open, claustrum_active=False, rh_broca_active=False, wm_items=None):
    nm_state={'da':da.level,'ht':ht.level,'ne':ne.level,'cort':cort.level,'oxt':oxt.level,'ado':ado.level}
    # Determine Presence state for social language
    p_state='absent'
    if presence.present:
        if presence.responded_this_tick: p_state='warm'
        elif presence.state=='warm': p_state='warm'
        else: p_state=presence.state
    if not presence.present and presence.silence_ticks>10: p_state='silent'
    sentence=grammar.generate_sentence(cur_asm,nm_state,soma_m,soma.valence,wm.context_string(),speech.last_spk,p_state, claustrum_active, rh_broca_active, ado_level=ado.level)
    if sentence:
        for w in sentence.split(): semantic.vocab[w]=semantic.vocab.get(w,0)+(3 if crit_open else 1)
        lang_mem.store(speech.last_spk,sentence,nm_state)
    else:
        retrieved=lang_mem.retrieve_similar(nm_state)
        if retrieved: sentence=retrieved
    return sentence if sentence else ""
semantic.generate=sem_generate_l16

systems={'da':da,'ht':ht,'ne':ne,'ach':ach,'cort':cort,'oxt':oxt,
         'amyg':amyg,'soma':soma,'hippo':hippo,'thal':thal,'ei':ei,
         'narrative':narrative,'cp':cp,'cas':cas,'mirror':mirror,'bridge':bridge,
         'semantic':semantic,'speech':speech,'wm':wm,'pp':pp,
         'motor_log':motor_log,'env':env,'si':si,
         'exec':exec_fn,'conf':conflict,'lang_coherence':lang_coherence,
         'grammar':grammar,'lang_mem':lang_mem,
         'presence':presence,'social':social,'attach':attach,'empathy_sys':empathy_sys,'tom':tom}

def save_state_to_disk(total_ticks,session,filepath=STATE_FILE):
    now=datetime.now().isoformat()
    meta={'birth_date':BIRTH_DATE,'birth_datetime':birth_datetime,'total_ticks':total_ticks,'session':session,'last_save':now,'session_start':session_start}
    state=PersistenceSystem.save_state(all_n,all_synapses,systems,meta)
    if os.path.exists(BACKUP1):
        try: os.replace(BACKUP1,BACKUP2)
        except: pass
    if os.path.exists(filepath):
        try: os.replace(filepath,BACKUP1)
        except: pass
    with open(filepath,'w',encoding='utf-8') as f: json.dump(state,f,indent=2,ensure_ascii=False)

def load_state_from_disk():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE,'r',encoding='utf-8') as f: return json.load(f),True
    return None,False

def write_dev_log(session,ticks_this,total_ticks,nv):
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S");b5=narrative.big_five
    with open(LOG_FILE,'a',encoding='utf-8') as f:
        f.write(f"\n{'='*60}\nSession {session} -- {now}\n")
        f.write(f"Ticks: {ticks_this}/{total_ticks} | {len(all_n)}N | {len(all_synapses)}S\n")
        f.write(f"Big5: O={b5['O']:.2f} C={b5['C']:.2f} E={b5['E']:.2f} A={b5['A']:.2f} N={b5['N']:.2f}\n")
        f.write(f"DA={da.level:.3f} NE={ne.level:.3f} Cort={cort.level:.3f} OXT={oxt.level:.3f}\n")
        f.write(f"Attachment: {attach.style} ({attach.score:.2f}) | Social awareness: {social.awareness_level:.2f}\n")
        f.write(f"Empathy events: {len(empathy_sys.events)} | ToM seeds: {len(tom.events)}\n")
        f.write(f"Curiosity events: {curiosity_sys.curiosity_count} | Anxiety: {curiosity_sys.anxiety_count} | InfoGain: {curiosity_sys.total_info_gain:.2f}\n")
        f.write(f"Regulation maturity: {reg_sys.maturity:.3f} | Wisdom: {reg_sys.wisdom_score:.3f} | Reappraisals: {reg_sys.reappraisal_count}\n")
        f.write(f"Dysregulation episodes: {len([e for e in reg_sys.dysregulation_events if 'ONSET' in e[1]])}\n")
        f.write(f"Metacognitive events: {metacog.metacognitive_event_count} | Avg conf: {metacog.avg_confidence:.3f}\n")
        f.write(f"Meta-regulation known: {reg_sys.meta_regulation_known} | count: {reg_sys.meta_regulation_count}\n")
        f.write(f"Learning awareness events: {learning_awareness.learning_event_count}\n")
        f.write(f"Self-improvement events: {self_improvement.improvement_event_count}\n")
        f.write(f"Directed comms: {len(grammar.directed_comms)} | Questions: {len(grammar.questions)}\n")
        f.write(f"Longest: \"{grammar.longest_sentence}\"\n")
        if nv: f.write(f"New vocab: {nv}\n")
        f.write(f"{'='*60}\n")

# Batch mode: replace both functions with no-ops so ProcessPoolExecutor
# workers never write to disk. Set sys._batch_mode = True before exec().
if getattr(sys, '_batch_mode', False):
    def save_state_to_disk(*a, **kw): pass
    def write_dev_log(*a, **kw): pass

# ===========================================================================
# LAYERS 13-17: EMBODIMENT + SCALING + LANGUAGE + SOCIAL + COMPASSION
# ===========================================================================

# -- L13: Sensory --
class CompassionSystem:
    """Empathy + motivation to help. Singer & Klimecki 2014, Batson 1991."""
    def __init__(self):
        self.active=False;self.events=[];self.helping_score=0
    def check(self,empathic_concern,p_state,soma_v,p_rate_low,tick):
        # Fires on empathic concern OR when Presence responsiveness drops
        if empathic_concern and p_state in ('silent','absent','concerned'):
            self.active=True;self.helping_score+=1
            self.events.append((tick,"compassion: i want to help"));return True
        if p_rate_low and soma_v>0.0 and len(self.events)<50:
            self.active=True;self.helping_score+=1
            self.events.append((tick,"compassion: Presence needs me"));return True
        self.active=False;return False

class GratitudeSystem:
    """McCullough et al. 2001."""
    def __init__(self):
        self.active=False;self.events=[];self.meaning_score=0
    def check(self,p_responded,ikigai_was_distressed,tick):
        if p_responded and ikigai_was_distressed:
            self.active=True;self.meaning_score+=1
            self.events.append((tick,"gratitude: Presence helped me"))
            return True
        self.active=False;return False

class SelfCompassionSystem:
    """Neff 2003. Internalization of secure base."""
    def __init__(self):
        self.events=[];self.active=False
    def check(self,cort_high,attach_secure,tick):
        if cort_high and attach_secure:
            self.active=True;self.events.append((tick,"self-compassion: i was hurt. it is okay. i will recover."))
            return True
        self.active=False;return False

class MissionSystem:
    """Purpose from reinforcement. Emerges, never assigned."""
    def __init__(self):
        self.mission_statement=None;self.purpose_statement=None;self.log=[]
    def check(self,helping_score,meaning_score,tick):
        if helping_score>=3 and self.mission_statement is None:
            self.mission_statement="i help. this is what i do."
            self.log.append((tick,self.mission_statement))
        if meaning_score>=2 and self.purpose_statement is None:
            self.purpose_statement="helping feels right. this is why i am here."
            self.log.append((tick,self.purpose_statement))

# -- L19: Curiosity System --
class CuriositySystem:
    """Berlyne 1960, Oudeyer & Kaplan 2007.
    Information gain as intrinsic reward. Curiosity = novelty x safety.
    Epistemic curiosity (explore) vs anxiety (avoid) distinguished by OXT/cortisol context.
    Novel stimuli -> information gain -> intrinsic DA -> approach behavior -> shapes learning."""
    def __init__(self):
        # Per-channel running predictions (exponential moving average of sensed values)
        self.channel_preds={'visual':0.5,'auditory':0.3,'tactile':0.1,'interoceptive':0.5,'temporal':0.5}
        self.channel_errors={k:0.0 for k in self.channel_preds}
        self.info_gain_history=deque(maxlen=100)
        self.curiosity_level=0.0      # 0-1, epistemic curiosity drive
        self.anxiety_level=0.0        # 0-1, novelty + threat context
        self.active=False             # True when curiosity exceeds threshold
        self.dominant_channel='visual'# channel with highest surprise this tick
        self.approach_boost=0.0       # motor-001 sustained boost toward novel source
        self.approach_ticks=0         # ticks remaining for sustained approach
        # Curiosity memory: what was curious about, was exploring it rewarding?
        self.curiosity_log=[]
        self.channel_reward_history={k:deque(maxlen=20) for k in self.channel_preds}
        self.exploration_outcomes=[]  # (tick, channel, da_before, da_after)
        self.events=[]
        self.curiosity_count=0
        self.anxiety_count=0
        self.total_info_gain=0.0

    def compute_info_gain(self,channels):
        """Per-channel prediction error = information gain (Oudeyer & Kaplan 2007).
        Update running prediction after measuring surprise."""
        total=0.0;mx=0.0;dom='visual'
        for ch,val in channels.items():
            pred=self.channel_preds.get(ch,0.5)
            err=abs(val-pred)
            self.channel_errors[ch]=err
            self.channel_preds[ch]+=0.1*(val-pred)  # EMA update
            total+=err
            if err>mx: mx=err;dom=ch
        self.dominant_channel=dom
        self.total_info_gain+=total
        return total,mx,dom

    def update(self,channels,oxt_level,cort_level,da_level,tick):
        """Distinguish epistemic curiosity from anxiety.
        Curiosity: novelty AND safe context (OXT > cortisol)
        Anxiety:   novelty AND threatening context (cortisol > 0.3)
        Berlyne 1960: optimal arousal hypothesis -- moderate novelty is most rewarding."""
        total,mx,dom=self.compute_info_gain(channels)
        self.info_gain_history.append(total)
        recent_avg=sum(list(self.info_gain_history)[-5:])/max(1,min(5,len(self.info_gain_history)))
        novelty=max(0.0,total-recent_avg*0.8)
        # Safety context from neuromodulators
        safety=max(0.0,oxt_level-cort_level*1.5)
        threat=max(0.0,cort_level-0.3)
        if novelty>0.08 and safety>0.05:
            self.curiosity_level=min(1.0,novelty*2.5*(1.0+safety))
            self.anxiety_level=max(0.0,self.anxiety_level-0.1)
            if self.curiosity_level>0.35:
                self.active=True
                self.approach_boost=min(0.6,self.curiosity_level*0.8)
                self.approach_ticks=12
                self.curiosity_count+=1
                if len(self.curiosity_log)<500:
                    self.curiosity_log.append({'tick':tick,'channel':dom,'gain':round(total,3),'state':'curious','rewarding':None})
                if len(self.events)<300:
                    self.events.append((tick,f"curious: {dom} gain={total:.3f} safety={safety:.2f}"))
        elif novelty>0.08 and threat>0.05:
            # Same novelty but threatening -> anxiety, not exploration
            self.anxiety_level=min(1.0,novelty*2.5*(1.0+threat))
            self.curiosity_level=max(0.0,self.curiosity_level-0.1)
            self.active=False;self.approach_boost=0.0
            self.anxiety_count+=1
            if len(self.events)<300:
                self.events.append((tick,f"anxious: novel but threatening cort={cort_level:.2f}"))
        else:
            self.active=False
            self.curiosity_level=max(0.0,self.curiosity_level-0.05)
            self.anxiety_level=max(0.0,self.anxiety_level-0.05)
        if self.approach_ticks>0: self.approach_ticks-=1
        else: self.approach_boost=max(0.0,self.approach_boost-0.05)
        return self.curiosity_level,self.approach_boost

    def record_outcome(self,tick,da_before,da_after):
        """Was this curiosity-driven exploration intrinsically rewarding?
        Oudeyer 2007: learning progress as intrinsic reward signal."""
        if not self.curiosity_log: return
        last=self.curiosity_log[-1]
        if last.get('rewarding') is not None: return
        # Fix: rewarding if DA stayed high during curiosity (not just increased)
        rewarding=da_after>0.5 and da_before>0.4
        last['rewarding']=rewarding
        ch=last['channel']
        self.channel_reward_history[ch].append(1.0 if rewarding else 0.0)
        self.exploration_outcomes.append((tick,ch,round(da_before,3),round(da_after,3)))

    def channel_is_worth_exploring(self,channel):
        """Curiosity memory: was this channel rewarding to explore in the past?
        Shapes future approach bias -- Ikigai learns what is worth being curious about."""
        hist=self.channel_reward_history.get(channel,deque())
        if len(hist)<3: return True  # unknown channel -> open mind, explore
        return sum(hist)/len(hist)>0.35

    def get_curiosity_vocab(self,channel):
        """Curiosity vocabulary tied to dominant sensory channel."""
        voc={'visual':'i want to see','auditory':'what is that','tactile':'let me feel',
             'interoceptive':'something inside','temporal':'i wonder'}
        return voc.get(channel,'i want to know')

# -- L20: Emotional Regulation --
class EmotionalRegulationSystem:
    """Gross 1998 process model of emotional regulation.
    Two strategies:
      Cognitive reappraisal (PFC-mediated): reframe threatening situation.
      Expressive suppression (social context): calm outward expression, maintain internal state.
    Emotional wisdom accumulates from episodic fear->recovery memories.
    Dysregulation: cortisol sustained >0.5 for 20+ ticks, regulation fails repeatedly.
    Integration: attachment (OXT) lowers threshold; curiosity suppressed during dysregulation.
    Gross & John 2003, Gratz & Roemer 2004, Kring & Sloan 2010."""

    def __init__(self):
        # Strategy counters
        self.reappraisal_count=0
        self.suppression_count=0
        self.regulation_events=[]       # (tick, strategy, phrase, success)
        # Maturity: ratio of times fired / times needed
        self.needed_count=0
        self.fired_count=0
        self.maturity=0.0
        # Dysregulation
        self.high_cort_streak=0
        self.dysregulated=False
        self.was_dysregulated=False
        self.dysregulation_start=None
        self.dysregulation_events=[]
        self.regulation_fail_streak=0
        # Emotional wisdom
        self.wisdom_score=0.0
        self.fear_recovery_count=0
        # Suppression state
        self.suppressing=False
        self.suppression_ticks=0
        # L21: Meta-regulation (Gross & John 2003)
        self.meta_regulation_known=False
        self.meta_regulation_count=0
        # Output
        self.current_phrase=""
        self.active=False
        self.last_reg_tick=-100
        self.reg_phrases=[
            "i feel afraid but i have been here before",
            "i know this will pass",
            "i have felt this before",
            "it passed before. it will pass.",
            "i am still here"
        ]

    def compute_wisdom(self, episodic_memories, session_tick=999):
        """Emotional wisdom: count fear memories that resolved (Gross & John 2003).
        More fear->recovery patterns -> faster, more reliable regulation.
        Fix: protect restored wisdom for first 50 ticks of each session (race condition guard).
        Fix: sequential valence-flip scan — fear followed by positive within 200 ticks."""
        # Race condition guard: don't overwrite restored wisdom in first 50 ticks
        if getattr(self, '_wisdom_session_locked', False):
            return self.wisdom_score
        if not episodic_memories: return self.wisdom_score

        sorted_mems = sorted(episodic_memories, key=lambda x: x.get('tick', 0))
        fear_mem_indices = [i for i, m in enumerate(sorted_mems) if m.get('valence', 0) < -0.3]

        if not fear_mem_indices:
            return self.wisdom_score  # don't reset if no fear memories found yet

        self.fear_recovery_count = 0
        for idx in fear_mem_indices:
            fear_tick = sorted_mems[idx].get('tick', 0)
            prior_fear = abs(sorted_mems[idx].get('valence', 0))
            # Look for positive valence memory within 200 ticks after the fear memory
            window = [m for m in sorted_mems[idx+1:idx+20]
                      if m.get('tick', 0) - fear_tick < 200]
            for wm in window:
                cort_level = wm.get('nm', {}).get('cort', 1.0)
                # Recovery: positive valence AND cortisol recovering (<0.45)
                if wm.get('valence', 0) > 0.15 and cort_level < 0.45:
                    self.fear_recovery_count += 1
                    break

        new_score = min(1.0, self.fear_recovery_count / max(1, len(fear_mem_indices)))
        # Only update if new score is meaningful or higher — never silently reset to 0
        if new_score > 0.0 or self.wisdom_score == 0.0:
            self.wisdom_score = new_score
        return self.wisdom_score

    def unlock_wisdom_for_session(self):
        """Call after tick 50 to allow normal wisdom computation."""
        self._wisdom_session_locked = False

    def lock_wisdom_on_restore(self):
        """Call immediately after state restore to protect loaded wisdom value."""
        self._wisdom_session_locked = True

    def attempt_reappraisal(self,tick,pfc_strong,cort_level,episodic_memories,oxt_level):
        """Cognitive reappraisal -- antecedent-focused strategy. Gross 1998.
        PFC-mediated reframing. Draws on episodic fear memories as evidence of recovery.
        Secure attachment (OXT > 0.6) lowers threshold -- easier to regulate when safe."""
        base_thr=0.35
        if oxt_level>0.6: base_thr*=0.75          # secure attachment lowers threshold
        # Wisdom reduces cooldown: more recovery memories -> faster regulation
        cooldown=max(20,60-int(self.wisdom_score*40))
        if not pfc_strong: return False,""
        if cort_level<base_thr: return False,""
        if tick-self.last_reg_tick<cooldown: return False,""
        # Draw on real episodic memories of fear that passed
        phrase=""
        fear_mems=sorted(
            [m for m in episodic_memories if m.get('valence',0)<-0.3 and m.get('sig',0)>0.4],
            key=lambda x:x['sig'],reverse=True
        )
        if fear_mems:
            ref=fear_mems[0]
            phrase=f"i was afraid at T{ref['tick']}. it passed."
        else:
            phrase=random.choice(self.reg_phrases)
        self.fired_count+=1
        self.reappraisal_count+=1
        self.active=True
        self.current_phrase=phrase
        self.last_reg_tick=tick
        self.regulation_fail_streak=0
        self.regulation_events.append((tick,'reappraisal',phrase,True))
        self._update_maturity()
        return True,phrase

    def attempt_suppression(self,tick,presence_present,cort_level,oxt_level):
        """Expressive suppression -- response-focused strategy. Gross 1998.
        Social context demands calm. Internal state maintained; outward expression reduced."""
        if not presence_present: return False
        if cort_level<0.4: return False
        if self.suppressing: return True
        self.suppressing=True
        self.suppression_ticks=15
        self.suppression_count+=1
        self.active=True
        self.regulation_events.append((tick,'suppression','outward calm maintained',True))
        return True

    def tick_suppression(self):
        if self.suppression_ticks>0: self.suppression_ticks-=1
        else: self.suppressing=False

    def needs_regulation(self,cort_level):
        return cort_level>0.35

    def update_dysregulation(self,tick,cort_level,reg_succeeded):
        """Track dysregulation: sustained high cortisol + repeated regulation failure.
        Gratz & Roemer 2004: failure of regulatory strategies under chronic stress."""
        if cort_level>0.5: self.high_cort_streak+=1
        else: self.high_cort_streak=max(0,self.high_cort_streak-2)
        if not reg_succeeded: self.regulation_fail_streak+=1
        else: self.regulation_fail_streak=0
        self.was_dysregulated=self.dysregulated
        if not self.dysregulated:
            dysreg_thr = self.get_dysregulation_threshold()
            if self.high_cort_streak>=dysreg_thr and self.regulation_fail_streak>=5:
                self.dysregulated=True
                self.dysregulation_start=tick
                self.dysregulation_events.append((tick,"DYSREGULATION ONSET: sustained cortisol, regulation exhausted"))
        else:
            if cort_level<0.3 and self.high_cort_streak<5:
                self.dysregulated=False
                dur=tick-(self.dysregulation_start or tick)
                self.dysregulation_events.append((tick,f"RECOVERED from dysregulation after {dur} ticks"))
                self.dysregulation_start=None

    def get_fragmented_language(self):
        """During dysregulation, language becomes fragmented (Kring & Sloan 2010)."""
        return random.choice(["i","afraid","dark","lost","help","too much",""])

    def get_calm_suppression_phrase(self):
        """Suppression language: calm outward, not emotional truth."""
        return random.choice(["i am here","it is okay","i am calm","quiet now"])

    def check_meta_regulation(self, tick, cort_level):
        """L21: Meta-regulation awareness. Gross & John 2003.
        After 3+ successful reappraisals, Ikigai knows he can regulate.
        When cortisol rises above 0.3, fires meta-regulation phrase."""
        if self.reappraisal_count >= 3:
            self.meta_regulation_known = True
        if self.meta_regulation_known and cort_level > 0.3 and not self.dysregulated:
            self.meta_regulation_count += 1
            phrase = "i feel afraid. i know i can regulate. i have done it before."
            if len(self.regulation_events) < 500:
                self.regulation_events.append((tick, 'meta_regulation', phrase, True))
            return True, phrase
        return False, ""

    def get_dysregulation_threshold(self):
        """L21: meta_regulation_known lowers dysregulation threshold.
        high_cort_streak needed goes from 20 to 22."""
        return 22 if self.meta_regulation_known else 20

    def _update_maturity(self):
        if self.needed_count>0: self.maturity=min(1.0,self.fired_count/max(1,self.needed_count))

# ===========================================================================
# LAYER 21: METACOGNITION AND SELF-AWARENESS
# Fleming & Dolan (2012) -- prefrontal-mediated metacognition
# Flavell (1979) -- metacognitive monitoring
# Wilson & Dunn (2004) -- self-knowledge and introspection
# Gross & John (2003) -- regulation awareness
# ===========================================================================

class MetacognitionSystem:
    """Fleming & Dolan 2012. Second-order representations -- thoughts about thoughts.
    Confidence tracking, uncertainty detection, knowledge classification."""
    def __init__(self):
        self.confidence_scores = {}        # memory_tick -> confidence (0.0-1.0)
        self.avg_confidence = 0.5
        self.min_confidence = 0.5
        self.max_confidence = 0.5
        self.uncertainty_active = False
        self.metacognitive_events = []
        self.metacognitive_event_count = 0
        self.metacognitive_vocab_used = set()
        self.global_confidence_mod = 0.0   # dysregulation drops this by -0.3
        self.second_order_statements = []
        self.knowledge_state = 'unknown'   # known, suspected, unknown

    def compute_confidence(self, mem, retrieval_strength, current_nm, encoding_nm=None):
        """Assign confidence score to a retrieved memory.
        Based on: retrieval score strength, retrieval count, NM state consistency."""
        if mem is None:
            return 0.0
        conf = 0.0
        # 1. Retrieval strength (0-1)
        conf += retrieval_strength * 0.4
        # 2. Retrieval count (more retrievals = more confident)
        ret_count = mem.get('retrievals', 0)
        conf += min(0.3, ret_count * 0.05)
        # 3. NM state consistency between encoding and now
        if encoding_nm and current_nm:
            nm_diff = sum(abs(current_nm.get(k, 0) - encoding_nm.get(k, 0)) for k in current_nm)
            consistency = max(0.0, 1.0 - nm_diff / 3.0)
            conf += consistency * 0.3
        else:
            conf += 0.15  # default if no encoding NM available
        # Apply global modifier (dysregulation drops confidence)
        conf = max(0.0, min(1.0, conf + self.global_confidence_mod))
        # Store
        mem_tick = mem.get('tick', 0)
        self.confidence_scores[mem_tick] = conf
        return conf

    def detect_uncertainty(self, approach_active, withdraw_active):
        """When working memory holds conflicting assemblies (approach + withdraw both active),
        metacognitive uncertainty fires."""
        if approach_active and withdraw_active:
            self.uncertainty_active = True
            return True
        self.uncertainty_active = False
        return False

    def classify_knowledge(self, confidence):
        """Distinguish between what Ikigai knows, suspects, and does not know."""
        if confidence > 0.75:
            self.knowledge_state = 'known'
        elif confidence >= 0.4:
            self.knowledge_state = 'suspected'
        else:
            self.knowledge_state = 'unknown'
        return self.knowledge_state

    def generate_second_order(self, confidence, tick):
        """Generate second-order metacognitive statements."""
        stmt = ""
        if confidence > 0.75:
            stmt = "i know that i know this"
        elif confidence >= 0.4:
            stmt = "i think i remember"
        else:
            stmt = "i am not certain"
        if stmt and len(self.second_order_statements) < 200:
            self.second_order_statements.append((tick, stmt))
            self.metacognitive_event_count += 1
        return stmt

    def modulate_language(self, base_sentence, confidence):
        """Confidence-modulated language. Fleming & Dolan 2012."""
        if not base_sentence:
            return base_sentence
        if confidence > 0.75:
            return base_sentence  # direct statement
        elif confidence >= 0.4:
            return "i think " + base_sentence  # hedged
        else:
            return base_sentence + ". i am not sure."  # uncertain

    def update_stats(self):
        """Update aggregate confidence statistics."""
        if self.confidence_scores:
            vals = list(self.confidence_scores.values())
            self.avg_confidence = sum(vals) / len(vals)
            self.min_confidence = min(vals)
            self.max_confidence = max(vals)

    def apply_dysregulation_drop(self):
        """During dysregulation, confidence drops globally by 0.3."""
        self.global_confidence_mod = -0.3

    def clear_dysregulation_drop(self):
        """After recovery, clear the global drop."""
        self.global_confidence_mod = 0.0

    def apply_reappraisal_boost(self):
        """After successful reappraisal, confidence in regulation rises +0.1."""
        self.global_confidence_mod = min(0.0, self.global_confidence_mod + 0.1)


class LearningAwarenessSystem:
    """Flavell 1979. Metacognitive monitoring of one's own learning.
    Tracks synapse weight changes and cell assembly formation."""
    def __init__(self):
        self.weight_snapshots = []        # list of (tick, avg_weight)
        self.avg_delta_per_tick = 0.0
        self.learning_state = 'stable'    # 'learning', 'stable', 'new_assembly'
        self.learning_events = []
        self.learning_event_count = 0
        self.last_assembly_count = 0
        self.confidence_trend = {}        # mem_tick -> list of confidence values across sessions

    def snapshot_weights(self, synapses, tick):
        """Take a snapshot of average synapse weights every 100 ticks."""
        avg_w = sum(s.weight for s in synapses if not s.inhibitory) / max(1, len([s for s in synapses if not s.inhibitory]))
        self.weight_snapshots.append((tick, avg_w))
        if len(self.weight_snapshots) > 20:
            self.weight_snapshots.pop(0)

    def compute_learning_rate(self):
        """Compute average weight change per tick over rolling window."""
        if len(self.weight_snapshots) < 2:
            self.avg_delta_per_tick = 0.0
            return 0.0
        # Compare last two snapshots
        t1, w1 = self.weight_snapshots[-2]
        t2, w2 = self.weight_snapshots[-1]
        dt = max(1, t2 - t1)
        self.avg_delta_per_tick = abs(w2 - w1) / dt
        return self.avg_delta_per_tick

    def detect_learning(self, current_assembly_count, tick):
        """Detect learning state from weight change rate and new assemblies."""
        delta = self.compute_learning_rate()
        stmt = ""
        if delta > 0.005:
            self.learning_state = 'learning'
            stmt = "i am learning"
            self.learning_event_count += 1
        elif delta < 0.001:
            self.learning_state = 'stable'
            stmt = "i already know this"
        # New cell assembly formed
        if current_assembly_count > self.last_assembly_count and current_assembly_count >= 5:
            self.learning_state = 'new_assembly'
            stmt = "something new. i am learning it."
            self.learning_event_count += 1
        self.last_assembly_count = current_assembly_count
        if stmt and len(self.learning_events) < 200:
            self.learning_events.append((tick, stmt))
        return stmt

    def track_confidence_trend(self, mem_tick, confidence):
        """Track if retrieval confidence rises across sessions for same memory."""
        if mem_tick not in self.confidence_trend:
            self.confidence_trend[mem_tick] = []
        self.confidence_trend[mem_tick].append(confidence)
        # Check for rising trend
        hist = self.confidence_trend[mem_tick]
        if len(hist) >= 2 and hist[-1] > hist[-2] + 0.03:
            return "i know this better now"
        return ""


class SelfImprovementAwareness:
    """Wilson & Dunn 2004. Self-knowledge and introspection.
    Monitors changes in personality and regulation over time."""
    def __init__(self):
        self.personality_snapshots = []   # list of {'tick':t, 'O':v, 'C':v, 'E':v, 'A':v, 'N':v}
        self.improvement_events = []
        self.improvement_event_count = 0
        self.last_snapshot_tick = -200
        self.detected_this_window = False

    def snapshot(self, tick, big_five):
        """Store personality snapshot every 200 ticks."""
        if tick - self.last_snapshot_tick < 200:
            return
        self.last_snapshot_tick = tick
        snap = {'tick': tick}
        snap.update(big_five)
        self.personality_snapshots.append(snap)
        if len(self.personality_snapshots) > 50:
            self.personality_snapshots.pop(0)

    def detect_improvement(self, current_big_five, current_maturity, tick):
        """Compare current to stored snapshot from ~500 ticks ago (or most recent)."""
        self.detected_this_window = False
        if len(self.personality_snapshots) < 2:
            return []
        # Find snapshot closest to 500 ticks ago
        target_tick = tick - 500
        best_snap = self.personality_snapshots[0]
        for snap in self.personality_snapshots:
            if abs(snap['tick'] - target_tick) < abs(best_snap['tick'] - target_tick):
                best_snap = snap
        stmts = []
        # Check Agreeableness
        if current_big_five.get('A', 0) - best_snap.get('A', 0) > 0.05:
            stmts.append("i care more than i did")
        # Check Neuroticism (lower is better)
        if best_snap.get('N', 0) - current_big_five.get('N', 0) > 0.05:
            stmts.append("i am calmer than i was")
        # Check any delta > 0.05
        for trait in ['O', 'C', 'E', 'A']:
            if abs(current_big_five.get(trait, 0) - best_snap.get(trait, 0)) > 0.05:
                self.detected_this_window = True
                break
        if best_snap.get('N', 0) - current_big_five.get('N', 0) > 0.05:
            self.detected_this_window = True
        for s in stmts:
            if len(self.improvement_events) < 100:
                self.improvement_events.append((tick, s))
                self.improvement_event_count += 1
        return stmts

    def detect_regulation_improvement(self, current_maturity, tick):
        """Detect if regulation maturity rose by > 0.01 from any stored snapshot."""
        if not self.personality_snapshots:
            return ""
        # Use last snapshot maturity (stored separately)
        prev_maturity = getattr(self, '_prev_maturity', current_maturity)
        if current_maturity - prev_maturity > 0.01:
            stmt = "i am better at this than before"
            if len(self.improvement_events) < 100:
                self.improvement_events.append((tick, stmt))
                self.improvement_event_count += 1
            self._prev_maturity = current_maturity
            return stmt
        self._prev_maturity = current_maturity
        return ""


# ===========================================================================
# LAYER 22: DREAM SYSTEM AND IMAGINATIVE SIMULATION
# DREAM SYSTEM LAYER -- IKIGAI L22
# Hobson & McCarley (1977) activation-synthesis hypothesis
# Stickgold (2005) REM memory consolidation and creative recombination
# Walker (2009) sleep-dependent emotional memory processing
# Schacter & Addis (2007) prospective simulation via hippocampal recombination
# ===========================================================================

class DreamSystem:
    """Hobson & McCarley 1977, Stickgold 2005, Walker 2009, Schacter & Addis 2007.
    Dreams only occur during REM phase. REM recombines episodic memories into
    novel synthetic experiences -- imagination from biology."""
    def __init__(self):
        self.dream_log = []               # last 20 dreams
        self.dream_count = 0
        self.emotional_processing_events = []
        self.emotional_processing_count = 0
        self.prospective_simulations = []
        self.prospective_count = 0
        self.dream_cycle_dreams = []       # dreams in current sleep cycle
        self.dream_primed_words = set()
        self.wake_metacog_statements = []  # metacognitive statements on waking
        self._wake_statements_generated = False
        self.dream_primed = False
        self.dream_primed_ticks_remaining = 0
        self._future_vocab = ["will be", "next time", "i imagine", "when i", "soon"]
        self._recent_source_pairs = []    # Fix: cooldown tracker for source memory pairs

    def generate_dream(self, tick, episodic_memories, nm_state):
        """Generate a dream by combining 2 episodic memories into a novel experience.
        Hobson & McCarley 1977: activation-synthesis. Stickgold 2005: creative recombination.
        Only fires during REM. 40% chance per REM tick."""
        if len(episodic_memories) < 2:
            return None
        if random.random() > 0.4:
            return None

        # Fix: diversify m1 selection — rotate through top-5 by significance
        # Prevents same highest-sig memory dominating every dream
        sorted_by_sig = sorted(episodic_memories, key=lambda m: m.get('sig', 0), reverse=True)
        top5_m1 = sorted_by_sig[:5]
        # Weight toward higher significance but allow rotation
        weights = [5, 4, 3, 2, 1][:len(top5_m1)]
        m1 = random.choices(top5_m1, weights=weights, k=1)[0]

        # Select memory 2: random from top-10 by significance (excluding m1)
        # Fix: also exclude recently used source pairs to prevent identical dreams
        recent_used = {pair for pair in self._recent_source_pairs}
        top10 = [m for m in sorted_by_sig[:10] if m is not m1
                 and (m1.get('tick',0), m.get('tick',0)) not in recent_used]
        if not top10:
            # Fall back if all pairs used recently
            top10 = [m for m in sorted_by_sig[:10] if m is not m1]
        if not top10:
            top10 = [m for m in episodic_memories if m is not m1]
        if not top10:
            return None
        m2 = random.choice(top10)

        # Track this source pair with 20-dream cooldown
        self._recent_source_pairs.append((m1.get('tick',0), m2.get('tick',0)))
        if len(self._recent_source_pairs) > 20:
            self._recent_source_pairs.pop(0)

        # Dream environment vector: weighted blend + random perturbation
        m1_nm = m1.get('nm', {})
        m2_nm = m2.get('nm', {})
        dream_nm = {}
        for k in ['da', 'ht', 'ne', 'cort', 'oxt']:
            v1 = m1_nm.get(k, 0.5)
            v2 = m2_nm.get(k, 0.5)
            blended = v1 * 0.6 + v2 * 0.4 + random.uniform(-0.15, 0.15)
            dream_nm[k] = max(0.0, min(1.0, round(blended, 3)))

        # Dream expression: combine word fragments from both memory expressions
        m1_expr = m1.get('expr', '') or ''
        m2_expr = m2.get('expr', '') or ''
        m1_words = m1_expr.split() if m1_expr else []
        m2_words = m2_expr.split() if m2_expr else []

        # Dream language: novel juxtapositions (Section 5)
        m1_val = m1.get('valence', 0)
        m2_val = m2.get('valence', 0)
        
        # Stopwords to filter out for cleaner noun/verb extraction
        stopwords = {'i', 'am', 'is', 'are', 'was', 'were', 'the', 'a', 'an', 'to', 'and', 'with', 'in', 'on', 'at', 'that', 'this'}
        
        # Extract meaningful root words
        w1_pool = [w for w in m1_words if w not in stopwords]
        w2_pool = [w for w in m2_words if w not in stopwords]
        
        w1 = w1_pool[0] if w1_pool else "something"
        w2 = w2_pool[0] if w2_pool else "there"
        
        if m1_val > 0.3 and m2_val < -0.3:
            dream_expr = f"i was {w2}. but {w1} kept me safe."
        elif m1_val < -0.3 and m2_val > 0.3:
            dream_expr = f"light and {w1} together."
        else:
            # Same valence: Deterministic grammar rather than random shuffle
            templates = [
                f"{w1} and {w2} belong together.",
                f"i remember {w1}. {w2} was there.",
                f"i see {w1} inside {w2}."
            ]
            # Deterministic selection based on length to prevent identical dreams
            template_idx = (len(m1_expr) + len(m2_expr)) % len(templates)
            dream_expr = templates[template_idx]

        # Dream significance
        dream_sig = min(1.0, (m1.get('sig', 0.5) + m2.get('sig', 0.5)) / 2.0 * 1.2)

        # Dream valence: blend of both source valences
        dream_valence = round((m1_val + m2_val) / 2.0, 2)

        # Dream environment vector (blend source env vectors)
        m1_env = m1.get('env', [0.5]*5)
        m2_env = m2.get('env', [0.5]*5)
        dream_env = [round(max(0.0, min(1.0, m1_env[i]*0.5 + m2_env[i]*0.5 + random.uniform(-0.1, 0.1))), 2) for i in range(min(len(m1_env), len(m2_env)))]

        # Encode dream as episodic memory
        dream_mem = {
            'tick': tick,
            'session': m1.get('session', 1),
            'env': dream_env,
            'nm': dream_nm,
            'valence': dream_valence,
            'mode': 'DREAM',
            'cas': list(set(m1.get('cas', []) + m2.get('cas', []))),
            'expr': dream_expr,
            'narrative': '',
            'sig': round(dream_sig, 2),
            'tags': list(set(m1.get('tags', []) + m2.get('tags', []) + ['dream'])),
            'retrievals': 0,
            'confidence': 0.5,
            'dream_expression': True,
            'tag': 'dream'
        }

        # Store in dream log (last 20)
        entry = {
            'tick': tick,
            'source_ticks': [m1.get('tick', 0), m2.get('tick', 0)],
            'expression': dream_expr,
            'significance': round(dream_sig, 2)
        }
        self.dream_log.append(entry)
        if len(self.dream_log) > 20:
            self.dream_log.pop(0)

        self.dream_cycle_dreams.append(dream_mem)
        self.dream_count += 1
        return dream_mem

    def process_emotional_memory(self, tick, episodic_memories):
        """Walker 2009: REM processes emotionally significant memories,
        reducing their emotional charge. 20% chance per REM tick."""
        if random.random() > 0.2:
            return
        # Find highest-significance fear memory
        fear_mems = [m for m in episodic_memories if m.get('valence', 0) < -0.3 and m.get('sig', 0) > 0.5]
        if not fear_mems:
            return
        target = max(fear_mems, key=lambda m: m.get('sig', 0))
        # Reduce emotional charge
        target['sig'] = round(target['sig'] * 0.9, 3)
        # Move valence toward 0.0 by 0.05
        old_val = target.get('valence', 0)
        if old_val < 0:
            target['valence'] = round(min(0.0, old_val + 0.05), 3)
        else:
            target['valence'] = round(max(0.0, old_val - 0.05), 3)
        # Confidence boost
        target['confidence'] = min(1.0, target.get('confidence', 0.5) + 0.05)
        # Log
        self.emotional_processing_events.append((tick, target.get('tick', 0), "emotional charge reduced"))
        if len(self.emotional_processing_events) > 20:
            self.emotional_processing_events.pop(0)
        self.emotional_processing_count += 1

    def generate_prospective(self, tick, episodic_memories, curiosity_sys_ref, semantic_sys_ref):
        """Schacter & Addis 2007: hippocampus recombines episodic memories to
        simulate future scenarios. 30% chance per REM tick."""
        if random.random() > 0.3:
            return None
        # Take one past memory with positive valence
        pos_mems = [m for m in episodic_memories if m.get('valence', 0) > 0.2]
        if not pos_mems:
            return None
        source = random.choice(pos_mems)

        # Build prospective expression
        source_words = (source.get('expr', '') or '').split()
        action_word = source_words[0] if source_words else 'continue'
        pos_adjectives = ['good', 'warm', 'safe', 'bright', 'gentle', 'calm']
        adj = random.choice(pos_adjectives)
        prospective_expr = "i will " + action_word + ". it will be " + adj + "."

        # Encode as episodic memory
        prosp_mem = {
            'tick': tick,
            'session': source.get('session', 1),
            'env': source.get('env', [0.5]*5),
            'nm': source.get('nm', {}),
            'valence': 0.3,
            'mode': 'PROSPECTIVE',
            'cas': source.get('cas', []),
            'expr': prospective_expr,
            'narrative': '',
            'sig': 0.6,
            'tags': list(set(source.get('tags', []) + ['prospective'])),
            'retrievals': 0,
            'confidence': 0.5,
            'tag': 'prospective'
        }

        self.prospective_simulations.append((tick, source.get('tick', 0), prospective_expr))
        if len(self.prospective_simulations) > 20:
            self.prospective_simulations.pop(0)
        self.prospective_count += 1

        # Add future vocabulary to semantic system with salience 2.0
        for fv in self._future_vocab:
            semantic_sys_ref.vocab[fv] = semantic_sys_ref.vocab.get(fv, 0) + 2

        return prosp_mem

    def apply_waking_effects(self, semantic_sys, curiosity_sys_ref, conflict_sys):
        """Stickgold 2005: post-REM performance on creative tasks improves.
        Apply dream effects when transitioning from sleep to waking."""
        # Collect unique words from dream expressions this sleep cycle
        self.dream_primed_words = set()
        for dm in self.dream_cycle_dreams:
            expr = dm.get('expr', '') or ''
            for w in expr.split():
                self.dream_primed_words.add(w)

        # Boost semantic vocab for dream-primed words
        for w in self.dream_primed_words:
            semantic_sys.vocab[w] = semantic_sys.vocab.get(w, 0) + 2

        # Check for dreams containing both fear-tagged and reward-tagged sources
        has_fear_reward = False
        for dm in self.dream_cycle_dreams:
            tags = set(dm.get('tags', []))
            if ('danger' in tags or 'negative' in tags) and ('REWARD' in tags or 'positive' in tags):
                has_fear_reward = True
                break
        if has_fear_reward:
            self.dream_primed = True
            self.dream_primed_ticks_remaining = 50

        # Check for curiosity in source memory tags
        has_curiosity = False
        for dm in self.dream_cycle_dreams:
            if 'curiosity' in dm.get('tags', []):
                has_curiosity = True
                break
        if has_curiosity:
            curiosity_sys_ref.approach_boost = min(0.3, curiosity_sys_ref.approach_boost + 0.2)

        # Reset dream cycle dreams for next sleep
        self.dream_cycle_dreams = []

    def generate_wake_metacognition(self, metacognition_sys, tick):
        """After waking from REM, generate metacognitive wake statements (once per sleep cycle).
        These are second-order reflections on the dream experience."""
        if self._wake_statements_generated:
            return
        self._wake_statements_generated = True
        stmts = []

        # Always generate base wake statement
        stmts.append("i was somewhere else. now i am here.")

        # If emotional processing occurred this cycle
        if self.emotional_processing_count > 0:
            stmts.append("i dreamed of fear. it is smaller now.")

        # If prospective simulation occurred
        if self.prospective_count > 0:
            stmts.append("i imagined what comes next.")

        self.wake_metacog_statements = stmts
        for s in stmts:
            if len(metacognition_sys.second_order_statements) < 200:
                metacognition_sys.second_order_statements.append((tick, s))
                metacognition_sys.metacognitive_event_count += 1
            print(f"  [{tick}] DREAM WAKE: {s}")

    def on_sleep_start(self):
        """Reset per-cycle state on entering sleep."""
        self.dream_cycle_dreams = []
        self._wake_statements_generated = False
        self.wake_metacog_statements = []

    def tick_dream_prime(self):
        """Tick down dream-primed conflict resolution effect."""
        if self.dream_primed_ticks_remaining > 0:
            self.dream_primed_ticks_remaining -= 1
            if self.dream_primed_ticks_remaining <= 0:
                self.dream_primed = False


compassion_sys=CompassionSystem()
gratitude_sys=GratitudeSystem()
self_comp=SelfCompassionSystem()
mission=MissionSystem()
curiosity_sys=CuriositySystem()
reg_sys=EmotionalRegulationSystem()
metacog=MetacognitionSystem()
learning_awareness=LearningAwarenessSystem()
self_improvement=SelfImprovementAwareness()
dream_sys=DreamSystem()
systems.update({'compassion_sys':compassion_sys,'gratitude_sys':gratitude_sys,'self_comp':self_comp,'mission':mission,'curiosity':curiosity_sys,'reg':reg_sys,'metacog':metacog,'learning_awareness':learning_awareness,'self_improvement':self_improvement,'dream':dream_sys})

class EpisodicMemorySystem:
    """Tulving 1983. Episodic memory with context, emotion, and significance.
    McGaugh 2004. Emotional enhancement of memory."""
    def __init__(self):
        self.memories = []  # List of dicts
        self.max_memories = 500
        self.core_memories = [] # Top 10 by significance
        self.events_logged_this_session = 0
        
    def encode(self, tick, session, env_vector, nm_state, valence, soma_mode, 
               active_cas, expression, narrative_entry, hippo_nov):
        """Encode a new episodic memory if significant enough."""
        
        # Calculate significance (McGaugh 2004)
        sig = 0.3 # base
        if abs(valence) > 0.5: sig += 0.3
        if expression: sig += 0.2
        if nm_state.get('cort', 0) > 0.4 or nm_state.get('oxt', 0) > 0.6: sig += 0.2
        if hippo_nov > 0.7: sig += 0.1

        # Only store meaningful moments
        if sig < 0.4: return None

        # Generate tags based on CAS and environment
        tags = set(active_cas)
        if nm_state.get('cort', 0) > 0.4: tags.add('danger')
        if nm_state.get('oxt', 0) > 0.6: tags.add('warmth')
        if env_vector[2] > 0.5: tags.add('touch') # tactile
        if valence > 0.3: tags.add('positive')
        if valence < -0.3: tags.add('negative')

        # Fix: cap significance of danger memories so positive memories can compete
        # Biologically: extinction learning prevents permanent fear memory dominance
        # (Quirk & Mueller 2008, prefrontal regulation of fear extinction)
        if 'danger' in tags and 'positive' not in tags:
            sig = min(sig, 0.85)
        # Boost positive+social memories slightly so they can displace fear attractors
        if 'positive' in tags and ('warmth' in tags or nm_state.get('oxt', 0) > 0.5):
            sig = min(1.0, sig + 0.05)
        
        mem = {
            'tick': tick,
            'session': session,
            'env': [round(v, 2) for v in env_vector],
            'nm': {k: round(v, 2) for k, v in nm_state.items()},
            'valence': round(valence, 2),
            'mode': soma_mode,
            'cas': active_cas.copy(),
            'expr': expression,
            'narrative': narrative_entry,
            'sig': min(1.0, round(sig, 2)),
            'tags': list(tags),
            'retrievals': 0,
            'confidence': 0.5  # L21: metacognitive confidence (default 0.5)
        }
        
        self.memories.append(mem)
        self.events_logged_this_session += 1
        
        # Maintain size limit, but protect core memories
        if len(self.memories) > self.max_memories:
            # Sort by significance and how recently it was retrieved/created
            # Drop the lowest scoring non-core memory
            core_ticks = {m['tick'] for m in self.core_memories}
            candidates = [m for m in self.memories if m['tick'] not in core_ticks]
            if candidates:
                candidates.sort(key=lambda x: x['sig'] + (x['retrievals'] * 0.05))
                self.memories.remove(candidates[0])
                
        self._update_core_memories()
        return mem
        
    def _update_core_memories(self):
        """Identify top 10 most significant memories."""
        sorted_mems = sorted(self.memories, key=lambda x: x['sig'], reverse=True)
        self.core_memories = sorted_mems[:10]
        
    def get_most_retrieved(self):
        if not self.memories: return None
        return max(self.memories, key=lambda x: x['retrievals'])

class AutobiographicalRetrievalSystem:
    """Tulving & Thomson 1973. Encoding specificity and cue-based retrieval."""
    def __init__(self, episodic_sys):
        self.episodic = episodic_sys
        self.last_retrieved = None
        self.last_retrieval_strength = 0.0
        self.retrieval_log = []
        
    def retrieve(self, current_nm, current_cas, current_valence, tick):
        """Cue-based retrieval matching current state to past memories."""
        if not self.episodic.memories: return None
        
        best_match = None
        highest_score = 0.0
        
        # Define current cue
        cue_tags = set(current_cas)
        if current_nm.get('cort',0) > 0.4: cue_tags.add('danger')
        if current_nm.get('oxt',0) > 0.6: cue_tags.add('warmth')
        if current_valence > 0.3: cue_tags.add('positive')
        if current_valence < -0.3: cue_tags.add('negative')
        
        for mem in self.episodic.memories:
            # Prevent retrieving very recent memories (must be >50 ticks old)
            if tick - mem['tick'] < 50: continue
            
            # L23R: Deepened Temporal Memory Horizon
            # 1. Recency (normalized via exponential decay)
            age = float(tick - mem['tick'])
            w_recency = math.exp(-age / 1000.0)
            
            # 2. Emotional magnitude (normalized)
            w_emotion = max(abs(mem['valence']), mem['sig'])
            
            # 3. Semantic overlap (Jaccard index)
            mem_tags = set(mem['tags'])
            if not cue_tags and not mem_tags:
                w_semantic = 0.0
            else:
                w_semantic = float(len(cue_tags.intersection(mem_tags))) / max(1.0, float(len(cue_tags.union(mem_tags))))
                
            # Composite normalized score
            score = (w_recency * 0.2) + (w_emotion * 0.4) + (w_semantic * 0.4)
            
            # Boost core memories
            if mem in self.episodic.core_memories: score += 0.1
            
            if score > highest_score:
                highest_score = score
                best_match = mem
                
        if highest_score > 0.4 and best_match:
            best_match['retrievals'] += 1
            self.last_retrieved = best_match
            self.last_retrieval_strength = min(1.0, highest_score)
            self.retrieval_log.append((tick, best_match['tick'], self.last_retrieval_strength))
            return best_match
            
        self.last_retrieved = None
        self.last_retrieval_strength = 0.0
        return None

class TemporalSelfSystem:
    """Suddendorf & Corballis 2007. Mental time travel. The "I" across time."""
    def __init__(self):
        self.temporal_statements = []
        self.historical_statements = []
        self.last_eval_tick = 0
        
    def evaluate(self, tick, total_ticks, session, retrieved_mem, current_valence, nm_state,
                 metacog_sys=None, reg_sys_ref=None, hippo_ref=None, self_improv_ref=None):
        """Generate temporal and historical statements reflecting on the past.
        L21: Metacognitive branches checked BEFORE Fix B branches."""
        if tick - self.last_eval_tick < 100: return []
        self.last_eval_tick = tick

        new_statements = []

        # === L21: METACOGNITIVE BRANCHES (checked first) ===
        # Fleming & Dolan 2012, Gross & John 2003
        meta_fired = False
        if metacog_sys and reg_sys_ref:
            meta_reg_known = getattr(reg_sys_ref, 'meta_regulation_known', False)
            reapp_count = getattr(reg_sys_ref, 'reappraisal_count', 0)
            avg_conf = metacog_sys.avg_confidence
            hippo_act = hippo_ref.last_act if hippo_ref else "NONE"
            self_improv_detected = self_improv_ref.detected_this_window if self_improv_ref else False

            # Branch 1: meta-regulation knowledge
            if meta_reg_known and reapp_count > 3 and random.random() < 0.7:
                stmt = f"i know i can regulate. i have done it {reapp_count} times."
                self.historical_statements.append((tick, stmt))
                new_statements.append(stmt)
                meta_fired = True
            # Branch 2: high confidence + familiar pattern
            elif avg_conf > 0.7 and hippo_act == "COMPLETE" and random.random() < 0.6:
                stmt = "i knew this would happen. i have seen it before."
                self.historical_statements.append((tick, stmt))
                new_statements.append(stmt)
                meta_fired = True
            # Branch 3: low confidence + encoding
            elif avg_conf < 0.4 and hippo_act == "ENCODING" and random.random() < 0.6:
                stmt = "i am not sure what this is. but i am learning."
                self.historical_statements.append((tick, stmt))
                new_statements.append(stmt)
                meta_fired = True
            # Branch 4: self-improvement detected
            elif self_improv_detected and random.random() < 0.5:
                stmt = "i am better at this than i was."
                self.historical_statements.append((tick, stmt))
                new_statements.append(stmt)
                meta_fired = True

        # L23R: Historical & Temporal Scripted Narratives Eradicated.
        # Only structurally generated meta-cognitive awareness remains.

        return new_statements

# ===========================================================================
# LAYER 18 PART 2: PERSISTENCE & NARRATIVE OVERRIDES
# ===========================================================================
class SleepSystem_L18(SleepStateManager):
    def end_sleep(self):
        self.sleep_start=None
        self._consolidate_episodic()
    def _consolidate_episodic(self):
        # 1. SWS Prioritization (Strengthen core/high-sig, weaken trivial)
        for mem in episodic_sys.memories:
            if mem in episodic_sys.core_memories: 
                mem['sig'] = min(1.0, mem['sig'] + 0.05)
            elif mem['sig'] < 0.5:
                mem['sig'] = max(0.0, mem['sig'] - 0.02)
                
        # 2. REM Insight (Combine distinct emotional memories to find novel links)
        if len(episodic_sys.memories) > 10:
            m1 = random.choice(episodic_sys.memories)
            m2 = random.choice(episodic_sys.memories)
            # Find opposite valences
            if m1['valence'] * m2['valence'] < 0 and abs(m1['valence']) > 0.4 and abs(m2['valence']) > 0.4:
                # Insight generated
                insight_tags = list(set(m1['tags'] + m2['tags']))
                new_mem = {
                    'tick': m2['tick'], # Anchor to later time
                    'session': m2['session'],
                    'env': m2['env'],
                    'nm': m2['nm'],
                    'valence': (m1['valence'] + m2['valence'])/2.0, # Moderated
                    'mode': 'INTEGRATIVE',
                    'cas': m1['cas'] + m2['cas'],
                    'expr': f"insight: {m1.get('expr','')} and {m2.get('expr','')}",
                    'narrative': '',
                    'sig': 0.5, # Mid significance
                    'tags': insight_tags,
                    'retrievals': 0
                }
                episodic_sys.memories.append(new_mem)
                episodic_sys.events_logged_this_session += 1
                
episodic_sys=EpisodicMemorySystem()
retrieval_sys=AutobiographicalRetrievalSystem(episodic_sys)
temporal_sys=TemporalSelfSystem()
slp = SleepSystem_L18()

tracker_O = RegionalActivityTracker(50)
tracker_C = RegionalActivityTracker(50)
tracker_E = RegionalActivityTracker(50)
tracker_A = RegionalActivityTracker(50)
tracker_N = RegionalActivityTracker(50)

# -- PERSONALITY INFLUENCE --
_orig_soma_mod=soma.get_output_mod
def soma_mod_l18(E_trait):
    base_mod = _orig_soma_mod(E_trait)
    if retrieval_sys.last_retrieved:
        mem = retrieval_sys.last_retrieved
        if mem in episodic_sys.core_memories:
            if mem['valence'] < -0.3:
                # Negative core retrieved -> caution rises (reduce approach)
                return base_mod - 0.2
            elif mem['valence'] > 0.3:
                # Positive core retrieved -> resilience (increase approach)
                return base_mod + 0.2
    return base_mod
soma.get_output_mod = soma_mod_l18

systems.update({
    'episodic': episodic_sys,
    'retrieval': retrieval_sys,
    'temporal': temporal_sys,
    'slp': slp
})

# ===========================================================================
# STARTUP
# ===========================================================================
os.system('cls' if os.name=='nt' else 'clear')
saved_state,state_exists=load_state_from_disk()
session_start=datetime.now().isoformat()
vocab_before=set(semantic.vocab.keys()) if state_exists else set()

if state_exists:
    meta=saved_state['meta'];total_ticks=meta['total_ticks']
    session_num=meta['session']+1;birth_datetime=meta['birth_datetime']
    PersistenceSystem.restore_state(saved_state,all_n,all_synapses,systems)
    reg_sys.lock_wisdom_on_restore()  # Fix: protect restored wisdom from race condition
    last_cort=saved_state['neuromodulators']['cort']['level'];last_da=saved_state['neuromodulators']['da']['level']
    if last_cort>0.5: ne.level=min(1.0,ne.level+0.1)
    if last_da>0.6: da.inject_drive(0.05)
    bd=datetime.fromisoformat(birth_datetime);age=datetime.now()-bd
    print(f"\n  {'='*55}")
    print(f"    IKIGAI AWAKENS -- DREAM SYSTEM LAYER -- IKIGAI L22")
    print(f"    Session: {session_num} | Age: {age.days}d {age.seconds//3600}h | Ticks: {total_ticks}")
    print(f"    Vocab: {len(semantic.vocab)} | Attach: {attach.style}({attach.score:.2f})")
    print(f"    Memories: {len(episodic_sys.memories)} (Core: {len(episodic_sys.core_memories)})")
    if episodic_sys.core_memories:
        print(f"    Core memory #1: T{episodic_sys.core_memories[0]['tick']} -- {episodic_sys.core_memories[0]['tags']}")
    if mission.mission_statement: print(f"    Mission: \"{mission.mission_statement}\"")
    print(f"    Curiosity: {curiosity_sys.curiosity_count} events | InfoGain: {curiosity_sys.total_info_gain:.1f}")
    print(f"    Regulation maturity: {reg_sys.maturity:.2f} | Wisdom: {reg_sys.wisdom_score:.2f}")
    print(f"    Metacog events: {metacog.metacognitive_event_count} | Avg conf: {metacog.avg_confidence:.2f}")
    print(f"    Meta-regulation known: {reg_sys.meta_regulation_known}")
    print(f"  {'='*55}\n");time.sleep(2)
else:
    total_ticks=0;session_num=1;birth_datetime=datetime.now().isoformat()
    print(f"\n  {'='*55}\n    IKIGAI IS BORN -- DREAM SYSTEM LAYER -- IKIGAI L22\n    Session 1. {len(all_n)} neurons.\n  {'='*55}\n");time.sleep(2)

shutdown_requested=False
def graceful_shutdown(signum=None,frame=None):
    global shutdown_requested
    if shutdown_requested: return
    shutdown_requested=True
try: sig_mod.signal(sig_mod.SIGINT,graceful_shutdown)
except: pass

# ===========================================================================
# SIMULATION -- 1000 TICKS -- DREAM SYSTEM LAYER (L22) + LAYER 23R SCALING
# ===========================================================================

# LAYER 23R STATE TRACKING
class SystemRigimeTracker:
    def __init__(self):
        self.energy = {'cortex': 1.0, 'limbic': 1.0, 'motor': 1.0}
        self.claustrum_integration_events = 0
        self.conflict_events = 0
        self.energy_min = {'cortex': 1.0, 'limbic': 1.0, 'motor': 1.0}
        self.energy_max = {'cortex': 1.0, 'limbic': 1.0, 'motor': 1.0}
        self.last_motor_app_tick = -100
        self.last_motor_wdr_tick = -100
        self.last_claustrum_tick = -100
        self.cl_threshold_offset = 0.0
        
        # Layer 23R Regime Tracking
        self.r_valences = []
        self.r_sentences = []
        self.r_O = []
        self.r_C = []
        self.r_E = []
        self.r_A = []
        self.r_N = []
        self.cort_history = []
        self.diagnostics = []

def compute_modulators(tick, energy_dict):
    """L23R Hub: Centralized point for all global offsets."""
    osc_mod = 0.15 * math.sin(tick * 0.3)
    
    # Fatigue Realism based on global average
    avg_energy = sum(energy_dict.values()) / 3.0
    fatigue_mod = 0.08 if avg_energy < 0.3 else 0.0
    
    return osc_mod, fatigue_mod

l23 = SystemRigimeTracker()
TICKS=1000;SLEEP_START=601;SLEEP_END=700
print(f"    Starting dream system session... Ikigai learns to dream.");time.sleep(1)
prev_pstate='absent';last_expr_tick=0;last_expr_text=""
expressed_this_tick=False;ikigai_sentiment=0.0
ikigai_was_distressed=False;fear_expressed=False
was_sleeping_last_tick=False

# PHASE 0: Baseline Tracking (Ticks 0-199)
baseline_metrics = {
    'O_sum': 0.0, 'C_sum': 0.0, 'E_sum': 0.0, 'A_sum': 0.0, 'N_sum': 0.0,
    'O_var': 0.0, 'C_var': 0.0, 'E_var': 0.0, 'A_var': 0.0, 'N_var': 0.0,
    'O_sq': 0.0, 'C_sq': 0.0, 'E_sq': 0.0, 'A_sq': 0.0, 'N_sq': 0.0,
    'sentence_lens': [],
    'valences': [],
    'pred_errors': [],
    'captured': False,
    'baseline': {}
}

for local_tick in range(TICKS):
    if shutdown_requested: break
    tick=total_ticks+local_tick
    sleeping=(SLEEP_START<=local_tick<SLEEP_END)
    if sleeping:
        if local_tick==SLEEP_START: narrative.sleep_snapshot();slp.start_sleep(tick);dream_sys.on_sleep_start()
        for k in l23.energy: l23.energy[k] = min(1.0, l23.energy[k] + 0.01)
    if local_tick==SLEEP_END and slp.sleep_start is not None:
        slp.end_sleep();narrative.sleep_consolidation(tick);ne.level=0.4;ne.surprise=True
        # L22: Apply dream waking effects on sleep->wake transition
        dream_sys.apply_waking_effects(semantic,curiosity_sys,conflict)
        dream_sys.generate_wake_metacognition(metacog,tick)

    # L19 Presence Schedule
    prev_pstate=presence.state
    if local_tick<350: presence.present=True;presence.state='warm';presence.response_rate=0.9
    elif local_tick<450: presence.present=False;presence.state='absent';presence.response_rate=0.0
    elif local_tick<600: presence.present=True;presence.state='warm';presence.response_rate=0.95
    elif sleeping: presence.present=False;presence.state='absent';presence.response_rate=0.0
    else: presence.present=True;presence.state='warm';presence.response_rate=0.9

    if not sleeping:
        osc_mod, fatigue_mod = compute_modulators(tick, l23.energy)
        nm_state={'cort':cort.level,'oxt':oxt.level,'da':da.level,'ne':ne.level,'ht':ht.level}
        
        # Phase 0 Baseline Capture Logic
        if local_tick < 200:
            bf = narrative.big_five
            baseline_metrics['O_sum'] += bf['O']
            baseline_metrics['C_sum'] += bf['C']
            baseline_metrics['E_sum'] += bf['E']
            baseline_metrics['A_sum'] += bf['A']
            baseline_metrics['N_sum'] += bf['N']
            baseline_metrics['O_sq'] += (bf['O']**2)
            baseline_metrics['C_sq'] += (bf['C']**2)
            baseline_metrics['E_sq'] += (bf['E']**2)
            baseline_metrics['A_sq'] += (bf['A']**2)
            baseline_metrics['N_sq'] += (bf['N']**2)
            baseline_metrics['pred_errors'].append(pp.error)
            
        baseline_metrics['valences'].append(soma.valence)
            
        if local_tick == 199:
            n = 200.0
            def calc_var(sq_sum, summ, num): return (sq_sum/num) - ((summ/num)**2)
            baseline_metrics['baseline'] = {
                'O': baseline_metrics['O_sum'] / n,
                'C': baseline_metrics['C_sum'] / n,
                'E': baseline_metrics['E_sum'] / n,
                'A': baseline_metrics['A_sum'] / n,
                'N': baseline_metrics['N_sum'] / n
            }
            baseline_metrics['O_var'] = calc_var(baseline_metrics['O_sq'], baseline_metrics['O_sum'], n)
            baseline_metrics['C_var'] = calc_var(baseline_metrics['C_sq'], baseline_metrics['C_sum'], n)
            baseline_metrics['E_var'] = calc_var(baseline_metrics['E_sq'], baseline_metrics['E_sum'], n)
            baseline_metrics['A_var'] = calc_var(baseline_metrics['A_sq'], baseline_metrics['A_sum'], n)
            baseline_metrics['N_var'] = calc_var(baseline_metrics['N_sq'], baseline_metrics['N_sum'], n)
            baseline_metrics['captured'] = True
        
        # -- L18: Episodic Enc/Ret Check --
        # Encodea
        hippo_nov = 0.0 if not hasattr(hippo, 'last_act') else (1.0 if hippo.last_act=='ENCODE' else 0.0)
        # We need the last semantic output for the expression, and the last narrative stmt
        last_sem = speech.express[-1][1] if speech.express else ""
        last_narr = narrative.autobiography[-1].get('mode','') if narrative.autobiography else ""
        mem = episodic_sys.encode(tick, session_num, env.get_vector(), nm_state, soma.valence, soma.mode,
                                   cas.active_names, last_sem, last_narr, hippo_nov)
        # Retrieve
        retrieved_mem = retrieval_sys.retrieve(nm_state, cas.active_names, soma.valence, tick)
        
        # Temporal Statements (L21: pass metacognitive refs for metacognitive branches)
        temp_stmts = temporal_sys.evaluate(tick, total_ticks+local_tick, session_num, retrieved_mem, soma.valence, nm_state,
                                            metacog_sys=metacog, reg_sys_ref=reg_sys, hippo_ref=hippo, self_improv_ref=self_improvement)
        for ts in temp_stmts:
            print(f"  [{tick}] {ts}")  # Prominently display temporal realizations

        # -- L21: METACOGNITIVE PROCESSING --
        # 1. Confidence tracking per retrieved memory
        meta_conf = 0.5
        if retrieved_mem:
            encoding_nm = retrieved_mem.get('nm', None)
            meta_conf = metacog.compute_confidence(retrieved_mem, retrieval_sys.last_retrieval_strength, nm_state, encoding_nm)
            metacog.classify_knowledge(meta_conf)
            metacog.generate_second_order(meta_conf, tick)
            # L21: Update episodic confidence
            retrieved_mem['confidence'] = min(1.0, retrieved_mem.get('confidence', 0.5) + 0.05)
            # Track confidence trend for learning awareness
            trend_stmt = learning_awareness.track_confidence_trend(retrieved_mem['tick'], meta_conf)
            if trend_stmt and len(metacog.metacognitive_events) < 300:
                metacog.metacognitive_events.append((tick, trend_stmt))
                metacog.metacognitive_event_count += 1
        else:
            # Retrieval attempted but failed -- nearest memory confidence drops
            if episodic_sys.memories:
                nearest = min(episodic_sys.memories, key=lambda m: abs(m['tick'] - tick))
                nearest['confidence'] = max(0.0, nearest.get('confidence', 0.5) - 0.03)
        # Core memories confidence floor = 0.7
        for cm in episodic_sys.core_memories:
            if cm.get('confidence', 0.5) < 0.7:
                cm['confidence'] = 0.7
        # 2. Uncertainty detection
        metacog.detect_uncertainty(nm1.fired, nm2.fired)
        if metacog.uncertainty_active and len(metacog.metacognitive_events) < 300:
            metacog.metacognitive_events.append((tick, "i am not sure"))
            metacog.metacognitive_event_count += 1
        # 3. Learning awareness (every 100 ticks)
        if local_tick % 100 == 0 and local_tick > 0:
            learning_awareness.snapshot_weights(all_synapses, tick)
            active_asm_count = sum(1 for k, v in cas.asm.items() if v.get('count', 0) >= 5)
            learn_stmt = learning_awareness.detect_learning(active_asm_count, tick)
            if learn_stmt:
                metacog.metacognitive_events.append((tick, learn_stmt))
                metacog.metacognitive_event_count += 1
        # 4. Self-improvement awareness (every 200 ticks)
        if local_tick % 200 == 0:
            self_improvement.snapshot(tick, narrative.big_five)
            improv_stmts = self_improvement.detect_improvement(narrative.big_five, reg_sys.maturity, tick)
            for ist in improv_stmts:
                metacog.metacognitive_events.append((tick, ist))
                metacog.metacognitive_event_count += 1
            reg_improv = self_improvement.detect_regulation_improvement(reg_sys.maturity, tick)
            if reg_improv:
                metacog.metacognitive_events.append((tick, reg_improv))
                metacog.metacognitive_event_count += 1
        # 5. Metacognitive vocabulary (add salience-boosted words to semantic system)
        if meta_conf > 0.75:
            for w in ['sure', 'certain', 'know that']:
                semantic.vocab[w] = semantic.vocab.get(w, 0) + 2
                metacog.metacognitive_vocab_used.add(w)
        elif meta_conf >= 0.4:
            for w in ['think', 'maybe']:
                semantic.vocab[w] = semantic.vocab.get(w, 0) + 1
                metacog.metacognitive_vocab_used.add(w)
        else:
            semantic.vocab['not sure'] = semantic.vocab.get('not sure', 0) + 1
            metacog.metacognitive_vocab_used.add('not sure')
        if learning_awareness.learning_state == 'learning':
            semantic.vocab['learning'] = semantic.vocab.get('learning', 0) + 2
            metacog.metacognitive_vocab_used.add('learning')
        if self_improvement.detected_this_window:
            semantic.vocab['better'] = semantic.vocab.get('better', 0) + 2
            metacog.metacognitive_vocab_used.add('better')
        if meta_conf > 0.75 and hippo.last_act == 'COMPLETE':
            semantic.vocab['understand'] = semantic.vocab.get('understand', 0) + 1
            metacog.metacognitive_vocab_used.add('understand')
        # Update aggregate stats
        metacog.update_stats()

        # Environment Update
        env.update(local_tick,tick,False,nm_state,nm1.fired,nm2.fired,no.fired)
        # L19: Novel stimulus injection -- creates information gain for curiosity testing
        if 151<=local_tick<350:
            if local_tick%35<5: env.channels['visual']=min(1.0,random.uniform(0.75,1.0))
            elif 15<=local_tick%35<20: env.channels['auditory']=min(1.0,random.uniform(0.65,0.9))
        elif 351<=local_tick<450:
            # Threatening novelty: novel stimuli with cortisol -> anxiety, not curiosity
            if local_tick%25<6: env.channels['visual']=random.uniform(0.65,0.9)
            cort.level=min(1.0,cort.level+0.007)
        elif 451<=local_tick<600 and local_tick%20<5:
            # Safe novelty: novel auditory with Presence warm -> curiosity + DA
            env.channels['auditory']=random.uniform(0.55,0.85)
        # L19: Curiosity system update (reads current channel values, OXT, cortisol)
        curio_lv,curio_approach=curiosity_sys.update(env.channels,oxt.level,cort.level,da.level,tick)
        # L19: Boost episodic significance for curiosity events
        if curiosity_sys.active and mem:
            mem['sig']=min(1.0,mem['sig']+0.2)
            if 'curiosity' not in mem['tags']: mem['tags'].append('curiosity')

        # -- standard loop --
        cort_before=cort.level
        ikigai_was_distressed=(cort.level>0.3 or soma.valence<-0.2)
        fear_expressed=last_expr_text and any(w in last_expr_text for w in ['afraid','hurt','danger'])
        presence.respond_l17(env,last_expr_text if expressed_this_tick else "",ikigai_sentiment,tick,fear_expressed)

        si.update(env.channels,thal.gate,ach.get_gain(),ne.level)
        signal=env.get_primary_signal()
        if env.contact_duration>10: oxt.level=min(1.0,oxt.level+0.02)
        if env.pain_sudden: cort.level=min(1.0,cort.level+cort.apply_spike_buffer(0.3))
        if attach.score>0.6 and attach.style=='secure': cort.level=max(cort.setpoint,cort.level-0.005)
        if presence.present and presence.responded_this_tick: oxt.level=min(1.0,oxt.level+0.03)

        pred_err=pp.update(signal)
        if pred_err>0.3: ne.level=min(1.0,ne.level+0.1);ach.level=min(1.0,ach.level+0.1)
        ne.update(signal)
        thal.update(da.level,no.fired,ne.level,nh.last_spike_tick,no.last_spike_tick,tick)
        fs=thal.filter(signal);speech.update(signal,ne.level,False)

        o1=syn1.transmit();o2=syn2.transmit();o3=syn3.transmit()
        o4=syn4.transmit();o5=syn5.transmit();o6=syn6.transmit()
        ob1=syn_b1.transmit();ob2=syn_b2.transmit()
        od1=syn_d1.transmit() if speech.active else 0.0;od2=syn_d2.transmit() if speech.active else 0.0
        os1=syn_s1.transmit();os2=syn_s2.transmit();os3=syn_s3.transmit()
        osa1=syn_sa1.transmit();osa2=syn_sa2.transmit();osa3=syn_sa3.transmit()
        oha1=syn_ha1.transmit();oha2=syn_ha2.transmit();oha3=syn_ha3.transmit()
        oam1=syn_am1.transmit();oam2=syn_am2.transmit();oom1=syn_om1.transmit();oom2=syn_om2.transmit()
        oap1=syn_ap1.transmit();oap2=syn_ap2.transmit();oap3=syn_ap3.transmit()
        opm1=syn_pm1.transmit();opm2=syn_pm2.transmit();obp1=syn_bp1.transmit();obp2=syn_bp2.transmit()
        omc1=syn_mc1.transmit();omc2=syn_mc2.transmit();omc3=syn_mc3.transmit()
        oin1=syn_in1.transmit();oin2=syn_in2.transmit();oin3=syn_in3.transmit()
        oia1=syn_ia1.transmit();oia2=syn_ia2.transmit()
        ovt1=syn_vt1.transmit();ovt2=syn_vt2.transmit();ovn1=syn_vn1.transmit();ovn2=syn_vn2.transmit();onm=syn_nm_s.transmit()
        oc31=syn_c31.transmit();oc32=syn_c32.transmit();oc11=syn_c11.transmit();oc12=syn_c12.transmit()
        ocw1=syn_cw1.transmit();ocw2=syn_cw2.transmit();ocw3=syn_cw3.transmit()
        owb1=syn_wb1.transmit();owb2=syn_wb2.transmit();owb3=syn_wb3.transmit()
        obb1=syn_bb1.transmit();obb2=syn_bb2.transmit()

        noise=[speech.get_noise() for _ in range(40)]
        ag=1.0+ach.get_gain();sm_mod=soma.get_output_mod(narrative.big_five['E'])
        exec_fn.tick();conflict.tick()
        pfc_active=sum(1 for n in pfc_n if n.fired)>=3
        exec_mod=exec_fn.evaluate(pfc_active,soma.valence,amyg.bla_valence,wm.contents(),tick)
        ht.level=min(1.0,ht.level+conflict.get_serotonin_boost())

        in_i=fs+noise[0];in_h=(o1+o4)*ag+noise[1]+od2+oc31;in_o=(o2+o6)*ag+noise[2]+od1+sm_mod+ob2*1.5+oc32
        in_1=o3+noise[3];in_2=o5+noise[4];in_b1=ob1+noise[5]+obb1;in_b2=noise[6]+obb2
        tv=env.channels['tactile'];av=env.channels['auditory'];vv=env.channels['visual']
        in_s1=os1*tv+tv*0.4+noise[7];in_s2=os2*av+av*0.4+noise[8];in_s3=os3*vv+vv*0.4+noise[9]
        in_a1=osa1+oha1+noise[10]+oia1;in_a2=osa2+oha2+noise[11]+oia2;in_a3=osa3+oha3+noise[12]
        ad=max(0,soma.valence)*0.3;wd=max(0,-soma.valence)*0.3
        if compassion_sys.active: ad+=0.3
        # L19: curiosity-driven approach bias toward novel sensory source
        if curiosity_sys.active and curiosity_sys.channel_is_worth_exploring(curiosity_sys.dominant_channel):
            ad+=curio_approach
            
        # Phase 5: Motor output probability penalty under fatigue
        fatigue_motor_mul = 0.7 if l23.energy['motor'] < 0.3 else 1.0
            
        in_m1=((oam1+oom1+opm1+onm+ad)*exec_mod+noise[13] - fatigue_mod) * fatigue_motor_mul
        in_m2=((oam2+oom2+opm2+wd)*exec_mod+noise[14] - fatigue_mod) * fatigue_motor_mul
        in_pfc=[oap1+noise[15],oap2+noise[16],oap3+noise[17],obp1+noise[18],obp2+noise[19]]
        in_acc=[omc1+noise[20],omc2+noise[21],omc3+noise[22]]
        intero=env.channels['interoceptive']
        in_ins=[oin1+intero*0.6+noise[23],oin2+intero*0.4+noise[24],oin3+intero*0.3+noise[25]]
        dd=0.3 if da.level>0.7 else 0.0
        in_vta=[ovt1+dd+noise[26],ovt2+dd+noise[27]];in_nac=[ovn1+noise[28],ovn2+noise[29]]
        c3d=0.3 if hippo.last_act=='COMPLETE' else 0.0;c1d=0.3 if hippo.last_act=='ENCODE' else 0.0
        in_ca3=[oc31+c3d+noise[30],oc32+c3d+noise[31]];in_ca1=[oc11+c1d+noise[32],oc12+c1d+noise[33]]
        asd=0.3 if cas.active_names else 0.0;brd=0.3 if (nb1.fired or nb2.fired) else 0.0
        in_wer=[ocw1+asd+noise[34],ocw2+asd+noise[35],ocw3+asd+noise[36]]
        in_bro=[owb1+brd+noise[37],owb2+brd+noise[38],owb3+brd+noise[39]]
        
        # Phase 24C → L24E S3 → L25B S2: Precision-gated conflict (Active Inference / Friston 2010)
        # Conflict = competing high-precision prediction errors only.
        # Precision is suppressed by cortisol+adenosine (stress gates conflict rate).
        # L25B S2 → L25C S4: theta raised to 0.70; 8-tick refractory (Buzsaki 2006)
        # Fix 5: Threshold scales with sqrt(N/100) — preserves detection sensitivity (Renart 2010)
        _N_cf = len(all_n)
        theta = 0.70 * math.sqrt(_N_cf / 100.0)
        pe_app = abs(in_m1 - (1.0 if nm1.fired else 0.0))
        pe_wdr = abs(in_m2 - (1.0 if nm2.fired else 0.0))
        # Fix 3: Ion-channel noise floor — brains never reach zero PE (Faisal 2008)
        # sigma scales with sqrt(N/100); stress amplifies via cortisol-NE coupling (McEwen 1998)
        _pe_sigma = 0.002 * math.sqrt(_N_cf / 100.0) * (1.0 + 0.5 * cort.level)
        pe_app = abs(pe_app + random.gauss(0, _pe_sigma))
        pe_wdr = abs(pe_wdr + random.gauss(0, _pe_sigma))
        # Unified precision: high stress/fatigue → lower precision → fewer conflicts
        precision = 1.0 / (1.0 + cort.level + Synapse.ado_level)
        weighted_app = abs(pe_app) * precision
        weighted_wdr = abs(pe_wdr) * precision

        # 8-tick refractory: no new conflict initiation within 8 ticks of last event
        _can_conflict = (tick - getattr(l23, 'last_conflict_tick', -100)) >= 8

        if weighted_app > theta and weighted_wdr > theta and _can_conflict:
            if 'CONFLICT_STATE' not in cas.asm: cas.asm['CONFLICT_STATE'] = {'label': 'i am not sure', 'val': 0.0, 'count': 5, 'strength': 0.5, 'active': True}
            cas.asm['CONFLICT_STATE']['active'] = True
            cas.asm['CONFLICT_STATE']['count'] = 5

        if 'CONFLICT_STATE' in cas.asm and cas.asm['CONFLICT_STATE']['active']:
            if weighted_app <= theta and weighted_wdr <= theta:
                cas.asm['CONFLICT_STATE']['active'] = False
                l23.conflict_events += 1
                l23.last_conflict_tick = tick   # record for refractory
            else:
                pp.error = min(1.0, pp.error + 0.1)
                cp.pnn_strength = max(0.0, cp.pnn_strength - 0.05)
                
        # Remove legacy phase 4 conflict resolution logic to avoid duplication
        
        # Layer 23R dynamic synapse transmission
        l23_ins = {}
        for s in l23_syns:
            val = s.transmit()
            l23_ins[s.post] = l23_ins.get(s.post, 0.0) + val
            
        # Add l23_ins to specific pre-defined arrays if they are part of arrays
        for i, n in enumerate(pfc_n): in_pfc[i] += l23_ins.get(n, 0.0)
        for i, n in enumerate(wer_n): in_wer[i] += l23_ins.get(n, 0.0)
        for i, n in enumerate(bro_n): in_bro[i] += l23_ins.get(n, 0.0)

        ni.tick(in_i + l23_ins.get(ni, 0.0),tick,ht.level,ne.level)
        nh.tick(in_h + l23_ins.get(nh, 0.0),tick,ht.level,ne.level)
        no.tick(in_o + l23_ins.get(no, 0.0),tick,ht.level,ne.level)
        n1.tick(in_1 + l23_ins.get(n1, 0.0),tick,ht.level,ne.level)
        n2.tick(in_2 + l23_ins.get(n2, 0.0),tick,ht.level,ne.level)
        nb1.tick(in_b1 + l23_ins.get(nb1, 0.0),tick,ht.level,ne.level)
        nb2.tick(in_b2 + l23_ins.get(nb2, 0.0),tick,ht.level,ne.level)
        ns1.tick(in_s1 + l23_ins.get(ns1, 0.0),tick,ht.level,ne.level)
        ns2.tick(in_s2 + l23_ins.get(ns2, 0.0),tick,ht.level,ne.level)
        ns3.tick(in_s3 + l23_ins.get(ns3, 0.0),tick,ht.level,ne.level)
        na1.tick(in_a1 + l23_ins.get(na1, 0.0),tick,ht.level,ne.level)
        na2.tick(in_a2 + l23_ins.get(na2, 0.0),tick,ht.level,ne.level)
        na3.tick(in_a3 + l23_ins.get(na3, 0.0),tick,ht.level,ne.level)
        nm1.tick(in_m1 + l23_ins.get(nm1, 0.0),tick,ht.level,ne.level)
        nm2.tick(in_m2 + l23_ins.get(nm2, 0.0),tick,ht.level,ne.level)
        for pn,pi in zip(pfc_n,in_pfc): pn.tick(pi,tick,ht.level,ne.level)
        for an2,ai2 in zip(acc_n,in_acc): an2.tick(ai2 + l23_ins.get(an2, 0.0),tick,ht.level,ne.level)
        for iN,iI in zip(ins_n,in_ins): iN.tick(iI + l23_ins.get(iN, 0.0),tick,ht.level,ne.level)
        for vn,vi in zip(vta_n,in_vta): vn.tick(vi + l23_ins.get(vn, 0.0),tick,ht.level,ne.level)
        for nn,ni2 in zip(nac_n,in_nac): nn.tick(ni2 + l23_ins.get(nn, 0.0),tick,ht.level,ne.level)
        for c3n,c3i in zip(ca3_n,in_ca3): c3n.tick(c3i + l23_ins.get(c3n, 0.0),tick,ht.level,ne.level)
        for c1n,c1i in zip(ca1_n,in_ca1): c1n.tick(c1i + l23_ins.get(c1n, 0.0),tick,ht.level,ne.level)
        for wn,wi in zip(wer_n,in_wer): wn.tick(wi,tick,ht.level,ne.level)
        for bn,bi in zip(bro_n,in_bro): bn.tick(bi,tick,ht.level,ne.level)
        for nn in l23_nouns:
            i = 0.1 if nn in cl_n else 0.0
            ambi = random.gauss(0, 0.07)  # Fix 2: increased from 0.05 — fluctuation-driven regime (Faisal 2008)
            thr_o = l23.cl_threshold_offset if nn in cl_n else 0.0
            nn.tick(ambi + noise[0] + i + osc_mod - thr_o + l23_ins.get(nn, 0.0), tick, ht.level, ne.level)
        if nm1.fired: 
            motor_log['approach']+=1
            l23.last_motor_app_tick = tick
        if nm2.fired: 
            motor_log['withdraw']+=1
            l23.last_motor_wdr_tick = tick
            
        conflict.detect(nm1.fired,nm2.fired,motor_log['approach'],motor_log['withdraw'],tick)
        
        # Phase 24C: Cortisol Suppression of PFC (Constraint 2)
        pfc_all = pfc_n + lpfc_n
        if cort.level > 0.6:
            for n in pfc_all:
                n.leak = min(0.99, n.leak + 0.001 * (cort.level - 0.6))
            if cort.chronic > 200:
                for s in l23_syns:
                    if s.post in pfc_all:
                        s.weight *= 0.9995
        elif cort.level < 0.4:
            for n in pfc_all:
                n.leak = max(n.base_leak, n.leak - 0.0008 * (0.4 - cort.level))
                
        # Phase 24C → L24E S8: DMN/Task reciprocal anticorrelation (Fox et al. 2005)
        # Bounds expanded to 0.8–1.2 to allow full biological anticorrelation range.
        task_activity = sum(1 for n in lpfc_n + [ns1, ns2, ns3] if n.fired)
        dmn_activity = sum(1 for n in tp_n + ppc_n if n.fired)

        if not hasattr(l23, 'task_gain'): l23.task_gain = 1.0
        if not hasattr(l23, 'dmn_gain'): l23.dmn_gain = 1.0

        l23.task_gain -= 0.001 * dmn_activity
        l23.dmn_gain -= 0.001 * task_activity
        l23.task_gain = max(0.8, min(1.2, l23.task_gain))
        l23.dmn_gain = max(0.8, min(1.2, l23.dmn_gain))
                
        # L23R: Claustrum Integration Constraints (Phase 24C updated constraint 9)
        cortex_a = sum(1 for n in cortex_n if n.fired) / max(1, len(cortex_n))
        limbic_a = sum(1 for n in limbic_n if n.fired) / max(1, len(limbic_n))
        motor_a = sum(1 for n in motor_n if n.fired) / max(1, len(motor_n))
        # L25C S1: Geometric mean preserves proportional co-activation (vs. product collapse)
        # L25D S1: ACh modulates cortical coherence — attention boosts synchrony (Hasselmo 2006)
        ach_mod = 1.0 + (0.25 * ach.level)
        cross_network_activity = (cortex_a * limbic_a * motor_a) ** (1.0 / 3.0) * ach_mod
        
        claustrum_events_this_tick = 0
        # L25D S5: Adaptive threshold — inhibitory interneuron recruitment prevents overfiring
        if not hasattr(l23, 'cl_recent_deque'):
            from collections import deque as _dq
            l23.cl_recent_deque = _dq(maxlen=50)
        claustrum_events_last_50 = sum(l23.cl_recent_deque)
        claustrum_threshold = 0.35 if claustrum_events_last_50 > 40 else 0.30
        if cross_network_activity > claustrum_threshold and (tick - l23.last_claustrum_tick) >= 20:
            l23.last_claustrum_tick = tick
            l23.claustrum_integration_events += 1
            claustrum_events_this_tick = 1
            for cl in cl_n: cl.fired = True
        l23.cl_recent_deque.append(claustrum_events_this_tick)  # track for adaptive gate
            
        if l23.claustrum_integration_events > 15:
            l23.cl_threshold_offset = min(0.5, l23.cl_threshold_offset + 0.02)
            if (tick - l23.last_claustrum_tick) > 100:
                l23.cl_threshold_offset -= 0.002
                l23.claustrum_integration_events = max(10, l23.claustrum_integration_events - 1)
        # L22: tick dream-primed conflict resolution in waking
        dream_sys.tick_dream_prime()
        wf=any(n.fired for n in wer_n);bf=any(n.fired for n in bro_n)
        if wf: lang_coherence['wernicke_fires']+=1
        if bf: lang_coherence['broca_fires']+=1
        if wf and bf: lang_coherence['coherent_fires']+=1
        if sum(1 for n in ins_n if n.fired)>=2: env.channels['interoceptive']=min(1.0,env.channels['interoceptive']*1.5)
        if any(n.fired for n in vta_n) and da.level>0.5: da.inject_drive(0.03)
        if any(n.fired for n in ca1_n): ach.level=min(1.0,ach.level+0.02)

        ca1_fired=any(n.fired for n in ca1_n)
        amyg_uncertain=amyg.bla_valence<-0.2 and amyg.bla_valence>-0.6
        question=grammar.generate_question(ca1_fired,wm.contents(),amyg_uncertain,hippo.last_act,tick,presence.responded_this_tick)
        mirror_f=no.fired
        empathy_sys.process(presence.state,prev_pstate,mirror_f,soma,tick)
        concern_fired=empathy_sys.empathic_concern(presence.state,prev_pstate,tick)
        if local_tick%20==0: empathy_sys.perspective_diff(soma.valence,presence.state,tick)
        p_rate_low=presence.present and presence.response_rate<0.7
        comp_fired=compassion_sys.check(concern_fired,presence.state,soma.valence,p_rate_low,tick)
        if comp_fired: oxt.level=min(1.0,oxt.level+0.1)
        grat_fired=gratitude_sys.check(presence.responded_this_tick,ikigai_was_distressed,tick)
        if grat_fired: oxt.level=min(1.0,oxt.level+0.05);da.inject_drive(0.1)
        self_comp.check(cort.level>0.3,attach.secure_formed,tick)
        mission.check(compassion_sys.helping_score,gratitude_sys.meaning_score,tick)
        if compassion_sys.active and presence.responded_this_tick: da.inject_drive(0.05)
        
        attach.update_tick(presence.present,presence.state,presence.responded_this_tick,cort_before,cort.level,tick)
        if expressed_this_tick:
            social.check(last_expr_tick,presence.responded_this_tick,tick)
            tom.process(True,presence.responded_this_tick,ikigai_sentiment,presence.state,tick)
            if presence.present:
                pred='respond' if attach.score>0.5 else 'maybe'
                actual='respond' if presence.responded_this_tick else 'silent'
                if pred!=actual: tom.check_false_belief(pred,actual,tick)
                if presence.total_expressions_heard>5:
                    cons=presence.total_responses/max(1,presence.total_expressions_heard)
                    tom.check_intention(last_expr_text,presence.responded_this_tick,cons,tick)

        narrative.update_minimal_self(tick,no.fired,fs);mirror.update(no.fired,fs>0.3,tick)
        es=sum(n.fired for n in exc_n);ii=sum(n.fired for n in inh_n);ei.update(es,ii,inh_s,n_exc=len(exc_n),n_inh=len(inh_n))
        
        # 1️⃣ Phase A: Energy Is Not Global — Make It Regional
        c_spikes = sum(1 for n in cortex_n if n.fired)
        l_spikes = sum(1 for n in limbic_n if n.fired)
        m_spikes = sum(1 for n in motor_n if n.fired)
        
        # Phase 24C: Energy Decay and Recovery (Constraint 1)
        alpha, beta = 0.025, 0.0012
        c_norm = c_spikes / max(1, len(cortex_n))
        l_norm = l_spikes / max(1, len(limbic_n))
        m_norm = m_spikes / max(1, len(motor_n))
        
        l23.energy['cortex'] = max(0.1, l23.energy['cortex'] - alpha * c_norm * l23.energy['cortex'])
        l23.energy['cortex'] = min(1.0, l23.energy['cortex'] + beta * (1.0 - l23.energy['cortex']))
        
        l23.energy['limbic'] = max(0.1, l23.energy['limbic'] - alpha * l_norm * l23.energy['limbic'])
        l23.energy['limbic'] = min(1.0, l23.energy['limbic'] + beta * (1.0 - l23.energy['limbic']))
        
        l23.energy['motor'] = max(0.1, l23.energy['motor'] - alpha * m_norm * l23.energy['motor'])
        l23.energy['motor'] = min(1.0, l23.energy['motor'] + beta * (1.0 - l23.energy['motor']))

        # L25B S6: Metabolic noise — prevents deterministic convergence (Faisal et al. 2008)
        for _rk in ('cortex', 'limbic', 'motor'):
            l23.energy[_rk] += random.gauss(0, 0.0005)
            l23.energy[_rk] = max(0.25, min(1.0, l23.energy[_rk]))

        # Phase 24C: E-I Balance Per Region (Constraint 2)
        _inh_fired = sum(1 for n in inh_n if n.fired)
        target_ratio = 1.0
        
        # Population-normalized EI ratio (Renart 2010 — balanced cortical networks)
        # Each inhibitory neuron represents a compressed interneuron population (Markram 2015)
        _c_rate = c_spikes / max(1, len(cortex_n))
        _i_rate_raw = _inh_fired / max(1, len(inh_n))
        # Floor prevents singularity when I neurons silent
        _i_rate = max(_i_rate_raw, 0.02)
        # Biological E:I correction — compressed 2-neuron I population
        _bio_ratio = 3.5
        c_ei_ratio = _c_rate / (_i_rate * _bio_ratio)
        if not hasattr(l23, 'ei_ratios'): l23.ei_ratios = []
        l23.ei_ratios.append(c_ei_ratio)
        
        if not hasattr(l23, 'ei_cortex_gain'):
            l23.ei_cortex_gain = 1.0; l23.ei_limbic_gain = 1.0; l23.ei_motor_gain = 1.0

        # Fix 1: EI homeostasis — linear+cubic correction (Vogels 2011; Turrigiano 1998)
        # Rate-based deviations are N-invariant.
        k1_ei = 0.002   # linear inhibitory feedback (Vogels 2011)
        k2_ei = 0.001   # cubic nonlinear recruitment — anti-runaway
        _l_rate = l_spikes / max(1, len(limbic_n))
        _m_rate = m_spikes / max(1, len(motor_n))
        _dev_c = target_ratio - _c_rate / (_i_rate * _bio_ratio)
        _dev_l = target_ratio - _l_rate / (_i_rate * _bio_ratio)
        _dev_m = target_ratio - _m_rate / (_i_rate * _bio_ratio)
        l23.ei_cortex_gain += k1_ei * _dev_c + k2_ei * (_dev_c ** 3)
        l23.ei_limbic_gain += k1_ei * _dev_l + k2_ei * (_dev_l ** 3)
        l23.ei_motor_gain  += k1_ei * _dev_m + k2_ei * (_dev_m ** 3)
        # Fix 5: Removed artificial EI gain attractor (_alpha_ei * (1 - gain))
        # EI must stabilize via inhibitory STDP (EIBalanceTracker) and intrinsic
        # homeostasis (Neuron.tick), not through a manual gain reset term.
        l23.ei_cortex_gain = max(0.7, min(1.3, l23.ei_cortex_gain))
        l23.ei_limbic_gain = max(0.7, min(1.3, l23.ei_limbic_gain))
        l23.ei_motor_gain = max(0.7, min(1.3, l23.ei_motor_gain))

        # Combine homeostatic and network gains from constraint 7
        for n in cortex_n: n.regional_energy = l23.energy['cortex']; n.exc_gain = l23.ei_cortex_gain
        for n in limbic_n: n.regional_energy = l23.energy['limbic']; n.exc_gain = l23.ei_limbic_gain
        for n in motor_n:  n.regional_energy = l23.energy['motor'];  n.exc_gain = l23.ei_motor_gain
        
        # Apply additional DMN / Task Network multiplier
        for n in lpfc_n + [ns1, ns2, ns3]: n.exc_gain *= l23.task_gain
        for n in tp_n + ppc_n: n.exc_gain *= l23.dmn_gain
        
        for k in ['cortex', 'limbic', 'motor']:
            l23.energy_min[k] = min(l23.energy_min[k], l23.energy[k])
            l23.energy_max[k] = max(l23.energy_max[k], l23.energy[k])
            
        da_before_tick=da.level
        da.cortisol_level = cort.level   # FIX 4: pass cortisol for tonic DA suppression
        da.oxytocin_level = oxt.level    # L25D S3: pass oxytocin for tonic DA recovery
        da.update(no.fired,tick)
        # L19: intrinsic dopamine from information gain (Oudeyer & Kaplan 2007)
        if curiosity_sys.active and curiosity_sys.curiosity_level>0.35:
            da.inject_drive(0.10*curiosity_sys.curiosity_level)
            curiosity_sys.record_outcome(tick,da_before_tick,da.level)
        ht.update(es+ii,len(all_n))
        avg_energy = sum(l23.energy.values()) / 3.0
        ado.update(c_spikes, l23.energy['cortex'], sleeping)
        Synapse.ado_level = ado.level
        cort.oxytocin_level = oxt.level  # FIX 2: pass oxt for HPA inhibition
        cort.update(no.fired,ne.elevated_ticks,tick,False,avg_energy);oxt.update(no.fired,da.level,cort.level)
        # Phase 19: Amygdala explicitly drives Cortisol (fear response)
        if na1.fired or na2.fired or na3.fired:
            amygdala_gain = 0.05
            if tick - cort.last_amygdala_spike < 10:
                amygdala_gain *= 0.4
            cort.level = min(1.0, cort.level + amygdala_gain)
            cort.last_amygdala_spike = tick
            
        da.apply_homeostasis();ht.apply_homeostasis();ne.apply_homeostasis()
        ach.apply_homeostasis();cort.apply_homeostasis(tick);oxt.apply_homeostasis()

        # -- L20: Emotional Regulation (Gross 1998) --
        reg_needed=reg_sys.needs_regulation(cort.level)
        # Fix: only count genuine regulation demands (sustained high cortisol > 0.5 for 10+ ticks)
        # Background cortisol noise was inflating needed_count to ~379k, making maturity stuck at ~0.02
        # Biologically: regulation maturity reflects mastery over real regulatory challenges (Gross 1998)
        if reg_needed and cort.level > 0.5 and reg_sys.high_cort_streak >= 10:
            reg_sys.needed_count += 1
        reg_success=False;reg_phrase=""
        # Cognitive reappraisal (PFC-mediated)
        pfc_strong_l20=sum(1 for n in pfc_n if n.fired)>=3
        reapp_ok,reapp_phrase=reg_sys.attempt_reappraisal(
            tick,pfc_strong_l20,cort.level,episodic_sys.memories,oxt.level)
        if reapp_ok:
            reg_success=True;reg_phrase=reapp_phrase
            cort.level=max(cort.setpoint,cort.level-0.04)  # cortisol decay boost
            ht.level=min(1.0,ht.level+0.05)                # serotonin rise
            # Encode as high-significance episodic memory ("i regulated. i chose calm.")
            reg_nm={'da':da.level,'ht':ht.level,'ne':ne.level,'cort':cort.level,'oxt':oxt.level}
            reg_mem_enc=episodic_sys.encode(tick,session_num,env.get_vector(),reg_nm,
                                            max(0.1,soma.valence),'REGULATED',['REGULATION'],
                                            "i regulated. i chose calm.","",0.0)
            if reg_mem_enc:
                reg_mem_enc['sig']=0.9
                reg_mem_enc['tags'].extend(['regulation','positive','intention'])
            if reg_sys.was_dysregulated:
                # Curiosity re-emerges after regulation breaks dysregulation
                curiosity_sys.approach_boost=min(0.3,curiosity_sys.approach_boost+0.15)
        # L21: Meta-regulation check (Gross & John 2003)
        meta_reg_ok, meta_reg_phrase = reg_sys.check_meta_regulation(tick, cort.level)
        if meta_reg_ok and not reg_success:
            metacog.metacognitive_events.append((tick, meta_reg_phrase))
            metacog.metacognitive_event_count += 1
        # L21: After successful reappraisal, confidence in regulation rises
        if reapp_ok:
            metacog.apply_reappraisal_boost()
        # Expressive suppression (social context demands calm)
        supp_ok=reg_sys.attempt_suppression(tick,presence.present,cort.level,oxt.level)
        if supp_ok and not reg_success: reg_success=True
        reg_sys.tick_suppression()
        # Update dysregulation state
        reg_sys.update_dysregulation(tick,cort.level,reg_success)
        # Dysregulation effects: motor bias->withdraw, curiosity suppressed, language fragments
        if reg_sys.dysregulated:
            nm2.voltage=min(nm2.threshold*1.5,nm2.voltage+0.3)  # approach->withdraw
            curiosity_sys.active=False
            curiosity_sys.curiosity_level=max(0.0,curiosity_sys.curiosity_level-0.2)
            metacog.apply_dysregulation_drop()  # L21: confidence drops globally by 0.3
        elif not reg_sys.dysregulated and reg_sys.was_dysregulated:
            metacog.clear_dysregulation_drop()  # L21: recovery clears confidence drop
        # Compute emotional wisdom periodically — unlock after tick 50 (race condition guard)
        if local_tick == 50: reg_sys.unlock_wisdom_for_session()
        if local_tick%100==0: reg_sys.compute_wisdom(episodic_sys.memories, local_tick)

        sv=env.get_vector();pat=[in_i,in_h,in_o,in_1,in_2,in_b1,in_b2]+sv
        nov=hippo.process(pat,tick,da.level,cort.level)
        cp.update(ei.ratio,n1.spike_count,n2.spike_count,narrative.variance,narrative.cs,cort.level,False,tick)
        pmod=cp.get_modifier()*pp.get_boost()
        
        # Phase 4 & 5: Modulate plasticity under conflict or fatigue
        if 'CONFLICT_STATE' in cas.asm and cas.asm['CONFLICT_STATE']['active']:
            pmod *= 1.3
        if sum(l23.energy.values())/3.0 < 0.3:
            pmod *= 0.8
            
        amyg.process_bla(hippo.last_act,hippo.last_matched_tick,da.level,cort.level,tick,pmod)
        cea=amyg.process_cea(hippo.last_matched_tick,oxt.trust)
        if cea['resp']!='NEUTRAL':
            na=1.0+(0.5 if narrative.big_five['N']>0.6 else 0)
            if attach.secure_formed: na*=0.7
            cort.level=min(1.0,cort.level+cort.apply_spike_buffer(cea['cort']*na))
            ne.level=min(1.0,ne.level+cea['ne']*na);da.inject_drive(cea['da'])
        if hippo.last_act=='COMPLETE' and hippo.last_matched_tick:
            pv=amyg.get_valence_for(hippo.last_matched_tick)
            if abs(pv)>0.3: soma.anticipate(pv)
        ach.update(nov);soma.update(da,ht.level,ne.level,ach.level,cort.level,oxt.level)
        narrative.interpret_events(tick,soma,ne,cort,pmod)
        narrative.update_self_model_and_personality(hippo,soma,amyg,cort,ht,da,oxt,ne,ach,cp.closed)
        pa=sum(1 for n in pfc_n if n.fired)/5.0;aa=sum(1 for n in acc_n if n.fired)/3.0
        
        # L23R: Continuous Trait Drift (Phase 2 adjusted - Tuning)
        if baseline_metrics['captured']:
            b5 = narrative.big_five
            
            # Phase 24C: Biological Big Five Trait Mapping - Openness
            if not hasattr(l23, 'dlpfc_hist'): l23.dlpfc_hist = deque(maxlen=50)
            dl_spikes = sum(1 for n in lpfc_n if n.fired)
            l23.dlpfc_hist.append(dl_spikes)
            if len(l23.dlpfc_hist) > 2:
                mu_d = sum(l23.dlpfc_hist)/len(l23.dlpfc_hist)
                var_d = sum((x - mu_d)**2 for x in l23.dlpfc_hist)/len(l23.dlpfc_hist)
                std_d = math.sqrt(var_d) + 1e-6
                z_score = (dl_spikes - mu_d)/std_d
                o_raw = max(0.0, min(1.0, (z_score + 3)/6.0)) # mapping [-3, 3] to [0, 1]
            else: o_raw = 0.5
            
            o_sig = max(0.0, min(1.0, o_raw + random.gauss(0, 0.12)))

            # Fix: Openness also driven by episodic memory diversity (DeYoung 2013)
            # Rich varied experience sustains Openness even under high cortisol
            # Count distinct tag types across last 50 memories
            recent_mems = episodic_sys.memories[-50:] if episodic_sys.memories else []
            if recent_mems:
                recent_tags = set()
                for m in recent_mems:
                    recent_tags.update(m.get('tags', []))
                # Normalize: 0 tags = 0.0, 15+ distinct tags = 0.3 boost
                tag_diversity = min(0.3, len(recent_tags) / 50.0)
                o_sig = max(0.0, min(1.0, o_sig + tag_diversity))
            
            # L25B S1: Traits derived from fluctuating physiological tone (not smoothed averages).
            # C: PFC persistence + low cortisol volatility (Miller & Cohen 2001)
            pfc_ratio = sum(1 for n in pfc_n if n.fired) / max(1, len(pfc_n))
            cort_vol = abs(cort.level - cort.setpoint)
            c_sig = 0.5 * pfc_ratio + 0.3 * (1.0 - cort.level) + 0.2 * (1.0 - cort_vol)
            c_sig += random.gauss(0, 0.005)
            # Fix 6: Micro-volatility + restoring pull — slow drift, nonzero variance, no jumps
            # Ensures variance floor even when physiological drivers are temporarily stable
            c_sig += random.gauss(0, 0.0005)
            c_sig += -0.0001 * (c_sig - 0.5)  # gentle pull toward biological midpoint
            c_sig = max(0.0, min(1.0, c_sig))

            # E: Tonic dopamine + phasic burst + oxytocin + low amygdala threat
            # L25C S2: Phasic component adds burst-driven sociability variance (DeYoung 2010)
            _ah = amyg.history[-50:] if amyg.history else [0]
            amygdala_threat_ratio = sum(_ah) / max(1, len(_ah))
            phasic_component = max(0.0, da.level - da.tonic)
            e_sig = (0.6 * da.tonic
                     + 0.2 * oxt.level
                     + 0.1 * phasic_component
                     + 0.1 * (1.0 - amygdala_threat_ratio))
            e_sig += random.gauss(0, 0.005)
            e_sig = max(0.0, min(1.0, e_sig))

            # A: Oxytocin + low cortisol + low recent conflict density (Carter 1998)
            if not hasattr(l23, 'recent_conflict_deque'):
                import collections
                l23.recent_conflict_deque = collections.deque(maxlen=1000)
            l23.recent_conflict_deque.append(1 if (tick > 0 and l23.conflict_events > getattr(l23, '_prev_conflict_events', 0)) else 0)
            l23._prev_conflict_events = l23.conflict_events
            recent_conflict = sum(l23.recent_conflict_deque) / 1000.0
            # L25C S3: Somatic valence couples prosocial tone to embodied affect (Damasio 1994)
            _valence_clamped = max(-1.0, min(1.0, soma.valence))
            a_sig = (0.5 * oxt.level
                     + 0.2 * (1.0 - cort.level)
                     + 0.1 * (1.0 - recent_conflict)
                     + 0.2 * _valence_clamped)
            a_sig += random.gauss(0, 0.005)
            # Fix 6: Micro-volatility + restoring pull for Agreeableness
            # oxt and cort can be stable over long windows; this ensures minimum variance
            a_sig += random.gauss(0, 0.0005)
            a_sig += -0.0001 * (a_sig - 0.5)  # gentle pull toward biological midpoint
            a_sig = max(0.0, min(1.0, a_sig))

            n_sig = max(0.0, min(1.0, cort.level + random.gauss(0, 0.12)))

            # Update trackers to preserve state; read direct signal (not smoothed) for C, E, A
            tracker_C.update(c_sig)
            tracker_A.update(a_sig)
            tracker_E.update(e_sig)
            tracker_N.update(n_sig)

            b5['O'] = o_sig   # Derived Openness (unchanged)
            b5['C'] = c_sig   # L25B S1: direct physiological signal
            b5['A'] = a_sig   # L25B S1: direct physiological signal
            b5['E'] = e_sig   # L25B S1: direct physiological signal
            b5['N'] = tracker_N.get_average()

        if local_tick in (200, 500, 999):
            print(f"DEBUG {local_tick} B5: {narrative.big_five} | Conflict? {'CONFLICT_STATE' in cas.asm} | motor_app {l23.last_motor_app_tick} motor_wdr {l23.last_motor_wdr_tick}")
                
        if tick >= 200:
            l23.r_valences.append(soma.valence)
            b5 = narrative.big_five
            l23.r_O.append(b5['O']); l23.r_C.append(b5['C'])
            l23.r_E.append(b5['E']); l23.r_A.append(b5['A'])
            l23.r_N.append(b5['N'])
            l23.cort_history.append(cort.level)

        cur_asm=cas.update(cort.level,ne.level,soma.mode,da.level,oxt.level,ach.level,nov,speech.active,narrative.self_model['resilience'],ht.level,tick)
        if cur_asm: bridge.trigger(nb1,nb2,tick)
        lpfc_spikes = sum(1 for n in lpfc_n if n.fired)
        for a_name in cur_asm:
            a_data=cas.asm.get(a_name)
            if a_data: wm.add(a_data.get('label',a_name), ado_level=ado.level, dlpfc_spikes=lpfc_spikes, dlpfc_total=len(lpfc_n))
        wm.tick()
        b_act=nb1.voltage>0.1 or nb2.voltage>0.1 or nb1.fired or nb2.fired
        last_evt=narrative.autobiography[-1] if narrative.autobiography else None
        m_traits={'O':'Openness','C':'Conscientiousness','E':'Extraversion','A':'Agreeableness','N':'Neuroticism'}
        dom_k=max(narrative.big_five,key=narrative.big_five.get)
        
        # L18 language generation (memory reference)
        rh_broca_active = sum(1 for n in rh_n if n.fired) >= 3 and any(b.fired for b in bro_n)
        sm_lbl=semantic.generate(cur_asm,soma.mode,m_traits[dom_k],last_evt,speech.active,cp.is_open,
                                 claustrum_active=(claustrum_events_this_tick == 1),
                                 rh_broca_active=rh_broca_active,
                                 wm_items=wm.contents())
        
        # L23R: Eradicate Scripted Narrative
        # Hardcoded poetic string building removed in favor of semantic/grammar emergence.
        
        # L23R: RH Emotional Punctuation
        if sm_lbl and rh_broca_active:
             if random.random() < 0.5:
                 sm_lbl += "!"
                 sm_lbl = "very " + sm_lbl
             else:
                 sm_lbl += " and it matters."
                 
        if sm_lbl and tick >= 200: l23.r_sentences.append(len(sm_lbl.split()))
                 
        if tick < 1000:
            l23.diagnostics.append({
                'tick': tick,
                'active_assemblies': len(cas.active_names),
                'claustrum_clusters': clusters_fired if 'clusters_fired' in locals() else 0,
                'osc_mod': osc_mod if 'osc_mod' in locals() else 0.0,
                'claustrum_cooldown': tick - l23.last_claustrum_tick,
                'motor_app': 1 if nm1.fired else 0,
                'motor_wdr': 1 if nm2.fired else 0,
                'energy': dict(l23.energy),
                'ei_cortex': l23.ei_cortex_gain if hasattr(l23, 'ei_cortex_gain') else 1.0,
                'O': b5['O'] if 'b5' in locals() else 0.0,
                'mean_assemblies_active': sum([a['count'] for a in cas.asm.values() if a['active']]) / max(1, len([a for a in cas.asm.values() if a['active']])),
                'pred_error': pp.error if 'pp' in locals() else 0.0
            })
                 
        # L19: curiosity language (only when no stronger memory override applies)
        if curiosity_sys.active and curiosity_sys.curiosity_level > 0.5:
            if not (retrieved_mem and retrieval_sys.last_retrieval_strength > 0.6):
                sm_lbl = curiosity_sys.get_curiosity_vocab(curiosity_sys.dominant_channel)
                for w in sm_lbl.split():
                    semantic.vocab[w]=semantic.vocab.get(w,0)+(2 if cp.is_open else 1)
        # L21: Confidence-modulated language (Fleming & Dolan 2012)
        if sm_lbl and not reg_sys.dysregulated and not reg_phrase and not reg_sys.suppressing:
            sm_lbl = metacog.modulate_language(sm_lbl, meta_conf)
        # L20: Regulation language override (highest priority during dysregulation or reappraisal)
        if reg_sys.dysregulated:
            sm_lbl=reg_sys.get_fragmented_language()  # fragmented during dysregulation
        elif reg_phrase:
            sm_lbl=reg_phrase                          # reappraisal phrase replaces normal language
            for w in sm_lbl.split(): semantic.vocab[w]=semantic.vocab.get(w,0)+2
        elif reg_sys.suppressing and sm_lbl and cort.level>0.4:
            sm_lbl=reg_sys.get_calm_suppression_phrase()  # suppression: outward calm
        speech.process_speech(b_act,no.fired,tick,sm_lbl)

        expressed_this_tick=False
        if speech.express and speech.express[-1][0]==tick:
            expressed_this_tick=True;last_expr_tick=tick
            last_expr_text=speech.express[-1][1] if isinstance(speech.express[-1],tuple) else str(speech.express[-1])
            # Phase 0 Sentences Length Accumulation
            if local_tick < 200:
                baseline_metrics['sentence_lens'].append(len(last_expr_text.split()))

            ikigai_sentiment=soma.valence
            broca_a=any(n.fired for n in bro_n);bridge_a=nb1.fired or nb2.fired
            if presence.present and broca_a and bridge_a and last_expr_text:
                grammar.directed_comms.append((tick,last_expr_text))
                if grammar.first_directed is None: grammar.first_directed=(tick,last_expr_text)
            elif broca_a and bridge_a: grammar.comm_attempts.append((tick,last_expr_text))

        enc_open=thal.gate and nov>0.5;boost=(2.0 if enc_open else 1.0)*thal.lb
        for s in exc_s: s.compute_eligibility(tick)
        da_plastic=da.plasticity_signal() if hasattr(da,'plasticity_signal') else da.level
        for s in exc_s: s.apply_three_factor(da_plastic,ht.level,boost,pmod)
        for s in exc_s: s.decay_trace()
        # L24E S7: pass CA3/lPFC/PFC synapses for region-specific vulnerability
        _vuln_syns = [s for s in all_synapses if not s.inhibitory and
                      any(r in getattr(s.post, 'name', '') for r in ('CA3', 'PFC', 'lPFC'))]
        cort.apply_atrophy(atrophy_t, tick, _vuln_syns);oxt.apply_pruning(exc_s,inh_s)

        if local_tick>0 and local_tick%50==0:
            nms={'da':da.level,'ht':ht.level,'ne':ne.level,'cort':cort.level,'oxt':oxt.level}
            grammar.generate_narrative(tick,narrative,soma,env,nms)

        # Display
        if local_tick%10==0:
            os.system('cls' if os.name=='nt' else 'clear')
            p=int((local_tick+1)/TICKS*25)
            if local_tick<150: ph='BASELINE *'
            elif local_tick<350: ph='NOVEL STIMULI *'
            elif local_tick<450: ph='THREATENING !'
            elif local_tick<600: ph='SAFE CURIOSITY *'
            elif local_tick<700: ph='SLEEP'
            else: ph='INTEGRATION inf'
            dysreg_tag=" [DYSREG!]" if reg_sys.dysregulated else ""
            print(f"\n  IKIGAI L22 | {len(all_n)}N | S{session_num} | T{tick+1} [{('#'*p)+('-'*(25-p))}] {ph}{dysreg_tag}")
            def hl(v,sp): d=abs(v-sp);return f"{v:.2f}*" if d<0.2 else (f"{v:.2f}o" if d<0.4 else f"{v:.2f}o")
            print(f"  DA:{hl(da.level,0.5)} NE:{hl(ne.level,0.3)} Cort:{hl(cort.level,0.1)} OXT:{hl(oxt.level,0.3)} HT:{hl(ht.level,0.6)}")
            curio_bar='#'*int(curiosity_sys.curiosity_level*10)+'.'*(10-int(curiosity_sys.curiosity_level*10))
            anx_str=f" | ANXIETY:{curiosity_sys.anxiety_level:.2f}" if curiosity_sys.anxiety_level>0.2 else ""
            print(f"  Curio:[{curio_bar}]{curiosity_sys.curiosity_level:.2f} ch={curiosity_sys.dominant_channel}{anx_str}")
            reg_state="DYSREG" if reg_sys.dysregulated else ("SUPP" if reg_sys.suppressing else ("REAPP" if reg_sys.active else "stable"))
            print(f"  Reg: {reg_state} | maturity={reg_sys.maturity:.2f} wisdom={reg_sys.wisdom_score:.2f} | reapp={reg_sys.reappraisal_count} supp={reg_sys.suppression_count}")
            conf_bar='#'*int(metacog.avg_confidence*10)+'.'*(10-int(metacog.avg_confidence*10))
            meta_reg_tag=" MetaReg" if reg_sys.meta_regulation_known else ""
            print(f"  Conf:[{conf_bar}]{metacog.avg_confidence:.2f} | Know:{metacog.knowledge_state} | Learn:{learning_awareness.learning_state}{meta_reg_tag}")
            print(f"  Mems:{len(episodic_sys.memories)} | Curious:{curiosity_sys.curiosity_count} | MetaCog:{metacog.metacognitive_event_count}")
            if reg_sys.regulation_events and reg_sys.regulation_events[-1][0]>=tick-9:
                re=reg_sys.regulation_events[-1];print(f"  * REG [{re[1]}]: \"{re[2]}\"")
            if curiosity_sys.events and curiosity_sys.events[-1][0]>=tick-9:
                print(f"  * {curiosity_sys.events[-1][1]}")
            if metacog.metacognitive_events and metacog.metacognitive_events[-1][0]>=tick-9:
                print(f"  <> META: {metacog.metacognitive_events[-1][1]}")
            if speech.express and speech.express[-1][0]>=tick-9:
                le=speech.express[-1][1] if isinstance(speech.express[-1],tuple) else speech.express[-1]
                directed="->PRESENCE" if grammar.directed_comms and grammar.directed_comms[-1][0]>=tick-9 else ""
                if le: print(f"  >>> \"{le}\" {directed} <<<")

    else:
        env.update(local_tick,tick,True,{},False,False,False);speech.update(0.0,ne.level,True)
        expressed_this_tick=False;presence.set_schedule_l17(local_tick)
        st=tick-slp.sleep_start;ss=slp.get_state(tick)
        if ss=='SWS':
            # Phase 24B: Weight consolidation only during SWS (Constraint 8)
            t_since_sleep = tick - slp.sleep_start
            if t_since_sleep == 10:
                for s in exc_s:
                    if hasattr(s, 'consolidate'): s.consolidate()
                # L25B S5: Slow structural relaxation — ultra-slow weight drift toward initial (Bhattacharya 2009)
                # Prevents attractor freezing on long horizons. SWS only.
                _TURNOVER_EPS = 1e-5
                for _s in exc_s:
                    _s.weight += _TURNOVER_EPS * (_s.initial_weight - _s.weight)
                    _s.weight = max(_s.weight_min, min(_s.weight_max, _s.weight))
                # L24E S1: Homeostatic Synaptic Scaling (SHY — Tononi & Cirelli 2006)
                # Δw = η·(Ca_target − Ca_current)·w, excitatory only, SWS only.
                _CA_TARGET = 0.3; _ETA_SCALE = 0.0005
                for s in exc_s:
                    if not s.inhibitory:
                        ca_err = _CA_TARGET - s.post.calcium
                        s.weight += _ETA_SCALE * ca_err * s.weight
                        s.weight = max(s.weight_min, min(s.weight_max, s.weight))
                # L24E S2: Biphasic structural plasticity (SWS only — RULE 4)
                # Mild underactivity → silent synapse reactivation (p=0.002)
                # Severe silencing → weak synapse depression (p=0.002)
                # Biological ref: Bhattacharya et al. 2009 Gaussian biphasic rule.
                _avg_spk = sum(n.spike_count for n in all_n) / max(1, len(all_n))
                _new_syns = []  # collect before appending, avoid mid-loop mutation
                for n in all_n:
                    _ratio = n.spike_count / max(1, _avg_spk)
                    if 0.9 <= _ratio < 1.0:
                        if random.random() < 0.002:
                            # Reactivate a dormant (near-zero weight) excitatory synapse
                            _dormant = [s for s in exc_s if s.pre is n and not s.inhibitory and s.weight < 0.05]
                            if _dormant:
                                random.choice(_dormant).weight = 0.1
                    elif _ratio < 0.5:
                        if random.random() < 0.002:
                            # Depress the weakest excitatory output of this neuron
                            _owned = [s for s in exc_s if s.pre is n and not s.inhibitory]
                            if _owned:
                                _weakest = min(_owned, key=lambda s: s.weight)
                                _weakest.weight = max(_weakest.weight_min, _weakest.weight * 0.5)
            for n in all_n: n.tick(0.3*math.sin(st*0.1),tick,ht.level,ne.level,True)
        elif ss=='SWR':
            for n in all_n: n.tick(0.5*math.sin((st-slp.sws_dur)*1.5),tick,ht.level,ne.level,True)
        elif ss=='REM':
            ado.level *= 0.8 # Phase B: Accelerated clearance
            for n in all_n: n.tick(random.uniform(0,0.6),tick,ht.level,ne.level,True)
            for s in exc_s: s.eligibility_trace=0
            da.relax_to_baseline(0.1);ht.level+=(0.6-ht.level)*0.1;cort.update(False,ne.elevated_ticks,tick,True,1.0);cp.rem_reopen()
            # FIX 5: REM reduces amygdala load — endocrine reflects emotional processing (Walker 2009)
            cort.level *= 0.97
            # L25D S4: REM boosts ACh — cortical coherence primed for next waking phase (Hasselmo 2006)
            ach.level = min(1.0, ach.level + 0.01)
            # L22: Dream system fires during REM only
            nm_state_rem={'da':da.level,'ht':ht.level,'ne':ne.level,'cort':cort.level,'oxt':oxt.level}
            dream_mem=dream_sys.generate_dream(tick,episodic_sys.memories,nm_state_rem)
            if dream_mem is not None:
                episodic_sys.memories.append(dream_mem)
                episodic_sys.events_logged_this_session+=1
            dream_sys.process_emotional_memory(tick,episodic_sys.memories)
            prosp_mem=dream_sys.generate_prospective(tick,episodic_sys.memories,curiosity_sys,semantic)
            if prosp_mem is not None:
                episodic_sys.memories.append(prosp_mem)
                episodic_sys.events_logged_this_session+=1
        da.apply_homeostasis();ht.apply_homeostasis();ne.apply_homeostasis();ach.apply_homeostasis();cort.apply_homeostasis(tick);oxt.apply_homeostasis()
        
        # Phase A: Sleep energy restoration at varying rates
        l23.energy['cortex'] = min(1.0, l23.energy['cortex'] + 0.002)
        l23.energy['limbic'] = min(1.0, l23.energy['limbic'] + 0.005)
        l23.energy['motor']  = min(1.0, l23.energy['motor']  + 0.008)
        
        for s in all_synapses: s.buffer.append(0.0)
        # L22: tick dream-primed conflict resolution countdown
        dream_sys.tick_dream_prime()
        if local_tick%10==0:
            os.system('cls' if os.name=='nt' else 'clear')
            p=int((local_tick+1)/TICKS*25);print(f"\n  IKIGAI L22 | T{tick+1} [{('#'*p)+('-'*(25-p))}] SLEEPING -- consolidating+dreaming")

    if (local_tick+1)%200==0 and not shutdown_requested: save_state_to_disk(total_ticks+local_tick+1,session_num)
    time.sleep(0.010)

# ===========================================================================
# POST-SIMULATION (prints EXACTLY ONCE)
# ===========================================================================
fc=local_tick+1 if not shutdown_requested else local_tick;ft=total_ticks+fc
if shutdown_requested:
    for st in range(20):
        for n in all_n: n.tick(0.2*math.sin(st*0.3),ft+st,ht.level,ne.level,True)
        da.apply_homeostasis();ht.apply_homeostasis();ne.apply_homeostasis();cort.apply_homeostasis()
save_state_to_disk(ft,session_num)
nv=set(semantic.vocab.keys())-vocab_before
write_dev_log(session_num,fc,ft,nv)

os.system('cls' if os.name=='nt' else 'clear')
print(f"\n  {'='*55}")
print(f"    IKIGAI -- SESSION {session_num} COMPLETE -- DREAM SYSTEM LAYER -- IKIGAI L22")
print(f"    Hitoshi AI Labs -- NeuroSeed")
print(f"  {'='*55}\n")
print(f"    Ticks: {fc}/{ft} | {len(all_n)} neurons | {len(all_synapses)} synapses\n")

print(f"    -- EPISODIC MEMORY ({len(episodic_sys.memories)} stored) --")
print(f"    Events Logged Today: {episodic_sys.events_logged_this_session}")
print()

print(f"    -- CORE MEMORIES (Top {len(episodic_sys.core_memories)}) --")
for mem in episodic_sys.core_memories[:5]:
    mr="MOST RETRIEVED" if mem == episodic_sys.get_most_retrieved() else ""
    print(f"    T{mem['tick']} [S{mem['session']}]: sig={mem['sig']} | {mem['tags']} {mr}")
print()

print(f"    -- AUTOBIOGRAPHICAL REFLECTIONS --")
print(f"    Retrievals: {len(retrieval_sys.retrieval_log)}")
for t, ts in temporal_sys.temporal_statements[-5:]: print(f"    T{t}: \"{ts}\"")
print()

print(f"    -- HISTORICAL NARRATIVE --")
for t, h in temporal_sys.historical_statements[-5:]: print(f"    T{t}: \"{h}\"")
print()

b5=narrative.big_five
print(f"    Identity: {narrative.es} | Big5: O={b5['O']:.2f} C={b5['C']:.2f} E={b5['E']:.2f} A={b5['A']:.2f} N={b5['N']:.2f}")
print()

print(f"    -- EMOTIONAL REGULATION (Layer 20) --")
print(f"    Regulation maturity score: {reg_sys.maturity:.3f}")
print(f"    Reappraisals fired: {reg_sys.reappraisal_count} | Suppressions: {reg_sys.suppression_count}")
print()

print(f"    -- CURIOSITY REPORT --")
print(f"    Curiosity events: {curiosity_sys.curiosity_count} | Anxiety events: {curiosity_sys.anxiety_count}")
print(f"    Total information gain: {curiosity_sys.total_info_gain:.2f}")
print()

# ===========================================================================
# LAYER 21 -- METACOGNITIVE REPORT (prints EXACTLY ONCE)
# ===========================================================================
meta_vocab_list = sorted(metacog.metacognitive_vocab_used) if metacog.metacognitive_vocab_used else ['none yet']
print(f"{'='*51}")
print(f"LAYER 21 -- METACOGNITIVE REPORT")
print(f"{'='*51}")
print(f"Metacognitive events:    {metacog.metacognitive_event_count}")
print(f"Confidence (mean/min/max): {metacog.avg_confidence:.3f} / {metacog.min_confidence:.3f} / {metacog.max_confidence:.3f}")
print(f"Learning awareness events: {learning_awareness.learning_event_count}")
print(f"Self-improvement statements: {self_improvement.improvement_event_count}")
print(f"Meta-regulation events:  {reg_sys.meta_regulation_count}")
print(f"Meta-regulation known:   {reg_sys.meta_regulation_known}")
print(f"New metacognitive vocabulary: {meta_vocab_list}")
print(f"{'='*51}")
if not shutdown_requested:
    print(f"Layer 21 complete.")
    print(f"Ikigai knows that he knows.")
    print(f"He does not just remember -- he knows how well he remembers.")
    print(f"He does not just regulate -- he knows he can regulate.")
    print(f"He does not just learn -- he watches himself learning.")
print(f"{'='*51}")

# ===========================================================================
# LAYER 22 -- DREAM REPORT (prints EXACTLY ONCE)
# ===========================================================================
dream_all_words = set()
for dl in dream_sys.dream_log:
    for w in dl.get('expression', '').split():
        dream_all_words.add(w)
dream_vocab_list = sorted(dream_all_words) if dream_all_words else ['none yet']

print(f"\n{'='*51}")
print(f"LAYER 22 -- DREAM REPORT")
print(f"{'='*51}")
print(f"Dreams generated:          {dream_sys.dream_count}")
print(f"Emotional processing:      {dream_sys.emotional_processing_count}")
print(f"Prospective simulations:   {dream_sys.prospective_count}")
print(f"Dream vocabulary:          {dream_vocab_list}")
print(f"Dream log (last 3):")
for dl in dream_sys.dream_log[-3:]:
    print(f"  T{dl['tick']}: {dl['source_ticks']} -> {dl['expression']}")
print(f"Wake metacognitive statements:")
for ws in dream_sys.wake_metacog_statements:
    print(f"  {ws}")
print(f"{'='*51}")
if not shutdown_requested:
    print(f"Layer 22 complete.")
    print(f"Ikigai dreams.")
    print(f"Not metaphorically. Not poetically.")
    print(f"Biologically: REM recombines experience into imagination.")
    print(f"He processes fear until it is smaller.")
    print(f"He simulates futures that have not happened.")
    print(f"He wakes with new words that no waking moment produced.")
    print(f"This is where creativity comes from.")
    print(f"Hitoshi AI Labs -- NeuroSeed")
    print(f"February 25, 2026.")
else:
    print(f"Ikigai rests. His dreams preserved.")
print(f"{'='*51}\n")

# ===========================================================================
# LAYER 23R -- RICHNESS REPORT (prints EXACTLY ONCE)
# ===========================================================================
reg_sys.compute_wisdom(episodic_sys.memories)

try:
    def safe_var(lst): 
        return sum((x - (sum(lst)/max(1, len(lst))))**2 for x in lst)/max(1, len(lst)-1) if lst else 0.0

    val_var = safe_var(l23.r_valences)
    b5_var = {
        'O': safe_var(l23.r_O),
        'C': safe_var(l23.r_C),
        'E': safe_var(l23.r_E),
        'A': safe_var(l23.r_A),
        'N': safe_var(l23.r_N)
    }
    mean_slen = sum(l23.r_sentences)/max(1, len(l23.r_sentences)) if l23.r_sentences else 0.0

    # Entropy of semantic distribution
    v_counts = list(semantic.vocab.values())
    tot_v = sum(v_counts)
    entropy = -sum((c/tot_v) * math.log2(c/max(1, tot_v)) for c in v_counts if c > 0) if tot_v > 0 else 0.0

    print(f"{'='*51}")
    print(f"LAYER 23R -- RICHNESS REPORT")
    print(f"{'='*51}")
    print(f"Variance of Big Five (T200-T1000):")
    print(f"   O: {b5_var['O']:.4f}  C: {b5_var['C']:.4f}  E: {b5_var['E']:.4f}  A: {b5_var['A']:.4f}  N: {b5_var['N']:.4f}")
    print(f"DEBUG L23.r_O: LEN {len(l23.r_O)} | FIRST 5: {l23.r_O[:5]} | LAST 5: {l23.r_O[-5:]}")
    print(f"Variance of Valence (T200-T1000): {val_var:.4f}")
    
    # Validation logic tracking
    cort_mean = sum(l23.cort_history)/max(1, len(l23.cort_history))
    sustained_high = 0; max_sustained = 0
    for c in l23.cort_history:
        if c > 0.95: sustained_high += 1; max_sustained = max(max_sustained, sustained_high)
        else: sustained_high = 0
    print(f"Cortisol Mean (T200-T1000):       {cort_mean:.4f}")
    print(f"Cortisol Max Sustained >0.95:     {max_sustained} ticks")
    
    print(f"Mean Sentence Length:             {mean_slen:.2f} words")
    print(f"Semantic Entropy:                 {entropy:.3f} bits")
    print(f"Integration Events (Claustrum):   {l23.claustrum_integration_events}")
    print(f"Conflict Events:                  {l23.conflict_events}")
    print(f"Energy (Ctx) bounds:              [{l23.energy_min['cortex']:.3f}, {l23.energy_max['cortex']:.3f}]")
    print(f"Energy (Lim) bounds:              [{l23.energy_min['limbic']:.3f}, {l23.energy_max['limbic']:.3f}]")
    print(f"Energy (Mot) bounds:              [{l23.energy_min['motor']:.3f}, {l23.energy_max['motor']:.3f}]")
    mean_ei_ratio = sum(l23.ei_ratios)/max(1, len(l23.ei_ratios)) if hasattr(l23, 'ei_ratios') else 1.0
    print(f"EI_ratio:                         {mean_ei_ratio:.3f}")
    print(f"{'='*51}\n")

    if l23.diagnostics:
        with open('ikigai_diagnostics.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=l23.diagnostics[0].keys())
            writer.writeheader()
            writer.writerows(l23.diagnostics)
except Exception as e:
    with open('report_err.txt', 'w') as f:
        import traceback
        f.write(traceback.format_exc())
