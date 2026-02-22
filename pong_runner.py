"""
ARM Retro Console v1.0 - Pong Runner
Executes an ARM assembly-written game in the Unicorn emulator.
Controls: W (Up) / S (Down) or Arrow keys. Q to quit.
"""
import sys
import time
import ctypes
import binascii
import threading
import struct
import random
from unicorn import *
from unicorn.arm_const import *

# Windows API: returns 0x8000 if the key is physically held down
_GetAsyncKeyState = ctypes.windll.user32.GetAsyncKeyState
def _key_held(vk): return bool(_GetAsyncKeyState(vk) & 0x8000)

VK_UP, VK_DOWN = 0x26, 0x28
VK_W,  VK_S    = 0x57, 0x53
VK_Q           = 0x51

# --- CONFIGURATION ---
CODE_ADDR  = 0x10000
DATA_ADDR  = 0x20000
VRAM_ADDR  = 0x30000
IO_ADDR    = 0x40000

CONSOLE_WIDTH  = 40
CONSOLE_HEIGHT = 20

# COMPILED HEX CODE OF THE GAME:
PONG_BINARY = (
    "2040a0e30446a0e10100a0e3001194e5010051e30b00000a0810a0e3001084e5041084e51410a0e3081084e50a10a0e30c1084e50110a0e3101084e5141084e50110a0e3001184e5085094e5106094e5065085e00c6094e5147094e5076086e0010056e3020000ca0170a0e3147084e5030000ea120056e3010000ba007067e2147084e5240055e30a0000ba040094e5011040e2012080e2010056e1050000ba020056e1030000ca107094e5007067e2107084e5140000ea030055e3120000ca000094e5011040e2012080e2010056e1040000ba020056e1020000ca0170a0e3107084e5080000ea000055e3010000ba270055e3040000da1450a0e30a60a0e30170a0e3107084e5147084e5085084e50c6084e50c0094e5041094e5010050e10b00000a050000ba041094e5110051e3070000aa011081e2041084e5040000ea041094e5020051e3010000da011041e2041084e53000a0e30006a0e12010a0e3202300e30110c0e4012052e2fcffff1a3000a0e30006a0e12d10a0e32820a0e30110c0e4012052e2fcffff1a3000a0e30006a0e1f83200e3030080e02d10a0e32820a0e30110c0e4012052e2fcffff1a005094e5020055e30250a0b3110055e31150a0c3005084e5015045e23000a0e30006a0e12810a0e3950106e0060080e0020080e27c10a0e30010c0e5280080e20010c0e5280080e20010c0e5045094e5020055e30250a0b3110055e31150a0c3045084e5015045e23000a0e30006a0e12810a0e3950106e0060080e0250080e27c10a0e30010c0e5280080e20010c0e5280080e20010c0e5085094e50c6094e5000055e30d0000ba270055e30b0000ca000056e3090000ba130056e3070000ca3000a0e30006a0e12810a0e3960107e0070080e0050080e04f10a0e30010c0e54000a0e30006a0e1001090e5010011e30400000a002094e5020052e3010000da012042e2002084e5020011e30400000a002094e5110052e3010000aa012082e2002084e5"
)

def init_emulator():
    """Creates and initializes the Unicorn emulator with the retro console memory map."""
    mu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    mu.mem_map(CODE_ADDR, 0x10000)
    mu.mem_map(DATA_ADDR, 0x10000)
    mu.mem_map(VRAM_ADDR, 0x1000)
    mu.mem_map(IO_ADDR, 0x1000)

    # Load the code
    binary = binascii.unhexlify(PONG_BINARY)
    mu.mem_write(CODE_ADDR, binary)
    return mu, len(binary)

def render_vram(mu):
    """Draws the VRAM to the terminal as ASCII characters."""
    vram = mu.mem_read(VRAM_ADDR, CONSOLE_WIDTH * CONSOLE_HEIGHT)

    # Move cursor to top-left corner using ANSI code (prevents flickering)
    sys.stdout.write("\033[H")

    lines = []
    lines.append("+" + "-" * CONSOLE_WIDTH + "+")
    for row in range(CONSOLE_HEIGHT):
        row_chars = []
        for col in range(CONSOLE_WIDTH):
            b = vram[row * CONSOLE_WIDTH + col]
            # Print only valid ASCII characters, otherwise space
            char = chr(b) if 32 <= b <= 126 else ' '
            row_chars.append(char)
        lines.append("|" + "".join(row_chars) + "|")
    lines.append("+" + "-" * CONSOLE_WIDTH + "+")
    lines.append("\nControls: W/S or Up/Down arrows. Q = Quit.")

    sys.stdout.write("\n".join(lines) + "\n")
    sys.stdout.flush()

def input_thread_func(mu, running):
    """Reads keyboard input using GetAsyncKeyState and updates the MMIO controller port (0x40000).
    Works on a 'held down' principle: the gamepad bit is 1 as long as the key is pressed."""
    while running[0]:
        if _key_held(VK_Q):
            running[0] = False

        buttons = 0
        if _key_held(VK_UP)   or _key_held(VK_W): buttons |= 1  # Up
        if _key_held(VK_DOWN) or _key_held(VK_S): buttons |= 2  # Down

        mu.mem_write(IO_ADDR, struct.pack("<I", buttons))
        time.sleep(0.01)  # 10ms polling interval

def run_game():
    if PONG_BINARY == "TÄHÄN_KOPIT_SEN_HEX_PÖTKÖN":
        print("Remember to copy the final hex code into the PONG_BINARY variable!")
        return

    mu, code_len = init_emulator()

    # Clear the entire console memory just in case
    mu.mem_write(DATA_ADDR, bytes(0x10000))
    mu.mem_write(VRAM_ADDR, bytes(0x1000))
    mu.mem_write(IO_ADDR, bytes(0x1000))

    # Clear the terminal
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

    running = [True]
    input_t = threading.Thread(target=input_thread_func, args=(mu, running), daemon=True)
    input_t.start()

    # Game loop
    try:
        while running[0]:
            # 1. Update Hardware RNG (0x40004)
            mu.mem_write(IO_ADDR + 4, struct.pack("<I", random.randint(0, 0xFFFFFFFF)))

            # 2. Run ARM code (one "frame")
            # timeout=50000 = 50ms, forces return even if code loops (b halt)
            mu.emu_start(CODE_ADDR, CODE_ADDR + code_len, timeout=50000)

            # 3. Draw VRAM to screen
            render_vram(mu)

            # 4. Game speed (FPS limiter)
            time.sleep(0.05)  # Adjust this if the game is too fast/slow

    except UcError as e:
        print(f"\nEmulator error: {e}")
    except KeyboardInterrupt:
        pass

    print("\nGame over.")

if __name__ == "__main__":
    run_game()
