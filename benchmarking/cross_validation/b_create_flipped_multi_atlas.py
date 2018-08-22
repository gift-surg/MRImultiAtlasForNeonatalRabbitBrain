"""
From the multi atlas, it copies the multi atlas in the benchmarking
folder and creates a copy of Right/Left flipped subjects.
"""
import os
import nibabel as nib
from os.path import join as jph

import path_manager

from nilabel.tools.aux_methods.utils_nib import set_new_data
from nilabel.tools.aux_methods.utils import print_and_run
from nilabel.tools.aux_methods.label_descriptor_manager import LabelsDescriptorManager as LdM

from nilabel.main import Nilabel as NiL


def flip_data(in_data, axis='x'):
    msg = 'Input array must be 3 or 4-dimensional.'
    assert not in_data.ndim == 3 or not in_data.ndim == 4, msg

    msg = 'axis variable must be one of the following: {}.'.format(['x', 'y', 'z'])
    assert axis in ['x', 'y', 'z'], msg

    out_data = None

    if in_data.ndim == 3:
        if axis == 'x':
            out_data = in_data[::-1, :, :]
        elif axis == 'y':
            out_data = in_data[:, ::-1, :]
        elif axis == 'z':
            out_data = in_data[:, :, ::-1]
    elif in_data.ndim == 4:
        if axis == 'x':
            out_data = in_data[::-1, :, :, :]
        elif axis == 'y':
            out_data = in_data[:, ::-1, :, :]
        elif axis == 'z':
            out_data = in_data[:, :, ::-1, :]

    return out_data


def flip_left_right_from_path(pfi_im_input, pfi_im_flipped):
    im_input = nib.load(pfi_im_input)
    im_flipped = set_new_data(im_input, flip_data(im_input.get_data(), axis='x'))
    nib.save(im_flipped, pfi_im_flipped)


def flipper(pfo_atlas, atlas_charts_names, sufix_atlas, labels_descriptor):

    for chart in atlas_charts_names:
        print
        print('Flipping chart {}'.format(chart))

        pfo_chart         = jph(pfo_atlas, chart)
        pfo_chart_flipped = jph(pfo_atlas, chart + sufix_atlas)

        cmd = 'cp -r {0} {1}'.format(pfo_chart, pfo_chart_flipped)

        os.system(cmd)

        for root, dirs, files in os.walk(pfo_chart_flipped):
            for name in files:
                if name.endswith(('.nii', '.nii.gz')):
                    name_flipped = name.replace(chart, chart + sufix_atlas)
                    pfi_nii = jph(root, name)
                    pfi_nii_flipped = jph(root, name_flipped)

                    print 'old : {}'.format(pfi_nii)
                    print 'new : {}'.format(pfi_nii_flipped)

                    flip_left_right_from_path(pfi_nii, pfi_nii_flipped)

                    os.system('rm {}'.format(pfi_nii))

                    if '_segm' in name_flipped:
                        # substitute labels left-right:
                        ld_dict = labels_descriptor.get_dict()

                        left_labels = [l for l in ld_dict.keys() if 'left' in ld_dict[l][2].lower()]
                        right_labels = [l + 1 for l in left_labels]

                        lt = NiL()
                        lt.manipulate_labels.relabel(pfi_nii_flipped, pfi_nii_flipped,
                                                     list_old_labels=left_labels + right_labels,
                                                     list_new_labels=right_labels + left_labels)


def run_create_flipped_multi_atlas(phases):

    if phases[1]:
        # Phase 1) copy the atlas in the folder pfo_atlas_validation_leave_one_out
        cmd = 'mkdir {}'.format(path_manager.pfo_atlas_validation_leave_one_out)
        print_and_run(cmd)
        for d in os.listdir(path_manager.pfo_multi_atlas):
            if not d.startswith('.') and not d.startswith('z'):
                cmd = 'cp -r {} {}'.format(jph(path_manager.pfo_multi_atlas, d),
                                           path_manager.pfo_atlas_validation_leave_one_out)
                print cmd
                print_and_run(cmd)

    if phases[2]:
        # Phase 2) Flip the multi-atlas in the same folder.
        print(path_manager.atlas_subjects)
        print(path_manager.pfo_atlas_validation_leave_one_out)
        suffix_atlas = 'flip'

        dlm = LdM(jph(path_manager.pfo_atlas_validation_leave_one_out, 'labels_descriptor.txt'))

        flipper(path_manager.pfo_atlas_validation_leave_one_out, path_manager.atlas_subjects, suffix_atlas, dlm)


if __name__ == '__main__':

    phases_ = {1: True, 2: True}
    run_create_flipped_multi_atlas(phases_)
