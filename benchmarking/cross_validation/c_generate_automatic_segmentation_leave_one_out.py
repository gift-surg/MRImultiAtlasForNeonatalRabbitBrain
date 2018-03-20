"""
All the subjects, flipped and not, are used to re-do the automatic segmentation of all subjects,
with the leave one out cross validation strategy.
"""

import os
from collections import OrderedDict
from os.path import join as jph
import numpy as np

import path_manager
from spot.spotter import SpotDS


def run_generate_automatic_segmentation_leave_one_out():

    assert os.path.exists(path_manager.pfo_atlas_validation_leave_one_out)

    # atlas flipped created with benchmarking/cross_validation/flipper
    atlas_charts_flipped = [sj + 'flip' for sj in path_manager.atlas_subjects]

    atlas_chart_complete = [item
                            for pair in zip(path_manager.atlas_subjects, atlas_charts_flipped + [0]) for item in pair]

    for target_chart_name in path_manager.atlas_subjects:

        sub_atlas_charts_with_flipped = np.sort(list(set(atlas_chart_complete) -
                                                     {target_chart_name, target_chart_name + 'flip'}))

        print('\n\nLeave one out segmentation [START]:\nSub-template is {0}\nTarget is {1}\n Spot target started!!\n'
              '\n'.format(sub_atlas_charts_with_flipped, target_chart_name))

        assert target_chart_name not in sub_atlas_charts_with_flipped

        spot_sj = SpotDS(atlas_pfo=path_manager.pfo_atlas_validation_leave_one_out,
                         target_pfo=jph(path_manager.pfo_atlas_validation_leave_one_out, target_chart_name),
                         target_name=target_chart_name,
                         parameters_tag='CrossValidation')

        # Template parameters:
        spot_sj.atlas_name = 'CrossValidationWithFlipped'  # Multi Atlas Newborn Rabbit
        spot_sj.atlas_list_charts_names = sub_atlas_charts_with_flipped
        spot_sj.atlas_list_suffix_modalities = ['T1', 'S0', 'V1', 'MD', 'FA']
        spot_sj.atlas_list_suffix_masks = ['roi_mask', 'roi_reg_mask']
        spot_sj.atlas_reference_chart_name = '1305'
        spot_sj.atlas_segmentation_suffix = 'segm'

        # --- target parameters
        spot_sj.target_list_suffix_modalities = ['T1', 'S0', 'V1', 'MD', 'FA']
        spot_sj.target_name = target_chart_name

        # --- Utils
        spot_sj.bfc_corrector_cmd = path_manager.bfc_corrector_cmd

        # --- Propagator option
        spot_sj.propagation_options['Affine_modalities'] = ('T1', 'FA')
        spot_sj.propagation_options['Affine_reg_masks'] = ()  # if (), there is a single mask for all mods
        spot_sj.propagation_options['Affine_parameters'] = ' '
        spot_sj.propagation_options['N_rigid_modalities'] = ('T1', 'FA')  # if empty, no non-rigid step.
        spot_sj.propagation_options['N_rigid_reg_masks'] = ()  # if [], same mask for all modalities
        spot_sj.propagation_options['N_rigid_slim_reg_mask'] = False
        spot_sj.propagation_options['N_rigid_mod_diff_bfc'] = ('T1',)  # empty list no diff bfc. - put a comma!!
        spot_sj.propagation_options['N_rigid_parameters'] = '  -vel -be 0.5 -ln 6 -lp 4  -smooR 0.07 -smooF 0.07  '
        spot_sj.propagation_options['N_rigid_same_mask_moving'] = False
        spot_sj.propagation_options['N_reg_mask_target'] = 0  # 0 roi_mask, 1 reg_mask
        spot_sj.propagation_options['N_reg_mask_moving'] = 1  # 0 roi_mask, 1 reg_mask
        spot_sj.propagation_options['Final_smoothing_factor'] = 0

        # --- Propagator controller
        spot_sj.propagation_controller['Aff_alignment']         = True
        spot_sj.propagation_controller['Propagate_aff_to_segm'] = True
        spot_sj.propagation_controller['Propagate_aff_to_mask'] = True
        spot_sj.propagation_controller['Get_N_rigid_slim_mask'] = True
        spot_sj.propagation_controller['Get_differential_BFC']  = True
        spot_sj.propagation_controller['N_rigid_alignment']     = True
        spot_sj.propagation_controller['Propagate_n_rigid']     = True
        spot_sj.propagation_controller['Smooth_results']        = True
        spot_sj.propagation_controller['Stack_warps_and_segms'] = True

        # --- Fuser option
        spot_sj.fuser_options['Fusion_methods'] = ['MV']  # 'MV', multi atlas only.
        spot_sj.fuser_options['Tp_mod_to_stack'] = 0
        spot_sj.fuser_options['STAPLE_params'] = OrderedDict([('pr_1', None)])
        spot_sj.fuser_options['STEPS_params'] = OrderedDict([('pr_{0}_{1}'.format(k, n), [k, n, 0.4])
                                                                  for n in [5, 7, 9]
                                                                  for k in [5,  11]])
        # --- Fuser controller
        spot_sj.fuser_controller['Fuse'] = True
        spot_sj.fuser_controller['Save_results'] = True

        spot_sj.spot_on_target_initialise()
        spot_sj.propagate()
        spot_sj.fuse()

        print('\n\nAutomatic initialisation [END] for subject {0} '
              '\n Complete atlas chart was {1} \n'.format(target_chart_name, sub_atlas_charts_with_flipped))

if __name__ == '__main__':
    run_generate_automatic_segmentation_leave_one_out()
