import exsh

fdb = exsh.clicmd('sho fdb', capture=True)
fdb = fdb.splitlines(True)

f = open('fdb_output.txt', 'w')

f.writelines(fdb)

f.close()

print("Done")
