#!/usr/bin/env python2

import subprocess
import os
import glob
import sys
import json
from datetime import datetime

MACHINES_DIR = "machines" + os.sep

def pkglist():
    pkglist_raw = subprocess.check_output("dpkg --get-selections | awk '{print $1}'", shell=True)
    pkglist_ret = pkglist_raw.split("\n")
    pkglist_ret.pop()
    return set(pkglist_ret)

def dump(machine_name, pkg_list):
    if not os.path.exists(machine_name):
        os.mkdir(machine_name)
    timestamp = datetime.today().strftime('%Y%m%d_%H%M%S')
    filename = machine_name + os.sep + timestamp + ".json"
    with open(filename, "w") as file:
        json.dump(pkg_list, file)

def load(filename):
    with open(filename) as file:
        return set(json.load(file))

def diff(machine_with):
    machine_file = MACHINES_DIR + machine_with + ".json"
    set_a = load(machine_file)
    set_b = pkglist()
    
    pkg_diff = [x for x in set_a if x not in set_b]
    for elem in sorted(pkg_diff):
        print elem
    
if __name__ == "__main__":
    #machine_name = sys.argv[1]
    #dump(machine_name, pkglist())
    
    diff("minhaz-desktop")
    