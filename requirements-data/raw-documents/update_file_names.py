import glob
import os
import re

reqFileNames = glob.glob("REQ_DOC_*.pdf") # get all pdf files

reqFileNames.sort(key=lambda f: int(re.sub('\D', '', f)))

index = 1
for fileName in reqFileNames:
    print(fileName)
    newName = re.sub(r'\d+', str(index), fileName)
    print(newName)
    os.rename(fileName,newName)
    index = index + 1
