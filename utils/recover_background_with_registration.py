"""
From the atlas and the original nifti image, it recovers the background of the
atlas T1 with simple rigid registration (naive).
-
To use this code you need to have the data in the original space other than the data processed and stored in the
multi-atlas.
Contact s.ferraris@ucl.ac.uk if interested.
"""
import os
import numpy as np
import nibabel as nib

from os.path import join as jph
from nilabels.tools.image_shape_manipulations.merger import grafting
from nilabels.tools.aux_methods.utils_nib import set_new_data

import path_manager


if __name__ == '__main__':
    # where to find the temporary files of the T1 elaborations (usually starting with z_T1 for each subject)
    pfo_temporary_files = path_manager.pfo_tmp
    # where to find the atlas
    pfo_atlas = path_manager.pfo_multi_atlas
    # Results are saved in temporary files as well...

    for sj in path_manager.atlas_subjects:
        print('Subject {} registration!'.format(sj))

        pfi_sj_T1 = jph(pfo_atlas, sj, 'mod', '{}_T1.nii.gz'.format(sj))  # '1201_T1.nii.gz'
        pfi_sj_T1_reg_mask = jph(pfo_atlas, sj, 'masks', '{}_reg_mask.nii.gz'.format(sj))  # '1201_reg_mask.nii.gz'

        pfi_sj_to_std = jph(pfo_temporary_files, sj, '{}_to_std.nii.gz'.format(sj))
        pfi_sj_roi_mask_not_adjusted = jph(pfo_temporary_files, sj, '{}_T1_roi_mask_not_adjusted.nii.gz'.format(sj))

        assert os.path.exists(pfi_sj_T1)
        assert os.path.exists(pfi_sj_T1_reg_mask)

        assert os.path.exists(pfi_sj_to_std)
        assert os.path.exists(pfi_sj_roi_mask_not_adjusted)

        pfi_result = jph(pfo_temporary_files, sj, 'z_{}_T1_with_skull_and_everything.nii.gz'.format(sj))
        pfi_result_aff = jph(pfo_temporary_files, sj, 'z_{}_T1_with_skull_and_everything_aff.txt'.format(sj))

        cmd_reg = 'reg_aladin -ref {0} -rmask {1} -flo {2} -fmask {3} -res {4} -aff {5} -rigOnly'.format(
            pfi_sj_T1, pfi_sj_T1_reg_mask, pfi_sj_to_std, pfi_sj_roi_mask_not_adjusted,
            pfi_result, pfi_result_aff
        )

        print(cmd_reg)
        os.system(cmd_reg)

        print('Subject {} patch extraction and replacement'.format(sj))

        im_with_background = nib.load(pfi_result)
        im_foreground = nib.load(pfi_sj_T1)

        patch_region = im_foreground.get_data().astype(np.bool)

        condition = im_foreground.get_data().astype(np.float64).flatten() > 0
        normalisation = np.median(np.extract(condition, im_with_background.get_data().astype(np.float64).flatten()))

        grafted_data = im_with_background.get_data().astype(np.float64) * np.invert(patch_region.astype(np.bool)) /normalisation  + im_foreground.get_data().astype(np.float64)

        grafted_image = set_new_data(im_foreground, grafted_data)

        nib.save(grafted_image, jph(pfo_temporary_files, sj, 'zz_{}_T1_with_skull_and_everything_aff.nii.gz'.format(sj)))
