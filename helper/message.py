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


def show_confirmation_message(parent, title, message):
    confirmation_box = QMessageBox()
    confirmation_box.setIcon(QMessageBox.Question)
    confirmation_box.setWindowTitle(title)
    confirmation_box.setText(message)
    confirmation_box.setWindowIcon(parent.windowIcon())
    confirmation_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    confirmation_box.setDefaultButton(QMessageBox.No)
    return confirmation_box.exec_()
