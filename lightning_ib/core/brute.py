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
from datetime import datetime
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import quantstats as qs
from rich import print as rprint
from rich.progress import Progress

from lightning_ib.metrics.factors import log_returns, strategy_metrics

FILEPATH = Path(__file__)
PROJECTPATH = FILEPATH.parents[2]
SPYDATAPATH = os.path.join(PROJECTPATH, "data", "markets", "raw", "equities", "SPY.pq")
RESULTSPATH = os.path.join(PROJECTPATH, "logs", "bf_optimizer", "results.csv")
OPTIMIZEDDMAPATH = os.path.join(PROJECTPATH, "data", "optimized_dma.pq")


class BruteForceLearner:
    """optimizes for a dual moving average given a selection heuristic


    Note:
        see page 490 of Dr. yves Hilpicsh's Python for Finance second edition
    """

    def __init__(self):
        self.cagr = 0.05
        self.sharpe = 0.5
        self.max_drawdown = -0.3

        self.results = pd.DataFrame(columns=["Fast", "Slow", "CAGR", "Sharpe", "Drawdown", "Returns"])

        self.rawdata = pd.read_parquet(SPYDATAPATH, columns=["Close"])
        self.rawdata["returns"] = log_returns(self.rawdata["Close"])
        self.rawdata.dropna(inplace=True)

    def optimize(self):

        rprint(f"[{datetime.now().time()}] STARTING BFO")

        fast_range = range(10, 51, 1)
        slow_range = range(50, 125, 1)

        with Progress() as progress:
            task = progress.add_task(f"BRUTE FORCE OPTIMIZATION", total=len(fast_range) * len(slow_range))

            # TODO make this faster
            for fast, slow in product(fast_range, slow_range):
                testdata = self.rawdata.copy()
                if fast != slow:  # account for 50, 50 overlap
                    testdata["fast"] = testdata["Close"].rolling(fast).mean()
                    testdata["slow"] = testdata["Close"].rolling(slow).mean()
                    testdata["position"] = np.where(testdata["fast"] >= testdata["slow"], 1, 0)
                    testdata["strategy_returns"] = testdata["position"] * testdata["returns"]  # do not shift position
                    testdata.dropna(inplace=True)
                    metrics = strategy_metrics(testdata["strategy_returns"])
                    self.results = pd.concat(
                        [
                            self.results,
                            pd.DataFrame(
                                {
                                    "Fast": fast,
                                    "Slow": slow,
                                    "CAGR": metrics["CAGR"],
                                    "Sharpe": metrics["Sharpe"],
                                    "Drawdown": metrics["Max Drawdown"],
                                    "Returns": np.exp(testdata["strategy_returns"].sum()),
                                }
                            ),
                        ],
                    )

                    progress.advance(task)

        self.results = self.results.loc[self.results["Drawdown"] >= self.max_drawdown, :]

        self.results.sort_values("Returns", ascending=False, inplace=True)
        self.results.to_csv(RESULTSPATH)

        best = self.results.iloc[0]
        best = pd.DataFrame(best).T
        best.to_parquet(OPTIMIZEDDMAPATH)

        rprint(
            f"[{datetime.now().time()}] BFO RESULTS: CAGR {best['CAGR'].iloc[0]}, DD {best['Drawdown'].iloc[0]}, Fast {best['Fast'].iloc[0]}, Slow {best['Slow'].iloc[0]}"
        )


if __name__ == "__main__":
    BruteForceLearner().optimize()
