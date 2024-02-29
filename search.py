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
    filepath = 'Library'
    shouldOpen = False

    opts, args = getopt.getopt(argv, "hm:i:f:o",["--mode","--input", "--help", "--file", "--filepath", "--open"])
    for opt, arg in opts:
        # print usage info and exit if -h is specified
        if opt in ('-h', '--help'):
            print("search.py -m <mode: folder, ...> -i <search: str> -f <relative path to directory or file: str> [-o: flag to autoopen files, -h: prints usage] ") # TODO write actually decent help instructions
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

    # check what to run if run from cli and execute the necessary functions with the necessary arguments, etc.
    #print(f"searching {mode} for \"{input}\"")
    if mode == 'folder':
        d_foldersearch = pd.DataFrame(foldersearch(input, filepath, shouldOpen=shouldOpen), columns=["filename", "pagenumber", "occurences"])
        print(d_foldersearch)
    elif mode == 'file':
        d_filesearch = pd. DataFrame(filesearch(input, filepath, shouldOpen=shouldOpen), columns=["page", "pagenumbers"])
        print(d_filesearch)
    else:
        print("please specify a valid mode by which to search")

# searches folder "path" for string (usually 'library'), returns array of arrays : filename, pagenumber, occurences
def foldersearch(input : str, path : str, shouldOpen : bool = False):
    hits = []
    # Iterate over contents of specified path "path" and check wether they are pdfs; if yes open PDF and look for searchstring in pages.
    for file in os.listdir(path):
        if file.endswith('.pdf'):    
            FileReader = PyPDF2.PdfReader(f"{path}/{file}")
            hasOccured = False
            for page in FileReader.pages:
                # if input string is found in extracted text from page print filename and pagenumber
                if input in page.extract_text():
                    hits.append([file, FileReader.get_page_number(page) + 1, page.extract_text().count(input)]) # Add 1 to pagenumber due to 0- vs. 1-indexing :/
                    hasOccured = True
            # check, wether script should open file in browser and wether a occurence was found in the file. If yes: open new tab to file://... URL.
            if hasOccured & shouldOpen:
                webbrowser.open_new_tab(f"file://{os.path.abspath(f"{path}/{file}")}") # f"{path}/{file} curiously worked to fix issue, where os.path.abspath(file) didn't open cwd/path/file but cwd/file. Looking at earlier code this usage actually kinda makes sense :/
        else: 
            print(f"non-pdf file found in library: {file}. continuing with search...")
    return hits

# searches file at "path" for string (usually 'library'), returns array of arrays : pagenumber, occurences
def filesearch(input : str, filepath : str, shouldOpen : bool = False):
    # check wether wether specified path filepath is pdf; if yes open PDF and look for searchstring in pages.
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
        # check, wether script should open file in browser and wether a occurence was found in the file. If yes: open new tab to file://... URL.
        if hasOccured & shouldOpen:
            webbrowser.open_new_tab(f"file://{os.path.abspath(filepath)}")
    return hits  
    
# Entrypoint
if __name__ == "__main__":
    main(sys.argv[1:])