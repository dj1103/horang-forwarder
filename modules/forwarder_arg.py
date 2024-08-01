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
import sys


class Locator:
    def __init__(self):
        # <directory> is madatory
        self.dirlocator = sys.argv[1]
        # <Interval> is optional
        self.interval = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        # <dest option> is optional, then but please add the interval
        self.dest_opt = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        self.fileposition = {}
        self.client = None

    def set_filepath(self, root, filename):
        filepath = os.path.join(root, filename)
        print(filepath)
        if not validate_file_json(filepath):
            return "" 
        if filepath not in self.fileposition:
            self.fileposition[filepath] = 0        
        return filepath

    def set_filelocator(self, filepath, pointer):
        self.fileposition[filepath] = pointer

    def set_client(self, client):
        self.client = client

    def get_filepointer(self, filepath):
        return self.fileposition[filepath]


def validate_file_json(filename):
    '''
    validate if the file is a json
    '''
    # if it's a file
    if not os.path.isfile(filename):
        return False
    
    # either csv or xlsx
    if filename.lower().endswith("json"):
        return True
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