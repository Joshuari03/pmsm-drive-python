# PMSM Drive Simulation (FOC)

This project implements a Python-based simulation of a Permanent Magnet Synchronous Motor (PMSM) with field-oriented control (FOC) in the dq reference frame.

## Features

- PMSM electrical model in dq coordinates
- PI-based current control (id/iq loops)
- Modular architecture (model, control, simulation)
- Configurable reference profiles (constant, step)
- Basic visualization of current response

## Structure

```
models/ # motor and inverter models
control/ # PI controllers and FOC logic
simulation/ # simulation loop
utils/ # transformations and helpers
main.py # entry point
config.py # parameters
```

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate
pip install numpy scipy matplotlib
python main.py
```
## Notes
Simulation uses discrete-time integration (Euler)
Current control is implemented without decoupling (baseline version)
Designed as a foundation for further extensions (inverter, speed loop, etc.)
## Future Work
Decoupling feedforward terms
Mechanical dynamics (speed loop)
Inverter model and voltage saturation
Hardware integration (ESP32)
