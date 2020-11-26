# requirements-data

## Disclaimer
To comply with the Terms of Use of the libraries www.everyspec.com, www.etsi.org/standards, www.eurocontrol.int, sci.esa.int and ntrs.nasa.gov, we only share the source URLs of the collected requirement documents in this data set. 
We do not claim any ownership rights to the documents.

## Setup
The URLs of all documents are stored in the `raw-documents/urls.txt` file. 
To download all documents into the `raw-documents` folder, just run the python script `raw-documents/download_documents.py`. 

## Extraction & Preprocessing
To extract and preprocess all sentences from the documents just run the python script `sentence-extraction/extract_sentences.py`. This will exctract sentences from all pdf files currently located in the 'raw-documents' folder and save them line by line to `sentences/sentences_<current date>.txt`.

## Add new URLs
If you want to add new requirement documents to the set, just run the python script `raw-documents/add_urls.py`. This script will first check for duplicates in the URLs file and then let you enter new URLs. 

 