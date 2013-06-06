# -*- coding: utf-8 -*-
# handles all adding, removing, and delivery of files
# it doesn't work with the files beyond that
import re
import tkFileDialog

import joinfile

# TO DO: arcpy, csv, sqlite
#try:
#    import arcpy
#    # example, i'm guess it's more involved selecting something from an esri database
#    askopenfiletype['filetypes'].append(('gdb layers','.gdb'))
#except:
#    pass


class FileManager(object):
    def __init__(self):
        # all variables are meant to be accessed through functions
        # filesbyfilename[filename] = JoinFile
        self.filesbyfilename = {}
        # filenamesbyalias[alias] = filename
        self.filenamesbyalias = {}
        # JoinFile
#        self.targetFile = joinfile.JoinFile()
        
        # usable filetypes (and initial directory)
        self.askopenfiletype = {}
        self.askopenfiletype['filetypes'] = [('dbf files','.dbf'), ('dbf files','.DBF')]
        
        
    def _isnew(self, filename):
        return filename not in self.filesbyfilename
        
    def addfile(self):
        """Open a new file. If the file is already open, add an alias for it"""
        filename = tkFileDialog.askopenfilename(**self.askopenfiletype)
        
        # check that a file was selected
        if filename:
            # save the directory so that it defaults there next time a file dialog is opened
            pathsplit = re.findall('[a-zA-Z0-9\.]+',filename)
            self.askopenfiletype['initialdir'] = filename[:-len(pathsplit[-1])]
            
            # check if file is already opened
            if filename in self.filesbyfilename:
                newFile = self.filesbyfilename[filename]
            else:
                # open the file. need to catch exceptions in JoinFile
                newFile = joinfile.JoinFile(filename)
                self.filesbyfilename[filename] = newFile
                
            # get a unique alias (in case another loaded file has the same name)
            filealias = newFile.generatealias()
            while filealias in self.filenamesbyalias:
                filealias = newFile.generatealias()
            self.filenamesbyalias[filealias] = filename
                
            return filealias
        # return empty string if no file was selected
        return ''
        
    def removefile(self, alias):
        """Remove an alias for a file and remove/close the file if it has no other alias"""
        filename = self.filenamesbyalias[alias]
        del self.filenamesbyalias[alias]
        # if the file has no other alias pointing to it, close the file and remove it
        if filename not in self.filenamesbyalias.keys():
            self.filesbyfilename[filename].close()
            del self.filesbyfilename[filename]
            
    def openoutputfile(self, filename):
        return joinfile.JoinFile(filename, mode='w')
        
    def __getitem__(self, key):
        """Return a file object given either a file name or alias"""
        if key in self.filenamesbyalias:
            return self.filesbyfilename[self.filenamesbyalias[key]]
        # not sure if this will be useful
        elif key in self.filesbyfilename:
            return self.filesbyfilename[key]
            
    def __iter__(self):
        return iter([self.filesbyfilename[fn] for fn in self.filesbyfilename])
            