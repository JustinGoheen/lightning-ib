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

import multiprocessing
import os
from pathlib import Path
from typing import Any, Union

from lightning.pytorch import LightningDataModule
from lightning.pytorch.utilities.types import EVAL_DATALOADERS, TRAIN_DATALOADERS
from torch.utils.data import DataLoader, random_split

from lightning_ib.pipeline.dataset import LitDataset

filepath = Path(__file__)
PROJECTPATH = os.getcwd()
NUMWORKERS = int(multiprocessing.cpu_count() // 2)


class LitDataModule(LightningDataModule):
    def __init__(
        self,
        dataset: Any = LitDataset,
        data_dir: str = "data",
        split: bool = True,
        train_size: float = 0.8,
        num_workers: int = NUMWORKERS,
    ):
        super().__init__()
        self.data_dir = os.path.join(PROJECTPATH, data_dir, "cache")
        self.dataset = dataset
        self.split = split
        self.train_size = train_size
        self.num_workers = num_workers

    def prepare_data(self) -> None:
        self.dataset()

    def setup(self, stage: Union[str, None] = None) -> None:
        if stage == "fit" or stage is None:
            full_dataset = self.dataset()
            train_size = int(len(full_dataset) * self.train_size)
            test_size = len(full_dataset) - train_size
            self.train_data, self.val_data = random_split(full_dataset, lengths=[train_size, test_size])
        if stage == "test" or stage is None:
            self.test_data = self.dataset()

    def train_dataloader(self) -> TRAIN_DATALOADERS:
        return DataLoader(self.train_data, num_workers=self.num_workers)

    def test_dataloader(self) -> EVAL_DATALOADERS:
        return DataLoader(self.test_data, num_workers=self.num_workers)

    def val_dataloader(self) -> EVAL_DATALOADERS:
        return DataLoader(self.val_data, num_workers=self.num_workers)
