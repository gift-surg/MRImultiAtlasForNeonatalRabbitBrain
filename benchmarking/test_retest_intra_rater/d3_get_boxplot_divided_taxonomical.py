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

    x_labels = ['adj1 vs adj2', 'auto vs adj1', 'auto vs adj2']

    df_measures_man1_man2_taxo = pa.read_pickle(ph.pfi_pickled_scoring_man1_man2_taxo)
    df_measures_auto_man1_taxo = pa.read_pickle(ph.pfi_pickled_scoring_auto_man1_taxo)
    df_measures_auto_man2_taxo = pa.read_pickle(ph.pfi_pickled_scoring_auto_man2_taxo)

    plt.rc('font', family='serif')

    fig, ax = plt.subplots(figsize=(10, 3), nrows=1, ncols=4)
    fig.canvas.set_window_title('Auto vs man1 vs man2 - intra rater variability manual adjustment taxonomical')

    sns.set(color_codes=True)

    # Dice score
    ax[0].set_title('1 - Dice')
    data_ds = [[1 - m for m in df_measures_man1_man2_taxo['dice_score'] if m > 10e-6],
               [1 - m for m in df_measures_auto_man1_taxo['dice_score'] if m > 10e-6],
               [1 - m for m in df_measures_auto_man2_taxo['dice_score'] if m > 10e-6]]
    ax[0].boxplot(data_ds)
    ax[0].set_ylabel('%')
    ax[0].set_ylim([-0.001, 0.010])  # set manually for easy comparisons between figures.
    ax[0].set_xticks(range(1,4))
    ax[0].set_xticklabels(x_labels, rotation=45)

    # Covariance Distance
    ax[1].set_title('CD')
    data_cd = [[m for m in df_measures_man1_man2_taxo['covariance_distance'] if m > 10e-6],
               [m for m in df_measures_auto_man1_taxo['covariance_distance'] if m > 10e-6],
               [m for m in df_measures_auto_man2_taxo['covariance_distance'] if m > 10e-6]]
    ax[1].boxplot(data_cd)
    ax[1].set_ylabel('mm')
    ax[1].set_ylim([-0.001, 0.02])  # set manually for easy comparisons between figures.
    ax[1].set_xticks(range(1,4))
    ax[1].set_xticklabels(x_labels, rotation=45)

    # Hausdorff Distance
    ax[2].set_title('HD')
    data_hd = [[m for m in df_measures_man1_man2_taxo['hausdorff_distance'] if m > 10e-6],
               [m for m in df_measures_auto_man1_taxo['hausdorff_distance'] if m > 10e-6],
               [m for m in df_measures_auto_man2_taxo['hausdorff_distance'] if m > 10e-6]]
    ax[2].boxplot(data_hd)
    ax[2].set_ylabel('mm')
    ax[2].set_ylim([-0.001, 0.4])  # set manually for easy comparisons between figures.
    ax[2].set_xticks(range(1,4))
    ax[2].set_xticklabels(x_labels, rotation=45)

    # Normalised symmetric contour distance
    ax[3].set_title('NSCD')
    data_nscd = [[m for m in df_measures_man1_man2_taxo['normalised_symmetric_contour_distance'] if m > 10e-6],
                 [m for m in df_measures_auto_man1_taxo['normalised_symmetric_contour_distance'] if m > 10e-6],
                 [m for m in df_measures_auto_man2_taxo['normalised_symmetric_contour_distance'] if m > 10e-6]]
    ax[3].boxplot(data_nscd)
    ax[3].set_ylabel('mm')
    ax[3].set_ylim([-0.001, 0.02])  # set manually for easy comparisons between figures.
    ax[3].set_xticks(range(1, 4))
    ax[3].set_xticklabels(x_labels, rotation=45)

    fig.tight_layout()

    # plt.savefig(ph.pfi_boxplot_comparison_taxo, format='pdf', dpi=200)
    plt.show()
