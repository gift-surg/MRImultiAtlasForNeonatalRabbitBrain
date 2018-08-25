"""
Common parameters used by other modules in this python package.
"""

from os.path import join as jph

from nilabels.tools.aux_methods.label_descriptor_manager import LabelsDescriptorManager
from nilabels.tools.caliber.distances import dice_score, covariance_distance, hausdorff_distance, \
    normalised_symmetric_contour_distance

import path_manager


segm_tags = ['CrossValidation']  # 'Multi' 'Mono'  # only Mono as the multi has not provided any improvements.

segm_suffix = ['MV']
# Other possible suffix:
# ['segm_STEPS_pr_{}'.format(j) for j in range(1, 13)], 'segm_STAPLE_pr_1'] +
# ['segm_STEPS_pr_{}'.format(j) for j in range(1, 6)]
metrics = ['dice_score', 'covariance_distance', 'hausdorff_distance', 'normalised_symmetric_contour_distance']
metrics_def = [dice_score, covariance_distance, hausdorff_distance, normalised_symmetric_contour_distance]
dict_metric_to_metric_name = {'dice_score': 'Dice Score',
                              'covariance_distance': 'Covariance Distance',
                              'hausdorff_distance': 'Hausdorff Distance',
                              'normalised_symmetric_contour_distance': 'Normalised Symmetric Contour Distance'}

methods_names = []
mod = ''
for cat in segm_tags:
    for segm in segm_suffix:
        if mod == '':
            methods_names += ['{0}_{1}'.format(segm, cat)]
        else:
            methods_names += ['{0}_{1}_{2}'.format(mod, segm, cat)]

ldm = LabelsDescriptorManager(path_manager.pfi_labels_descriptor)
label_descriptor_dict = ldm.dict_label_descriptor(as_string=False)
all_labels_list = list(label_descriptor_dict.keys())
all_labels_list.remove(0)
all_labels_list.remove(255)
all_labels_names = []
for l in all_labels_list:
    all_labels_names += [label_descriptor_dict[l][2]]

# OUTPUT - figures and tables

# Data, global
pfi_df_global_outline_error = jph(path_manager.pfo_data_elaborations_leave_one_out, 'global_outline_error.pickle')
pfi_df_global_dice_score = jph(path_manager.pfo_data_elaborations_leave_one_out, 'global_dice_score.pickle')

pfi_barchart_global_dice_score_per_subjects = jph(path_manager.pfo_data_elaborations_leave_one_out, 'Barchart_global_dice_score.pdf')
