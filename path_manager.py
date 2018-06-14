"""
Module where the paths names are called throughout the code.
prefix pfo_ ->  path to folder
prefix pfi_ ->  path to file
-----
pfo_root is where the folders with the elaborations are created and where the data downloaded from Zenodo should be
downloaded.
"""

import os
from os.path import join as jph


# Change the root folder according to the location of the downloaded data.
if os.path.exists('/cluster/project0'):
    pfo_root = '/cluster/project0/fetalsurgery/Data/MRI/KUL_preterm_rabbit_model/data/'
    bfc_corrector_cmd = '/share/apps/cmic/NiftyMIDAS/bin/niftkMTPDbc'
else:
    pfo_root = '/Volumes/SmartWare/rabbit'
    bfc_corrector_cmd = '/Applications/niftk-16.1.0/NiftyView.app/Contents/MacOS/niftkMTPDbc'

atlas_subjects = ['1201', '1203', '1305', '1404', '1507', '1510', '1702', '1805', '2002', '2502', '3301', '3404']

# Multi atlas paths:
pfo_download_from_Zenodo = jph(pfo_root, 'Zenodo')  # Change here, where you downloaded the data from Zenodo.
pfo_multi_atlas = jph(pfo_download_from_Zenodo, 'MultiAtlas')
pfi_labels_descriptor = jph(pfo_multi_atlas, 'labels_descriptor.txt')

# Leave one out:
pfo_atlas_validation_leave_one_out = jph(pfo_root, 'C_atlas_validation_leave_one_out')
pfo_data_elaborations_leave_one_out = jph(pfo_atlas_validation_leave_one_out, 'data_elaborations')

# test-retest inter-rater input - compare segmentation of hippocampi
pfo_test_retest_inter_rater_input = jph(pfo_download_from_Zenodo, 'ValidationData', 'InterRater')
# test-retest inter-rater elaborations
pfo_test_retest_inter_rater_elaborations = jph(pfo_root, 'C_atlas_validation_test_retest_inter_rater')

# test-retest intra-rater input - compare two manual adjustment
pfo_test_retest_intra_rater_input = jph(pfo_download_from_Zenodo, 'ValidationData', 'IntraRater')
# test-retest intra-rater elaborations
pfo_test_retest_intra_rater_elaborations = jph(pfo_root, 'C_atlas_validation_test_retest_intra_rater')

# probabilistic atlas:
pfo_root_probabilistic_atlas = jph(pfo_root, 'A_probabilistic_atlas')

# folder with material for images
pfo_root_for_images = jph(pfo_root, 'Z_results_for_images')

# extra temporary folder for temporary output generated during image processing
pfo_tmp = jph(pfo_root, 'Z_tmp')
