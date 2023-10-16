import subprocess

version = input("Version: (xyz) ")

command = [
    "pyinstaller",
    "--noconfirm",
    "--onefile",
    "--console",
    "--hidden-import", "chess",
    "--hidden-import", "search",
    "--distpath", "./",
    "--name", f"FilajabotCLI_v{version}",
    "cli.py"
]

try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while running PyInstaller: {e}")