import os
from os.path import join as jph

from probabilistic_atlas_creation.probabilistic_multi_atlas_creator import \
    binarise_and_adjust_mask_from_segmentation_path
import path_manager


if __name__ == '__main__':

    pfo_atlas_main = jph(path_manager.pfo_root, 'A_MultiAtlas')

    pfo_temp = path_manager.pfo_tmp

    for sj in path_manager.atlas_subjects:

        print('Extracting brain tissue from segmentation - Subject {}'.format(sj))

        pfi_segm_input = jph(pfo_atlas_main, sj, 'segm', '{}_segm.nii.gz'.format(sj))

        assert os.path.exists(pfi_segm_input)

        pfi_mask_output = jph(pfo_atlas_main, sj, 'masks', '{}_brain_tissue.nii.gz'.format(sj))

        if True:

            binarise_and_adjust_mask_from_segmentation_path(pfi_segm_input, pfi_mask_output, pfo_temp, subject_name=sj,
                                                            labels_to_exclude=[201, ], dil_factor=2, ero_factor=1)
