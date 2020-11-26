import requests
import sys
import os.path

with open("urls.txt", "r", encoding="utf-8") as urlFile:
    for (i, url) in enumerate(list(urlFile), start=1):
        docFileName = "REQ_DOC_" + str(i) + ".pdf"
        if os.path.exists(docFileName):
            print("Already exists: " + url)
            continue
        
        print("Downloading from " + url)
        url = url.lstrip().rstrip().replace("\n", "")
        if len(url) == 0:
            print("URL at position " + str(i) + " is empty")
            continue
        
        r = requests.get(url, allow_redirects=True)
        if not (r.headers['Content-Type'].startswith("application/pdf") or r.headers['Content-Type'].startswith("application/octet-stream")) :
            print("Not a pdf: " + url)
            print("Content type: " + r.headers['Content-Type'])
            print(r.content)
            sys.exit()
        if r.status_code != 200:
            print("URL not working: " + url)
            sys.exit()
        with open(docFileName, 'wb') as f:
            f.write(r.content)
            
