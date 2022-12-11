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
import sys
from pathlib import Path

import lightning as L

from lightning_ib.agents import LearningAgent, PipelineAgent, TradingAgent


class Agent(L.LightningFlow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.counter = 0
        self.pipeline = PipelineAgent()
        self.learner = LearningAgent()
        self.trader = TradingAgent()

    def run(self):

        # pipeline performs data acquisition, preprocessing, label generation with BFO
        self.pipeline.run()

        # the learner will learn a binary problem
        # the learner performs hpo with lightning-hpo
        # the learner logs with wandb
        self.learner.run()

        # once the learner is complete, start the trader
        # the trader is an ib_insync interface to the IBKR API
        self.trader.run()

        # stop the agent at first iteration
        sys.exit()


app = L.LightningApp(Agent())
