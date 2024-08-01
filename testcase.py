import unittest
import re


from modules.json_convert import validate_json
from modules.json_convert import read_csv_to_json
from modules.json_convert import read_to_json
from modules.json_load import load_json_to_elk
from modules.forwarder_arg import validate_args
from modules.forwarder_arg import Locator

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
        json_file = "test\\test.json"
        pointer = 0
        json_ret_val = read_to_json(json_file, pointer)
        self.assertTrue(isinstance(json_ret_val[0], list))
        self.assertEqual(json_ret_val[1], 18393)
        json_file = "test\\test1.json"
        pointer = 0
        json_ret_val2 = read_to_json(json_file, pointer)
        self.assertTrue(isinstance(json_ret_val2[0], dict))
        self.assertEqual(json_ret_val2[1], 65)
        self.assertTrue(validate_json(json_ret_val2[0]))


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
