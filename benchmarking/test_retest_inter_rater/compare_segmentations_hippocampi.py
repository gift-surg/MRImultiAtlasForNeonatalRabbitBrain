"""
Details of the differences between automatic method, rater1 and rater2, for the inter-modality segmentation.
Hippocampus left is compared between automatic and manual rater1 and rater2.
"""
import os
from os.path import join as jph

from collections import OrderedDict
import numpy as np
import nibabel as nib

import pandas as pa

from LABelsToolkit.main import LABelsToolkit as LabT
from LABelsToolkit.tools.caliber.distances import dice_score_l, hausdorff_distance_l, symmetric_contour_distance_l, \
    covariance_distance

import path_manager


def run_comparison_inter_rater():
    # -- CONTROLLER

    label_hippocampus = 31
    pfo_root_experiments_input = path_manager.pfo_test_retest_inter_rater_input
    pfo_root_experiments_output = path_manager.pfo_test_retest_inter_rater_elaborations

    controller = {'compute_data'      : True,
                  'plot_data_table'   : True,
                  'see_segmentations' : True}

    # -- DATA

    pfi_segm_raterH = jph(pfo_root_experiments_input, 'H.nii.gz')
    pfi_segm_raterL = jph(pfo_root_experiments_input, 'L.nii.gz')
    pfi_segm_auto = jph(pfo_root_experiments_input, 'auto.nii.gz')

    assert os.path.exists(pfi_segm_raterH)
    assert os.path.exists(pfi_segm_raterL)
    assert os.path.exists(pfi_segm_auto)

    # -- WORKFLOW

    if controller['compute_data']:
        raterH_vs_raterL = np.zeros(4)
        raterH_vs_auto = np.zeros(4)
        raterL_vs_auto = np.zeros(4)

        im_raterH = nib.load(pfi_segm_raterH)
        im_raterL = nib.load(pfi_segm_raterL)
        im_auto = nib.load(pfi_segm_auto)

        # dice score:
        raterH_vs_raterL[0] = dice_score_l(im_raterH, im_raterL, label_hippocampus)
        raterH_vs_auto[0] = dice_score_l(im_raterH, im_auto, label_hippocampus)
        raterL_vs_auto[0] = dice_score_l(im_raterL, im_auto, label_hippocampus)

        # Covariance distance:
        raterH_vs_raterL[1] = covariance_distance(im_raterH, im_raterL, [label_hippocampus, ], [label_hippocampus, ],
                                                  factor=10)[label_hippocampus]
        raterH_vs_auto[1] = covariance_distance(im_raterH, im_auto, [label_hippocampus, ], [label_hippocampus, ],
                                                factor=10)[label_hippocampus]
        raterL_vs_auto[1] = covariance_distance(im_raterL, im_auto, [label_hippocampus, ], [label_hippocampus, ],
                                                factor=10)[label_hippocampus]

        # Hausdorff distance:
        raterH_vs_raterL[2] = hausdorff_distance_l(im_raterH, im_raterL, label_hippocampus, return_mm3=True)
        raterH_vs_auto[2] = hausdorff_distance_l(im_raterH, im_auto, label_hippocampus, return_mm3=True)
        raterL_vs_auto[2] = hausdorff_distance_l(im_raterL, im_auto, label_hippocampus, return_mm3=True)

        # NSCD:
        raterH_vs_raterL[3] = symmetric_contour_distance_l(im_raterH, im_raterL, label_hippocampus, return_mm3=True)
        raterH_vs_auto[3] = symmetric_contour_distance_l(im_raterH, im_auto, label_hippocampus, return_mm3=True)
        raterL_vs_auto[3] = symmetric_contour_distance_l(im_raterL, im_auto, label_hippocampus, return_mm3=True)

        print raterH_vs_raterL
        print raterH_vs_auto
        print raterL_vs_auto

        d = OrderedDict(
            {'raterH_vs_raterL': raterH_vs_raterL, 'raterH_vs_auto': raterH_vs_auto, 'raterL_vs_auto': raterL_vs_auto})
        df = pa.DataFrame(data=d, index=['Dice', 'CovDist', 'HD', 'NSCD'])

        df.T.to_pickle(jph(pfo_root_experiments_output, 'results.pickle'))

    if controller['compute_data']:
        df = pa.read_pickle(jph(pfo_root_experiments_output, 'results.pickle'))
        print df.to_latex()
        df.to_latex(jph(pfo_root_experiments_output, 'result_comparison.tex'))

    if controller['see_segmentations']:
        """
        Colourig idea:
        Primary colors: segmentations
        - RED      7   auto
        - YELLOW   1   L (rater 2)
        - BLUE     4   H (rater 1)

        Secondary colours: intersections
        - Orange 11   auto + H
        - Purple 8    auto + L
        - Green 5    L + H

        Axial slice suggested 181
        """

        for f, f_label in zip(['L', 'H', 'auto'], [1, 4, 7]):
            # get contours
            pfi_segm = jph(pfo_root_experiments_input, '{}.nii.gz'.format(f))
            assert os.path.exists(pfi_segm)
            pfi_contour = jph(pfo_root_experiments_output, '{}_contour.nii.gz'.format(f))

            lt = LabT()
            lt.manipulate_intensities.get_contour_from_segmentation(pfi_segm, pfi_contour, omit_axis='y', verbose=1)
            # change labels values:
            os.system('seg_maths {0} -bin {0}'.format(pfi_contour))
            os.system('seg_maths {0} -mul {1} {0}'.format(pfi_contour, f_label))

        # sum contour together within a single segmentation:
        pfi_final_sum = jph(pfo_root_experiments_output, 'sum_contours.nii.gz')
        os.system('cp {0} {1}'.format(jph(pfo_root_experiments_output, '{}_contour.nii.gz'.format('L')), pfi_final_sum))
        for f in ['H', 'auto']:
            os.system('seg_maths {0} -add {1} {0}'.format(pfi_final_sum,
                                                          jph(pfo_root_experiments_output,
                                                              '{}_contour.nii.gz'.format(f))))

        # open them: (anonymised and randomly selected subject 1203, hidden from the rater)
        sj = '1203'
        pfi_anatomy = jph(path_manager.pfo_multi_atlas, sj, 'mod', '{}_T1.nii.gz'.format(sj))
        assert os.path.exists(pfi_anatomy)
        pfi_labels_descriptor = jph(pfo_root_experiments_input, 'label_descriptor.txt')
        cmd = 'itksnap -g {0} -s {1} -l {2}'.format(pfi_anatomy, pfi_final_sum, pfi_labels_descriptor)
        os.system(cmd)


if __name__ == "__main__":
    run_comparison_inter_rater()
