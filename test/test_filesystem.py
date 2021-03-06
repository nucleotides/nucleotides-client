import os.path
import nose.tools             as nose
import helper.application     as app_helper
import nucleotides.filesystem as fs

from nose.plugins.attrib import attr

def test_get_output_biobox_file_contents():
    app = app_helper.setup_app_state('sra', 'intermediates')
    args = fs.get_output_biobox_file_contents(app)
    nose.assert_in('fasta', args[0])


def test_copy_container_output_files_with_no_files():
    app = app_helper.setup_app_state('quast', 'execute')
    input_files = {'container_log' : 'meta/log.txt', 'assembly_metrics' : 'tmp/combined_quast_output/report.tsv'}
    fs.copy_container_output_files(app, input_files)
    # Should do nothing if files don't exist


def test_copy_container_output_files_with_intermediates():
    app = app_helper.setup_app_state('quast', 'intermediates')
    input_files = {'container_log' : 'meta/log.txt', 'assembly_metrics' : 'tmp/report.tsv'}
    output_files = ['assembly_metrics/63d2a18fa1', 'container_log/e0e8af3790']

    fs.copy_container_output_files(app, input_files)
    for f in output_files:
        loc = fs.get_task_file_path(app, "outputs/" + f)
        assert os.path.isfile(loc), "Output file should be copied: {}".format(loc)


def test_biobox_yaml_exists():
    app = app_helper.setup_app_state('quast', 'execute')
    assert not fs.biobox_yaml_exists(app)
    app = app_helper.setup_app_state('quast', 'intermediates')
    assert fs.biobox_yaml_exists(app)
