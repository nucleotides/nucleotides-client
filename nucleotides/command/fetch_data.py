import os.path

import boltons.fileutils       as fu
import nucleotides.util        as util
import nucleotides.api_client  as api
import nucleotides.s3          as s3
import nucleotides.bio         as bio

MIN_CONTIG_LENGTH = 1000

EXTENSION_MAPPING = {
        'short_read_fastq' : '.fq.gz',
        'reference_fasta'  : '.fa.gz',
        'contig_fasta'     : '.fa' }

def destination_path(path, f):
    filename = os.path.basename(f['url']) + EXTENSION_MAPPING[f['type']]
    return os.path.join(path, 'inputs', f['type'], filename)

def which_download_file(f):
    return f['type'] in EXTENSION_MAPPING.keys()

def create_input_files(app):
    input_files = app['task']['inputs']
    for f in filter(which_download_file, input_files):
        dst = destination_path(app['path'], f)
        fu.mkdir_p(os.path.dirname(dst))
        app['logger'].debug("Downloading S3 file '{}' to '{}'".format(f['url'], dst))
        s3.fetch_file(f['url'], dst)
        if f['type'] == 'contig_fasta':
            bio.filter_contig_file(dst, MIN_CONTIG_LENGTH)

def run(task, args):
    app = util.application_state(task)
    app['logger'].info("Fetching input files for task {}".format(task))
    create_input_files(app)
    app['logger'].info("Downloaded all input files for task {}".format(task))
