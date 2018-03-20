import os
from collections import OrderedDict

from LABelsToolkit.tools.descriptions.manipulate_descriptors import LabelsDescriptorManager


nomenclature_anatomical = OrderedDict(
    # center  - sector : [labels]
    {1: [83, 251, 247],
     2: [84, 252, 248],
     # round 1
     3: [237, 218, 78],  # central upper
     4: [71, 75, 223],
     5: [243, 239, 227],
     6: [139, 31],
     7: [127, 253],  # central lower
     8: [140, 32],
     9: [244, 240, 228],
     10: [72, 76, 224],
     # round 2
     11: [77, 233, 215],  # central upper
     12: [211, 69],
     13: [219, 53, 225],
     14: [129, 229, 43],
     15: [121, 201],  # central lower
     16: [130, 230, 44],
     17: [220, 54, 226],
     18: [212, 70],
     # round 3
     19: [25, 5, 7, 15],
     20: [11, 9, 17],
     21: [27, 13, 45, 19],
     22: [241, 55, 109],
     23: [141, 133, 135, 179, 203],
     24: [151, 153, 161], # central lower
     25: [142, 134, 136, 180, 204],
     26: [242, 56, 110],
     27: [28, 14, 46, 20],
     28: [12, 10, 18],
     29: [26, 6, 8, 16]
     })

nomenclature_taxonomical = OrderedDict(
    {
     # round 1
     1: ['CST', [223, 224, 225, 226, 227, 228, 229, 230]],
     2: ['CC', [218, 219, 220]],
     3: ['Other fibretracts', [215, 233, 237, 239, 240, 241, 242, 243, 244, 247, 248, 251, 252, 253]],
     # round 2
     4: ['Cerebellar Vermis', [161]],
     5: ['Ventricular System', [201, 211, 212, 203, 204]],
     6: ['Cerebellar Hemisphere', [179, 180]],
     # round 3
     7: ['Hypotalamus', [109, 110, 121]],
     8: ['Rombocephalon', [151, 153]],
     9: ['Mesencephalon', [127, 129, 130, 133, 134, 135, 136, 139, 140, 141, 142]],
     10: ['Thalamus', [83, 84]],
     # round 4
     11: ['Allocortex', [25, 26, 27, 28]],
     12: ['Hippocampal Formation', [31, 32, 43, 44, 45, 46]],
     13: ['Deep Cortex', [53, 54, 55, 56]],
     14: ['Basal Ganglia', [69, 70, 71, 72, 75, 76]],
     15: ['Septum and Basal Forebrain', [77, 78]],
     16: ['Isocortex', [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]],
    })

taxonomy_abbreviations = OrderedDict(
    {
     5 : 'PFrA L',
     6 : 'PFrA R',
     7 : 'FrA L',
     8 : 'FrA R',
     9 : 'OA L',
     10 : 'OA R',
     11 : 'PtA L',
     12 : 'PtA R',
     13 : 'TeA L',
     14 : 'TeA R',
     15 : 'Cg L',
     16 : 'Cg R',
     17 : 'RS L',
     18 : 'RS R',
     19 : 'Ins L',
     20 : 'Ins R',
     25 : 'OB L',
     26 : 'OB R',
     27 : 'Pir L',
     28 : 'Pir R',
     31 : 'HA L',
     32 : 'HA R',
     43 : 'S L',
     44 : 'S R',
     45 : 'Ent L',
     46 : 'Ent R',
     53 : 'CL L',
     54 : 'CL R',
     55 : 'Am L',
     56 : 'Am R',
     69 : 'CA CN L',
     70 : 'CA CN R',
     71 : 'Pu L',
     72 : 'Pu R',
     75 : 'GP L',
     76 : 'GP R',
     77 : 'BF',
     78 : 'SA',
     83 : 'THA L',
     84 : 'THA R',
     109 : 'HYP L',
     110 : 'HYP R',
     121 : 'MAM',
     127 : 'MB',
     129 : 'PRT L',
     130 : 'PRT R',
     133 : 'SC L',
     134 : 'SC R',
     135 : 'IC L',
     136 : 'IC R',
     139 : 'SN L',
     140 : 'SN R',
     141 : 'PAG L',
     142 : 'PAG R',
     151 : 'PO',
     153 : 'MY',
     161 : 'VERM',
     179 : 'HEM L',
     180 : 'HEM R',
     201 : 'VS',
     203 : 'LV L',
     204 : 'LV R',
     211 : 'PV L',
     212 : 'PV R',
     215 : 'OT',
     218 : 'cc',
     219 : 'ec L',
     220 : 'ec R',
     223 : 'int L',
     224 : 'int R',
     225 : 'cr L',
     226 : 'cr R',
     227 : 'cp L',
     228 : 'cp R',
     229 : 'swm L',
     230 : 'swm R',
     233 : 'ac',
     237 : 'hc',
     239 : 'fi L',
     240 : 'fi R',
     241 : 'fx L',
     242 : 'fx R',
     243 : 'st L',
     244 : 'st R',
     247 : 'mt L',
     248 : 'mt R',
     251 : 'fr L',
     252 : 'fr R',
     253 : 'pc'
     })

nomenclature_labels = ''


# Sanity tests:
if __name__ == '__main__':
    pfi_current_descriptor = '/Users/sebastiano/Dropbox/RabbitEOP-MRI/study/A_atlas/labels_descriptor.txt'

    ldm = LabelsDescriptorManager(pfi_current_descriptor)
    dict = ldm.get_dict()

    labels_current_descriptor = dict.keys()

    labels_nomenclature_anatomical = []
    for d in nomenclature_anatomical.keys():
        labels_nomenclature_anatomical += nomenclature_anatomical[d]

    labels_nomenclature_taxonomical = []
    for d in nomenclature_taxonomical.keys():
        labels_nomenclature_taxonomical += nomenclature_taxonomical[d][1]

    print 'descriptor - anatomical : {}'.format(set(labels_current_descriptor) - set(labels_nomenclature_anatomical))
    print 'anatomical - descriptor  : {}'.format(set(labels_nomenclature_anatomical) - set(labels_current_descriptor))

    print 'descriptor - taxonomical : {}'.format(set(labels_current_descriptor) - set(labels_nomenclature_taxonomical))
    print 'taxonomical - descriptor : {}'.format(set(labels_nomenclature_taxonomical) - set(labels_current_descriptor))

    print 'taxonomical - anatomical : {}'.format(set(labels_nomenclature_taxonomical) - set(labels_nomenclature_anatomical))
    print 'anatomical - taxonomical : {}'.format(set(labels_nomenclature_anatomical) - set(labels_nomenclature_taxonomical))
