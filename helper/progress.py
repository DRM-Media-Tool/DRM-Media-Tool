from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QLabel


class DownloadProgressDialog(QDialog):
    def __init__(self, binary_name):
        super().__init__()
        self.setWindowTitle("Downloading Missing Binaries")
        self.resize(300, 70)
        self.layout = QVBoxLayout()
        self.progress_label = QLabel(f"Downloading {binary_name}")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_label)
        self.layout.addWidget(self.progress_bar)
        self.setLayout(self.layout)

    def set_progress(self, percent):
        self.progress_bar.setValue(percent)
