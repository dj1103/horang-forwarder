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
# Validate the JSON, and a function to connect to Elasticsearch.
# No Service account token or bearer tokens option
# Author: Dave Jang as 28 July 2024
# If codes relate to Elasticsearch, please see the Elasticsearch API license below.
# https://elasticsearch-py.readthedocs.io/en/latest/
# Copyright 2023 Elasticsearch B.V. Licensed under the Apache License, Version 2.0.
# Driver Code: print(validate_json("{\"id\": \"1\", \"details\": \"1001abc\", \"pages\": \"12\"}"))


from elasticsearch import Elasticsearch as elk_db
import os

def validate_json(json_str):
    """
        Validate if it's a JSON.
        It validates a specfic format.
        Ex. {"id": "1 or {'id': '1

    Args:
        json_str (str): _JSON string_

    Returns:
        _bool_: _if it's not a json, then return false_
    """
    # string is required
    if not isinstance(json_str, str):
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


def connect_elk_db():
    """
        connect to Elasticsearch to load JSON
    
    Returns:
        _obj_: if it's none, then no connection is established
    """
    ret_val = None
    # HTTPS or HTTP
    option = input("Please choose the option to connect the Elastic DB:\n\
                   1: non-secure mode - HTTP (non-production or testing)\n\
                   2: secure mode - HTTPS and authentication (production)")
    # ip and port holders
    ip = input("Please provide the IP address of the DB - default:localhost")
    if ip == "":
        ip = "localhost"
    port = input("Please provide the port number of the DB - default:9200")
    if port == "":
        port = "9200"

    # either secure or non-secure modes
    if option == "1":
        # non-secure mode - testing and non-production
        # secure mode only uses either username and password
        # clear traffic
        http_connect = f'http://{ip}:{port}' 
        ret_val = elk_db([http_connect])

    elif option == "2":
        # secure mode
        https_connect = f'https://{ip}:{port}'
        option = input("Please choose the option to connect the Elastic DB:\n\
                        1: Basic Authentication - Username and Password\n\
                        2: API Authentication - API Key")
        ca_path = input("Please provide the CA path - HTTPS certification\n\
                         Ex. the root CA certificate can be found in certs/https_ca.crt")
        # default path
        if ca_path == "":
            ca_path = "$ES_CONF_PATH/certs/http_ca.crt"

        # authentication methods 
        if option == "1":
            # basic authentication
            http_connect = f'http://{ip}:{port}'
            user = "Please provide the user name of the DB"
            password = "Please provide the password of the user"
            ret_val = elk_db(
                [https_connect], 
                ca_path, 
                basic_auth=(user, password))
        elif option == "2":
            # API authentication
            api_key = input("Please provide the API key - Ex. Kibana Stack Management\
                             or Elastic API Key")
            ret_val = elk_db(
                [https_connect], 
                ca_path,
                api_key)
        else:
            # no option - authentication
            return ret_val
    else:
        # no option - HTTP/HTTPS
        return ret_val

    # succssful response - ret_val.info()

    return ret_val


def load_json(client=None, json_val=[], index_name="default"):
    """
        load json string or list to Elk DB

    Args:
        client (_obj_): Elasticsearch instance
        json_val (_str or list_): _load the JSON to Elk DB_
        index_name (_str_): index name

    """
    if client == None:
        print("No connection to the SIEM...... Please press ctrl-c")
        return

    # string ops
    if isinstance(json_val, str):
        if validate_json(json_val):
            client.index(index=index_name,\
                            document=json_val)
    # list ops
    elif isinstance(json_val, list):
        for json_str in json_val:
            if validate_json(json_str):
                client.index(index=index_name,\
                             document=json_val)
    # invalid type
    else:
        return
    
    return
