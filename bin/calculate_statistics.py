import sys
import argparse
import pandas as pd
import numpy as np

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
            try:
                group1_quants.append(feature_row[group1_filename + " Peak area"])
            except:
                continue

        for group2_filename in group2_filenames:
            try:
                group2_quants.append(feature_row[group2_filename + " Peak area"])
            except:
                continue

        # calcualte the t-test statistic and mannwhitney statistic
        # and p-value for each feature
        try:

            import scipy.stats as stats
            ttest_statistic, ttest_pvalue = stats.ttest_ind(group1_quants, group2_quants)

            mannwhitney_statistic, mannwhitney_pvalue = stats.mannwhitneyu(group1_quants, group2_quants)

            # we shoudl also calculate -log p-value for each test
            # and add it to the output dict

            # check if the p-value is 0, if so set it to a small value
            if ttest_pvalue == 0:
                ttest_pvalue = 1e-10
            if mannwhitney_pvalue == 0:
                mannwhitney_pvalue = 1e-10

            # calculate -log p-value
            ttest_log_pvalue = -1 * np.log10(ttest_pvalue)
            mannwhitney_log_pvalue = -1 * np.log10(mannwhitney_pvalue)

            output_dict = {
                'feature': feature_row['feature'],
                'ttest_pvalue': ttest_pvalue,
                'ttest_log_pvalue': ttest_log_pvalue,
                'ttest_statistic': ttest_statistic,
                'mannwhitney_pvalue': mannwhitney_pvalue,
                'mannwhitney_log_pvalue': mannwhitney_log_pvalue,
                'mannwhitney_statistic': mannwhitney_statistic,
            }

            output_stats.append(output_dict)
        except:
            raise

    # write out the output stats to a file
    output_df = pd.DataFrame(output_stats)
    output_df.to_csv(args.output_filename, sep="\t", index=False)



if __name__ == "__main__":
    main()