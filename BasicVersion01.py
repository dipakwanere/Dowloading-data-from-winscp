"""
_summary_:
    To download data folders/files from a WinSCP drive location
    using Python, you can utilize the paramiko library, 
    which provides an implementation of the SSHv2 protocol. 
    Here's an example script that demonstrates how to achieve this

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


"""
_summary_

Make sure to replace 'your_hostname', 'your_username', 'your_password', '/path/to/remote_directory', and '/path/to/local_directory' with the actual values corresponding to your WinSCP configuration.

The script establishes an SSH connection to the remote server using the provided credentials and navigates to the specified remote directory. It then retrieves a list of files present in that directory and proceeds to download each file using SCP (Secure Copy Protocol) to the local directory.

Note: You need to have the paramiko library installed in your Python environment. You can install it using pip:


"""

#pip install paramiko
