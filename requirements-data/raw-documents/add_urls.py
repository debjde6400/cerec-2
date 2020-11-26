import sys

def cleanUrl(url):
    return url.lstrip().rstrip().replace("\n", "")

def checkForDuplicates(urls):
    urlSet = set()
    for (n, url) in enumerate(urls, start=1):
        if url in urlSet:
            print("Duplicate: " + url)
        urlSet.add(url)


with open("urls.txt", "r", encoding="utf-8") as urlsFile:
    urls = list(urlsFile)
    urls = list(map(cleanUrl , urls))
    checkForDuplicates(urls)

with open("urls.txt", "a+", encoding="utf-8") as urlsFile:
    while True:
        newUrl = input("New URL: ")
        newUrl = cleanUrl(newUrl)
        if newUrl in urls:
            print("This url is already contained in the set")
        elif newUrl == "exit":
            sys.exit()
        else:
            urlsFile.write("\n" + newUrl)
            urls.append(newUrl)
            print("Saved " + newUrl + " to the set")
    
