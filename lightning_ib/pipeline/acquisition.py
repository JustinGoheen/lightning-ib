import os
import json
import yfinance as yf

from pathlib import Path
from rich import print as rprint

filepath = Path(__file__)
projectpath = filepath.parents[2]
marketspath = os.path.join(projectpath, "data", "markets")
rawdatapath = os.path.join(marketspath, "raw")
marketsblobpath = os.path.join(marketspath, "markets.json")

with open(marketsblobpath) as f:
    markets = json.load(f)

rprint("\n" + f"[bold cyan]FETCHING DATA[/bold cyan]" + "\n")

for key in markets.keys():

    rprint(f"[bold white]{key.upper()}[/bold white]")

    if not os.path.isdir(os.path.join(rawdatapath, key)):
        os.mkdir(os.path.join(rawdatapath, key))

    for ticker in markets[key]:
        if ticker == "VIX":
            ticker = "^VIX"

        tickerdata = yf.Ticker(ticker).history("max")

        if ticker == "^VIX":
            ticker = "VIX"

        rprint(f"[bold green]{ticker}[/bold green]: start {tickerdata.index[0]} end {tickerdata.index[-1]}")

        tickerdatapath = os.path.join(rawdatapath, key, f"{ticker}.pq")
        tickerdata.to_parquet(tickerdatapath)

rprint("\n" + f"[bold cyan]DATA FETCHED[/bold cyan]" + "\n")
