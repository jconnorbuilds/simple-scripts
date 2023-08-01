#!/usr/bin/env python3

import os
import re
import shlex
import subprocess
from datetime import datetime

print(
"""
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
=====-----=====-----=====-----=====-----=====-----=====
This program will rename your files with today's date,
and it will also set the Created On and Modified On dates
to the current date and time. Useful for re-dating files
to be sent to clients.

Note that you CAN NOT undo this action from Finder.

For the time being, only files (not directories) are supported.
Directories will be ignored. 

When you're done, you can highlight the file and press
cmd+I to verify the dates are correct.
=====-----=====-----=====-----=====-----=====-----=====
"""
      )

current_time = datetime.now()
created_time = current_time.strftime("%m/%d/%Y %H:%M:%S")
modified_time = current_time.strftime("%Y%m%d%H%M.%S")
filename_date = current_time.strftime("%y%m%d")

if __name__ == "__main__":

    files_input = input("Simply drag and drop the files for which you want to change the dates, and press Enter! \n\n")
    files = shlex.split(files_input)

    files_to_process = []
    all_files = []
    ignored_files_and_dirs = []
    modified_files = []
    
    for filepath in files:
        filename = filepath.split('/')[-1]
        new_filename = filename_date + "_" + "_".join(filename.split("_")[1::])
        if os.path.isdir(filepath):
            all_files.append(f"✖︎ {filename}  -  IGNORED (directory)")
            ignored_files_and_dirs.append(filename)
            continue

        # elif re.match(r"^\d{6}", filename):
        #     all_files.append(f"o {filename}")
        #     files_to_process.append(filepath)
        #     continue
        elif not re.match(r"^\d{6}", filename):
            answer = ""
            while answer == "":
                try:
                    answer = input(f"\nThis doesn't look like a file for a client: {filename} \nAre you sure you want to proceed? (y/n) ").lower()
                except:
                    answer = ""
            if answer != "y":
                all_files.append(f"✖︎ {filename}  -  SKIPPED")
                ignored_files_and_dirs.append(filepath)

            else: 
                all_files.append(f"○ {filename} 👉 {new_filename}")
                files_to_process.append(filepath)

        elif os.path.exists("/".join(filepath.split('/')[:-1]) + "/" + new_filename) == True:
            answer = ""
            while answer == "":
                try:
                    answer = input(f"\nA file with this name {new_filename} already exists. Modify anyway? (y/n) ").lower()
                except:
                    answer = ""
            if answer != "y":
                all_files.append(f"✖︎ {filename}  -  IGNORED (file with new name already exists)")
                ignored_files_and_dirs.append(filename)
            else:
                os.rename(filepath, "/".join(filepath.split('/')[:-1]) + "/" + new_filename)
                all_files.append(f"○ {filename} 👉 {new_filename}")
                files_to_process.append(filepath)

        else: 
            all_files.append(f"○ {filename} 👉 {new_filename}")
            files_to_process.append(filepath)
            

    if not files_to_process:
        print("\nNo files were found. Run this script again to try again. Bye!")
        exit()
    else:
        answer = ""
        while answer == "":
            try:
                print("Here are the files you selected:\n")
                for file in all_files: 
                    print(file)
                answer = input(f"\nYOU ARE ABOUT TO MODIFY THE FILES MARKED WITH '○' ({len(files_to_process)} files). \nAre you sure you want to do this? (y/n) ").lower()
            except:
                answer = ""
        if answer != "y":
            print("Later 💨")
            exit()

    for i,filepath in enumerate(files_to_process, start=1):
        filename = filepath.split('/')[-1]
        new_filename = filename_date + "_" + "_".join(filename.split("_")[1::])
        path = "/".join(filepath.split('/')[:-1])
        set_created_date = f"zsh -c 'setfile -d \"{created_time}\" \"{filepath}\"'"
        set_modified_date = f"zsh -c 'touch -t {modified_time} \"{filepath}\"'"
        
        subprocess.run(set_created_date, shell=True)
        subprocess.run(set_modified_date, shell=True)

        if os.path.isfile(filepath):
            os.rename(filepath, "/".join(filepath.split('/')[:-1]) + "/" + new_filename)
            modified_files.append(new_filename)

    print(f"\nThe following file(s) were renamed and reformatted to the current date ({current_time.strftime('%Y/%m/%d %H:%M:%S')}): \n")
    for j,file in enumerate(modified_files, start=1):
        print(f"✅ {j}. {file}")

    print("\nRun this script again to reformat more files. Goodbye! 😈")

    
