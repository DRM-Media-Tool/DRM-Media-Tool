import os
import requests
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QApplication
from bs4 import BeautifulSoup
from helper.message import show_error_message, show_success_message
import sqlite3


class UploadCDMDialog(QDialog):
    def __init__(self, debug_logger, info_logger):
        super().__init__()

        self.debug_logger = debug_logger
        self.info_logger = info_logger

        self.setWindowTitle('Upload Your CDM')
        self.setGeometry(100, 100, 400, 200)

        main_layout = QVBoxLayout()

        device_id_layout = QGridLayout()
        device_id_layout.setSpacing(5)

        device_id_label = QLabel('Device ID:')
        self.device_id_edit = QLineEdit()
        device_id_upload_button = QPushButton('Upload File')
        device_id_upload_button.clicked.connect(self.upload_device_id_file)
        device_id_layout.addWidget(device_id_label, 1, 0)
        device_id_layout.addWidget(self.device_id_edit, 1, 1)
        device_id_layout.addWidget(device_id_upload_button, 1, 2)

        private_key_layout = QGridLayout()
        private_key_layout.setSpacing(5)

        private_key_label = QLabel('Private Key:')
        self.private_key_edit = QLineEdit()
        private_key_upload_button = QPushButton('Upload File')
        private_key_upload_button.clicked.connect(self.upload_private_key_file)
        private_key_layout.addWidget(private_key_label, 2, 0)
        private_key_layout.addWidget(self.private_key_edit, 2, 1)
        private_key_layout.addWidget(private_key_upload_button, 2, 2)

        submit_layout = QHBoxLayout()
        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.handle_submit_click)
        submit_layout.addWidget(submit_button)

        main_layout.addLayout(device_id_layout)
        main_layout.addLayout(private_key_layout)
        main_layout.addLayout(submit_layout)
        self.setLayout(main_layout)

    def upload_device_id_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, 'Select Device ID File')
        if file_path:
            self.device_id_edit.setText(file_path)

    def upload_private_key_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, 'Select Private Key File')
        if file_path:
            self.private_key_edit.setText(file_path)

    def handle_submit_click(self):
        device_id_file_path = self.device_id_edit.text()
        private_key_file_path = self.private_key_edit.text()

        if device_id_file_path and private_key_file_path:
            # Prepare headers with X-API-Key
            headers = {'X-API-Key': os.getenv("X_API_KEY")}

            # Prepare files for upload
            files = {
                'blob': ('device_id_file.txt', open(device_id_file_path, 'rb')),
                'key': ('private_key_file.txt', open(private_key_file_path, 'rb'))
            }
            print(files)

            # Prepare the URL
            base_url = os.getenv("API_URL")
            path = "/upload"
            url = f"{base_url.rstrip('/')}{path}"

            try:
                # Send the POST request with files and headers
                response = requests.post(url, files=files, headers=headers)
                response_text = response.text

                # Handle the response
                if response.status_code in [200, 302]:
                    soup = BeautifulSoup(response_text, 'html.parser')
                    h1_section_titles = soup.find_all(
                        'h1', class_='section-title')

                    # Extract the text within the <h1> tag
                    if len(h1_section_titles) >= 2:
                        extracted_value = h1_section_titles[1].text.strip()
                        conn = sqlite3.connect('db.db')
                        cursor = conn.cursor()

                        # Create a new table if not exists
                        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS cdm (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                device_info TEXT
                            )
                        ''')
                        cursor.execute(
                            'INSERT INTO cdm (device_info) VALUES (?)', (extracted_value,))
                        conn.commit()

                        conn.close()

                        success_message = f"New CDM Uploaded: {extracted_value}."
                        show_success_message(self, success_message)
                        self.info_logger.info(success_message)
                    else:
                        print("Could not find the specified second <h1> tag.")
                else:
                    error_message = "API ERROR."
                    show_error_message(self, error_message)
                    self.info_logger.info(error_message)
            except requests.RequestException as e:
                print(f'Error sending request: {e}')
        else:
            print('Please select both Device ID and Private Key files before submitting')
