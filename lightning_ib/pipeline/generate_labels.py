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

from lightning_ib.core import BruteForceLearner

FILEPATH = Path(__file__)
PROJECTPATH = FILEPATH.parents[2]
MARKETSPATH = os.path.join(PROJECTPATH, "data", "markets")
PROCESSEDDATAPATH = os.path.join(MARKETSPATH, "processed")
LABELSPATH = os.path.join(PROCESSEDDATAPATH, "labels")

if not os.path.isdir(os.path.join(LABELSPATH)):
    os.mkdir(os.path.join(LABELSPATH))

labels = BruteForceLearner("SPY")
labels.to_parquet(LABELSPATH)
