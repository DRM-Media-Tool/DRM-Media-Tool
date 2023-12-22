from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QFileDialog


class UploadCDMDialog(QDialog):
    def __init__(self, debug_logger, info_logger):
        super().__init__()

        self.debug_logger = debug_logger
        self.info_logger = info_logger

        self.setWindowTitle('Upload Your CDM')
        self.setGeometry(100, 100, 400, 200)

        main_layout = QVBoxLayout()

        api_layout = QHBoxLayout()
        api_label = QLabel('Select API:')
        self.api_dropdown = QComboBox()
        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_dropdown)

        device_id_layout = QHBoxLayout()
        device_id_label = QLabel('Device ID:')
        self.device_id_edit = QLineEdit()
        device_id_upload_button = QPushButton('Upload File')
        device_id_upload_button.clicked.connect(self.upload_device_id_file)
        device_id_layout.addWidget(device_id_label)
        device_id_layout.addWidget(device_id_upload_button)

        private_key_layout = QHBoxLayout()
        private_key_label = QLabel('Private Key:')
        self.private_key_edit = QLineEdit()
        private_key_upload_button = QPushButton('Upload File')
        private_key_upload_button.clicked.connect(self.upload_private_key_file)
        private_key_layout.addWidget(private_key_label)
        private_key_layout.addWidget(private_key_upload_button)

        submit_layout = QHBoxLayout()
        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.handle_submit_click)
        submit_layout.addWidget(submit_button)

        main_layout.addLayout(api_layout)
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
        print('Submit Clicked')
