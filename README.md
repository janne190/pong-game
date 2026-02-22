# ARM Assembly Pong

A classic Pong game written entirely in ARM Assembly, running inside a custom Python-based emulator using the [Unicorn Engine](https://www.unicorn-engine.org/). The game renders directly in your terminal using ASCII graphics.
[![Web CAD Demo](https://img.youtube.com/vi/ucHH_omNkWA/maxresdefault.jpg)](https://www.youtube.com/watch?v=ucHH_omNkWA)
## Features

- **Pure ARM Assembly**: The core game logic, physics, and rendering are written in ARM assembly.
- **Python Runner**: A lightweight Python script acts as the "console hardware", providing memory mapping, input handling, and terminal-based video output.
- **Terminal Graphics**: Renders the game state directly to the command line using ASCII characters.
- **Real-time Input**: Uses Windows API for responsive, real-time keyboard input.

## Requirements

- Python 3.x
- Windows OS (for `ctypes.windll.user32.GetAsyncKeyState` input handling)
- `unicorn` Python package

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/arm-assembly-pong.git
   cd arm-assembly-pong
   ```

2. Install the required dependencies:
   ```bash
   pip install unicorn
   ```

## How to Play

Run the Python emulator script:

```bash
python pong_runner.py
```

### Controls

- **W** or **Up Arrow**: Move paddle up
- **S** or **Down Arrow**: Move paddle down
- **Q**: Quit the game

## Architecture

The project is divided into two main parts:

1. **The Game Code (`code_1771774285_ok.s`)**: Contains the ARM assembly instructions for the game logic. It handles ball movement, collision detection, paddle movement, and drawing to the Video RAM (VRAM).
2. **The Emulator (`pong_runner.py`)**: Sets up the Unicorn emulator with a specific memory map:
   - `0x10000`: Code Segment (ROM)
   - `0x20000`: Data Segment (RAM)
   - `0x30000`: Video RAM (VRAM)
   - `0x40000`: Memory-Mapped I/O (MMIO) for input and RNG

The Python script continuously executes the ARM code frame by frame, reads the VRAM, and prints it to the terminal.

## License

MIT License
