<div align="center">

# Lightning IB

<!--[![codecov](https://codecov.io/gh/JustinGoheen/lightning-pod/branch/main/graph/badge.svg)](https://codecov.io/gh/JustinGoheen/lightning-pod) -->

A Lightning AI Application for Interactive Brokers

</div>

## Overview

This repo is for basic regression (ordinary least squares, and logistic) problems given a set of training labels created by brute force optimization. The training labels are a binary set of position indicators formed from a dual moving average trend following system.

The heuristic used to determine the "best" dual moving average pair during brute force optimization is the cumulative returns of the pair being tested.

## Research Concept

Once the "best" pair is found, a logistic regression system is trained. The cumultive returns are also tested at each training iteration, and although the agent is allowed to train in a traditional gradient descent method, the thetas (bias-intercept and weights) will be selected based on which set provided the highest returns and not the final thetas that converged (or reached the max iterations). In this sense, the gradient descent method is more of a search method than it is a convergence method.

## Using the Machine Learning CLI

A basic command line interface `learner` has been provided. The CLI commands are shown below:

`learner teardown` will destroy any existing data splits, saved predictions, logs, profilers, checkpoints, and ONNX. <br>

`learner train` runs the Trainer. <br>

`learner bug-report` creates a bug report to [submit issues on GitHub](https://github.com/Lightning-AI/lightning/issues) for Lightning. the report is printed to screen in terminal, and generated as a markdown file for easy submission.

## Using the Trader CLI

A basic command line interface `trader` has been provided. The CLI commands are shown below:

`coming soon`