from os.path import join as jph
from collections import OrderedDict

from spot.spotter import SpotDS
from spot.tools.system_parameters import bfc_corrector_cmd

import path_manager

# --- initialise the class spot:

if __name__ == '__main__':

    root_rabbits = path_manager.pfo_root

    # Set here the target name. Note that options and controller may need to be updated to the last version of
    # SPOT a neonatal rabbit. This version works for first release v0.0.0
    target_name = 'zzz'
    spot_sj = SpotDS(atlas_pfo=jph(root_rabbits, 'A_MultiAtlas'),  # here path to the folder with the atlas.
                     target_pfo=jph(root_rabbits, 'A_data/PTB/ex_vivo/{0}/stereotaxic'.format(target_name)),
                     target_name=target_name,
                     parameters_tag='P2')

    # Template parameters:
    spot_sj.atlas_name = 'MANRround3'  # Multi Atlas Newborn Rabbit
    spot_sj.atlas_list_charts_names = path_manager.atlas_subjects
    spot_sj.atlas_list_suffix_modalities = ['T1', 'S0', 'V1', 'MD', 'FA']
    spot_sj.atlas_list_suffix_masks = ['roi_mask', 'roi_reg_mask']
    spot_sj.atlas_reference_chart_name = '1305'
    spot_sj.atlas_segmentation_suffix = 'segm'

    # --- target parameters
    spot_sj.target_list_suffix_modalities = ['T1', 'S0', 'V1', 'MD', 'FA']
    spot_sj.target_name = target_name

    # --- Utils
    spot_sj.bfc_corrector_cmd = bfc_corrector_cmd

    # --- Propagator option
    spot_sj.propagation_options['Affine_modalities'] = ('T1', 'FA')
    spot_sj.propagation_options['Affine_reg_masks'] = ('T1', 'S0')  # if (), there is a single mask for all modalities
    spot_sj.propagation_options['Affine_parameters'] = ' -speeeeed '
    spot_sj.propagation_options['N_rigid_modalities'] = ('T1', 'FA')  # if empty, no non-rigid step.
    spot_sj.propagation_options['N_rigid_reg_masks'] = ('T1', 'S0')  # if [], same mask for all modalities
    spot_sj.propagation_options['N_rigid_slim_reg_mask'] = True
    spot_sj.propagation_options['N_rigid_mod_diff_bfc'] = ('T1',)  # empty list no diff bfc. - put a comma!!
    spot_sj.propagation_options['N_rigid_parameters'] = '  -be 0.5 -ln 6 -lp 4  -smooR 1.5 -smooF 1.5 '
    spot_sj.propagation_options['N_rigid_same_mask_moving'] = True
    spot_sj.propagation_options['Final_smoothing_factor'] = 0

    # --- Propagator controller
    spot_sj.propagation_controller['Aff_alignment'] = True
    spot_sj.propagation_controller['Propagate_aff_to_segm'] = True
    spot_sj.propagation_controller['Propagate_aff_to_mask'] = True
    spot_sj.propagation_controller['Get_N_rigid_slim_mask'] = True
    spot_sj.propagation_controller['Get_differential_BFC'] = True
    spot_sj.propagation_controller['N_rigid_alignment'] = True
    spot_sj.propagation_controller['Propagate_n_rigid'] = True
    spot_sj.propagation_controller['Smooth_results'] = True
    spot_sj.propagation_controller['Stack_warps_and_segms'] = True

    # --- Fuser option
    spot_sj.fuser_options['Fusion_methods'] = ['MV', 'STAPLE', 'STEPS']  # 'MV', 'STAPLE',
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
