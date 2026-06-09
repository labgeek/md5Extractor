README

Program name:  md5Extractor.py
Date:  2/27/2015
Support files: extractor.py
Author:  JD Durick <labgeek@gmail.com>
Description: Simple script to parse all PDF's within a specific directory and pull out all the MD5 values.  After extraction
it writes them all to a file of your choice.

Tested on the following platforms:
Ubuntu 12/13/14 however, should work on Windoze boxes.

Requirements:
1.  Python 3
2.  pip install -r requirements.txt   (installs pypdf and PyQt5)

Usage:
python md5Extractor.py

Tests:
pip install pytest
python -m pytest

TODO:
1.  Much needed error checking

I wrote it quick but it does work.
