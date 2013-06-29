"""FileManager handles all adding, removing, and delivery of files.

It doesn't do anything further with the files.""" 
# -*- coding: utf-8 -*-
##
#   Copyright 2013 Chad Spratt
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
##
# 
import joinfile

class FileManager(object):
    """Manages opening, closing, and providing access to files."""
    def __init__(self):
        # all variables are meant to be accessed through functions
        # filesbyfilename[filename] = JoinFile
        self.filesbyfilename = {}
        # filenamesbyalias[alias] = filename
        self.filenamesbyalias = {}
        # usable filetypes (and initial directory)
        self.filetypes = {}
        self.filetypes['All files'] = {'mimes' : [], 'patterns' : ['*']}
        self.filetypes['dbf files'] = {'mimes' : ['application/dbase', 
                                                  'application/x-dbase', 
                                                  'application/dbf', 
                                                  'application/x-dbf'],
                                       'patterns' : ['*.dbf']}
        
    def addfile(self, filename):
        """Open a new file. If the file is already open, add an alias for it."""        
        # check if file is already opened
        if filename in self.filesbyfilename:
            newfile = self.filesbyfilename[filename]
        else:
            # open the file. need to catch exceptions in JoinFile
            newfile = joinfile.JoinFile(filename)
            self.filesbyfilename[filename] = newfile
            
        # get a unique alias (in case another loaded file has the same name)
        filealias = newfile.generatealias()
        while filealias in self.filenamesbyalias:
            filealias = newfile.generatealias()
        self.filenamesbyalias[filealias] = filename
            
        return filealias
        
    def removealias(self, alias):
        """Remove an alias and remove the file if it has no other aliases."""
        filename = self.filenamesbyalias[alias]
        del self.filenamesbyalias[alias]
        # if the file has no other alias pointing to it, close and remove it
        if filename not in self.filenamesbyalias.values():
            self.filesbyfilename[filename].close()
            del self.filesbyfilename[filename]
            
    @classmethod
    def openoutputfile(cls, filename):
        """Returns a file, with the given filenam,e opened for writing."""
        return joinfile.JoinFile(filename, mode='w')
        
    def __getitem__(self, key):
        """Return a file object given either a file name or alias"""
        if key in self.filenamesbyalias:
            return self.filesbyfilename[self.filenamesbyalias[key]]
            
    def __iter__(self):
        return iter([self.filesbyfilename[fn] for fn in self.filesbyfilename])
            