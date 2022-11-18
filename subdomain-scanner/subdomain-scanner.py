#!/usr/bin/env python3
import requests
from threading import Thread, Lock
from queue import Queue
import argparse
from colorama import init, Fore
import sys, os

__version__ = '0.1'

# Colorama
init()
RED   = Fore.RED
BLUE  = Fore.LIGHTBLUE_EX
GREEN = Fore.GREEN
GRAY  = Fore.LIGHTBLACK_EX
RESET = Fore.RESET

q = Queue()
list_lock = Lock()
discovered_domains = []

# Wordlist from `https://github.com/rajesh6927/subdomain-bruteforce-wordlist/blob/main/Subdomain-wordlist.txt`

def scan_subdomains(domain):
    global q
    while True:
        # Get the subdomain from the queue
        subdomain = q.get()
        # Scan the subdomain
        url = f"http://{subdomain}.{domain}"
        try:
            requests.get(url)
        except requests.ConnectionError as err:
            if args.verbose:
                print(RED + "[!] Subdomain '" + url + "' does not exist!" + RESET)
            else:
                pass
        else:
            print(GREEN + "[+] Subdomain found:" + url + RESET)
            # Add the subdomain to the global list
            with list_lock:
                discovered_domains.append(url)

        q.task_done()

def main(domain, num_threads, subdomains):
    global q

    # Fill the queue with all the subdomains
    for subdomain in subdomains:
        q.put(subdomain)


    # Threads
    for t in range(num_threads):
        # Start all threads
        worker = Thread(target=scan_subdomains, args=(domain,))
        worker.daemon = True
        worker.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Multithreaded Subdomain Scanner") 
    parser.add_argument("domain", help="Domain to scan for subdomains without protocol (e.g without 'http://' or 'https://')")
    parser.add_argument("-l", "--wordlist", help="File that contains all subdomains to scan, line by line. Default is wordlist.txt", default="wordlists/wordlist.txt")
    parser.add_argument("-t", "--num-threads", help="The number for threads to use to scan the domain. Default is 10.", default=10, type=int)
    parser.add_argument("-o", "--output-file", help="Specify the output text file to write discovered subdomains", default="discovered_subdomains.txt")
    parser.add_argument("-v", "--verbose", help="Display more detailed information. Default is False", action="store_true")
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    # Parse the arguments
    args        = parser.parse_args()
    domain      = args.domain
    wordlist    = args.wordlist
    num_threads = args.num_threads
    output_file = args.output_file

    main(domain=domain, num_threads=num_threads, subdomains=open(wordlist).read().splitlines())
    q.join()

    # Save the file
    if args.verbose:
        print(BLUE + '[~] Saving results to file.' + RESET)

    with open(output_file, "w") as f:
        for url in discovered_domains:
            print(url, file=f)
