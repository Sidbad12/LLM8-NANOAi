
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Medical AI Test")
        self.setGeometry(100, 100, 600, 400)

        # Add a simple label
        self.label = QLabel("Medical AI Assistant Running!", self)
        self.label.move(180, 180)
        self.label.resize(250, 30)

        # Add a test button
        self.button = QPushButton("Click Me", self)
        self.button.move(250, 220)
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        self.label.setText("Button Clicked! ✅")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())
