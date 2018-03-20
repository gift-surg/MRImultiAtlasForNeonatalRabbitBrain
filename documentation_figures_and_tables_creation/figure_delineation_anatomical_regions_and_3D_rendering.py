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
import copy

from LABelsToolkit.tools.aux_methods.utils_nib import set_new_data
from LABelsToolkit.tools.aux_methods.utils import print_and_run
from LABelsToolkit.main import LABelsToolkit as LabT

import path_manager


def exploded_segmentation(im_segm, direction, intercepts, offset, dtype=np.int):
    """
    Damien Hirst like sectioning of an anatomical segmentation.
    :param im_segm: nibabel image segmentation
    :param direction: sectioning direction, can be sagittal, axial or coronal
    (conventional names for images oriented to standard (diagonal affine transformation))
    :param intercepts: list of values of the stack plane in the input segmentation.
    Needs to include the max plane and the min plane
    :param offset: voxel to leave empty between one slice and the other
    :return: nibabel image output as sectioning of the input one.
    """
    if direction.lower() == 'axial':
        block = np.zeros([im_segm.shape[0], im_segm.shape[1], offset]).astype(dtype)
        stack = []
        for j in range(1, len(intercepts)):
            stack += [im_segm.get_data()[:, :, intercepts[j-1]:intercepts[j]].astype(dtype)] + [block]
        return set_new_data(im_segm, np.concatenate(stack, axis=2))

    elif direction.lower() == 'sagittal':
        block = np.zeros([offset, im_segm.shape[1], im_segm.shape[2]]).astype(dtype)
        stack = []
        for j in range(1, len(intercepts)):
            stack += [im_segm.get_data()[intercepts[j - 1]:intercepts[j], :, :].astype(dtype)] + [block]
        return set_new_data(im_segm, np.concatenate(stack, axis=0))

    elif direction.lower() == 'coronal':
        block = np.zeros([im_segm.shape[0], offset, im_segm.shape[2]]).astype(dtype)
        stack = []
        for j in range(1, len(intercepts)):
            stack += [im_segm.get_data()[:, intercepts[j - 1]:intercepts[j], :].astype(dtype)] + [block]
        for st in stack:
            print st.shape
        return set_new_data(im_segm, np.concatenate(stack, axis=1))

    else:
        raise IOError


def create_cuts_on_segmentation(im_segm, direction, intercepts, offset, dtype=np.int, cuts_label=0):
    """
    Slices of the input segmentation are substituted with black lines.
    :param im_segm:
    :param direction:
    :param intercepts:
    :param offset:
    :param dtype:
    :return:
    """
    new_data = copy.deepcopy(im_segm.get_data())
    where_segmentation = im_segm.get_data() > 0
    where_segmentation = where_segmentation.astype(np.int) * cuts_label

    if direction.lower() == 'axial':
        for j in range(1, len(intercepts) - 1):
            new_data[:, :, intercepts[j]:intercepts[j]+offset] = \
                where_segmentation[:, :, intercepts[j]:intercepts[j]+offset]

    elif direction.lower() == 'sagittal':
        for j in range(1, len(intercepts)):
            new_data[intercepts[j]:intercepts[j]+offset, :, :] = \
                where_segmentation[intercepts[j]:intercepts[j]+offset, :, :]

    elif direction.lower() == 'coronal':
        for j in range(1, len(intercepts)):
            print j
            new_data[:, intercepts[j]:intercepts[j]+offset, :] = \
                where_segmentation[:, intercepts[j]:intercepts[j]+offset, :]

    else:
        raise IOError

    return set_new_data(im_segm, new_data)


def segmentation_disjoint_union(im_segm1, im_segm2):

    assert im_segm1.shape == im_segm2.shape
    where_segmentation_1 = im_segm1.get_data() > 0
    where_segmentation_2 = im_segm2.get_data() > 0
    where_segmentation_1_and_2 = where_segmentation_1 * where_segmentation_2

    new_data = copy.deepcopy(im_segm1.get_data())

    new_data = new_data * np.logical_not(where_segmentation_1_and_2).astype(np.int)
    new_data = new_data + im_segm2.get_data()
    return set_new_data(im_segm1, new_data)


def get_zebra_midplane(im_segm, direction, intercepts, offset, foreground=0, background=254):

    midplane = np.zeros_like(im_segm.get_data())
    if direction.lower() == 'axial':
        midplane[int(midplane.shape[0]/2), :, :] = background * np.ones_like(midplane[int(midplane.shape[0]/2), :, :])
        for j in range(1, len(intercepts) - 1):
            midplane[int(midplane.shape[0]/2), :, intercepts[j]:intercepts[j]+offset] = \
                foreground * np.ones_like(midplane[int(midplane.shape[0]/2), :, intercepts[j]:intercepts[j]+offset])

    elif direction.lower() == 'sagittal':
        midplane[:, int(midplane.shape[1]/2), :] = background * np.ones_like(midplane[:, int(midplane.shape[1]/2), :])
        for j in range(1, len(intercepts) - 1):
            midplane[intercepts[j]:intercepts[j] + offset, int(midplane.shape[1]/2), :] = \
                foreground * np.ones_like(midplane[intercepts[j]:intercepts[j] + offset, int(midplane.shape[1]/2), :])

    elif direction.lower() == 'coronal':
        midplane[int(midplane.shape[0]/2), :, :] = background * np.ones_like(midplane[int(midplane.shape[0]/2), :, :])
        for j in range(1, len(intercepts) - 1):
            midplane[int(midplane.shape[0]/2), intercepts[j]:intercepts[j]+offset, :] = \
                foreground * np.ones_like(midplane[int(midplane.shape[0]/2), intercepts[j]:intercepts[j]+offset, :])
    else:
        raise IOError

    return set_new_data(im_segm, midplane)


if __name__ == '__main__':

    atlas_name_model = '1305'

    # Create a copy of the model in the local image folder
    pfi_original_T1 = jph(path_manager.pfo_multi_atlas, atlas_name_model, 'mod', '{}_T1.nii.gz'.format(atlas_name_model))
    pfi_original_segm = jph(path_manager.pfo_multi_atlas, atlas_name_model, 'segm', '{}_segm.nii.gz'.format(atlas_name_model))

    pfi_model_T1   = jph(path_manager.pfo_root_for_images, '{}_T1.nii.gz'.format(atlas_name_model))
    pfi_model_segm = jph(path_manager.pfo_root_for_images, '{}_segm.nii.gz'.format(atlas_name_model))

    print_and_run('cp {} {}'.format(pfi_original_T1, pfi_model_T1))
    print_and_run('cp {} {}'.format(pfi_original_segm, pfi_model_segm))

    pfi_output_contour_coronal = jph(path_manager.pfo_root_for_images, '{}_contour_coronal.nii.gz'.format(atlas_name_model))

    # initial 15:
    # coronal_coordinates = [88, 106, 117, 130, 151, 162, 172, 185, 197, 212, 228, 247, 266, 279, 306]
    # selected 6 out of the 15:
    # coronal_coordinates = [106, 130, 162, 197, 231, 279]

    coronal_coordinates = [98, 132, 166, 198, 230, 262]
    print len(coronal_coordinates)

    im_segm = nib.load(pfi_model_segm)

    create = True
    get_divided = False

    # get the planes halfed:
    pfi_output_slicing_planes_halfed = jph(path_manager.pfo_root_for_images, '{}_slicing_planes_halfed.nii.gz'.format(atlas_name_model))

    vol_slices = np.zeros_like(im_segm.get_data())
    for c in coronal_coordinates:
        vol_slices[159:, c, :] = np.ones_like(vol_slices[159:, c, :])

    im_slices = set_new_data(im_segm, vol_slices)
    nib.save(im_slices, pfi_output_slicing_planes_halfed)

    # get the space halfed:
    pfi_output_slicing_volume_halfed = jph(path_manager.pfo_root_for_images, '{}_slicing_volume_halfed.nii.gz'.format(atlas_name_model))

    vol_halfed = np.zeros_like(im_segm.get_data())
    vol_halfed[159:, :, :] = np.ones_like(vol_halfed[159:, :, :])

    im_halfed = set_new_data(im_segm, vol_halfed)
    nib.save(im_halfed, pfi_output_slicing_volume_halfed)

    print('Get the contour of the segmentation')
    if create:
        lt = LabT()
        lt.manipulate_intensities.get_contour_from_segmentation(pfi_model_segm, pfi_output_contour_coronal,
                                                                omit_axis='y', verbose=1)

    print('Get half_intersections = get the planes halfed intersection with binarised parcellation')
    pfi_binarised_parcellation = jph(path_manager.pfo_root_for_images, 'binarised_parcellation.nii.gz')
    pfi_half_intersections = jph(path_manager.pfo_root_for_images, 'half_plane_intesection_parcellation.nii.gz')
    print_and_run('seg_maths {0} -bin {1}'.format(pfi_model_segm, pfi_binarised_parcellation), safety_on=not create)
    print_and_run('seg_maths {0} -mul {1} {2}'.format(pfi_binarised_parcellation, pfi_output_slicing_planes_halfed, pfi_half_intersections), safety_on=not create)

    print('Get halfed_slice_holder = get the whole parcellation minus the half_intersection')
    pfi_halfed_slice_holder = jph(path_manager.pfo_root_for_images, 'halfed_slice_holder.nii.gz')
    print_and_run('seg_maths {0} -sub {1} {2}'.format(pfi_binarised_parcellation, pfi_half_intersections, pfi_halfed_slice_holder), safety_on=not create)

    print('Set half_slice_holder to label equals to 255')
    print_and_run('seg_maths {0} -mul {1} {0}'.format(pfi_halfed_slice_holder, 255), safety_on=not create)

    print('Get halfed_slices = get the halfed slices as intersection between the half_intersections and the parcellations')
    pfi_halfed_slices = jph(path_manager.pfo_root_for_images, 'halfed_slices.nii.gz')
    print_and_run('seg_maths {0} -mul {1} {2}'.format(pfi_half_intersections, pfi_model_segm, pfi_halfed_slices), safety_on=not create)

    print('Get half_sliced_3d_view = combine halfed_slice_holder with halfed_slices in the final half_sliced_3d_view')
    pfi_half_sliced_3d_view = jph(path_manager.pfo_root_for_images, 'half_sliced_3d_view.nii.gz')
    print_and_run('seg_maths {0} -add {1} {2}'.format(pfi_halfed_slice_holder, pfi_halfed_slices, pfi_half_sliced_3d_view), safety_on=not create)

    if get_divided:
        print('OPTIONAL: divide left and right hemispheres of half_sliced_3d_view in left and right')
        pfi_right_hem_binarised_parcellation = jph(path_manager.pfo_root_for_images, 'right_hem_binarised_parcellation.nii.gz')
        print_and_run('seg_maths {0} -mul {1} {2}'.format(pfi_binarised_parcellation, pfi_output_slicing_volume_halfed, pfi_right_hem_binarised_parcellation), safety_on=not create)

        pfi_left_hem_binarised_parcellation = jph(path_manager.pfo_root_for_images, 'left_hem_binarised_parcellation.nii.gz')
        print_and_run('seg_maths {0} -sub {1} {2}'.format(pfi_binarised_parcellation, pfi_right_hem_binarised_parcellation, pfi_left_hem_binarised_parcellation), safety_on=not create)

        print_and_run('seg_maths {0} -sub {1} {2}'.format(pfi_half_sliced_3d_view, pfi_left_hem_binarised_parcellation, pfi_half_sliced_3d_view), safety_on=not create)

    # print them out:
    cmd0 = 'itksnap -g {0} -s {1} -l {2}'.format(pfi_model_T1, pfi_output_slicing_planes_halfed, path_manager.pfi_labels_descriptor)
    os.system(cmd0)

    cmd1 = 'itksnap -g {0} -s {1} -l {2}'.format(pfi_model_T1, pfi_output_contour_coronal, path_manager.pfi_labels_descriptor)
    os.system(cmd1)

    cmd1 = 'itksnap -g {0} -s {1} -l {2}'.format(pfi_model_T1, pfi_half_sliced_3d_view, path_manager.pfi_labels_descriptor)
    os.system(cmd1)
