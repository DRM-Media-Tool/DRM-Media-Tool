import os
from datetime import datetime
import argparse


def get_channel_from_input():
    parser = argparse.ArgumentParser(
        description='Generate and update version information.')
    parser.add_argument('-c', '--channel', choices=[
                        'Beta', 'Stable', 'Dev'],
                        help='Select a channel (Stable, Beta or Dev)',
                        required=True)
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

# Read the existing versions from the file if it exists
file_path = "version.py"
existing_versions = []
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                existing_versions.append(
                    int(line.split("=")[1].strip().strip("'").split(".")[-1]))
                # print(existing_version)
                break

# Generate new version
if not existing_versions:
    # First time, use base version
    new_version = f"{base_version}.01"
else:
    # Increment the last two digits by finding the maximum and adding 1
    max_value = max(existing_versions)
    new_last_two_digits = str(max_value + 1).zfill(2)
    new_version = f"{base_version}.{new_last_two_digits}"

# Update version.py file
with open(file_path, "w") as f:
    f.write("\n")
    f.write(f"__version__ = '{new_version}'\n\n")
    f.write(f"CHANNEL = '{channel}'")
    f.write("\n")

# Print updated version
print(f"Version updated to: {new_version} for channel: {channel}")
