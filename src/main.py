#! /usr/bin/env python
# coding: utf-8

'''
Author: Radosław Szalski
'''

import sys

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTFigure, LTImage, LTTextBox, LTTextLine, LAParams
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

        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()

            for lt_obj in layout._objs:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    print(lt_obj.get_text())

if __name__ == '__main__':
    try:
        parsePDF(sys.argv[1])
    except Exception as ex:
        print(ex);
