# Collect measurements out of the results of previous step.
import os
import pickle
from collections import OrderedDict
from benchmarking.parameters_selection import a_paths as ph
from os.path import join as jph
from pprint import pprint

from nilabels.tools.caliber import distances as dist
from nilabels.tools.aux_methods.label_descriptor_manager import LabelsDescriptorManager
import nibabel as nib
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D


def exploratory_data_analysis(control):

    # input
    pfi_labels_descriptor = jph(ph.pfo_mutli_atlas_leave_one_out, 'labels_descriptor.txt')
    pfi_ground_truth = jph(ph.pfo_target, 'segm', '{}_segm.nii.gz'.format(ph.selected_target))

    assert os.path.exists(pfi_labels_descriptor), pfi_labels_descriptor
    assert os.path.exists(pfi_ground_truth), pfi_ground_truth

    # output per phase
    pfi_dict_paths_struct = jph(ph.pfo_target, 'segm', 'paths_methods.pickle')
    pfi_data_frame_dice_score = jph(ph.pfo_target, 'segm', 'dice_scores_region_methods.csv')
    pfi_figure_params_selection = jph(ph.pfo_target, 'boxplot_parameter_selection.pdf')

    if control['save_path_structure']:

        dict_paths_methods = OrderedDict()

        steps_params = ['STEPS_pr_{0}_{1}'.format(k, n) for n in [5, 7] for k in [5, 7, 10]]
        for met in ['MV'] + ['STAPLE_pr_1'] + steps_params:
            for tag_suffix in ['Mono', 'Multi']:

                name_method = '{}_{}'.format(met, tag_suffix)
                path_to_method = jph(ph.pfo_target, 'segm', 'automatic{}'.format(tag_suffix),
                                     '{}_{}_CrossValidation{}.nii.gz'.format(ph.selected_target, met, tag_suffix))

                assert os.path.exists(path_to_method), path_to_method
                dict_paths_methods.update({name_method: path_to_method})

        pprint(dict_paths_methods)
        pickle.dump(dict_paths_methods, open(pfi_dict_paths_struct, 'w+'))

    if control['collect_data']:
        print('------------- DATA COLLECTION --------------')

        # input
        dict_paths_methods = pickle.load(open(pfi_dict_paths_struct))
        ldm = LabelsDescriptorManager(pfi_labels_descriptor)  # 218 : [[128, 0, 128], [1.0, 1.0, 1.0], 'Corpus callosum'
        im_ground_segm = nib.load(pfi_ground_truth)

        # output to fill:
        df_dice_scores = pd.DataFrame()

        for met, met_path in dict_paths_methods.items():
            print('---')
            print('\n\nMethod: {}'.format(met))
            im_segm = nib.load(met_path)
            ds = dist.dice_score(im_ground_segm, im_segm,
                                 labels_list=ldm.dict_label_descriptor.keys(),
                                 labels_names=[ldm.dict_label_descriptor[k][-1] for k in ldm.dict_label_descriptor.keys()],
                                 verbose=1)
            df_dice_scores.insert(len(df_dice_scores.columns), met, ds)

        print(df_dice_scores)
        df_dice_scores.to_csv(pfi_data_frame_dice_score)

    if control['show_graph']:
        print('-------------- Showing graph -------------')
        df_dice_scores = pd.read_csv(pfi_data_frame_dice_score, index_col=0)
        dict_paths_methods = pickle.load(open(pfi_dict_paths_struct))

        print(df_dice_scores)

        font_top = {'family': 'serif', 'color': 'darkblue', 'weight': 'normal', 'size': 14}
        font_bl = {'family': 'serif', 'color': 'black', 'weight': 'normal', 'size': 12}
        legend_prop = {'size': 11}

        sns.set_style('darkgrid')

        fig, ax = plt.subplots(figsize=(11, 6.5))
        fig.canvas.set_window_title('boxplot_parameters_selection')

        fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

        bp = ax.boxplot(1 - df_dice_scores.as_matrix(), patch_artist=True, notch=True)

        for xv in [2 * j + 0.5 for j in range(1, 8)]:
            ax.axvline(xv, color='k', linestyle='--', linewidth=0.4)
        ax.set_xticks([2 * j + 1.5 for j in range(8)])
        ax.set_xticklabels(
            [d.replace('_Mono', '').replace('pr_', '').replace('E_1', 'E') for d in dict_paths_methods.keys()[::2]],
            rotation=45, fontdict=font_bl)

        ax.set_title('Segmentation propagation and labels fusion parameters selection', fontdict=font_top)

        ax.set_ylim(0, 0.55)
        ax.set_xlabel('Label fusion methods', fontdict=font_bl, labelpad=5)
        ax.set_ylabel('1 - Dice score', fontdict=font_bl, labelpad=5)

        colors = ['lightgrey', 'lightblue']
        for patch_id, patch in enumerate(bp['boxes']):
            color = colors[patch_id % 2]
            patch.set_facecolor(color)

        legend_elements = [Line2D([0], [0], color='lightgrey', lw=4, label='Mono'),
                           Line2D([0], [0], color='lightblue', lw=4, label='Multi')]
        ax.legend(handles=legend_elements, loc='upper right')

        plt.tight_layout()

        plt.savefig(pfi_figure_params_selection, dpi=150)

        plt.show(block=True)


if __name__ == '__main__':
    controller = {'save_path_structure' : False,
                  'collect_data'        : False,
                  'show_graph'          : True}

    exploratory_data_analysis(controller)