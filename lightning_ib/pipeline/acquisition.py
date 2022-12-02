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

        tickerdata = yf.Ticker(ticker).history("max")

        if ticker == "^VIX":
            ticker = "VIX"

        rprint(f"[bold green]{ticker}[/bold green]: start {tickerdata.index[0]} end {tickerdata.index[-1]}")

        tickerdatapath = os.path.join(RAWDATAPATH, key, f"{ticker}.pq")
        tickerdata.to_parquet(tickerdatapath)

rprint("\n" + f"[bold cyan]DATA FETCHED[/bold cyan]" + "\n")
