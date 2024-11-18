import sys
import os


SPACE = ' '
LAST_ENTRY = chr(9492)
LINE = chr(9472)
VERTICAL_LINE = chr(9474)
CROSS = chr(9500)

class DirectoryTree:
    
    def __init__(self, path=None ):
        #check source of path variable
        if ( len(sys.argv) < 2 and path == None):
            print("Usage: tree.py <path>")
            sys.exit(1)

        if (len(sys.argv) == 2):
            path = sys.argv[1]
        else:
            path = path 

        self.__scan_and_display(path)


    def __scan_and_display(self, path):
        nfiles, ndirectories = self.__print_directory(path)
        if (nfiles == 0 and ndirectories == 0):
            print(f"No files or directories found in {os.path.abspath(path)}")
            return
        
        print("\n")
        print(f"{str(nfiles)} file(s), in {str(ndirectories)} directories")
        print(f"Starting directory: {os.path.abspath(path)}")

    def __print_directory(self, path, prefix_pattern = "", intendation_level = 0, is_last_directory = False):

        if (os.path.exists(path) == False):
            print(f"Error: Path {os.path.abspath(path)} can not be found!")
            return (0,0)

        if (intendation_level == 0):
            os.chdir(path)
            print(f"{os.path.abspath(path)}")
        else:
            if (is_last_directory == True):
                prefix_pattern += 3*SPACE
            else:
                prefix_pattern += VERTICAL_LINE+ 2*SPACE

        if (os.access(path, os.F_OK) == False):
            print(f"{prefix_pattern}{LAST_ENTRY} NO PERMISSION {path.name}")
            return (0,0)

        #get list of files and directories
        dir_list = self.__try_scan_dir(path, prefix_pattern)

        if (dir_list is None):
            return (0,0)

        #sort the list by name   
        sorted_list = sorted(dir_list, key=lambda f: f.name.lower(), reverse=False)

        nfiles = 0
        ndirectories = 0
        is_last_directory = False

        for entry in sorted_list :

            if (entry.is_dir() or entry.is_file()):             
                
                #create line pattern for optical representation
                line_pattern = ''

                #special case for last file or directory
                if (entry == sorted_list[-1]):
                    is_last_directory = True
                    line_pattern =  LAST_ENTRY + LINE
                else:
                    line_pattern = CROSS + LINE

                print(f"{prefix_pattern}{line_pattern}{SPACE}{entry.name}")
                
                if (entry.is_dir()):
                    ndirectories += 1
                    (sub_nfiles, sub_ndirectories) = self.__print_directory(entry, prefix_pattern, intendation_level + 1, is_last_directory)      
                    nfiles += sub_nfiles
                    ndirectories += sub_ndirectories
                else:
                    nfiles += 1 

        dir_list.close()
        return (nfiles, ndirectories)

    #try scan directory and catch exceptions    
    def __try_scan_dir(self, path, prefix_pattern):
        dir_list = None
        try:
            dir_list = os.scandir(path) 
            if (dir_list is None):
                print(f"{prefix_pattern}{LAST_ENTRY} NO PERMISSION { path.name}")
                return None
        except PermissionError:
            print(f"{prefix_pattern}{LAST_ENTRY} NO PERMISSION { path.name}")
            return None
        except FileNotFoundError:
            print(f"{prefix_pattern}{LAST_ENTRY} FILE NOT FOUND { path.name}")
        except OSError:
            print(f"{prefix_pattern}{LAST_ENTRY} OS ERROR { path.name}")
            return None
        
        return dir_list


if __name__ == "__main__":
    DirectoryTree("D:")