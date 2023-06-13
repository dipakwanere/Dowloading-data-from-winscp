from datetime import time
import os
import paramiko
import openpyxl

def download_files(hostname, username, password, remote_path, local_path, selected_dates=None):
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

            # Check if the file is an Excel file and has data in the first sheet
            if file.filename.endswith('.xlsx'):
                workbook = openpyxl.load_workbook(local_file_path)
                first_sheet = workbook.worksheets[0]
                if first_sheet.max_row > 1:
                    print(f"The file '{file.filename}' has data.")
                else:
                    print(f"The file '{file.filename}' is empty.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the SCP client and the SSH connection
        scp.close()
        client.close()

# Example usage
hostname = 'your_hostname'
username = 'your_username'
password = 'your_password'
remote_path = '/path/to/remote_directory'
local_path = '/path/to/local_directory'

# If you want to download files for specific dates, provide them in YYYY-MM-DD format
selected_dates = ['2023-06-01', '2023-06-05']

download_files(hostname, username, password, remote_path, local_path, selected_dates)


"""
_summary_
In this updated script, the selected_dates parameter allows you to specify a list of dates in the format 'YYYY-MM-DD'. The script will download files from those dates or, if no dates are provided, it will download files from the most recent date.

For Excel files (.xlsx), it checks if they exist and whether the first sheet has any data. If the file is not an Excel file or if it's empty, it will display a corresponding message.

Please note that you need to have the paramiko and openpyxl libraries installed in your Python environment. You can install them using pip:
"""

# pip install paramiko openpyxl