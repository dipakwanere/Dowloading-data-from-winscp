import os
import openpyxl

def check_xlsx_files(directory_path):
    files = os.listdir(directory_path)

    for file in files:
        file_path = os.path.join(directory_path, file)
        if file.endswith('.xlsx'):
            workbook = openpyxl.load_workbook(file_path)
            first_sheet = workbook.worksheets[0]
            if first_sheet['A1'].value == 0:
                print(f"The file '{file}' is an .xlsx file but it has no data.")
            else:
                print(f"The file '{file}' is an .xlsx file and it has data.")
        else:
            print(f"The file '{file}' is not an .xlsx file.")

# Example usage
directory_path = '/path/to/local_directory'
check_xlsx_files(directory_path)
