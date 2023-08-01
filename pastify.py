#!/usr/bin/env python3

import os
import re
import shlex
import subprocess
from datetime import datetime
from datetime import time

print(
"""
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
=====-----=====-----=====-----=====-----=====-----=====
This program will rename your files with a date that you set,
appending the date in YYMMDD format (i.e. 230801_myfile.wav)
and it will also set the Created On and Modified On dates
to that date. Useful for re-dating files to be sent to clients.
Note that the current local time will be used for hours/mins/secs.

Note that you CAN NOT undo this action from Finder.

For the time being, only files (not directories) are supported.
Directories will be ignored. 

When you're done, you can highlight the file and press
cmd+I to verify the dates are correct.
=====-----=====-----=====-----=====-----=====-----=====
"""
      )

user_date = ""
current_time = datetime.now()
files_to_modify = []
formatted_files = {}
files_to_ignore = []
modified_files = []

def get_user_date():
    """
    User enters a date in format %y%d%m (YYDDMM).
    
    return: user_date (string in format %y%d%m (YYDDMM).
    """
    user_date_is_valid = False
    date_format = "%y%m%d"
    while user_date_is_valid == False:
        user_date = input("\nEnter the new date for these files (use format YYDDMM): ")
        try:
            user_date_is_valid = bool(datetime.strptime(user_date, date_format))
        except:
            user_date = ""

    return user_date

def format_output_strings(files, user_date):
    """
    ARGS:
    files: a list of files (filepaths)
    user_date: a numerical string in format %y%d%m (YYDDMM)

    RETURNS: None
    """
    
    for filepath in files:
        filename = filepath.split('/')[-1]
        print(f'filename {filename}')
        new_filename = get_new_filename(filename, user_date)
        
        if os.path.isdir(filepath):
            formatted_files[filename] = f"✖︎ {filename}  -  IGNORED (directory)",
            print(1)
            continue

        elif not re.match(r"^\d{6}", filename):
            answer = ""
            while answer == "":
                try:
                    answer = input(f"\nThis doesn't look like a file for a client: {filename} \nAre you sure you want to proceed? (y/n) ").lower()
                except:
                    answer = ""
            if answer != "y":
                formatted_files[filename] = f"✖︎ {filename}  -  SKIPPED"

            else: 
                formatted_files[filename] = f"○ {filename} 👉 {str(user_date)}_{filename}"
                files_to_modify.append(filepath)

        elif os.path.exists("/".join(filepath.split('/')[:-1]) + "/" + new_filename) == True:
            answer = ""
            while answer == "":
                try:
                    answer = input(f"\nA file with this name {new_filename} already exists. Modify anyway? (y/n) ").lower()
                except:
                    answer = ""
            if answer != "y":
                formatted_files[filename] = f"✖︎ {filename}  -  IGNORED (file with new name already exists)"
            else:
                os.rename(filepath, "/".join(filepath.split('/')[:-1]) + "/" + new_filename)
                formatted_files[filename] = f"○ {filename} 👉 {new_filename}"
                files_to_modify.append(filepath)

        else:
            formatted_files[filename] = f"○ {filename} 👉 {new_filename}"
            files_to_modify.append(filepath)

def get_new_filename(filename, user_date):
    new_filename = ""
    if not re.match(r"^\d{6}", filename):
        new_filename = user_date + "_" + filename
    else:
        new_filename = user_date + "_" + "_".join(filename.split("_")[1::])
    
    return new_filename


if __name__ == "__main__":

    files_input = input("Simply drag and drop the files for which you want to change the dates, and press Enter! \n\n")
    files = shlex.split(files_input)
    user_date = get_user_date()

    format_output_strings(files, user_date)
    
    if files_to_modify:
        print("The files will be processed as follows:\n")
        for file in formatted_files:
            print(formatted_files[file])
    else:
        print("\nNo files were found. Run this script again to try again. Bye!")
        exit()

    answer = ""
    while answer == "":
        try:
            answer = input(f"\nYOU ARE ABOUT TO MODIFY THE FILES MARKED WITH '○' ({len(files_to_modify)} files). \nAre you sure you want to do this? (y/n) ").lower()
        except:
            answer = ""
    if answer != "y":
        print("Later 💨")
        exit()
            
    for i,filepath in enumerate(files_to_modify, start=1):
        """
        created_date must be in format "%m/%d/%Y %H:%M:%S"
        modified_date must be in format "%Y%m%d%H%M.%S"
        """
        filename = filepath.split('/')[-1]
        user_date_obj = datetime.strptime(user_date, "%y%m%d")
        new_created_datetime = user_date_obj.strftime("%m/%d/%Y") + " " + current_time.strftime("%H:%M:%S")
        new_modified_datetime = user_date_obj.strftime("%Y%m%d") + current_time.strftime("%H%M.%S")
        new_filename = get_new_filename(filename, user_date)

        path = "/".join(filepath.split('/')[:-1])
        set_created_date = f"zsh -c 'setfile -d \"{new_created_datetime}\" \"{filepath}\"'"
        set_modified_date = f"zsh -c 'touch -t {new_modified_datetime} \"{filepath}\"'"
        
        subprocess.run(set_created_date, shell=True)
        subprocess.run(set_modified_date, shell=True)

        if os.path.isfile(filepath):
            os.rename(filepath, "/".join(filepath.split('/')[:-1]) + "/" + new_filename)
            modified_files.append(new_filename)

    print(f"\nThe following file(s) were renamed and reformatted to the specified date ({datetime.strptime(user_date, '%y%m%d').strftime('%m/%d/%Y')} {current_time.strftime('%H:%M:%S')}): \n")
    for j,file in enumerate(modified_files, start=1):
        print(f"✅ {j}. {file}")

    print("\nRun this script again to reformat more files. Goodbye! 😈")

