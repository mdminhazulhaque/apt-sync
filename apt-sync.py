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
    return pkglist_ret

def dump(machine_name, pkg_list):
    if not os.path.exists(machine_name):
        os.mkdir(machine_name)
    filename = MACHINES_DIR + machine_name + ".json"
    with open(filename, "w") as file:
        json.dump(pkg_list, file)

def load(filename):
    with open(filename) as file:
        return json.load(file)

def diff(machine_name):
    machine_file = MACHINES_DIR + machine_name + ".json"
    set_a = set(load(machine_file))
    set_b = set(pkglist())
    
    pkg_diff = [x for x in set_a if x not in set_b]
    
    for elem in sorted(pkg_diff):
        print elem
    
if __name__ == "__main__":
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        
        if arg1 == "dump":
            dump(arg2, pkglist())
        elif arg1 == "diff":
            diff(arg2)
    except:
        pass