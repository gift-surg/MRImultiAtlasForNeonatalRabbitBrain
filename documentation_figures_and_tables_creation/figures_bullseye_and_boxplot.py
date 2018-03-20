import os
from os.path import join as jph

import benchmarking.test_retest_intra_rater.a_paths_intra_rater as ph

import path_manager


if __name__ == '__main__':
    nomenclature = 'taxonomical'
    method = 'MV_CrossValidation'
    pfi_bullseye_cross_validation = jph(path_manager.pfo_data_elaborations_leave_one_out, 'Bullseye_{0}_{1}.pdf'.format(nomenclature, method))

    print('Figure cross validaton')
    print(pfi_bullseye_cross_validation)

    print('Figures intra-rater variability (two manual adjustments compared with the auotmatic)')
    print(ph.pfi_bullseye_man1_man2)
    print(ph.pfi_bullseye_auto_man1)
    print(ph.pfi_bullseye_auto_man2)

    print('Figure intra-rater boxplot')
    print(ph.pfi_boxplot_comparison_taxo)

    for p in [pfi_bullseye_cross_validation, ph.pfi_bullseye_man1_man2, ph.pfi_bullseye_auto_man1,
              ph.pfi_bullseye_auto_man2, ph.pfi_boxplot_comparison_taxo]:
        assert os.path.exists(p), 'Run benchmarking to reproduce the images before running this module. {}'.format(p)
        os.system('open {}'.format(p))
