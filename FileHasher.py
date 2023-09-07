import hashlib
import sys
import zlib

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QFileDialog


class FileHasher(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QUiLoader instance
        loader = QUiLoader()

        # Load the UI file
        ui_file = "FileHasher.ui"  # Replace with the path to your UI file
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        # Create a widget from the UI file
        self.ui = loader.load(ui_file)
        ui_file.close()

        # Button Events
        self.ui.BtnFile.clicked.connect(self.choose_file)
        self.ui.BtSubmit.clicked.connect(self.calculate_hashes)
        self.ui.BtnClear.clicked.connect(self.Clear_Text)
        self.ui.BtnClose.clicked.connect(self.Close)

        # Show the widget
        self.ui.show()

        # Rest of code

        # Add style sheet to the widget
        style_sheet = """
            /* Add your custom styles here */
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #357934;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """
        self.ui.setStyleSheet(style_sheet)

        # Set window title
        self.setWindowTitle("File Hasher")

        # choosing file 1from GUI

    def choose_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Choose File")
        self.ui.File_Path.setText(file_path)

    def calculate_hashes(self):
        file_path = self.ui.File_Path.text()
        if not file_path:
            self.show_error_dialog("Please choose a file.")
            return

        try:
            with open(file_path, "rb") as file:
                data = file.read()
            # Different hash for calculation
            md5_hash = hashlib.md5(data).hexdigest()
            sha256_hash = hashlib.sha256(data).hexdigest()
            blake2_hash = hashlib.blake2b(data).hexdigest()
            sha3_hash = hashlib.sha3_256(data).hexdigest()
            sha512_hash = hashlib.sha512(data).hexdigest()
            sha1_hash = hashlib.sha1(data).hexdigest()
            crc32_checksum = zlib.crc32(data)  # Calculate CRC32 checksum using z lib Library 
            crc32_hash = f"{crc32_checksum & 0xffffffff:08x}"  # Convert checksum to hexadecimal CRC32 hash

            self.ui.lineEdit_3.setText(md5_hash)
            self.ui.lineEdit_4.setText(sha256_hash)
            self.ui.lineEdit_5.setText(blake2_hash)
            self.ui.lineEdit_6.setText(sha3_hash)
            self.ui.lineEdit.setText(sha512_hash)
            self.ui.lineEdit_2.setText(crc32_hash)
            self.ui.lineEdit_7.setText(sha1_hash)
        except IOError:
            self.show_error_dialog("Error reading the file.")

    def show_error_dialog(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec()

    def Clear_Text(self):
        self.ui.File_Path.clear()
        self.ui.lineEdit.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_7.clear()

    def Close(self):
        self.ui.close()


if __name__ == "__main__":
    app = QApplication([])
    form = FileHasher()
    sys.exit(app.exec())
