
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Telemetry-Test | Test Platform")
        self.setMinimumSize(900, 600)

        # Main application container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Application title
        title = QLabel("Telemetry Test Platform")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        # Initial device status
        status = QLabel("Device Status: DISCONNECTED")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status.setStyleSheet("font-size: 18px;")

        layout.addWidget(title)
        layout.addWidget(status)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
