# CS: Source Entity List Health Monitor All Player
# Educational tool for understanding source engine memory structures
# Created: by pxcvbe!
import pymem
import time
import sys
from colorama import Fore, Back, Style, init
from typing import Optional
from title_obfuscator import call_title_obfuscator

# Color init
init()

# Constants
PROCESS_NAME = "cstrike_win64.exe"
MODULE_NAME = "client.dll"
OFFSETS = {
    "ENTITY_LIST": 0x006098C8,
    "HEALTH": 0xD0
}
MAX_ENTITIES = 64
# Entity size to the next player
ENTITY_SIZE = 0x20
REFRESH_RATE = 0.05
SHOW_INDEX = True
HEALTH_MIN = 1
HEALTH_MAX = 100
VALIDATE_POINTERS = True
MIN_POINTER_VALUE = 0x10000000
DEBUG = False

class EntityHealthMonitor:
    """Monitor player health by reading game memory"""

    def __init__(self):
        self.pm: Optional[pymem.Pymem] = None
        self.client_base: int = 0
        self.entity_base_address: int = 0
        self.running: bool = False

    def initialize(self) -> bool:
        """Initialize memory connection"""
        try:
            print(f"[*] Connecting to {Fore.GREEN}{PROCESS_NAME}{Fore.RESET}...")
            self.pm = pymem.Pymem(PROCESS_NAME)

            print(f"[*] Getting {Fore.GREEN}{MODULE_NAME}{Fore.RESET} base address...")
            client_module = pymem.process.module_from_name(
                self.pm.process_handle,
                MODULE_NAME
            )
            self.client_base = client_module.lpBaseOfDll

            self.entity_base_address = self.client_base + OFFSETS.get("ENTITY_LIST")

            print(f"[+] {Fore.GREEN}Successfully connected!{Fore.RESET}")
            print(f"[+] Client base: {Fore.YELLOW}0x{self.client_base:X}{Fore.RESET}")
            print(f"[+] Entity list: {Fore.YELLOW}0x{self.entity_base_address:X}{Fore.RESET}")
            print(f"[+] Monitoring {MAX_ENTITIES} entities...")
            print("-" * 80)

            return True
        
        except pymem.exception.ProcessNotFound:
            print(f"[!] Error: {PROCESS_NAME} not found!")
            print(f"[!] Make sure CS:Source is running")
            return False
        except pymem.exception.ModuleNotFoundError:
            print(f"[!] Error: {MODULE_NAME} not found!")
            print(f"[!] Make sure you're using CS:S x64 version")
            return False
        except Exception as e:
            print(f"[!] Unexpected Error: {e}")
            return False
        
    def read_entity_pointer(self, index: int) -> Optional[int]:
        """Read entity pointer at given index"""
        try:
            address = self.entity_base_address + index * ENTITY_SIZE
            pointer = self.pm.read_ulonglong(address)

            # Validate pointer
            if VALIDATE_POINTERS:
                if not pointer or pointer < MIN_POINTER_VALUE:
                    return None
                
            if DEBUG:
                print(f"[DEBUG] Index {index}: 0x{pointer:X}")

            return pointer
        
        except Exception as e:
            if DEBUG:
                print(f"[DEBUG] Error reading index {index}: {e}")
            return None

    def read_entity_health(self, entity_ptr: int) -> Optional[int]:
        """Read health value from entity pointer"""
        try:
            health = self.pm.read_int(entity_ptr + OFFSETS.get("HEALTH"))

            # Validate health range
            if HEALTH_MIN <= health <= HEALTH_MAX:
                return health
            
            return None
        
        except Exception as e:
            if DEBUG:
                print(f"[DEBUG] Error reading health: {e}")
            return None

    def scan_entities(self) -> list:
        """Scan all entities and return list of player with health"""
        players = []

        for i in range(MAX_ENTITIES):
            entity_ptr = self.read_entity_pointer(i)

            if not entity_ptr:
                continue

            health = self.read_entity_health(entity_ptr)

            if health is not None:
                players.append({
                    "index": i,
                    "health": health,
                    "pointer": entity_ptr
                })

        return players
    
    def format_output(self, players: list) -> str:
        """Format player data for display"""
        if not players:
            return "No players detected"
        
        output_parts = []
        for player in players:
            if SHOW_INDEX:
                output_parts.append(f"[PLAYER_IDX: {Fore.LIGHTYELLOW_EX}{player['index']}{Fore.RESET}] HP:{Fore.LIGHTGREEN_EX}{player['health']}{Fore.RESET}")
            else:
                output_parts.append(f"HP:{player['health']}")
        
        return " | ".join(output_parts)

    def run(self):
        """Main monitoring loop"""
        if not self.initialize():
            return
        
        self.running = True

        try:
            while self.running:
                players = self.scan_entities()
                output = self.format_output(players)

                # Clear line and print output
                print(f"\r{output}".ljust(160), end="", flush=True)

                time.sleep(REFRESH_RATE)
        except KeyboardInterrupt:
            print(f"\n[*] {Fore.RED} Monitoring stopped by user {Fore.RESET}")
        except pymem.exception.MemoryReadError:
            print(f"\n[!] {Fore.YELLOW} Lost connection to game process {Fore.RESET}")
        except Exception as e:
            print(f"\n[!] Unexpected error: {e}")
        # Always cleanup
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup resources"""
        self.running = False
        if self.pm:
            try:
                self.pm.close_process()
            except:
                pass
        print("\n[*] Cleanup complete!")

def print_banner():
    """Print application banner"""
    banner = f"""
    {Fore.LIGHTBLUE_EX}
            ____ ___ _   _ _____ ___ ______  __     _   ___  
     _ __  / ___|_ _| \ | |_   _|_ _|  _ \ \/ /    / | / _ \ 
    | '_ \| |  _ | ||  \| | | |  | || |_) \  /     | || | | |
    | | | | |_| || || |\  | | |  | ||  __//  \     | || |_| |
    |_| |_|\____|___|_| \_| |_| |___|_|  /_/\_\    |_(_)___/                                            
    {Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}
    ╔═══════════════════════════════════════════════╗
    ║  CS:S Entity List Health Monitor              ║
    ║  ⚠️ Educational Purpose Only                  ║
    ╚═══════════════════════════════════════════════╝
    {Fore.RESET}
    """
    print(banner)

def main():
    """Main entry point"""
    print_banner()

    print()

    """ Call Title Obfuscator"""
    call_title_obfuscator()

    # Create and run monitor
    monitor = EntityHealthMonitor()
    monitor.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[!] Fatal error: {e}")
        sys.exit(1)
