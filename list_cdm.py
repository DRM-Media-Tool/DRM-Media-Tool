from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QTextBrowser,
    QPlainTextEdit,
    QComboBox,
    QFormLayout
)
import os
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, "assets", ".env")
load_dotenv(dotenv_path)


class Cdm(QWidget):
    def __init__(self, debug_logger, info_logger):
        super().__init__()
        self.debug_logger = debug_logger
        self.info_logger = info_logger
        self.init_ui()

    def init_ui(self):
        # Create layout
        layout = QVBoxLayout()

        # Create a FormLayout
        form_layout = QFormLayout()

        # labels and input fields
        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input3 = QLineEdit()
        self.input4 = QPlainTextEdit()
        self.input5 = QLineEdit()
        self.input6 = QComboBox()

        # Add labels and inputs to the FormLayout
        form_layout.addRow('PSSH:', self.input1)
        form_layout.addRow('Licence URL:', self.input2)
        form_layout.addRow('Name:', self.input3)
        form_layout.addRow('Headers:', self.input4)
        form_layout.addRow('Proxy:', self.input5)
        form_layout.addRow('Build Info:', self.input6)

        # Add the FormLayout to the main layout
        layout.addLayout(form_layout)

        # Create a button layout
        buttons_layout = QHBoxLayout()

        # Create buttons and connect them to slots
        submit_button = QPushButton('Submit')
        buttons_layout.addWidget(submit_button)

        upload_cdm_button = QPushButton('Upload CDM')
        buttons_layout.addWidget(upload_cdm_button)

        # Add the buttons layout to the main layout
        layout.addLayout(buttons_layout)

        # Create a text browser to display the API response
        self.response_browser = QTextBrowser()

        # Add the text browser to the layout
        layout.addWidget(self.response_browser)

        # Set the layout for the main window
        self.setLayout(layout)