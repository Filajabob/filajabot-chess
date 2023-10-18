# The Filajabot Chess Engine v0.2.1-beta

## Overview

Filajabot is a Python chess engine which can interactively play chess with a human 
(cli.py or gui.py) or calculate the best move from a FEN string (via search.py). You're probably better off with Stockfish tho

## Utilizes

- Minimax algorithm (with alpha-beta pruning)
- Move ordering (MVV-LVA, SEE)
- Robust evaluation at leaf nodes (middle-game/end-game dynamic values, piece tables)
  - See more about Filajabot's evaluation here: [PeSTO](https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function)
- Opening and Endgame book/tablebase probing
- Quiescent search
- More to come

## Features
- Interactive CLI to play against the bot (cli.py)
- GUI to play against the bot (.exe coming soon!)
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
2. Install the executable(s) you wish to use.
3. Install the source code.
4. Navigate to your downloaded files. Decompress and open the source code.
5. Insert the exectuable(s) into the source code folder.
6. You can now run the exectuable(s) as you wish. You may also create a shortcut for easier access.

#### Source Code
1. Navigate to the Releases panel and select the latest release.
2. Install the source code.
3. Decompress and open the folder.
4. Confirm you have installed all **Prerequisites**.
5. Run `cli.py` for an interactive game.

You can choose to run `search.py [FEN] [max_time]` or `FilajabotAPI_v021_beta.exe [FEN] [max_time]` for a single position evaluation.
