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
    publishDir "$params.publishdir/stats", mode: 'copy'

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
    $params.metadata_group2 \
    feature_stats.tsv
    """
}


process copyFiles {
    publishDir "$params.publishdir", mode: 'copy'

    conda "$TOOL_FOLDER/conda_env.yml"

    input:
    file input_mgf
    file input_graphml

    output:
    file 'stats_copy'

    """
    mkdir stats_copy
    cp $input_mgf stats_copy/specs_ms.mgf
    cp $input_graphml stats_copy/network.graphml
    """
}

// TODO: We should integrate these directly into the graphml to make it more portable

workflow {
    metadata_ch = Channel.fromPath(params.input_metadata)
    feature_ch = Channel.fromPath(params.input_feature)

    input_mgf = Channel.fromPath(params.input_mgf)
    input_graphml = Channel.fromPath(params.input_graphml)

    // process
    calculatestats(feature_ch, metadata_ch)

    copyFiles(input_mgf, input_graphml)
}
