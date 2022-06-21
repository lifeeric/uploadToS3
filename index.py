#!/usr/bin/env python3.9

import logging
import boto3
from botocore.exceptions import ClientError
import os
import sys
import threading
import time
from datetime import datetime
import json

errors = []
path = None
try:
	path = sys.argv[1]
except IndexError as e:
	print('pass the file directory path.')
	print('Example: python index.py ~/test/')
	sys.exit('')

def upload_file(_s3_client, _file_name, _bucket, _object_name=None):
    """Upload files to an S3 bucket

    :param _file_name: File to upload
    :param _bucket: Bucket to upload to
    :param _object_name: S3 object name. if not used, _file_name will be used
    :return: True if file was upload, use _file_name
    """

    if _object_name is None:
        _object_name = _file_name

    # s3_client = boto3.client('s3')

    try:
        print('[UPLOADING]', _object_name)
        time.sleep(1)
        response = _s3_client.upload_file(_file_name, _bucket, _object_name)
    except ClientError as e:
        print('[Error]', e)
        errors.append(_file_name)
        return False
    except FileNotFoundError as e:
        print('[Error]', e)
        errors.append(_file_name)
    return True



def main():
    boto3_session = boto3.session.Session()
    s3_client =  boto3_session.client('s3')
    thread_list = []

    for root, dirs, files in os.walk(path):
        for file in files:
            _file_name = os.path.join(root, file)
            thread = threading.Thread(target=upload_file, args=(s3_client, _file_name, 'hdpbxrecordings',))  # noqa: E501

            thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == "__main__":
    main()

    with open(f"/home/centos/logs/uploadToS3-uploading-{datetime.now()}.json", "w") as f:
        json.dump(errors, f)
