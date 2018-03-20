"""
ITK-snap based software to automatise the opening of the atlas elements.
"""
import os
from os.path import join as jph

import path_manager


def open_sesame(sj_name, pfo_folder_data=path_manager.pfo_multi_atlas, outside_folder_segm=path_manager.pfo_tmp,
                pfi_label_descriptor=path_manager.pfi_labels_descriptor):
    pfi_T1 = jph(pfo_folder_data, sj_name, 'mod', '{}_T1.nii.gz'.format(sj_name))
    pfi_S0 = jph(pfo_folder_data, sj_name, 'mod', '{}_S0.nii.gz'.format(sj_name))
    pfi_FA = jph(pfo_folder_data, sj_name, 'mod', '{}_FA.nii.gz'.format(sj_name))
    pfi_MD = jph(pfo_folder_data, sj_name, 'mod', '{}_MD.nii.gz'.format(sj_name))
    pfi_V1 = jph(pfo_folder_data, sj_name, 'mod', '{}_V1.nii.gz'.format(sj_name))
    pfi_segm = jph(pfo_folder_data, sj_name, 'segm', '{}_approved.nii.gz'.format(sj_name))
    if not os.path.exists(pfi_segm) and outside_folder_segm is not None:
        pfi_segm = jph(outside_folder_segm, '{}_segm.nii.gz'.format(sj_name))
    if not os.path.exists(pfi_segm):
        pfi_segm = None

    cmd = 'itksnap -g {0} -o {1} {2} {3} {4} '.format(pfi_T1, pfi_S0, pfi_FA, pfi_MD, pfi_V1)  # {2} {3} {4}
    if pfi_segm is not None:
        cmd += ' -s {0} '.format(pfi_segm)
        if pfi_label_descriptor is not None:
            cmd += ' -l {0} '.format(pfi_label_descriptor)
    os.system(cmd)


def open_sesame_list(subjects_list, pfo_folder_data=path_manager.pfo_multi_atlas,
                     outside_folder_segm=path_manager.pfo_tmp,
                     pfi_label_descriptor=path_manager.pfi_labels_descriptor):
    for sj in subjects_list:
        open_sesame(sj, pfo_folder_data=pfo_folder_data, outside_folder_segm=outside_folder_segm,
                    pfi_label_descriptor=pfi_label_descriptor)


def open_all_T1_with_semg(sj_name_list, pfo_folder_data=path_manager.pfo_multi_atlas):
    for sj in sj_name_list:
        pfi_T1 = jph(pfo_folder_data, sj, 'mod', '{}_T1.nii.gz'.format(sj))
        pfi_segm = jph(pfo_folder_data, sj, 'segm', '_{}_approved.nii.gz'.format(sj))
        pfi_label_descriptor = jph(pfo_folder_data, 'labels_descriptor.txt')

        cmd = 'itksnap -g {0} '.format(pfi_T1)
        if os.path.exists(pfi_segm):
            cmd += ' -s {0} '.format(pfi_segm)
        if os.path.exists(pfi_label_descriptor):
            cmd += ' -l {0} '.format(pfi_label_descriptor)
        os.system(cmd)


def open_all_same_mod_in_block(sj_name_list, mod='T1', pfo_folder_data=path_manager.pfo_multi_atlas):
    pfi_mod_1 = jph(pfo_folder_data, sj_name_list[0], 'mod', '{0}_{1}.nii.gz'.format(sj_name_list[0], mod))
    cmd = 'itksnap -g {0} '.format(pfi_mod_1)
    if len(sj_name_list) > 1:
        cmd += ' -o '
        for sj in sj_name_list[1:]:
            cmd += ' {} '.format(jph(pfo_folder_data, sj, 'mod', '{0}_{1}.nii.gz'.format(sj, mod)))
    print cmd
    os.system(cmd)


if __name__ == '__main__':
    # open_sesame_list(['1203'])
    # open_sesame_list(['1201', '1203', '1305'])
    # open_sesame_list(['1404', '1507', '1510', ])
    # open_sesame_list(['1702', '1805', '2002', '2502'])
    # open_sesame_list(['3301'])

    # open_all_T1_with_semg(['1201', '1203', '1305', '1404', '1507', '1510', '1702', '1805', '2002', '2502'])
    open_all_same_mod_in_block(['1201', '1203', '1305', '1404', '1507', '1510', '1702',
                                '1805', '2002', '2502', '3301', '3404'])
