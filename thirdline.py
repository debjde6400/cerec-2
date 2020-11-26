ipr = input()
nl =0

for i in range(len(ipr)):
  if ipr[i]=='\n':
    if(nl<1):
      nl+=1
    else:
      j=i+1
      while(ipr[j]!='\n'):
        j+=1
      print(ipr[i:j+1])
        
