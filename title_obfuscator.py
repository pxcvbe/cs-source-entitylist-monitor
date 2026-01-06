import os
import sys
import random
import string
import threading
import time

# ==============================
# FAST title update
# ==============================
if os.name == "nt":
    import ctypes
    SetConsoleTitleW = ctypes.windll.kernel32.SetConsoleTitleW

    def update_title(title: str):
        SetConsoleTitleW(title)
else:
    def update_title(title: str):
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()

# ==============================
# Faster random generator
# ==============================
CHARS = string.ascii_letters + string.digits
RAND = random.SystemRandom()  # lebih cepat & aman

def get_random_string():
    length = random.randint(1, 35)
    return "".join(RAND.choice(CHARS) for _ in range(length))

# ==============================
# High-speed background thread
# ==============================
def title_obfuscator():
    while True:
        update_title(get_random_string())
        # time.sleep(0.05)  # 🔥 50ms (20x per second)

# ==============================
# Main
# ==============================
def call_title_obfuscator():
    threading.Thread(
        target=title_obfuscator,
        daemon=True
    ).start()