"""
This module considers the outcomes of the cross validation and separates the results in macro regions (taxonomical
grouping as proposed in documentation, Table 2, see also the python module
./benchmarking.cross_validation.a_parameters.py).
"""
import os
from os.path import join as jph

from nilabel.main import Nilabel as NiL

import path_manager
import benchmarking.cross_validation.a_paths_and_parameters_cross_validation as param
from benchmarking.a_nomenclatures import nomenclature_taxonomical, nomenclature_anatomical


def run_separate_brain_regions(controller):

    # --- loop over subjects id ----

    for sj in path_manager.atlas_subjects:
        pfo_elaborations = jph(path_manager.pfo_atlas_validation_leave_one_out, sj, 'segm', 'elaborations')
        os.system('mkdir -p {}'.format(pfo_elaborations))
        pfi_segm_manual = jph(path_manager.pfo_atlas_validation_leave_one_out, sj, 'segm', '{}_segm.nii.gz'.format(sj))
        assert os.path.exists(pfi_segm_manual), pfi_segm_manual

        if controller['verbose']:
            print '\n\n==================='
            print 'Grouping segmentation according to given subdivision {}'.format(sj)
            print '===================\n'

        # -------------- get the selected nomenclature labels correspondence -----------

        nomenclature_old_labels = []
        nomenclature_new_labels = []

        if controller['Nomenclature'] == 'anatomical':
            nomenclature = nomenclature_anatomical
        elif controller['Nomenclature'] == 'taxonomical':
            nomenclature = nomenclature_taxonomical

        for k in nomenclature.keys():
            nomenclature_old_labels += nomenclature[k][1]
            nomenclature_new_labels += [k] * len(nomenclature[k][1])

        # -------------- create ground segmentation divided by selected nomenclature --------------

        if controller['Divide_manual_segm']:
            pfi_segm_manual_divided_nomenclature = jph(pfo_elaborations, sj +
                                                       '_segm_{}.nii.gz'.format(controller['Nomenclature']))

            if controller['verbose']:
                print '\n==================='
                print '\n\nDivide_manual_segm nomenclature {}, subject {}'.format(controller['Nomenclature'], sj)
                print 'From {0} to {1}'.format(pfi_segm_manual, pfi_segm_manual_divided_nomenclature)
            nil = NiL()
            nil.manipulate_labels.relabel(pfi_segm_manual, pfi_segm_manual_divided_nomenclature,
                                          list_old_labels=nomenclature_old_labels,
                                          list_new_labels=nomenclature_new_labels)

        # -------------- create automatic segmentations divided Taxonomical --------------

        if controller['Divide_automatic_segm']:

            for segm_suffix in param.segm_suffix:
                name_segm = '{0}_{1}_{2}'.format(sj, segm_suffix, param.segm_tag)
                pfi_segm_automatic = jph(path_manager.pfo_atlas_validation_leave_one_out, sj, 'segm', 'automatic',
                                         '{}.nii.gz'.format(name_segm))
                assert os.path.exists(pfi_segm_automatic), pfi_segm_automatic

                pfi_segm_automatic_divided_by_nomenclature = jph(pfo_elaborations,
                                                                 '{}_{}.nii.gz'.format(name_segm,
                                                                                       controller['Nomenclature']))

                if controller['verbose']:
                    print('\n===================')
                    print('\nDivide_automatic_segm nomenclature {}, subject {}'.format(controller['Nomenclature'], sj))
                    print 'From {0} to {1}'.format(pfi_segm_automatic, pfi_segm_automatic_divided_by_nomenclature)
                    nil = NiL()
                    nil.manipulate_labels.relabel(pfi_segm_automatic, pfi_segm_automatic_divided_by_nomenclature,
                                                  list_old_labels=nomenclature_old_labels,
                                                  list_new_labels=nomenclature_new_labels)

if __name__ == '__main__':
    controller_ = {'verbose'               : True,
                   'Nomenclature'          : 'taxonomical',  # 'taxonomical' or 'anatomical'. See ../a_nomenclatures.py
                   'Divide_manual_segm'    : True,
                   'Divide_automatic_segm' : True}

    run_separate_brain_regions(controller_)
