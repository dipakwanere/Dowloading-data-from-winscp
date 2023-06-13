import openpyxl

def generate_excel_report(data_folder, zip_files):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Report'

    sheet['A1'] = 'Data Folders'
    sheet['B1'] = 'Zip Files'
    sheet['C1'] = 'XLSX Files with Data'

    row = 2
    for folder, files in data_folder.items():
        sheet[f'A{row}'] = folder
        sheet[f'B{row}'] = ', '.join(files)

        row += 1

    workbook.save('/path/to/excel_report.xlsx')

# Example usage
data_folder = {
    'Folder 1': ['file1.zip', 'file2.zip'],
    'Folder 2': ['file3.zip']
}

zip_files = {
    'file1.zip': True,
    'file2.zip': False,
    'file3.zip': True
}

generate_excel_report(data_folder, zip_files)
