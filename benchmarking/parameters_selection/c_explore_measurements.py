# Collect measurements out of the results of previous step.
import os
import pickle
from collections import OrderedDict
from benchmarking.parameters_selection import a_paths as ph
from os.path import join as jph

import pandas as pd


def exploratory_data_analysis(control):

    pfi_dict_paths_struct = jph(ph.pfo_mutli_atlas_leave_one_out, ph.selected_target, 'segm', 'paths_methods.pickle')

    if control['save_path_structure']:
        pfi_ground_truth = jph(ph.pfo_mutli_atlas_leave_one_out, ph.selected_target, 'segm',
                               '{}_segm.nii.gz'.format(ph.selected_target))

        assert os.path.exists(pfi_ground_truth), pfi_ground_truth

        dict_paths_methods = OrderedDict()

        for tag_suffix in ['Mono', 'Multi']:
            steps_params = ['pr_{0}_{1}'.format(k, n) for n in [5, 7, 9] for k in [5, 7, 10]]
            for met in ['MV'] + ['STAPLE_pr_1'] + steps_params:

                name_method = '{}_{}'.format(met, tag_suffix)
                path_to_method = jph(ph.pfo_mutli_atlas_leave_one_out, ph.selected_target, 'segm',
                                     'automatic{}'.format(tag_suffix),
                                     '{}_{}_CrossValidation{}'.format(ph.selected_target, met, tag_suffix))

                assert os.path.exists(path_to_method)
                dict_paths_methods.update({name_method: path_to_method})

        print(dict_paths_methods)
        pickle.dump(dict_paths_methods, open(pfi_dict_paths_struct, 'w+'))

    if control['collect_data']:
        dict_paths_methods = pickle.load(open(pfi_dict_paths_struct))

        print(dict_paths_methods)

if __name__ == '__main__':
    controller = {'save_path_structure' : True,
                  'collect_data'        : True,
                  'show_graph'          : True}

    exploratory_data_analysis(controller)