import re
hand = open('mbox-short.txt')
for line in hand:
	line=line.rstrip()
	if(re.search('From: ',line)):
		print(line)
hand = open('mbox-short.txt')
for line in hand:
	line=line.rstrip()
	if(re.search('^X-DS.*:',line)):
		print(line)
hand = open('mbox-short.txt')
for line in hand:
	line=line.rstrip()
	if(re.search('^X-\S+:',line)):
		print(line)