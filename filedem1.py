flobj = open('myf.txt','w')
flobj.write('Abc\n Our India will be the most populous country of the world \nand we firmly believe that India will recover her problems \n So we are proud.')
flobj.close()

flobj = open('myf.txt','r')
n_lines = 0
for line in flobj :
    n_lines+=1

print(n_lines)
flobj.close()

