#!/usr/bin/env python3

from loguru import logger
import click

from dewar import Dewar

import config

app = Dewar(storage_backend=config.storage,
            storage_incoming_other=config.incoming_other,
            storage_incoming_knowngood=config.incoming_knowngood,
            ingestor=config.Ingestor,
            )

config.frontend.config.update(dewar=app)

@click.command()
def web():
    """ starts the webserver """
    config.frontend.run(debug=True)

@click.command()
@click.option("--single", is_flag=True, default=False, help="Do a single file ingest")
def ingestor(single):
    """ runs the ingestor """
    if single:
        logger.debug("CLI Ingestor Single-run mode")
    else:
        logger.debug("Ingestor funloops")

@click.group()
def cli():
    """ placeholder for the cli, based on the `click` quickstart """
    pass

cli.add_command(web)
cli.add_command(ingestor)

cli()