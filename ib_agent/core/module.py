# code is based on the following
# https://github.com/Lightning-AI/lightning-bolts/blob/master/pl_bolts/models/regression/logistic_regression.py

import pytorch_lightning as pl
import torch.nn.functional as F
from torch import nn, optim
from torchmetrics.functional import accuracy


class LitModel(pl.LightningModule):
    """a custom PyTorch Lightning LightningModule"""

    def __init__(
        self,
        input_dim,
        num_classes=2,
        learning_rate=0.001,
        bias=True,
        l1_strength=0.0,
        l2_strength=0.0,
    ):
        self.input_dim = input_dim
        self.num_classes = num_classes
        self.lr = learning_rate
        self.bias = bias
        self.l1_strength = l1_strength
        self.l2_strength = l2_strength
        self.save_hyperparameters()

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = nn.Linear(x)
        y_hat = F.softmax(x)
        return y_hat

    def training_step(self, batch, batch_idx: int):
        x, y = batch
        x = x.view(x.size(0), -1)
        y_hat = self.linear(x)
        loss = F.cross_entropy(y_hat, y)

        if self.hparams.l1_strength > 0:
            l1_reg = self.linear.weight.abs().sum()
            loss += self.hparams.l1_strength * l1_reg

        if self.hparams.l2_strength > 0:
            l2_reg = self.linear.weight.pow(2).sum()
            loss += self.hparams.l2_strength * l2_reg

        return loss / x.size(0)

    def test_step(self, batch, *args):
        self._shared_eval(batch, "test")

    def validation_step(self, batch, *args):
        self._shared_eval(batch, "val")

    def _shared_eval(self, batch, prefix):
        x, y = batch
        x = x.view(x.size(0), -1)
        y_hat = self.linear(x)
        acc = accuracy(F.log_softmax(y_hat, -1), y)
        loss = F.cross_entropy(y_hat, y)
        self.log(f"{prefix}_loss: {loss}", f"{prefix}_acc: {acc}")

    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        x, y = batch
        return self(x)

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=self.lr)
        return optimizer
