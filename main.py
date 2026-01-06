# CS: Source Entity List Health Monitor All Player
# Educational tool for understanding source engine memory structures
# Created: by pxcvbe!
import pymem
import time
from colorama import Fore, Back, Style

# Constants
MAX_ENTITIES = 64

# Offsets (CS- Source updated)
OFFSETS_ENTITY_LIST = 0x006098C8
OFFSET_HEALTH = 0xD0
# Entity size to the next player
ENTITY_SIZE = 0x20

# Init
pm = pymem.Pymem("cstrike_win64.exe")

# Get module bases
client_base = pymem.process.module_from_name(
    pm.process_handle, "client.dll"
).lpBaseOfDll

# Pointer bases
entity_base_address = client_base + OFFSETS_ENTITY_LIST

# Main loop
while True:
    # line output
    line_output = []

    # Loop through entities
    for i in range(MAX_ENTITIES):
        try:
            entity_list_pointer = pm.read_ulonglong(entity_base_address + i * ENTITY_SIZE)

            # check valid pointer & skip invalid entities
            if not entity_list_pointer or entity_list_pointer < 0x10000:
                continue

            # read health value
            health = pm.read_int(entity_list_pointer + OFFSET_HEALTH)

            # check health
            if 0 < health <= 100:
                # print(f"PLAYER {i} HEALTH: {health}")
                line_output.append(f"[Player: {Fore.YELLOW}{i}{Fore.RESET} - HP: {Fore.GREEN}{health}{Fore.RESET}]")

        except Exception as e:
            print(f"Error: {e}")

    print(" | ".join(line_output).ljust(120), end="\r", flush=True)
    time.sleep(0.05)

        