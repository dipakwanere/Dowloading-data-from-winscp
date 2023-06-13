"""
_summary_:

   Please note that you need to provide the appropriate values 
   for the hostname, username, password, remote path, local path, 
   and other paths in the scripts. Also, make sure to have the 
   required libraries (paramiko and openpyxl) installed in your Python environment. 


"""





import paramiko

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

# Example usage
hostname = 'your_hostname'
username = 'your_username'
password = 'your_password'
remote_path = '/path/to/remote_directory'
local_path = '/path/to/local_directory'

download_files(hostname, username, password, remote_path, local_path)
