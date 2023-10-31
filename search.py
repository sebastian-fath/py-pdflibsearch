""" 
name: py-pdflibsearch
author: Sebastian Fath
version: 0.1
created: 2023-10-31
last updated: 2023-10-31
 """

import sys, getopt
import os
import PyPDF2
import pandas as pd

def main(argv):
    # set defaults
    mode = 'folder'
    input = ''

    opts, args = getopt.getopt(argv, "hm:i:",["--mode","--input"])
    for opt, arg in opts:
        if opt == '-h':
            print("search.py -m <mode: folder, ...> -i <search: str>")
            sys.exit()
        if opt in ('-m', '--mode'):
            mode = arg
        if opt in ('-i', '--input'):
            input = arg

    #print(f"searching {mode} for \"{input}\"")
    if mode == 'folder':
        d_foldersearch = pd.DataFrame(foldersearch(input), columns=["filename", "pagenumber", "occurences"])
        print(d_foldersearch)
    else:
        print("please specify a mode by which to search")

# searches "library" folder for string, returns array of arrays : filename, pagenumber, occurences
def foldersearch(input):
    hits = []
    for file in os.listdir('library'):
        if file.endswith('.pdf'):    
            #FileObject = open(f"library/{file}")
            ##FileReader = PyPDF2.PdfReader(FileObject)
            FileReader = PyPDF2.PdfReader(f"library/{file}")
            for page in FileReader.pages:
                # if input string is found in extracted text from page print filename and pagenumber
                if input in page.extract_text():
                    hits.append([file, FileReader.get_page_number(page), page.extract_text().count(input)])
            #FileObject.close()
        else: 
            print(f"non-pdf file found in library: {file}. continuing with search...")
    return hits

# Entrypoint
if __name__ == "__main__":
    main(sys.argv[1:])