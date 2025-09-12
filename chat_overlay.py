from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QGuiApplication
import sys


class ChatOverlay(QWidget):
    """Floating chat overlay widget."""

    message_sent = Signal(str)

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool | Qt.FramelessWindowHint)
        self.setFixedSize(380, 550)
        self._build_ui()
        self._position_bottom_right()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        self.chatHistory = QTextEdit(objectName="chatHistory")
        self.chatHistory.setReadOnly(True)
        layout.addWidget(self.chatHistory)

        input_layout = QHBoxLayout()
        self.inputBox = QLineEdit(objectName="inputBox")
        input_layout.addWidget(self.inputBox)

        send_btn = QPushButton("Send")
        input_layout.addWidget(send_btn)

        layout.addLayout(input_layout)

        send_btn.clicked.connect(self._handle_send)
        self.inputBox.returnPressed.connect(self._handle_send)

    def _handle_send(self):
        text = self.inputBox.text().strip()
        if text:
            self.message_sent.emit(text)
            self.inputBox.clear()

    def _position_bottom_right(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        x = screen.x() + screen.width() - self.width()
        y = screen.y() + screen.height() - self.height()
        self.move(x, y)

    def append_message(self, role: str, text: str) -> None:
        prefix = "User:" if role.lower() == "user" else "AI:"
        self.chatHistory.append(f"{prefix} {text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = ChatOverlay()
    overlay.message_sent.connect(lambda msg: overlay.append_message("User", msg))
    overlay.append_message("AI", "Type a message and press Send")
    overlay.show()

    # Quit after a short delay when run headless
    QTimer.singleShot(1000, app.quit)
    sys.exit(app.exec())
