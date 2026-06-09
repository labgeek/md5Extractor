from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from extractor import MD5Extractor
import os
import sys

class pdfAnalysis(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        layout = QVBoxLayout()
        pdf_layout = QHBoxLayout()
        save_layout = QHBoxLayout()

        self.dir = QLineEdit()
        self.save_location = QLineEdit()
        self.progress = QProgressBar()
        execute = QPushButton("Execute")
        browse_pdf = QPushButton("Browse PDFs")
        browse_save = QPushButton("Output Folder")

        self.dir.setPlaceholderText("Location of PDF's to parse!")
        self.save_location.setPlaceholderText("Output directory for md5Output.txt")
        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignCenter)

        pdf_layout.addWidget(self.dir)
        pdf_layout.addWidget(browse_pdf)
        save_layout.addWidget(self.save_location)
        save_layout.addWidget(browse_save)

        layout.addLayout(pdf_layout)
        layout.addLayout(save_layout)
        layout.addWidget(self.progress)
        layout.addWidget(execute)
        
        self.setLayout(layout)
        
        self.setGeometry(200, 200, 650, 220)
        self.setWindowTitle("md5Extractor v0.1 by labgeek")
        self.setFocus()
        
        execute.clicked.connect(self.search)
        browse_pdf.clicked.connect(self.browse_pdf_directory)
        browse_save.clicked.connect(self.browse_file)

    def browse_pdf_directory(self):
        directory = QFileDialog.getExistingDirectory(self, caption="Select PDF Directory", directory=".")
        if directory:
            self.dir.setText(QDir.toNativeSeparators(directory))
    
    def browse_file(self):
        directory = QFileDialog.getExistingDirectory(self, caption="Select Output Directory", directory=".")
        if directory:
            self.save_location.setText(QDir.toNativeSeparators(directory))
           
    def search(self):
        dir = self.dir.text()
        output_directory = self.save_location.text()
        save_location = os.path.join(output_directory, "md5Output.txt")
        extractor = MD5Extractor(dir, save_location)

        if extractor.dir_exists() == False:
            QMessageBox.warning(self, "Whoa dog!", "The PDF input directory does not exist")
            return

        try:
            os.makedirs(output_directory, exist_ok=True)
        except OSError as error:
            QMessageBox.warning(self, "Whoa dog!", "The output directory could not be created: %s" % error)
            return

        extractor.extract(self.progress.setValue)
        exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p = pdfAnalysis()
    p.show()
    app.exec_()
