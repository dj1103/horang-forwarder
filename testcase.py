import unittest
import json


from modules.json_convert import validate_json
from modules.json_convert import read_csv_to_json
from modules.json_convert import read_to_json
from modules.json_convert import reformat_to_json
from modules.forwarder_arg import validate_args
from modules.forwarder_arg import Locator
from horang_forwarder import load_data
from modules.json_load import load_json_to_elk

class TestModuleMethods(unittest.TestCase):

    def test_Locator(self):
        # locator instance and path
        locator = Locator("test")
        self.assertTrue(isinstance(locator, Locator))
        self.assertEqual(locator.dirlocator, "test")
        path = locator.set_filepath("test", "test.json")
        self.assertEqual(path, "test\\test.json")


    def test_IndexNamingConversion(self):
        # index value for each JSON
        locator = Locator("test")
        self.assertTrue(isinstance(locator, Locator))
    
        # common test cases
        locator.set_index("conn.log")
        self.assertEqual(locator.get_index(), "conn_index")
        locator.set_index("ntlm.log")
        self.assertEqual(locator.get_index(), "ntlm_index")
        locator.set_index("known_bug.log")
        self.assertEqual(locator.get_index(), "known_index")
        locator.set_index("pe.log")
        self.assertEqual(locator.get_index(), "pe_index")
        locator.set_index("x509.log")
        self.assertEqual(locator.get_index(), "x509_index")
        locator.set_index("conn_2018_9999-111.log.gz")
        self.assertEqual(locator.get_index(), "conn_index")
        locator.set_index("conn_2018_9999-111.log")
        self.assertEqual(locator.get_index(), "conn_index")
        locator.set_index("netflow_data_2018.csv")
        self.assertEqual(locator.get_index(), "netflow_index")
   
        # upper and lower cases
        locator.set_index("Netflow_data_2018.csv")
        self.assertEqual(locator.get_index(), "netflow_index")
        locator.set_index("Netflow_DATA_2018.CSV")
        self.assertEqual(locator.get_index(), "netflow_index")
        locator.set_index("CAPTURE_LOSS.LOG")
        self.assertEqual(locator.get_index(), "capture_index")
   
        # unknown
        locator.set_index("s3892834dfksdofsosdfsf0ss9ds9.log")
        self.assertEqual(locator.get_index(), "unknown_index")
        locator.set_index("329j239j90fsdkfa0.log")
        self.assertEqual(locator.get_index(), "unknown_index")
   
        # invalid file
        locator.set_index("329j239j90fsdkfa0.exe")
        self.assertEqual(locator.get_index(), "invalid_index")
        locator.set_index("ntaa.dll")
        self.assertEqual(locator.get_index(), "invalid_index")
        locator.set_index("zeekctl.cfg")
        self.assertEqual(locator.get_index(), "invalid_index")
        locator.set_index("broctl")
        self.assertEqual(locator.get_index(), "invalid_index")


    def test_to_json(self):
        # basic JSON formats
        json_file = "test\\test.json"
        pointer = 0
        json_ret_val = read_to_json(json_file, pointer)
        self.assertTrue(isinstance(json_ret_val[0], list))
        self.assertNotEqual(json_ret_val[1], 0)
        json_file = "test\\test1.json"
        json_ret_val2 = read_to_json(json_file, pointer)
        self.assertTrue(isinstance(json_ret_val2[0], dict))
        self.assertNotEqual(json_ret_val2[1], 0)
        self.assertTrue(validate_json(json_ret_val2[0]))
    
        # different types
        json_file = "test\\test2.ndjson"
        json_ret_val3 = read_to_json(json_file, pointer)
  
        if (json_ret_val3[1] == -1):
            # try again..
            json_ret_val3 = reformat_to_json(json_file, pointer)
            self.assertTrue(isinstance(json_ret_val3[0], list))
            self.assertTrue(isinstance(json_ret_val3[0][0], dict))
        json_file = "test\\test3.json"
        json_ret_val4 = read_to_json(json_file, pointer)
        self.assertTrue(isinstance(json_ret_val4[0], list))


    def test_load_data(self):
        # load data validation
        json_file = "test\\test3.json"
        pointer = 0
        json_ret_val5 = load_data(json_file, pointer)
        self.assertTrue(isinstance(json_ret_val5[0], list))
     
        for ele in json_ret_val5[0]:
            self.assertTrue(isinstance(ele, dict))
      
        print("\n############# 1) JSON FILE TEST SUCCESS! ################")
   
        for idx, ele in enumerate(json_ret_val5[0]):
            if idx == 3:
                break
            print(ele)
            self.assertTrue(isinstance(ele, dict))

        # line items - text format
        json_file = "test\\test2.ndjson"
        pointer = 0      
        json_ret_val6 = load_data(json_file, pointer)
        self.assertTrue(isinstance(json_ret_val6[0], list))
   
        for ele in json_ret_val6[0]:
            self.assertTrue(isinstance(ele, dict))
        print("\n############# 2) JSON TEXT TEST SUCCESS! ################")
      
        for idx, ele in enumerate(json_ret_val6[0]):
            if idx == 2:
                break
            print(ele)
        # line items - CSV
        csv_file = "test\\test.csv"
        pointer = 0      
        json_ret_val7 = load_data(csv_file, pointer)
        self.assertTrue(isinstance(json_ret_val7[0], list))
       
        for ele in json_ret_val7[0]:
            self.assertTrue(isinstance(ele, dict))
        print("\n############# 3) CSV FILE TEST SUCCESS! ################")
      
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
        csv_file = "test\\test.csv"
        pointer = 0
        json_ret_val = load_data(csv_file, pointer)
        locator.set_filelocator(csv_file, json_ret_val[1])
        self.assertNotEqual(json_ret_val[1], 0)
        self.assertEqual(str(json_ret_val[0][0]), \
                         "{'id': '1', 'details': '1001abc', 'pages': '12'}")
        
        for idx in range(0, 3):
            json_ret_val = load_data(csv_file, 
                                     locator.fileposition[csv_file])
            self.assertEqual(csv_file, "test\\test.csv")
            self.assertNotEqual(locator.fileposition[csv_file], 0)
            self.assertEqual(csv_file, "test\\test.csv")
            self.assertEqual(json_ret_val[0], '')
            self.assertEqual(json_ret_val[1], locator.fileposition[csv_file])
        print("\n############# 4) MULTI ATTEMPT (CSV) TEST SUCCESS! ################")
        print("File count: ", locator.fileposition[csv_file])

        # line items - JSON
        json_file = "test\\test.json"
        pointer = 0
        json_ret_val = load_data(json_file, pointer)
        locator.set_filelocator(json_file, json_ret_val[1])
        self.assertNotEqual(json_ret_val[1], 0)
        self.assertEqual(str(json_ret_val[0][0]), \
                         "{'id': '1', 'details': '1001abc', 'pages': '12'}")
        
        for idx in range(0, 3):
            json_ret_val = load_data(json_file, 
                                     locator.fileposition[json_file])
            self.assertEqual(json_file, "test\\test.json")
            self.assertNotEqual(locator.fileposition[json_file], 0)
            self.assertEqual(json_file, "test\\test.json")
            self.assertEqual(json_ret_val[0], '')
            self.assertEqual(json_ret_val[1], locator.fileposition[json_file])
        print("\n############# 5) MULTI ATTEMPT (JSON) TEST SUCCESS! ################")
        print("File count: ", locator.fileposition[json_file])


    def test_csv_to_json(self):
        # CSV file to JSON conversion
        csv_file = "test\\test.csv"
        pointer = 0
        csv_ret_val = read_csv_to_json(csv_file, pointer)
        # file to JSON conversion
        json_file = "test\\test.json"
        pointer = 0
        json_ret_val = read_to_json(json_file, pointer)
        self.assertEqual(csv_ret_val[0], json_ret_val[0])



if __name__ == '__main__':
    unittest.main()
