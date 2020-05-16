#!/usr/bin/env python3
""" s3 storage backend for dewar """

from loguru import logger
import boto3
import botocore.errorfactory

from . import DewarStorage


class S3(DewarStorage):
    """ s3 storage backend for dewar """
    def __init__(self,
                 bucket: str,
                 endpoint_url: str,
                 aws_access_key_id: str,
                 aws_secret_access_key: str,
                 metadatastore,
                 **kwargs,
                 ):
        """ simple s3 backend using boto3 """
        self.bucket = bucket
        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = kwargs.get('region', 'us-east-1')

        self._s3client = boto3.client('s3',
                                      endpoint_url=self.endpoint_url,
                                      aws_access_key_id=self.aws_access_key_id,
                                      aws_secret_access_key=self.aws_secret_access_key,
                                      region_name=self.region,
                                      )
        self.metadatastore = metadatastore

    def delete(self, filename: str, bucket: str=None):
        """ deletes a file from a bucket """
        if not bucket:
            bucket=self.bucket
        try:
            response = self._s3client.delete_object(Bucket=bucket,
                                                    Key=filename,
                                                    )
        except botocore.errorfactory.NoSuchKey:
            return False
        return True

    def put(self, filename: str, contents: bytes, metadata: dict):
        """ store a file """
        response = self._s3client.put_object(Bucket=self.bucket,
                                             Body=contents,
                                             Key=filename,
                                             )
        return True

    def get(self, filename):
        """ gets the file, returns a dict of the file contents and metadata """
        try:
            filedata = self._s3client.get_object(Bucket=self.bucket,
                                                 Key=filename,
                                                 )
        except botocore.errorfactory.NoSuchKey:
            return False
        if not filedata.get('ContentLength'):
            return False
        return {
            'content' : filedata.get('Body'),
            'size' : filedata.get('ContentLength'),
        }
    
    def search(self, **kwargs):
        """ search for a file by one of the various metadata options
        size: int
        type: explicit type"
        """
        raise NotImplementedError

    def dir(self, bucket: str, **kwargs):
        """ list the objects in a bucket """
        file_list = {}
        files = self._s3client.list_objects(Bucket=bucket)
        while files:
            for filedata in files.get('Contents'):
                file_list[filedata.get('Key')] = {
                    'size' : filedata.get('Size'),
                }
            if files.get('IsTruncated'):
                logger.debug(f"Querying bucket... NextMarker: {files.get('NextMarker')}")
                logger.debug(files)
                files = self._s3client.list_objects(Bucket=bucket, Marker=files.get('NextMarker'))
            else:
                break
        return file_list
