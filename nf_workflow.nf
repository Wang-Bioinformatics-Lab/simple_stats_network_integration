#!/usr/bin/env nextflow
nextflow.enable.dsl=2

params.input_mgf = ""
params.input_graphml = ""
params.input_feature = ""
params.input_metadata = ""

params.metadata_attribute = ""
params.metadata_group1 = ""
params.metadata_group2 = ""

//This publish dir is mostly  useful when we want to import modules in other workflows, keep it here usually don't change it
params.publishdir = "$baseDir/nf_output"
TOOL_FOLDER = "$baseDir/bin"

process calculatestats {
    publishDir "$params.publishdir", mode: 'copy'

    conda "$TOOL_FOLDER/conda_env.yml"

    input:
    file input_feature
    file input_metadata

    output:
    file 'feature_stats.tsv'

    """
    python $TOOL_FOLDER/calculate_statistics.py $input_feature \
    $input_metadata \
    $params.metadata_attribute \
    $params.metadata_group1 \
    $params.metadata_group2
    """
}

workflow {
    metadata_ch = Channel.fromPath(params.input_metadata)
    feature_ch = Channel.fromPath(params.input_feature)

    // process
    calculatestats(input_feature: feature_ch, input_metadata: metadata_ch)
}
