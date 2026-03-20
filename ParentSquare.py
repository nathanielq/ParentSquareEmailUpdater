import csv
import os
import sys
import paramiko
from datetime import datetime
import pandas as pd

# <>  Running Log <> #
log_file = 'PATH_TO_LOG_FILE'
sys.stdout = open(log_file,'a')
sys.stderr = sys.stdout
print(f'\n\nStarting FILENAME at {datetime.now()}\n\n')

# <> Actual function to get the staff-guardian personal email and map it to their userid <> #
def Get_Guardians():
    guardians = guardians_dir + guardians_file
    staff_emails = {}
    with open(staff_file) as staff_f:
        reader = csv.DictReader(staff_f)
        for row in reader:
            if row['new_email'] == '':
                print(f'No personal email found for {row['email']}')
            staff = {row['sourcedId'][9:] : row['new_email']}
            staff_emails.update(staff)
        try:
            df = pd.read_csv(guardians)
            try:
                df.drop('Employee Name', axis = 1, inplace = True)
                df.drop('Email_2', axis = 1, inplace = True)
            except Exception as e:
                print(f'Error {e}: already deleted!')
            
            #set headers
            df_headers = ['school_id', 'student_id', 'parent_id', 'first_name', 'last_name', 'email', 'mobile', 'language', 'relationship', 'login', 'secondary_phone', 'educational_rights']
            # Add in any columns missing from the csv #
            for header in df_headers:
                if header not in df.columns:
                    position = df_headers.index(header)
                    df.insert(position, header, pd.Series([None]*len(df)))
            df.columns = df_headers

            # ensure leading zeros are on the student_ids
            df['student_id'] = df['student_id'].astype('string')
            i = 0
            for student_id in df['student_id']:
                student_id = student_id
                if student_id[0] != '0':
                    student_id = '0' + student_id
                    df.loc[i, 'student_id'] = student_id
                    #print(df.loc[i, 'student_id'])
                    i = i + 1
            #.keys reference the key in the key-value pair .values references the values <=^)
            print(len(staff_emails))
            for key in staff_emails.keys():
                    print(f'key: {key} == value: {staff_emails[key]}\n')
                    target_index = key #the target in this case being the sourcedid which is how they are being found
                    col_name = 'email'
                    #The line below uses loc to find the row index where sourcedID of parents.csv matches SourcedID of 
                    #staff.csv and then points to the intersection of the column we are modifying, 'email', and that row
                    #Then sets that intersection point, i.e. cell, to that new email value in that location
                    df['parent_id'] = df['parent_id'].astype('string') #staff email id is string so cast parent_id as string
                    #print(df.loc[df['parent_id'] == target_index, col_name].item())
                    df.loc[df['parent_id'] == target_index, col_name] = staff_emails[key]
                    print(f'Guardian id [{key}]: Replaced staff email with {staff_emails[key]}\n')

            df.to_csv(guardians, index=False) #write the dataframe to the csv
        except Exception as e:
            print(f'error {e}')

#self explanatory and used a million times already by me. FIGURE IT OUT.
def Delete_Files():
    files = os.listdir(guardians_dir)
    for file in files:
         if '_' in file:
              path = guardians_dir + file
              os.remove(path)
              print(f'Deleted {path}')

#Good ol paramiko. This bad boy uploads it. Below is the server information.
def upload_file():
    server = 'SERVER ADDRESS'
    port = 22
    username = 'USERNAME'
    password = 'PASSWORD' # Recommended to use keyring if running on a windows device
    local_path = 'PATH_TO_COMPLETED_FILE'
    remote_path = 'FILENAME FOR UPLOAD'

    transport = paramiko.Transport((server,port))
    transport.connect(username=username, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        sftp.put(local_path, remote_path, confirm=False)
        print(f"File {local_path} uploaded successfully to {remote_path}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sftp.close()
        transport.close()

# <> variables/directories <> #
guardians_dir = 'PATH_TO_FILE'
guardians_file = 'FILENAME'
staff_file = 'PATH_TO_FILE'

# Function Calls #
if __name__ == '__main__':
    Delete_Files()
    Get_Guardians()
    upload_file()
    print(f'\n\nFinished running FILENAME')
