# phys-fuzz-core

An adversarial framework for testing physical simulation engines. 

## Architecture
This project implements a multi-agent adversarial loop:
* **The Attacker:** An LLM-based auditor (using Qwen 2.5) that attempts to find inputs that force the engine into a failure (breach) state.
* **The Defender:** An internal, Rust-based logic controller that monitors internal engine pressure and throttles input parameters to prevent system failure.

## Components
* `src/lib.rs`: The `cavitation_engine` logic, containing the physics simulation and the Defender's throttle threshold (800.0 pressure units).
* `orchestrator/adversarial_agent.py`: The Python-based orchestrator that drives the interaction between the Attacker and the Engine.
* `logs/`: Telemetry files capturing Attacker attempts and Defender interventions.

## Setup
1. **Build the engine:**
   `maturin develop --release`
2. **Run the audit loop:**
   `python3 orchestrator/adversarial_agent.py`

## License
Cory Hodson - 2026
