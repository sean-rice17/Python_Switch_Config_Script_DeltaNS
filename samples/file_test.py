with open('fdb_output.txt', 'r') as f:
    count = 0
    for line in f:
        count += 1
        print(line)
    if count == 0:
        print("No lines found.")
    else:
        print("Done")