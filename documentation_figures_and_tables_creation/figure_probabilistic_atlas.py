"""
Overlay the probabilistic segmentation to each of the subjects of the multi-atlas.
This code uses the data created in probabilistic_multi_atlas_creator.py.
"""

import os
from os.path import join as jph
import numpy as np
import nibabel as nib
from matplotlib import rc
from matplotlib import pyplot as plt

import nilabels as nis
from nilabels.tools.aux_methods.label_descriptor_manager import LabelsDescriptorManager as LdM

import path_manager


if __name__ == "__main__":

    # Paths:
    pfo_atlas = path_manager.pfo_multi_atlas

    pfo_probabilistic_template = path_manager.pfo_root_probabilistic_atlas
    pfo_probabilistic_template_results = jph(pfo_probabilistic_template, 'a_results')

    pfi_labels_descritpor = path_manager.pfi_labels_descriptor

    # Sanity test:
    assert os.path.exists(pfo_atlas)
    assert os.path.exists(pfo_probabilistic_template)
    assert os.path.exists(pfo_probabilistic_template_results), 'Run probabilistic_multi_atlas_creator.py first'
    assert os.path.exists(pfi_labels_descritpor)

    pfo_tmp = path_manager.pfo_tmp
    os.system('mkdir -p {}'.format(pfo_tmp))

    # Controller:
    labels_to_keep = [11, 12, 31, 32, 69, 70, 233]

    if True:

        print('From segmentations to RGB with the selected labels:')

        nis_app = nis.App()
        ldm = LdM(pfi_labels_descritpor)

        for sj_id in path_manager.atlas_subjects:

            print('Subject {}'.format(sj_id))

            # Input:
            pfi_segmentation = jph(pfo_probabilistic_template, 'all_segm', '{}_segm.nii.gz'.format(sj_id))
            assert os.path.exists(pfi_segmentation), pfi_segmentation
            # Output
            pfi_my_labels_segmentation = jph(pfo_tmp, '{}_my_labels.nii.gz'.format(sj_id))
            pfi_rgb_segmentation = jph(pfo_tmp, '{}_rgb.nii.gz'.format(sj_id))

            # remove all other labels:
            nis_app.manipulate_labels.assign_all_other_labels_the_same_value(pfi_segmentation, pfi_my_labels_segmentation,
                                                                             labels_to_keep=labels_to_keep,
                                                                             same_value_label=0)
            # Save the selected labels
            im_rgb = nib.load(pfi_my_labels_segmentation)
            im_rgb = ldm.get_corresponding_rgb_image(im_rgb, invert_black_white=True)
            nib.save(im_rgb, pfi_rgb_segmentation)

    if True:

        print('Grab the required data and generate the figure:')

        rc('text', usetex=True)
        rc('font', family='serif')
        plt.figure(figsize=(12, 4))
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
        # Add each single atlas to the figure:
        # ------------------------------------

        for ax, sj_id in zip(axis_list, path_manager.atlas_subjects):

            print('Subject {}'.format(sj_id))

            # Get the background image (T1) - skull stripped from the A_probabilistic_atlas folder.
            if os.path.exists(jph(pfo_probabilistic_template, 'subjects')):
                pfi_anatomy = jph(pfo_probabilistic_template, 'subjects', '{}_T1.nii.gz'.format(sj_id))
                im_sj = nib.load(pfi_anatomy)
                data = im_sj.get_data()[:, axis_quote, :].T
            elif os.path.exists(jph(pfo_probabilistic_template, 'subjects_bimodal')):
                pfi_anatomy = jph(pfo_probabilistic_template, 'subjects_bimodal', '{}_bimodal.nii.gz'.format(sj_id))
                im_sj = nib.load(pfi_anatomy)
                data = im_sj.get_data()[:, axis_quote, :, 0].T
            else:
                raise IOError('Probabilistic atlas folder not found or not correctly filled.')

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

            data_seg = np.stack([im_seg.get_data()[:, axis_quote, :, j].T for j in range(3)], axis=2).astype(np.uint8)
            data_seg = data_seg[passepartout_x:-passepartout_x, passepartout_y:-passepartout_y, :]
            shape_seg = data_seg.shape

            # get mask where to put the non-labels in transparency (RGBA)
            pfi_my_labels_segmentation = jph(pfo_tmp, '{}_my_labels.nii.gz'.format(sj_id))
            im_my_labels = nib.load(pfi_my_labels_segmentation)
            mask = im_my_labels.get_data().T[:, axis_quote, :] > 1
            mask = mask[passepartout_x:-passepartout_x, passepartout_y:-passepartout_y]

            data_seg_masked = np.dstack([data_seg, mask.astype(np.uint8) * 255])

            ax.imshow(data_seg_masked, origin='lower', alpha=0.5)

            ax.set_axis_off()

        # ------------------------------------
        # Add the average on the final slot:
        # ------------------------------------

        # Probabilistic average on the background - Check AFF_IT_NUM and NRR_IT_NUM in probabilistic
        # multi atlas creation corresponds to the one below (default is 7, 7)
        pfi_pa = jph(pfo_probabilistic_template_results, 'PA_T1_bimodal_aff7nrig7_tp1.nii.gz')

        assert os.path.exists(pfi_pa)

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
            # Get the data for each label
            pfi_prob_finding_label_l = jph(pfo_probabilistic_template_results, 'probabilities',
                                           'prob_label_{}.nii.gz'.format(l))
            im_prob_l = nib.load(pfi_prob_finding_label_l)
            # Get the right section
            data_prob_l = im_prob_l.get_data()[:, axis_quote, :].T
            # get the right passepartout
            data_prob_l = 255 * data_prob_l[passepartout_x:-passepartout_x, passepartout_y:-passepartout_y]
            # Use data_prob_l as alpha, fourth channel of the rgb:
            ldm = LdM(pfi_labels_descritpor)
            labels_dict = ldm.get_dict()

            # Create and combine channels:
            first_three_channels_l = np.dstack([rgb * np.ones_like(data_prob_l).astype(np.uint8)
                                                for rgb in labels_dict[l][0]])

            rgba_data_l = np.dstack([first_three_channels_l, data_prob_l.astype(np.uint8)])

            # im-show:
            ax04.imshow(rgba_data_l, origin='lower', alpha=0.9, extent=extent)

        # Select the grid
        ax04.grid(color='grey', linestyle='-', linewidth=0.5)
        ax04.set_aspect('equal')

        for tick in ax04.xaxis.get_major_ticks():
            tick.label.set_fontsize(8)
        for tick in ax04.yaxis.get_major_ticks():
            tick.label.set_fontsize(8)

        ax04.set_xlabel(r'mm')

        plt.tight_layout()

        # Save the figure in the output folder:
        plt.savefig(jph(path_manager.pfo_root_for_images, 'probabilistic_atlas_representation.pdf'),
                    format='pdf', dpi=200)

        plt.show()
