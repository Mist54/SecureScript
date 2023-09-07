import hashlib
import sys

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox


class HashForm(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QUiLoader instance
        loader = QUiLoader()

        # Load the UI file
        ui_file = "HashForm.ui"  # Replace with the path to your UI file
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        # Create a widget from the UI file
        self.ui = loader.load(ui_file)
        ui_file.close()

        # Button Events
        self.ui.MD5_Encrypt.clicked.connect(self.encrypt_md5)
        self.ui.SHA_3.clicked.connect(self.sha3_encrypt)
        self.ui.Blake_2.clicked.connect(self.blake2_encrypt)
        self.ui.SHA_256.clicked.connect(self.sha256_encrypt)
        self.ui.Btn_Clear.clicked.connect(self.clear_text)
        self.ui.Btn_Close.clicked.connect(self.close)

        # Set the window properties
        self.setWindowTitle("Hash Form")
        self.setMinimumSize(800, 600)

        # Apply custom styles
        self.apply_styles()

        # Show the widget
        self.ui.show()

    # Rest of the code...

    def encrypt_md5(self):
        text = self.ui.Encrypt_Text.toPlainText()
        if not text:
            self.show_error_dialog("Please enter text to encrypt.")
            return
        hashed_text = hashlib.md5(text.encode()).hexdigest()
        self.ui.Hash_Text.setPlainText(hashed_text)

    def sha3_encrypt(self):
        text = self.ui.Encrypt_Text.toPlainText()
        if not text:
            self.show_error_dialog("Please enter text to encrypt.")
            return
        hash_value = hashlib.sha3_256(text.encode()).hexdigest()
        self.ui.Hash_Text.setPlainText(hash_value)

    def blake2_encrypt(self):
        text = self.ui.Encrypt_Text.toPlainText()
        if not text:
            self.show_error_dialog("Please enter text to encrypt.")
            return
        hash_value = hashlib.blake2s(text.encode()).hexdigest()
        self.ui.Hash_Text.setPlainText(hash_value)

    def sha256_encrypt(self):
        text = self.ui.Encrypt_Text.toPlainText()
        if not text:
            self.show_error_dialog("Please enter text to encrypt.")
            return
        hash_value = hashlib.sha256(text.encode()).hexdigest()
        self.ui.Hash_Text.setPlainText(hash_value)

    def clear_text(self):
        self.ui.Encrypt_Text.clear()
        self.ui.Hash_Text.clear()

    def close(self):
        self.ui.close()

    def show_error_dialog(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec()

    def apply_styles(self):
        # Set background color of the main widget
        self.ui.setStyleSheet(
            "QWidget { background-color: #f5f5f5; }"
        )

        # Set stylesheet for buttons
        button_style = (
            "QPushButton { background-color: #4CAF50; color: white;"
            " border: none; border-radius: 15px; padding: 10px 20px; font-size: 14px; }"
            "QPushButton:hover { background-color: #0056b3; }"
            "QPushButton:pressed { background-color: #43ad13; }"
        )
        self.ui.MD5_Encrypt.setStyleSheet(button_style)
        self.ui.SHA_3.setStyleSheet(button_style)
        self.ui.Blake_2.setStyleSheet(button_style)
        self.ui.SHA_256.setStyleSheet(button_style)
        self.ui.Btn_Clear.setStyleSheet(button_style)
        self.ui.Btn_Close.setStyleSheet(button_style)

        # Set stylesheet for text areas
        text_area_style = (
            "QPlainTextEdit { background-color: #f0f0f0; color: #333; border: 1px solid #ccc;"
            " border-radius: 10px; padding: 10px; font-size: 16px; }"
        )
        self.ui.Encrypt_Text.setStyleSheet(text_area_style)
        self.ui.Hash_Text.setStyleSheet(text_area_style)


if __name__ == "__main__":
    app = QApplication([])
    form = HashForm()
    sys.exit(app.exec())
