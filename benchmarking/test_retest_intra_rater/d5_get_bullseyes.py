import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pa
from LABelsToolkit.tools.visualiser.graphs_and_stats import multi_bull_eyes

import benchmarking.test_retest_intra_rater.a_paths_intra_rater as ph


def see_bullseyes_tst_retest():
    # Parameters
    radial_subdivision = (3, 3, 4, 6)
    centered = (True, True, True, True)
    metrics = ['dice_score', 'covariance_distance', 'hausdorff_distance', 'normalised_symmetric_contour_distance']
    dict_metric_to_metric_name = {'dice_score': 'Dice Score',
                                  'covariance_distance': 'Covariance Distance',
                                  'hausdorff_distance': 'Hausdorff Distance',
                                  'normalised_symmetric_contour_distance': 'Normalised Symmetric Contour Distance'}

    for pfi_pickle_input, pfi_image_output in zip([ph.pfi_pickled_scoring_man1_man2_taxo, ph.pfi_pickled_scoring_auto_man1_taxo, ph.pfi_pickled_scoring_auto_man2_taxo],
                                                  [ph.pfi_bullseye_man1_man2,             ph.pfi_bullseye_auto_man1,             ph.pfi_bullseye_auto_man2]):
        # Load data
        df_all_labels_measures_taxon = pa.read_pickle(pfi_pickle_input)
        print df_all_labels_measures_taxon
        multi_data = []
        metrics_title = []
        for metric in metrics:
            print '\nMetric {}'.format(metric)
            metrics_title += [dict_metric_to_metric_name[metric]]
            values = df_all_labels_measures_taxon[metric]
            print values
            multi_data += [values]

            print 'max metric value : {}'.format(np.max(values))
            print 'min metric value : {}'.format(np.min(values))
            print 'average metric value (%) : {}'.format(np.mean(values))

        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')

        multi_bull_eyes(multi_data, global_title='', titles=metrics_title,
                        raidal_subdivisions=radial_subdivision, centered=centered,
                        add_nomenclatures=(True, False, False, False),
                        nomenclature_white=['<20', False, False, False],
                        cmaps=[mpl.cm.Blues_r, mpl.cm.Blues, mpl.cm.Blues, mpl.cm.Blues],
                        pfi_where_to_save=pfi_image_output)


if __name__ == '__main__':
    see_bullseyes_tst_retest()
