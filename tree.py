import os
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class DirectoryTree:

    
    def __init__(self):

        self.root = tk.Tk("Directory Tree")
        self.root.title("Directory Tree Viewer")
        self.root.geometry('600x400+50+50')
        self.root.resizable(False, False)
        self.root.iconbitmap('./assets/my_icon.ico')
        ttk.Label(self.root, text=chr(9472)).pack()
        ttk.Label(self.root, text=chr(9474)).pack()
        ttk.Label(self.root, text=chr(9492)).pack()
        ttk.Label(self.root, text=chr(9500)).pack()
        self._text_widget = scrolledtext.ScrolledText(self.root)
        

    def show_window(self):
        self._text_widget.pack()
        self.root.mainloop()

    def print_directory(self,path):
        dir_list = os.scandir(path)

        self._text_widget.insert(tk.END, os.path.abspath(path) + '\n')
        sorted_list = sorted(dir_list, key=lambda f: f.name.lower(), reverse=False)
        
        for entry in sorted_list :
            if entry.is_dir() or entry.is_file():
                print(entry.name)
                #todo use printf for better formatting
                #check if entry is the last one in the list
                if entry == sorted_list[-1]:
                    self._text_widget.insert(tk.END, chr(9492) +  chr(9472) + ' ' +  entry.name + '\n')
                else:
                    self._text_widget.insert(tk.END, chr(9500) + chr(9472) + ' ' +  entry.name + '\n')
            
        dir_list.close()
        self.show_window()

if __name__ == "__main__":
    tree = DirectoryTree()
    tree.print_directory("y:")
    tree.show_window()


#quellen: 
#https://www.pythontutorial.net/