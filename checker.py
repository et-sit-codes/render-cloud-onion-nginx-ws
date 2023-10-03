"""checker"""
import os
import time

while True:
    if os.path.isfile("./tor_server/torrc.in"):
        break
    time.sleep(0.3)
