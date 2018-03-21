"""
Module to visualise cross-validation and intra-rater test retest in a single barchart.
"""

import os
from os.path import join as jph
import numpy as np

import matplotlib.pyplot as plt
import pandas as pa

import seaborn as sns

from benchmarking.a_nomenclatures import taxonomy_abbreviations, nomenclature_taxonomical, nomenclature_anatomical
import benchmarking.cross_validation.a_paths_and_parameters_cross_validation as param
import benchmarking.test_retest_intra_rater.a_paths_intra_rater as ph

import path_manager


def run_create_boxplots_and_barchart_same_graph():

    # [nomenclature_taxonomical[k][0] for k in nomenclature_taxonomical.keys()]
    region_names = [str(a) for a in range(1, 17)]
    fontsize = 8
    ha = 'center'
    figsize=(12, 8)

    dict_metric_to_metric_name = {'dice_score': ' 1 - Dice Score',
                                  'covariance_distance': 'Covariance Distance',
                                  'hausdorff_distance': 'Hausdorff Distance',
                                  'normalised_symmetric_contour_distance': 'Normalised Symmetric Contour Distance'}

    dict_y_axis_metric = {'dice_score': '%',
                                  'covariance_distance': 'mm',
                                  'hausdorff_distance': 'mm',
                                  'normalised_symmetric_contour_distance': 'mm'}

    # prepare intra-rater variability data beforehand:

    df_auto_man1 = pa.read_pickle(ph.pfi_pickled_scoring_auto_man1_taxo)
    df_auto_man2 = pa.read_pickle(ph.pfi_pickled_scoring_auto_man2_taxo)

    bar_width = 0.3
    index = np.arange(1, 17)
    opacity = 0.5

    plt.rc('font', family='serif')

    for method in param.methods_names:

        fig, ax = plt.subplots(figsize=figsize, nrows=4, ncols=1)
        fig.canvas.set_window_title('Boxplot per region and test_retest intra-rater, method {}'.format(method))
        sns.set(color_codes=True)

        for metric_id, metric in enumerate(param.metrics):
            print '\nMetric {}'.format(metric)

            # fetch data:
            pfi_df_metric = jph(path_manager.pfo_data_elaborations_leave_one_out, '{0}_{1}_{2}.pickle'.format(metric, method, 'taxonomical'))
            assert os.path.exists(pfi_df_metric), 'Did you run phase e_? File {} is not around'.format(pfi_df_metric)
            df_metric = pa.read_pickle(pfi_df_metric)
            if metric == 'dice_score':
                data_bar_auto_man1 = 1 - df_auto_man1[metric]
                data_bar_auto_man2 = 1 - df_auto_man2[metric]
                data_boxplot = [1 - df_metric.as_matrix()[n, :] for n in range(len(region_names))]
            else:
                data_bar_auto_man1 = df_auto_man1[metric]
                data_bar_auto_man2 = df_auto_man2[metric]
                data_boxplot = [df_metric.as_matrix()[n, :] for n in range(len(region_names))]

            ax[metric_id].set_title(dict_metric_to_metric_name[metric])
            # Add the barplot
            ax[metric_id].bar(index - bar_width / 2, data_bar_auto_man1, bar_width, alpha=opacity, color='r', label='First manual adjustment')
            ax[metric_id].bar(index + bar_width / 2, data_bar_auto_man2, bar_width, alpha=opacity, color='b', label='Second manual adjustment')
            # Add the boxplot
            ax[metric_id].boxplot(data_boxplot)

            ax[metric_id].set_ylabel(dict_y_axis_metric[metric])
            ax[metric_id].set_xticks(range(1, len(region_names) + 1))
            ax[metric_id].set_xticklabels(region_names, ha=ha, fontsize=fontsize)

            if metric == 'dice_score':
                ax[metric_id].legend(prop={'family': 'serif'})

        # pfi_where_to_save = jph(path_manager.pfo_data_elaborations_leave_one_out, 'Boxplot_{0}_{1}.pdf'.format('taxonomical', method))

        # plt.legend(prop={'family': 'serif'})
        plt.tight_layout()

        pfi_where_to_save = jph(path_manager.pfo_data_elaborations_leave_one_out, 'cross_visualisation_{}.pdf'.format(method))
        plt.savefig(pfi_where_to_save, format='pdf', dpi=330)

        plt.show()

if __name__ == '__main__':
    run_create_boxplots_and_barchart_same_graph()
