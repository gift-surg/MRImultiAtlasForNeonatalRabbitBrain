"""
CREATE CONTOUR SEGMENTATIONS:
Images are axial screenshots of the resulting files at coronal coordinates.
https://stackoverflow.com/questions/31464345/fitting-a-closed-curve-to-a-set-of-points
https://stackoverflow.com/questions/42124192/how-to-centre-the-origin-in-the-centre-of-an-imshow-plot
https://stackoverflow.com/questions/6999621/how-to-use-extent-in-matplotlib-pyplot-imshow
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


pfo_atlas = '/Users/sebastiano/Dropbox/RabbitEOP-MRI/study/A_atlas'
atlas_subjects = ['1201', '1203', '1305', '1404', '1507', '1510', '1702', '1805', '2002', '2502']

pfo_probabilistic_template = '/Volumes/sebastianof/rabbits/A_probabilistic_template'

pfo_model = '/Users/sebastiano/Dropbox/RabbitEOP-MRI/docs/Atlas_Paper/images/subject_model'
pfo_resulting_images_folder = '/Users/sebastiano/Dropbox/RabbitEOP-MRI/docs/Atlas_Paper/images/figure_6'

chart_name = '1305'

pfi_input_anatomy = jph(pfo_model, '{}_T1.nii.gz'.format(chart_name))
pfi_input_segmentation = jph(pfo_model, '{}_approved.nii.gz'.format(chart_name))
os.path.exists(pfi_input_anatomy)
os.path.exists(pfi_input_segmentation)

pfi_output_contour = jph(pfo_resulting_images_folder, '{}_contour.nii.gz'.format(chart_name))
pfi_labels_descriptor = jph(pfo_atlas, 'labels_descriptor.txt')


pfo_temporary_template = '/Volumes/sebastianof/rabbits/A_probabilistic_template'
assert os.path.exists(pfo_temporary_template)


# OLD
if False:
    # get sliced image on the coronal coordinates (y)
    coronal_coordinates = [int(a) for a in np.linspace(120, 260, 5)]
    print len(coronal_coordinates)
    pfi_output_slicing_planes = jph(pfo_resulting_images_folder, '{}_slicing_planes.nii.gz'.format(chart_name))

    im_segm = nib.load(pfi_input_segmentation)

    vol_slices = np.zeros_like(im_segm.get_data())
    for c in coronal_coordinates:
        vol_slices[:, c, :] = np.ones_like(vol_slices[:, c, :])

    im_slices = set_new_data(im_segm, vol_slices)
    nib.save(im_slices, pfi_output_slicing_planes)

    cmd0 = 'itksnap -g {0} -s {1} -l {2}'.format(pfi_input_anatomy, pfi_output_slicing_planes, pfi_labels_descriptor)
    os.system(cmd0)

# OLD
if False:
    # open each subject of the atlas/segmentation, with the segmentation itself as its segmentation.
    # Take screenshot of the default zoom to fit view of the Coronal slices according to the selected slices previously
    # obtained. Black screens for the subjects not yet insterted.

    for sj in ['1201', '1203', '1305', '1404', '1507', '1510', '1702', '1805', '2002', '2502']:
        pfi_sj_segm = jph(pfo_temporary_template, sj + '_approved.nii.gz')

        # Set translational part to 0 in case.
        # im_seg = nib.load(pfi_sj_segm)
        # new_im = replace_translational_part(im_seg, np.array([0, 0, 0]))
        # nib.save(new_im, pfi_sj_segm)

        cmd0 = 'itksnap -g {0} -s {1} -l {2}'.format(pfi_sj_segm, pfi_sj_segm, pfi_labels_descriptor)
        os.system(cmd0)

# OK
if True:

    pfi_average_atlas = '/Volumes/sebastianof/rabbits/A_probabilistic_template/a_results/PA_T1_no_skull.nii.gz'

    assert os.path.exists(pfi_average_atlas)

    pfo_where_to_save_results = '/Users/sebastiano/Dropbox/RabbitEOP-MRI/docs/Atlas_Paper/images/f6_grid_probabilistic'
    # pfi_inverted_zeros = '/Volumes/sebastianof/rabbits/A_probabilistic_template/a_results/PA_T1_no_skull_inverted_zeros.nii.gz'
    #
    # im = nib.load(pfi_average_atlas)
    # m = np.max(im.get_data())
    # mask = 2 * (im.get_data() == 0)
    # print mask.shape
    # print mask[150, 150, 150]
    # im_zeros_inverted = set_new_data(im, im.get_data() + mask )
    #
    # nib.save(im_zeros_inverted, pfi_inverted_zeros)

    see_image_slice_with_a_grid(pfi_average_atlas, fig_num=1, axis_quote=('x', 158), vmin=0, vmax=1.5,
                                # pfi_where_to_save=jph(pfo_where_to_save, 'sagittal.pdf'),
                                cmap='gray',
                                )
    plt.show(block=False)
    see_image_slice_with_a_grid(pfi_average_atlas, fig_num=2, axis_quote=('y', 230), vmin=0, vmax=1.5,
                                # pfi_where_to_save=jph(pfo_where_to_save, 'coronal.pdf')
                                )
    plt.show(block=False)
    see_image_slice_with_a_grid(pfi_average_atlas, fig_num=3, axis_quote=('z', 99), vmin=0, vmax=1.5,
                                # pfi_where_to_save=jph(pfo_where_to_save, 'axial.pdf')
                                )
    plt.show()

# OK
if False:
    pfi_average_atlas = '/Volumes/sebastianof/rabbits/A_probabilistic_template/a_results/z_final_res.nii.gz'
    pfi_where_to_save = jph('/Users/sebastiano/Dropbox/RabbitEOP-MRI/docs/Atlas_Paper/images/f6_grid_probabilistic',
                            'axial_ptb_probabilities.pdf')
    see_image_slice_with_a_grid(pfi_average_atlas, fig_num=4, axis_quote=('z', 116), vmin=0, vmax=1.5,
                                pfi_where_to_save=pfi_where_to_save, cmap='gray_r')
    plt.show()