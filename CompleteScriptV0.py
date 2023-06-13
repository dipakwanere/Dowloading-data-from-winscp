"""
    _summary_:
        Please make sure to replace 'your_hostname', 'your_username', 'your_password', 
        '/path/to/remote_directory', '/path/to/local_directory', and '/path/to/excel_report.xlsx' 
        with the appropriate values in the example usage section.
    """

import os
import paramiko
import openpyxl
import time

def download_files(hostname, username, password, remote_path, local_path):
    # Create an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        client.connect(hostname, username=username, password=password)

        # Create an SCP client
        scp = client.open_sftp()

        # Change to the remote directory
        scp.chdir(remote_path)

        # List the files in the remote directory
        files = scp.listdir()

        # Download each file from the remote directory
        for file in files:
            remote_file_path = remote_path + '/' + file
            local_file_path = local_path + '/' + file
            scp.get(remote_file_path, local_file_path)
            print(f"Downloaded: {file}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the SCP client and the SSH connection
        scp.close()
        client.close()

def download_most_recent_files(hostname, username, password, remote_path, local_path, selected_dates=None):
    # Create an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        client.connect(hostname, username=username, password=password)

        # Create an SCP client
        scp = client.open_sftp()

        # Change to the remote directory
        scp.chdir(remote_path)

        # List the files and folders in the remote directory
        files = scp.listdir_attr()

        # Filter files based on selected dates or find the most recent date
        filtered_files = []
        if selected_dates:
            for file in files:
                file_date = file.st_mtime
                file_date_str = time.strftime('%Y-%m-%d', time.localtime(file_date))
                if file_date_str in selected_dates:
                    filtered_files.append(file)
        else:
            most_recent_file = max(files, key=lambda f: f.st_mtime)
            filtered_files.append(most_recent_file)

        # Download each file from the remote directory
        for file in filtered_files:
            remote_file_path = remote_path + '/' + file.filename
            local_file_path = local_path + '/' + file.filename
            scp.get(remote_file_path, local_file_path)
            print(f"Downloaded: {file.filename}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the SCP client and the SSH connection
        scp.close()
        client.close()

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
hostname = 'your_hostname'
username = 'your_username'
password = 'your_password'
remote_path = '/path/to/remote_directory'
local_path = '/path/to/local_directory'
selected_dates = ['2023-06-01', '2023-06-05']

# Download files
download_files(hostname, username, password, remote_path, local_path)

# Download most recent files
download_most_recent_files(hostname, username, password, remote_path, local_path, selected_dates)

# Check .xlsx files and data
check_xlsx_files(local_path)

# Generate Excel report
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
