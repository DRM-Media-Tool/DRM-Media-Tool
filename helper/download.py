import os
import zipfile
import urllib.request
from pathlib import Path
import shutil
from logger import setup_logging
from .progress import DownloadProgressDialog
from PyQt5.QtWidgets import QApplication

info_logger, debug_logger = setup_logging()

# Define dictionaries for each binary
binaries = [
    {
        'name': 'mp4decrypt',
        'download_link': 'https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-641.x86_64-microsoft-win32.zip',
        'binary_location': f'{os.getcwd()}/binaries/mp4decrypt.exe',
        'zip_location': f'{os.getcwd()}/downloads/temp/mp4decrypt.zip',
        'unzip_folder_location': f"{os.getcwd()}/downloads/temp/Bento4-SDK-1-6-0-641.x86_64-microsoft-win32/",
        'expected_executable': 'mp4decrypt.exe'
    },
    {
        'name': 'ffmpeg',
        'download_link': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip',
        'binary_location': f'{os.getcwd()}/binaries/ffmpeg.exe',
        'zip_location': f'{os.getcwd()}/downloads/temp/ffmpeg.zip',
        'unzip_folder_location': f"{os.getcwd()}/downloads/temp/ffmpeg-master-latest-win64-gpl/",
        'expected_executable': 'ffmpeg.exe'
    }
]


def check_binaries_exist(binaries):
    for binary_info in binaries:
        binary_location = Path(binary_info['binary_location'])
        if not binary_location.is_file():
            return True  # Return True if any binary is missing
    return False


def check_binaries_dir_exist(binaries):
    for binary_info in binaries:
        binaries_dir = Path(binary_info['binary_location']).parent
        if not binaries_dir.exists():
            return True  # Return True if any binaries directory is missing
    return False


def download_and_extract_binary(binary_info):
    # Check if any of the binaries or binaries directory is missing
    if check_binaries_exist([binary_info]) or check_binaries_dir_exist([binary_info]):
        # Check if QApplication is already instantiated
        if QApplication.instance() is None:
            app = QApplication([])
        else:
            app = QApplication.instance()

        # Create the progress dialog
        binary_name = binary_info['name']
        dialog = DownloadProgressDialog(binary_name)

        # Set window title with message
        dialog.setWindowTitle(f"Downloading {binary_name}")

        dialog.show()

        binary_location = Path(binary_info['binary_location'])

        # Check if the binary already exists
        if binary_location.is_file():
            info_logger.info(f"{binary_info['name']} is already present.")
            return

        # Create the binaries directory if it doesn't exist
        binaries_dir = binary_location.parent
        binaries_dir.mkdir(parents=True, exist_ok=True)

        # Create the downloads/temp directory if it doesn't exist
        temp_dir = Path(binary_info['unzip_folder_location'])
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Download the binary zip file with progress display
        def progress(count, block_size, total_size):
            percent = int(count * block_size * 100 / total_size)
            dialog.set_progress(percent)
            app.processEvents()  # Allow GUI updates

        urllib.request.urlretrieve(
            binary_info['download_link'], binary_info['zip_location'],
            reporthook=progress)

        # Extract the binary from the zip file
        with zipfile.ZipFile(binary_info['zip_location'], 'r') as zip_ref:
            # Get the list of files in the zip
            zip_file_contents = zip_ref.namelist()

            # Look for the expected executable within the zip file contents
            executable_file = next(
                (f for f in zip_file_contents if f.endswith(binary_info['expected_executable'])), None)

            # If found, extract and move the executable file to the binaries folder
            if executable_file:
                zip_ref.extract(executable_file,
                                binary_info['unzip_folder_location'])
                extracted_binary_path = Path(
                    binary_info['unzip_folder_location']) / executable_file
                os.rename(extracted_binary_path,
                          binary_info['binary_location'])
                info_logger.info(
                    f"{binary_info['name']} downloaded and extracted successfully.")
            else:
                debug_logger.debug(
                    f"Error: Executable file ({binary_info['expected_executable']}) not found in the zip file for {binary_info['name']}.")

        # Clean up: Remove the downloads folder after extraction
        shutil.rmtree(Path(os.getcwd()) / 'downloads')


# Check if any of the binaries or binaries directory is missing, then call the function to download and extract
if check_binaries_exist(binaries) or check_binaries_dir_exist(binaries):
    for binary_info in binaries:
        download_and_extract_binary(binary_info)
