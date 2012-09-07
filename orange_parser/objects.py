#! /usr/bin/env python
# coding: utf-8

'''
Classes representing distinct sections/objects on an Orange invoice.

Author: Radosław Szalski
'''

class Call:
    def __init__(self, callLine):
        '''
        A call line represents a single logged call
        listed on the invoice.

        Example:
            16:02 sieć PTC 999999999 0029 0,11 0,14 0,00

        '''
        splitLine = callLine.split()
        self.hour = splitLine[0]
        self.total = splitLine[-1]
        self.gross = splitLine[-2]
        self.netto = splitLine[-3]
        self.length = splitLine[-4]
        self.number = splitLine[-5]
        self.operator = ''

        # Remaining data (in between hour and number) denotes the Cell Operator
        for entry in splitLine:
            if 0 < splitLine.index(entry) < len(splitLine) - 5:
                self.operator += entry

class Billing:
    def __init__(self, pageLayout):
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

    def spreadLines(self, textLines):
        '''
        '''
        dataList = []

        for index, line in enumerate(textLines):
            if ':' in line:
                call = Call(line)
                dataList.append(call)

        return dataList

