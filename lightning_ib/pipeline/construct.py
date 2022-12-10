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


# use this to construct the training dataset that will be used by dataset.py

import os
import json
import pandas as pd

from pyarrow import parquet as pq
from pathlib import Path
from rich import print as rprint
from datetime import datetime

FILEPATH = Path(__file__)
PROJECTPATH = FILEPATH.parents[2]
MARKETSPATH = os.path.join(PROJECTPATH, "data", "markets")
MARKETSBLOBPATH = os.path.join(MARKETSPATH, "markets.json")
PROCESSEDDATAPATH = os.path.join(MARKETSPATH, "processed")
TRAININGDATADIR = os.path.join(MARKETSPATH, "training")
TRAININGDATAPATH = os.path.join(TRAININGDATADIR, "training.pq")


def run():

    if not os.path.isdir(os.path.join(TRAININGDATADIR)):
        os.mkdir(os.path.join(TRAININGDATADIR))

    with open(MARKETSBLOBPATH) as f:
        markets = json.load(f)

    rprint(f"[{datetime.now().time()}] CONSTRUCTING DATASET")

    trainingdataset = pd.DataFrame()

    for key in markets.keys():
        for ticker in markets[key]:
            processedtickerdatapath = os.path.join(PROCESSEDDATAPATH, key, f"{ticker}.pq")
            data = pq.read_table(processedtickerdatapath).to_pandas()
            trainingdataset = trainingdataset.join(data, how="outer")

    trainingdataset.dropna(inplace=True)
    trainingdataset.to_parquet(TRAININGDATAPATH)

    rprint(f"[{datetime.now().time()}] DATASET CONSTRUCTED")


if __name__ == "__main__":
    run()
