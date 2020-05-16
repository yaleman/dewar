#!/usr/bin/env python3
""" s3 storage backend for dewar """


import boto3
from . import DewarStorage


class S3(DewarStorage):
    """ s3 storage backend for dewar """
    def __init__(self, bucket: str, endpoint_url: str, aws_access_key_id: str, aws_secret_access_key: str, **kwargs):
        """ simple s3 backend using boto3 """
        self.bucket = bucket
        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = kwargs.get('region', 'us-east-1')
        super().__init__(self)

    def _s3client(self):
        """ returns a boto3.client object, saves me doing this over and over """
        return boto3.client('s3',
                            endpoint_url=self.endpoint_url,
                            aws_access_key_id=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key,
                            region_name=self.region,
                            )

    def get(self, filehash):
        """ gets the file by hash, returns a dict of the file contents and metadata """

        return {
            'content' : b"testing",
            'size' : 7,
        }
