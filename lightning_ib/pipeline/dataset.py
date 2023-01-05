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

import os
from pathlib import Path
from typing import Any

import pandas as pd
import torch
from torch.utils.data import Dataset

FILEPATH = Path(__file__)
PROJECTPATH = FILEPATH.parents[2]
FEATURESPATH = os.path.join(PROJECTPATH, "data", "markets", "training", "features.pq")
LABELSPATH = os.path.join(PROJECTPATH, "data", "markets", "training", "labels.pq")


class LitDataset(Dataset):
    def __init__(self):
        self.features = pd.read_parquet(FEATURESPATH).reset_index().drop("Date", axis=1)
        self.labels = pd.read_parquet(LABELSPATH).reset_index().drop("Date", axis=1)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        x, y = self.features.iloc[idx], self.labels.iloc[idx]
        return dict(features=torch.tensor(x), labels=torch.tensor(y))
