import os
import numpy as np
import nibabel as nib
from os.path import join as jph

from LABelsToolkit.tools.caliber.distances import centroid
from LABelsToolkit.main import LABelsToolkit as LT

from LABelsToolkit.tools.aux_methods.utils_nib import remove_nan, set_new_header_description, set_new_data
from LABelsToolkit.tools.image_colors_manipulations.normaliser import normalise_below_labels


import path_manager

# from labels_manager.tools.manipulations.normaliser import divide_by_median_below_labels_path

'''
Moduel with manual methods to perform small adjustments of various kind (data types, orientation, translation) 
on the existing dataset. DO NOT USE UNLESS VERY SURE!
'''


def adjust_nifti_translation_path(pfi_nifti_input, new_traslation, pfi_nifti_output, q_form=True, s_form=True,
                                  verbose=1):
    """
    Change q_form or s_form or both translational part.
    :param pfi_nifti_input: path to file of the input image
    :param new_traslation: 3dim array, affine coordinates, will be the future translational part of the affine.
    :param pfi_nifti_output: path to file of the image with the modifed translation. Try not to be destructive,
    unless you do not really want.
    :param q_form: [True] affect q_form
    :param s_form: [True] affect s_form
    :param verbose:
    :return: None. It creates a new image in pfi_nifti_output with defined translational part.
    """
    im_input = nib.load(pfi_nifti_input)

    # generate new affine transformation (from bicommissural to histological)
    aff = im_input.affine
    # create output image on the input
    if im_input.header['sizeof_hdr'] == 348:
        new_image = nib.Nifti1Image(im_input.get_data(), aff, header=im_input.header)
    # if nifty2
    elif im_input.header['sizeof_hdr'] == 540:
        new_image = nib.Nifti2Image(im_input.get_data(), aff, header=im_input.header)
    else:
        raise IOError

    new_transf = np.copy(aff)
    if len(new_traslation) == 4 and new_traslation[-1] == 1:
        new_transf[:, 3] = new_traslation
    elif len(new_traslation) == 3:
        new_transf[:3, 3] = new_traslation
    else:
        raise IOError

    if q_form:
        new_image.set_qform(new_transf)

    if s_form:
        new_image.set_sform(new_transf)

    new_image.update_header()

    if verbose > 0:
        # print intermediate results
        print('Affine input image:')
        print(im_input.get_affine())
        print('Affine after update:')
        print(new_image.get_affine())
        print('Q-form after update:')
        print(new_image.get_qform())
        print('S-form after update:')
        print(new_image.get_sform())

    # save output image
    nib.save(new_image, pfi_nifti_output)


def adjust_nifti_image_type_path(pfi_nifti_input, new_dtype, pfi_nifti_output, update_description=None, verbose=1):
    im_input = nib.load(pfi_nifti_input)
    if update_description is not None:
        if not isinstance(update_description, str):
            raise IOError('update_description must be a string')
        hd = im_input.header
        hd['descrip'] = update_description
        im_input.update_header()
    new_im = set_new_data(im_input, im_input.get_data().astype(new_dtype), new_dtype=new_dtype, remove_nan=True)
    if verbose > 0:
        print('Data type before {}'.format(im_input.get_data_dtype()))
        print('Data type after {}'.format(new_im.get_data_dtype()))
    nib.save(new_im, pfi_nifti_output)


def custom_cleaner(pfi_image):
    print 'Custom cleaner path {}'.format(pfi_image)
    assert os.path.exists(pfi_image), pfi_image
    im_ = nib.load(pfi_image)
    # set custom description
    im_ = set_new_header_description(im_, 'Newborn Brain Rabbit Multi-Atlas Dataset')
    # remove nan
    im_ = remove_nan(im_)
    nib.save(im_, pfi_image)


if __name__ == '__main__':
    # for each chart in the template:
    pfo_multi_atlas = path_manager.pfo_multi_atlas

    assert os.path.exists(pfo_multi_atlas)

    atlas_charts = []

    ''' set the origin in the center of mass of the segmentation of a chart of the atlas '''
    if False:

        for p in os.listdir(pfo_multi_atlas):
            if p.isdigit():
                pass
                # Already used. Do not use twice on the same dataset!!
                # atlas_charts += [p]

        for ch in atlas_charts:
            pfo_mod = jph(pfo_multi_atlas, ch, 'mod')
            pfo_masks = jph(pfo_multi_atlas, ch, 'masks')
            pfo_segm = jph(pfo_multi_atlas, ch, 'segm')

            # binarise the approved segmentation, or if not present, one of the automatic.
            pfi_segm = jph(pfo_segm, '{}_approved.nii.gz'.format(ch))
            pfi_segm_bin = jph(path_manager.pfo_tmp, '{}_approved_bin.nii.gz'.format(ch))
            cmd = 'seg_maths {0} -bin {1}'.format(pfi_segm, pfi_segm_bin)
            os.system(cmd)

            # Get the centroid of the segmentation
            c_m = -1 * centroid(nib.load(pfi_segm_bin), [1, ])[0]

            # -- apply centroid to sform and qform for each modality, segmentation and masks:
            # Modalities:
            for mo in os.listdir(pfo_mod):
                if ch in mo:
                    pfi_mo = jph(pfo_mod, mo)
                    adjust_nifti_translation_path(pfi_mo, c_m, pfi_mo)
                    adjust_nifti_image_type_path(pfi_mo, np.float32, pfi_mo, update_description='')
            # Masks:
            for ma in os.listdir(pfo_masks):
                if ch in ma:
                    pfi_ma = jph(pfo_masks, ma)
                    adjust_nifti_translation_path(pfi_ma, c_m, pfi_ma)
                    adjust_nifti_image_type_path(pfi_ma, np.uint8, pfi_ma, update_description='')
            # Segm:
            for se in os.listdir(pfo_segm):
                if ch in se:
                    pfi_se = jph(pfo_segm, se)
                    adjust_nifti_translation_path(pfi_se, c_m, pfi_se)
                    adjust_nifti_image_type_path(pfi_se, np.uint16, pfi_se, update_description='')

            # for T1 and S0 apply the re-normalisation based on the registration mask.
            pfi_reg_mask = jph(pfo_masks, '{}_roi_reg_mask.nii.gz'.format(ch))
            pfi_T1 = jph(pfo_mod, '{}_T1.nii.gz'.format(ch))
            pfi_S0 = jph(pfo_mod, '{}_S0.nii.gz'.format(ch))

            lt = LT(pfo_mod)
            lt.manipulate_intensities.normalise_below_label(pfi_T1, pfi_T1, pfi_segm, )
            lt.manipulate_intensities.normalise_below_label(pfi_S0, pfi_S0, pfi_segm, )

    ''' set the origin in the center of mass of the segmentation of a chart of the atlas '''
    if False:

        for fi in os.listdir(pfo_multi_atlas):
            if fi.endswith('.nii.gz'):
                pfi_im = jph(pfo_multi_atlas, fi)
                im = nib.load(pfi_im)

                print ''
                print fi
                print 'current affine: '
                print im.affine
                new_center = -1 * im.affine[:3, :3].dot(np.array([157, 230, 90]))
                print 'new center:'
                print new_center
                pfi_im_new = jph(pfo_multi_atlas, 'a_{}'.format(fi))
                adjust_nifti_translation_path(pfi_im, new_center, pfi_im_new, verbose=0)

                im_again = nib.load(pfi_im_new)
                print 'new affine:'
                print im_again.affine

    if False:
        atlas_list_charts_names = ['1201', '1203', '1305', '1404', '1507', '1510', '1702', '1805', '2002', '2502',
                                   '3301']
        modalities_names = ['T1', 'FA', 'MD', 'S0', 'V1']
        masks_names = ['roi_mask', 'reg_mask']

        ''' Merge labels as a test labels'''
        for sj in atlas_list_charts_names:
            pfi_orignal = jph(pfo_multi_atlas, sj, 'segm', '{}_approved.nii.gz'.format(sj))
            pfi_merged = jph(pfo_multi_atlas, sj, 'segm', 'test_PV_{}_approved.nii.gz'.format(sj))

            lt = LT(pfo_multi_atlas)
            lt.manipulate_labels.relabel(pfi_orignal, pfi_merged, list_old_labels=(211, 212),
                                         list_new_labels=(201, 201))

        pfo = '/Users/sebastiano/Dropbox/RabbitEOP-MRI/study/A_atlas/3301/segm/automatic'
        for fin in os.listdir(pfo):
            if fin.endswith('.nii.gz'):
                pfi_new = jph(pfo, 'test_PV_' + fin)
                lt = LT()
                lt.manipulate_labels.relabel(jph(pfo, fin), pfi_new, list_old_labels=(211, 212),
                                             list_new_labels=(201, 201))

        ''' Remove nan and set up a message'''
        for sj in atlas_list_charts_names:
            print 'Remove nan and set up descriptor, chart {}'.format(sj)
            pfo_chart_sj = jph(pfo_multi_atlas, sj)
            assert os.path.exists(pfo_chart_sj)
            # modalities:
            for mod in modalities_names:
                pfi_im = jph(pfo_chart_sj, 'mod', '{0}_{1}.nii.gz'.format(sj, mod))
                custom_cleaner(pfi_im)
            # masks:
            for ma in masks_names:
                pfi_im = jph(pfo_chart_sj, 'masks', '{0}_{1}.nii.gz'.format(sj, ma))
                custom_cleaner(pfi_im)
            # segmentation:
            pfi_segm = jph(pfo_chart_sj, 'segm', '{0}_{1}.nii.gz'.format(sj, 'approved'))
            if os.path.exists(pfi_segm):
                custom_cleaner(pfi_segm)
            pfi_segm = jph(pfo_chart_sj, 'segm', '{0}_{1}_{2}.nii.gz'.format('test_PV', sj, 'approved'))
            if os.path.exists(pfi_segm):
                custom_cleaner(pfi_segm)

    if True:
        ''' normalise values below T1 and S0 : use binarised segmentation with the. '''
        for sj in ['2502']:
            print 'normalisation T1, S0, chart {}'.format(sj)

            pfo_chart_sj = jph(path_manager.pfo_multi_atlas, sj)
            pfi_T1 = jph(pfo_chart_sj, 'mod', '{0}_T1.nii.gz'.format(sj))
            pfi_S0 = jph(pfo_chart_sj, 'mod', '{0}_S0.nii.gz'.format(sj))
            pfi_segm = jph(pfo_chart_sj, 'segm', '{0}_segm.nii.gz'.format(sj))
            if not os.path.exists(pfi_segm):
                pfi_segm = jph(pfo_chart_sj, 'segm', 'automatic','{0}_T1_MV_s.nii.gz'.format(sj))
            pfi_roi = jph(pfo_chart_sj, 'masks', '{0}_roi_mask.nii.gz'.format(sj))

            assert os.path.exists(pfi_T1)
            assert os.path.exists(pfi_S0)
            assert os.path.exists(pfi_segm)
            assert os.path.exists(pfi_roi)

            im_T1 = nib.load(pfi_T1)
            im_S0 = nib.load(pfi_S0)
            im_segm = nib.load(pfi_segm)
            im_roi  = nib.load(pfi_roi)

            im_T1_normalised = normalise_below_labels(im_T1, im_segm)
            im_S0_normalised = normalise_below_labels(im_S0, im_segm)

            pfi_T1 = jph(pfo_chart_sj, 'mod', '{0}_T1_normalised.nii.gz'.format(sj))
            pfi_S0 = jph(pfo_chart_sj, 'mod', '{0}_S0_normalised.nii.gz'.format(sj))
            nib.save(im_T1_normalised, pfi_T1)
            nib.save(im_S0_normalised, pfi_S0)
