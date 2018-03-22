from matplotlib import pyplot as plt
import pandas as pa
import numpy as np

from benchmarking.a_nomenclatures import taxonomy_abbreviations
import benchmarking.test_retest_intra_rater.a_paths_intra_rater as ph
import seaborn as sns

if __name__ == '__main__':

    # Parameters
    metrics = ['dice_score', 'covariance_distance', 'hausdorff_distance', 'normalised_symmetric_contour_distance']
    dict_metric_to_metric_name = {'dice_score': 'Dice Score',
                                  'covariance_distance': 'Covariance Distance',
                                  'hausdorff_distance': 'Hausdorff Distance',
                                  'normalised_symmetric_contour_distance': 'Normalised Symmetric Contour Distance'}

    region_names = [taxonomy_abbreviations[k] for k in taxonomy_abbreviations.keys()]
    n = len(region_names)

    print(region_names)

    for pfi_pickle_input, pfi_image_output, title in zip(
            [ph.pfi_pickled_scoring_man1_man2_all, ph.pfi_pickled_scoring_auto_man1_all, ph.pfi_pickled_scoring_auto_man2_all],
            [ph.pfi_histogram_man1_man2_all,       ph.pfi_histogram_auto_man1_all,       ph.pfi_histogram_auto_man2_all],
            ['man1 vs man2',                        'auto vs man1',                        'auto vs man2']):
        # Load data
        df_measures_all = pa.read_pickle(pfi_pickle_input)
        print 'man1 man2'
        print df_measures_all

        fig, ax = plt.subplots(figsize=(12, 8), nrows=4, ncols=1)
        fig.canvas.set_window_title(title)

        sns.set(color_codes=True)

        # Dice score
        ax[0].set_title('1 - (Dice score)')
        one_minus_dice = [1 - m for m in df_measures_all['dice_score']]
        ax[0].bar(range(n), one_minus_dice)
        ax[0].set_ylabel('%')
        ax[0].set_ylim([0, 0.25])  # set manually for easy comparisons between figures.
        ax[0].set_xticks(range(n))
        # ax[0].set_xticklabels([])
        ax[0].set_xticklabels(region_names, ha='right', rotation=45, fontsize=6)

        mu_dice = np.mean([m for m in one_minus_dice if m > 10e-6])
        std_dice = np.std([m for m in one_minus_dice if m > 10e-6])

        ax[0].annotate('mu(>0) {0:1.4f}\nstd(>0) {1:1.4f}'.format(mu_dice, std_dice), xy=(0, 0.125), xytext=(0, 0.125), fontsize=10)

        # Covariance Distance
        ax[1].set_title('Covariance Distance')
        significant_cov_dist = [m if m > 10e-5 else 0 for m in df_measures_all['covariance_distance']]
        ax[1].bar(range(n), significant_cov_dist)
        ax[1].set_ylabel('mm')
        ax[1].set_ylim([0, 1])
        ax[1].set_xticks(range(n))
        # ax[1].set_xticklabels([])
        ax[1].set_xticklabels(region_names, ha='right', rotation=45, fontsize=6)

        mu_cd = np.mean([m for m in significant_cov_dist if m > 10e-6])
        std_cd = np.std([m for m in significant_cov_dist if m > 10e-6])

        ax[1].annotate('mu(>0) {0:1.4f}\nstd(>0) {1:1.4f}'.format(mu_cd, std_cd), xy=(0, .5), xytext=(0, .5), fontsize=10)

        for m_id, m in enumerate(significant_cov_dist):
            if float(m) > 1:
                ax[1].annotate('{0:1.4f}'.format(m), xy=(m_id + 1, 0.75), xytext=(m_id + 1, 0.75), fontsize=7)

        # Hausdorff Distance
        ax[2].set_title('Hausdorff Distance')
        ax[2].bar(range(n), df_measures_all['hausdorff_distance'])
        ax[2].set_ylabel('mm')
        ax[2].set_ylim([0, 1.5])
        ax[2].set_xticks(range(n))
        # ax[2].set_xticklabels([])
        ax[2].set_xticklabels(region_names, ha='right', rotation=45, fontsize=6)

        mu_hd = np.mean([m for m in df_measures_all['hausdorff_distance'] if m > 10e-6])
        std_hd = np.std([m for m in df_measures_all['hausdorff_distance'] if m > 10e-6])

        ax[2].annotate('mu(>0) {0:1.4f}\nstd(>0) {1:1.4f}'.format(mu_hd, std_hd), xy=(0, 0.75), xytext=(0, 0.75), fontsize=10)

        for m_id, m in enumerate(df_measures_all['hausdorff_distance']):
            if float(m) > 1.5:
                ax[2].annotate('{0:1.4f}'.format(m), xy=(m_id + 1, 1), xytext=(m_id + 1, 1), fontsize=7)

        # Normalised symmetric contour distance
        ax[3].set_title('Normalised Symmetric Contour Distance')
        ax[3].bar(range(n), df_measures_all['normalised_symmetric_contour_distance'])
        ax[3].set_ylabel('mm')
        ax[3].set_ylim([0, 0.06])
        ax[3].set_xticks(range(n))
        ax[3].set_xticklabels(region_names, ha='right', rotation=45, fontsize=6)

        mu_nscd = np.mean([m for m in df_measures_all['normalised_symmetric_contour_distance'] if m > 0])
        std_nscd = np.std([m for m in df_measures_all['normalised_symmetric_contour_distance'] if m > 0])

        ax[3].annotate('mu(>0) {0:1.4f}\nstd(>0) {1:1.4f}'.format(mu_nscd, std_nscd), xy=(0, 0.03), xytext=(0, 0.03), fontsize=10)

        for m_id, m in enumerate(df_measures_all['normalised_symmetric_contour_distance']):
            if float(m) > 0.06:
                ax[3].annotate('{0:1.4f}'.format(m), xy=(m_id + 1, 0.04), xytext=(m_id + 1, 0.04), fontsize=7)

        fig.tight_layout()
        plt.savefig(pfi_image_output, format='pdf', dpi=200)
        plt.show()
