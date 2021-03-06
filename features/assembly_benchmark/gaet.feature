Feature: Running a GAET-based reference assembly benchmark task

  Background:
    Given a clean set of benchmarks
    And no files in the S3 directory "s3://nucleotides-testing/uploads/"
    And I set the environment variables to:
      | variable           | value                             |
      | NUCLEOTIDES_S3_URL | s3://nucleotides-testing/uploads/ |


  Scenario: Executing a GAET reference assembly benchmark task
    Given I copy the example data files:
      | tasks/gaet_crash_test.json | nucleotides/6/metadata.json |
    And I copy the example data files to their SHA256 named versions:
      | generated_files/contigs.fa             | nucleotides/6/inputs/contig_fasta/     |
      | generated_files/reference.fa.gz        | nucleotides/6/inputs/reference_fasta/  |
    When I run `nucleotides --polling=1 run-image 6`
    Then the stderr should not contain anything
    And the stdout should not contain anything
    And the exit status should be 0
    And the file "nucleotides/6/outputs/container_runtime_metrics/metrics.json.gz" should exist
    And the file "nucleotides/6/outputs/container_log/1661337965" should exist
    And the file "nucleotides/6/outputs/assembly_metrics/d70c163200" should exist
    And the file "nucleotides/6/benchmark.log" should exist


  Scenario: Executing a GAET reference assembly benchmark task when there are no contigs
    # When the contigs are empty because none were generated or because they
    # were all too small and filtered out, then the client should not try to run the
    # image. The client should instead skip trying to run the container.
    Given the empty file "nucleotides/4/inputs/contig_fasta/0000000000.fa"
    And I copy the example data files:
      | tasks/gaet_crash_test.json | nucleotides/4/metadata.json |
    And I copy the example data files to their SHA256 named versions:
      | generated_files/reference.fa.gz | nucleotides/4/inputs/reference_fasta/ |
    When I run `nucleotides --polling=1 run-image 4`
    Then the stderr should not contain anything
    And the stdout should not contain anything
    And the exit status should be 0
    And the directory "nucleotides/4/outputs/container_runtime_metrics/" should not exist
    And the directory "nucleotides/4/outputs/assembly_metrics/" should not exist
    And the directory "nucleotides/4/outputs/container_log/" should not exist
    And the file "nucleotides/4/benchmark.log" should exist


  Scenario: Posting successful GAET benchmark results
    Given I copy the example data files:
      | tasks/gaet.json  | nucleotides/6/metadata.json  |
      | biobox/gaet.yaml | nucleotides/6/tmp/biobox.yaml |
      | generated_files/cgroup_metrics.json.gz | nucleotides/6/outputs/container_runtime_metrics/metrics.json.gz |
    And I copy the example data files to their SHA256 named versions:
      | generated_files/log.txt                | nucleotides/6/outputs/container_log/             |
      | generated_files/gaet_metrics.tsv       | nucleotides/6/outputs/assembly_metrics/          |
    When I run `nucleotides post-data 6`
    And I get the url "/tasks/6"
    Then the stderr should not contain anything
    And the stdout should not contain anything
    And the exit status should be 0
    And the file "nucleotides/6/benchmark.log" should exist
    And the S3 bucket "nucleotides-testing" should contain the files:
      | uploads/f8/f8efa7d0bcace3be05f4fff453e414efae0e7d5f680bf215f8374b0a9fdaf9c4 |
      | uploads/e0/e0e8af37908fb7c275a9467c3ddbba0994c9a33dbf691496a60f4b0bec975f0a |
      | uploads/f9/f962ad068784f667bb763e0f0080a832f3966dd335930638477cd66267bb289e |
    And the JSON should have the following:
      | complete                                                                  | true |
      | success                                                                   | true |
      | events/0/metrics/comparison.gene_type_distance.cds.n_symmetric_difference | 7.0  |
      | events/0/metrics/assembly.minimum_gene_set.single_copy                    | 0.0  |


  Scenario: Posting a GAET benchmark when the output includes non-mappable values
    Given I copy the example data files:
      | tasks/gaet.json  | nucleotides/6/metadata.json  |
      | biobox/gaet.yaml | nucleotides/6/tmp/biobox.yaml |
      | generated_files/cgroup_metrics.json.gz | nucleotides/6/outputs/container_runtime_metrics/metrics.json.gz |
    And I copy the example data files to their SHA256 named versions:
      | generated_files/log.txt                | nucleotides/6/outputs/container_log/             |
    And the directory "nucleotides/6/outputs/assembly_metrics/"
    And I run the bash command:
      """
      sed '/assembly.gene_type_size.cds.sum_length/s/4233/unknown/' ../../example_data/generated_files/gaet_metrics.tsv > nucleotides/6/outputs/assembly_metrics/a5c753ccb2
      """
    When I run `nucleotides post-data 6`
    And I get the url "/tasks/6"
    Then the stderr should not contain anything
    And the stdout should not contain anything
    And the exit status should be 0
    And the JSON should have the following:
       | complete          | true  |
       | success           | false |
       | events/0/metrics  | {}    |
    And the file "nucleotides/6/benchmark.log" should contain:
      """
      Error, unparsable value for assembly.gene_type_size.cds.sum_length: unknown
      """
