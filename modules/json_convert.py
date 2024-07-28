import csv
import json
import os

'''
Convert from CSV to JSON 

Save as a CSV file first for encoding

Dependency: csv, os

Ex. print(csv_to_json("..\\test\\test.csv"))

Author: Dave Jang as 28 July 2024

'''

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
    
    # neither csv or xlsx, then the file is invalid 
    print(f"Error: '{filename}' is not a CSV valid file.")    
    return False


def csv_to_json(csv_file):
    '''
    Read the CSV file only and add data to a list to load
    
    return: a list of JSON
    '''
    # return list
    data = []

    # validate if the file is a CSV
    if validate_file_csv(csv_file) == False:
        return data

    try:
        # read with UTF-8 - csv
        with open(csv_file, mode='r', encoding='utf-8-sig') as cf:
            # read the csv and add to the list
            reader = csv.DictReader(cf)
            data = [row for row in reader]

    # unknown errors or unable to covert
    except Exception as ex:
        print(f'Unable to convert the file.. Error: {ex}')

    return data
