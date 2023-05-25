import exsh

result = exsh.clicmd('sho fdb', True)

print("----------")
print("Printing sho fdb")
print("----------")
print("")

print(result)

fdb_file = open("fdb_file.txt", 'w')

for line in result:
	fdb_file.write(line)

print("Done\n")
