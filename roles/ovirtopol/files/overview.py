#!/usr/bin/python3

import os
import json
import subprocess

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.strip() if result.returncode == 0 else "N/A"

def collect_kvm_general_info():
    data = {
        "Host Information": {
            "Hostname": run_command("hostname"),
            "IP Address": run_command("hostname -I | awk \'{print $1}\'"),
            "Active VMs": run_command("virsh --readonly list --all --name | wc -l"),
            "Logical CPU Cores": run_command("lscpu | grep \'^CPU(s):\' | awk \'{print $2}\'"),  
            "Boot Time": run_command("who -b | awk '{print $3, $4}'")
        },
        "Hardware": {
            "Manufacturer": run_command("dmidecode -s system-manufacturer"),
            "CPU Model Name": run_command("lscpu | grep 'Model name' | awk -F \':\' \'{print $2}\' | xargs"),
            "CPU Cores per Socket": run_command("lscpu | grep \'Core(s) per socket\' | awk \'{print $NF}\'"),
            "CPU Threads per Core": run_command("lscpu | grep \'Thread(s) per core\' | awk \'{print $NF}\'"),
            "Product Name": run_command("dmidecode -s system-product-name"),
            "Serial Number": run_command("dmidecode -s system-serial-number"),
            "CPU Sockets": run_command("lscpu | grep \'Socket(s)\' | awk \'{print $NF}\'"),
            "TSC Frequency": run_command("lscpu | grep \'CPU MHz\' | awk \'{print $NF}\'")
        },
        "Software": {
            "OS Version": run_command("cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"'"),
            "Kernel Version": run_command("uname -r"),
            "KVM Version": run_command("rpm -q qemu-kvm"),
            "LIBVIRT Version": run_command("libvirtd --version 2>/dev/null || virsh --version"),
            "VDSM Version": run_command("rpm -q vdsm"),
        },
        "Storage & Memory": {
            "Physical Memory": run_command("lsmem | grep \"Total online memory\" | awk \'{print $4}\'"),
            "SELinux Mode": run_command("getenforce")
        },
    }
    var_hostname = run_command("hostname")
    output_file = f"{var_hostname}.json"
    try:
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"KVM General information saved to {output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    collect_kvm_general_info()
