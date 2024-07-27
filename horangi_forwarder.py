import os
import time
import sys
import json

## horangi forwarder ##

def validate_args():
    '''
    Argument validation and helper
    '''
    if len(sys.argv) < 2:
        print("[USAGE] python3 logforwarder.py <directory> [<interval>]")
        return False
    
    if sys.argv[1] == "-h" or sys.argv[1] == "help":
        print("[USAGE] python3 logforwarder.py <directory> [<interval>]")
        print("[USAGE] please define the directory to load data")
        print("[USAGE] Interval is optional")
        print("[USAGE] Interval 10 second is recommeded for data ingestion rate")
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
        monitor_directory(dirlocator, interval)
    except KeyboardInterrupt:
        print("closing out...")
        sys.exit()

if __name__ == "__main__":
    # validate the arguments
    if validate_args() == False:
        sys.exit(1)
    main()
