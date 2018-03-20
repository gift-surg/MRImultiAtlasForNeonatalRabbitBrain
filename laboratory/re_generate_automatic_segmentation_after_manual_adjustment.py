"""
To remove the bias we want to update the automatic segmentation, re-doing all the segmentation propagation from an
atlas to itself, or from the atlas + atlas flipped to the original atlas.

This code is to manage the segmentation rounds.
It can be performed using the normal multi-atlas or the multi-atlas enhanced with the flipped elements, created
with the method add_flipped_atlas.py.
----
NOTE:
All the subjects are used to re-do the automatic segmentation initialisation of all subjects.
In creating the multi atlas this procedure has been alternated three times with the manual adjustment.

"""

import os
from collections import OrderedDict
from os.path import join as jph

from spot.spotter import SpotDS
from spot.tools.system_parameters import bfc_corrector_cmd

import path_manager


def run_update_automatic_segmentation_for_atlas():

    pfo_multi_atlas_third_round  = jph(path_manager.pfo_root, 'C_atlas_third_round')

    assert os.path.exists(pfo_multi_atlas_third_round)

    atlas_subjects = path_manager.atlas_subjects

    # atlas flipped created with benchmarking/cross_validation/flipper
    atlas_charts_flipped = [sj + 'flip' for sj in atlas_subjects]

    atlas_chart_complete = [item for pair in zip(atlas_subjects, atlas_charts_flipped + [0]) for item in pair]

    for target_name in atlas_subjects:

        print('\n\nAutomatic initialisation [START]: \nSub-template is {0} \n Target is {1} \n Spot target started!!\n'
              '\n'.format(atlas_chart_complete, target_name))

        atlas_pfo = pfo_multi_atlas_third_round,
        target_pfo = jph(pfo_multi_atlas_third_round, target_name)

        spot_sj = SpotDS(atlas_pfo=atlas_pfo,
                         target_pfo=target_pfo,
                         target_name=target_name,
                         parameters_tag='AutoRound3')

        # Template parameters:
        spot_sj.atlas_name = 'AutoRound3'  # Automatic round 3
        spot_sj.atlas_list_charts_names = atlas_chart_complete
        spot_sj.atlas_list_suffix_modalities = ['T1', 'S0', 'V1', 'MD', 'FA']
        spot_sj.atlas_list_suffix_masks = ['roi_mask', 'roi_reg_mask']
        spot_sj.atlas_reference_chart_name = '1305'
        spot_sj.atlas_segmentation_suffix = 'approved_round3'

        # --- target parameters
        spot_sj.target_list_suffix_modalities = ['T1', 'S0', 'V1', 'MD', 'FA']
        spot_sj.target_name = target_name

        # --- Utils
        spot_sj.bfc_corrector_cmd = bfc_corrector_cmd

        # --- Propagator option
        spot_sj.propagation_options['Affine_modalities'] = ('T1', 'FA')
        spot_sj.propagation_options['Affine_reg_masks'] = (
            'T1', 'S0')  # if (), there is a single mask for all modalities
        spot_sj.propagation_options['Affine_parameters'] = ' -speeeeed '
        spot_sj.propagation_options['N_rigid_modalities'] = ('T1', 'FA')  # if empty, no non-rigid step.
        spot_sj.propagation_options['N_rigid_reg_masks'] = ('T1', 'S0')  # if [], same mask for all modalities
        spot_sj.propagation_options['N_rigid_slim_reg_mask'] = True
        spot_sj.propagation_options['N_rigid_mod_diff_bfc'] = ('T1',)  # empty list no diff bfc. - put a comma!!
        spot_sj.propagation_options['N_rigid_parameters'] = '  -be 0.5 -ln 6 -lp 4  -smooR 1.5 -smooF 1.5 '
        spot_sj.propagation_options['N_rigid_same_mask_moving'] = True
        spot_sj.propagation_options['Final_smoothing_factor'] = 0

        # --- Propagator controller
        spot_sj.propagation_controller['Aff_alignment'] = False
        spot_sj.propagation_controller['Propagate_aff_to_segm'] = False
        spot_sj.propagation_controller['Propagate_aff_to_mask'] = False
        spot_sj.propagation_controller['Get_N_rigid_slim_mask'] = True
        spot_sj.propagation_controller['Get_differential_BFC'] = True
        spot_sj.propagation_controller['N_rigid_alignment'] = True
        spot_sj.propagation_controller['Propagate_n_rigid'] = True
        spot_sj.propagation_controller['Smooth_results'] = True
        spot_sj.propagation_controller['Stack_warps_and_segms'] = True

        # --- Fuser option
        spot_sj.fuser_options['Fusion_methods'] = ['MV']  # 'MV', 'STAPLE',
        spot_sj.fuser_options['Tp_mod_to_stack'] = 0
        spot_sj.fuser_options['STAPLE_params'] = OrderedDict([('pr1', None)])
        spot_sj.fuser_options['STEPS_params'] = OrderedDict([('pr{0}_{1}'.format(k, n), [k, n, 4])
                                                             for n in [9] for k in [5, 11]])
        # --- Fuser controller
        spot_sj.fuser_controller['Fuse'] = True
        spot_sj.fuser_controller['Save_results'] = True

        spot_sj.spot_on_target_initialise()
        spot_sj.propagate()
        spot_sj.fuse()

        print('\n\nAutomatic initialisation [END] for subject {0} '
              '\n Complete atlas chart was {1} \n'.format(target_name, atlas_chart_complete))

if __name__ == '__main__':
    run_update_automatic_segmentation_for_atlas()
