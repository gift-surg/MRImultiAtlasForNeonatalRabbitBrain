import os
from os.path import join as jph
import nibabel as nib

from nilabel.tools.image_colors_manipulations.relabeller import relabel_half_side_one_label
from nilabel.tools.aux_methods.utils_nib import set_new_data

import path_manager


def segmentation_separator(pfi_segm_input, pfi_segm_output):
    im_seg = nib.load(pfi_segm_input)

    data_seg_new = relabel_half_side_one_label(im_seg.get_data(), 213, 214, 'above', 'x', 159)

    im_seg_new = set_new_data(im_seg, data_seg_new)
    nib.save(im_seg_new, pfi_segm_output)


if __name__ == '__main__':

    atlas_subjects = ['1201', '1203', '1305', '1404', '1507', '1510', '1702', '1805', '2002', '2502']  # '3301', '3404'
    if False:
        pfo_atlas = path_manager.pfo_multi_atlas
        for sj in atlas_subjects:
            print sj
            pfo_segm = jph(pfo_atlas, sj, 'segm')
            pfi_one = jph(pfo_segm, sj + '_approved.nii.gz')
            pfi_two = jph(pfo_segm, 'test_PV_' + sj + '_approved.nii.gz')

            assert os.path.exists(pfi_one)
            assert os.path.exists(pfi_two)

            segmentation_separator(pfi_one, pfi_one)
            segmentation_separator(pfi_two, pfi_two)
    if False:
        pfo_atlas = path_manager.pfo_multi_atlas
        pfo_new_chart_segm_auto = jph(pfo_atlas, '3301', 'segm', 'automatic')
        pfo_new_chart_segm_manual = jph(pfo_atlas, '3301', 'segm', 'manual')

        for fin in os.listdir(pfo_new_chart_segm_auto):
            if fin.endswith('.nii.gz'):
                pfi_segm = jph(pfo_new_chart_segm_auto, fin)
                print pfi_segm
                assert os.path.exists(pfi_segm)
                segmentation_separator(pfi_segm, pfi_segm)

        for fin in os.listdir(pfo_new_chart_segm_manual):
            if fin.endswith('.nii.gz'):
                pfi_segm = jph(pfo_new_chart_segm_manual, fin)
                print pfi_segm
                assert os.path.exists(pfi_segm)
                segmentation_separator(pfi_segm, pfi_segm)
    if False:
        pfo_atlas = path_manager.pfo_multi_atlas
        for sj in ['1201', '1203', '1305', '1404', '1507', '1510', '1702', '1805', '2002', '2502'] :
            print sj
            pfo_segm = jph(pfo_atlas, sj, 'segm')
            pfi_one = jph(pfo_segm, sj + '_segm.nii.gz')
            pfi_two = jph(pfo_segm, 'test_PV_' + sj + '_segm.nii.gz')

            assert os.path.exists(pfi_one)
            assert os.path.exists(pfi_two)

            segmentation_separator(pfi_one, pfi_one)
            segmentation_separator(pfi_two, pfi_two)

            pfo_mono = jph(pfo_segm, 'automatic')
            for fin in os.listdir(pfo_mono):
                if fin.endswith('.nii.gz'):
                    pfi_segm = jph(pfo_mono, fin)
                    print pfi_segm
                    assert os.path.exists(pfi_segm)
                    segmentation_separator(pfi_segm, pfi_segm)
