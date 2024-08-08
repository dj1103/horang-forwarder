# Horang-Forwarder


## Description

This Horang forwarder is a log forwarder using Python language that inspects multiple subdirectories within a designated leading directory for files. The script will routinely load files and append data to a user-defined database or SIEM. This script is designed to support users in automatically loading data to their SIEMs, forwarding the logs to the next node, or enriching the data with other sources.


     Currently, the script supports TSV, CSV, and various types of JSON, 
     enabling the conversion of these formats into a list of JSONs (dictionary) or a singular JSON.
     
     Multiple unit tests have been carried out, and as of now, no issues have been identified. 
     
     Please do not hesitate to reach out if you encounter any problems. Thank you.

     
## Usage

     [USAGE] python3 horang_forwarder.py <directory> [<interval>] [<dest option>]")
          1. <directory> is madatory. Please define the directory to load data 
               Ex. python3 horang_forwarder.py /nids
          2. <Interval> is optional. A 10-second Interval is recommended for the data ingestion rate. 
               Ex. python3 horang_forwarder.py <directory> 10
          3. <dest option> is optional. However, if you choose the destination option, then the interval is mandatory.")
               Ex. python3 horang_forwarder.py /nids/zeek 10 1
                     Destination option:
                         Elastic API : 1
                         Only Elastic API using Python is currently available.
                         It is currently under development for other platforms.
               
     A designated main directory is the folder with multiple subdirectories and files.
     The interval is optional. An interval of 10 seconds is by default for the data ingestion rate.

         python3 logforwarder.py <directory> [<interval>]
         Ex. python3 horang_forwarder.py /nsm/zeek/
         Ex. python3 horang_forwarder.py c:\users\myaccount\Desktop\zeek\


## Continous Integration and Continuos Development (CI/CD Pipeline)  

     You can check the status of the repo with the "Actions" tap or CI/CD pipeline.


## Unit Test

     python -m unittest


## Version

     Testing with Python 3.12, published on 2023-10-02, expires on 2028-10, PEP 693
          https://www.python.org/downloads/


## Dependency

     [required] apt install python3 or download the bianry    # python 3.10 or above
     [optional] python3 -m pip install        # different SIEM API libaries
     [optional] pip install elasticsearch     # if you wish to use APIs to post data
             or python -m pip install elasticsearch
            API Key Management from Elastic
            https://www.elastic.co/guide/en/kibana/current/api-keys.html


## Future

1. File validation and Data normalization

        1. remove garbage data
        2. compressed file (ex. gz) unzip to JSON
        3. filter out or skip non-loadable data (ex. exe)
        4. [optional] field normalization - (ex. id.resp_h to dest_ip and ips)

2. Data Enrichment

        1. Maxmind DB - ASN and GeoIP
        2. DHCP Host name adding to conn.log
        3. MAC OUI Lookup (Randomized MAC is very common)
        4. Threat Intel Lookup
        5. More...

3. Features

        1. different SIEM ingestion with APIs
        2. different Log forwarding (ex. syslog)
        3. HTTP POST or CURL
             Ex. "curl -X POST "[ELASTIC HOST IP]:9200/?[INDEX]" 
        

## License and Copyright

The Horang log forwarder is Copyright 2024 Dave Jang and licensed under the MIT License. See 'LICENSE' for the terms of its release. 

https://opensource.org/license/mit

Copyright (c) 2024 Dave Jang

If you are interested in including this in your project, please feel free to contact me.
