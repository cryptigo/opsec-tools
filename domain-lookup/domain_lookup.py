#!/usr/bin/env python3
"""Get various information about a specific domain."""
import whois
import argparse
from colorama import Fore, init

__author__ = "cryptigo"
__version__ = "0.0.1"

# Colorama
init()
RED   = Fore.RED
GREEN = Fore.GREEN
RESET = Fore.RESET

def is_registered(domain_name):
    """
    Returns a boolean indicating
    whether a `domain_name` is currently registered.
    """
    try:
        w = whois.whois(domain_name)
    except Exception as e:
        return False
    else:
        return bool(w.domain_name)