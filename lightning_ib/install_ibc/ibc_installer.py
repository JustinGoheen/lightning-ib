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

# for error on MacOS
# ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)
# see https://stackoverflow.com/questions/68275857/urllib-error-urlerror-urlopen-error-ssl-certificate-verify-failed-certifica


import os
import platform
import zipfile

from functools import partial
from urllib.request import urlopen

IBC_LATEST = "3.15.2"


def unzip(filepath, destination):
    with zipfile.ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall(destination)
        os.remove(filepath)


def add_ibconfigs_section(configpath):
    with open(configpath, "r") as file:
        contents = file.readlines()
    contents.insert(0, "[ibconfigs]\n")
    with open(configpath, "w") as file:
        contents = "".join(contents)
        file.write(contents)


def run():

    opsys = platform.system()
    if opsys == "Darwin":
        opsys = "Macos"

    destination = "ibc"

    if not os.path.isdir(destination):
        os.mkdir(destination)

    download_destination = os.path.join(os.getcwd(), destination)

    url = f"https://github.com/IbcAlpha/IBC/releases/download/{IBC_LATEST}/IBC{opsys}-{IBC_LATEST}.zip"

    response = urlopen(url)
    filename = url.split("/")[-1]
    dest_path = os.path.join(destination, filename)

    with open(dest_path, "wb") as dest_file:
        for data in iter(partial(response.read, 32768), b""):
            dest_file.write(data)

    filepath = os.path.join(download_destination, f"IBC{opsys}-{IBC_LATEST}.zip")

    unzip(filepath, download_destination)

    add_ibconfigs_section(os.path.join(download_destination, "config.ini"))


if __name__ == "__main__":
    run()
