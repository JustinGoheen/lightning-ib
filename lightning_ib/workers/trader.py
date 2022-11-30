import lightning as L

from lightning_ib.core import trader


class TradingWorker(L.LightningWork):
    def run():
        """runs an ib_insync script"""
