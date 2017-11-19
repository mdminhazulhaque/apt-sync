import subprocess
import os
import json
from datetime import datetime

pkglist_raw = subprocess.check_output("dpkg --get-selections | awk '{print $1}'", shell=True)
pkglist = pkglist_raw.split("\n")
pkglist.pop()

machine = "minhaz-desktop"
timestamp = datetime.today().strftime('%Y%m%d_%H%M%S')

try:
    os.mkdir(machine)
except:
    pass

filename = machine + os.sep + timestamp + ".json"
with open(filename, "w") as file:
    json.dump(pkglist, file)
    