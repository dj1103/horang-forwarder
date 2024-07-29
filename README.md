# Horang-Forwarder

## Description

This Horang forwarder is a log forwarder to inspect multiple subdirectories within a designated main directory for files. The script should load files with appended data and verify if the files have already been loaded before proceeding to the next file.

     Note: Test Version! Please don't use it for the production environment.

## Version

Testing with Python 3.12, published on 2023-10-02, expires on 2028-10, PEP 693
     https://www.python.org/downloads/

## Dependency

     python3 -m pip install

## Usage

A designated main directory is the folder with multiple subdirectories and files.
The interval is optional. An interval of 10 seconds is recommended for the data ingestion rate.

    python3 logforwarder.py <directory> [<interval>]
    Ex. python3 horang_forwarder.py /nsm/zeek/
    Ex. python3 horang_forwarder.py c:\users\myaccount\Desktop\zeek\

## Future

1. Elastic API to load JSONs to the destination Elasticsearch DB

       Dependency: python -m pip install elasticsearch
2. File validation and Data normalization

        1. JSON to load
        2. CSV to JSON to load
        3. remove garbage data
        4. compressed file (ex. gz) unzip to JSON
        5. filter out or skip non-loadable data (ex. exe)
        6. [optional] field normalization - (ex. id.resp_h to dest_ip and ips)

4. Data Enrichment

        1. Maxmind DB - ASN and GeoIP
        2. DHCP Host name adding to conn.log
        3. MAC OUI Lookup (Randomized MAC is very common)
        4. Threat Intel Lookup
        5. More...

6. Features

        1. HTTP Post or CURL
             Ex. "curl -X POST "[ELASTIC HOST IP]:9200/?[INDEX]" 
        2. different SIEM ingestion
        3. different Log forwarding (ex. syslog)

## License and Copyright

The Horang log forwarder is Copyright 2024 D Jang and licensed under the MIT License. See 'LICENSE' for the terms of its release.

https://opensource.org/license/mit

Copyright (c) 2024 D Jang

If you are interested in including this in your project, please feel free to contact me.
