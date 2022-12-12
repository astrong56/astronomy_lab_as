#!/usr/bin/env python3

import requests
import datetime
import json

response = requests.post("http://ip-api.com/batch", json=[
  {"query": "18.208.32.56"},
  {"query": "18.208.32.56"},
]).json()

for ip_info in response:
    print(ip_info["lat"], ip_info["lon"])