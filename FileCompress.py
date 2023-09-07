import bz2
import os
import shutil
import sys
import tarfile
import zipfile

import py7zr
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMessageBox,
    QFileDialog,
)


class FileCompress(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QUiLoader instance
        loader = QUiLoader()

        # Load the UI file
        ui_file = "FileCompress.ui"  # Replace with the path to your UI file
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        # Create a widget from the UI file
        self.ui = loader.load(ui_file)
        ui_file.close()

        # Button and events
        self.ui.BtnFileChoose.clicked.connect(self.choose_file)
        self.ui.BtnCompress.clicked.connect(self.compress_folder)
        self.ui.BtnDecompress.clicked.connect(self.decompress_folder)
        self.ui.ChooseFile.textChanged.connect(self.validate_path_input)
        self.ui.ChooseFile.textChanged.connect(self.update_button_states)
        self.ui.BtnMainMenu.clicked.connect(self.close)

        # Set the window properties
        self.setWindowTitle("File Compressor")
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 800)

        # Apply custom styles
        self.apply_styles()

        # Show the widget
        self.ui.show()

    def choose_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Choose File")
        self.ui.ChooseFile.setText(file_path)

    def compress_folder(self):
        folder_path = self.ui.ChooseFile.text()
        if not folder_path:
            self.show_error_dialog("Please choose a folder.")
            return

        compression_type = self.get_selected_compression_type()
        if not compression_type:
            self.show_error_dialog("Please select a compression type.")
            return

        try:
            output_file = f"{folder_path}.{compression_type}"
            if compression_type == "zip":
                self.compress_zip(folder_path, output_file)
            elif compression_type == "tar":
                self.compress_tar(folder_path, output_file)
            elif compression_type == "7z":
                self.compress_7z(folder_path, output_file)
            elif compression_type == "bz2":
                self.compress_bz2(folder_path, output_file)

            self.show_info_dialog("Compression successful.")
        except Exception as e:
            self.show_error_dialog(f"Compression error: {str(e)}")

    def decompress_folder(self):
        file_path = self.ui.ChooseFile.text()
        if not file_path:
            self.show_error_dialog("Please choose a file or folder.")
            return

        compression_type = self.get_selected_compression_type()
        if not compression_type:
            self.show_error_dialog("Please select a compression type.")
            return

        try:
            if os.path.isfile(file_path):
                self.decompress_file(file_path, compression_type)
            elif os.path.isdir(file_path):
                if compression_type == "zip":
                    self.decompress_zip(file_path)
                elif compression_type == "tar":
                    self.decompress_tar(file_path)
                elif compression_type == "7z":
                    self.decompress_7z(file_path)
                elif compression_type == "bz2":
                    self.decompress_bz2(file_path)

            self.show_info_dialog("Decompression successful.")
        except Exception as e:
            self.show_error_dialog(f"Decompression error: {str(e)}")

    def compress_zip(self, folder_path, output_file):
        with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, relative_path)

    def decompress_zip(self, zip_file):
        output_dir = os.path.dirname(zip_file)
        with zipfile.ZipFile(zip_file, "r") as zipf:
            zipf.extractall(output_dir)

    def compress_tar(self, folder_path, output_file):
        with tarfile.open(output_file, "w") as tar:
            tar.add(folder_path, arcname=os.path.basename(folder_path))

    def decompress_tar(self, tar_file):
        output_dir = os.path.dirname(tar_file)
        with tarfile.open(tar_file, "r") as tar:
            tar.extractall(output_dir)

    def compress_7z(self, folder_path, output_file):
        with py7zr.SevenZipFile(output_file, "w") as archive:
            archive.writeall(folder_path, os.path.basename(folder_path))

    def decompress_7z(self, archive_file):
        output_dir = os.path.dirname(archive_file)
        with py7zr.SevenZipFile(archive_file, "r") as archive:
            archive.extractall(output_dir)

    def compress_bz2(self, file_path, output_file):
        with open(file_path, "rb") as input_file, bz2.open(output_file, "wb") as bz2_file:
            shutil.copyfileobj(input_file, bz2_file)

    def decompress_bz2(self, file_path):
        output_dir = os.path.dirname(file_path)
        output_file = os.path.splitext(file_path)[0]
        with bz2.open(file_path, "rb") as bz2_file, open(output_file, "wb") as output_file:
            shutil.copyfileobj(bz2_file, output_file)

    def decompress_file(self, file_path, compression_type):
        if compression_type == "zip":
            self.decompress_zip(file_path)
        elif compression_type == "tar":
            self.decompress_tar(file_path)
        elif compression_type == "7z":
            self.decompress_7z(file_path)
        elif compression_type == "bz2":
            self.decompress_bz2(file_path)

    def get_selected_compression_type(self):
        if self.ui.RdZip.isChecked():
            return "zip"
        elif self.ui.RdRAR.isChecked():
            return "tar"
        elif self.ui.Rd7z.isChecked():
            return "7z"
        elif self.ui.RdBzip.isChecked():
            return "bz2"
        else:
            return ""

    def show_error_dialog(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec()

    def validate_path_input(self, text):
        if not os.path.exists(text):
            self.ui.ChooseFile.setStyleSheet(
                "QLineEdit { background-color: #f0f0f0; color: red; border: 1px solid #ccc; padding: 10px; }"
            )
        else:
            self.ui.ChooseFile.setStyleSheet(
                "QLineEdit { background-color: #f0f0f0; color: #333; border: 1px solid #ccc; padding: 10px; }"
            )
            self.enable_buttons()

    def update_button_states(self, text):
        if not os.path.exists(text):
            self.disable_buttons()

    def disable_buttons(self):
        self.ui.BtnCompress.setEnabled(False)
        self.ui.BtnDecompress.setEnabled(False)

    def enable_buttons(self):
        self.ui.BtnCompress.setEnabled(True)
        self.ui.BtnDecompress.setEnabled(True)

    def close(self):
        self.ui.close()

    def show_info_dialog(self, message):
        info_dialog = QMessageBox(self)
        info_dialog.setIcon(QMessageBox.Information)
        info_dialog.setWindowTitle("Info")
        info_dialog.setText(message)
        info_dialog.setStandardButtons(QMessageBox.Ok)
        info_dialog.exec()

    def apply_styles(self):
        # Set background color of the main widget
        self.ui.setStyleSheet(
            "QWidget { background-color: #f5f5f5; }"
        )

        # Set stylesheet for buttons
        buttons = [self.ui.BtnFileChoose, self.ui.BtnCompress, self.ui.BtnDecompress, self.ui.BtnMainMenu]
        for button in buttons:
            button.setStyleSheet(
                "QPushButton { background-color: #4CAF50; color: white; border: 1px solid #61afef; border-radius: 5px; padding: 10px; }"
                "QPushButton:hover { background-color: #2faf31; }"
            )

        # Set stylesheet for radio buttons
        radio_buttons = [self.ui.RdZip, self.ui.RdRAR, self.ui.Rd7z, self.ui.RdBzip]
        for radio_button in radio_buttons:
            radio_button.setStyleSheet(
                "QRadioButton { color: black; font-size: 16px; }"
                "QRadioButton::indicator { width: 16px; height: 16px; }"
                "QRadioButton::indicator:checked { border: 2px solid #6ee04e; background-color: #6ee04e; }"
                "QRadioButton::indicator:unchecked { border: 2px solid #6ee04e; background-color: white; }"
            )

        # Set stylesheet for line edit
        self.ui.ChooseFile.setStyleSheet(
            "QLineEdit { background-color: #f0f0f0; color: #333; border: 1px solid #ccc; padding: 10px; }"
        )

        # Set stylesheet for information and warning dialogs
        self.setStyleSheet(
            "QMessageBox { background-color: #f5f5f5; color: #333; }"
            "QMessageBox QPushButton { background-color: #61afef; color: white; }"
        )


if __name__ == "__main__":
    app = QApplication([])
    form = FileCompress()
    sys.exit(app.exec())
