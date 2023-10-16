import subprocess

version = input("Version: (xyz) ")

command = [
    "pyinstaller",
    "--noconfirm",
    "--onefile",
    "--console",
    "--hidden-import", "chess",
    "--hidden-import", "chess.polygot",
    "--hidden-import", "minimax",
    "--hidden-import", "constants",
    "--hidden-import", "logger",
    "--hidden-import", "result",
    "--hidden-import", "requests",
    "--distpath", "testing",
    "--name", f"version{version}",
    "search.py"
]

try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while running PyInstaller: {e}")
