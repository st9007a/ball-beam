# Ball Beam System

## Ball Beam Environment Configuration

- a = 1
- r, theta = (1, 0.0564), (2, 0.1129), (3, 0.1698)
- b = 0.6
- G = 9.81

## Find Parameters of PID

- Execute: `python3 run_optimize.py [A] [R] [THETA]`
- Example: `python3 run_optimize.py 1 1 0.0564`

## Simulation

1. Record the configuration to `result.csv`
2. Execute: `python3 evaluate.py`
3. Result will be `visualize/log/`
4. Open `visualize/index.html` with browser

## Show the Curve

1. Make sure `result.csv` exist
2. Execute all cells in `curve.ipynb`
