import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from PyQt5.QtCore import Qt

class FilePickerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 400, 60)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText('Drag and drop a file here or click to open a file picker.')

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        files = e.mimeData().urls()
        file_path = files[0].toLocalFile()
        self.display_file(file_path)

    def mousePressEvent(self, e):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*);;Text Files (*.txt)', options=options)
        if file_path:
            self.display_file(file_path)

    def display_file(self, file_path):
        self.label.setText('Selected File: ' + file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FilePickerApp()
    window.setGeometry(100, 100, 420, 100)
    window.setWindowTitle('File Picker and Dropper')
    window.show()
    sys.exit(app.exec_())
