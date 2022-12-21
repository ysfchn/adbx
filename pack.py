import httpx
import platform
import sys
import shutil
import subprocess
from zipfile import ZipFile
from pathlib import Path

if len(sys.argv) not in [2, 3]:
    print("Usage: python pack.py (wheel_platform) [adb_platform]")
    exit(1)

CWD = Path(".").resolve()
PLATFORMS = ["linux", "darwin", "windows"]

# Remove old files.
shutil.rmtree((CWD / "dist"), ignore_errors = True)

# Download ADB for current OS.
adb_platform = platform.system().lower()

# Get wheel platform.
wheel = sys.argv[1]

# If a custom OS name has specified in arguments, use that instead.
if len(sys.argv) == 3:
    adb_platform = sys.argv[2].lower()

# Some OSes can return a blank value for platform.system().
if adb_platform not in PLATFORMS:
    print(f"Unsupported platform name '{adb_platform}'! Platform must be one of: {PLATFORMS}")
    sys.exit(1)

# Get binary download URL.
download_url = httpx.get(
    f"https://dl.google.com/android/repository/platform-tools-latest-{adb_platform}.zip", 
    follow_redirects = False
).headers["Location"]

version = download_url.replace('r', '').replace(' ', '').replace('_', '-').split('-')[-2]

# Write version information to __init__.py.
(CWD / "adbx" / "__init__.py").write_text(
    "__version__ = \"{0}\"".format(version)
)

# Set platform in setup.cfg
(CWD / "setup.cfg").write_text(
    "[bdist_wheel]\nplat-name={0}".format(wheel)
)

print(f"Downloading ADB for '{adb_platform}' version '{version}'...")

# Start downloading.
with httpx.stream("GET", download_url) as stream:
    with open("adb.zip", "wb") as file:
        for i in stream.iter_bytes(2048):
            file.write(i)

print("Unpacking...")

with ZipFile("adb.zip") as zipf:
    zipf.extractall("adbx/bin")

# Set executable flag for binaries in linux.
if platform.system() == "Linux":
    subprocess.run('chmod -R +x ./adbx/bin', shell = True)

print(f"Building wheel for '{wheel}'...")

subprocess.run('python -m pip wheel . --wheel-dir dist --no-cache-dir', shell = True)
# subprocess.run('python -m build -o dist -w -n .', shell = True)

print("Cleaning up...")

shutil.rmtree((CWD / "adbx" / "bin"), ignore_errors = True)
shutil.rmtree((CWD / "build"), ignore_errors = True)
shutil.rmtree((CWD / "adbx.egg-info"), ignore_errors = True)
(CWD / "setup.cfg").unlink(missing_ok = True)
(CWD / "adb.zip").unlink(missing_ok = True)
(CWD / "adbx" / "__init__.py").unlink(missing_ok = True)