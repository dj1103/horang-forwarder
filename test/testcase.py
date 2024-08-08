import unittest
import json


from modules.json_convert import read_csv_to_json
from modules.json_convert import read_to_json
from modules.json_convert import reformat_to_json
from modules.json_convert import read_log_to_json
from modules.json_convert import get_fields_from_tsv
from modules.json_convert import parse_tsv_to_json
from modules.json_convert import read_gz_to_json
from modules.forwarder_arg import validate_args
from modules.forwarder_arg import Locator
from horang_forwarder import load_data
from modules.json_load import load_json_to_elk


import os
import sys

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, "test"
)
sys.path.append(SOURCE_PATH)

PRINT_FLAG = False

class TestModuleMethods(unittest.TestCase):

    def test_Locator(self):
        # locator instance and path
        locator = Locator("test")
        self.assertTrue(isinstance(locator, Locator))
        self.assertEqual(locator.dirlocator, "test")


    def test_IndexNamingConversion(self):
        # index value for each JSON
        locator = Locator("test")
        self.assertTrue(isinstance(locator, Locator))
    
        # common test cases
        locator.set_index("conn.log")
        self.assertEqual(locator.get_index(), "Conn")
        locator.set_index("ntlm.log")
        self.assertEqual(locator.get_index(), "Ntlm")
        locator.set_index("known_bug.log")
        self.assertEqual(locator.get_index(), "Known")
        locator.set_index("pe.log")
        self.assertEqual(locator.get_index(), "Pe")
        locator.set_index("x509.log")
        self.assertEqual(locator.get_index(), "X509")
        locator.set_index("conn_2018_9999-111.log.gz")
        self.assertEqual(locator.get_index(), "Conn")
        locator.set_index("conn_2018_9999-111.log")
        self.assertEqual(locator.get_index(), "Conn")
        locator.set_index("netflow_data_2018.csv")
        self.assertEqual(locator.get_index(), "Netflow")
   
        # upper and lower cases
        locator.set_index("Netflow_data_2018.csv")
        self.assertEqual(locator.get_index(), "Netflow")
        locator.set_index("Netflow_DATA_2018.CSV")
        self.assertEqual(locator.get_index(), "Netflow")
        locator.set_index("CAPTURE_LOSS.LOG")
        self.assertEqual(locator.get_index(), "Capture")
   
        # unknown
        locator.set_index("s3892834dfksdofsosdfsf0ss9ds9.log")
        self.assertEqual(locator.get_index(), "Unknown")
        locator.set_index("329j239j90fsdkfa0.log")
        self.assertEqual(locator.get_index(), "Unknown")
   
        # invalid file
        locator.set_index("329j239j90fsdkfa0.exe")
        self.assertEqual(locator.get_index(), "Invalid")
        locator.set_index("ntaa.dll")
        self.assertEqual(locator.get_index(), "Invalid")
        locator.set_index("zeekctl.cfg")
        self.assertEqual(locator.get_index(), "Invalid")
        locator.set_index("broctl")
        self.assertEqual(locator.get_index(), "Invalid")

        if PRINT_FLAG == True:
            print("\n############# 1) INDEX NAMING CONVERSION TEST SUCCESS! ################")
            locator.set_index("conn.log")
            print("INDEX NAME OF CONN.LOG: ", locator.get_index())


    def test_from_log_to_json(self):
        
        ret = ['ts', 'uid', 'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto', 'service']
        locator = Locator('test')
        json_file = locator.set_filepath(SOURCE_PATH, "test5.log")
        self.assertEqual(get_fields_from_tsv(json_file), ret)
        # for future..
        # read log to json
        json_file = "test4.log"
        pointer = 0
        # json_ret_val = read_log_to_json(json_file, pointer)
        # compare
        lines = ["1.1.1.1\t53\t2.2.2.2\t1111", \
                 "1.2.1.1\t53\t2.2.2.2\t2222", \
                 "1.1.3.1\t53\t2.2.2.2\t3333", \
                 "1.1.1.4\t53\t2.2.2.2\t4444"]
        tsv_fields = ["id.orig_h","id.orig_p","id.resp_h", "id.resp_p"]
        data = parse_tsv_to_json(lines, tsv_fields, pointer)
        compare = [[{'id.orig_h': '1.1.1.1', 'id.orig_p': '53', \
                     'id.resp_h': '2.2.2.2', 'id.resp_p': '1111'}, \
                    {'id.orig_h': '1.2.1.1', 'id.orig_p': '53', \
                     'id.resp_h': '2.2.2.2', 'id.resp_p': '2222'}, 
                    {'id.orig_h': '1.1.3.1', 'id.orig_p': '53', \
                     'id.resp_h': '2.2.2.2', 'id.resp_p': '3333'}, \
                    {'id.orig_h': '1.1.1.4', 'id.orig_p': '53', \
                     'id.resp_h': '2.2.2.2', 'id.resp_p': '4444'}], 92]
        self.assertEqual(data, compare)
        # missing data
        lines = ["1.1.1.1\t53\t2.2.2.2\t1111", \
                 "1.2.1.1\t53\t2.2.2.2\t2222", \
                 "1.1.3.1\t53\t2.2.2.2\t3333", \
                 "1.1.1.4\t53\t\t4444"]
        tsv_fields = ["id.orig_h","id.orig_p","id.resp_h", "id.resp_p"]
        pointer = 0
        data = parse_tsv_to_json(lines, tsv_fields, pointer)
        for ele in data[0]:
            self.assertTrue(isinstance(ele, dict))
        if PRINT_FLAG == True:
            print("\n############# 2) TSV PARSING TEST SUCCESS! ################")
            for idx, ele in enumerate(data[0]):
                if idx == 2:
                    break
                print(ele)
        # text log with JSONs
        pointer = 0
        json_file = 'test4.log'
        data = read_log_to_json(json_file, pointer)
        for ele in data[0]:
            self.assertTrue(isinstance(ele, dict))
        if PRINT_FLAG == True:
            print("\n############# 3) TEXT JSON TEST SUCCESS! ################")
            #print(ele)


    def test_to_json(self):
        # JSON formats testing
        # Test case 1
        locator = Locator("test")
        json_file = locator.set_filepath(SOURCE_PATH, "test.json")
        pointer = 0
        json_ret_val = read_to_json(json_file, pointer)
        self.assertTrue(isinstance(json_ret_val[0], list))
        self.assertNotEqual(json_ret_val[1], 0)

        # Test case 2
        json_file = locator.set_filepath(SOURCE_PATH, "test1.json")
        pointer = 0
        json_ret_val2 = read_to_json(json_file, pointer)
        self.assertTrue(isinstance(json_ret_val2[0], dict))
        self.assertNotEqual(json_ret_val2[1], 0)
    
        # Test case 3
        json_file = locator.set_filepath(SOURCE_PATH, "test2.ndjson")
        pointer = 0
        json_ret_val3 = read_to_json(json_file, pointer)
  
        if (json_ret_val3[1] == -1):
            # try again..
            json_ret_val3 = reformat_to_json(json_file, pointer)
            self.assertTrue(isinstance(json_ret_val3[0], list))
            self.assertTrue(isinstance(json_ret_val3[0][0], dict))
        
        # Test case 4
        json_file = locator.set_filepath(SOURCE_PATH, "test3.json")
        pointer = 0
        json_ret_val4 = read_to_json(json_file, pointer)
        self.assertTrue(isinstance(json_ret_val4[0], list))


    def test_load_data(self):
        # load data validation

        locator = Locator("test")
        json_file = locator.set_filepath(SOURCE_PATH, "test3.json")
        pointer = 0
        json_ret_val5 = load_data(json_file, pointer)
        self.assertTrue(isinstance(json_ret_val5[0], list))
     
        for ele in json_ret_val5[0]:
            self.assertTrue(isinstance(ele, dict))

        if PRINT_FLAG == True:      
            print("\n############# 4) JSON FILE TEST SUCCESS! ################")
   
        for idx, ele in enumerate(json_ret_val5[0]):
            if idx == 3:
                break
            self.assertTrue(isinstance(ele, dict))
            if PRINT_FLAG == True:
                print(ele)
                

        # line items - text format
        json_file = locator.set_filepath(SOURCE_PATH, "test2.ndjson")
        pointer = 0   
        json_ret_val6 = load_data(json_file, pointer)
        self.assertTrue(isinstance(json_ret_val6[0], list))
   
        for ele in json_ret_val6[0]:
            self.assertTrue(isinstance(ele, dict))
        if PRINT_FLAG == True:        
            print("\n############# 5) JSON TEXT TEST SUCCESS! ################")
        
            for idx, ele in enumerate(json_ret_val6[0]):
                if idx == 2:
                    break
                print(ele)
        # line items - CSV
        csv_file = locator.set_filepath(SOURCE_PATH, "test.csv")
        pointer = 0
        json_ret_val7 = load_data(csv_file, pointer)
        self.assertTrue(isinstance(json_ret_val7[0], list))
       
        for ele in json_ret_val7[0]:
            self.assertTrue(isinstance(ele, dict))
        
        if PRINT_FLAG == True:        
            print("\n############# 6) CSV FILE TEST SUCCESS! ################")
        
            for idx, ele in enumerate(json_ret_val7[0]):
                if idx == 3:
                    break
                print(ele)


    def test_multiple_loads(self):
        # attempt to read and load multiple times - stress testing
        # index value for each JSON
        locator = Locator("test")
        self.assertTrue(isinstance(locator, Locator))
        # line items - CSV
        csv_file = locator.set_filepath(SOURCE_PATH, "test.csv")
        pointer = 0
        json_ret_val = load_data(csv_file, pointer)
        assert json_ret_val[0]
        locator.set_filelocator(csv_file, json_ret_val[1])
        self.assertNotEqual(json_ret_val[1], 0)
        self.assertEqual(str(json_ret_val[0][0]), \
                         "{'id': '1', 'details': '1001abc', 'pages': '12'}")
        
        for idx in range(0, 3):
            json_ret_val = load_data(csv_file, 
                                     locator.fileposition[csv_file])
            self.assertNotEqual(locator.fileposition[csv_file], 0)
            self.assertEqual(json_ret_val[0], [])
            self.assertEqual(json_ret_val[1], locator.fileposition[csv_file])
        
        if PRINT_FLAG == True:        
            print("\n############# 7) MULTI ATTEMPT (CSV) TEST SUCCESS! ################")
            print("File count: ", locator.fileposition[csv_file])

        # line items - JSON
        json_file = locator.set_filepath(SOURCE_PATH, "test.json")
        pointer = 0
        json_ret_val = load_data(json_file, pointer)
        locator.set_filelocator(json_file, json_ret_val[1])
        self.assertNotEqual(json_ret_val[1], 0)
        self.assertEqual(str(json_ret_val[0][0]), \
                         "{'id': '1', 'details': '1001abc', 'pages': '12'}")
        
        for idx in range(0, 3):
            json_ret_val = load_data(json_file, 
                                     locator.fileposition[json_file])
            self.assertNotEqual(locator.fileposition[json_file], 0)
            self.assertEqual(json_ret_val[0], [])
            self.assertEqual(json_ret_val[1], locator.fileposition[json_file])
        
        if PRINT_FLAG == True:            
            print("\n############# 8) MULTI ATTEMPT (JSON) TEST SUCCESS! ################")
            print("File count: ", locator.fileposition[json_file], "\n")

        # JSON LOG TEXT - read_log_to_json
        json_file1 = locator.set_filepath(SOURCE_PATH, "test4.log")
        pointer = 0
        json_ret_val = load_data(json_file1, pointer)
        assert json_ret_val[0]
        locator.set_filelocator(json_file1, json_ret_val[1])
        self.assertNotEqual(json_ret_val[1], 0)       
        
        for idx in range(0, 3):
            json_ret_val = load_data(json_file1, 
                                     locator.fileposition[json_file1])
            self.assertNotEqual(locator.fileposition[json_file1], 0)
            self.assertEqual(json_ret_val[0], [])

        if PRINT_FLAG == True:        
            print("\n############# 9) MULTI ATTEMPT (JSON TEXT) TEST SUCCESS! ################")
            print("File count: ", locator.fileposition[json_file1], "\n")

        # TSV Testing
        json_file5 = locator.set_filepath(SOURCE_PATH, "test5.log")
        pointer = 0
        json_ret_val = load_data(json_file5, pointer)
        assert json_ret_val[0]
        locator.set_filelocator(json_file5, json_ret_val[1])
        self.assertNotEqual(json_ret_val[1], 0)       
        
        for idx in range(0, 3):
            json_ret_val = load_data(json_file5, 
                                     locator.fileposition[json_file5])    
            self.assertNotEqual(locator.fileposition[json_file5], 0)
            self.assertEqual(json_ret_val[0], [])
        
        if PRINT_FLAG == True:        
            print("\n############# 10) MULTI ATTEMPT (TSV) TEST SUCCESS! ################")
            print("File count: ", locator.fileposition[json_file5], "\n")


    def test_csv_to_json(self):
        # CSV file to JSON conversion
        csv_file = "test.csv"
        pointer = 0
        csv_ret_val = read_csv_to_json(csv_file, pointer)
        # file to JSON conversion
        json_file = "test.json"
        pointer = 0
        json_ret_val = read_to_json(json_file, pointer)
        self.assertEqual(csv_ret_val[0], json_ret_val[0])


if __name__ == '__main__':
    unittest.main()
