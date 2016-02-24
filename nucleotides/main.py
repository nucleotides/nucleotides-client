"""
nucleotides - Command line interface for running nucleotides benchmarks

Usage:
    nucleotides <command> <task> [<args>...]

Commands:
    fetch-data       Download all data necessary to perform a benchmarking task
"""

import biobox_cli.main  as bbx_main
import nucleotides.util as util

import nucleotides.command.fetch_data
import nucleotides.command.run_image
import nucleotides.command.post_data

def select_command(c):
    return {
            'fetch-data' : nucleotides.command.fetch_data,
            'run-image'  : nucleotides.command.run_image,
            'post-data'  : nucleotides.command.post_data
            }[c]

def run():
    args    = bbx_main.input_args()
    command = util.parse(__doc__, args, True)['<command>']
    select_command(command).run(args)
