import lightning as L

from lightning_ib.core import brute


class BruteWorker(L.LightningWork):
    def run():
        """runs a brute force optimizer"""
