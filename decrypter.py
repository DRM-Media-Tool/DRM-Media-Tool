from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QListWidget
    )
import os
import sys
import sqlite3
import subprocess
from popup.file_merger_dialog import FileMergerDialog
from helper.message import show_error_message, show_success_message

current_dir = os.path.dirname(sys.executable)
mp4decrypt = os.path.join(current_dir, 'binaries', 'mp4decrypt')


class Decrypter(QWidget):
    def __init__(self, debug_logger, info_logger):
        super().__init__()
        self.init_ui()
        self.conn = None  # Database connection
        self.cursor = None  # Database cursor
        self.debug_logger = debug_logger
        self.info_logger = info_logger
        self.create_database()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create a horizontal layout for the "Select Folder" and folder path
        select_folder_layout = QHBoxLayout()
        select_folder_label = QLabel("Select Folder:")
        select_button = QPushButton("Select Folder")
        select_button.clicked.connect(self.browse_folder)
        self.folder_path_lineedit = QLineEdit()

        select_folder_layout.addWidget(select_folder_label)
        select_folder_layout.addWidget(select_button)
        select_folder_layout.addWidget(self.folder_path_lineedit)

        layout.addLayout(select_folder_layout)

        # Create horizontal layout for buttons (Check Folder, GetKeys, Decrypt)
        buttons_layout = QHBoxLayout()

        check_folder_button = QPushButton("Check Folder")
        check_folder_button.clicked.connect(self.check_folder_existence)
        buttons_layout.addWidget(check_folder_button)

        get_keys_button = QPushButton("Get Keys from DB")
        get_keys_button.clicked.connect(self.get_keys_from_db)
        buttons_layout.addWidget(get_keys_button)

        decrypt_button = QPushButton("Decrypt")
        decrypt_button.clicked.connect(self.decrypt_files)
        buttons_layout.addWidget(decrypt_button)

        merge_button = QPushButton("Media Merger")
        merge_button.clicked.connect(self.merger)
        buttons_layout.addWidget(merge_button)

        layout.addLayout(buttons_layout)

        # Create a QListWidget for displaying search results
        layout.addWidget(QLabel("Search Results:"))
        self.search_result_list = QListWidget()
        layout.addWidget(self.search_result_list)

        self.setLayout(layout)

    # Add these methods to handle button clicks
    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_path_lineedit.setText(folder_path)
            # self.search_database(folder_path)

    def check_folder_existence(self):
        folder_path = self.folder_path_lineedit.text()
        if os.path.exists(folder_path):
            show_success_message(self, "Folder exists.")
            self.info_logger.info("Folder exists.")
        else:
            show_error_message(self, "Folder does not exist.")
            self.debug_logger.debug("Folder does not exist.")

    def get_keys_from_db(self):
        folder_path = self.folder_path_lineedit.text()
        if os.path.exists(folder_path):
            keys_found = self.search_database(folder_path)
            # print(keys_found)
            if keys_found:
                success_message = "Keys retrieved successfully."
                show_success_message(self, success_message)
                self.info_logger.info(success_message)
            else:
                # Customize this message as needed
                error_message = "No keys found in the database."
                show_error_message(self, error_message)
                self.debug_logger.debug(error_message)
        else:
            show_error_message(self, "No Folder Found.")
            self.debug_logger.debug("No Folder Found.")

    def decrypt_files(self):
        folder_path = self.folder_path_lineedit.text()
        if os.path.exists(folder_path):
            decrypt = self.decrypt_file(folder_path)
            if decrypt:
                success_message = "Decryption successfully."
                show_success_message(self, success_message)
                self.info_logger.info(success_message)
            else:
                # Customize this message as needed
                error_message = "Decryption Failed."
                show_error_message(self, error_message)
                self.debug_logger.debug(error_message)
        else:
            show_error_message(self, "No Folder Selected.")
            self.debug_logger.debug("No Folder Selected.")

    def merger(self):
        folder_path = self.folder_path_lineedit.text()
        if os.path.exists(folder_path):
            self.file_merger(folder_path)
            self.info_logger.info("Files Merged Succesfully")
        else:
            show_error_message(self, "No Folder Selected.")
            self.debug_logger.debug("No Folder Selected.")

    def create_database(self):
        self.conn = sqlite3.connect('db.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pssh (
                pssh_id INTEGER PRIMARY KEY,
                pssh TEXT,
                license_url TEXT,
                movie_name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS keys (
                key_id INTEGER PRIMARY KEY,
                key TEXT,
                pssh_id INTEGER,
                FOREIGN KEY(pssh_id) REFERENCES pssh(pssh_id)
            )
        ''')
        self.conn.commit()

    def search_database(self, folder_name):
        self.search_result_list.clear()

        # Search DB for entries with a movie_name that matches the folder_name
        query = "SELECT rowid, movie_name FROM pssh WHERE movie_name = ?"
        pattern = os.path.basename(folder_name)
        self.cursor.execute(query, (pattern,))
        results = self.cursor.fetchall()
        keys = []

        for result in results:
            rowid, movie_name = result
            self.search_result_list.addItem(
                f"rowid: {rowid}, Movie Name: {movie_name}")

            # Search for keys based on the pssh_id
            keys_query = "SELECT key FROM keys WHERE pssh_id = ?"
            self.cursor.execute(keys_query, (rowid,))
            keys = self.cursor.fetchall()

            if not keys:
                # Customize this message as needed
                error_message = "No key found in DB."
                show_error_message(self, error_message)
                self.debug_logger.debug(error_message)
            else:
                self.info_logger.info("Keys Found in Database")
                for key in keys:
                    self.search_result_list.addItem(f"   Key: {key[0]}")
        return bool(keys)

    def decrypt_file(self, folder_name):
        self.search_result_list.clear()
        # Search DB for entries with a movie_name that matches the folder_name
        query = "SELECT rowid, movie_name FROM pssh WHERE movie_name = ?"
        pattern = os.path.basename(folder_name)
        self.cursor.execute(query, (pattern,))
        results = self.cursor.fetchall()
        keys = []

        for result in results:
            rowid, movie_name = result
            self.search_result_list.addItem(
                f"rowid: {rowid}, Movie Name: {movie_name}")

            # Search for keys based on the pssh_id
            keys_query = "SELECT key FROM keys WHERE pssh_id = ?"
            self.cursor.execute(keys_query, (rowid,))
            keys = self.cursor.fetchall()

        # Get video and audio files in the selected folder
        video_audio_formats = ['.mp4', '.avi', '.webm',
                               '.mkv', '.m4a', '.wav', '.flac', '.mp3']
        files = [f for f in os.listdir(folder_name) if os.path.isfile(
            os.path.join(folder_name, f))]
        video_audio_files = [f for f in files if os.path.splitext(
            f)[1].lower() in video_audio_formats]

        # self.search_result_list.addItem("\nVideo and Audio Files:")
        # print(files)
        for file in video_audio_files:
            # self.search_result_list.addItem(f"   {file}")

            # Decrypt the file using mp4decrypt
            decrypted_file = os.path.splitext(
                file)[0] + "_decrypted" + os.path.splitext(file)[1]
            input_file_path = os.path.normpath(os.path.join(folder_name, file))
            output_file_path = os.path.normpath(
                os.path.join(folder_name, decrypted_file))

            decrypt_command = [mp4decrypt]
            if not keys:
                # Customize this message as needed
                error_message = "No key found in DB."
                show_error_message(self, error_message)
            else:
                for key in keys:
                    decrypt_command.extend(["--key", key[0]])
            decrypt_command.extend([input_file_path, output_file_path])
            try:
                # print(decrypt_command)
                subprocess.run(decrypt_command, shell=True, check=True)
                self.search_result_list.addItem(
                    f"   Decrypted File: {decrypted_file}")
                # Remove the original input file
                os.remove(input_file_path)
                # Rename the decrypted file to the original file name
                os.rename(output_file_path, input_file_path)
                show_success_message(self, "Decryption successfully Completed")
                self.info_logger.info(
                    "Decryption of {decrypted_file} is successfully Completed")
                # # Ask the user if they want to delete the encrypted file
                # reply = QMessageBox.question(
                #     self, 'Delete Encrypted File',
                #    'Do you want to delete the encrypted file?',
                #     QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                # )
                # if reply == QMessageBox.Yes:
                #     # Code to delete the encrypted file
                #     self.search_result_list.addItem(
                #         f"   Deleted Encrypted File: {QMessageBox.Yes}")
                #     show_success_message(self,
                #         "Encrypted file deleted successfully")
            except subprocess.CalledProcessError as e:
                self.search_result_list.addItem(
                    f"   Error decrypting file: {e}")
                show_error_message(self, "Error decrypting file")
                self.debug_logger.debug("Error: {e}")
        return bool(keys)

    def file_merger(self, folder_name):
        file_merger_dialog = FileMergerDialog(
            self.debug_logger, self.info_logger, folder_name)
        file_merger_dialog.exec_()
