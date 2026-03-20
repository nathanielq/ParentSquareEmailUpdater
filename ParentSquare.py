# <> Imports <> #
# - Config - #
import config
# - Built-in - #
import csv
import os
import sys
import glob
from datetime import datetime
# - Third-party - #
import paramiko
import polars as pl

sys.stdout = open(config.log_file,'a', encoding='utf-8')
sys.stderr = sys.stdout
print(f'Starting ParentSquare.py at {datetime.now()}\n\n')

# <> Replace Staff District Emails With Personal Emails <> #
def Get_Guardians():
    # - Read in staff-parent email file - #
    with open(config.staff_file, encoding='utf-8') as staff_f:
        reader = csv.DictReader(staff_f)
        mappings = [{'parent_id':row['sourcedId'][9:], 'email':row['new_email']} for row in reader if row['new_email'] != '']
    # - Read in the full parents file - #
    try:
        parents_df = pl.read_csv(config.guardians_path, encoding='utf-8-sig')
    except:
        raise Exception("Could not read parents csv! Program stopped! Check filename/permissions/path!") 
    
    # - Drop unusable columns - #
    parents_df = parents_df.select(config.start_cols)
    # - Add new ParentSquare required columns | Cast parent_id as string | force leading zeros on student IDs  - #
    parents_df = parents_df.with_columns(
        *(pl.lit('').alias(col) for col in config.add_cols),
        (pl.col('parent_id').cast(pl.String)),
        student_id=pl.col('student_id').cast(pl.String).str.zfill(7)
    )
    # - convert mappings list to a dataframe - #
    key_df = pl.from_dicts(mappings)
    key_df = key_df.with_columns(pl.col('parent_id').cast(pl.String))
    # - Join the two dataframes on parentId key. Left join to keep in rows where there is no match - #
    parents_df = parents_df.join(key_df, on="parent_id", how='left')
    # - When our domain is in the email column replace with the staff's personal email, otherwise just leave it as original email - #
    parents_df = parents_df.with_columns(pl.when(
        pl.col('email').str.contains('@domain.org')).
        then(pl.col('email_right')).
        otherwise(pl.col('email')).
        alias('email')
    )
    # - drop the email_right column created by .join - #
    parents_df = parents_df.drop('email_right')

    print(parents_df)
    # - Write to csv for uploading - #
    try:
        parents_df.write_csv(config.upload_csv, separator=',')
    except:
        raise Exception('Could not write to upload CSV! Program stopped! Check file!')

# <> Updated method of deleting. Check modified time, if over a day ago delete <> #
def Delete_File():
    for name in glob.glob((config.guardians_dir + 'parents*')):
        if '_21' in name:
            print(f'Deleting {name}..')
            try:
                os.remove((config.guardians_dir + name))
            except FileNotFoundError:
                print(f'{name} not found, unable to delete')
            except PermissionError:
                print(f'Unable to delete {name}')
            print(f'Deleted {name}')
        else:
            print('No files to delete.')


# <> Uses Paramiko to open an SSH connection to the parentsquare sftp server. Put action to upload file. #
def Upload_File():
    transport = paramiko.Transport((config.server,config.port))
    transport.connect(username=config.username, password=config.password)

    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        sftp.put(config.upload_csv, config.remote_path, confirm=False)
        print("Parents.csv uploaded successfully to ParentSquare server")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sftp.close()
        transport.close()

# <> Function Calls <> #
if __name__ == '__main__':
    Delete_File()
    Get_Guardians()
    Upload_File()
    print(f'\n\nFinished running parentsquare.py')