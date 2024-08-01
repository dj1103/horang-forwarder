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
from modules.json_load import load_json
from modules.json_load import validate_file_json
from modules.forwarder_arg import validate_args
from modules.forwarder_arg import Locator


## horang forwarder ##


def load_data(filepath, pointer):
    """
    Load data from the pointer position
    if it's a CSV, then convert it to JSON

    Args:
        filepath (_str_): _full path and name - file name and path_
        pointer (_int_): _file line locator_

    Returns:
        _a list with data and pointer_ (_list_): _returns JSON str data and pointer_
    """
    ret_val = ["", pointer]
    if not validate_file_json(filepath):
        return ret_val
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as file:
            # file load with the position
            file.seek(pointer)
            data = json.load(file)
            newpointer = file.tell()
        return [data, newpointer]
    except Exception as e:
        print(f"Error loading data from {filepath}: {e}")
    return ret_val


def monitor_directory(locator=None):
    '''
    os walk to check all files from sub directories to load JSONs to a SIEM
    multi-threading using _thread
    '''
    if locator == None or not isinstance(locator, Locator):
        return

    try:
        # in order to check the directories and files periodically with the interval (default: 10 second)
        while True:
            # Get the list of subfolders and files in the base directory
            for root, dirs, files in os.walk(locator.dirlocator):
                # for loop to iterate each file
                for file in files:
                    filepath = locator.set_filepath(root, file)
                    # not JSON
                    if filepath == "":
                        print(f'{filepath} is NOT a JSON.. moving to the next file..')
                        continue
                    # initial position to load the file
                    data, newpointer = load_data(filepath, 
                                                 locator.get_filepointer(filepath))
                    # load json
                    ret = load_json(locator.client, data) # _thread.start_new_thread(load_json, (client, list_data[0]))
                    
                    # if succefully loaded
                    if ret == True:
                        # pointer assignment
                        locator.set_filelocator(filepath, newpointer)
            time.sleep(locator.interval)
    except KeyboardInterrupt:
        print("closing out...")
        sys.exit()
    return

def main():
    '''
    log forwader main
    '''
    try:
        locator = Locator()
        # option 1 is ELK
        if locator.dest_opt == 1:
            client = connect_elk_db()
            if client != None:
                monitor_directory(locator)
        # other options for future
        else:
            print("Under development for integration..")
            print("Please contact us if you need more integration to other SIEMs")
    except KeyboardInterrupt:
        print("Closing out...")
        sys.exit()
    return


if __name__ == "__main__":
    # validate the arguments
    if validate_args() == False:
        sys.exit(1)
    main()
