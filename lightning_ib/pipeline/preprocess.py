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

# use this to create a preprocessing script if needed

import json
import os
from datetime import datetime
from pathlib import Path

from pyarrow import parquet as pq
from rich import print as rprint
from rich.progress import Progress

from lightning_ib.metrics import factors

FILEPATH = Path(__file__)
PROJECTPATH = FILEPATH.parents[2]
MARKETSPATH = os.path.join(PROJECTPATH, "data", "markets")
RAWDATAPATH = os.path.join(MARKETSPATH, "raw")
PROCESSEDDATAPATH = os.path.join(MARKETSPATH, "processed")
MARKETSBLOBPATH = os.path.join(MARKETSPATH, "markets.json")


def run():

    if not os.path.isdir(os.path.join(PROCESSEDDATAPATH)):
        os.mkdir(os.path.join(PROCESSEDDATAPATH))

    with open(MARKETSBLOBPATH) as f:
        markets = json.load(f)

    nobs = len([l for b in [markets[k] for k in markets.keys()] for l in b])

    rprint(f"[{datetime.now().time()}] STARTING PRE PROCESSING")

    with Progress() as progress:
        task = progress.add_task(f"PROCESSING DATA", total=nobs)

        for key in markets.keys():

            if not os.path.isdir(os.path.join(PROCESSEDDATAPATH, key)):
                os.mkdir(os.path.join(PROCESSEDDATAPATH, key))

            for ticker in markets[key]:

                rawtickerdatapath = os.path.join(RAWDATAPATH, key, f"{ticker}.pq")
                processedtickerdatapath = os.path.join(PROCESSEDDATAPATH, key, f"{ticker}.pq")

                data = pq.read_table(rawtickerdatapath, columns=["Date", "Open", "High", "Low", "Close"]).to_pandas()

                if ticker == "VIX":
                    data[f"{ticker.upper()}_RANK"] = factors.expanding_rank(data["Close"])
                else:
                    data[f"{ticker.upper()}_NATR_RANK"] = factors.expanding_rank(
                        factors.normalized_average_true_range(data, period=20)
                    )
                    data[f"{ticker.upper()}_AROON_RANK"] = factors.expanding_rank(
                        factors.aroon_oscillator(data, period=20)
                    )
                    data[f"{ticker.upper()}_RSI_RANK"] = factors.expanding_rank(
                        factors.relative_strength_index(data["Close"], period=20)
                    )
                    data[f"{ticker.upper()}_ROC_RANK"] = factors.expanding_rank(
                        factors.rate_of_change(data["Close"], period=20)
                    )
                    data[f"{ticker.upper()}_RTNS_RANK"] = factors.expanding_rank(factors.log_returns(data["Close"]))

                data.drop(["Open", "High", "Low", "Close"], axis=1, inplace=True)
                data.to_parquet(processedtickerdatapath)

                progress.advance(task)

    rprint(f"[{datetime.now().time()}] PRE PROCESSING COMPLETE")


if __name__ == "__main__":
    run()
