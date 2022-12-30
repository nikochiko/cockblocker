#!/bin/bash

sudo python3 monitor_process.py blocker.py /etc/hosts

# repeat monitor_process.py multiple times to build a chain of monitors
# sudo python3 monitor_process.py monitor_process.py monitor_process.py blocker.py /etc/hosts
