import nucleotides.command.run_image as image

def create_biobox_args(app):
    return ["run",
            "assembler_benchmark",
            app["task"]["image"]["name"],
            "--input-fasta={}".format(image.get_input_file_path('contig_fasta', app)),
            "--input-ref={}".format(image.get_input_dir_path('reference_fasta', app)),
            "--output={}".format(image.get_output_file_path('assembly_metrics', app)),
            "--task={}".format(app["task"]["image"]["task"]),
            "--no-rm"]