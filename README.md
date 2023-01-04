<div align="center">

# Lightning IB

<!--[![codecov](https://codecov.io/gh/JustinGoheen/lightning-pod/branch/main/graph/badge.svg)](https://codecov.io/gh/JustinGoheen/lightning-pod) -->

A Lightning AI Application for the Interactive Brokers TWS API

:warning: **FOR LOCAL USE ONLY. DO NOT RUN THIS IN LIGHTNING CLOUD** :warning:

</div>

## Disclaimer

The intent of this project is to create boilerplate for an [IBKR](https://www.interactivebrokers.com/en/home.php) trading application powered by [Lightning](https://lightning.ai); the intent does not include creating a profitable strategy. In other words, this project serves as a template for IBKR customers who are proficient enough in Python that they can take this template and build on it, using [ib_insync](https://lightning.ai) and the Lightning ecosystem.

By switching the TWS port from paper trading to live trading, then running and deploying this template in live trading, you assume full liability.

## Overview

The target market is any S&P 500 product: ES, MES, SPY, VOO etc. This project uses SPY. Additional ETFs are included in feature (factor) engineering to form a broader macro picture for the model.

The mock strategy is a basic logistic regression model trained on a binary (long only) set of labels created by brute force optimization. The training labels are position indicators formed from a dual moving average trend following system. The training features (factors) are normalized, expanding rank technical indicators. These indicators were chosen arbitrarily, without any empirical evidence of these indicators having any real predictive qualities. No effort is given to undertake feature selection based on importance or covariance.

The heuristic used to determine the "best" dual moving average pair during brute force optimization is the cumulative returns of the pair being tested.

[QuantStats](https://github.com/ranaroussi/quantstats) is used to collect strategy metrics.

## Usage

After forking and cloning the repo, do the following in terminal:

```bash
cd {{ path to clone }}
python3 -m venv .venv
#assumes mac or linux
source .venv/bin/activate
pip install -e ".[dev]"
```

then install the [SWIG version of TA-Lib](https://ta-lib.org/hdr_dw.html) with:

```bash
# for mac users with homebrew
brew install ta-lib
# for linux
bash scripts/install_talib.sh
```

then install the [Cython wrapper](https://mrjbq7.github.io/ta-lib/index.html) with:

```bash
pip install ta-lib
```

## Research Concept

Once the "best" pair is found via brute force optimization, a logistic regression system is trained. The cumulative returns are also collected at each training iteration, and although the agent is allowed to train in a traditional gradient descent method, the thetas (bias-intercept and weights) will be selected based on which set provided the highest returns and not the final thetas reached on convergence or after reaching a max iteration. In this sense, the gradient descent method is more of a search method than it is a optimization method.

## Using the Machine Learning CLI

A basic command line interface `learner` has been provided. The CLI commands are shown below:

`learner teardown` will destroy any existing data splits, saved predictions, logs, profilers, checkpoints, and ONNX. <br>

`learner train` runs the Trainer. <br>

`learner bug-report` creates a bug report to [submit issues on GitHub](https://github.com/Lightning-AI/lightning/issues) for Lightning. the report is printed to screen in terminal, and generated as a markdown file for easy submission.

## Using the Trader CLI

A basic command line interface `trader` has been provided. The CLI commands are shown below:

`coming soon`

## Running as a Lightning Application

Given each agent (or worker) is created as a seperate Python script or module, those modules can ran individually from the command line, or by using the main module `app.py` found in the project's root directory. A handy bash script has been provided in `scripts/`.

Running the Lightning application will:

- fetch using [yfinance](https://github.com/ranaroussi/yfinance)
- pre-process data with Pandas
- create and store a directory of data files in Apache parquet file format
- do feature (factor) engineering
- do brute force optimization to find a best dual moving average pair
- create labels given that pair
- create a LightningDataSet and LightningDataModule
- performs hyper parameter optimization with Lightning Training Studio
- trains the model to find a "best" set of weights
- takes an action based on the model's decision on today's input:
  - if trade signal is received: initiates a paper trading session with TWS using [IBC](https://github.com/IbcAlpha/IBC)
  - else: shuts down

> over and under fitting, and concept drift are not accounted for

To run the Lightning application, do the following in terminal:

```bash
bash scripts/run_app.sh
```

## Installation

A virtual environment can be created with Python's venv. The provided `setup.py` and `setup.cfg` will make creating this environment easy – just follow the instructions below after cloning the repo.

```sh
cd {{ path to clone }}
python3 -m venv .venv/
source .venv/bin/activate
pip install -e .
```

<details>
  <summary>Installing Extras</summary>

A set of dev and doc support extras have been provided. The optional extras can be viewed in `setup.cfg`.

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

</details>

Following completion of one of the above, test the install with the following in terminal:

```sh
learner --help
trader --help
```

both commands should show the help instructions if the install was successful.
