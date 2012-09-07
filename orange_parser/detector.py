#! /usr/bin/env python
# coding: utf-8

class Detector:
    self.pageLayouts = []

    def __init__(self, pages):
        for page in pages:
            interpreter.process_page(page)
            pageLayout = device.get_result()

            self.pageLayouts.append(pageLayout)

    def detectBillings(self):
        '''
        1. Get all vertical lines
        2. For each vertical line check if any other lines lie in its [area]
            2a. If yes, discard these lines
            2b. If not, extract Chars from that [area] as billing information

        [area] - Height: length of the vertical line, width: whole page width
        '''
