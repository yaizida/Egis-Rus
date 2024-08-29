from openpyxl import Workbook
import csv


wb = Workbook()
ws = wb.active
file_name = input('Enter file name: ')
with open(file_name, 'r') as f:
    for row in csv.reader(f):
        ws.append(row)
wb.save(file_name + '.xlsx')
