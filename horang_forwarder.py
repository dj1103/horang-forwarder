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
from modules.json_convert import validate_file_csv
from modules.json_convert import validate_file_json
from modules.json_convert import read_csv_to_json
from modules.json_convert import read_to_json
from modules.json_convert import reformat_to_json
from modules.json_load import connect_elk_db
from modules.json_load import load_json_to_elk
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
        _a list with data and pointer_ (_list_): _returns JSON data list and pointer_
    """
    ret_val = ["", pointer]
    if validate_file_json(filepath):
        ret_val = read_to_json(filepath, pointer)
        # fail over reformatting JSON files
        if ret_val[1] == -1:
            # pointer reset
            return reformat_to_json(filepath, pointer)
        return ret_val
    elif validate_file_csv(filepath):
        return read_csv_to_json(filepath, pointer)
    else:
        return ret_val


def monitor_directory(locator=None):
    '''
    os walk to check all files from sub directories to load JSONs to a SIEM
    multi-threading using _thread
    '''
    if not isinstance(locator, Locator):
        return

    try:
        # in order to check the directories and files periodically with the interval (default: 10 second)
        while True:
            # Get the list of subfolders and files in the base directory
            for root, dirs, files in os.walk(locator.dirlocator):
                # for loop to iterate each file
                for file in files:
                    filepath = locator.set_filepath(root, file)
                    # format error skip
                    if locator.get_filepointer(filepath) == -1:
                       continue
                    else:
                        # initial position to load the file
                        data, pointer = load_data(filepath, 
                                                  locator.get_filepointer(filepath))
                        # Notthing to load or flag to skip
                    if pointer == -1 or data == "":
                        # format Error then fail-over re-attempt
                        if pointer == -1:
                            # ignore the file..
                            locator.set_filelocator(filepath, pointer)
                            # break for invalid format mapping to pass the next time
                            time.sleep(locator.interval)
                        continue

                    ######################################################################
                    # Successfully loaded data as JSON, then load the JSON/s to the SIEM #
                    # possibly add threating for future                                  #
                    ###################################################################### 
                    ret = load_json_to_elk(locator.client, data)
                    # if succefully loaded
                    if ret == True:
                        locator.set_filelocator(filepath, pointer)
                    else:
                        print(f'Unable to load the JSON file \"{locator.filename}\" now...')
                        time.sleep(locator.interval)
            time.sleep(locator.interval)
    except Exception as err:
        print(f'Closing out... due to {err}')
        sys.exit(1)


def main():
    '''
    log forwader main
    '''
    try:
        locator = Locator()
        # option 1 is ELK
        if locator.dest_opt == "1":
            #locator.client = connect_elk_db()
            if locator.client == None:
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
