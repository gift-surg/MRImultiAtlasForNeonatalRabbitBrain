import benchmarking.test_retest_intra_rater.a_paths_intra_rater as ph
import nilabels as nis
from nilabels.tools.caliber import distances as dist

from benchmarking.a_nomenclatures import nomenclature_taxonomical


def collect_measurements_intra_rater_tst_retest():
    print '\n==================='
    print '\n\nTaxonomical division inter-rater test-re-test'
    print '==================='
    print 'Compare man1 with man2 taxonomical'
    nis_app = nis.App()
    nis_app.measure.verbose = True
    man1_man2_measures_divide_taxonomical = nis_app.measure.dist(ph.pfi_segm_man1_divided_taxonomical,
                                                                 ph.pfi_segm_man2_divided_taxonomical,
                                                                 labels_list=nomenclature_taxonomical.keys(),
                                                                 labels_names=nomenclature_taxonomical.keys(),
                                                                 metrics=(dist.dice_score,
                                                                           dist.covariance_distance,
                                                                           dist.hausdorff_distance,
                                                                           dist.normalised_symmetric_contour_distance),
                                                                 where_to_save=ph.pfi_pickled_scoring_man1_man2_taxo)

    print '---------------'
    print 'Compare man1 with man2 divided taxonomical'
    print man1_man2_measures_divide_taxonomical

    del nis_app

    print '\n\n==================='
    print 'Compare auto with man1 taxonomical'
    nis_app = nis.App()
    nis_app.measure.verbose = True
    auto_man1_measures_divide_taxonomical = nis_app.measure.dist(ph.pfi_segm_auto_divided_taxonomical,
                                                                 ph.pfi_segm_man1_divided_taxonomical,
                                                                 labels_list=nomenclature_taxonomical.keys(),
                                                                 labels_names=nomenclature_taxonomical.keys(),
                                                                 metrics=(dist.dice_score,
                                                                        dist.covariance_distance,
                                                                        dist.hausdorff_distance,
                                                                        dist.normalised_symmetric_contour_distance),
                                                                 where_to_save=ph.pfi_pickled_scoring_auto_man1_taxo)

    print '---------------'
    print 'Compare auto with man1 divided taxonomical'
    print auto_man1_measures_divide_taxonomical

    del nis_app

    print '\n\n==================='
    print 'Compare auto with man2  taxonomical'
    nis_app = nis.App()
    nis_app.measure.verbose = True
    auto_man2_measures_divide_taxonomical = nis_app.measure.dist(ph.pfi_segm_auto_divided_taxonomical,
                                                                 ph.pfi_segm_man2_divided_taxonomical,
                                                                 labels_list=nomenclature_taxonomical.keys(),
                                                                 labels_names=nomenclature_taxonomical.keys(),
                                                                 metrics=(dist.dice_score,
                                                                          dist.covariance_distance,
                                                                          dist.hausdorff_distance,
                                                                          dist.normalised_symmetric_contour_distance),
                                                                 where_to_save=ph.pfi_pickled_scoring_auto_man2_taxo)

    print '---------------'
    print 'Compare auto with man2 divided taxonomical'
    print auto_man2_measures_divide_taxonomical

    del nis_app


if __name__ == '__main__':
    collect_measurements_intra_rater_tst_retest()
