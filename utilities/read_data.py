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
        dict_keys = next(reader)
        for row in reader:
            dict_info = {}
            for i in range(len(row)):
                dict_info[dict_keys[i]] = row[i]
            rows.append(dict_info)
        return rows

    @staticmethod
    def GetExcelData(filename, sheetname):
        wb = xlrd.open_workbook(filename)
        sheet = wb.sheet_by_name(sheetname)
        rows = []
        dict_keys = sheet.row_values(0)
        for row in range(1, sheet.nrows):
            dict_info = {}
            for i in range(len(dict_keys)):
                dict_info[dict_keys[i]] = sheet.row_values(row)[i]
            rows.append(dict_info)
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

        rows = []
        dict_keys = sheet.get_all_values()[0]
        values = sheet.get_all_values()[1:]

        for v in values:
            dict_values = {}
            for i in range(len(dict_keys)):
                dict_values[dict_keys[i]] = v[i]
            rows.append(dict_values)

        return rows
