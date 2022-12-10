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

import json
import os
from datetime import datetime
from pathlib import Path

import yfinance as yf
from rich import print as rprint
from rich.progress import Progress

FILEPATH = Path(__file__)
PROJECTPATH = FILEPATH.parents[2]
MARKETSPATH = os.path.join(PROJECTPATH, "data", "markets")
RAWDATAPATH = os.path.join(MARKETSPATH, "raw")
MARKETSBLOBPATH = os.path.join(MARKETSPATH, "markets.json")


def run():

    if not os.path.isdir(os.path.join(RAWDATAPATH)):
        os.mkdir(os.path.join(RAWDATAPATH))

    with open(MARKETSBLOBPATH) as f:
        markets = json.load(f)

    rprint(f"[{datetime.now().time()}]FETCHING DATA")

    with Progress() as progress:
        for key in markets.keys():
            task = progress.add_task(f"FETCHING {key.upper()}", total=len(markets[key]))

            if not os.path.isdir(os.path.join(RAWDATAPATH, key)):
                os.mkdir(os.path.join(RAWDATAPATH, key))

            for ticker in markets[key]:

                if ticker == "VIX":
                    ticker = "^VIX"

                data = yf.Ticker(ticker).history("max")
                data.index = data.index.date
                data.reset_index(inplace=True)
                data.rename(columns={"index": "Date"}, inplace=True)
                data.set_index("Date", inplace=True)

                if ticker == "^VIX":
                    ticker = "VIX"

                datapath = os.path.join(RAWDATAPATH, key, f"{ticker}.pq")
                data.to_parquet(datapath)

                progress.advance(task)

    rprint(f"[{datetime.now().time()}] DATA FETCHED")


if __name__ == "__main__":
    run()
