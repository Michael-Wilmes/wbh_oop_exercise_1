import sys
import os
import tkinter as tk
from tkinter import scrolledtext

NEW_LINE = '\n'
SPACE = ' '

LAST_ENTRY = chr(9492)
LINE = chr(9472)
VERTICAL_LINE = chr(9474)
CROSS = chr(9500)

class DirectoryTree:
    
    def __init__(self):

        self.root = tk.Tk("Directory Tree")
        self.root.title("Directory Tree Viewer")
        self.root.geometry('800x800')
        self.root.resizable(True, True)
        self._text_widget = scrolledtext.ScrolledText(self.root, wrap = tk.WORD)
        self._text_widget.tag_config("no_permission", background="white", foreground="red")

    def show_window(self):
        
        self._text_widget.pack(expand = 1, fill = 'both')
        self.root.mainloop()

    def start(self, path=None):

        #check source of path variable
        if ( len(sys.argv) < 2 and path == None):
            print("Usage: tree.py <path>")
            sys.exit(1)

        if (len(sys.argv) == 2):
            path = sys.argv[1]
        else:
            path = path 

        nfiles, ndirectories = self.print_directory(path)

        if (nfiles == 0 and ndirectories == 0):
            self._text_widget.insert(tk.END, "No files or directories found in " + os.path.abspath(path) + NEW_LINE)
            return
        
        mes = NEW_LINE*3 + str(nfiles) + " file, in " + str(ndirectories) + " directories  " + NEW_LINE
        self._text_widget.insert(tk.END, mes)
        self._text_widget.insert(tk.END, 'Starting directory: ' + os.path.abspath(path) + NEW_LINE)


    def print_directory(self, path, prefix_pattern = "", intendation_level = 0, is_last_directory = False):

        if (os.path.exists(path) == False):
            self._text_widget.insert(tk.END, "Error: Path '" + os.path.abspath(path) +  "' can not be found! " + NEW_LINE)
            return (0,0)

        if intendation_level == 0:
            os.chdir(path)
            self._text_widget.insert(tk.END, os.path.abspath(path) + NEW_LINE)
        else:
            if is_last_directory == True:
                prefix_pattern += 3*SPACE
            else:
                prefix_pattern += VERTICAL_LINE+ 2*SPACE

        if os.access(path, os.F_OK) == False:
            self._text_widget.insert(tk.END, prefix_pattern + LAST_ENTRY + " NO PERMISSION " + path.name + NEW_LINE, "no_permission")
            return (0,0)

        #get list of files and directories
        dir_list = self.try_scan_dir(path, prefix_pattern)

        if dir_list is None:
            return (0,0)

        #sort the list by name   
        sorted_list = sorted(dir_list, key=lambda f: f.name.lower(), reverse=False)

        nfiles = 0
        ndirectories = 0
        is_last_directory = False

        for entry in sorted_list :

            if entry.is_dir() or entry.is_file():             
                
                #create line pattern for optical representation
                line_pattern = ''

                #special case for last file or directory
                if entry == sorted_list[-1]:
                    is_last_directory = True
                    line_pattern =  LAST_ENTRY + LINE
                else:
                    line_pattern = CROSS + LINE

                self._text_widget.insert(tk.END, prefix_pattern +  line_pattern + SPACE +  entry.name + NEW_LINE)

                if entry.is_dir():
                    ndirectories += 1
                    (sub_nfiles, sub_ndirectories) = self.print_directory(entry, prefix_pattern, intendation_level + 1, is_last_directory)      
                    nfiles += sub_nfiles
                    ndirectories += sub_ndirectories
                else:
                    nfiles += 1 

        dir_list.close()
        return (nfiles, ndirectories)

    #try scan directory and catch exceptions    
    def try_scan_dir(self, path, prefix_pattern):
        dir_list = None
        try:
            dir_list = os.scandir(path) 
            if dir_list is None:
                self._text_widget.insert(tk.END, prefix_pattern + LAST_ENTRY + " NO PERMISSION " + path.name + NEW_LINE, "no_permission")
                return None
        except PermissionError:
            self._text_widget.insert(tk.END, prefix_pattern + LAST_ENTRY + " NO PERMISSION " + path.name + NEW_LINE, "no_permission")
            return None
        except FileNotFoundError:
            self._text_widget.insert(tk.END, prefix_pattern + LAST_ENTRY + " FILE NOT FOUND " + path.name + NEW_LINE, "no_permission")
        except OSError:
            self._text_widget.insert(tk.END, prefix_pattern + LAST_ENTRY + " OS ERROR " + path.name + NEW_LINE, "no_permission")
            return None
        
        return dir_list


if __name__ == "__main__":
    tree = DirectoryTree()
    tree.start("D:")
    tree.show_window()


#quellen: 
#https://www.pythontutorial.net/

 #todo: (gilt für alle Aufgaben)
 # Quellenangabe
 # auf probleme eingehen
 #  - Java Klammer Aufgabe ("zählt nur Klammer Paare") 
 #  - Java Koch Kurve: Darstellung bei Level > 5, Berechnung der Linien  bei Änderung der Punkte-Reihenfolge


