# DataMatching
A script used to cleanup and replace emails in a file uploaded to CSV to save time from manual replacements.

# Tech Stack - Python, Polars, Paramiko

* Updated 3/20/26 *
Improved version of the ParentSquare.py file. Replaced the Pandas data manipulation with Polars to increase speed and modernize the program.

At the district we use ParentSquare for district-to-family communications. ParentSquare populates emails based on information from our SIS. Staff who are also parents by default were having their district email listed in ParentSquare rather than their personal emails. This script takes in two csv files, one that comes daily from the SIS and contains all parents, their emails and student IDs they are associated with. The other is a relatively static csv of staff email to personal email mappings. Using Polars, the script will replace the staff emails with personal and write the validated data to a csv. Paramiko is then used to put the file on ParentSquare's sftp server. A function is also ran to delete old files (Our SIS uses a weird method of overwriting that causes duplicate files to be written).
