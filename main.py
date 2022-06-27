import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Glass'
        self.left = 600
        self.top = 200
        self.width = 320
        self.height = 240
        self.text_path = None
        self.text_data = None
        self.bookmark = 0
        self.page_length = 250
        self.frameless = True
        self.label = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.openFileNameDialog()
        self.initCustomLabel()
        self.show()

    def initCustomLabel(self):
        self.label = CustomLabel(f"▇{self.text_data[self.bookmark:self.bookmark + self.page_length]}", self)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.text_path = fileName
            with open(fileName, 'rb') as f:
                self.text_data = f.read().decode()

    def resizeEvent(self, e):
        self.page_length = min(int(e.size().width() * e.size().height() / (640 * 480) * 1000), 1000)
        print(self.page_length)

    def closeEvent(self, e):
        sys.exit()


class CustomLabel(QLabel):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignTop)
        self.setTextFormat(Qt.RichText)
        self.setFont(QFont("Times", 10))
        self.setStyleSheet("color:white")

    def wheelEvent(self, e):
        if e.angleDelta().y() > 0:
            self.parent().bookmark = 0 if self.parent().bookmark - self.parent().page_length < 0 else self.parent().bookmark - self.parent().page_length
            text = self.parent().text_data[self.parent().bookmark:self.parent().bookmark + self.parent().page_length]
            self.setText(f"▇{text.strip()}")
            self.adjustSize()
        elif e.angleDelta().y() < 0:
            self.parent().bookmark = self.parent().bookmark + self.parent().page_length
            text = self.parent().text_data[self.parent().bookmark:self.parent().bookmark + self.parent().page_length]
            self.setText(f"▇{text.strip()}")
            self.adjustSize()

    def mouseMoveEvent(self, e):
        if e.y() < self.parent().height * 0.2 and e.x() > self.parent().width * 0.5 and self.parent().frameless:
            self.parent().frameless = False
            self.parent().setWindowFlags(Qt.Widget)
            self.parent().show()
        elif e.y() > self.parent().height * 0.5 and not self.parent().frameless:
            self.parent().frameless = True
            self.parent().setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
            self.parent().show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
