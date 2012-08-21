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

        for pageNumber, page in enumerate(doc.get_pages(), start=1):
            interpreter.process_page(page)
            pageLayout = device.get_result()

            if pageNumber == 6:
                content = parseBilling(pageLayout)
                printBilling(content)


def printBilling(textLines):
    for line in textLines:
        if ':' in line:
            print(line)

def parseBilling(pageLayout):
    from collections import defaultdict

    columns = {}
    columns['left'] = defaultdict(lambda: {})
    columns['right'] = defaultdict(lambda: {})
    finalLines = []

    lastUsedX, lastUsedY = 0, 0
    lastUsedSide = ''

    dividerCoordinate = 310.393

    for char in getChars(pageLayout):
        if hasattr(char, 'bbox'):
            (x, y, x1, y1) = char.bbox

            # Rounding up to avoid quirks like chars misaligned by one thousandth of a pt
            y = int(y)
            y1 = int(y1)

            text = char.get_text()

            # Small font, used for seconds, is 5 pts in height
            # We want it to go on the same line as minutes (7 pt)
            if y1 - y == 5:
                y = y - 2

            if x < dividerCoordinate:
                columns['left'][y][x] = text
                lastUsedSide = 'left'
            else:
                columns['right'][y][x] = text
                lastUsedSide = 'right'

            lastUsedY = y
            lastUsedX = x
        else:
            print('X: %f, Y: %f' % (lastUsedX, lastUsedY))
            if char.get_text() == '\n':
                columns[lastUsedSide][lastUsedY][lastUsedX + 0.000001] = ' '
            else:
                columns[lastUsedSide][lastUsedY][lastUsedX + 0.000001] = text

    for column in columns:
        for lineNumber in sorted(columns[column].keys(), reverse=True):
            line = ''

            for charPos in sorted(columns[column][lineNumber].keys()):
                char = columns[column][lineNumber][charPos]
                line += char

            finalLines.append(line)

    return finalLines

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
