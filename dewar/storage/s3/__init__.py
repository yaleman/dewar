#!/usr/bin/env python3
""" s3 storage backend for dewar """
import os

import boto3
from botocore.errorfactory import ClientError

from loguru import logger

from .. import Storage as BaseStorage


class Storage(BaseStorage):
    """ s3 storage backend for dewar """
    def __init__(self, **kwargs):
        """ simple s3 backend using boto3 """
        self.endpoint_url = kwargs.get('endpoint_url', os.environ.get('S3_ENDPOINT_URL'))
        self.aws_access_key_id = kwargs.get('aws_access_key_id', os.environ.get('AWS_ACCESS_KEY_ID'))
        self.aws_secret_access_key = kwargs.get('aws_secret_access_key', os.environ.get('AWS_SECRET_ACCESS_KEY'))
        self.region = kwargs.get('region', 'us-east-1')

        self._s3client = boto3.client('s3',
                                      endpoint_url=self.endpoint_url,
                                      aws_access_key_id=self.aws_access_key_id,
                                      aws_secret_access_key=self.aws_secret_access_key,
                                      region_name=self.region,
                                      )

        super().__init__(**kwargs)

    def delete(self, filehash: str, **kwargs):
        """ deletes a file from a bucket """
        #if not bucket:
        #    bucket = self.bucket
        bucket = kwargs.get('bucket', self.bucket)
        try:
            response = self._s3client.delete_object(Bucket=bucket,
                                                    Key=filehash,
                                                    )
            logger.debug(response)
        except ClientError as client_error:
            logger.error(client_error)
            return False
        return True

    def put(self, filehash: str, contents: bytes, metadata: dict):
        """ store a file """
        try:
            response = self._s3client.put_object(Bucket=self.bucket,
                                                 Body=contents,
                                                 Key=filehash,
                                                 )
        except ClientError as client_error:
            if 'InvalidaccessKeyId' in str(client_error):
                ak_snip = self.aws_access_key_id[:5]
                logger.error(f"InvalidaccessKeyId: Access Key supplied started with: {ak_snip}")
            else:
                logger.error(client_error)
        # TODO: put some error handling in this
        logger.debug(response)
        return True

    def get(self, filehash: str, **kwargs):
        """ gets the file, returns a dict of the file contents and metadata """
        try:
            filedata = self._s3client.get_object(Bucket=kwargs.get('bucket', self.bucket),
                                                 Key=filehash,
                                                 )
        except ClientError as client_error:
            if 'InvalidaccessKeyId' in str(client_error):
                ak_snip = self.aws_access_key_id[:5]
                logger.error(f"InvalidaccessKeyId: Access Key supplied started with: {ak_snip}")
            else:
                logger.error(client_error)
            return False
        if not filedata.get('ContentLength'):
            return False
        return {
            # if I could make content a proper file object I'd do it, but ... download_fileobj
            # seems weird, and returning it as one of them, even weirder and more prone to breaking?
            'content' : filedata.get('Body').read(),
            'size' : filedata.get('ContentLength'),
        }

    def search(self, **kwargs):
        """ search for a file by one of the various metadata options
        size: int
        type: explicit type"
        """
        raise NotImplementedError

    def dir(self, bucket: str = None):
        """ list the objects in a bucket """
        # TODO: add kwargs , **kwargs
        if not bucket:
            bucket = self.bucket
        file_list = {}
        files = self._s3client.list_objects(Bucket=bucket)
        while files:
            if files.get('Contents'):
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
            else:
                break
        return file_list
