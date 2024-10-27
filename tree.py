import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class DirectoryTree:

    
    def __init__(self):

        self.root = tk.Tk("Directory Tree")
        self.root.title("Directory Tree Viewer")
        self.root.geometry('800x800')
        self.root.resizable(True, True)
        self._text_widget = scrolledtext.ScrolledText(self.root, wrap = tk.WORD)
        

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
        mes = '\n'*3 + str(nfiles) + " Dateien, in " + str(ndirectories) + " Verzeichnissen"
        self._text_widget.insert(tk.END, mes + '\n')
        self._text_widget.insert(tk.END, 'Starverzeichnis: ' + os.path.abspath(path) + '\n')


    def print_directory(self, path, prefix_pattern = "", intendation_level = 0, is_last_directory = False):
        
        if (os.path.exists(path) == False):
            self._text_widget.insert(tk.END, "Fehler:  Pfad '" + path +  "' konnnte nicht gefunden werden: " + path + '\n')
            return (0,0)

        if intendation_level == 0:
            os.chdir(path)
            self._text_widget.insert(tk.END, os.path.abspath(path) + '\n')
        else:
            if is_last_directory == True:
                prefix_pattern += 3* ' '
            else:
                prefix_pattern += chr(9474) + 2*' '

        if os.access(path, os.F_OK) == False:
            self._text_widget.insert(tk.END, prefix_pattern + chr(9492) + " NO PERMISSION " + path.name + '\n')
            return (0,0)

        try:
            dir_list = os.scandir(path) 
        except PermissionError:
            self._text_widget.insert(tk.END, prefix_pattern + chr(9492) + " NO PERMISSION " + path.name + '\n')
            return (0,0)
        
            
        sorted_list = sorted(dir_list, key=lambda f: f.name.lower(), reverse=False)

        nfiles = 0
        ndirectories = 0
        is_last_directory = False

        for entry in sorted_list :

            if entry.is_dir() or entry.is_file():             
                if entry == sorted_list[-1]:
                    is_last_directory = True
                    self._text_widget.insert(tk.END, prefix_pattern + chr(9492) +  chr(9472) + ' ' +  entry.name + '\n')
                else:
                    self._text_widget.insert(tk.END, prefix_pattern +  chr(9500) + chr(9472)  + ' ' +  entry.name + '\n')

                if entry.is_dir():
                    ndirectories += 1
                    (sub_nfiles, sub_ndirectories) = self.print_directory(entry, prefix_pattern, intendation_level + 1,is_last_directory)      
                    nfiles += sub_nfiles
                    ndirectories += sub_ndirectories
                else:
                    nfiles += 1 

        dir_list.close()
        return (nfiles, ndirectories)
        

if __name__ == "__main__":
    tree = DirectoryTree()
    tree.start("y:")
    tree.show_window()


#quellen: 
#https://www.pythontutorial.net/

 #todo: (gilr für alle Aufgaben)
 # check: String concatenation
 # Kommentieren, was habe ich gemacht
 # Quellenangabe
 # Testen
 # Dokumentieren
 # auf probleme eingehen
 #  - Java Klammer Aufgabe ("zählt nur Klammer Paare") 
 #  - Java Koch Kurve: Darstellung bei Level > 5, Berechnung der Linien  bei Änderung der Punkte-Reihenfolge


