import os
from os.path import join as jph
import nibabel as nib
import numpy as np

from nilabel.tools.aux_methods.utils_nib import set_new_data

import path_manager

"""
Module to get the visual differencies between 
two segmentations.
"""


if __name__ == '__main__':

    # paths input:
    root_rabbit = path_manager.pfo_root
    root_main_sj = jph(root_rabbit, 'test_re_test_segmentation', 'target1111')

    # paths output:
    pfi_difference_segm = jph(root_rabbit, 'z_erase_me.nii.gz')

    pfi_segm_manual_1 = jph(root_main_sj, 'segm', 'approved', 'target1111_approved_first.nii.gz')
    pfi_segm_manual_2 = jph(root_main_sj, 'segm', 'approved', 'target1111_approved_second.nii.gz')
    pfi_segm_automatic_MV = jph(root_main_sj, 'segm', 'automatic', 'target1111_T1_segm_MV_s.nii.gz')
    pfi_multi_labels_descriptor = jph(root_rabbit, 'study', 'A_internal_template', 'LabelsDescriptors',
                                      'labels_descriptor_v8.txt')

    im1 = nib.load(pfi_segm_manual_1)
    im2 = nib.load(pfi_segm_manual_2)

    diff = (im1.get_data() - im2.get_data()).astype(np.bool)

    im_diff = set_new_data(im1, diff)

    nib.save(im_diff, pfi_difference_segm)