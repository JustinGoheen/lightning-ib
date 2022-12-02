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

# use this to create a pre-processing script if needed

import os
import json
import yfinance as yf

from pathlib import Path
from rich import print as rprint
from pyarrow import parquet as pq

from lightning_ib.metrics import factors


FILEPATH = Path(__file__)
PROJECTPATH = FILEPATH.parents[2]
MARKETSPATH = os.path.join(PROJECTPATH, "data", "markets")
RAWDATAPATH = os.path.join(MARKETSPATH, "raw")
PROCESSEDDATAPATH = os.path.join(MARKETSPATH, "processed")
MARKETSBLOBPATH = os.path.join(MARKETSPATH, "markets.json")

if not os.path.isdir(os.path.join(PROCESSEDDATAPATH)):
    os.mkdir(os.path.join(PROCESSEDDATAPATH))

with open(MARKETSBLOBPATH) as f:
    markets = json.load(f)

rprint("\n" + f"[bold cyan]PRE PROCESSING[/bold cyan]" + "\n")

for key in markets.keys():

    if not os.path.isdir(os.path.join(PROCESSEDDATAPATH, key)):
        os.mkdir(os.path.join(PROCESSEDDATAPATH, key))

    for ticker in markets[key]:

        rawtickerdatapath = os.path.join(RAWDATAPATH, key, f"{ticker}.pq")
        processedtickerdatapath = os.path.join(PROCESSEDDATAPATH, key, f"{ticker}.pq")

        data = pq.read_table(rawtickerdatapath, columns=["Date", "Open", "High", "Low", "Close"]).to_pandas()

        if ticker == "VIX":
            data["RANK"] = factors.expanding_rank(data["Close"])
        else:
            data["NATR_RANK"] = factors.expanding_rank(factors.normalized_average_true_range(data, period=20))
            data["AROON_RANK"] = factors.expanding_rank(factors.aroon_oscillator(data, period=20))
            data["RSI_RANK"] = factors.expanding_rank(factors.relative_strength_index(data["Close"], period=20))
            data["ROC_RANK"] = factors.expanding_rank(factors.rate_of_change(data["Close"], period=20))
            data["RTNS_RANK"] = factors.expanding_rank(factors.log_returns(data["Close"]))

        data.drop(["Open", "High", "Low", "Close"], axis=1, inplace=True)

        data.to_parquet(processedtickerdatapath)

rprint("\n" + f"[bold cyan]DATA PROCESSED[/bold cyan]" + "\n")
