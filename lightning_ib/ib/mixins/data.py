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

import datetime
import time
from abc import ABC
from typing import List, Optional

import numpy as np
import pandas as pd
from rich import print as rprint

import ib_insync as ib
from ibquant.markets import EquityFutureFrontMonth


class DataMixins(ABC):
    def __init__(self) -> None:
        super().__init__()

    def req_previous_tick(self):
        if not self.ib.isConnected():
            self.ib.connect(self.host, self.port, self.clientid)
        snapshot = self.ib.reqMktData(self.contract)
        ib.util.sleep(5)
        self.ib.cancelMktData(self.contract)
        return snapshot

    def req_historical_data(
        self,
        end_datetime: str = "",
        duration: str = "1 D",
        bar_size: str = "1 min",
        what_to_show: str = "TRADES",
        use_rth: bool = False,
        keep_connected: bool = False,
        data=None,
        multi_request: bool = False,
    ):
        """fetches historical bars"""

        if not self.ib.isConnected():
            self.ib.connect(self.host, self.port, self.clientid)

        data = self.ib.reqHistoricalData(
            self.contract,
            endDateTime=end_datetime,
            durationStr=duration,
            barSizeSetting=bar_size,
            whatToShow=what_to_show,
            useRTH=use_rth,
        )

        ib.util.sleep(30)

        if keep_connected:
            return data

        self.ib.disconnect()
        ib.util.sleep(5)

        return data

    def _process_bars(self):
        """used to process bars to make dataframe"""
        pass

    def historical_ticks(
        self,
        start_date_time: str = "20210319 09:30:00",
        end_date_time: str = "",
        number_of_ticks: int = 1000,  # max is 1000
        what_to_show: str = "TRADES",  # TRADES, MIDPOINT, BID, ASK, BID_ASK
        ignore_size: bool = False,
        use_rth: bool = True,
    ):
        """fetches historical ticks"""

        data = self.ib.reqHistoricalTicks(
            self.contract,
            startDateTime=start_date_time,
            endDateTime=end_date_time,
            numberOfTicks=number_of_ticks,
            whatToShow=what_to_show,
            useRth=use_rth,
            ignoreSize=ignore_size,
        )

        time.sleep(60)

        return data

    def _process_ticks(self):
        """used to process ticks for dataframe"""
        pass

    def histogram(
        self,
        use_rth: bool = False,
        period: str = "15 min",
    ):
        """
        fetches a historical histogram of volume at price

        Note:
            https://ib-insync.readthedocs.io/api.html#ib_insync.ib.IB.reqHistoricalTicks
            http://interactivebrokers.github.io/tws-api/historical_time_and_sales.html#reqHistoricalTicks
        """

        data = self.ib.reqHistogramData(
            self.contract,
            use_rth,
            period,
        )

        rprint(f"[bold green][FETCHING HISTOGRAM][/bold green] {datetime.datetime.now()}")

        ib.util.sleep(60)

        return data

    def news(self):
        pass

    def to_dataframe(self, data, use_cols: Optional[List[str]] = None):
        return ib.util.df(data, labels=use_cols)
