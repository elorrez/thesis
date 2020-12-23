# Make a list of all hdf file path names in a directory
import os
import glob

def listfilepaths(directory):
    os.chdir(directory)
    paths = []
    for file in glob.glob("*.hdf"):
        path = os.path.join(directory, file)
        paths.append(path)
    return paths

def listfilenames(directory):
    os.chdir(directory)
    files = []
    for file in glob.glob("*.hdf"):
        #path = os.path.join(directory, file)
        files.append(file)
    return files

