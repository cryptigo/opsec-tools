#!/usr/bin/env python3
"""
An advanced network scanner build in Python 3
Features:
    - ARP Scanner
    - DHCP Listener
    - UDP/TCP Scanner
    - ICMP Scanner
    - Passive monitor
    - Wi-Fi Scanner
"""

__version__ = "0.0.1"
__author__  = "cryptigo"

from scapy.all import *
import time
import requests
import argparse
import colorama
import socket
import urllib3

def main(target):
    


