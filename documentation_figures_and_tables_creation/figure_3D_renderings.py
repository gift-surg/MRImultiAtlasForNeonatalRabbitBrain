"""
Simply opens ITK-snap with the correctly grouped segmentations and label descriptor to provide th screenshot for
 the 3D surface rendering from a selected model subject from the multi-atlas (1305).
"""
import os
from os.path import join as jph

import numpy as np
import nibabel as nib

from nilabels.tools.image_colors_manipulations.relabeller import assign_all_other_labels_the_same_value
from nilabels.tools.aux_methods.utils_nib import set_new_data

import path_manager


if __name__ == '__main__':
    # --- labels divided by area - macro regions options:

    macro_region_labels = {
        'cerebrum'             : [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                                  17, 18, 19, 20, 21, 22, 25, 26, 27, 28, 31,
                                  32, 43, 44, 45, 46, 47, 48, 53, 54, 55, 56,
                                  69, 70, 71, 72, 75, 76, 77, 78],
        'brainstem_interbrain' : [83, 84, 109, 110, 121],
        'brainstem_midbrain'   : [127, 129, 130, 133, 134, 135, 136, 139, 140,
                                  141, 142, 151, 153],
        'cerebellum'           : [161, 179, 180],
        'ventricular_system'   : [201, 211, 212],
        'fibre_tracts'         : [213, 215, 218, 219, 220, 223, 224, 225, 226,
                                  227, 228, 229, 230, 233, 237, 239, 240, 241,
                                  242, 243, 244, 247, 248, 249, 250, 251, 252,
                                  253, 255]
    }

    macro_region_labels_joints = {
        'cerebrum'             : [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                                  17, 18, 19, 20, 21, 22, 25, 26, 27, 28, 31,
                                  32, 43, 44, 45, 46, 47, 48, 53, 54, 55, 56,
                                  69, 70, 71, 72, 75, 76, 77, 78],
        'brainstem_interbrain_brainstem_midbrain_cerebellum' : [83, 84, 109, 110, 121] +
                                                               [127, 129, 130, 133, 134, 135, 136, 139, 140,
                                                                141, 142, 151, 153] + [161, 179, 180],
        'ventricular_system_fibre_tracts'   : [201, 211, 212] + [213, 215, 218, 219, 220, 223, 224, 225, 226,
                                                                 227, 228, 229, 230, 233, 237, 239, 240, 241,
                                                                 242, 243, 244, 247, 248, 249, 250, 251, 252,
                                                                 253, 255]
    }

    macro_region_labels_joints_side_only = {
        'cerebrum_left'             : [5, 7, 9, 11, 13, 15, 17, 19, 21, 25, 27, 31, 32, 43, 45, 47, 53, 55,
                                       69, 71, 75, 77],
        'brainstem_interbrain_brainstem_midbrain_cerebellum_left' : [83, 109, 121] +
                                                               [127, 129, 133, 135, 139, 141, 151, 153] + [161, 179],
        'ventricular_system_fibre_tracts_left'   : [201, 211] + [213, 215, 219, 223, 225, 227, 229, 233, 237, 239, 241,
                                                                 243, 247, 249, 250, 251, 253, 255]
    }

    # OK - the chosen one
    macro_region_labels_for_ptb = {
        'ptb_regions'             : [179, 180, 83, 84, 31, 32, 223, 224, 69, 70, 218, 215],
        'cerebrum_left'             : [5, 7, 9, 11, 13, 15, 17, 19, 21, 25, 27, 31, 32, 43, 45, 47, 55, 77],
        'fibre_tracts'   : [215, 218, 225, 226, 229, 230, 233, 249, 250, 253, 255]
    }

    # Images input

    pfo_template = path_manager.pfo_multi_atlas

    atlas_name_model = '1305'

    pfi_input_anatomy = jph(path_manager.pfo_multi_atlas, atlas_name_model, 'mod', '{}_T1.nii.gz'.format(atlas_name_model))
    pfi_input_segmentation = jph(path_manager.pfo_multi_atlas, atlas_name_model, 'segm', '{}_segm.nii.gz'.format(atlas_name_model))
    os.path.exists(pfi_input_anatomy)
    os.path.exists(pfi_input_segmentation)

    # Controller

    compute = False  # if False only visualisation.

    # generate output folder

    os.system('mkdir -p {}'.format(path_manager.pfo_root_for_images))

    # Start elaborations:

    im_segm = nib.load(pfi_input_segmentation)
    labels_in_image = list(np.sort(list(set(im_segm.get_data().astype(np.int).flat))))

    print labels_in_image

    for mr_key in macro_region_labels_for_ptb.keys():

        pfi_macro_region_output = jph(path_manager.pfo_root_for_images,
                                      '{0}_approved_macro_region_{1}.nii.gz'.format(atlas_name_model, mr_key))

        if compute:
            new_data = assign_all_other_labels_the_same_value(im_segm.get_data(),
                                                              labels_to_keep=macro_region_labels_for_ptb[mr_key],
                                                              same_value_label=255)
            new_im_segm = set_new_data(im_segm, new_data)
            nib.save(new_im_segm, pfi_macro_region_output)

        cmd = 'itksnap -g {0} -s {1} -l {2}'.format(pfi_input_anatomy,
                                                    pfi_macro_region_output,
                                                    path_manager.pfi_labels_descriptor)
        os.system(cmd)

