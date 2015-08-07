from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pyPdf
import support
import sys
import re
from collections import defaultdict

class pdfAnalysis(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        layout = QVBoxLayout()

        self.dir = QLineEdit()
        #self.label = QLabel()
        self.save_location = QLineEdit()
        self.progress = QProgressBar()
        execute = QPushButton("Execute")
        browse = QPushButton("Browse")

        self.dir.setPlaceholderText("Location of PDF's to parse!")
        #self.dir.setText("set for static directory")
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
        savefile = QFileDialog.getSaveFileName(self, caption="Save File As", directory=".", filter="All Files (*.*)")
        self.save_location.setText(QDir.toNativeSeparators(savefile))
           
    def search(self):
        mainDict = defaultdict(list)
        dir = self.dir.text()
        dirThere = support.dirExists(dir)
        count = 0
        if dirThere == False:
            QMessageBox.warning(self, "Whoa dog!", "The PDF input directory does not exist")
            return

        save_location = self.save_location.text()
        pdfList = support.readDir(str(dir))
        sizeoflist = len(pdfList)
        for pdf in pdfList:
            count+=1
            try:
                if sizeoflist > 0:
                    percent = count * 100 / sizeoflist
                    self.progress.setValue(int(percent))
                pageContent = support.getPDFContent(pdf).encode("ascii", "xmlcharrefreplace")
                md5s = re.findall('[a-fA-F0-9]{32}',pageContent)
                uniqueMd5s = set(md5s)
                mainDict[pdf] = uniqueMd5s
            except:
                pass

        support.writedata(mainDict, str(save_location))
        exit()
    
    def report(self, numsofar, listSize):
        if listSize > 0:
            percent = numsofar * 100 / listSize
            self.progress.setValue(int(percent))

app = QApplication(sys.argv)
p = pdfAnalysis()
p.show()
app.exec_()
