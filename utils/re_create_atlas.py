"""
Re-Create atlas:
----------
From the data converted and processed in their original spaces, a single target provided externally and manually
 aligned in the selected space, and the manual segmentations of each subject, it re-creates the atlas from scratch.
 Useful for:
 - atlas reproducibility
 - small adjustment on the orientation.
 - new initial data processing
or any situation when the original segmentations has to be keept and transposed on a new processing of the same
dataset.
----------
In this code the existing atlas is used only for the manual segmentations
that are transferred on the newly generated atlas.
-
To use this code you need to have the data in the original space other than the data processed and stored in the
multi-atlas.
Contact s.ferraris@ucl.ac.uk if interested.
----------
Names variables conventions:
_data -> _reference -> _new_chart
_old_atlas

_data = files from data folder.
_reference = files from the reference subject, oriented according to histological convention.
_new_chart = output, here will go the subjects of the newly created atlas.
_old_atlas = where to get the previously made manual segmentations.
"""
import os
from os.path import join as jph
import pickle
from collections import OrderedDict
import nibabel as nib
import numpy as np

from nilabel.main import Nilabel as NiL


if __name__ == '__main__':
    #
    # WARNING! Check paths and backup multi-atlas before running.
    #
    # where to get the angles from histological to bicommissural:
    pfo_subjects_parameters = '/Volumes/sebastianof/rabbits/A_data/Utils/subjects_parameters'
    # where to get the converted data:
    pfo_data = '/Volumes/sebastianof/rabbits/A_data/PTB/ex_vivo'
    # where to get the reference subject:
    pfo_oriented_1305 = '/Users/sebastiano/a_data/atlas_re_orient/target_oriented/1305'
    # where to save the new atlas:
    pfo_new_atlas = '/Users/sebastiano/a_data/atlas_re_orient/new_atlas'
    # where to get the manual segmentations:
    pfo_current_atlas = '/Users/sebastiano/Desktop/A_temporary_template'

    # modalities involved, excluding the pivotal T1:
    mod_indexes = ['S0', 'FA', 'MD', 'V1']
    # template subjects:
    atlas_subjects = ['1201', '1203', '1305', '1404', '1507', '1510', '1702', '1805', '2002', '2502']  # '3301', '3404'

    ''' Generate new chart structure folder: '''

    controller = OrderedDict({'register_first_chart'           : True,
                              'complete_first_chart'           : False,
                              'complete_all_other_charts'      : False,
                              'adjust_propagated'              : False,
                              'propagate_manual_segmentations' : False,
                              'erase_intermediate_files'       : False,
                              'de_couple_segmentations'        : False})

    ''' 0) Talk to the user and test  '''

    assert not pfo_new_atlas == pfo_current_atlas

    print
    print 're-creation atlas: '
    print atlas_subjects, len(atlas_subjects)
    print 'Operations: '
    for c in controller.keys():
        print('{0: <40} : {1: <7}'.format(c, controller[c]))

    ''' 1) Register 1305_T1 with the oriented reference '''

    if controller['register_first_chart']:

        pfo_new_chart_1305 = jph(pfo_new_atlas, '1305')
        os.system('mkdir -p {}'.format(pfo_new_chart_1305))

        os.system('mkdir -p {}'.format(jph(pfo_new_chart_1305, 'masks')))
        os.system('mkdir -p {}'.format(jph(pfo_new_chart_1305, 'mod')))
        os.system('mkdir -p {}'.format(jph(pfo_new_chart_1305, 'segm')))

        pfo_tmp_1305_new_chart = jph(pfo_new_chart_1305, 'z_tmp_ori')
        os.system('mkdir -p {}'.format(pfo_tmp_1305_new_chart))

        pfi_1305_T1_data                      = jph(pfo_data, '1305', 'mod', '1305_T1.nii.gz')
        pfi_1305_T1_data_roi_mask             = jph(pfo_data, '1305', 'masks', '1305_T1_roi_mask.nii.gz')
        pfi_1305_T1_data_reg_mask             = jph(pfo_data, '1305', 'masks', '1305_T1_reg_mask.nii.gz')
        pfi_oriented_reference_1305_T1        = jph(pfo_oriented_1305, '1305_T1.nii.gz')
        pfi_oriented_reference_mask_1305_T1   = jph(pfo_oriented_1305, '1305_reg_mask.nii.gz')

        assert os.path.exists(pfi_1305_T1_data)
        assert os.path.exists(pfi_1305_T1_data_roi_mask)
        assert os.path.exists(pfi_oriented_reference_1305_T1)
        assert os.path.exists(pfi_oriented_reference_mask_1305_T1)

        pfi_1305_T1_hd_oriented          = jph(pfo_tmp_1305_new_chart, '1305_T1_hd_oriented.nii.gz')
        pfi_1305_T1_roi_mask_hd_oriented = jph(pfo_tmp_1305_new_chart, '1305_T1_roi_mask_hd_oriented.nii.gz')
        pfi_1305_T1_reg_mask_hd_oriented = jph(pfo_tmp_1305_new_chart, '1305_T1_reg_mask_hd_oriented.nii.gz')

        print('set header in histological orientation')

        sj_parameters = pickle.load(open(jph(pfo_subjects_parameters, '1305'), 'r'))
        if isinstance(sj_parameters['angles'][0], list):
            angle_parameter = sj_parameters['angles'][0]
        else:
            angle_parameter = sj_parameters['angles']

        angle = -1 * angle_parameter[1] # + from histo to bicomm, - from bicomm to histo.

        lt = NiL()
        lt.header.apply_small_rotation(pfi_1305_T1_data, pfi_1305_T1_hd_oriented,
                                       angle=angle, principal_axis='pitch')
        lt.header.apply_small_rotation(pfi_1305_T1_data_roi_mask, pfi_1305_T1_roi_mask_hd_oriented,
                                       angle=angle, principal_axis='pitch')
        lt.header.apply_small_rotation(pfi_1305_T1_data_reg_mask, pfi_1305_T1_reg_mask_hd_oriented,
                                       angle=angle, principal_axis='pitch')
        del lt, angle_parameter, sj_parameters

        assert os.path.exists(pfi_1305_T1_hd_oriented)
        assert os.path.exists(pfi_1305_T1_roi_mask_hd_oriented)
        assert os.path.exists(pfi_1305_T1_reg_mask_hd_oriented)

        print('register T1')

        pfi_1305_T1_on_oriented_aff = jph(pfo_tmp_1305_new_chart, '1305_T1_data_on_1305_T1_new.txt')
        pfi_1305_T1_on_oriented_warp = jph(pfo_new_chart_1305, 'mod', '1305_T1.nii.gz')

        cmd = 'reg_aladin -ref {0} -rmask {1} -flo {2} -fmask {3} -aff {4} -res {5} -rigOnly'.format(
            pfi_oriented_reference_1305_T1, pfi_oriented_reference_mask_1305_T1,
            pfi_1305_T1_hd_oriented, pfi_1305_T1_reg_mask_hd_oriented,
            pfi_1305_T1_on_oriented_aff, pfi_1305_T1_on_oriented_warp)

        os.system(cmd)

        print('adjust the resampled image')

        os.system('seg_maths {0} -thr 0 {0}'.format(pfi_1305_T1_on_oriented_warp))

        print('Propagate registration 1305_T1 to masks')

        assert os.path.exists(pfi_1305_T1_roi_mask_hd_oriented)
        assert os.path.exists(pfi_1305_T1_reg_mask_hd_oriented)

        pfi_1305_T1_roi_mask_in_new_chart = jph(pfo_new_chart_1305, 'masks', '1305_roi_mask.nii.gz')
        pfi_1305_T1_reg_mask_in_new_chart = jph(pfo_new_chart_1305, 'masks', '1305_reg_mask.nii.gz')

        cmd1 = 'reg_resample -ref {0} -flo {1} -trans {2} -res {3} -inter 0'.format(
            pfi_oriented_reference_1305_T1,
            pfi_1305_T1_roi_mask_hd_oriented,
            pfi_1305_T1_on_oriented_aff,
            pfi_1305_T1_roi_mask_in_new_chart
        )

        os.system(cmd1)

        cmd2 = 'reg_resample -ref {0} -flo {1} -trans {2} -res {3} -inter 0'.format(
            pfi_oriented_reference_1305_T1,
            pfi_1305_T1_reg_mask_hd_oriented,
            pfi_1305_T1_on_oriented_aff,
            pfi_1305_T1_reg_mask_in_new_chart
        )

        os.system(cmd2)

        del cmd1, cmd2, pfi_1305_T1_on_oriented_warp, pfi_1305_T1_on_oriented_aff, pfi_1305_T1_reg_mask_in_new_chart, \
            pfi_oriented_reference_1305_T1, pfi_1305_T1_reg_mask_hd_oriented, pfi_1305_T1_roi_mask_in_new_chart, \
            pfi_1305_T1_roi_mask_hd_oriented

    ''' 2) Complete other mods of the new chart 1305'''

    if controller['complete_first_chart']:
        # The assumption that all the modalities are registered in the same space does not hold.
        # Need to register S0 in the T1 space, considering to correct initialisation angle, then propagate the same
        # transformation for FA MD and V1.

        # Get angle parameters:
        sj_parameters = pickle.load(open(jph(pfo_subjects_parameters, '1305'), 'r'))
        if isinstance(sj_parameters['angles'][0], list):
            angle_parameter = sj_parameters['angles'][0]
        else:
            angle_parameter = sj_parameters['angles']
        angle = -1 * angle_parameter[1]  # + from histo to bicomm, - from bicomm to histo.

        # target
        pfi_1305_T1_in_new_chart = jph(pfo_new_atlas, '1305', 'mod', '1305_T1.nii.gz')
        pfi_1305_T1_reg_mask_in_new_chart = jph(pfo_new_atlas, '1305', 'masks', '1305_reg_mask.nii.gz')
        assert os.path.exists(pfi_1305_T1_in_new_chart)

        # temporary folder:
        pfo_tmp_1305_new_chart = jph(pfo_new_atlas, '1305', 'z_tmp_ori')

        # pre-orient S0 on T1
        pfi_1305_S0_data = jph(pfo_data, '1305', 'mod', '1305_S0.nii.gz')
        pfi_1305_S0_reg_mask_data = jph(pfo_data, '1305', 'masks', '1305_S0_reg_mask.nii.gz')
        assert os.path.exists(pfi_1305_S0_data)
        assert os.path.exists(pfi_1305_S0_reg_mask_data)

        pfi_1305_S0_hd_oriented = jph(pfo_tmp_1305_new_chart, '1305_S0_hd_oriented.nii.gz')
        pfi_1305_S0_reg_mask_hd_oriented = jph(pfo_tmp_1305_new_chart, '1305_S0_reg_mask_hd_oriented.nii.gz')

        nil = NiL()
        nil.header.apply_small_rotation(pfi_1305_S0_data, pfi_1305_S0_hd_oriented,
                                       angle=angle, principal_axis='pitch')
        nil.header.apply_small_rotation(pfi_1305_S0_reg_mask_data, pfi_1305_S0_reg_mask_hd_oriented,
                                       angle=angle, principal_axis='pitch')
        del nil

        # orient S0 on T1
        pfi_1305_S0_on_T1_oriented_aff  = jph(pfo_tmp_1305_new_chart, '1305_S0_on_oriented_aff.txt')
        pfi_1305_S0_on_T1_oriented_warp = jph(pfo_new_atlas, '1305', 'mod', '1305_S0.nii.gz')

        cmd = 'reg_aladin -ref {0} -rmask {1} -flo {2} -fmask {3} -aff {4} -res {5} -rigOnly'.format(
            pfi_1305_T1_in_new_chart, pfi_1305_T1_reg_mask_in_new_chart,
            pfi_1305_S0_hd_oriented, pfi_1305_S0_reg_mask_hd_oriented,
            pfi_1305_S0_on_T1_oriented_aff, pfi_1305_S0_on_T1_oriented_warp)

        os.system(cmd)

        # orient MD, FA and V1 on T1, using the S0 -> T1 transformation:
        for m in ['MD', 'FA', 'V1']:
            print('ORIENT chart 1305 mod {}'.format(m))
            pfi_1305_MOD_data = jph(pfo_data, '1305', 'mod', '1305_{}.nii.gz'.format(m))
            assert os.path.exists(pfi_1305_S0_data)
            pfi_1305_MOD_data_hd_oriented = jph(pfo_tmp_1305_new_chart, '1305_{}_hd_oriented.nii.gz'.format(m))

            nil = NiL()
            nil.header.apply_small_rotation(pfi_1305_MOD_data, pfi_1305_MOD_data_hd_oriented,
                                           angle=angle, principal_axis='pitch')
            nil.header.apply_small_rotation(pfi_1305_S0_reg_mask_data, pfi_1305_S0_reg_mask_hd_oriented,
                                           angle=angle, principal_axis='pitch')
            del nil

            print('RESAMPLE chart 1305 mod {}'.format(m))

            pfi_1305_mod_on_T1_resampled_new_chart = jph(pfo_new_atlas, '1305', 'mod', '1305_{}.nii.gz'.format(m))

            cmd = 'reg_resample -ref {0} -flo {1} -trans {2} -res {3} '.format(pfi_1305_T1_in_new_chart,
                                                                               pfi_1305_MOD_data_hd_oriented,
                                                                               pfi_1305_S0_on_T1_oriented_aff,
                                                                               pfi_1305_mod_on_T1_resampled_new_chart)
            os.system(cmd)

    ''' 3) Orient all the other charts to the newly created chart 1305'''

    if controller['complete_all_other_charts']:
        """
        From the processed input data to the new template, using as reference point the new created chart 1305.
        This part uses only the input data (divided into subfolders and named according to convention)
        and the initial chart 1305 of the new atlas.
        """
        # point to the reference chart in the new template:
        pfi_1305_T1_new_chart          = jph(pfo_new_atlas, '1305', 'mod', '1305_T1.nii.gz')
        pfi_1305_T1_reg_maks_new_chart = jph(pfo_new_atlas, '1305', 'masks', '1305_reg_mask.nii.gz')

        assert os.path.exists(pfi_1305_T1_new_chart)
        assert os.path.exists(pfi_1305_T1_reg_maks_new_chart)

        # cycle over all the other charts:
        atlas_subjects_no_1305 = sorted(set(atlas_subjects) - {'1305'})
        for sj_ch in atlas_subjects_no_1305:

            print('Creation chart {} started '.format(sj_ch))

            print('0 - Create folder structure:')
            os.system('mkdir -p {}'.format(pfo_new_atlas, sj_ch))

            pfo_sj_mask_new_chart = jph(pfo_new_atlas, sj_ch, 'masks')
            pfo_sj_mod_new_chart  = jph(pfo_new_atlas, sj_ch, 'mod')
            pfo_sj_segm_new_chart = jph(pfo_new_atlas, sj_ch, 'segm')

            os.system('mkdir -p {}'.format(pfo_sj_mask_new_chart))
            os.system('mkdir -p {}'.format(pfo_sj_mod_new_chart))
            os.system('mkdir -p {}'.format(pfo_sj_segm_new_chart))

            pfo_sj_tmp_new_chart = jph(pfo_new_atlas, sj_ch, 'z_tmp_ori')

            os.system('mkdir -p {}'.format(pfo_sj_tmp_new_chart))

            print('1 - orient header:')
            # Get angle parameters:
            sj_parameters = pickle.load(open(jph(pfo_subjects_parameters, sj_ch), 'r'))
            if isinstance(sj_parameters['angles'][0], list):
                angle_parameter = sj_parameters['angles'][0]
            else:
                angle_parameter = sj_parameters['angles']
            angle = -1 * angle_parameter[1]  # + from histo to bicomm, - from bicomm to histo.

            # Orient headers of ALL-modalities:
            for mod in ['T1', 'S0', 'FA', 'MD', 'V1']:
                pfi_mod_sj_data = jph(pfo_data, sj_ch, 'mod', '{0}_{1}.nii.gz'.format(sj_ch, mod))
                assert os.path.exists(pfi_mod_sj_data)
                pfi_mod_sj_data_hd_oriented = jph(pfo_sj_tmp_new_chart, '{0}_{1}_hd_oriented.nii.gz'.format(sj_ch, mod))
                nil = NiL()
                nil.header.apply_small_rotation(pfi_mod_sj_data, pfi_mod_sj_data_hd_oriented,
                                               angle=angle, principal_axis='pitch')

            # Orient headers roi mask and registration mask T1 and S0 :
            pfi_sj_T1_roi_mask_data = jph(pfo_data, sj_ch, 'masks', '{0}_T1_roi_mask.nii.gz'.format(sj_ch))
            pfi_sj_T1_reg_mask_data = jph(pfo_data, sj_ch, 'masks', '{0}_T1_reg_mask.nii.gz'.format(sj_ch))
            pfi_sj_S0_reg_mask_data = jph(pfo_data, sj_ch, 'masks', '{0}_S0_reg_mask.nii.gz'.format(sj_ch))
            assert os.path.exists(pfi_sj_T1_roi_mask_data)
            assert os.path.exists(pfi_sj_T1_reg_mask_data)
            assert os.path.exists(pfi_sj_S0_reg_mask_data)
            pfi_sj_T1_roi_mask_hd_oriented = jph(pfo_sj_tmp_new_chart, '{0}_T1_roi_mask_hd_oriented.nii.gz'.format(sj_ch))
            pfi_sj_T1_reg_mask_hd_oriented = jph(pfo_sj_tmp_new_chart, '{0}_T1_reg_mask_hd_oriented.nii.gz'.format(sj_ch))
            pfi_sj_S0_reg_mask_hd_oriented = jph(pfo_sj_tmp_new_chart, '{0}_S0_reg_mask_hd_oriented.nii.gz'.format(sj_ch))

            nil = NiL()
            nil.header.apply_small_rotation(pfi_sj_T1_roi_mask_data, pfi_sj_T1_roi_mask_hd_oriented,
                                            angle=angle, principal_axis='pitch')
            nil.header.apply_small_rotation(pfi_sj_T1_reg_mask_data, pfi_sj_T1_reg_mask_hd_oriented,
                                            angle=angle, principal_axis='pitch')
            nil.header.apply_small_rotation(pfi_sj_S0_reg_mask_data, pfi_sj_S0_reg_mask_hd_oriented,
                                            angle=angle, principal_axis='pitch')

            print('2 register T1 subject over T1 reference:')
            # register T1 header oriented over T1 1305 in new chart:
            pfi_T1_sj_data_hd_oriented = jph(pfo_sj_tmp_new_chart, '{0}_T1_hd_oriented.nii.gz'.format(sj_ch))

            pfi_sj_T1_over_1305_T1_aff = jph(pfo_sj_tmp_new_chart, '{}_T1_over_1305_T1_aff.txt'.format(sj_ch))
            pfi_sj_T1_over_1305_T1_warp = jph(pfo_new_atlas, sj_ch, 'mod', '{}_T1.nii.gz'.format(sj_ch))

            cmd = 'reg_aladin -ref {0} -rmask {1} -flo {2} -fmask {3} -aff {4} -res {5} -rigOnly'.format(
                pfi_1305_T1_new_chart, pfi_1305_T1_reg_maks_new_chart,
                pfi_T1_sj_data_hd_oriented, pfi_sj_T1_reg_mask_hd_oriented,
                pfi_sj_T1_over_1305_T1_aff, pfi_sj_T1_over_1305_T1_warp)
            os.system(cmd)

            # propagate to the roi and reg mask hd oriented
            pfi_sj_T1_roi_mask_new_chart = jph(pfo_new_atlas, sj_ch, 'masks', '{}_roi_mask.nii.gz'.format(sj_ch))
            cmd = 'reg_resample -ref {0} -flo {1} -trans {2} -res {3} -inter 0'.format(pfi_1305_T1_new_chart,
                                                                                       pfi_sj_T1_roi_mask_hd_oriented,
                                                                                       pfi_sj_T1_over_1305_T1_aff,
                                                                                       pfi_sj_T1_roi_mask_new_chart)
            os.system(cmd)

            pfi_sj_T1_reg_mask_new_chart = jph(pfo_new_atlas, sj_ch, 'masks', '{}_reg_mask.nii.gz'.format(sj_ch))
            cmd = 'reg_resample -ref {0} -flo {1} -trans {2} -res {3} -inter 0'.format(pfi_1305_T1_new_chart,
                                                                                       pfi_sj_T1_reg_mask_hd_oriented,
                                                                                       pfi_sj_T1_over_1305_T1_aff,
                                                                                       pfi_sj_T1_reg_mask_new_chart)
            os.system(cmd)

            print('3 register S0 subject over T1 subject:')
            pfi_S0_sj_data_hd_oriented = jph(pfo_sj_tmp_new_chart, '{0}_S0_hd_oriented.nii.gz'.format(sj_ch))

            pfi_sj_S0_over_sj_T1_aff = jph(pfo_sj_tmp_new_chart, '{0}_S0_over{0}_T1_aff.txt'.format(sj_ch))
            pfi_sj_S0_over_sj_T1_warp = jph(pfo_new_atlas, sj_ch, 'mod', '{}_S0.nii.gz'.format(sj_ch))

            cmd = 'reg_aladin -ref {0} -rmask {1} -flo {2} -fmask {3} -aff {4} -res {5} -rigOnly'.format(
                pfi_sj_T1_over_1305_T1_warp, pfi_sj_T1_reg_mask_new_chart,
                pfi_S0_sj_data_hd_oriented, pfi_sj_S0_reg_mask_hd_oriented,
                pfi_sj_S0_over_sj_T1_aff, pfi_sj_S0_over_sj_T1_warp)
            os.system(cmd)

            print('4 propagate registration to other modalities')  # Interpolation 1, as visually better results.
            for mod in ['FA', 'MD', 'V1']:
                pfi_mod_sj_data_hd_oriented = jph(pfo_sj_tmp_new_chart, '{0}_{1}_hd_oriented.nii.gz'.format(sj_ch, mod))
                pfi_mod_sj_new_chart = jph(pfo_new_atlas, sj_ch, 'mod', '{0}_{1}.nii.gz'.format(sj_ch, mod))
                cmd = 'reg_resample -ref {0} -flo {1} -trans {2} -res {3} -inter 1'.format(
                    pfi_1305_T1_new_chart,
                    pfi_mod_sj_data_hd_oriented,
                    pfi_sj_S0_over_sj_T1_aff,
                    pfi_mod_sj_new_chart)
                os.system(cmd)

        del pfi_1305_T1_new_chart, pfi_1305_T1_reg_maks_new_chart, atlas_subjects_no_1305

    ''' 4) Clean the newly converted data  '''

    if controller['adjust_propagated']:
        # Note: to reverse it, you will need to re-create the data.
        for sj_ch in atlas_subjects:
            pfi_roi_mask_new_chart = jph(pfo_new_atlas, sj_ch, 'masks', '{0}_roi_mask.nii.gz'.format(sj_ch))
            assert os.path.exists(pfi_roi_mask_new_chart)
            # adjust S0, MD, FA in_new_chart - thr and trim.
            for m in ['T1', 'S0', 'MD', 'FA']:
                print('Clean {0}, subject {1}'.format(m, sj_ch))
                pfi_mod_new_chart = jph(pfo_new_atlas, sj_ch, 'mod', '{0}_{1}.nii.gz'.format(sj_ch, m))
                assert os.path.exists(pfi_mod_new_chart)
                cmd_thr = 'seg_maths {0} -thr 0 {0}'.format(pfi_mod_new_chart)
                cmd_trim = 'seg_maths {0} -mul {1} {0}'.format(pfi_mod_new_chart, pfi_roi_mask_new_chart)
                print(cmd_thr)
                os.system(cmd_thr)
                print(cmd_trim)
                os.system(cmd_trim)
            # adjust V1 in_new_chart - triple the mask and trim.
            print('Clean V1, subject {0}'.format(sj_ch))
            pfi_V1_new_chart = jph(pfo_new_atlas, sj_ch, 'mod', '{0}_{1}.nii.gz'.format(sj_ch, 'V1'))
            pfi_V1_mask = jph(pfo_new_atlas, sj_ch, 'z_tmp_ori', '{}_V1_trimask.nii.gz'.format(sj_ch))
            cmd_tri_mask_creation = 'seg_maths {0} -merge 2 4 {0} {0} {1}'.format(pfi_roi_mask_new_chart, pfi_V1_mask)
            cmd_trim = 'seg_maths {0} -mul {1} {0}'.format(pfi_V1_new_chart, pfi_V1_mask)
            print(cmd_tri_mask_creation)
            os.system(cmd_tri_mask_creation)
            print(cmd_trim)
            os.system(cmd_trim)

    ''' 5) Orient all the manual segmentation to the new orientation '''

    if controller['propagate_manual_segmentations']:
        # for each chart, register T1 and propagate the segmentation.
        for sj in atlas_subjects:
            print('Propagate manual segmentation: subject {}'.format(sj))
            pfi_sj_T1_old_atlas            = jph(pfo_current_atlas, sj, 'mod', '{}_T1.nii.gz'.format(sj))
            pfi_sj_roi_mask_old_atlas      = jph(pfo_current_atlas, sj, 'masks', '{}_roi_mask.nii.gz'.format(sj))

            pfi_sj_T1_new_chart            = jph(pfo_new_atlas, sj, 'mod', '{}_T1.nii.gz'.format(sj))
            pfi_sj_roi_mask_new_chart      = jph(pfo_new_atlas, sj, 'masks', '{}_roi_mask.nii.gz'.format(sj))

            assert os.path.exists(pfi_sj_T1_old_atlas)
            assert os.path.exists(pfi_sj_roi_mask_old_atlas)

            assert os.path.exists(pfi_sj_T1_new_chart)
            assert os.path.exists(pfi_sj_roi_mask_new_chart)

            pfi_sj_old_T1_on_new_T1_aff = jph(pfo_new_atlas, sj, 'z_tmp_ori', '{}_old_T1_on_new_T1_aff.txt'.format(sj))
            pfi_sj_old_T1_on_new_T1_warp = jph(pfo_new_atlas, sj, 'z_tmp_ori', '{}_old_T1_on_new_T1_warp.nii.gz'.format(sj))

            # Shrink the maks
            pfi_new_mask_old_atlas = jph(pfo_new_atlas, sj, 'z_tmp_ori', '{}_new_mask_old_atlas.nii.gz'.format(sj))
            cmd = 'seg_maths {0} -ero 4 {1} '.format(pfi_sj_roi_mask_old_atlas, pfi_new_mask_old_atlas)
            os.system(cmd)

            if sj  == '2502':
                cmd = 'reg_aladin -ref {0} -rmask {1} -flo {2} -fmask {3} -aff {4} -res {5} '.format(
                    pfi_sj_T1_new_chart, pfi_sj_roi_mask_new_chart,
                    pfi_sj_T1_old_atlas, pfi_new_mask_old_atlas,
                    pfi_sj_old_T1_on_new_T1_aff, pfi_sj_old_T1_on_new_T1_warp)
            else:
                cmd = 'reg_aladin -ref {0} -rmask {1} -flo {2} -fmask {3} -aff {4} -res {5} -rigOnly'.format(
                    pfi_sj_T1_new_chart, pfi_sj_roi_mask_new_chart,
                    pfi_sj_T1_old_atlas, pfi_new_mask_old_atlas,
                    pfi_sj_old_T1_on_new_T1_aff, pfi_sj_old_T1_on_new_T1_warp)

            os.system(cmd)

            pfi_sj_approved_segm_old_atlas = jph(pfo_current_atlas, sj, 'segm', '{}_approved.nii.gz'.format(sj))
            assert os.path.exists(pfi_sj_approved_segm_old_atlas)
            pfi_sj_segm_approved_new_chart = jph(pfo_new_atlas, sj, 'segm', '{}_approved.nii.gz'.format(sj))

            cmd = 'reg_resample -ref {0} -flo {1} -trans {2} -res {3} -inter 0 '.format(pfi_sj_T1_new_chart,
                                                                                        pfi_sj_approved_segm_old_atlas,
                                                                                        pfi_sj_old_T1_on_new_T1_aff,
                                                                                        pfi_sj_segm_approved_new_chart)
            os.system(cmd)

            # set the segmentation with the appropriate data type (np.uint8).
            img = nib.load(pfi_sj_segm_approved_new_chart)
            img.set_data_dtype(np.uint8)
            nib.openers.Opener.default_compresslevel = 5
            nib.save(img, pfi_sj_segm_approved_new_chart)

    ''' 6) Erase intermediate folders '''

    if controller['erase_intermediate_files']:
        for sj_ch in atlas_subjects:
            pfo_tmp = jph(pfo_new_atlas, sj_ch, 'z_tmp_ori')
            os.system('rm -r {}'.format(pfo_tmp))

    ''' 7) De-couple segmentation '''

    if controller['de_couple_segmentations']:
        """
        To decuple the segmentations in an external folder with a git lfs repository.
        """
        pfo_destination = ''
        assert os.path.exists(pfo_destination)

        for sj in atlas_subjects:
            pfi_sj_segm_new_chart = jph(pfo_new_atlas, sj, 'segm', '{}_approved.nii.gz'.format(sj))
            pfi_sj_decoupled_new_chart = jph(pfo_destination, '{}_segm.nii.gz'.format(sj))
            os.system('cp {0} {1}'.format(pfi_sj_segm_new_chart, pfi_sj_decoupled_new_chart))
