""" constants to use across all the things """


METADATA_TYPES = {
    'file' : { # stored file
        'filehash' : str, # sha256 hash of the file
        'known_good' : bool, # if this has been tagged known-good
    },
    'job' : { # ingestion job
        'guid' : str, # a uuid.uuid4()
        'timestamp' : int,  # unix seconds since epoch
        'name' : str, # filename of the archive ingested
        'notes' : str,
        'known_good' : bool, # if the whole job was tagged known-good
    },
    'jobfile' : { # files within a job
        'job' : str, # the uuid.uuid4() of the job
        'path' : str, # relative file path within the job
        'filehash' : str, # file['filehash']
    },
    'other' : {},
}


METADATA_FILEHASH_LENGTH = 64
METADATA_GUID_LENGTH = 36
METADATA_RELATIVE_PATH_LENGTH = 255
