import csv
import xlrd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os


class DataHandler:

    @staticmethod
    def GetCsvData(filename):
        rows = []
        data = open(filename, "r")
        reader = csv.reader(data)
        next(reader)
        for row in reader:
            rows.append(row)
        return rows

    @staticmethod
    def GetExcelData(filename, sheetname):
        wb = xlrd.open_workbook(filename)
        sheet = wb.sheet_by_name(sheetname)
        rows = []
        for row in range(1, sheet.nrows):
            rows.append(sheet.row_values(row))
        return rows

    @staticmethod
    def GetGoogleData(projectname, sheetname):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join('config',
                                                                              'My-Automation-Project-ae9d0149564d.json'),
                                                                 scope)
        client = gspread.authorize(creds)

        sheet = client.open(projectname).worksheet(sheetname)
        return sheet.get_all_values()[1:]
