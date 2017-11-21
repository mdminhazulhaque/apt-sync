#!/usr/bin/env python2

import subprocess
import os
import glob
import sys
import json
from datetime import datetime

MACHINES_DIR = "machines" + os.sep
MACHINE_FILE = ".machine"

def dump(machine_name):
    print("Dumping to " + machine_name)
    os.system("dpkg --get-selections | awk '{print $1}' > " + machine_name)

def diff(machine_this, machine_that, verbose=False):
    dump(machine_this)
    
    regexp = "| egrep \"<|>\""
    out = subprocess.check_output(" ".join([
            "diff",
            machine_this,
            machine_that,
            regexp]),
        shell=True).split("\n")
    
    out.pop()
    
    for item in out:
        if item.startswith("<"):
            print("+ " + item[2:])
        else:
            print("- " + item[2:])
        
if __name__ == "__main__":
    if not os.path.exists(MACHINES_DIR):
        os.mkdir(MACHINES_DIR)
        
    machine_this = None
    
    try:
        with open(MACHINE_FILE) as file:
            machine_this = file.read().strip()
    except:
        machine_this = raw_input("No machine name was deteced.\nMachine-Name: ")
        with open(MACHINE_FILE, 'w') as file:
            file.write(machine_this)
            
    try:
        arg1 = sys.argv[1]
        
        if arg1 not in ["diff", "dump"]:
            exit()
        
        if arg1 == "dump":
            dump(machine_this)
        elif arg1 == "diff":
            os.chdir(MACHINES_DIR)
            try:
                diff(sys.argv[2])
            except:
                machines = []
                for m in os.listdir("."):
                    if m != machine_this:
                        machines.append(m)
                
                if len(machines) == 1:
                    machine_that = machines[0]
                else:
                    print("Select machine ID to compare\n")
                    for id, name in enumerate(machines):
                        print(str(id) + " " + name)
                    print
                    machine_id = raw_input("Choice: ")
                    machine_that = machines[int(machine_id)]
                
                diff(machine_this, machine_that)
    except:
        pass
    