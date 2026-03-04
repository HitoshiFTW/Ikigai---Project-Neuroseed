# Ikigai — Project NeuroSeed

Biologically inspired neural simulation modeling excitation–inhibition balance, neuromodulators, and emergent cognitive traits.

---

## Overview

NeuroSeed is an experimental research project exploring how cognitive traits can emerge from interacting neural systems rather than being explicitly programmed.

The simulation models simplified brain dynamics including:

* cortical excitation–inhibition balance
* neuromodulator systems
* stress and hormonal regulation
* motor competition and decision conflict
* intrinsic plasticity and homeostasis

Instead of hardcoding behaviors, the system attempts to produce **emergent patterns** from biologically motivated mechanisms.

---

## Core File

```
ikigai.py
```

This file contains the entire simulation engine, including:

* neuron models
* synapse dynamics
* neuromodulator systems
* hormonal feedback loops
* plasticity mechanisms
* trait emergence calculations

The architecture intentionally stays in a single file to make the full system easier to inspect and experiment with.

---

## Research Logs

```
research_logs/
```

This folder contains development notes documenting:

* experimental changes
* simulation observations
* biological reasoning behind design choices
* test results and stability experiments

The logs serve as a running record of the research process.

---

## Key Systems Modeled

### Neural Dynamics

Neurons use a simplified leaky-integrator model with:

* threshold firing
* refractory periods
* calcium fatigue
* intrinsic homeostatic plasticity

---

### Excitation–Inhibition Balance

The network attempts to maintain stability through:

* inhibitory plasticity
* intrinsic neuron threshold adaptation
* population-scaled inhibitory influence

Inspired by:

* Vogels et al. (2011)
* Turrigiano (1998)

---

### Neuromodulators

The simulation includes simplified versions of several neuromodulatory systems:

| System         | Role                                |
| -------------- | ----------------------------------- |
| Dopamine       | reward and motivation               |
| Norepinephrine | arousal and gain control            |
| Acetylcholine  | cortical coordination               |
| Oxytocin       | social bonding and stress buffering |
| Cortisol       | stress and HPA-axis regulation      |

These systems interact to influence neural firing and behavioral dynamics.

---

### Motor Competition

Two motor pathways simulate approach and withdrawal behavior.

Lateral inhibition between them creates competition and occasional **conflict events**, similar to basal ganglia decision circuits.

---

### Trait Emergence

The simulation derives several behavioral traits from neural activity patterns rather than fixed parameters.

Traits evolve over time based on:

* reward dynamics
* stress levels
* cortical stability
* prediction error signals
* neuromodulator balance

---

## Purpose

NeuroSeed is an exploration into how biological principles can inform artificial neural systems.

The project investigates whether stable cognitive dynamics can emerge from relatively simple neural rules when multiple regulatory systems interact.

---

## Status

Research prototype.
The architecture is actively being refined and tested for biological plausibility and stability.

---

## License

MIT License
