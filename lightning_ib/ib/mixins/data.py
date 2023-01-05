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

import ib_insync as ib
import numpy as np
import pandas as pd
from rich import print as rprint


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

    def to_dataframe(self, data, use_cols: Optional[List[str]] = None):
        return ib.util.df(data, labels=use_cols)
