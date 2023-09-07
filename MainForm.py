import os
import subprocess
import sys
from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor, QLinearGradient, QPainter, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QGridLayout,
    QLabel,
    QWidget,
)


class GradientWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        gradient = QLinearGradient(self.rect().topLeft(), self.rect().bottomRight())
        gradient.setColorAt(0, QColor(49, 117, 185))  # Start color (blue)
        gradient.setColorAt(1, QColor(231, 62, 1))  # End color (red)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(gradient)
        painter.drawRect(self.rect())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and icon
        self.setWindowTitle("SecureCrypt")
        self.setWindowIcon(QIcon("icon.png"))

        # Create the main widget and the layout
        widget = GradientWidget()
        layout = QGridLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Add the header label
        header_label = QLabel("SecureCrypt")
        header_label.setAlignment(Qt.AlignCenter)
        header_font = QFont("Arial", 36, QFont.Bold)
        header_label.setFont(header_font)
        header_label.setStyleSheet("color: white;")

        # Add the header label to the layout
        layout.addWidget(header_label, 0, 0, 1, 2)

        # Add the buttons
        buttons_info = [
            ("Text Hasher", "HashForm.py"),
            ("File Hasher", "FileHasher.py"),
            ("File Lock", "FileLock.py"),
            ("File Encrypt", "FileEncrypt.py"),
            ("File Compress", "FileCompress.py"),
            ("File Shredder", "FileShredder.py"),

        ]

        for row, (btn_text, file_path) in enumerate(buttons_info):
            button = QPushButton(btn_text)
            button.setFont(QFont("Arial", 18, QFont.Bold))
            button.clicked.connect(partial(self.open_file, file_path))
            layout.addWidget(button, row + 1, 0, 1, 2)

        # Center the layout
        layout.setAlignment(Qt.AlignCenter)

        # Adjust the window size
        self.resize(600, 400)

        # Apply the gradient background to the main window
        self.apply_gradient_background()

    def apply_gradient_background(self):
        pal = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(49, 117, 185))  # Start color (blue)
        gradient.setColorAt(1, QColor(231, 62, 1))  # End color (red)
        pal.setBrush(QPalette.Window, gradient)
        self.setPalette(pal)

    @staticmethod
    def open_file(file_path):
        if os.path.exists(file_path):
            try:
                subprocess.Popen([sys.executable, file_path])
            except Exception as e:
                print(f"Error opening {file_path}: {e}")
        else:
            print(f"Error: {file_path} not found!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
