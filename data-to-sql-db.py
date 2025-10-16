import os
import subprocess

# initiate list of shell processes that will start running sqlite3, open the database and set the mode to tab-separated values
processes = ['sqlite3', 'dbname.db', '.mode csv', '.separator "\t"'] 

# get all files in data folder
for file in os.listdir('EHITables'):
    # get table name from file name
    filename = file.split('.')[0]
    # create string that will import tsv data into table of same name
    command = " ".join(['.import', '"/path/Requested Record/EHITables/' + file + '"', filename])
    # add command to list of strings
    processes.append(command)

subprocess.run(processes) # run all the commands
