#!/usr/bin/env python3

from loguru import logger
from dewar import Dewar
import config

app = Dewar(storage_backend=config.storage,
            storage_incoming_other=config.incoming_other,
            storage_incoming_knowngood=config.incoming_knowngood,
            ingestor=config.Ingestor,
            )

config.frontend.config.update(dewar=app)
config.frontend.run(debug=True)