""" default config file """

from loguru import logger
try:
    import config_local
except ImportError as error:
    logger.info(f"Import Error importing local config: {error}")

from dewar.frontend import frontend
import dewar.ingestor
from dewar.metadata import MetadataStore
from dewar.storage.s3 import Storage
import os

buckets = {
    'storage' : 'dewar',
    'incoming-knowngood' : 'dewar-incoming-knowngood',
    'incoming-other' : 'dewar-incoming-other',
}



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

Ingestor = dewar.ingestor.Ingestor

Ingestor.storage = storage
Ingestor.incoming_knowngood = incoming_knowngood
Ingestor.incoming_other = incoming_other
