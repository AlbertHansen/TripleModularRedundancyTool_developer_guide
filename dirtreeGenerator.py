import os

# Place this in the preamble of your Latex project
# \usepackage{dirtree}

# E.g. C:/Users/user/Desktop/Folder/ on windows or /home/user/Desktop/Folder/ on Linux
dir = "C:/Users/alber/git_repositories/TripleModularRedundancyTool_developer_guide/"



# Link to the Github e.g. https://github.com/UnknownDK/LaTeX-Dirtree-Generator/
gitlink = "https://github.com/AlbertHansen/TripleModularRedundancyTool_developer_guide"
gitlink = gitlink.replace("\\", "/").replace("//", "/").replace("_", "\_")              # replace common errors with latex

# Name of branch
branch = "master"

# List of folders to include in the dirtree.
whitelist = ['figures', 'helper\_functions', 'rewire\_scripts', 'triplicate\_scripts', 'update\_scripts']

# List of folders and file extensions to ignore in the dirtree.
ignorelist = []

def dirtreeGenerate(startpath : str, whitelist : list, ignorelist : list):
    """dirtreeGenerate generates a directory tree for latex using the dirtree package.

    Parameters
    ----------
    startpath : string
        Directory to start the dirtree from.
    whitelist : list
        List of folders to include in the dirtree.
    ignorelist : list
        List of folders and file extensions to ignore in the dirtree.
    """
    with open("dirtreeAppendix.tex", "w") as open_file:
        open_file.write("\chapter{Github References}\label{app:GitHubRef} \n") # start dirtree
        open_file.write("\dirtree{% \n") # start dirtree
        for dirpath, dirnames, filenames in os.walk(startpath):
            dirpath = dirpath.replace("\\", "/").replace("//", "/").replace("_", "\_")              # replace common errors with latex
            startpath_clean = startpath.replace("\\", "/").replace("//", "/").replace("_", "\_")    # replace common errors with latex
            dirpath = dirpath.replace(startpath_clean, '')      

            if dirpath.split("/")[0] not in whitelist and len(whitelist) != 0:          # if the last folder in the path is not in the whitelist
                continue                                                                # skip the folder

            # SKAL FIKSES SÅ TINGENE I UNDERMAPPEN IKKE BLIVER PRINTET
            for element in dirpath.split("/"):  
                if element.strip() in ignorelist:                                
                    break                                                            # skip the folder
            else: 
                directory   = dirpath.split("/")[-1]                                        # get directory name            
                indentation = dirpath.count("/") + 1                                        # calculate indentation for directory

                # write directory to dirtree
                open_file.write("." + str(indentation) + " \href{" + gitlink + "tree/" + branch + "/" + dirpath + "/}{" + directory + "/}.\n")
                for files in filenames:
                    if files.split(".")[-1] in ignorelist:
                        continue
                    # write files to dirtree
                    open_file.write("." + str(indentation + 1) + " \href{" + gitlink + "blob/" + branch + "/" + dirpath + "/" + files + "}{" + files.replace("\\", "/").replace("//", "/").replace("_", "\_") + "}.\n")

        open_file.write("}")    # end dirtree

dirtreeGenerate(dir, whitelist, ignorelist)
