# coding=utf-8
import win32com.client
import os
class easy_excel:
    def __init__(self, filename=None):
        self.xlApp = win32com.client.Dispatch('Excel.Application')
        if filename:
            self.filename = filename
            self.xlBook = self.xlApp.Workbooks.Open(self.filename)
        else:
            self.xlBook = self.xlApp.Workbooks.Add()
            self.filename = ''

    def getCell(self, sheet, row, col):
        sht = self.xlBook.Worksheets(1)
        return sht.Cells(row, col).Value

    def close(self):
        self.xlBook.Close(SaveChanges=0)
        self.xlApp.Quit()
