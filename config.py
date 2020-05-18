""" default config file """

from loguru import logger
try:
    import config_local
except ImportError as error:
    logger.info(f"Import Error importing local config: {error}")

from dewar.frontend import frontend
import dewar.ingestor.basic
import dewar.metadata.tinydb


from dewar.storage.s3 import Storage
import os

buckets = {
    'storage' : 'dewar',
    'incoming-knowngood' : 'dewar-incoming-knowngood',
    'incoming-other' : 'dewar-incoming-other',
}

MetadataStore = dewar.metadata.tinydb.MetadataStore(filename='dewar.json')


storage = Storage(bucket=buckets['storage'],
                         endpoint_url=os.environ.get('S3_ENDPOINT_URL'),
                         metadatastore=MetadataStore,
                         )

incoming_knowngood = Storage(bucket=buckets['incoming-knowngood'],
                         endpoint_url=os.environ.get('S3_ENDPOINT_URL'),
                         metadatastore=MetadataStore,
                         )

incoming_other = Storage(bucket=buckets['incoming-other'],
                         endpoint_url=os.environ.get('S3_ENDPOINT_URL'),
                         metadatastore=MetadataStore,
                         )

Ingestor = dewar.ingestor.basic.Ingestor()

Ingestor.storage = storage
Ingestor.incoming = {
   'known_good': incoming_knowngood,
   'other' : incoming_other,
}
