# The Filajabot Chess Engine v0.2.1-beta

## Overview

Filajabot is a Python chess engine which can interactively play chess with a human 
(cli.py) or calculate the best move from a FEN string (via search.py).

## Utilizes

- Minimax algorithm (with alpha-beta pruning)
- Move ordering (MVV-LVA, SEE)
- Robust evaluation at leaf nodes (middle-game/end-game dynamic values, piece tables)
  - See more about Filajabot's evaluation here: [PeSTO](https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function)

## Features
- Interactive CLI to play against the bot (cli.py)
- API for best move from a FEN string (search.py)

## Getting Started

### Prerequisites 

**These prerequisites are only required if you wish to use the source code.**

- Windows 10 (other operating systems not tested, attempt at your own risk)
- Python 3.10 (other versions not tested)
- Python prerequisites available in `requirements.txt`
  - Depending on usage, some packages may not be required.

### Installation

#### Executable (.EXE)
1. Navigate to the Releases panel and select the latest release.
2. Install the EXE file.
3. Run the file. If the program closes immediately, try **Source Code**, then insert the executable into the source code directory.

#### Source Code
1. Navigate to the Releases panel and select the latest release.
2. Install the source code.
3. Decompress and open the folder.
4. Confirm you have installed all **Prerequisites**.
5. Run `cli.py` for an interactive game.

You can choose to run `search.py [FEN] [max_time]` for a single position evaluation.