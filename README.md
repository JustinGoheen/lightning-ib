<div align="center">

# Lightning IB

<!--[![codecov](https://codecov.io/gh/JustinGoheen/lightning-pod/branch/main/graph/badge.svg)](https://codecov.io/gh/JustinGoheen/lightning-pod) -->

A Lightning AI Application for Interactive Brokers

</div>

## Overview

This repo is for basic logistic regression given a set of training labels created by brute force optimization. The training labels are a binary set of position indicators formed from a dual moving average trend following system.

The heuristic used to determine the "best" dual moving average pair during brute force optimization is the cumulative returns of the pair being tested.

## Research Concept

Once the "best" pair is found via brute force optimization, a logistic regression system is trained. The cumulative returns are also collected at each training iteration, and although the agent is allowed to train in a traditional gradient descent method, the thetas (bias-intercept and weights) will be selected based on which set provided the highest returns and not the final thetas reached on convergence or after reaching a max iteration. In this sense, the gradient descent method is more of a search method than it is a convergence method.

## Using the Machine Learning CLI

A basic command line interface `learner` has been provided. The CLI commands are shown below:

`learner teardown` will destroy any existing data splits, saved predictions, logs, profilers, checkpoints, and ONNX. <br>

`learner train` runs the Trainer. <br>

`learner bug-report` creates a bug report to [submit issues on GitHub](https://github.com/Lightning-AI/lightning/issues) for Lightning. the report is printed to screen in terminal, and generated as a markdown file for easy submission.

## Using the Trader CLI

A basic command line interface `trader` has been provided. The CLI commands are shown below:

`coming soon`

## Running as a Lightning Application

Given each agent (or worker) is created as a seperate Python script or module, those modules can also be used in Lightning App Agents or ran with Lightning App's `TracerPythonScript`.

## Installation

A virtual environment can be created with Python's venv. The provided `setup.py` and `setup.cfg` will make creating this environment easy – just follow the instructions below after cloning the repo.

```sh
cd {{ path to clone }}
python3 -m venv .venv/
source .venv/bin/activate
pip install -e .
```

A set off dev and doc support extras have been provided. The optional extras can be viewed in `setup.cfg`.

To install both sets of extras do the following in terminal:

```sh
cd {{ path to clone }}
python3 -m venv .venv/
source .venv/bin/activate
pip install -e ".[all]"
```

Or, to only install `dev` along with the required installs, do the following in terminal: 

```sh
cd {{ path to clone }}
python3 -m venv .venv/
source .venv/bin/activate
pip install -e ".[dev]"
```

Or, to only install `docs` along with the required installs, do the following in terminal: 

```sh
cd {{ path to clone }}
python3 -m venv .venv/
source .venv/bin/activate
pip install -e ".[docs]"
```

Following completion of one of the above, test the install with the following in terminal:

```sh
learner --help
trader --help
```

both commands should show the help instructions if the install was successful.
