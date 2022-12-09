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
import json
import yfinance as yf

from pathlib import Path
from rich import print as rprint

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

    rprint("\n" + f"[bold cyan]FETCHING DATA[/bold cyan]" + "\n")

    for key in markets.keys():

        rprint(f"[bold white]{key.upper()}[/bold white]")

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

            rprint(f"[bold green]{ticker}[/bold green]: start {data.index[0]} end {data.index[-1]}")

            datapath = os.path.join(RAWDATAPATH, key, f"{ticker}.pq")
            data.to_parquet(datapath)

    rprint("\n" + f"[bold cyan]DATA FETCHED[/bold cyan]" + "\n")


if __name__ == "__main__":
    run()
