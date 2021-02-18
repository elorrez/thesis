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

def listfilepaths_tiff(directory):
    os.chdir(directory)
    paths = []
    for file in glob.glob("*.tiff"):
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

def listcoords_csv(directory):
    os.chdir(directory)
    coords = []
    for file in glob.glob("*.csv"):
        coord = file.split('_')[-1].split('.csv')[0]
        coords.append(coord)
    return coords

