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
import os
import sys
from typing import Any, Dict, Optional

import ib_insync as ib
import pytz
from rich import print as rprint

from lightning_ib.ib.base import AppBase


class Trader(AppBase):
    """
    a base class for Trading Agents
    """

    def __init__(
        self,
        platform: str,
        connection_type: str,
        contract_type: str,
        contract_kwargs: Dict[str, Any],
        account: Optional[str] = None,
        price_source: str = "close",
        order_size: int = 1,
        stop_offset: Optional[int] = None,
        time_sentinel: Optional[int] = None,
        backfill_history: bool = False,
        persist_history: bool = False,
        data_dir: Optional[str] = None,
        logs_dir: Optional[str] = None,
        tws_timezone: Optional[str] = None,
        history_end_datetime: Optional[str] = None,
        history_duration: Optional[str] = None,
        history_bar_size: Optional[str] = None,
        history_price_source: Optional[str] = None,
        history_use_rth: bool = False,
    ) -> None:
        super().__init__(
            platform=platform, connection_type=connection_type, account=account, contract_type=contract_type
        )

        self.validate_contract_config()

        self.contract = self.contract_method(**contract_kwargs)

        self.order_size = order_size
        self.time_sentinel = time_sentinel
        self._stop_offset = stop_offset
        self.price_source = price_source
        self.data_dir = data_dir
        self.logs_dir = logs_dir
        self.ib.TimezoneTWS = pytz.timezone(tws_timezone) if tws_timezone is not None else None

        if backfill_history:
            rprint("\n" + f"[bold green][FETCHING HISTORY][/bold green] {datetime.datetime.now()}")
            # TODO add rich progress bar
            self.history = self.historical_bars(
                end_date_time=history_end_datetime,
                duration=history_duration,
                bar_size=history_bar_size,
                what_to_show=history_price_source,
                use_rth=history_use_rth,
            )

            self.history = self.to_dataframe(self.history)

            if persist_history:
                self.persist_history_to_logs(
                    data_dir=f"{os.path.join('data', f'history_{datetime.datetime.now().date().csv}')}"
                )

    @property
    def offset(self) -> Dict[str, str]:
        return dict(stop=self._stop_offset)

    @property
    def open_orders(self) -> bool:
        trades = [getattr(self, attr) for attr in ["parent_trade", "trailing_oder"] if hasattr(self, attr)]
        return any(i.isActive() for i in trades)

    @property
    def no_position(self) -> bool:
        """determines if position is 0"""
        return self.position == 0

    @property
    def pending_parentorder(self) -> bool:
        """determines if a parent order associated"""
        if hasattr(self, "parent_trade"):
            return self.parent_trade.isActive() and self.no_position
        else:
            return False

    @property
    def start_trading_ops(self) -> bool:
        """sets a logic to trade if position is 0 when first data message arrives"""

    @property
    def continue_trading_ops(self) -> bool:
        """determines if trades have been placed or a position is open when first data message arrives"""
        return hasattr(self, "parent_trade") or not self.no_position

    @property
    def position(self) -> int:
        """sets the position associated with the symbol"""
        _position = [i for i in self.ib.positions(self.account) if i.contract.symbol == self.contract.symbol]
        return _position[0].position if _position else 0

    @property
    def pnl(self):
        """fetches the PnL associated with the symbol"""

    def log_data_message_to_terminal(self) -> None:
        """logs market data messages to terminal"""

    def persist_history_to_logs(self, data_dir) -> None:
        """sends logs to data directory"""

    def order_filled_message(self) -> None:
        """logs fills to terminal"""

    def place_trailing_order(self, **kwargs) -> None:
        """places order"""

    def cancel_parentorder_if_stale(self) -> None:
        time_delta = (datetime.datetime.now() - self.timeoftrade).total_seconds()
        if time_delta >= self.time_sentinel:
            if self.parent_trade.isActive():
                rprint(
                    f"[bold green][CANCELLING TRADE {self.parent_trade.order.orderId}][/bold green]",
                    f"{datetime.datetime.now()}",
                )
                if self.parent_trade.order.orderId in [o.orderId for o in self.ib.openOrders()]:
                    self.ib.cancelOrder(self.trailing_order.order)
                    self.ib.cancelOrder(self.parent_trade.order)

    def execute_trade(self) -> None:
        """
        creates an order and places the associated trades

        Example:

        ```python
        action = "BUY" if some_logic_is_true else "SELL"
        entry_price = self.bars[-1].close
        limit_order = ib.LimitOrder(action=action, totalQuantity=1, lmtPrice=limit_price)
        self.trade = self.ib.placeOrder(self.contract, limit_order)
        ```

        """

    def trader_logic(self):
        """the trader's execution logic

        Example:

        ```python
        if self.start_trading_ops:
            self.execute_trade(trade_message="opening trade")

        if self.continue_trading_ops:
            if self.pending_parentorder:
                self.cancel_parentorder_if_stale()

            if self.flank_cancelled:
                self.resubmit_flanks()

            if self.reentry:
                self.execute_trade(trade_message="re-entry")

            if self.trend_reversal:
                self.cancel_flanks(purpose="reverse")
                self.execute_trade(trade_message="reversal")
        ```

        """

    async def run_async(self) -> None:
        """
        allows for async streaming

        Example:

        ```python
        with await self.ib.connectAsync(
            self.host,
            self.ports[self.platform][self.connection_type],
            clientId=self.clientid,
        ):

            self.bars = self.ib.reqRealTimeBars(
                self.contract,
                barSize=5,
                whatToShow="TRADES",
                useRTH=False,
                realTimeBarsOptions=[],
            )

            rprint(f"[bold green][DATA REQUESTED][/bold green] {datetime.datetime.now()}")

            async for update_event in self.bars.updateEvent:
                if self.persist_history:
                    self.update_history()

                log_data_message_to_terminal(
                    self.contract.symbol, self.bars, self.fastma, self.slowma, self.position, self.trend_direction
                )

                self.trader_logic()
        ```

        """

    def run(self):
        """runs non-async jobs

        Example:

        ```python
        self.ib.connect(
            self.host,
            self.ports[self.platform][self.connection_type],
            clientId=self.clientid,
        )

        self.bars = self.ib.reqRealTimeBars(
            self.contract,
            barSize=5,
            whatToShow="TRADES",
            useRTH=False,
            realTimeBarsOptions=[],
        )

        rprint(f"[bold green][DATA REQUESTED][/bold green] {datetime.datetime.now()}")

        ib.util.sleep(30)

        if self.persist_history:
            self.update_history()

        log_data_message_to_terminal(
            self.contract.symbol, self.bars, self.fastma, self.slowma, self.position, self.trend_direction
        )

        self.trader_logic()
        ```

        """

    def stop(self) -> None:
        self.ib.disconnect()
        sys.exit()
