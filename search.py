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

import webbrowser

def main(argv):
    # set defaults
    mode = 'folder'
    input = ''
    filepath = ''
    shouldOpen = False

    opts, args = getopt.getopt(argv, "hm:i:f:o",["--mode","--input", "--help", "--file", "--filepath", "--open"])
    for opt, arg in opts:
        # print usage info and exit if -h is specified
        if opt in ('-h', '--help'):
            print("search.py -m <mode: folder, ...> -i <search: str> -f <relative path to directory or file: str> [-o: flag to open documents, where string was found] ") # TODO write actually decent help instructions
            sys.exit()
        # this specifies how this program is supposed to be run.
        if opt in ('-m', '--mode'):
            mode = arg
        # all modes require a "searchstring"
        if opt in ('-i', '--input'):
            input = arg
        # for some modes, a filepath can be supplied 
        if opt in ('-f', '--file', '--filepath'):
            filepath = arg
        # parameter to open document with found occurences
        if opt in ('-o', '--open'):
            shouldOpen = True

    #print(f"searching {mode} for \"{input}\"")
    if mode == 'folder':
        if filepath != '':
            d_foldersearch = pd.DataFrame(foldersearch(input, filepath, shouldOpen=shouldOpen), columns=["filename", "pagenumber", "occurences"])
        else:
            d_foldersearch = pd.DataFrame(foldersearch(input, shouldOpen=shouldOpen), columns=["filename", "pagenumber", "occurences"])
        print(d_foldersearch)
    elif mode == 'file':
        d_filesearch = pd. DataFrame(filesearch(input, filepath, shouldOpen=shouldOpen), columns=["page", "pagenumbers"])
        print(d_filesearch)
    else:
        print("please specify a mode by which to search")

# searches folder "path" for string (usually 'library'), returns array of arrays : filename, pagenumber, occurences
def foldersearch(input : str, path : str = 'library', shouldOpen : bool = False):
    hits = []
    for file in os.listdir(path):
        if file.endswith('.pdf'):    
            FileReader = PyPDF2.PdfReader(f"{path}/{file}")
            hasOccured = False
            for page in FileReader.pages:
                # if input string is found in extracted text from page print filename and pagenumber
                if input in page.extract_text():
                    hits.append([file, FileReader.get_page_number(page), page.extract_text().count(input)])
                    hasOccured = True
            if hasOccured & shouldOpen:
                webbrowser.open_new_tab(f"file://{os.path.abspath(path)}")
        else: 
            print(f"non-pdf file found in library: {file}. continuing with search...")
    return hits

# searches file at "path" for string (usually 'library'), returns array of arrays : pagenumber, occurences
def filesearch(input : str, filepath : str, shouldOpen : bool = False):
    if filepath.endswith('.pdf') != True:
        ValueError('file is not specified or is not a .pdf!')
    hits = []
    FileReader = PyPDF2.PdfReader(filepath)
    for page in FileReader.pages:
        hasOccured = False
        # if input string is found in extracted text from page print filename and pagenumber
        if input in page.extract_text():
            hits.append([FileReader.get_page_number(page), page.extract_text().count(input)])
            hasOccured = True
        if hasOccured & shouldOpen:
            webbrowser.open_new_tab(f"file://{os.path.abspath(filepath)}")
    return hits  
    
# Entrypoint
if __name__ == "__main__":
    main(sys.argv[1:])