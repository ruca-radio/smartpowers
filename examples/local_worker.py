#!/usr/bin/env python3
"""Deterministic protocol fixture; replace the command with a real harness."""
import json
import sys

request = json.load(sys.stdin)
parents = ', '.join(request['dependencies']) or 'none'
json.dump({'version':1,'status':'completed',
           'output':f"Task {request['task']['id']} processed; dependencies: {parents}",
           'evidence':['Local protocol worker executed']},sys.stdout)
