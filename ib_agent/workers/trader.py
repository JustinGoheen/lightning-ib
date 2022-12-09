import lightning as L

from ib_agent.core import trader


class TradingAgent(L.LightningWork):
    def run():
        """runs an ib_insync script"""
