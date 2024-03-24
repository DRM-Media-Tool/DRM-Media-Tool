import os
import requests
from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
    QFormLayout
)
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

        main_layout = QFormLayout()

        device_id_layout = QHBoxLayout()
        device_id_label = QLabel('Device ID:')
        self.device_id_edit = QLineEdit()
        device_id_upload_button = QPushButton('Select File')
        device_id_upload_button.clicked.connect(self.upload_device_id_file)
        device_id_layout.addWidget(device_id_label)
        device_id_layout.addWidget(self.device_id_edit)
        device_id_layout.addWidget(device_id_upload_button)
        main_layout.addRow(device_id_layout)

        private_key_layout = QHBoxLayout()
        private_key_label = QLabel('Private Key:')
        self.private_key_edit = QLineEdit()
        private_key_upload_button = QPushButton('Select File')
        private_key_upload_button.clicked.connect(self.upload_private_key_file)
        private_key_layout.addWidget(private_key_label)
        private_key_layout.addWidget(self.private_key_edit)
        private_key_layout.addWidget(private_key_upload_button)
        main_layout.addRow(private_key_layout)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.handle_submit_click)
        main_layout.addRow(submit_button)

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

        if not device_id_file_path or not private_key_file_path:
            error_message = "Both 'client_id' and 'private_key' "
            "must be provided."
            show_error_message(self, error_message)
            self.debug_logger.debug(error_message)

        if device_id_file_path and private_key_file_path:
            # Prepare headers with X-API-Key
            headers = {'X-API-Key': os.getenv("X_API_KEY")}

            # Prepare files for upload
            files = {
                'blob': (
                    'device_id_file.txt',
                    open(device_id_file_path, 'rb')
                ),
                'key': ('private_key.txt', open(private_key_file_path, 'rb'))
            }

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
                        id = h1_section_titles[1].text.strip()
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
                            'INSERT INTO cdm (device_info) VALUES (?)', (id,))
                        conn.commit()

                        conn.close()

                        success_message = f"New CDM Uploaded: {id}."
                        show_success_message(self, success_message)
                        self.info_logger.info(success_message)
                    else:
                        self.debug_logger.debug("Could not find the "
                                                "specified Build Info.")
                else:
                    error_message = "API ERROR."
                    show_error_message(self, error_message)
                    self.info_logger.info(error_message)
            except requests.RequestException as e:
                self.debug_logger.debug(f'Error sending request: {e}')
        else:
            self.debug_logger.debug(
                'Please select both files before submitting')
