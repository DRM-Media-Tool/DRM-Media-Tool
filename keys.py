from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QGroupBox
)
import sqlite3
from datetime import datetime
import requests
from logger import setup_logging
from helper.message import show_error_message, show_success_message

info_logger, debug_logger = setup_logging()


def send_key(kid, license_url, key):
    api_url = 'https://cdm.infobus.in/receive_key'

    if not license_url:
        license_url = "None"

    data = {
        'kid': kid,
        'license_url': license_url,
        'keys': key
    }

    headers = {
        "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (Ktesttemp, like Gecko) "
                       "Chrome/90.0.4430.85 Safari/537.36"),
        "Content-Type": "application/json",
    }
    try:
        r = requests.post(api_url, headers=headers, json=data)
        if r.status_code in [200, 302]:
            info_logger.info(r.text)
            info_logger.info(r.status_code)
        else:
            debug_logger.debug(f"Response content:{r.text}")
            debug_logger.debug("Request failed with status "
                               f"code: {r.status_code}")
    except requests.exceptions.RequestException as e:
        debug_logger.debug("An error occurred:", e)


class Keys(QWidget):
    def __init__(self, debug_logger, info_logger):
        super().__init__()
        self.debug_logger = debug_logger
        self.info_logger = info_logger
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        group_box1 = QGroupBox("Keys")
        layout1 = QFormLayout()

        self.key_input1 = QLineEdit()
        self.key_input2 = QLineEdit()
        self.key_input3 = QLineEdit()
        self.name_input = QLineEdit()
        self.license_input = QLineEdit()

        layout1.addRow("Key 1:", self.key_input1)
        layout1.addRow("Key 2:", self.key_input2)
        layout1.addRow("Key 3:", self.key_input3)
        layout1.addRow("Name: ", self.name_input)
        layout1.addRow("License URL:", self.license_input)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.handle_submit_click)
        layout1.addWidget(submit_button)
        group_box1.setLayout(layout1)

        group_box2 = QGroupBox("JSON Data")
        layout2 = QVBoxLayout()
        coming_soon_label = QLabel("This section is coming soon.")
        layout2.addWidget(coming_soon_label)
        group_box2.setLayout(layout2)

        # Add Group Boxes to main layout
        main_layout.addWidget(group_box1)
        main_layout.addWidget(group_box2)

        self.setLayout(main_layout)

    def handle_submit_click(self):
        key_1 = self.key_input1.text()
        key_2 = self.key_input2.text()
        key_3 = self.key_input3.text()
        name = self.name_input.text()
        license_url = self.license_input.text()

        if not key_1 or not name:
            error_message = "Both 'Key' and 'Name' must be provided."
            show_error_message(self, error_message)
            self.debug_logger.debug(error_message)
            return

        try:
            kid_1, keyval_1 = key_1.split(":")
        except ValueError:
            error_message = "Invalid format for 'Key'. Must be 'kid:keyval'."
            show_error_message(self, error_message)
            self.debug_logger.debug(error_message)
            return

        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()

        pssh_data = ("", license_url, name, datetime.now())
        insert_pssh_query = "INSERT INTO pssh (pssh, license_url, movie_name, "
        "created_at) VALUES (?, ?, ?, ?)"
        cursor.execute(insert_pssh_query, pssh_data)
        pssh_id = cursor.lastrowid

        keys_data_1 = (key_1, pssh_id)
        insert_keys_query = "INSERT INTO keys (key, pssh_id) VALUES (?, ?)"
        cursor.execute(insert_keys_query, keys_data_1)

        if key_2:
            try:
                kid_2, keyval_2 = key_2.split(":")
                keys_data_2 = (key_2, pssh_id)
                cursor.execute(insert_keys_query, keys_data_2)
            except ValueError:
                error_message = "Invalid format for Key 2."
                show_error_message(self, error_message)
                self.debug_logger.debug(error_message)

        if key_3:
            try:
                kid_3, keyval_3 = key_3.split(":")
                keys_data_3 = (key_3, pssh_id)
                cursor.execute(insert_keys_query, keys_data_3)
            except ValueError:
                error_message = "Invalid format for Key 3"
                show_error_message(self, error_message)
                self.debug_logger.debug(error_message)

        conn.commit()

        show_success_message("keys Inserted Succesfully")
        send_key(kid_1, license_url, key_1)

        if key_2:
            send_key(kid_2, license_url, key_2)
        if key_3:
            send_key(kid_3, license_url, key_3)
