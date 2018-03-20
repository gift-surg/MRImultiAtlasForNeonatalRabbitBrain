import numpy as np
import nibabel as nib
import os
from os.path import join as jph

from LABelsToolkit.main import LABelsToolkit as LM
from LABelsToolkit.tools.aux_methods.utils_nib import remove_nan, set_new_header_description, set_new_data
from LABelsToolkit.tools.image_colors_manipulations.normaliser import intensities_normalisation_linear, \
    normalise_below_labels


atlas_list_charts_names = ['1201', '1203', '1305', '1404', '1507', '1510', '1702', '1805', '2002', '2502', '3301']
modalities_names = ['T1', 'FA', 'MD', 'S0', 'V1']
masks_names    = ['roi_mask', 'reg_mask']

# pfo_atlas = '/Volumes/sebastianof/rabbits/A_atlas'
pfo_atlas = '/Users/sebastiano/Dropbox/RabbitEOP-MRI/study/A_atlas'
# pfo_atlas = '/Users/sebastiano/Desktop/z_test_atlas'

assert os.path.exists(pfo_atlas), 'Connect to external hdd'


def custom_clean(pfi_image):
    print 'Custom cleaner path {}'.format(pfi_image)
    assert os.path.exists(pfi_image), pfi_image
    im = nib.load(pfi_image)
    # set custom description
    im = set_new_header_description(im, 'Newborn Brain Rabbit Multi-Atlas Dataset')
    # remove nan
    im = remove_nan(im)
    nib.save(im, pfi_image)


if __name__ == '__main__':

    ''' Merge labels as a test labels'''
    # for sj in atlas_list_charts_names:
    #     pfi_orignal = jph(pfo_atlas, sj, 'segm', '{}_approved.nii.gz'.format(sj))
    #     pfi_merged = jph(pfo_atlas, sj, 'segm', 'test_PV_{}_approved.nii.gz'.format(sj))
    #
    #     lm = LM(pfo_atlas)
    #     lm.manipulate_labels.relabel(pfi_orignal, pfi_merged, list_old_labels=(211, 212), list_new_labels=(201, 201))
    #
    #
    # pfo = '/Users/sebastiano/Dropbox/RabbitEOP-MRI/study/A_atlas/3301/segm/automatic'
    # for fin in os.listdir(pfo):
    #     if fin.endswith('.nii.gz'):
    #         pfi_new = jph(pfo, 'test_PV_' + fin)
    #         lm = LM()
    #         lm.manipulate_labels.relabel(jph(pfo, fin), pfi_new, list_old_labels=(211, 212), list_new_labels=(201, 201))

    ''' Remove nan and set up a message'''
    # for sj in atlas_list_charts_names:
    #     print 'Remove nan and set up descriptor, chart {}'.format(sj)
    #     pfo_chart_sj = jph(pfo_atlas, sj)
    #     assert os.path.exists(pfo_chart_sj)
    #     # modalities:
    #     for mod in modalities_names:
    #         pfi_im = jph(pfo_chart_sj, 'mod', '{0}_{1}.nii.gz'.format(sj, mod))
    #         custom_clean(pfi_im)
    #     # masks:
    #     for ma in masks_names:
    #         pfi_im = jph(pfo_chart_sj, 'masks', '{0}_{1}.nii.gz'.format(sj, ma))
    #         custom_clean(pfi_im)
    #     # segmentation:
    #     pfi_segm = jph(pfo_chart_sj, 'segm', '{0}_{1}.nii.gz'.format(sj, 'approved'))
    #     if os.path.exists(pfi_segm):
    #         custom_clean(pfi_segm)
    #     pfi_segm = jph(pfo_chart_sj, 'segm', '{0}_{1}_{2}.nii.gz'.format('test_PV', sj, 'approved'))
    #     if os.path.exists(pfi_segm):
    #         custom_clean(pfi_segm)

    ''' normalise values below T1 and S0 : use binarised segmentation with the. '''
    for sj in atlas_list_charts_names:
        print 'normalisation T1, S0, chart {}'.format(sj)

        pfo_chart_sj = jph(pfo_atlas, sj)
        pfi_T1 = jph(pfo_chart_sj, 'mod', '{0}_T1.nii.gz'.format(sj))
        pfi_S0 = jph(pfo_chart_sj, 'mod', '{0}_S0.nii.gz'.format(sj))
        pfi_segm = jph(pfo_chart_sj, 'segm', '{0}_approved.nii.gz'.format(sj))
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

        # pfi_T1 = jph(pfo_chart_sj, 'mod', '{0}_T1_normalised.nii.gz'.format(sj))
        # pfi_S0 = jph(pfo_chart_sj, 'mod', '{0}_S0_normalised.nii.gz'.format(sj))
        nib.save(im_T1_normalised, pfi_T1)
        nib.save(im_S0_normalised, pfi_S0)

