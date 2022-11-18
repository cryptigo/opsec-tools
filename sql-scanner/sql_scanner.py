#!/usr/bin/env python3
"""
A SQL injection vunerability scanner written in python.
"""

import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
import argparse
from colorama import Fore, init
from fake_useragent import UserAgent
import untangle

# load error xml file
error_doc = untangle.parse('data/errors.xml')

# Colorama
init()
RED   = Fore.RED
GRAY  = Fore.LIGHTBLACK_EX
GREEN = Fore.GREEN
RESET = Fore.RESET

# Initialize an HTTP session and set the browser to a random useragent
s = requests.Session()
ua = UserAgent()
s.headers["User-Agent"] = ua.random

def get_all_forms(url):
    """
    Given a `url`, get all forms from the HTML content
    """
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """
    Extracts all possible useful information about an HTML `form`
    """
    details = {}

    # Get the form action (target url)
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None

    # Get the form method (POST, GET, etc)
    method = form.attrs.get("method", "get").lower()

    # Get all the input details (type, name)
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    
    # Put everything into a dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def is_vulnerable(response):
    """
    Determines whether a page is vunerable to SQL Injection
    from its `response`
    """
    # Get error messages
    mysql_errors  = error_doc.root.db[0].error["value"]
    sqlsrv_errors = error_doc.root.db[1].error["value"]
    oracle_errors = error_doc.root.db[2].error["value"]

    errors = {
        # mysql
        mysql_errors,
        sqlsrv_errors,
        oracle_errors
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True

    # No error
    return False

def scan_sql_injection(url):
    # Test on url
    for c in "\"'":
        # Add quote char to the url
        new_url = f"{url}{c}"
        print(GRAY + "[~] Trying", new_url)
        # Make the HTTP request
        res = s.get(new_url)
        if is_vulnerable(res):
            print(GREEN + "[+] SQL vulnerability detected, link: " + new_url + RESET)
            return
    # Test on

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description="SQL injection vunerability scanner written in Python 3.")