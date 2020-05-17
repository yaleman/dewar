""" general utilities functions """

import os
import hashlib

from uuid import uuid4

def hash_file(filename: str):
    """ reurn the sha256 hash of a filename """
    if not os.path.exists(filename):
        raise ValueError(f"File {filename} does not exist!")
    with open(filename, 'rb') as fh:
        sha_sum = hashlib.sha256()
        # read a chunk
        while True:
            data = fh.read(HASH_BLOCK_SIZE)
            if not data:
                break
            sha_sum.update(data)
    return sha_sum.hexdigest()

def generate_job_id():
    """ yes, it's just using the uuid function - but it means there's one canonical way of doing it """
    return str(uuid4())
