# -*- coding: utf-8 -*-
import logging

import click
from path import path

from .restart import update_maxgaussian, restart_mip
from .start import start_mip
from trailblazer.store import api

log = logging.getLogger(__name__)


@click.group()
@click.pass_context
def analyze(context):
    pass


@analyze.command()
@click.option('-p', '--ccp', type=click.Path(exists=True), required=True)
@click.option('-a', '--analysis-type', default='genomes')
@click.option('-f', '--family', required=True)
@click.option('-c', '--config', type=click.Path(exists=True))
@click.option('-x', '--executable', type=click.Path(exists=True))
@click.option('-i', '--customer')
@click.option('-g', '--gene-list')
@click.option('-e', '--email', help='email to send errors to')
@click.option('--dryrun', is_flag=True)
@click.option('-o', '--out', type=click.File('w'), default='-')
@click.option('--conda-env')
@click.option('--script-dir', type=click.Path(exists=True))
@click.pass_context
def start(context, ccp, analysis_type, family, config, customer, gene_list,
          dryrun, executable, out, conda_env, email, script_dir):
    """Start a new analysis."""
    config = config or context.obj['mip_config']
    executable = executable or context.obj['mip_exe']
    gene_list = gene_list or context.obj['mip_genelist']
    conda_env = conda_env or context.obj.get('conda_env')
    script_dir = script_dir or context.obj.get('script_dir')

    ccp_abs = path(ccp).abspath()
    script = start_mip(
        analysis_type,
        family,
        config,
        ccp_abs,
        executable=executable,
        customer=customer,
        gene_list=gene_list,
        dryrun=dryrun,
        conda_env=conda_env,
        email=email)

    if script_dir:
        out_filename = "{}-{}.sh".format(customer or 'NA', family)
        out_path = path(script_dir).joinpath(out_filename)
        click.echo(script, file=out_path.open('w'))
    else:
        click.echo(script, file=out)


@analyze.group()
@click.pass_context
def restart(context):
    pass


@restart.command('max-gaussian')
@click.option('--restart/--no-restart', default=True)
@click.argument('config_path', type=click.Path(exists=True))
@click.argument('case_id', required=False)
@click.pass_context
def max_gaussian(context, restart, config_path, case_id):
    """Update config file to restart with Max Gaussian for SNV enabled."""
    if case_id:
        most_recent = api.case(case_id).first()
        config_path = most_recent.config_path

    update_maxgaussian(config_path)
    log.info("updated config: {}".format(config_path))
    script_dir = context.obj.get('script_dir')
    if restart and script_dir:
        restart_mip(script_dir, config_path)