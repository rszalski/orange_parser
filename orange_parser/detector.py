#! /usr/bin/env python
# coding: utf-8

'''
Author: Radosław Szalski
'''

from pdfminer.layout import LTLine, LTChar, LTTextBoxHorizontal

class Detector:
    def __init__(self, pages):
        self.pageLayouts = pages

        self.detectBillings()

    def detectBillings(self):
        '''
        0. For each page, 
        1. Get all vertical lines,
        2. For each vertical line check if any other lines lie in its [area],
            2a. If yes, discard these lines,
            2b. If not, extract Chars from that [area] as billing information.

        [area] - has height equal to length of the vertical line, and width of the whole page.

        TODO weird results on page 3 of Account Billing.
        '''
        billingLines = {}

        for pageNumber, pageLayout in enumerate(self.pageLayouts, start=1):
            billingLines[pageNumber] = set()

            lines = self.getLinesOnPage(pageLayout)
            verticalLines = {line for line in lines if self.isVertical(line)}
            isAloneInArea = True

            for verticalLine in verticalLines:
                for otherLine in lines:
                    if self.lineAreaContainsOtherLine(verticalLine, otherLine):
                        isAloneInArea = False
                        break

                if isAloneInArea:
                    billingLines[pageNumber].add(verticalLine)

        for page in billingLines:
            for line in billingLines[page]:
                print('[Page %d] We have a billing area.' % page)
                print(line)

    def lineAreaContainsOtherLine(self, line, otherLine):
        '''
        Since line area has a widht of a whole page, we only need to check y coordinates.
        '''
        if line == otherLine:
            return False

        (_, y1, _, y2) = line.bbox
        (_, other_y1, _, other_y2) = otherLine.bbox

        return y1 <= other_y1 <= y2 or y1 <= other_y2 <= y2

    def isVertical(self, line):
        (x1, _, x2, _) = line.bbox

        return x1 == x2

    def getLinesOnPage(self, pageLayout):
        lines = set()

        for obj in pageLayout._objs:
            if isinstance(obj, LTLine):
                lines.add(obj)

        self.lines = lines

        return lines
