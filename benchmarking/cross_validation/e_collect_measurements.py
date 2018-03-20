"""
Collect data for each couple of images (ground truth, automatic) in an appropriate data structure.
 Results are plotted in the next structure. and plot
the results

OUTPUT
-----------

## Output Global_measure_confusion:

- global_dice_score.pickle
- global_outline_error.pickle

## Output Local_measures_all_labels:

- <metrics>_<methods names>_all_labels.pickle
(num_metrics x num_methods files each with shape num_regions x num_subjects)

## Output Local_measures_all_labels_taxonomical:

- <metrics>_<methods names>_labels_grouped_taxonomical.pickle
(num_metrics x num_methods files each with shape num_regions x num_subjects)

----
Each output have a shape like:

                                    1201      1203      1305      1404  ...
Medial Prefrontal Left          0.896170  0.899676  0.856563  0.783628  ...
Medial Prefrontal Right         0.879236  0.876940  0.872748  0.839293  ...
Frontal Left                    0.929168  0.930368  0.921900  0.900285  ...
Frontal Right                   0.915814  0.917815  0.926551  0.922137  ...
...                                  ...
...                                  ...
-----

"""
import os
from os.path import join as jph

import benchmarking.cross_validation.a_paths_and_parameters_cross_validation as param
import nibabel as nib
import numpy as np
import pandas as pa
from LABelsToolkit.tools.caliber import distances as dist

from benchmarking.a_nomenclatures import nomenclature_taxonomical, nomenclature_anatomical
import benchmarking.cross_validation.a_paths_and_parameters_cross_validation as ph
import path_manager


def get_measurements_by_metric_method_and_nomenclature(metric, method, nomenclature='taxonomical'):
    """
    :param metric:
    :param method:
    :param nomenclature: can be 'all' or 'taxonomical' or 'anatomical' according to the subdivision.
    :return: dataframe having labels in the rows and subjects in the column.
    """
    map_nomenclatures_lables_list = {'all': [param.all_labels_list, param.all_labels_names],
                                     'taxonomical': [nomenclature_taxonomical.keys(), [nomenclature_taxonomical[k][0] for k in nomenclature_taxonomical.keys()]],
                                     'anatomical': [nomenclature_anatomical.keys(), [nomenclature_anatomical[k][0] for k in nomenclature_anatomical.keys()]]
                                     }
    labels_list_names = map_nomenclatures_lables_list[nomenclature]
    del map_nomenclatures_lables_list

    df_metric_method_nomenclature = pa.DataFrame(
        np.zeros([len(labels_list_names[0]), len(path_manager.atlas_subjects)]), index=labels_list_names[1],
        columns=path_manager.atlas_subjects)

    for sj in path_manager.atlas_subjects:
        print sj
        pfo_segmentations_sj = jph(path_manager.pfo_atlas_validation_leave_one_out, sj, 'segm')
        if nomenclature == 'all':
            pfi_manual_segm = jph(pfo_segmentations_sj, '{}_segm.nii.gz'.format(sj))
            pfi_automatic_segm = jph(pfo_segmentations_sj, 'automatic', '{0}_{1}.nii.gz'.format(sj, method))
        else:
            pfi_manual_segm = jph(pfo_segmentations_sj, 'elaborations', '{0}_segm_{1}.nii.gz'.format(sj, nomenclature))
            pfi_automatic_segm = jph(pfo_segmentations_sj, 'elaborations', '{0}_{1}_{2}.nii.gz'.format(sj, method, nomenclature))

        assert os.path.exists(pfi_manual_segm), pfi_manual_segm
        assert os.path.exists(pfi_automatic_segm), pfi_automatic_segm

        print('Path to manual segmentation considered : {}'.format(pfi_manual_segm))
        print('Path to automatic segmentation considered : {}'.format(pfi_automatic_segm))

        im_manual = nib.load(pfi_manual_segm)
        im_automatic = nib.load(pfi_automatic_segm)
        df_metric_method_nomenclature[sj] = metric(im_manual, im_automatic, labels_list_names[0], labels_list_names[1], verbose=1)

    return df_metric_method_nomenclature


def compute_all_metric_all_methods_given_nomenclature(nomenclature):
    print '\n\n========================================'
    print 'compute all metric all methods given nomenclature {}'.format(nomenclature)
    for me in param.metrics_def:
        print '\n\nMetric {}'.format(me.__name__)
        for mn in param.methods_names:
            print 'method name {}'.format(mn)
            df_metric_method_nomenclature = get_measurements_by_metric_method_and_nomenclature(me, mn, nomenclature=nomenclature)
            pfi_df_metric_method_nomenclature = jph(path_manager.pfo_data_elaborations_leave_one_out, '{0}_{1}_{2}.pickle'.format(me.__name__, mn, nomenclature))
            df_metric_method_nomenclature.to_pickle(pfi_df_metric_method_nomenclature)


# ----------------- Global measures confusion matrices -----------------

def get_global_measurements():

    # Output:
    df_global_outline_error = pa.DataFrame(np.zeros([len(param.methods_names), len(path_manager.atlas_subjects)]),
                                           index=param.methods_names, columns=path_manager.atlas_subjects)
    df_global_dice_score = pa.DataFrame(np.zeros([len(param.methods_names), len(path_manager.atlas_subjects)]),
                                        index=param.methods_names, columns=path_manager.atlas_subjects)

    for sj in path_manager.atlas_subjects:
        print '\n============'
        print 'Subject {}'.format(sj)
        pfi_segm_manual = jph(path_manager.pfo_atlas_validation_leave_one_out, sj, 'segm', '{}_segm.nii.gz'.format(sj))
        im_manual = nib.load(pfi_segm_manual)
        for mn in param.methods_names:
            print 'Method {}'.format(mn)
            pfo_segm_automatic = jph(path_manager.pfo_atlas_validation_leave_one_out, sj, 'segm', 'automatic')
            pfi_segm_automatic = jph(pfo_segm_automatic, '{0}_{1}.nii.gz'.format(sj, mn))
            assert os.path.exists(pfi_segm_automatic), pfi_segm_automatic

            im_automatic = nib.load(pfi_segm_automatic)

            goe = dist.global_outline_error(im_manual, im_automatic)
            gds = dist.global_dice_score(im_manual, im_automatic)
            print '   Global outline error : {}'.format(goe)
            print '   Global dice score    : {}'.format(gds)

            df_global_outline_error[sj][mn] = goe
            df_global_dice_score[sj][mn]    = gds

    os.system('mkdir -p {}'.format(path_manager.pfo_data_elaborations_leave_one_out))

    df_global_outline_error.to_pickle(ph.pfi_df_global_outline_error)
    df_global_dice_score.to_pickle(ph.pfi_df_global_dice_score)


# ----------------- Metric-wise, method-wise and label-wise: all labels / taxonomical / anatomical -------------

def get_local_measurements(nomenclature):
    for nom in nomenclature:
        compute_all_metric_all_methods_given_nomenclature(nom)


if __name__ == '__main__':
    # get_global_measurements()
    get_local_measurements(nomenclature=['taxonomical', 'all'])
