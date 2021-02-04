#!/usr/bin/env python3

import socket
import time
import subprocess
import requests
import os


def check():
    try:
        host = socket.gethostbyname("www.google.com")
        s = socket.create_connection((host, 80), 2)
        return True
    except Exception:
        return False


status = False
domain = "http://127.0.0.1:8000/"
api = "robotarium-api/v1.0/robot-status/"
hostname = "autobot1"

while True:
    if check() == True and check() != status:
        form_data = {'robot': hostname, 'status': check()}
        resp = requests.put(domain + api, data=form_data)
    elif check() == False and check() != status:
        form_data = {'robot': hostname, 'status': check()}
        resp = requests.put(domain + api, data=form_data)
    status = check()
    time.sleep(4)
