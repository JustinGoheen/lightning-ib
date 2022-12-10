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

import lightning as L

from datetime import datetime
from rich import print as rprint

from lightning_ib.core import brute


class BruteAgent(L.LightningWork):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self):
        """runs a brute force optimizer"""
        rprint(f"[{datetime.now().time()}] {self.__class__.__name__} STARTING")
        rprint(f"[{datetime.now().time()}] {self.__class__.__name__} WORKING")
        rprint(f"[{datetime.now().time()}] {self.__class__.__name__} COMPLETE")
