# Horangi-Forwarder

## [Description]

This horangi forwarder is a log forwarder to inspect multiple subdirectories within a designated main directory for files. The script should load files with appended data and verify if the files have already been loaded before proceeding to the next file.

     Note: Test Version! Please don't use it for the production environment.

## [Usage]

A desinated main directory is the folder with multiple subdirectories and files.
The interval is optional. An interval of 10 seconds is recommended for the data ingestion rate.

    python3 logforwarder.py \<directory> \[\<interval\>\]
    Ex. python3 horangi_forwarder.py /nsm/zeek/
    Ex. python3 horangi_forwarder.py c:\users\myaccount\Desktop\zeek\

## [Future]

1. Elastic API to load JSONs to the destination Elasticsearch DB

       Dependency: python -m pip install elasticsearch
2. File validation
