import os
import sys

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QFileDialog
from cryptography.fernet import Fernet


def generate_random_key():
    """Generates a random 32-byte key for encryption"""
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)
    return key


class FileEncrypt(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QUiLoader instance
        loader = QUiLoader()

        # Load the UI file
        ui_file = "FileEncrypt.ui"  # Replace with the path to your UI file
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        # Create a widget from the UI file
        self.ui = loader.load(ui_file)
        ui_file.close()

        # Button Events
        self.ui.BtnChooseFile.clicked.connect(self.choose_file)
        self.ui.BtnSaveFile.clicked.connect(self.choose_save_folder)
        self.ui.BtnEncrypt.clicked.connect(self.encrypt_file)
        self.ui.BtnDecrypt.clicked.connect(self.decrypt_file)
        self.ui.BtnClear.clicked.connect(self.clear_fields)
        self.ui.BtnMainMenu.clicked.connect(self.Close)

        # Set the window properties
        self.setWindowTitle("File Encryptor")
        self.setFixedSize(800, 600)

        # Apply custom styles
        self.apply_styles()

        # Show the widget
        self.ui.show()

        self.setWindowTitle("File Encryptor")

    # Rest of the code...
    def choose_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_paths, _ = file_dialog.getOpenFileNames(self, "Choose file(s)")

        if file_paths:
            # Update the QLineEdit with the selected file path
            self.ui.FileSelect.setText(file_paths[0])

    def choose_save_folder(self):
        save_folder = QFileDialog.getExistingDirectory(self, "Choose a folder to save the file")

        if save_folder:
            # Update the QLineEdit with the selected folder path
            self.ui.FileSave.setText(save_folder)

    def encrypt_file(self):
        file_path = self.ui.FileSelect.text()
        save_folder = self.ui.FileSave.text()

        if not file_path or not save_folder:
            QMessageBox.warning(self, "Encryption Error", "Please choose a file and a save folder.")
            return

        # Generate a random 32-byte key for encryption
        key = generate_random_key()
        self.ui.HashKey.setText(key.decode())
        fernet = Fernet(key)

        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()

            encrypted_data = fernet.encrypt(file_data)

            # Get the file name from the original file path
            file_name = os.path.basename(file_path)

            # Create the save file path using the selected folder and original file name
            save_path = os.path.join(save_folder, file_name + '.enc')

            with open(save_path, 'wb') as file:
                file.write(encrypted_data)

            QMessageBox.information(self, "Encryption Successful", "File encrypted and saved successfully.")
        except FileNotFoundError:
            QMessageBox.critical(self, "Encryption Error", "File not found.")
        except PermissionError:
            QMessageBox.critical(self, "Encryption Error", "Permission denied. Please check file access permissions.")
        except Exception as e:
            QMessageBox.critical(self, "Encryption Error", f"An error occurred while encrypting the file:\n{str(e)}")

    def decrypt_file(self):
        file_path = self.ui.FileSelect.text()
        save_folder = self.ui.FileSave.text()
        key = self.ui.HashKey.text().encode()

        if not file_path or not save_folder:
            QMessageBox.warning(self, "Decryption Error", "Please choose a file and a save folder.")
            return

        if not key:
            QMessageBox.warning(self, "Decryption Error", "Please enter a valid decryption key.")
            return

        try:
            fernet = Fernet(key)

            with open(file_path, 'rb') as file:
                file_data = file.read()

            decrypted_data = fernet.decrypt(file_data)

            # Get the original file name from the encrypted file path
            file_name = os.path.splitext(os.path.basename(file_path))[0]

            # Create the save file path using the selected folder and original file name
            save_path = os.path.join(save_folder, file_name)

            with open(save_path, 'wb') as file:
                file.write(decrypted_data)

            QMessageBox.information(self, "Decryption Successful", "File decrypted and saved successfully.")
        except FileNotFoundError:
            QMessageBox.critical(self, "Decryption Error", "File not found.")
        except PermissionError:
            QMessageBox.critical(self, "Decryption Error", "Permission denied. Please check file access permissions.")
        except Exception as e:
            QMessageBox.critical(self, "Decryption Error", f"An error occurred while decrypting the file:\n{str(e)}")

    def clear_fields(self):
        # Clear the file selection, save folder, and hash key fields
        self.ui.FileSelect.clear()
        self.ui.FileSave.clear()
        self.ui.HashKey.clear()

    def Close(self):
        self.ui.close()

    def apply_styles(self):
        # Set background color of the main widget
        self.ui.setStyleSheet(
            "QWidget { background-color: #f5f5f5; }"
        )

        # Set stylesheet for buttons
        button_style = (
            "QPushButton { background-color: #4CAF50; color: white;"
            " border: none; border-radius: 8px; padding: 10px 20px; font-size: 16px; }"
            "QPushButton:hover { background-color: #43ad13; }"
            "QPushButton:pressed { background-color: #43ad13; }"
        )
        self.ui.BtnChooseFile.setStyleSheet(button_style)
        self.ui.BtnSaveFile.setStyleSheet(button_style)
        self.ui.BtnEncrypt.setStyleSheet(button_style)
        self.ui.BtnDecrypt.setStyleSheet(button_style)
        self.ui.BtnClear.setStyleSheet(button_style)
        self.ui.BtnMainMenu.setStyleSheet(button_style)

        # Set stylesheet for text areas
        text_area_style = (
            "QPlainTextEdit { background-color: #f0f0f0; color: #333; border: 4px solid #ccc;"
            " border-radius: 15px; padding: 10px; font-size: 28px; }"
        )
        self.ui.FileSelect.setStyleSheet(text_area_style)
        self.ui.FileSave.setStyleSheet(text_area_style)
        self.ui.HashKey.setStyleSheet(text_area_style)

        # Set stylesheet for message boxes
        message_box_style = (
            "QMessageBox { background-color: #f5f5f5; color: #333; border: 1px solid #ccc; }"
            "QMessageBox QLabel { font-size: 18px; }"
            "QMessageBox QPushButton { background-color: #007BFF; color: white;"
            " border: none; border-radius: 8px; padding: 10px 20px; font-size: 16px; }"
            "QMessageBox QPushButton:hover { background-color: #0056b3; }"
            "QMessageBox QPushButton:pressed { background-color: #003d80; }"
        )
        self.ui.setStyleSheet(self.ui.styleSheet() + message_box_style)


if __name__ == "__main__":
    app = QApplication([])
    form = FileEncrypt()
    sys.exit(app.exec())
