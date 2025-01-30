#!/usr/bin/python3

import os
import json
import subprocess

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.strip() if result.returncode == 0 else "N/A"

def collect_ovirt_general_info():
    data = {
        "Host Information": {
            "Hostname": run_command("hostname"),
            "IP Address": run_command("hostname -I | awk \'{print $1}\'"),
            "Boot Time": run_command("who -b | awk '{print $3, $4}'")
        },
        "Hardware": {
            "Manufacturer": run_command("dmidecode -s system-manufacturer"),
            "Product Name": run_command("dmidecode -s system-product-name"),
            "Serial Number": run_command("dmidecode -s system-serial-number"),
        },
        "Software": {
            "OS Version": run_command("cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"'"),
            "Kernel Version": run_command("uname -r"),
            "oVirt Version": run_command("rpm -q ovirt-engine"),
        },
        "Storage & Memory": {
            "Physical Memory": run_command("lsmem | grep \"Total online memory\" | awk \'{print $4}\'"),
            "SELinux Mode": run_command("getenforce")
        },
    }
    output_file = "engine.json"
    try:
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"oVirt engine General information saved to {output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}")
    
if __name__ == "__main__":
    collect_ovirt_general_info()
