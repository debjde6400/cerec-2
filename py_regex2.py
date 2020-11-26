import re
hand = open('mbox-short.txt')
for line in hand:
	line=line.rstrip()
	if(re.findall('^From (\S+@\S+) ',line)):
		print(line)
		words = line.split()
		email=words[1]
		pieces=email.split('@')
		print(pieces[1])
		print(re.findall('@([^ u]*)',line))