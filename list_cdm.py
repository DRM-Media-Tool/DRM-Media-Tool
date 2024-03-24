from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHeaderView,
    QMessageBox
)
from helper.message import show_confirmation_message
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
delete = os.path.join(current_dir, 'assets', 'delete.svg')


class Cdm(QWidget):
    def __init__(self, debug_logger, info_logger):
        super().__init__()
        self.debug_logger = debug_logger
        self.info_logger = info_logger
        self.init_ui()

    def init_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Device Info", "Delete"])

        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def clear_table(self):
        self.table.clearContents()
        self.table.setRowCount(0)

    def populate_table_from_database(self):
        self.clear_table()
        connection = sqlite3.connect('db.db')
        cursor = connection.cursor()

        cursor.execute("SELECT id, device_info FROM cdm")
        rows = cursor.fetchall()

        for row_data in rows:
            id, device_info = row_data
            self.add_row(str(id), device_info, id)

        connection.close()

    def add_row(self, id, device_info, action_id):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        id_item = QTableWidgetItem(id)
        id_item.setTextAlignment(Qt.AlignCenter)
        id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
        device_info_item = QTableWidgetItem(device_info)
        device_info_item.setTextAlignment(Qt.AlignCenter)
        device_info_item.setFlags(device_info_item.flags()
                                  & ~Qt.ItemIsEditable)
        action_button = QPushButton()
        action_button.setIcon(QIcon(delete))
        action_button.setToolTip("Delete")
        action_button.setObjectName(str(action_id))
        action_button.clicked.connect(self.delete_row)

        self.table.setItem(row_position, 0, id_item)
        self.table.setItem(row_position, 1, device_info_item)
        self.table.setCellWidget(row_position, 2, action_button)

    def showEvent(self, event):
        self.populate_table_from_database()

    def delete_row(self):
        button = self.sender()
        if button:
            title = 'Delete Confirmation'
            message = "Are you sure you want to delete this CDM?"
            reply = show_confirmation_message(self, title, message)
            if reply == QMessageBox.Yes:
                index = self.table.indexAt(button.pos())
                if index.isValid():
                    # Get the row of the button
                    row = index.row()

                    # get id to delete
                    id_to_delete = button.objectName()

                    connection = sqlite3.connect('db.db')
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM cdm WHERE id=?",
                                   (id_to_delete,))
                    connection.commit()
                    connection.close()

                    # Update the table
                    self.table.removeRow(row)
                    message = f"CDM {id_to_delete} Deleted"
                    self.info_logger.info(message)
            else:
                id_to_delete = button.objectName()
                message = f"CDM {id_to_delete} Not Deleted"
                self.info_logger.info(message)
                # self.debug_logger.debug(error_message)
