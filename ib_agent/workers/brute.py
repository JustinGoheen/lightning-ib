import lightning as L

from ib_agent.core import brute


class BruteAgent(L.LightningWork):
    def run():
        """runs a brute force optimizer"""
