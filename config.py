# - Imports - #
import keyring
# - file_paths - #
guardians_dir = 'PATH_TO_FILE'
guardians_path = guardians_dir + 'parents.csv'
staff_file = 'PATH_TO_FILE'
log_file = 'PATH_TO_LOG_FILE'
upload_csv = 'PATH_TO_FILE_TO_UPLOAD'
# - Paramiko - #
server = 'SERVER_ADDRESS'
port = 22
username = 'USERNAME'
password = keyring.get_password('SERVICE_NAME', username)
remote_path = 'PATH_FOR_UPLOAD'
# - Polars - #
# - csv columns - #
start_cols = ['school_id','student_id','parent_id','first_name','last_name','email','mobile']
add_cols = ['language', 'relationship', 'login', 'secondary_phone', 'educational_rights']