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
#

import os
import time
import sys
import json
from modules.json_load import connect_elk_db

## horangi forwarder ##

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
        print(" if you choose the destination option, then the inverval is mandatory.")
        print(" Destination option, such as ELK or other SIEM")
        print(" ELK is default as the SIEM")
        return False
    
    if os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]):
        return True
    else:
        print(f"The directory '{sys.argv[1]}' does not exist.")
        return False


def load_appended_data(filepath, pointer):
    '''
    Load appended data from the pointer position
    '''
    try:
        with open(filepath, 'r') as file:
            # file load with the position
            file.seek(pointer)
            data = file.readlines()
            newpointer = file.tell()
        print(f'loaded data....{data}')
        return data, newpointer
    except Exception as e:
        print(f"Error loading data from {filepath}: {e}")
    print(f"Unknown Error..")
    sys.exit()


def monitor_directory(dirlocator, interval):
    '''
    os walk to check all files from sub directories
    '''
    print("[Note] Please do not run the forwarder on the same folder multiple times!")
    print("[Note] It will load duplicated data if you do.")
    filepositions = {}
    while True:
        # Get the list of subfolders and files in the base directory
        for root, dirs, files in os.walk(dirlocator):
            for file in files:
                filepath = os.path.join(root, file)
                # initial position to load the file
                if filepath not in filepositions:
                    filepositions[filepath] = 0 
                curpointer = filepositions[filepath]
                data, newpointer = load_appended_data(filepath, curpointer)
                # Add your processing code here
                # temp for forward the data to ELK
                filepositions[filepath] = newpointer
        time.sleep(interval)


def main():
    '''
    log forwader main
    '''
    try:
        dirlocator = sys.argv[1]
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        dest_opt = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        # option 1 is ELK
        if dest_opt == 1:
            connect_elk_db()
            monitor_directory(dirlocator, interval)
        # other options for future
        else:
            print("Under development for integration..")
            print("Please contact us if you need more integration to other SIEMs")
    except KeyboardInterrupt:
        print("closing out...")
        sys.exit()

if __name__ == "__main__":
    # validate the arguments
    if validate_args() == False:
        sys.exit(1)
    main()
