import os
import random
from datetime import datetime
import argparse


def get_channel_from_input():
    parser = argparse.ArgumentParser(
        description='Generate and update version information.')
    parser.add_argument('-c', '--channel', choices=[
                        'Beta', 'Stable'], help='Select a channel (Beta or Stable)', required=True)
    args = parser.parse_args()
    return args.channel


# Prompt user to select a channel
# channel = input("Enter the channel number (1 or 2): ")
channel = get_channel_from_input()

# Get current date in the specified format (YYYY.MM.DD)
now = datetime.now()
year = now.year
month = now.month
day = now.day

# Build the base version string
base_version = f"{year}.{month:02d}.{day:02d}"

# Read the existing version from the file if it exists
file_path = "version.py"
existing_version = None
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                existing_version = line.split("=")[1].strip().strip("'")
                # print(existing_version)
                break

# Generate new version
if not existing_version:
    # First time, use base version
    new_version = base_version
else:
    # Append random 4-digit increment for Beta channel or use base version for Stable channel
    if channel == "Beta":
        new_version = f"{base_version}.{random.randint(1000, 9999)}"
    else:
        new_version = f"{base_version}.{random.randint(1000, 9999)}"

# Update version.py file
with open(file_path, "w") as f:
    f.write("\n")
    f.write(f"__version__ = '{new_version}'\n\n")
    f.write(f"CHANNEL = '{channel}'")
    f.write("\n")

# Print updated version
print(f"Version updated to: {new_version} for channel: {channel}")
