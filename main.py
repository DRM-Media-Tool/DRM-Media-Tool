import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox, QAction, QMenu
from PyQt5.QtGui import QIcon
from key_getter import KeyGeter
from decrypter import Decrypter
from logger import setup_logging
import platform
import webbrowser
import os
from helper.download import download_and_extract_binary, binaries
from version import __version__, CHANNEL

info_logger, debug_logger = setup_logging()
current_dir = os.path.dirname(os.path.abspath(__file__))
icon = os.path.join(current_dir, 'assets', 'logo.ico')
git = os.path.join(current_dir, 'assets', 'github.png')
discord = os.path.join(current_dir, 'assets', 'discord.svg')
bug = os.path.join(current_dir, 'assets', 'bug.svg')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(icon))
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"DRM & Media Tool {__version__} ({CHANNEL})")
        self.setGeometry(100, 100, 750, 450)

        # Create the tab widget
        tab_widget = QTabWidget(self)

        # Create the menu bar
        menu_bar = self.menuBar()

        # Create the Help menu
        help_menu = menu_bar.addMenu('Help')

        # Create "Tools Used" action
        tools_used_action = QAction('Tools Used', self)
        tools_used_action.triggered.connect(self.show_tools_used)
        help_menu.addAction(tools_used_action)

        # Create "About" action
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        feature_bug_menu = QMenu('Feature/Bug', self)
        request_feature_bug_action = QAction(
            'Request a New Feature or Report Bug', self)
        request_feature_bug_action.triggered.connect(
            self.open_feature_bug_form)
        feature_bug_menu.addAction(request_feature_bug_action)
        menu_bar.addMenu(feature_bug_menu)

        help_menu = menu_bar.addMenu('Discord')
        open_discord_action = QAction('Open Discord', self)
        open_discord_action.triggered.connect(self.open_discord)
        help_menu.addAction(open_discord_action)

        # Create tabs
        hello_tab = KeyGeter(debug_logger, info_logger)
        file_lister_tab = Decrypter(debug_logger, info_logger)

        # Add tabs to the tab widget
        tab_widget.addTab(hello_tab, "Key Graber")
        tab_widget.addTab(file_lister_tab, "Decrypter & Merger")

        # Set the central widget to be the tab widget
        self.setCentralWidget(tab_widget)

    def show_tools_used(self):
        tools_used_dialog = QMessageBox()
        tools_used_dialog.setWindowTitle("Tools Needed")
        tools_used_dialog.setWindowIcon(self.windowIcon())
        tools_used_dialog.setText(
            "List of tools Needed:\n- Mp4decrypt\n- FFmpeg")
        info_logger.info("Show tools used menu")
        tools_used_dialog.exec_()

    def open_feature_bug_form(self):
        try:
            info_logger.info(
                "https://forms.gle/xtVPKLcAKNUwY2WD6: Link opened")
            url = "https://forms.gle/xtVPKLcAKNUwY2WD6"
            webbrowser.open(url)
        except Exception as e:
            debug_logger.debug(f"ERROR: {str(e)}")

    def open_discord(self):
        try:
            info_logger.info("https://discord.gg/QpEHdyst5b: Link opened")
            url = "https://discord.gg/QpEHdyst5b"
            webbrowser.open(url)
        except Exception as e:
            debug_logger.debug(f"ERROR: {str(e)}")

    def show_about(self):
        about_dialog = QMessageBox()
        about_dialog.setWindowTitle("About")
        about_dialog.setWindowIcon(self.windowIcon())
        about_dialog.setIcon(QMessageBox.Information)

        app_info = "<font size=6>DRM & Media Tool</font><br>"
        os_details = f"""
            <font size=4><b>Operating System: {platform.system()} {platform.release()}</b></font> <br>
            <font size=4><b>Developed By: Rajeshwaran</b></font> <br>
            <font size=4><b>Version: {__version__} ({CHANNEL})</b></font> <br>
            <br>
            <a href="https://github.com/Rajeshwaran2001" target="_blank"><img src="{git}" height=25 alt="GitHub"> </a> &nbsp; <a href="https://discord.gg/QpEHdyst5b" target="_blank"><img src="{discord}" height=25 alt="Discord"> </a> &nbsp; <a href="https://forms.gle/xtVPKLcAKNUwY2WD6" target="_blank"><img src="{bug}" height=25 alt="BUG"> </a> <br>
            """

        about_dialog.setText(app_info)
        about_dialog.setInformativeText(os_details)
        # check_for_update_button = about_dialog.addButton(
        #     "Check for Update", QMessageBox.AcceptRole)
        about_dialog.exec_()
        # if about_dialog.clickedButton() == check_for_update_button:
        #     # Add your code for checking for updates here
        #     print("Checking for updates...")


def main():
    # Check and download binaries
    for binary_info in binaries:
        download_and_extract_binary(binary_info)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
