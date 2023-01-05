# code is based on the following
# https://github.com/Lightning-AI/lightning-bolts/blob/master/pl_bolts/models/regression/logistic_regression.py

import lightning as L
import torch.nn.functional as F
import torch
from torch import nn, optim
from torchmetrics.functional import accuracy


class LitModel(L.LightningModule):
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
        super().__init__()
        self.save_hyperparameters()

        self.linear = nn.Linear(
            in_features=self.hparams.input_dim,
            out_features=self.hparams.num_classes,
            bias=self.bias,
        )

    def forward(self, x):
        x = self.linear(x)
        y_hat = F.softmax(x)
        return y_hat

    def training_step(self, batch, batch_idx: int):
        x, y = batch["features"], batch["labels"]
        x = x.view(x.size(0), -1)
        y = torch.flatten(y)
        y_hat = self.linear(x)
        loss = F.cross_entropy(y_hat, y, reduction="sum")

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
        x, y = batch["features"], batch["labels"]
        x = x.view(x.size(0), -1)
        y_hat = self.linear(x)
        y = torch.flatten(y)
        # acc = accuracy(F.softmax(y_hat, -1), y, "binary")
        loss = F.cross_entropy(y_hat, y, reduction="sum")
        self.log(f"{prefix}_loss", loss)

    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        x, y = batch["features"], batch["labels"]
        return self(x)

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=self.lr)
        return optimizer
