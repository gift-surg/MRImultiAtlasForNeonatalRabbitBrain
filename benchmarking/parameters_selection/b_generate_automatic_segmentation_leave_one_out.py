# Select random element and perform a leave one out experiment with 6 different methods.
"""
All the subjects, flipped and not, are used to re-do the automatic segmentation of all subjects,
with the leave one out cross validation strategy.
"""

import os
from collections import OrderedDict
from os.path import join as jph
import numpy as np

from benchmarking.parameters_selection import a_paths as ph
from spot.spotter import SpotDS


def run_generate_automatic_segmentation_leave_one_out(modalities=('T1', 'FA'), target_pfo=''):

    assert os.path.exists(ph.pfo_benchmarking_parameters_leave_one_out)

    atlas_subjects = ph.atlas_subjects

    for target_chart_name in [ph.selected_target]:

        atlas_without_one = np.sort(list(set(atlas_subjects) - {ph.selected_target}))

        print('\n\nLeave one out segmentation [START]:\nSub-template is {0}\nTarget is {1}\n Spot target started!!\n'
              '\n'.format(atlas_without_one, target_chart_name))

        assert target_chart_name not in atlas_without_one

        spot_sj = SpotDS(atlas_pfo=ph.pfo_benchmarking_parameters_leave_one_out,
                         target_pfo=target_pfo,
                         target_name=target_chart_name,
                         parameters_tag='CrossValidation')

        # Template parameters:
        spot_sj.atlas_name = 'Multi Atlas Newborn Rabbit'  # Multi Atlas Newborn Rabbit
        spot_sj.atlas_list_charts_names = atlas_without_one
        spot_sj.atlas_list_suffix_modalities = ['T1', 'S0', 'V1', 'MD', 'FA']
        spot_sj.atlas_list_suffix_masks = ['roi_mask', 'roi_reg_mask']
        spot_sj.atlas_reference_chart_name = '1305'
        spot_sj.atlas_segmentation_suffix = 'segm'

        # --- target parameters
        spot_sj.target_list_suffix_modalities = ['T1', 'S0', 'V1', 'MD', 'FA']
        spot_sj.target_name = target_chart_name

        # --- Utils
        spot_sj.bfc_corrector_cmd = ph.bfc_corrector_cmd

        # --- Propagator option
        spot_sj.propagation_options['Affine_modalities']        = modalities
        spot_sj.propagation_options['Affine_reg_masks']         = ()  # if (), there is a single mask for all mods
        spot_sj.propagation_options['Affine_parameters']        = ' -speeeeed '
        spot_sj.propagation_options['N_rigid_modalities']       = modalities  # if empty, no non-rigid step.
        spot_sj.propagation_options['N_rigid_reg_masks']        = ()  # if [], same mask for all modalities
        spot_sj.propagation_options['N_rigid_slim_reg_mask']    = False
        spot_sj.propagation_options['N_rigid_mod_diff_bfc']     = ('T1',)  # empty list no diff bfc. - put a comma!!
        spot_sj.propagation_options['N_rigid_parameters']       = ' -be 0.5 -ln 6 -lp 4  -smooR 0.07 -smooF 0.07  '
        spot_sj.propagation_options['N_rigid_same_mask_moving'] = False
        spot_sj.propagation_options['N_reg_mask_target']        = 0  # 0 roi_mask, 1 reg_mask
        spot_sj.propagation_options['N_reg_mask_moving']        = 1  # 0 roi_mask, 1 reg_mask
        spot_sj.propagation_options['Final_smoothing_factor']   = 0

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
        spot_sj.fuser_options['Fusion_methods'] = ['MV', 'STEPS', 'STAPLE']  # 'MV', multi atlas only.
        spot_sj.fuser_options['Tp_mod_to_stack'] = 0
        spot_sj.fuser_options['STAPLE_params'] = OrderedDict([('pr_1', None)])
        spot_sj.fuser_options['STEPS_params'] = OrderedDict([('pr_{0}_{1}'.format(k, n), [k, n, 0.4])
                                                                  for n in [5, 7, 9]
                                                                  for k in [5, 7, 10]])
        # --- Fuser controller
        spot_sj.fuser_controller['Fuse'] = True
        spot_sj.fuser_controller['Save_results'] = True

        spot_sj.spot_on_target_initialise()
        spot_sj.propagate()
        spot_sj.fuse()

        print('\n\nAutomatic initialisation [END] for subject {0} '
              '\n Complete atlas chart was {1} \n'.format(target_chart_name, atlas_without_one))


if __name__ == '__main__':

    run_generate_automatic_segmentation_leave_one_out(modalities=('T1'), target_pfo=ph.pfo_target_for_mono)
    run_generate_automatic_segmentation_leave_one_out(modalities=('T1', 'FA'), target_pfo=ph.pfo_target_for_multi)
