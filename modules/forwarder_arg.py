# The MIT License
#
# Copyright (c) 2024 Dave Jang
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import sys


class Locator:
    def __init__(self, arg_one=".", arg_two="10", arg_three="1"):
        """
            Locator is to track the variables and file IO to send data accurately
        """
        # <directory> is madatory
        self.dirlocator = sys.argv[1] if len(sys.argv) > 1 else arg_one
        # <Interval> is optional
        self.interval = int(sys.argv[2]) if len(sys.argv) > 2 else arg_two
        # <dest option> is optional, then but please add the interval
        self.dest_opt = int(sys.argv[3]) if len(sys.argv) > 3 else arg_three
        self.fileposition = {}
        self.client = None
        # current values
        self.index = ""
        self.filename = ""
        self.root = ""
        self.dirs = []
        self.connection = False

    def set_filepath(self, root, filename):
        """
            set the file position from the root, path, and file name
        Args:
            root (_str_): _path_
            filename (_str_): _file name_

        Returns:
            _str_: _full path of the file and name_
        """
        self.filename = filename
        self.root = root
        filepath = os.path.join(root, filename)
        if filepath not in self.fileposition:
            self.set_index(root, filename)
            self.fileposition[filepath] = 0
        return filepath

    def is_filepath_in_position(self, filepath):
        if self.fileposition.get(filepath) is None:
            return 

    def set_filelocator(self, filepath, pointer):
        self.fileposition[filepath] = pointer

    def set_client(self, client):
        if isinstance(Locator, client):
            self.client = client
            return
        self.client = None

    def get_filepointer(self, filepath):
        if filepath == "":
            return ""
        return self.fileposition[filepath]
   
    def set_index(self, root, index):
        try:
            if index.lower().endswith("json") or\
               index.lower().endswith("csv") or\
               index.lower().endswith("log") or\
               index.lower().endswith("gz"):
                pattern = '^[a-zA-Z0-9]+'
                # index name is based on the file naming convention
                # unknown will be all default
                name = re.match(pattern, index).group()
                if len(name) > 1 and len(name) < 9:
                    if "suricata" in root:
                        self.index = "suricata_" + name.lower()
                    elif "zeek" in root:
                        self.index = "zeek_" + name.lower()
                    else: 
                        self.index = "unknown_" + name.lower()
                    
                else:
                    self.index = "unknown"
            else:
                self.index = "invalid"          
        except AttributeError:
            self.index = "invalid"
            
    def get_index(self):
        return self.index

    def skip_file(self, root, filename):
        # custom skip for zeek or suricata
        if filename.lower().endswith(".db") or\
           filename.lower().endswith(".sh") or\
           filename.startswith("."):
            if filepath not in self.fileposition:
                filepath = os.path.join(root, filename)
                self.fileposition[filepath] = -1
            return True
        elif "zeek" in root:
              # zeek custom that skip the directory
              if root.lower().endswith("spool") or\
                 root.lower().endswith("extract_file") or\
                 root.lower().endswith("tmp") or\
                 root.lower().endswith("do-not-touch") or\
                 filename.lower().startswith("stats"):
                if filepath not in self.fileposition:
                    filepath = os.path.join(root, filename)
                    self.fileposition[filepath] = -1
                return True
        elif "suricata" in root:
            if filename.lower().startswith("stats") or\
                filename.lower().startswith("suricata") or\
                filename.lower().startswith("fast"):
                if filepath not in self.fileposition:
                    filepath = os.path.join(root, filename)
                    self.fileposition[filepath] = -1
                return True
        else:
            return False
        return False
            
def validate_args():
    '''
    Argument validation and helper
    '''
    if len(sys.argv) < 2:
        print("[USAGE] python3 horang_forwarder.py <directory> [<interval>] [<dest option>]")
        return False
    
    if sys.argv[1] == "-h" or sys.argv[1] == "help":
        print("[USAGE] python3 horang_forwarder.py <directory> [<interval>] [<dest option>]")
        print("1. <directory> is madatory")
        print(" Please define the directory to load data")
        print(" Ex. python3 horang_forwarder.py /nids")
        print("2. <Interval> is optional")
        print(" Interval 10 second is recommeded for data ingestion rate")
        print("3. <dest option> is optional, then but please add the interval")
        print(" [USAGE] python3 horang_forwarder.py <directory> 10 1")
        print(" if you choose the destination option, then the inverval is mandatory.")
        print(" Destination option, such as ELK or other SIEM")
        print(" option 1 == ELK")
        print(" ELK is default as the SIEM")
        return False
    
    if os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]):
        return True
    else:
        print(f"The directory '{sys.argv[1]}' does not exist.")
        return False