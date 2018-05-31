# Ball Beam System

## Ball Beam Environment Configuration

- a = 1
- r, theta = (1, 0.0564), (2, 0.1129), (3, 0.1698)
- b = 0.6
- G = 9.81

## Find Parameters of PID

- Execute: `python3 run_optimize.py [A] [R] [THETA]`
- Example: `python3 run_optimize.py 1 1 0.0564`

## Evaluate

1. Record the configuration to `result.csv`
2. Execute: `python3 evaluate.py`
3. Result will be `visualize/log/`

## Show the Curve

Execute all cells in `curve.ipynb`
