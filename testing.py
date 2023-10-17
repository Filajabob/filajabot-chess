import subprocess
import statistics
import datetime
import time
import chess
import json
from chessboard import display

engine1 = input("Select engine #1 name: ")
engine2 = input("Select engine #2 name: ")

engine1_fp = f"testing/{engine1}.exe"
engine2_fp = f"testing/{engine2}.exe"

iterations = int(input("How many iterations should be run? "))
max_time = float(input("What should the max time per move be? (ms) ")) / 1000

print(f"Running {engine1} vs. {engine2} for {iterations} iterations...")

engine1_wins = 0
engine2_wins = 0
draws = 0

game_board = display.start(chess.Board().fen())

times = []

for i in range(iterations):
    if display.check_for_quit():
        break

    board = chess.Board()
    display.update(board.fen(), game_board)

    print(f"Match {i}... | {engine1}: {engine1_wins} wins - {engine2}: {engine2_wins} wins - {draws} draws")

    if i % 2 == 0:
        # engine1 is white
        print(f"{engine1} as white - {engine2} as black")

        start_time = time.time()
        while not board.is_game_over():
            if board.turn == chess.WHITE:
                move = subprocess.run(
                    [engine1_fp, board.fen(), str(max_time)],
                    text=True,  # Set to True to work with text data
                    stdout=subprocess.PIPE,  # Capture the standard output
                    stderr=subprocess.PIPE  # Capture the standard error (if needed))
                ).stdout

                if move not in [board.san(move) for move in board.legal_moves]:
                    print(f"Game complete in {round(time.time() - start_time, 2)} seconds.")
                    times.append(time.time() - start_time)
                    print(
                        f"Mean: {statistics.mean(times)} | Median: {statistics.median(times)} | Mode: {statistics.mode(times)}")
                    engine2_wins += 1
                    break
            else:
                move = subprocess.run(
                    [engine2_fp, board.fen(), str(max_time)],
                    text=True,  # Set to True to work with text data
                    stdout=subprocess.PIPE,  # Capture the standard output
                    stderr=subprocess.PIPE  # Capture the standard error (if needed))
                ).stdout

                if move not in [board.san(move) for move in board.legal_moves]:
                    print(f"Game complete in {round(time.time() - start_time, 2)} seconds.")
                    times.append(time.time() - start_time)
                    print(
                        f"Mean: {statistics.mean(times)} | Median: {statistics.median(times)} | Mode: {statistics.mode(times)}")
                    engine1_wins += 1
                    break

            board.push_san(move)
            display.update(board.fen(), game_board)

        else:
            print(f"Game complete in {round(time.time() - start_time, 2)} seconds.")
            times.append(time.time() - start_time)
            print(
                f"Mean: {statistics.mean(times)} | Median: {statistics.median(times)} | Mode: {statistics.mode(times)}")
            result = board.result()

            if result == "1-0":
                engine1_wins += 1
            elif result == "0-1":
                engine2_wins += 1
            else:
                draws += 1

    else:
        print(f"{engine2} as white - {engine1} as black")
        start_time = time.time()
        while not board.is_game_over():
            if board.turn == chess.WHITE:
                move = subprocess.run(
                    [engine2_fp, board.fen(), str(max_time)],
                    text=True,  # Set to True to work with text data
                    stdout=subprocess.PIPE,  # Capture the standard output
                    stderr=subprocess.PIPE  # Capture the standard error (if needed))
                ).stdout

                if move not in [board.san(move) for move in board.legal_moves]:
                    print(f"Game complete in {round(time.time() - start_time, 2)} seconds.")
                    times.append(time.time() - start_time)
                    print(
                        f"Mean: {statistics.mean(times)} | Median: {statistics.median(times)} | Mode: {statistics.mode(times)}")
                    engine1_wins += 1
                    break
            else:
                move = subprocess.run(
                    [engine1_fp, board.fen(), str(max_time)],
                    text=True,  # Set to True to work with text data
                    stdout=subprocess.PIPE,  # Capture the standard output
                    stderr=subprocess.PIPE  # Capture the standard error (if needed))
                ).stdout

                if move not in [board.san(move) for move in board.legal_moves]:
                    print(f"Game complete in {round(time.time() - start_time, 2)} seconds.")
                    times.append(time.time() - start_time)
                    print(
                        f"Mean: {statistics.mean(times)} | Median: {statistics.median(times)} | Mode: {statistics.mode(times)}")
                    engine2_wins += 1
                    break

            board.push_san(move)
            display.update(board.fen(), game_board)

        else:
            print(f"Game complete in {round(time.time() - start_time, 2)} seconds.")
            times.append(time.time() - start_time)
            print(
                f"Mean: {statistics.mean(times)} | Median: {statistics.median(times)} | Mode: {statistics.mode(times)}")
            result = board.result()

            if result == "1-0":
                engine2_wins += 1
            elif result == "0-1":
                engine1_wins += 1
            else:
                draws += 1

print("Testing complete.")
print(f"{engine1}: {engine1_wins} wins - {engine2}: {engine2_wins} wins - {draws} draws")

with open(f"testing/results/{engine1}-{engine2}-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json",
          'w') as f:
    data = {
        engine1: engine1_wins,
        engine2: engine2_wins,
        "draws": draws,
        "max_time": max_time
    }

    json.dump(data, f, indent=4)

display.terminate()
