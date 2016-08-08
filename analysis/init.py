# -*- coding: utf-8 -*-
import logging

import click

from analysis.store import api

log = logging.getLogger(__name__)


@click.command()
@click.option('-d', '--database')
@click.option('-r', '--reset', is_flag=True)
@click.pass_context
def init(context, database, reset):
    """Setup the analysis package."""
    db_uri = database or context.obj['database']
    log.info("setup a new database: %s", db_uri)
    manager = api.connect(db_uri)
    if reset:
        manager.drop_all()
    manager.create_all()
