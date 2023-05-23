# version 0

import re

# build regex patterns to use later
# OUI pattern
pattern1 = "((\w+:){3})"

# input stream from 'sho fdb' command
show_fdb = open("show_fdb.log", 'r')

fdb_file = open("fdb_file", 'w')

# find OUIs
for line in show_fdb:
    match = re.search(pattern1, line)
    if match != None:
        print(line)
        fdb_file.write(line)

fdb_file.close()