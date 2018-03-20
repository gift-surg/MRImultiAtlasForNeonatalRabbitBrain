import os
from os.path import join as jph

from LABelsToolkit.tools.aux_methods.utils import print_and_run

import path_manager


def extract_given_path_to_chart(pfo_input_chart, input_segm_suffix='_approved_round3',
                                output_segm_suffix='_brain_tissue'):
    pfi_segm = jph(pfo_input_chart, sj, 'segm', '{0}_{1}.nii.gz'.format(sj, input_segm_suffix))
    assert os.path.exists(pfi_segm)

    # binarise segmentation to get the brain mask
    pfi_segm_bin = jph(pfo_input_chart, sj, 'segm', '{0}_{1}.nii.gz'.format(sj, output_segm_suffix))
    print_and_run('seg_maths {0} -bin {1}'.format(pfi_segm, pfi_segm_bin))

    # fill and dil the binarised segmentation
    print_and_run('seg_maths {0} -fill {0}'.format(pfi_segm_bin))
    print_and_run('seg_maths {0} -dil 1 {0}'.format(pfi_segm_bin))
    print_and_run('seg_maths {0} -ero 1 {0}'.format(pfi_segm_bin))
    print_and_run('seg_maths {0} -fill {0}'.format(pfi_segm_bin))
    print_and_run('seg_maths {0} -smol 1.5 {0}'.format(pfi_segm_bin))


if __name__ == '__main__':

    pfo_atlas_main = path_manager.pfo_multi_atlas
    atlas_subjects_list = path_manager.atlas_subjects

    for sj in atlas_subjects_list:

        extract_given_path_to_chart(jph(pfo_atlas_main, sj))

        if False:
            # copy trimmed brain and mask in the final folder
            # input :
            pfo_input_chart = jph(pfo_atlas_main, sj)
            pfi_T1_sj = jph(pfo_input_chart, 'mod', '{0}_{1}.nii.gz'.format(sj, 'T1'))
            pfi_T1_brain_tissue_mask = jph(pfo_input_chart, 'masks', '{0}_brain_tissue.nii.gz'.format(sj))
            assert os.path.exists(pfo_input_chart), pfo_input_chart
            assert os.path.exists(pfi_T1_sj), pfi_T1_sj
            assert os.path.exists(pfi_T1_brain_tissue_mask), pfi_T1_brain_tissue_mask

            # output:
            pfo_subjects_no_skull = ''  # destination.
            assert os.path.exists(pfo_subjects_no_skull)
            pfi_T1_sj_brain_only = jph(pfo_subjects_no_skull, 'mod', '{0}_{1}.nii.gz'.format(sj, 'T1'))
            pfi_T1_sj_mask_brain_only = jph(pfo_subjects_no_skull, 'mask', '{0}_{1}_brain_only.nii.gz'.format(sj, 'T1'))

            print_and_run('seg_maths {0} -mul {1} {2}'.format(pfi_T1_sj, pfi_T1_brain_tissue_mask, pfi_T1_sj_brain_only))
            print_and_run('cp {0} {1}'.format(pfi_T1_brain_tissue_mask, pfi_T1_sj_mask_brain_only))
