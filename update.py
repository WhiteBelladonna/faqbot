import time
import subprocess
import sys
print("Waiting for Bot to Shut down.")
time.sleep(10)
print("Pulling Update")
subprocess.call("git pull https://github.com/d3molite/faqbot")
time.sleep(10)
subprocess.Popen([sys.executable, "./faqbot.py"], shell=True)