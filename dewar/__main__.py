#!/usr/bin/env python3

from dewar import Dewar
import config

app = Dewar(frontend=config.frontend,
            storage_backend=config.storage,
            )

app.frontend.run()