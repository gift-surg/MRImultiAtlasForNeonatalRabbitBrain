import os
from os.path import join as jph
import nibabel as nib
import numpy as np

from LABelsToolkit.tools.aux_methods.utils import print_and_run
from LABelsToolkit.tools.aux_methods.utils_nib import set_new_data
from LABelsToolkit.tools.detections.contours import contour_from_segmentation
from LABelsToolkit.tools.descriptions.manipulate_descriptors import LabelsDescriptorManager as LdM
from LABelsToolkit.tools.image_colors_manipulations.relabeller import relabeller

import path_manager


def binarise_and_adjust_mask_from_segmentation_path(pfi_segm_input, pfi_mask_output, pfo_temp, subject_name, labels_to_exclude=()):
    """
    Sequence of topological operation to pass from the manual segmentation to a single binary mask
    covering the brain tissue and excluding the skull.
    :param pfi_segm_input:
    :param pfi_mask_output:
    :param pfo_temp:
    :param subject_name:
    :param labels_to_exclude:
    :return:
    """
    pfi_intermediate = jph(pfo_temp, '{}_tmp_binarisation.nii.gz'.format(subject_name))

    print_and_run('cp {} {}'.format(pfi_segm_input, pfi_intermediate))

    if len(labels_to_exclude) > 0 :

        im_segm = nib.load(pfi_intermediate)
        array_segm_new_data = relabeller(im_segm.get_data(), list_old_labels=labels_to_exclude,
                                         list_new_labels=[0, ] * len(labels_to_exclude))
        im_segm_new = set_new_data(im_segm, array_segm_new_data)
        nib.save(im_segm_new, pfi_intermediate)

    print_and_run('seg_maths {0} -bin {0}'.format(pfi_intermediate))

    # fill and dil the binarised segmentation
    print_and_run('seg_maths {0} -fill {1}'.format(pfi_intermediate, pfi_intermediate))
    print_and_run('seg_maths {0} -dil 1 {0}'.format(pfi_intermediate))
    print_and_run('seg_maths {0} -ero 1 {0}'.format(pfi_intermediate))
    print_and_run('seg_maths {0} -fill {0}'.format(pfi_intermediate))

    print_and_run('seg_maths {0} -fill {1}'.format(pfi_intermediate, pfi_mask_output))
    # print_and_run('seg_maths {0} -smol 1.5 {0}'.format(pfi_mask_output))


def prepare_mask_eroded_contour_from_segmentation_path(pfi_segm_input, pfi_segm_output, pfo_temp, verbose=1):
    """
    Segmentation preparation for the bimodal probabilistic atlas generator.
    Segmentation is subtracted by its contour, binarised, eroded by 1 and then a gaussian filter is applied.
    :param pfi_segm_input:
    :param pfi_segm_output:
    :param pfo_temp:
    :param verbose:
    :return:
    """
    im_input = nib.load(pfi_segm_input)
    im_contour = contour_from_segmentation(im_input, verbose=verbose)
    im_1 = set_new_data(im_input, im_input.get_data() - im_contour.get_data())
    nib.save(im_1, pfo_temp)
    cmd = 'seg_maths {0} -bin {0}'.format(pfo_temp)
    os.system(cmd)
    # cmd = 'seg_maths {0} -ero 0.8 {0} -odt float'.format(pfi_tmp)
    # os.system(cmd)
    cmd = 'seg_maths {0} -smo 1 {1}'.format(pfo_temp, pfi_segm_output)
    os.system(cmd)


def cluster_access_commands(username='ferraris@comic100.cs.ucl.ac.uk', command='to_cluster'):
    """
    Copy to or from cluster
    :param username:
    :param command: can be 'to_cluster' or 'from_cluster'
    :return:
    """
    root_probabilistic_atlas_cluster = jph(path_manager.pfo_root, 'A_probabilistic_atlas_on_cluster')
    if command == 'to_cluster':
        # copy folders Atlas to cluster
        cmd = 'scp -r {0} {1}:{2}'.format(path_manager.pfo_root_probabilistic_atlas, username,
                                                                     root_probabilistic_atlas_cluster)
        print_and_run(cmd)
    elif command == 'from_cluster':
        cmd = 'scp -r {0}:{1} {2} '.format(username,
            jph(root_probabilistic_atlas_cluster, 'groupwise_result'),
            jph(path_manager.pfo_root_probabilistic_atlas, 'groupwise_result'))
        print_and_run(cmd)
    else:
        raise IOError


def run_probabilistic_atlas_generator(commands, options):

    # Atlas data (input) - only the atlas, the label descriptor
    leading_modality = 'T1'
    pfi_labels_descriptor = jph(path_manager.pfo_multi_atlas, 'labels_descriptor.txt')

    # Probabilistic Atlas output
    if options['Bimodal']:
        pfo_subjects = jph(path_manager.pfo_root_probabilistic_atlas, 'subjects_bimodal')
        pfo_masks = jph(path_manager.pfo_root_probabilistic_atlas, 'masks_bimodal')
    else:
        pfo_subjects = jph(path_manager.pfo_root_probabilistic_atlas, 'subjects')
        pfo_masks = jph(path_manager.pfo_root_probabilistic_atlas, 'masks')

    pfo_all_segmentations = jph(path_manager.pfo_root_probabilistic_atlas, 'all_segm')
    pfo_tmp = jph(path_manager.pfo_root_probabilistic_atlas, 'z_tmp')
    pfo_pa_results = jph(path_manager.pfo_root_probabilistic_atlas, 'a_results')  # most important

    # --- Main folder probabilistic atlas:
    print_and_run('mkdir {}'.format(path_manager.pfo_root_probabilistic_atlas))

    if commands['Create_structure']:

        for p in [pfo_subjects, pfo_masks, pfo_all_segmentations, pfo_pa_results, pfo_tmp]:
            print_and_run('mkdir -p {}'.format(p))

    # prepare folders structure and folder segmentations
    if commands['Prepare_data_in_folder_structure']:
        assert os.path.exists(pfo_all_segmentations)
        assert os.path.exists(pfo_tmp)

        for sj in path_manager.atlas_subjects:
            pfi_leading_mod = jph(path_manager.pfo_multi_atlas, sj, 'mod', '{0}_{1}.nii.gz'.format(sj, leading_modality))
            pfi_segm = jph(path_manager.pfo_multi_atlas, sj, 'segm', '{0}_segm.nii.gz'.format(sj))

            assert os.path.exists(pfi_leading_mod), pfi_leading_mod
            assert os.path.exists(pfi_segm), pfi_segm

            # ---- SEGMENTATION - just copy in the adequate folder ---
            pfi_segm_for_p_atlas = jph(pfo_all_segmentations, '{0}_segm.nii.gz'.format(sj))
            print_and_run('cp {0} {1}'.format(pfi_segm, pfi_segm_for_p_atlas))

            # ---- MASK AS BINARISED SEGMENTATION ---
            pfi_brain_mask = jph(pfo_tmp, '{0}_brain_tissue.nii.gz'.format(sj))
            binarise_and_adjust_mask_from_segmentation_path(pfi_segm_input=pfi_segm_for_p_atlas,
                                                            pfi_mask_output=pfi_brain_mask,
                                                            pfo_temp=pfo_tmp, subject_name=sj, labels_to_exclude=[201, ])

            # copy the obtained mask in the final masks folder, ready to create the probabilistic atlas.
            pfi_brain_mask_for_p_atlas = jph(pfo_masks, '{0}_mask.nii.gz'.format(sj))
            print_and_run('cp {0} {1}'.format(pfi_brain_mask, pfi_brain_mask_for_p_atlas))

            # ---- MAIN MODALITY ---

            # Trim:
            pfi_leading_mod_trimmed = jph(pfo_tmp, '{0}_{1}_trimmed.nii.gz'.format(sj, leading_modality))
            print_and_run('seg_maths {0} -mul {1} {2}'.format(pfi_leading_mod, pfi_brain_mask_for_p_atlas, pfi_leading_mod_trimmed))

            if options['Bimodal']:
                # prepare segmentation to be set in the second channel
                pfi_segm_prepared_for_second_channel = jph(pfo_tmp, '{}_segm_giraffe_skin.nii.gz'.format(sj))
                prepare_mask_eroded_contour_from_segmentation_path(pfi_segm_for_p_atlas, pfi_segm_prepared_for_second_channel, pfo_tmp)

                # create stack mask and copy in the final folder: - will overwrite pfi_brain_mask_for_p_atlas
                pfi_stack_mask = jph(pfo_masks, '{0}_mask.nii.gz'.format(sj))  # maks bimodal -  will overwrite pfi_brain_mask_for_p_atlas
                cmd = 'seg_maths {0} -merge 1 4 {1} {2}'.format(pfi_brain_mask_for_p_atlas, pfi_brain_mask_for_p_atlas, pfi_stack_mask)
                print_and_run(cmd)

                # create stack modalities and copy in the final folder:
                pfi_stack_T1 = jph(pfo_subjects, '{}_bimodal.nii.gz'.format(sj))  # pfo_subject_bimodal
                cmd = 'seg_maths {0} -merge 1 4 {1} {2}'.format(pfi_leading_mod_trimmed, pfi_segm_prepared_for_second_channel, pfi_stack_T1)
                print_and_run(cmd)

            else:
                pfi_leading_mod_final = jph(pfo_subjects, '{0}_{1}.nii.gz'.format(sj, leading_modality))
                print_and_run('cp {0} {1}'.format(pfi_leading_mod_trimmed, pfi_leading_mod_final))
                pass

    if commands['Create_probabilistic_atlas']:
        here = os.path.dirname(os.path.realpath(__file__))

        pfi_niftiyreg_run = jph(here, 'local_groupwise_niftyreg_run.sh')
        if options['Bimodal']:
            pfi_niftiyreg_param = jph(here, 'local_groupwise_niftyreg_params_bimodal.sh')
            cmd = 'cd {0}; ./groupwise_niftyreg_run.sh groupwise_niftyreg_params_bimodal.sh; cd {1}'.format(
                path_manager.pfo_root_probabilistic_atlas, here)
        else:
            pfi_niftiyreg_param = jph(here, 'local_groupwise_niftyreg_params.sh')
            cmd = 'cd {0}; ./groupwise_niftyreg_run.sh groupwise_niftyreg_params.sh; cd {1}'.format(
                path_manager.pfo_root_probabilistic_atlas, here)

        print_and_run('cp {0} {1}'.format(pfi_niftiyreg_run,
                                          jph(path_manager.pfo_root_probabilistic_atlas, 'groupwise_niftyreg_run.sh')))
        if options['Bimodal']:
            print_and_run('cp {0} {1}'.format(pfi_niftiyreg_param,
                                              jph(path_manager.pfo_root_probabilistic_atlas, 'groupwise_niftyreg_params_bimodal.sh')))
        else:
            print_and_run('cp {0} {1}'.format(pfi_niftiyreg_param,
                                              jph(path_manager.pfo_root_probabilistic_atlas, 'groupwise_niftyreg_params.sh')))

        print_and_run(cmd)

    # Apply transformations obtained to create the probabilistic atlas global mask and average the results:
    if commands['Warp_anatomical']:
        # IMPORTANT!! This must be manually set and coherent with the content of the .sh params files
        # --- parameters:

        # number of affine loop to perform [for the paper 7]
        AFF_IT_NUM = 7
        # number of non-rigid loop to perform [for the paper 7]
        NRR_IT_NUM = 7

        if options['Bimodal']:
            results_folder = 'results_bimodal'
            subjects_folder = 'subjects_bimodal'
            masks_folder = 'masks_bimodal'
            mod_suffix = 'bimodal'
        else:
            results_folder = 'results'
            subjects_folder = 'subjects'
            masks_folder = 'masks'
            mod_suffix = 'T1'
        # suffix according to the study number (should indicate number of iterations and mono/multi)
        suffix_result = 'aff{0}nrig{1}'.format(AFF_IT_NUM, NRR_IT_NUM)

        # ---- pipeline:
        # copy and rename the results of the groupwise registration
        pfi_result_groupwise = jph(path_manager.pfo_root_probabilistic_atlas, results_folder,
                                   'nrr_{}'.format(NRR_IT_NUM),
                                   'average_nonrigid_it_{}.nii.gz'.format(NRR_IT_NUM))
        assert os.path.exists(pfi_result_groupwise), pfi_result_groupwise
        pfi_result_groupwise_copy = jph(pfo_pa_results,
                                        'PA_{0}_{1}.nii.gz'.format(mod_suffix, suffix_result))
        cmd = 'seg_maths {0} -thr 0 {1}'.format(pfi_result_groupwise, pfi_result_groupwise_copy)
        print_and_run(cmd)

        # if multimodal, take only the first timepoint
        if results_folder == 'results_bimodal':
            pfi_result_groupwise_copy_tp1 = jph(pfo_pa_results,
                                            'PA_T1_{0}_{1}_tp1.nii.gz'.format(mod_suffix, suffix_result))

            cmd = 'seg_maths {0} -tp 0 {1}'.format(pfi_result_groupwise_copy, pfi_result_groupwise_copy_tp1)
            print_and_run(cmd)

        # resample each segmentation with the final transformation
        pfi_reference_image = jph(path_manager.pfo_root_probabilistic_atlas, subjects_folder, '1305_{}.nii.gz'.format(mod_suffix))
        assert os.path.exists(pfi_reference_image), pfi_reference_image
        for sj in path_manager.atlas_subjects:

            print sj
            # Resample the segmentations.
            pfi_segmentation_sj = jph(path_manager.pfo_root_probabilistic_atlas, 'all_segm', '{}_segm.nii.gz'.format(sj))
            pfi_sj_final_transformation = jph(path_manager.pfo_root_probabilistic_atlas, results_folder,
                                              'nrr_{}'.format(NRR_IT_NUM),
                                              'nrr_cpp_{0}_{1}_it{2}.nii.gz'.format(sj, mod_suffix, NRR_IT_NUM))
            assert os.path.exists(pfi_segmentation_sj), pfi_segmentation_sj
            assert os.path.exists(pfi_sj_final_transformation), pfi_sj_final_transformation
            pfi_sj_warped_segmentation = jph(pfo_pa_results, 'segm_{0}_warped_on_average_atlas.nii.gz'.format(sj))
            cmd = 'reg_resample -ref {0} -flo {1} -trans {2} -res {3} -inter 0'.format(pfi_reference_image,
                                                                              pfi_segmentation_sj,
                                                                              pfi_sj_final_transformation,
                                                                              pfi_sj_warped_segmentation)
            print_and_run(cmd)

            # Resample the Masks.
            pfi_mask_sj = jph(path_manager.pfo_root_probabilistic_atlas, masks_folder, '{0}_mask.nii.gz'.format(sj))
            assert os.path.exists(pfi_mask_sj), pfi_mask_sj
            pfi_sj_warped_mask = jph(pfo_pa_results, 'mask_{0}_warped_on_average_atlas.nii.gz'.format(sj))
            cmd = 'reg_resample -ref {0} -flo {1} -trans {2} -res {3} -inter 0'.format(pfi_reference_image,
                                                                                       pfi_mask_sj,
                                                                                       pfi_sj_final_transformation,
                                                                                       pfi_sj_warped_mask)
            print_and_run(cmd)

    # ------------------------------------------------------------------------- #
    # Now we have the resulting warped segmentations and the probabilistic T1.
    # We can do some manipulations to have what we need:
    # ------------------------------------------------------------------------- #
    # We can generate an image with the probabilities for each label
    if commands['Create_probability_for_each_level']:

        if options['Bimodal']:
            subjects_folder = 'subjects_bimodal'
            mod_suffix = 'bimodal'
        else:
            subjects_folder = 'subjects'
            mod_suffix = 'T1'

        pfo_probabilities = jph(pfo_pa_results, 'probabilities')
        print_and_run('mkdir -p {}'.format(pfo_probabilities))

        ldm = LdM(pfi_labels_descriptor)
        dict_labels = ldm.get_dict()

        for l in dict_labels.keys():
            print '\nLabel {}'.format(l)
            pfi_prob_finding_label_l = jph(pfo_probabilities, 'prob_label_{}.nii.gz'.format(l))

            # generate new empty data:
            pfi_reference_image = jph(path_manager.pfo_root_probabilistic_atlas, subjects_folder, '1305_{}.nii.gz'.format(mod_suffix))
            assert os.path.exists(pfi_reference_image), pfi_reference_image
            im_ref = nib.load(pfi_reference_image)
            data_label_l = np.zeros_like(im_ref)

            # fill data_label_l with all the labels
            for sj in path_manager.atlas_subjects:
                print 'Subject {}'.format(sj)
                pfi_sj_warped_segmentation = jph(pfo_pa_results, 'segm_{0}_warped_on_average_atlas.nii.gz'.format(sj))
                im_warp_segm_sj = nib.load(pfi_sj_warped_segmentation)
                where_l = im_warp_segm_sj.get_data() == l
                data_label_l = data_label_l + where_l.astype(np.float64)

            # normalise the filled labels:
            m = np.max(data_label_l)
            # in case the label is not present in the segmentation warn the user
            if m > 0:
                data_label_l = data_label_l / float(m)
            else:
                print 'Label {} not present in the segmentations'.format(l)

            im_prob_label_l = set_new_data(im_ref, data_label_l)

            nib.save(im_prob_label_l, pfi_prob_finding_label_l)


if __name__ == '__main__':

    commands_ = {'Create_structure'                   : True,
                 'Prepare_data_in_folder_structure'   : True,
                 'Create_bimodal'                     : True,
                 'Create_probabilistic_atlas'         : True,
                 'Warp_anatomical'                    : True,
                 'Create_probability_for_each_level'  : True}

    options_ = {'Bimodal' : True}

    run_probabilistic_atlas_generator(commands_, options_)
