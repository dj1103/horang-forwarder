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
# Convert from CSV to JSON 
# Save as a CSV file first for encoding
# Dependency: csv, os
# Ex. print(csv_to_json("..\\test\\test.csv"))
# Author: Dave Jang as 28 July 2024


import csv
import os
import json


def validate_file_csv(filename):
    '''
    validate if the file is a CSV
    '''
    # if it's a file
    if not os.path.isfile(filename):
        return False
    
    # either csv or xlsx
    if filename.lower().endswith("csv"):
        return True

    return False


def validate_file_json(filename):
    '''
    validate if the file is a json
    '''
    # if it's a file
    if not os.path.isfile(filename):
        return False
    
    # end with JSON
    if filename.lower().endswith("json"):
        return True

    return False


def validate_json(json_str):
    """
        Validate if it's a JSON.
        It validates a specfic format.
        Ex. {"id": "1 or {'id': '1
    Args:
        json_data (unk): _JSON data_
    Returns:
        _bool_: _if it's not a json, then return false_
    """
    if isinstance(json_str, dict):
        return True
    elif not isinstance(json_str, str):
        return False

    # strip off the empty spaces for the validation
    json_str = json_str.strip()

    # common json file
    if json_str.startswith('{') and json_str.endswith('}'):
        # filter out empty object 
        if json_str == "{}":
            return False
        # json object start with { and end with }
        if json_str[0] != '{' or json_str[-1] != '}':
            return False
        # split values to validate to a list
        # {"id": "1 or {'id': '1
        if json_str[1] == '\'':
            json_list = json_str.split('\', ')
            if not json_list.pop(0).startswith('{\''):
                return False
            for keyval_pair in json_list:
                if not keyval_pair.startswith('\''):
                    return False
                if not ":" in json_str:
                    return False
        else:
            json_list = json_str.split('\", ')
            # remove first element
            if not json_list.pop(0).startswith('{\"'):
                return False
            for keyval_pair in json_list:
                if not keyval_pair.startswith('\"'):
                    return False
                if not ":" in json_str:
                    return False
        return True


def read_csv_to_json(csv_file, pointer):
    '''
    Read the CSV file only and add data to a list to load
    
    return: a list of JSON
    '''
    # return list
    ret_val = ["", pointer]
    # validate if the file is a CSV
    if validate_file_csv(csv_file) == False:
        return ret_val

    try:
        # read with UTF-8 - csv
        with open(csv_file, mode='r', encoding='utf-8-sig') as file:
            if file.seek(pointer) == os.path.getsize(csv_file):
                ret_val[1] = file.tell()
                return ret_val
            # read the csv and add to the list
            reader = csv.DictReader(file)
            ret_val[0] = [row for row in reader]
            ret_val[1] = file.tell()
    # unknown errors or unable to covert
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
    except csv.Error as err:
        print(f"Error reading CSV file '{csv_file}': {err}")
    except Exception as err:
        print(f'Unable to convert the {csv_file} file.. Error: {err}')

    return ret_val


def read_to_json(filepath, pointer):
    # return list
    ret_val = ["", pointer]
    # validate if the file is a 
    if validate_file_json(filepath) == False:
        return ret_val

    # JSON Load
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as file:
            # file load with the position
            if file.seek(pointer) == os.path.getsize(filepath):
                ret_val[1] = file.tell()
                return ret_val
            ret_val[0] = json.load(file)
            ret_val[1] = file.tell()
        return ret_val

    # unknown errors or unable to covert
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except json.JSONDecodeError as err:
        #print(f'JSON Decode Error - File Name: {filepath}.. {err}\n\
        #        Please check the file format...')
        # invalid format.. skip
        ret_val[1] = -1
    except Exception as err:
        print(f'Error: {err} - {filepath} file..')

    return ret_val


def reformat_to_json(filepath, pointer):
    """
        if load_to_json function fails, then the format needs to reload
        Fail-over function to cover the format

    Args:
        filepath (_str_): _description_
        pointer (__): _description_

    Returns:
        _type_: _description_
    """
    # return list
    data = []
    ret_val = [data, pointer]
    # validate if the file is a 
    if validate_file_json(filepath) == False:
        return ret_val
    try:
        with open(filepath) as file:
            file.seek(pointer)
            lines = file.readlines()
            for line in lines:
                data.append(json.loads(line))
        # unknown errors or unable to covert
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except json.JSONDecodeError as err:
        # invalid format.. skip
        ret_val[1] = -1
    except Exception as err:
        print(f'Error: {err} - {filepath} file..')

    return ret_val