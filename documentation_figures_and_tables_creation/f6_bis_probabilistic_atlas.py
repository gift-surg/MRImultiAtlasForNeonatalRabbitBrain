"""
CREATE CONTOUR SEGMENTATIONS:
Each single atlas is aligned in the average space.
> We have the multi atlas and the labels descriptor.
> We have the folder with the segmentations aligned (created with atlas_manager/create_probabilistic_atlas.py)
> We have the T1 in the average space (again created with atlas_manager/create_probabilistic_atlas.py)

< We want to build a big figure with the 12 subjects of the multi atlas in coronal sections + a selection of
regions to be overlayed to the T1.

< We want the probabilistic atlas with the overlayed regions in coloured grayscale, overlayed.

-------
This module is paired with create probabilistic atlas, and should be executed afterwards.
"""

import os
from os.path import join as jph
import numpy as np
import nibabel as nib
from matplotlib import rc
from matplotlib import colors

from matplotlib import pyplot as plt
from scipy.interpolate import splprep, splev

from LABelsToolkit.tools.visualiser.see_volume import see_image_slice_with_a_grid
from LABelsToolkit.main import LABelsToolkit as LM
from LABelsToolkit.tools.aux_methods.utils_nib import set_new_data
from LABelsToolkit.tools.aux_methods.utils_nib import replace_translational_part

from LABelsToolkit.tools.descriptions.manipulate_descriptors import LabelsDescriptorManager as LDM


if __name__ == "__main__":

    # Path manager:

    pfo_atlas = '/Users/sebastiano/Dropbox/RabbitEOP-MRI/study/A_atlas'
    atlas_subjects = ['1201', '1203', '1305', '1404', '1507', '1510', '1702', '1805', '2002', '2502', '3301', '3404']

    pfo_probabilistic_template = '/Volumes/LC/sebastianof/rabbits/A_probabilistic_template'
    pfo_probabilistic_template_results = jph(pfo_probabilistic_template, 'a_prob_atlas_results')

    pfo_tmp = '/Users/sebastiano/Desktop/test_im'

    pfi_labels_descritpor = jph(pfo_atlas, 'labels_descriptor.txt')
    assert os.path.exists(pfi_labels_descritpor)

    pfi_where_to_save_final_figure = '/Users/sebastiano/Dropbox/RabbitEOP-MRI/docs/Atlas_Paper/images/f6_grid_probabilistic/f6_prob_final_v1.pdf'

    # Controller:
    labels_to_keep = [11, 12, 31, 32, 69, 70, 233]

    # Pipeline

    # From segmentations to RGB with the selected labels:
    if True:

        lm = LM()
        ldm = LDM(pfi_labels_descritpor)

        for sj_id in atlas_subjects:
            # input:
            pfi_segmentation = jph('/Volumes/LC/sebastianof/rabbits/A_probabilistic_template/all_segm',
                                   '{}_approved.nii.gz'.format(sj_id))

            pfi_my_labels_segmentation = jph(pfo_tmp, '{}_my_labels.nii.gz'.format(sj_id))
            pfi_rgb_segmentation = jph(pfo_tmp, '{}_rgb.nii.gz'.format(sj_id))

            assert os.path.exists(pfi_segmentation)
            lm.manipulate_labels.assign_all_other_labels_the_same_value(pfi_segmentation, pfi_my_labels_segmentation,
                                                                        labels_to_keep=labels_to_keep,
                                                                        same_value_label=0)

            im_rgb = nib.load(pfi_my_labels_segmentation)
            im_rgb = ldm.get_corresponding_rgb_image(im_rgb, invert_black_white=True)
            nib.save(im_rgb, pfi_rgb_segmentation)

    # Grab the required data and generate the figure
    if True:

        rc('text', usetex=True)
        rc('font', family='serif')
        plt.figure(figsize=(14, 4))
        ax00 = plt.subplot2grid((3, 7), (0, 0))
        ax01 = plt.subplot2grid((3, 7), (0, 1))
        ax02 = plt.subplot2grid((3, 7), (0, 2))
        ax03 = plt.subplot2grid((3, 7), (0, 3))
        ax10 = plt.subplot2grid((3, 7), (1, 0))
        ax11 = plt.subplot2grid((3, 7), (1, 1))
        ax12 = plt.subplot2grid((3, 7), (1, 2))
        ax13 = plt.subplot2grid((3, 7), (1, 3))
        ax20 = plt.subplot2grid((3, 7), (2, 0))
        ax21 = plt.subplot2grid((3, 7), (2, 1))
        ax22 = plt.subplot2grid((3, 7), (2, 2))
        ax23 = plt.subplot2grid((3, 7), (2, 3))

        ax04 = plt.subplot2grid((3, 7), (0, 4), rowspan=3, colspan=3)

        axis_list = [ax00, ax01, ax02, ax03,
                     ax10, ax11, ax12, ax13,
                     ax20, ax21, ax22, ax23]

        axis_quote = 230
        passepartout_x = 40
        passepartout_y = 50

        # ------------------------------------
        # Add each single atlas:
        # ------------------------------------

        for ax, sj_id in zip(axis_list, atlas_subjects):
            print sj_id

            # Get the background image (T1) - skull stripped from the A_probabilistic_template folder.
            pfi_anatomy = jph(pfo_probabilistic_template, 'no_skull', 'subjects', '{}_T1.nii.gz'.format(sj_id))
            im_sj = nib.load(pfi_anatomy)

            data = im_sj.get_data()[:, axis_quote, :].T
            data = data[passepartout_x:-passepartout_x, passepartout_y:-passepartout_y]
            shape = data.shape

            # invert background color of the background T1 image:
            m = np.max(data)
            data_bkg = data == 0
            data[data_bkg] = m

            if sj_id == '3404':
                v_max = 1.300
            else:
                v_max = 2.000
            ax.imshow(data, origin='lower',
                            interpolation='nearest',
                            cmap='gray', vmin=0, vmax=v_max)

            # get segmentation:
            pfi_segmentation_rgb = jph(pfo_tmp, '{}_rgb.nii.gz'.format(sj_id))
            im_seg = nib.load(pfi_segmentation_rgb)

            data_seg = np.stack( [im_seg.get_data()[:, axis_quote, :, j].T for j in range(3)], axis=2).astype(np.uint8)
            data_seg = data_seg[passepartout_x:-passepartout_x, passepartout_y:-passepartout_y, :]
            shape_seg = data_seg.shape

            # get mask where to put the non-labels in transparency (RGBA)
            pfi_my_labels_segmentation = jph(pfo_tmp, '{}_my_labels.nii.gz'.format(sj_id))
            im_my_labels = nib.load(pfi_my_labels_segmentation)
            mask = im_my_labels.get_data().T[:, axis_quote, :] > 1
            mask = mask[passepartout_x:-passepartout_x, passepartout_y:-passepartout_y]

            data_seg_masked = np.dstack([data_seg, (mask).astype(np.uint8) * 255])

            ax.imshow(data_seg_masked, origin='lower', alpha=0.5)

            ax.set_axis_off()

        # ------------------------------------
        # Add the average on the final slot:
        # ------------------------------------

        # Probabilistic average on the background
        pfi_pa = jph(pfo_probabilistic_template_results, 'PA_T1_no_skull_aff10nrig5multi_tp1.nii.gz')

        im_pa = nib.load(pfi_pa)

        data_pa = im_pa.get_data()[:, axis_quote, :].T
        data_pa = data_pa[passepartout_x:-passepartout_x, passepartout_y:-passepartout_y]

        # invert background color of the background T1 image:
        m = np.max(data_pa)
        data_bkg = data_pa < 0.2
        data_pa[data_bkg] = m

        # grid settings:
        epsilon = 10

        shape = im_pa.shape
        voxel_origin = np.array([passepartout_y, axis_quote, passepartout_x-epsilon, 1])
        voxel_x = np.array([shape[0] - passepartout_y, axis_quote, 0, 1])
        voxel_y = np.array([0, axis_quote, shape[2] - passepartout_x, 1])

        affine = im_pa.affine

        pt_origin = affine.dot(voxel_origin)
        pt_x = affine.dot(voxel_x)
        pt_y = affine.dot(voxel_y)

        horizontal_min = pt_origin[0]
        horizontal_max = pt_x[0]
        vertical_min = pt_origin[2]
        vertical_max = pt_y[2]

        extent = [horizontal_min, horizontal_max, vertical_min, vertical_max]

        print voxel_origin
        print voxel_x
        print voxel_y
        print pt_origin
        print pt_x
        print pt_y
        print extent

        # Get the background
        ax04.imshow(data_pa, origin='lower', interpolation='nearest',
                            cmap='gray', vmin=0, vmax=1.600, extent=extent)

        # Foreground overlay for each selected label:
        for l in labels_to_keep:
            # get the data for each label
            pfi_prob_finding_label_l = jph(pfo_probabilistic_template_results, 'probabilities', 'prob_label_{}.nii.gz'.format(l))
            im_prob_l = nib.load(pfi_prob_finding_label_l)
            # get the right section
            data_prob_l = im_prob_l.get_data()[:, axis_quote, :].T
            # get the right passepartout
            data_prob_l = 255 * data_prob_l[passepartout_x:-passepartout_x, passepartout_y:-passepartout_y]
            # use data_prob_l as alpha, fourth channel of the rgb:
            lm = LM()
            ldm = LDM(pfi_labels_descritpor)
            labels_dict = ldm.get_dict()

            # create and combine channels:
            first_three_channels_l = np.dstack([rgb * np.ones_like(data_prob_l).astype(np.uint8)
                                                for rgb in labels_dict[l][0]])

            rgba_data_l = np.dstack([first_three_channels_l, data_prob_l.astype(np.uint8)])

            # show:
            ax04.imshow(rgba_data_l, origin='lower', alpha=0.9, extent=extent)

        # select the grid
        ax04.grid(color='grey', linestyle='-', linewidth=0.5)
        ax04.set_aspect('equal')

        for tick in ax04.xaxis.get_major_ticks():
            tick.label.set_fontsize(8)
        for tick in ax04.yaxis.get_major_ticks():
            tick.label.set_fontsize(8)

        ax04.set_xlabel(r'mm')

        if pfi_where_to_save_final_figure is not None:
            plt.savefig(pfi_where_to_save_final_figure, format='pdf', dpi=200)

        plt.show()
