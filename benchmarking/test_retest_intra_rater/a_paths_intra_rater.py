import os
from os.path import join as jph


import path_manager


pfo_input = path_manager.pfo_test_retest_intra_rater_input
pfo_elaborations = path_manager.pfo_test_retest_intra_rater_elaborations

# Root folder where the three segmentations that we want to compare are stored (automatic, manual 1, manual 2)
# id subject is '2002' - hidden from the rater

pfi_segm_auto = jph(pfo_input, 'segm_auto.nii.gz')
pfi_segm_man1 = jph(pfo_input, 'segm_man1.nii.gz')
pfi_segm_man2 = jph(pfo_input, 'segm_man2.nii.gz')

assert os.path.exists(pfi_segm_auto), pfi_segm_auto
assert os.path.exists(pfi_segm_man1), pfi_segm_man1
assert os.path.exists(pfi_segm_man2), pfi_segm_man2

# Output:
pfi_segm_auto_divided_taxonomical = jph(pfo_elaborations, 'segm_auto_divided_taxonomical.nii.gz')
pfi_segm_man1_divided_taxonomical = jph(pfo_elaborations, 'segm_man1_divided_taxonomical.nii.gz')
pfi_segm_man2_divided_taxonomical = jph(pfo_elaborations, 'segm_man2_divided_taxonomical.nii.gz')

pfi_pickled_scoring_man1_man2_taxo = jph(pfo_elaborations, 'comparison_man1_man2_taxonomical.pickle')
pfi_pickled_scoring_auto_man1_taxo = jph(pfo_elaborations, 'comparison_auto_man1_taxonomical.pickle')
pfi_pickled_scoring_auto_man2_taxo = jph(pfo_elaborations, 'comparison_auto_man2_taxonomical.pickle')

pfi_pickled_scoring_man1_man2_all = jph(pfo_elaborations, 'comparison_man1_man2_all.pickle')
pfi_pickled_scoring_auto_man1_all = jph(pfo_elaborations, 'comparison_auto_man1_all.pickle')
pfi_pickled_scoring_auto_man2_all = jph(pfo_elaborations, 'comparison_auto_man2_all.pickle')

# output images
pfi_bullseye_man1_man2 = jph(pfo_elaborations, 'bullseye_man1_man2.pdf')
pfi_bullseye_auto_man1 = jph(pfo_elaborations, 'bullseye_auto_man1.pdf')
pfi_bullseye_auto_man2 = jph(pfo_elaborations, 'bullseye_auto_man2.pdf')

# todo
pfi_histogram_man1_man2_taxo = jph(pfo_elaborations, 'histogram_man1_man2_taxo.pdf')
pfi_histogram_auto_man1_taxo = jph(pfo_elaborations, 'histogram_auto_man1_taxo.pdf')
pfi_histogram_auto_man2_taxo = jph(pfo_elaborations, 'histogram_auto_man2_taxo.pdf')

pfi_boxplot_comparison_taxo = jph(pfo_elaborations, 'boxplot_auto_man_taxo.pdf')


pfi_histogram_man1_man2_all = jph(pfo_elaborations, 'histogram_man1_man2_all.pdf')
pfi_histogram_auto_man1_all = jph(pfo_elaborations, 'histogram_auto_man1_all.pdf')
pfi_histogram_auto_man2_all = jph(pfo_elaborations, 'histogram_auto_man2_all.pdf')

pfi_boxplot_comparison_all = jph(pfo_elaborations, 'boxplot_auto_man_all.pdf')
# end todo

# output tables
pfi_table_average_taxo = jph(pfo_elaborations, 'averages_taxo.tex')
pfi_table_std_taxo     = jph(pfo_elaborations, 'std_taxo.taxo')

pfi_table_average_all = jph(pfo_elaborations, 'averages_all.tex')
pfi_table_std_all     = jph(pfo_elaborations, 'std_all.tex')
