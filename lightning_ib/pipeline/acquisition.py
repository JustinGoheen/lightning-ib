import os
import json
import yfinance as yf

from pathlib import Path
from rich import print as rprint

filepath = Path(__file__)
projectpath = filepath.parents[2]
datapath = os.path.join(projectpath, "data", "markets")
marketsblobpath = os.path.join(datapath, "markets.json")

with open(marketsblobpath) as f:
    markets = json.load(f)

rprint("\n" + f"[bold cyan]FETCHING DATA[/bold cyan]" + "\n")

for key in markets.keys():

    rprint(f"[bold white]{key.upper()}[/bold white]")

    if not os.path.isdir(os.path.join(datapath, key)):
        os.mkdir(os.path.join(datapath, key))

    for ticker in markets[key]:
        if ticker == "VIX":
            ticker = "^VIX"

        tickerdata = yf.Ticker(ticker).history("max")

        if ticker == "^VIX":
            ticker = "VIX"

        rprint(f"[bold green]{ticker}[/bold green]: start {tickerdata.index[0]} end {tickerdata.index[-1]}")

        tickerdatapath = os.path.join(datapath, key, f"{ticker}.pq")
        tickerdata.to_parquet(tickerdatapath)

rprint("\n" + f"[bold cyan]DATA FETCHED[/bold cyan]" + "\n")
