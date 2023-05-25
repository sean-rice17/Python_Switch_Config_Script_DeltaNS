import re

with open('tokenizeme.txt') as inputfile:
    result = str(' '.join([line.strip('\n') for line in inputfile]))

pattern2 = "(\s){1,}"

result = re.sub(pattern2, '', result)

print(result)