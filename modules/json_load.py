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
import time
import getpass
import gc


def get_ipport_from_input():
    # ip and port holders
    ip = input("Please provide the IP address of the Elastic DB or press enter to use \"localhost\"\n\
                   Ex. 127.0.0.1\n : ")
    if ip == "":
        ip = "localhost"
    port = input("Please provide the port number of the Elastic DB or press enter to use default port number\n\
                    Ex. 9200\n : ")
    if port == "":
        port = "9200"

    return [ip, port]


def connect_elk_db():
    """
        connect to Elasticsearch to load JSON
    
    Returns:
        _obj_: if it's none, then no connection is established
    """
    client = None
    # connection time out set as 3 seconds
    connection_time_out = 3

    try:
        # HTTPS or HTTP
        option = input("Please choose the option to connect the Elastic DB\n\
                   1: non-secure mode - HTTP (non-production or testing)\n\
                   2: secure mode - HTTPS and authentication (production)\n\
                   Ex. 1\n : ")
        # either secure or non-secure modes
        if option == "1":
            ip, port = get_ipport_from_input()
            # non-secure mode [clear traffic] - testing and non-production
            # secure mode only uses either username and password
            http_connect = f'http://{ip}:{port}'
            client = elk_db(http_connect,
                            request_timeout=connection_time_out)
        elif option == "2":
            ip, port = get_ipport_from_input()
            # secure mode
            https_connect = f'https://{ip}:{port}'
            
            option = input("Please choose the option to connect the Elastic DB:\n\
                            1: Basic Authentication - Username and Password\n\
                            2: API Authentication - API Key\n : ")
            ca_path = input("Please provide the CA path - HTTPS certification\n\
                            Ex. the root CA certificate can be found in certs/https_ca.crt\n : ")
            # default path
            if ca_path == "":
                ca_path = "$ES_CONF_PATH/certs/http_ca.crt"

            # authentication methods 
            if option == "1":
                user = input("Please provide the user name of the DB\n : ")
                passwd = getpass.getpass("Please provide the password of the user\n : ")
                client = elk_db(https_connect, 
                                ca_certs=ca_path, 
                                basic_auth=(user, passwd),
                                request_timeout=connection_time_out)
                # flush the passwd and delete the variable from the enviroment
                del passwd
                del user
            elif option == "2":
                # API authentication
                api_key_val = getpass.getpass("Please provide the API key - Ex. Kibana Stack Management\n\
                                              or Elastic API Key\n : ")
                client = elk_db(
                    https_connect, 
                    ca_certs=ca_path,
                    api_key= api_key_val,
                    request_timeout=connection_time_out)
                # flush the API Key and delete the variable from the enviroment
                del api_key_val
            else:
                # no option - authentication
                return client
        else:
            return None
        # connecting to the DB..
        print(f'Connecting to {ip}..... Please wait...', \
              flush=True)
        client.info()
        return client
    except Exception as err:
        print(f'\nUnable to connect to the ELK DB (http://{ip}:{port})\n{err}', \
                flush=True)
        return None
    
    finally:
        # Explicitly Releasing Memory - garbage collection cycle 
        gc.collect()    


def load_json_to_elk(locator=None, json_val=[]):
    """
        load json string or a list of JSONs to Elk DB

    Args:
        locator (_Locator_): Locator instance
        json_val (JSON or _str or list_): _load the JSON to Elk DB_

        if the dict or list has strings, then it converts strings 
        to JSON to the Elasticsearch server.
    """
    if locator == None or locator.client == None:
        print("No connection to the SIEM...... Please press ctrl-c")
        return False

    # one index
    if isinstance(json_val, dict):
        # Elastic REST API
        locator.client.index(index=locator.get_index(),\
                             document=json_val)
    # multiple indexes
    elif isinstance(json_val, list):
        # Elastic REST API
        for idx, json_str in enumerate(json_val):
            # pause per 1000 indexes at the time
            if idx % 500 == 0:
                time.sleep(locator.interval)
            locator.client.index(index=locator.get_index(),\
                                 document=json_str)
    # invalid type
    else:
        return False
    
    return True
