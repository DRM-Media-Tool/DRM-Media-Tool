from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QTextBrowser
import sqlite3
import requests
import json
import os
from helper.message import show_error_message
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, "assets", ".env")
key_path = os.path.join(current_dir, 'assets', 'serviceAccountKey.json')
load_dotenv(dotenv_path)
# Initialize Firebase
cred = credentials.Certificate(key_path)
firebase_app = initialize_app(cred)
db = firestore.client()


class KeyGeter(QWidget):
    def __init__(self, debug_logger, info_logger):
        super().__init__()
        self.debug_logger = debug_logger
        self.info_logger = info_logger
        self.init_ui()

    def init_ui(self):
        # Create layout
        layout = QVBoxLayout()

        # Create labels and input fields
        label1 = QLabel('PSSH:')
        label2 = QLabel('Licence URL:')
        label3 = QLabel('Name:')
        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input3 = QLineEdit()

        # To have input and lable on same line
        row_layout1 = QHBoxLayout()
        row_layout1.addWidget(label1)
        row_layout1.addWidget(self.input1)
        layout.addLayout(row_layout1)

        row_layout2 = QHBoxLayout()
        row_layout2.addWidget(label2)
        row_layout2.addWidget(self.input2)
        layout.addLayout(row_layout2)

        row_layout3 = QHBoxLayout()
        row_layout3.addWidget(label3)
        row_layout3.addWidget(self.input3)
        layout.addLayout(row_layout3)

        # Create a button
        button = QPushButton('Submit')

        # Add labels, input fields, and button to the layout
        layout.addWidget(button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Connect the button to a function (e.g., handle_button_click)
        button.clicked.connect(self.handle_button_click)

        # Create a text browser to display the API response
        self.response_browser = QTextBrowser()

        # Add the text browser to the layout
        layout.addWidget(self.response_browser)

        self.show()

    def handle_button_click(self):
        self.info_logger.info("Submit Button Clicked")
        # Get user input from the input fields
        pssh = self.input1.text()
        license_url = self.input2.text()
        name = self.input3.text()
        # Check if any field is empty
        if not name:
            self.info_logger.info("Name Field is Empty")

        if not pssh:
            self.info_logger.info("pssh Field is Empty")

        if not license_url:
            self.info_logger.info("license_url Field is Empty")

        conn = sqlite3.connect('db.db')
        self.info_logger.info("DB Connected Succesfully")
        cursor = conn.cursor()
        # Create a table with columns if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS pssh (
                        pssh TEXT,
                        license_url TEXT,
                        movie_name TEXT
                    )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys (
        key_id INTEGER PRIMARY KEY,
        key TEXT,
        pssh_id INTEGER,
        FOREIGN KEY (pssh_id) REFERENCES pssh (pssh_id)
        )
        ''')

        # Insert the values into the table
        cursor.execute("INSERT INTO pssh (pssh, license_url, movie_name) VALUES (?, ?, ?)",
                       (pssh, license_url, name))

        conn.commit()
        pssh_id = cursor.lastrowid

        # Construct the API request
        api_url = os.getenv("API_URL")
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (Ktesttemp, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
            "Content-Type": "application/json",
            "X-API-Key": os.getenv("X_API_KEY"),
        }
        # Check if either pssh or license_url is empty
        if not pssh or not license_url:
            error_message = "Both 'pssh' and 'license_url' must be provided."
            show_error_message(self, error_message)
            self.debug_logger.debug(error_message)
        else:
            payload = {
                "license_url": license_url,
                "pssh": pssh,
            }

            # Make the API request
            response = requests.post(api_url, headers=headers, json=payload)
            self.info_logger.info(response)
            data = json.loads(response.text)
            key = None
            # print(data)
            self.info_logger.info("API response is: %s", response)
            if response.status_code == 302:
                if "keys" in data:
                    keys = data["keys"]
                    if isinstance(keys, list):
                        if len(keys) == 1:
                            for key_info in keys:
                                if isinstance(key_info, str):
                                    key = key_info
                                elif isinstance(key_info, dict) and "key" in key_info:
                                    key = key_info["key"]
                                else:
                                    print('error')
                                    continue
                            cursor.execute(
                                "INSERT INTO keys (key, pssh_id) VALUES (?, ?)", (key, pssh_id))
                            # print("One key found")
                            self.info_logger.info("Single key found")
                        else:
                            # key_strings = keys
                            # key_string = ', '.join(key_strings)
                            # part = key_string.replace(
                            #     '[', '').replace(']', '').replace("'", "")
                            # key_parts = part.split(', ')
                            # key = "\n".join(key_parts)
                            # print(key)
                            # print("Multiple keys found")
                            self.info_logger.info("Multiple keys found")
                            key_strings = keys
                            for key_string in key_strings:
                                key = key_string.replace(
                                    '[', '').replace(']', '').replace("'", "")
                                cursor.execute(
                                    "INSERT INTO keys (key, pssh_id) VALUES (?, ?)", (key, pssh_id))
                    else:
                        key = keys
                        cursor.execute(
                            "INSERT INTO keys (key, pssh_id) VALUES (?, ?)", (key, pssh_id))
                        self.info_logger.info("Keys Found")
                else:
                    error_message = "No 'key' or 'keys' found in the JSON data."
                    show_error_message(self, error_message)
                    self.debug_logger.debug(error_message)
            elif response.status_code == 400:
                try:
                    error_message = response.json()["message"]
                    show_error_message(self, error_message)
                    self.info_logger.info(error_message)
                except Exception as e:
                    self.debug_logger.debug(e)
            else:
                error_message = "API ERROR."
                show_error_message(self, error_message)
                self.info_logger.info(error_message)

            current_datetime = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            event_data = {
                'pssh': pssh,
                'license_url': license_url,
                'movie_name': name,
                'keys': keys if "keys" in data else [],
                'datetime': current_datetime,
            }

            # 'events' is the name of the collection
            events_ref = db.collection('events')
            events_ref.add(event_data)

            self.info_logger.info("Key Added to Globa Db")

            # Display the API response in the text browser
            conn.commit()
            # Close the database connection
            conn.close()
            if key is not None:
                key_str = json.dumps(keys)
                self.response_browser.setText(key_str)
                # Clear the input fields
                self.input1.clear()
                self.input2.clear()
                self.input3.clear()
            else:
                error_message = "No keys to display."  # Customize this message as needed
                # show_error_message(self, error_message)
                self.debug_logger.debug(error_message)
