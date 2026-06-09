from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from extractor import MD5Extractor
import sys

class pdfAnalysis(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        layout = QVBoxLayout()

        self.dir = QLineEdit()
        self.save_location = QLineEdit()
        self.progress = QProgressBar()
        execute = QPushButton("Execute")
        browse = QPushButton("Browse")

        self.dir.setPlaceholderText("Location of PDF's to parse!")
        self.save_location.setPlaceholderText("File Save location")
        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.dir)
        layout.addWidget(self.save_location)
        layout.addWidget(browse)
        layout.addWidget(self.progress)
        layout.addWidget(execute)
        
        self.setLayout(layout)
        
        self.setGeometry(200,200,350,200)
        self.setWindowTitle("md5Extractor v0.1 by labgeek")
        self.setFocus()
        
        execute.clicked.connect(self.search)
        browse.clicked.connect(self.browse_file)
    
    def browse_file(self):
        savefile, _ = QFileDialog.getSaveFileName(self, caption="Save File As", directory=".", filter="All Files (*.*)")
        self.save_location.setText(QDir.toNativeSeparators(savefile))
           
    def search(self):
        dir = self.dir.text()
        save_location = self.save_location.text()
        extractor = MD5Extractor(dir, save_location)

        if extractor.dir_exists() == False:
            QMessageBox.warning(self, "Whoa dog!", "The PDF input directory does not exist")
            return

        extractor.extract(self.progress.setValue)
        exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p = pdfAnalysis()
    p.show()
    app.exec_()
