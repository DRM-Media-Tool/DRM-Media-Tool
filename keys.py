from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QGroupBox
)


class Keys(QWidget):
    def __init__(self, debug_logger, info_logger):
        super().__init__()
        self.debug_logger = debug_logger
        self.info_logger = info_logger
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # First Group Box
        group_box1 = QGroupBox("Keys")
        layout1 = QFormLayout()

        key_label1 = QLabel("Key 1:")
        key_input1 = QLineEdit()
        layout1.addRow(key_label1, key_input1)

        key_label2 = QLabel("Key 2:")
        key_input2 = QLineEdit()
        layout1.addRow(key_label2, key_input2)

        key_label3 = QLabel("Key 3:")
        key_input3 = QLineEdit()
        layout1.addRow(key_label3, key_input3)

        license_label = QLabel("License URL:")
        license_input = QLineEdit()
        layout1.addRow(license_label, license_input)
        submit_button = QPushButton('Submit')
        # submit_button.clicked.connect(self.handle_submit_click)
        layout1.addWidget(submit_button)
        group_box1.setLayout(layout1)

        # Second Group Box
        group_box2 = QGroupBox("Coming Soon")
        layout2 = QVBoxLayout()
        coming_soon_label = QLabel("This section is coming soon.")
        layout2.addWidget(coming_soon_label)
        group_box2.setLayout(layout2)

        # Add Group Boxes to main layout
        main_layout.addWidget(group_box1)
        main_layout.addWidget(group_box2)

        self.setLayout(main_layout)
