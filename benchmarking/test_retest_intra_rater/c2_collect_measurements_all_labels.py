import benchmarking.test_retest_intra_rater.a_paths_intra_rater as ph
from LABelsToolkit.main import LABelsToolkit as LabT
from LABelsToolkit.tools.caliber import distances as dist

from benchmarking.a_nomenclatures import taxonomy_abbreviations


def collect_measurements_tst_retest():

    man1_man2 = True
    auto_man1 = True
    auto_man2 = True

    if man1_man2:
        print '\n==================='
        print '\n\nTaxonomical division inter-rater test-re-test'
        print '==================='
        print 'Compare man1 with man2 all labels'
        lt = LabT()
        lt.measure.verbose = True
        man1_man2_measures_divide_taxonomical = lt.measure.dist(ph.pfi_segm_man1,
                                                                 ph.pfi_segm_man2,
                                                                 labels_list=taxonomy_abbreviations.keys(),
                                                                 labels_names=taxonomy_abbreviations.keys(),
                                                                 metrics=(dist.dice_score,
                                                                           dist.covariance_distance,
                                                                           dist.hausdorff_distance,
                                                                           dist.normalised_symmetric_contour_distance),
                                                                 where_to_save=ph.pfi_pickled_scoring_man1_man2_all)

        print '---------------'
        print 'Compare man1 with man2 all labels'
        print man1_man2_measures_divide_taxonomical

        del lt

    if auto_man1:
        print '\n\n==================='
        print 'Compare auto with man1 all labels'
        lt = LabT()
        lt.measure.verbose = True
        auto_man1_measures_divide_taxonomical = lt.measure.dist(ph.pfi_segm_auto,
                                                                ph.pfi_segm_man1,
                                                                labels_list=taxonomy_abbreviations.keys(),
                                                                labels_names=taxonomy_abbreviations.keys(),
                                                                metrics=(dist.dice_score,
                                                                         dist.covariance_distance,
                                                                         dist.hausdorff_distance,
                                                                         dist.normalised_symmetric_contour_distance),
                                                                where_to_save=ph.pfi_pickled_scoring_auto_man1_all)

        print '---------------'
        print 'Compare auto with man1 all labels'
        print auto_man1_measures_divide_taxonomical

        del lt

    if auto_man2:
        print '\n\n==================='
        print 'Compare auto with man2  all labels'
        lt = LabT()
        lt.measure.verbose = True
        auto_man2_measures_divide_taxonomical = lt.measure.dist(ph.pfi_segm_auto,
                                                                ph.pfi_segm_man2,
                                                                labels_list=taxonomy_abbreviations.keys(),
                                                                labels_names=taxonomy_abbreviations.keys(),
                                                                metrics=(dist.dice_score,
                                                                         dist.covariance_distance,
                                                                         dist.hausdorff_distance,
                                                                         dist.normalised_symmetric_contour_distance),
                                                                where_to_save=ph.pfi_pickled_scoring_auto_man2_all)

        print '---------------'
        print 'Compare auto with man2 all labels'
        print auto_man2_measures_divide_taxonomical

        del lt


if __name__ == '__main__':
    collect_measurements_tst_retest()
