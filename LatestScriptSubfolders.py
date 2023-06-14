import os
import paramiko
import zipfile

# Function to download and extract .xlsx files from zip files recursively
def download_and_extract_xlsx(sftp, remote_path, local_path):
    # Retrieve file and directory information from remote path
    files = sftp.listdir_attr(remote_path)

    # Iterate through each file/directory
    for file in files:
        filename = file.filename
        remote_filepath = os.path.join(remote_path, filename)
        local_filepath = os.path.join(local_path, filename)

        # Download and extract zip file if it's not a directory
        if not file.st_mode & paramiko.stat.S_IFDIR and filename.endswith('.zip'):
            print(f"Downloading: {remote_filepath}")
            sftp.get(remote_filepath, local_filepath)

            # Extract .xlsx files from the downloaded zip file
            extract_xlsx_files(local_filepath, local_path)
        elif file.st_mode & paramiko.stat.S_IFDIR:
            # Recursively call function for subdirectories
            os.makedirs(local_filepath, exist_ok=True)
            download_and_extract_xlsx(sftp, remote_filepath, local_filepath)

# Function to extract .xlsx files from a zip file
def extract_xlsx_files(zip_filepath, destination_folder):
    print(f"Extracting: {zip_filepath}")
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('.xlsx'):
                zip_ref.extract(file, destination_folder)

# Establish SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('your_server_address', username='your_username', password='your_password')

# Create SFTP client
sftp = ssh.open_sftp()

# Remote and local paths
remote_path = '/path/to/remote_directory'
local_path = '/path/to/local_directory'

# Download and extract .xlsx files
download_and_extract_xlsx(sftp, remote_path, local_path)

# Close SFTP and SSH connections
sftp.close()
ssh.close()
