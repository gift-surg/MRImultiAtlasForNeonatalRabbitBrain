import os
from os.path import join as jph

import matplotlib.pyplot as plt
import pandas as pa

import seaborn as sns

from benchmarking.a_nomenclatures import taxonomy_abbreviations, nomenclature_taxonomical, nomenclature_anatomical
import benchmarking.cross_validation.a_paths_and_parameters_cross_validation as param
import path_manager


def run_create_boxplots(nomenclature, see=False):

    if nomenclature == 'all':
        region_names = [taxonomy_abbreviations[k] for k in taxonomy_abbreviations.keys()]
        fontsize = 6
        ha = 'center'
        figsize = (12, 8)
    elif nomenclature == 'taxonomical':
        region_names = [nomenclature_taxonomical[k][0] for k in nomenclature_taxonomical.keys()]
        fontsize = 8
        ha = 'right'
        figsize = (12, 12)
    elif nomenclature == 'anatomical':
        region_names = [str(k) for k in nomenclature_anatomical.keys()]
        fontsize = 8
        ha = 'right'
        figsize = (12, 12)
    else:
        raise IOError

    dict_metric_to_metric_name = {'dice_score': '1 - Dice Score',
                                  'covariance_distance': 'Covariance Distance',
                                  'hausdorff_distance': 'Hausdorff Distance',
                                  'normalised_symmetric_contour_distance': 'Normalised Symmetric Contour Distance'}

    dict_y_axis_metric = {'dice_score': '',
                                  'covariance_distance': 'mm',
                                  'hausdorff_distance': 'mm',
                                  'normalised_symmetric_contour_distance': 'mm'}

    plt.rc('font', family='serif')

    for method in param.methods_names:

        fig, ax = plt.subplots(figsize=figsize, nrows=4, ncols=1)
        fig.canvas.set_window_title('Boxplot per region, method {}'.format(method))
        sns.set(color_codes=True)

        metrics_title = []
        for metric_id, metric in enumerate(param.metrics):
            print '\nMetric {}'.format(metric)
            metrics_title += [param.dict_metric_to_metric_name[metric]]
            pfi_df_metric = jph(path_manager.pfo_data_elaborations_leave_one_out,
                                '{0}_{1}_{2}.pickle'.format(metric, method, nomenclature))
            assert os.path.exists(pfi_df_metric), 'Did you run phase e_? File {} is not around'.format(pfi_df_metric)
            df_metric = pa.read_pickle(pfi_df_metric)
            ax[metric_id].set_title(dict_metric_to_metric_name[metric])
            ax[metric_id].boxplot([df_metric.as_matrix()[n, :] for n in range(len(region_names))])
            ax[metric_id].set_ylabel(dict_y_axis_metric[metric])
            ax[metric_id].set_xticks(range(1, len(region_names) + 1))
            ax[metric_id].set_xticklabels(region_names, ha=ha, rotation=45, fontsize=fontsize)

        pfi_where_to_save = jph(path_manager.pfo_data_elaborations_leave_one_out, 'Boxplot_{0}_{1}.pdf'.format(nomenclature, method))
        # plt.rc('text', usetex=True)
        # plt.rc('font', family='serif')
        plt.tight_layout()
        # plt.savefig(pfi_where_to_save, format='pdf', dpi=330)
        if see:
            plt.show()

if __name__ == '__main__':
    # run_create_boxplots(nomenclature='all', see=True)
    run_create_boxplots(nomenclature='taxonomical', see=True)

    print('To get the latest boxplot, run the python module cross_visualisation.py')
