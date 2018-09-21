import time
import subprocess
import sys
print("Waiting for Bot to Shut down.")
time.sleep(15)
subprocess.Popen([sys.executable, "./faqbot.py"], shell=True)