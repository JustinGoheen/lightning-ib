# Copyright Justin R. Goheen.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from dataclasses import dataclass
from pathlib import Path

import lightning as L
import torch

from lightning_ib.workers import BruteWorker, LearningWorker, TradingWorker, DashWorker, PipelineWorker


class AppFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.lit_dash = DashWorker(parallel=True, cloud_compute=L.CloudCompute("default"))
        self.brute = BruteWorker(cloud_compute=L.CloudCompute("default"))
        self.learner = LearningWorker(cloud_compute=L.CloudCompute("default"))
        self.trader = TradingWorker(cloud_compute=L.CloudCompute("default"))
        self.pipeline = PipelineWorker(cloud_compute=L.CloudCompute("default"))

    def run(self):
        # start the dash app, it will receive input from each worker
        # as the workers complete their work
        self.lit_dash.run()
        # begin with the pipeline
        self.pipeline.run()
        # brute force optimizer
        # it should have some step to check for existing optimization
        # the optimization is stored in data/optimized_dma.json
        # or to begin a new optimization
        # the purpose of this optimization is to create a dual moving average pair
        # as labels for the learning agent, a logistic regression classifier
        self.brute.run()
        # the learning agent will receive a prompt from brute
        # the learner will learn a binary problem
        # the learner performs hpo with lightning-hpo
        # the learner logs with wandb
        self.learner.run()
        # once the learner is complete, start the trader
        # the trader is an ib_insync interface to the IBKR API
        self.trader.run()

    def configure_layout(self):
        # a tab is needed for brute
        # a tab is needed for learner
        # a tab is needed for wandb
        # a tab is needed for pyfolio
        ...


app = L.LightningApp(AppFlow())
