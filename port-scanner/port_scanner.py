#!/usr/bin/env python3
# A multithreaded CLI port scanner written in Python 3
import argparse
import socket
from colorama import init, Fore
from threading import Thread, Lock
from queue import Queue

# Colorama setup
init()
RED   = Fore.RED
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY  = Fore.LIGHTBLACK_EX

NUM_THREADS = 200

# Thread queue
q = Queue()
print_lock = Lock()

def port_scan(port):
    """
    Scan a port on the global variable `host`.
    """

    # Create a new socket
    s = socket.socket()
    try:
        # Try to connect to the host using the specified port.
        s.connect((host, port))
        # Set time out for faster speeds
        s.settimeout(0.2)
    except:
        # Cannot connect, port is closed
        with print_lock:
            print(f"{RED}{host:15}:{port:5} is closed {RESET}", end='\r')
    else:
        # The connection was established, the port is open!
        with print_lock:
            print(f"{GREEN}{host:15}:{port:5} is open {RESET}")
    finally:
        # Close the socket
        s.close()

def scan_thread():
    global q
    while True:
        # Get the port number from the queue
        worker = q.get()
        # Scan that port number
        port_scan(worker)
        # Tell the queue that the scanning for that port is done.
        q.task_done()

def main(host, ports):
    global q
    for t in range(NUM_THREADS):
        # For each thread, start it.
        t = Thread(target=scan_thread)

        # Thread will end when main thread ends
        t.daemon = True

        # Start the daemon thread
        t.start()

    for worker in ports:
        # For each port, put that port into the queue to start scanning.
        q.put(worker)
    
    # Wait for the threads to finish
    q.join()

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Multithreaded port scanner')
    parser.add_argument("host", help="The host to scan.")
    parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="Port range to scan, default is 1-65535 (all ports)")
    args = parser.parse_args()
    host, port_range = args.host, args.port_range

    start_port, end_port = port_range.split("-")
    start_port, end_port = int(start_port), int(end_port)

    ports = [ p for p in range(start_port, end_port) ]

    main(host, ports)



