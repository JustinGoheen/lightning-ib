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
from pathlib import Path

import numpy as np
import pandas as pd
from rich import print as rprint

FILEPATH = Path(__file__)
PROJECTPATH = FILEPATH.parents[2]
OPTIMIZEDDMAPATH = os.path.join(PROJECTPATH, "data", "optimized_dma.pq")
SPYDATAPATH = os.path.join(PROJECTPATH, "data", "markets", "raw", "equities", "SPY.pq")
LABELSPATH = os.path.join("data", "labels.pq")


def run():
    rprint(f"[{datetime.now().time()}] GENERATING LABELS")
    marketdata = pd.read_parquet(SPYDATAPATH, columns=["Close"])
    optimizeddma = pd.read_parquet(OPTIMIZEDDMAPATH)
    marketdata["Fast"] = marketdata["Close"].rolling(optimizeddma["Fast"].iloc[0]).mean()
    marketdata["Slow"] = marketdata["Close"].rolling(optimizeddma["Slow"].iloc[0]).mean()
    marketdata["Label"] = np.where(marketdata["Fast"] >= marketdata["Slow"], 1, 0)
    marketdata[["Label"]].to_parquet(LABELSPATH)


if __name__ == "__main__":
    run()
