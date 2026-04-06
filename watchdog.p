# =========================
# watchdog.py (AUTO RESTART)
# =========================

import subprocess
import time

while True:
    process = subprocess.Popen(["python3", "bot.py"])
    process.wait()
    print("Restarting bot in 5 seconds...")
    time.sleep(5)
