import pyPdf
import csv
import os
import re
import sys
import time
import datetime
import fnmatch
from optparse import OptionParser
import dircache

def getPDFContent(path):
    '''
    Gets the content of the entire PDF file
    '''
    content = ""
    pdf = pyPdf.PdfFileReader(file(path, "rb"))
    for i in range(0, pdf.getNumPages()):
        content += pdf.getPage(i).extractText() + "\n"
    return content


def mkdir(dir):
    '''
    Function not used but would create directory if needed
    '''
    currentdir = os.getcwd()
    finaldir = currentdir + "\\" + dir
    if not os.path.exists(finaldir):
        dirRes = os.makedirs(finaldir)
        return finaldir
    else:
        return finaldir

def readPDF(dir):
    '''
    Not used but would return a list of files within a directory containing only .pdfs
    '''
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '.pdf'):
            print(file)
            
def dirExists(dir):
    '''
    Function to test whether or not the directory exists
    '''
    if os.path.isdir(dir):
        return True
    return False
    
def readDir(dir):
    '''
    Reads the directory looking for only PDF files
    '''
    pattern = '*.pdf'
    dirlist =[]
    for root, dirs, files in os.walk(dir):
        for filename in fnmatch.filter(files, pattern):
            print filename
            dirlist.append(os.path.join(root, filename))
    return dirlist
    
def writedata(pdfDict, filepath):
    '''
    Accepts a dict and writes the output to 
    a file you choose
    '''
    outputfile = open(filepath, mode='ab')
    writer = csv.writer(outputfile, lineterminator='\n')
    header = ['Absolute_Path', 'MD5_Hash_Values']
    writer.writerow(header)
    
    '''
    Loops through dict
    '''
    for pdf in pdfDict:
        for md5 in pdfDict[pdf]:
            #print "%s == %s" % (pdf,md5)
            writer.writerow([pdf, md5])
        