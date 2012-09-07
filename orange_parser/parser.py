#! /usr/bin/env python
# coding: utf-8

'''
Author: Radosław Szalski
'''

from __future__ import print_function
import sys
import re
from pprint import pprint

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTFigure, LTImage, LTTextBox, LTTextLine, LAParams, LTText, LTChar, LTLine, LTAnon
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfdevice import PDFDevice

def parsePDF(PDFPath):
    with open(PDFPath, 'rb') as pdfFile:
        parser = PDFParser(pdfFile)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize()

        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed

        rsrcmgr = PDFResourceManager()

        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        detector = Detector(doc.get_pages())



def printBilling(textLines):
    for line in textLines:
        if ':' in line:
            print(line)

def getChars(pageLayout):
    '''
    Chars include actual characters as well as LTAnon objects (spaces, non-printable).
    '''
    for layoutObject in pageLayout._objs:
        if isinstance(layoutObject, LTText):
            for textLine in layoutObject._objs:
                for char in textLine._objs:
                    if isinstance (char, LTChar) or isinstance(char, LTAnon):
                        yield char

if __name__ == '__main__':
    try:
        parsePDF(sys.argv[1])
    except Exception as ex:
        print(ex);
