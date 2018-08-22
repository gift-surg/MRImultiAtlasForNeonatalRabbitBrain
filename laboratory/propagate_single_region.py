"""
Pick a single region r of a subject and propagate it over all the other subject of the atlas,
without impacting the existing regions.
(so only the difference between the existing region and the new region is added to the
segmentation).
"""
import os
from os.path import join as jph
import nibabel as nib
import numpy as np

from nilabel.tools.aux_methods.utils_nib import set_new_data
from nilabel.main import Nilabel as NiL

import path_manager


if __name__ == '__main__':
    pfo_multi_atlas = path_manager.pfo_multi_atlas
    subject_r = '3301'
    region_r = 201
    pfi_anatomy_subject_r = jph(pfo_multi_atlas, subject_r, 'mod', '{}_T1.nii.gz'.format(subject_r))
    pfi_reg_mask_subject_r  = jph(pfo_multi_atlas, subject_r, 'masks', '{}_reg_mask.nii.gz'.format(subject_r))
    pfi_segm_where_subject_r = jph(pfo_multi_atlas, subject_r, 'segm', 'manual',
                                              '{}_manual_refinement1_v3.nii.gz'.format(subject_r))
    pfo_tmp = './z_tmp'  # Set here temporary folder
    subjects_atlas = ['1201', '1203', '1305', '1404', '1507', '1510', '1702', '1805', '2002', '2502']

    assert os.path.exists(pfi_reg_mask_subject_r)
    assert os.path.exists(pfi_anatomy_subject_r)
    assert os.path.exists(pfi_segm_where_subject_r)

    for sj in subjects_atlas:
        print sj
        pfi_segm_sj = jph(pfo_multi_atlas, sj, 'segm', '{}_approved.nii.gz'.format(sj))
        assert os.path.exists(pfi_segm_sj)

        # --- Register subject r with sj, call subject_r_over_sj
        pfi_anatomy_sj = jph(pfo_multi_atlas, sj, 'mod', '{}_T1.nii.gz'.format(sj))
        pfi_reg_mask_sj = jph(pfo_multi_atlas, sj, 'masks', '{}_reg_mask.nii.gz'.format(sj))
        assert os.path.exists(pfi_anatomy_sj)
        assert os.path.exists(pfi_reg_mask_sj)
        aff_warp = jph(pfo_tmp, '{}_over_{}_warp.nii.gz'.format(subject_r, sj))
        aff_trans = jph(pfo_tmp, '{}_over_{}_aff.txt'.format(subject_r, sj))

        cmd = 'reg_aladin -ref {0} -rmask {1} -flo {2} -fmask {3} -aff {4} -res {5}'.format(
            pfi_anatomy_sj, pfi_reg_mask_sj,
            pfi_anatomy_subject_r, pfi_reg_mask_subject_r,
            aff_trans, aff_warp
        )
        # os.system(cmd)

        # --- Propagate the segmentation r over the subject sj, call segm_r_over_sj
        segm_r_over_sj = jph(pfo_tmp, 'segm_{}_over_{}.nii.gz'.format(subject_r, sj))
        cmd = 'reg_resample -ref {0} -flo {1} -trans {2} -res {3} -inter 0'.format(
            pfi_anatomy_sj, pfi_segm_where_subject_r,
            aff_trans, segm_r_over_sj
        )
        # os.system(cmd)

        # --- Isolate the single region r in segm_r_over_sj, call segm_r_over_sj_only_r
        pfi_segm_r_over_sj_only_r = jph(pfo_tmp, 'segm_{}_over_{}_only_r.nii.gz'.format(subject_r, sj))
        nil = NiL()
        # nil.manipulate_labels.keep_one_label(segm_r_over_sj, pfi_segm_r_over_sj_only_r, label_to_keep=region_r)

        # --- subtract segm_r_over_sj_only_r to all the existing regions in segm_sj
        # call label_r_over_sj_no_overlap
        pfi_label_r_over_sj_no_overlap = jph(pfo_tmp, 'label_{}_over_{}_no_overlap.nii.gz'.format(region_r, sj))

        im_segm_sj = nib.load(pfi_segm_sj)
        data_segm_bin = im_segm_sj.get_data().astype(np.bool)
        data_segm_bin_opposite = 1 - data_segm_bin

        im_label_r = nib.load(pfi_segm_r_over_sj_only_r)

        data_label_r = im_label_r.get_data()[:]

        # - barbatrucco intermediate to elongate the segmentation on the y+ direction
        for z in xrange(82, 150):
            print z
            for x in xrange(106, 201):
                y = data_label_r.shape[1]
                while y > 0:
                    y -= 1
                    if data_label_r[x, y, z] == region_r:
                        data_label_r[x, y:y+20, z] = region_r * np.ones([20])
                        y = -1

        data_label_r_filtered = data_label_r * data_segm_bin_opposite

        im_label_r_over_sj_no_overlap = set_new_data(im_label_r, data_label_r_filtered)
        nib.save(im_label_r_over_sj_no_overlap, pfi_label_r_over_sj_no_overlap)

        # --- add label_r_over_sj_no_overlap to segm_sj
        pfo_automatic_sj = jph(pfo_multi_atlas, sj, 'segm', 'automatic')
        os.system('mkdir -p {}'.format(pfo_automatic_sj))
        pfi_result = jph(pfo_automatic_sj, '{}_approved_with_draft_ventricular_system.nii.gz'.format(sj))
        cmd = 'seg_maths {0} -add {1} {2}'.format(pfi_segm_sj, pfi_label_r_over_sj_no_overlap, pfi_result)
        os.system(cmd)
