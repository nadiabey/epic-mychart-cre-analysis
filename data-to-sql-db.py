import os
import subprocess

# initiate list of shell processes that will start running sqlite3, open the database and set the mode to read tab-separated values
# originally used mode csv until encountering "unescaped character" error
processes = ['sqlite3', 'dbname.db', '.mode ascii', '.separator "\t" "\n"'] 

# function to iterate through export folders; only first export will have headers
def import_files(full_path, table_index):
    # get all files in data folder
    for file in os.listdir(full_path):
        filename = file.split('.')[0] # get table name from file name
        # create string that will import tsv data into table of same name
        import_cmd = '.import' if table_index == 0 else '.import --skip 1' # exclude first row for subsequent imports
        command = " ".join([import_cmd, '"' + full_path + file + '"', filename])
        processes.append(command) # add command to list of strings


# list of folder paths
paths = ['/path1/EHITables/', '/path2/EHITables/']
# put each path into function
for path in paths:
    import_files(path, paths.index(path))

subprocess.run(processes) # run all the commands
