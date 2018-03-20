"""
Details of the differences between automatic method, rater1 and rater2, for the inter-modality segmentation.
Hippocampus left is compared between automatic and manual rater1 and rater2.
"""
import os
from os.path import join as jph

import pandas as pa

import path_manager


if __name__ == "__main__":

    # -- DATA contour and values

    pfi_pickled_results = jph(path_manager.pfo_test_retest_inter_rater_elaborations, 'results.pickle')
    pfi_segm_sum_contours = jph(path_manager.pfo_test_retest_inter_rater_elaborations, 'sum_contours.nii.gz')

    # -- SANITY CHECK

    msg = 'Run .benckmarking.test_retest_inter_rater first '
    assert os.path.exists(pfi_pickled_results), msg
    assert os.path.exists(pfi_segm_sum_contours), msg

    # Open result table
    df = pa.read_pickle(pfi_pickled_results)
    print df.to_latex()

    print 'See under {} for latex version'.format(
        jph(path_manager.pfo_test_retest_inter_rater_elaborations, 'result_comparison.tex'))

    msg1 = """
    Colourig idea:
    Primary colors: segmentations
    - RED      7   auto
    - YELLOW   1   L (rater 2)
    - BLUE     4   H (rater 1)

    Secondary colours: intersections
    - Orange 11   auto + H
    - Purple 8    auto + L
    - Green 5    L + H

    Axial slice used for the documentation is 181
    """
    # show figure for screenshot

    print msg1

    sj = '1203'
    pfi_anatomy = jph(path_manager.pfo_multi_atlas, sj, 'mod', '{}_T1.nii.gz'.format(sj))
    assert os.path.exists(pfi_anatomy)

    pfi_labels_descriptor = jph(path_manager.pfo_test_retest_inter_rater_input, 'label_descriptor.txt')
    cmd = 'itksnap -g {0} -s {1} -l {2}'.format(pfi_anatomy, pfi_segm_sum_contours, pfi_labels_descriptor)
    os.system(cmd)
