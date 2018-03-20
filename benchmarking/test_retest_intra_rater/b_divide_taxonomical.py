import benchmarking.test_retest_intra_rater.a_paths_intra_rater as ph
from LABelsToolkit.main import LABelsToolkit as LabT

from benchmarking.a_nomenclatures import nomenclature_taxonomical


def divide_taxonomical_intra_rater_tst_retest():
    taxonomical_old_labels = []
    taxonomical_new_labels = []

    for k in nomenclature_taxonomical.keys():
        taxonomical_old_labels += nomenclature_taxonomical[k][1]
        taxonomical_new_labels += [k] * len(nomenclature_taxonomical[k][1])

    # divide auto
    lt = LabT()
    lt.manipulate_labels.relabel(ph.pfi_segm_auto, ph.pfi_segm_auto_divided_taxonomical,
                                 list_old_labels=taxonomical_old_labels,
                                 list_new_labels=taxonomical_new_labels)
    del lt

    # divide man1
    lt = LabT()
    lt.manipulate_labels.relabel(ph.pfi_segm_man1, ph.pfi_segm_man1_divided_taxonomical,
                                 list_old_labels=taxonomical_old_labels,
                                 list_new_labels=taxonomical_new_labels)
    del lt

    # divide man2
    lt = LabT()
    lt.manipulate_labels.relabel(ph.pfi_segm_man2, ph.pfi_segm_man2_divided_taxonomical,
                                 list_old_labels=taxonomical_old_labels,
                                 list_new_labels=taxonomical_new_labels)
    del lt


if __name__ == '__main__':
    divide_taxonomical_intra_rater_tst_retest()
