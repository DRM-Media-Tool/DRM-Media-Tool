import os
import zipfile
import urllib.request
from pathlib import Path
import shutil

# mp4decrypt dictionary
mp4decrypt = {
    'ZipName': 'mp4decrypt',
    'DownloadLink': 'https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-639.x86_64-microsoft-win32.zip',
    'BinaryLocation': f'{os.getcwd()}/binaries/mp4decrypt.exe',
    'UnzipBinaryLocation': f"{os.getcwd()}/downloads/temp/Bento4-SDK-1-6-0-639.x86_64-microsoft-win32/bin/mp4decrypt.exe",
    'UnzipFolderLocation': f"{os.getcwd()}/downloads/temp/Bento4-SDK-1-6-0-639.x86_64-microsoft-win32/",
    'ZipLocation': f'{os.getcwd()}/downloads/temp/mp4decrypt.zip'
}

# ffmpeg dictionary
ffmpeg = {
    'ZipName': 'ffmpeg',
    'DownloadLink': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip',
    'BinaryLocation': f'{os.getcwd()}/binaries/ffmpeg.exe',
    'UnzipBinaryLocation': f"{os.getcwd()}/downloads/temp/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe",
    'UnzipFolderLocation': f"{os.getcwd()}/downloads/temp/ffmpeg-master-latest-win64-gpl/",
    'ZipLocation': f'{os.getcwd()}/downloads/temp/ffmpeg.zip'
}


def download_and_extract_binary(binary_info):
    binary_location = Path(binary_info['BinaryLocation'])

    # Check if the binary already exists
    if binary_location.is_file():
        print(f"{binary_info['ZipName']} is already present.")
        return

    # Create the binaries directory if it doesn't exist
    binaries_dir = binary_location.parent
    binaries_dir.mkdir(parents=True, exist_ok=True)

    # Create the downloads/temp directory if it doesn't exist
    temp_dir = Path(binary_info['UnzipFolderLocation'])
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Download the binary zip file
    urllib.request.urlretrieve(
        binary_info['DownloadLink'], binary_info['ZipLocation'])

    # Extract the binary from the zip file
    with zipfile.ZipFile(binary_info['ZipLocation'], 'r') as zip_ref:
        # Get the list of files in the zip
        zip_file_contents = zip_ref.namelist()

        # Identify the actual executable file within the extracted folder
        executable_file = next((f for f in zip_file_contents if f.endswith('.exe')), None)

        # If found, extract and move the executable file to the binaries folder
        if executable_file:
            zip_ref.extract(executable_file, binary_info['UnzipFolderLocation'])
            extracted_binary_path = Path(
                binary_info['UnzipFolderLocation']) / executable_file
            os.rename(extracted_binary_path, binary_info['BinaryLocation'])
            print(
                f"{binary_info['ZipName']} downloaded and extracted successfully.")
        else:
            print(
                f"Error: Executable file not found in the zip file for {binary_info['ZipName']}.")

    # Remove the downloads folder after extraction
    shutil.rmtree(Path(os.getcwd()) / 'downloads')