from PyQt5.QtWidgets import QMessageBox


def show_error_message(parent, message):
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Critical)
    error_box.setWindowTitle("Error")
    error_box.setText(message)
    error_box.setWindowIcon(parent.windowIcon())
    error_box.exec_()


def show_success_message(parent, message):
    success_box = QMessageBox()
    success_box.setIcon(QMessageBox.Information)
    success_box.setWindowTitle("Success")
    success_box.setText(message)
    success_box.setWindowIcon(parent.windowIcon())
    success_box.exec_()
