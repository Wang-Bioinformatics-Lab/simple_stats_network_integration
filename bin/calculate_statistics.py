import sys
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='Test write out a file.')
    parser.add_argument('input_feature')
    parser.add_argument('input_metadata')
    parser.add_argument('metadata_attribute')
    parser.add_argument('group1')
    parser.add_argument('group2')
    parser.add_argument('output_filename', help='Output filename')

    args = parser.parse_args()

    features_df = pd.read_csv(args.input_feature, sep=",")
    metadata_df = pd.read_csv(args.input_metadata, sep="\t")

    group1_filenames = metadata_df[metadata_df[args.metadata_attribute] == args.group1]['filename'].tolist()
    group2_filenames = metadata_df[metadata_df[args.metadata_attribute] == args.group2]['filename'].tolist()

    # iterate through each feature row and calculate the stats
    # for each group
    output_stats = []

    features_list = features_df.to_dict(orient='records')

    for feature_row in features_list:
        group1_quants = []
        group2_quants = []

        for group1_filename in group1_filenames:
            group1_quants.append(feature_row[group1_filename + " Peak area"])

        for group2_filename in group2_filenames:
            group2_quants.append(feature_row[group2_filename + " Peak area"])

        # calcualte the t-test statistic and wilcoxon statistic
        # and p-value for each feature

        import scipy.stats as stats
        group1_ttest_statistic, group1_p_value = stats.ttest_ind(group1_quants, group2_quants)

        group2_wilcoxon_statistic, group2_p_value = stats.wilcoxon(group1_quants, group2_quants)

        output_dict = {
            'feature': feature_row['feature'],
            'group1_ttest_statistic': group1_ttest_statistic,
            'group1_p_value': group1_p_value,
            'group2_wilcoxon_statistic': group2_wilcoxon_statistic,
            'group2_p_value': group2_p_value
        }

        output_stats.append(output_dict)

    # write out the output stats to a file
    output_df = pd.DataFrame(output_stats)
    output_df.to_csv(args.output_filename, sep="\t", index=False)



if __name__ == "__main__":
    main()