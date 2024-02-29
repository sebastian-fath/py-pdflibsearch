# READ ME

This is a extremely rudimentary implementation of a way to search multiple pdf-files at once. I started this project, as I need(ed) to be able to somewhat easily search a library of many pdf-files regularly. It is entirely not done, wont be for a while and wont be really suitable for actual use for probably anytime.

# Usage

1. Open terminal in directory where search.py is located.
2. create a subdirectory, ideally in the same directory as the python file, in which you store the pdf-files to be searched (usually called "library")
3. run `python search.py -i <search: str>`

## Options and Flags:

- Options:
    - `-i` (`--input`): string for which the programm searches file or directory for
    - `-m` (`--mode`): string specifying what and how the script should search. Options: `'folder' (Standard), 'file'`
    - `-f` (`--file, --filepath`): string specifying non-standard directories or files to search. **REQUIRED WHEN RUNNING IN MODE 'FILE'**.
    - `-h` (`--help`): if specified prints usage
    - `-o` (`--open`): if specified, the programm will automatically open all pdf-files in a webbrowser or standard-editor, where the searchstring was found. 


# Project Roadmap

- [ ] Implement multiple searchterms
- [x] Implement Opening 
    - [ ] Highlighting?
    - [ ] Web-Portal / Integration?