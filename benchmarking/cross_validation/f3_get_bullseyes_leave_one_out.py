from os.path import join as jph

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pa

from nilabels.tools.visualiser.graphs_and_stats import multi_bull_eyes

import benchmarking.cross_validation.a_paths_and_parameters_cross_validation as param
import path_manager


def run_create_bull_eye_each_couple(nomenclature='taxonomical', see=False):

    if nomenclature == 'taxonomical':
        radial_subdivision = (3, 3, 4, 6)
        centered = (True, True, True, True)

    elif nomenclature == 'anatomical':
        radial_subdivision = (2, 8, 8, 11)
        centered = (True, False, False, True)
    else:
        raise IOError

    if False:
        # subjectwise:
        for sj in path_manager.atlas_subjects:
            print sj
            for method in param.methods_names:
                metrics = []
                data = []
                for metric in param.metrics:
                    print metric
                    metrics += [metric]
                    pfi_df_metric = jph(path_manager.pfo_data_elaborations_leave_one_out, '{0}_{1}_{2}.pickle'.format(metric, method, nomenclature))
                    df_metrics = pa.read_pickle(pfi_df_metric)
                    data += [[df_metrics[sj].as_matrix()]]

                multi_bull_eyes(multi_data=data, titles=metrics, units=metrics,
                                raidal_subdivisions=radial_subdivision,
                                centered=centered, add_nomenclatures=False)

                if see:
                    plt.show()

    if True:
        # mean and standard deviation (in percentage over the mean) for all subjects
        for method in param.methods_names:
            plt.rc('text', usetex=True)
            plt.rc('font', family='serif')
            print '\n ==============='
            print 'Method {}'.format(method)
            metrics_title = []
            data = []
            std = []
            for metric in param.metrics:
                print '\nMetric {}'.format(metric)
                metrics_title += [param.dict_metric_to_metric_name[metric]]
                pfi_df_metric = jph(path_manager.pfo_data_elaborations_leave_one_out,
                                    '{0}_{1}_{2}.pickle'.format(metric, method, nomenclature))
                df_metric = pa.read_pickle(pfi_df_metric)

                mean = list(df_metric.T.mean().as_matrix())
                st_dev = list(df_metric.T.std().as_matrix())
                st_dev_in_percentage_over_the_mean = [100 * s / float(m) for m,s in zip(mean, st_dev)]
                data += [mean]
                std += [st_dev_in_percentage_over_the_mean]

                print 'max mu : {}'.format(np.max(mean))
                print 'min mu : {}'.format(np.min(mean))
                print 'max std (%) : {}'.format(np.max(st_dev_in_percentage_over_the_mean))
                print 'min std (%) : {}'.format(np.min(st_dev_in_percentage_over_the_mean))

            print 'All data and standard deviation for the method {}: '.format(method)
            print data
            print std

            pfi_where_to_save = jph(path_manager.pfo_data_elaborations_leave_one_out, 'Bullseye_{0}_{1}.pdf'.format(nomenclature, method))

            multi_bull_eyes(multi_data=data, titles=metrics_title, units=None,
                            raidal_subdivisions=radial_subdivision,
                            centered=centered, add_nomenclatures=std,
                            nomenclature_white=['<20', '>90', '>90', '>80'],
                            canvas_title=method, cmaps=[mpl.cm.Blues_r, mpl.cm.Blues,
                                                        mpl.cm.Blues, mpl.cm.Blues],
                            pfi_where_to_save=pfi_where_to_save, show=False)

            print('Bullseye saved in {}'.format(pfi_where_to_save))
            if see:
                plt.show()


if __name__ == '__main__':
    run_create_bull_eye_each_couple(see=True)
