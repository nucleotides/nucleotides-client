from __future__ import print_function
import os, os.path

import nucleotides.log      as log
import biobox_cli.util.misc as bbx_util

def select_task(c):
    import nucleotides.task.short_read_assembler
    import nucleotides.task.reference_assembly_evaluation
    return {
            'short_read_assembler'          : nucleotides.task.short_read_assembler,
            'reference_assembly_evaluation' : nucleotides.task.reference_assembly_evaluation
            }[c]

def parse(doc, argv, opts = False):
    from docopt              import docopt
    from nucleotides.version import __version__
    return docopt(doc,
                  argv          = argv,
                  version       = __version__,
                  options_first = opts)

def create_application_state(task):
    path = os.path.join("nucleotides", task)
    bbx_util.mkdir_p(path)
    return {'api'    : get_environment_variable("NUCLEOTIDES_API"),
            'logger' : log.create_logger(os.path.join(path, "benchmark.log")),
            'path'   : path}

def get_task_metadata(task, app_state):
    import nucleotides.api_client as api
    import json
    metadata_json = os.path.join(app_state['path'], 'metadata.json')
    if os.path.isfile(metadata_json):
        with open(metadata_json, 'r') as f:
            metadata = json.loads(f.read())
    else:
        metadata = api.fetch_task(task, app_state)
        with open(metadata_json, "w") as f:
            f.write(json.dumps(metadata))
    return metadata

def application_state(task):
    app = create_application_state(task)
    app['task'] = get_task_metadata(task, app)
    return app

# http://stackoverflow.com/a/4213255/91144
def sha_digest(filename):
    import hashlib
    sha = hashlib.sha256()
    with open(filename,'rb') as f:
        for chunk in iter(lambda: f.read(sha.block_size), b''):
            sha.update(chunk)
    return sha.hexdigest()

def get_environment_variable(name):
    import sys
    if not name in os.environ:
        print("Missing environment variable: {}".format(name), file=sys.stderr)
        exit(1)
    return os.environ[name]

