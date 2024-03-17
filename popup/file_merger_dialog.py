from PyQt5.QtWidgets import (
    QWidget,
    QDialog,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QPushButton,
    QHBoxLayout,
    QTableWidgetItem,
    QCheckBox
)
import os
import json
import subprocess
import sys
from helper.message import show_error_message, show_success_message

current_dir = os.path.dirname(sys.executable)
ffmpeg_path = os.path.join(current_dir, 'binaries', 'ffmpeg ')


class FileMergerDialog(QDialog):
    def __init__(self, debug_logger, info_logger, folder_path, parent=None):
        super().__init__(parent)

        self.folder_path = folder_path

        self.setWindowTitle("Files Merger")
        self.setGeometry(100, 100, 600, 300)

        self.layout = QVBoxLayout()

        self.file_table_label = QLabel("Files in Directory:")
        self.file_table_widget = QTableWidget()
        self.file_table_widget.setColumnCount(
            3)  # Added a column for checkboxes
        self.file_table_widget.setHorizontalHeaderLabels(
            ["File Name", "Select", "Type"])

        self.merge_button = QPushButton("Merge")
        self.merge_button.clicked.connect(self.merge_files)

        self.layout.addWidget(self.file_table_label)
        self.layout.addWidget(self.file_table_widget)
        self.layout.addWidget(self.merge_button)

        self.setLayout(self.layout)

        self.populate_file_table()
        self.file_table_widget.setColumnWidth(0, 400)
        self.debug_logger = debug_logger
        self.info_logger = info_logger

    def populate_file_table(self):
        # Clear existing items in the table widget
        self.file_table_widget.setRowCount(0)

        try:
            # List only video and audio files in the specified directory
            video_files = [file for file in os.listdir(
                self.folder_path) if file.lower().endswith(('.mp4', '.mkv',
                                                            '.avi', '.webm'))]
            audio_files = [file for file in os.listdir(
                self.folder_path) if file.lower().endswith(('.mp3', '.wav',
                                                            '.ogg', '.m4a',
                                                            '.webm'))]

            # Add video files to the table widget
            for idx, file in enumerate(video_files):
                self.add_file_to_table(idx, file, "Video")

            # Add audio files to the table widget
            for idx, file in enumerate(audio_files, start=len(video_files)):
                self.add_file_to_table(idx, file, "Audio")

        except FileNotFoundError:
            # Handle the case where the specified directory does not exist
            self.file_table_widget.setRowCount(1)
            self.file_table_widget.setItem(
                0, 2, QTableWidgetItem("Directory not found"))

    def add_file_to_table(self, idx, file, file_type):
        self.file_table_widget.insertRow(idx)

        # Center-align the content in the first column
        item_file_name = QTableWidgetItem(file)
        item_file_name.setTextAlignment(0x0004 | 0x0080)  # AlignCenter
        self.file_table_widget.setItem(idx, 0, item_file_name)

        # Create a widget for the checkbox and center-align it
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.addStretch(3)
        checkbox = QCheckBox()
        checkbox.setChecked(False)
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.addStretch(3)

        # Set the widget with the centered checkbox in the second column
        self.file_table_widget.setCellWidget(idx, 1, checkbox_widget)

        # Set the file type in the third column
        self.file_table_widget.setItem(idx, 2, QTableWidgetItem(file_type))

    def merge_files(self):
        selected_files = []
        metadata = {}
        for row in range(self.file_table_widget.rowCount()):
            checkbox = self.file_table_widget.cellWidget(
                row, 1).layout().itemAt(1).widget()
            if checkbox.isChecked():
                file_name = self.file_table_widget.item(row, 0).text()
                file_type = self.file_table_widget.item(row, 2).text()
                selected_files.append((file_name, file_type))

        # Check if there are at least one video and one audio file selected
        if any(file_type == 'Video' for (_, file_type) in selected_files) or \
                any(file_type == 'Audio' for (_, file_type) in selected_files):

            # Get all files in the directory ending with .info.json
            info_files = [file for file in os.listdir(
                self.folder_path) if file.endswith('.info.json')]
            img_files = [file for file in os.listdir(
                self.folder_path) if file.lower().endswith(('.jpg', '.jpeg',
                                                            '.png', '.webp'))]
            language_mapping = {
                'en': 'eng',
                'eng': 'eng',
                'english': 'eng',
                'ta': 'tam',
                'tamil': 'tam',
                'tam': 'tam'
            }

            # Define language codes
            language_codes = list(language_mapping.keys())
            suffixes = tuple(f'.{code}.vtt' for code in language_codes)
            subtitle_files = [file for file in os.listdir(
                self.folder_path) if file.endswith(suffixes)]
            thumbnail_file = None  # Initialize with a default value
            # print(subtitle_files)

            if not info_files:
                show_error_message(self, "Error: No Metadata files found.")
                self.debug_logger.debug("Error: No Metadata files found.")
            else:
                # Assume the first found .info.json file
                # print(selected_files)
                info_file_name = info_files[0]
                info_file_path = os.path.join(self.folder_path, info_file_name)
                with open(info_file_path, 'r', encoding='utf-8') as info_file:
                    metadata = json.load(info_file)
            if not subtitle_files:
                show_error_message(self, "Error: No Subtitle files found.")
                self.debug_logger.debug("Error: No Subtitle files found.")
            if img_files:
                thumbnail_file = os.path.join(self.folder_path, img_files[0])
            else:
                print("No matching files found.")
                self.debug_logger.debug("No matching files found.")

            # Build the ffmpeg command
            ffmpeg_command = (f'{ffmpeg_path}')

            # Lists to store input options for video, audio, and subtitle
            video_inputs = []
            audio_inputs = []
            subtitle_inputs = []
            # Initialize an array to store metadata strings
            metadata_strings_array = []

            for file_info in selected_files:
                input_file_path = os.path.join(self.folder_path, file_info[0])
                if file_info[1] == 'Video':
                    video_inputs.append(f'-i "{input_file_path}" ')
                    # Extract the extension from the video file
                    # extension = os.path.splitext(input_file_path)[1]
                elif file_info[1] == 'Audio':
                    audio_inputs.append(f'-i "{input_file_path}" ')

            # Add subtitle inputs from the provided list
            for i, sub in enumerate(subtitle_files):
                for code in language_codes:
                    if f'.{code}.' in sub:
                        lang = language_mapping.get(code, 'Unknown')
                        if lang.lower() == 'eng':
                            title = 'English'
                        elif lang.lower() == 'tam':
                            title = 'Tamil'
                        else:
                            title = 'Unknown'
                        metadata_data = f'-metadata:s:s:{i} language="{lang}" -metadata:s:s:{i} title="{title}" '
                        metadata_strings_array.append(metadata_data)
                        subtitle_inputs.append(
                            f'-i "{os.path.join(self.folder_path, sub)}" ')
                        break

            # Combine the video, audio, and subtitle input options
            ffmpeg_command += ''.join(video_inputs) + \
                ''.join(audio_inputs) + ''.join(subtitle_inputs)
            # print(subtitle_file)

            # Prepare the output file name
            title_name = metadata.get(
                "title", os.path.basename(self.folder_path))
            release_year = metadata.get("release_year", "")
            year_suffix = f' ({release_year})' if release_year else ''
            output_file = f'{title_name.replace(":", " ").replace("?", "")} {year_suffix}.mp4'
            # Handle the case where the file already exists
            co = 1
            while os.path.exists(os.path.join(self.folder_path, output_file)):
                # Replace spaces with underscores and colons with empty spaces
                title_name = metadata.get(
                    "episode", os.path.basename(self.folder_path))
                release_year = metadata.get("release_year", "")
                year_suffix = f' ({release_year})' if release_year else ''

                output_file = f'{title_name.replace(":", " ").replace("?", "")} {year_suffix} ({co}).mp4'
                co += 1

            # Convert the genres to a string with semicolons as separators
            if "genres" in metadata:
                genre_string = ';'.join(metadata["genres"])
            elif "genre" in metadata:
                genre_string = ';'.join(metadata["genre"])
            else:
                genre_string = ""

            if "artists" in metadata:
                actor_string = ';'.join(metadata["artists"])
            elif "artist" in metadata:
                actor_string = ';'.join(metadata["artist"])
            else:
                actor_string = ""

            if "release_year" in metadata:
                release_year = metadata.get("release_year", "")
            elif "upload_date" in metadata:
                upload_date = metadata.get("upload_date")
                release_year = upload_date[:4]
            else:
                release_year = ""

            if thumbnail_file is not None:
                ffmpeg_command += f'-i "{thumbnail_file}" '

            # Add metadata and subtitle merging options to the ffmpeg command
            ffmpeg_command += (
                f'-c:v copy '
                f'-c:a copy '
                f'-c:s mov_text '  # Use the determined subtitle codec
                f'-c:v:1 png '
            )
            ffmpeg_command += ''.join(metadata_strings_array)

            if not info_files:
                ffmpeg_command += (
                    f'-metadata genre="{genre_string}" '
                    f'-metadata handler_name="Amazon Prime Video" '
                    f'-metadata encoder="FFmpeg" '
                )
            else:
                ffmpeg_command += (
                    '-metadata title="{}" '
                    '-metadata comment="{}" '
                    '-metadata COPYRIGHT="{}" '
                    '-metadata Artist="{}" '
                    '-metadata date="{}" '
                    '-metadata genre="{}" '
                    '-metadata handler_name="Amazon Prime Video" '
                    '-metadata encoder="FFmpeg" '
                ).format(
                    metadata.get("title", metadata.get("episode", "")),
                    metadata.get("description", "").replace("\"", ""),
                    metadata.get("extractor_key", ""),
                    actor_string,
                    release_year,
                    genre_string,
                )

            ffmpeg_command += (
                # Map all video, audio, and subtitle streams
                f'-map 0:v ' + ' '.join([f'-map {i + 1}:a' for i in range(len(audio_inputs))]) +
                ' ' + ' '.join([f'-map {i + 1 + len(audio_inputs)}:s' for i in range(len(subtitle_inputs))]) +
                ' ' + ' '.join([f'-map { 1 + (len(audio_inputs) + len(subtitle_inputs))}']
                               ) if thumbnail_file is not None else ''
            )

            ffmpeg_command += (
                ' -disposition:v:1 attached_pic '  # Set subtitle stream as default
                f'-movflags +faststart '  # Enable faststart for streaming
                f'-strict experimental '  # Necessary for using the AAC codec
                f'"{os.path.join(self.folder_path, output_file)}"'
            )

            # Run the ffmpeg command
            try:
                print(ffmpeg_command)
                subprocess.run(ffmpeg_command, shell=True, check=True)
                # Assuming you have access to the close method of your window
                self.close()
                success_message = "Files Merged successfully."
                show_success_message(self, success_message)
                self.info_logger.info(success_message)
            except subprocess.CalledProcessError as e:
                # Handle the error if ffmpeg command fails
                show_error_message(self, f"Error during merging: {e}")
                self.debug_logger.debug(f"Error during merging: {e}")
                return False, f"Error during merging: {e}"
        else:
            show_error_message(
                self, "Please select at least two files for merging.")
            self.debug_logger.debug(
                "Please select at least two files for merging.")
