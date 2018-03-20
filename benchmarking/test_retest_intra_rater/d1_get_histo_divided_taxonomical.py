from matplotlib import pyplot as plt
import pandas as pa
import numpy as np

from benchmarking.a_nomenclatures import nomenclature_taxonomical
import benchmarking.test_retest_intra_rater.a_paths_intra_rater as ph
import seaborn as sns


if __name__ == '__main__':
    # Parameters
    metrics = ['dice_score', 'covariance_distance', 'hausdorff_distance', 'normalised_symmetric_contour_distance']
    dict_metric_to_metric_name = {'dice_score': 'Dice Score',
                                  'covariance_distance': 'Covariance Distance',
                                  'hausdorff_distance': 'Hausdorff Distance',
                                  'normalised_symmetric_contour_distance': 'Normalised Symmetric Contour Distance'}

    region_names = [nomenclature_taxonomical[k][0] for k in nomenclature_taxonomical.keys()]

    print(region_names)
    n = len(region_names)

    for pfi_pickle_input, pfi_image_output, title in zip(
            [ph.pfi_pickled_scoring_man1_man2_taxo, ph.pfi_pickled_scoring_auto_man1_taxo, ph.pfi_pickled_scoring_auto_man2_taxo],
            [ph.pfi_histogram_man1_man2_taxo,       ph.pfi_histogram_auto_man1_taxo,       ph.pfi_histogram_auto_man2_taxo],
            ['man1 vs man2',                        'auto vs man1',                        'auto vs man2']):
        # Load data
        df_measures_taxon = pa.read_pickle(pfi_pickle_input)
        print 'man1 man2'
        print df_measures_taxon

        fig, ax = plt.subplots(figsize=(12, 8), nrows=4, ncols=1)
        fig.canvas.set_window_title(title)

        sns.set(color_codes=True)

        # Dice score
        ax[0].set_title('1 - (Dice score)')
        one_minus_dice = [1 - m for m in df_measures_taxon['dice_score']]
        ax[0].bar(range(n), one_minus_dice)
        ax[0].set_ylabel('%')
        ax[0].set_ylim([0, 0.085])  # set manually for easy comparisons between figures.
        ax[0].set_xticks(range(n))
        ax[0].set_xticklabels([])

        mu_dice = np.mean([m for m in one_minus_dice if m > 0])
        std_dice = np.std([m for m in one_minus_dice if m > 0])

        ax[0].annotate('mu(>0) {0:1.4f}\nstd(>0) {1:1.4f}'.format(mu_dice, std_dice),
                       xy=(-0.5, 0.045), xytext=(-0.5, 0.045))

        # Covariance Distance
        ax[1].set_title('Covariance Distance')
        significant_cov_dist = [m if m > 10e-5 else 0 for m in df_measures_taxon['covariance_distance']]
        ax[1].bar(range(n), significant_cov_dist)
        ax[1].set_ylabel('mm')
        ax[1].set_ylim([0, 0.1])
        ax[1].set_xticks(range(n))
        ax[1].set_xticklabels([])

        mu_cd = np.mean([m for m in significant_cov_dist if m > 0])
        std_cd = np.std([m for m in significant_cov_dist if m > 0])

        ax[1].annotate('mu(>0) {0:1.4f}\nstd(>0) {1:1.4f}'.format(mu_cd, std_cd), xy=(-0.5, 0.05), xytext=(-0.5, 0.05))

        # Hausdorff Distance
        ax[2].set_title('Hausdorff Distance')
        ax[2].bar(range(n), df_measures_taxon['hausdorff_distance'])
        ax[2].set_ylabel('mm')
        ax[2].set_ylim([0, 0.8])
        ax[2].set_xticks(range(n))
        ax[2].set_xticklabels([])

        mu_hd = np.mean([m for m in df_measures_taxon['hausdorff_distance'] if m > 0])
        std_hd = np.std([m for m in df_measures_taxon['hausdorff_distance'] if m > 0])

        ax[2].annotate('mu(>0) {0:1.4f}\nstd(>0) {1:1.4f}'.format(mu_hd, std_hd), xy=(-0.5, 0.4), xytext=(-0.5, 0.4))

        # Normalised symmetric contour distance
        ax[3].set_title('Normalised Symmetric Contour Distance')
        ax[3].bar(range(n), df_measures_taxon['normalised_symmetric_contour_distance'])
        ax[3].set_ylabel('mm')
        ax[3].set_ylim([0, 0.03])
        ax[3].set_xticks(range(n))
        ax[3].set_xticklabels(region_names, ha='right', rotation=45)

        mu_nscd = np.mean([m for m in df_measures_taxon['normalised_symmetric_contour_distance'] if m > 0])
        std_nscd = np.std([m for m in df_measures_taxon['normalised_symmetric_contour_distance'] if m > 0])

        ax[3].annotate('mu(>0) {0:1.4f}\nstd(>0) {1:1.4f}'.format(mu_nscd, std_nscd), xy=(-0.5, 0.015), xytext=(-0.5, 0.015))

        fig.tight_layout()
        plt.savefig(pfi_image_output, format='pdf', dpi=200)
