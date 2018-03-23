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

    x_labels = ['man1 vs man2', 'auto vs man1', 'auto vs man2']

    df_measures_man1_man2_all = pa.read_pickle(ph.pfi_pickled_scoring_man1_man2_all)
    df_measures_auto_man1_all = pa.read_pickle(ph.pfi_pickled_scoring_auto_man1_all)
    df_measures_auto_man2_all = pa.read_pickle(ph.pfi_pickled_scoring_auto_man2_all)

    # get data data with the positive 1 - dice

    df_measures_man1_man2_all["dice_smaller_than_1"] = df_measures_man1_man2_all['dice_score'] < 1.0
    df_measures_auto_man1_all["dice_smaller_than_1"] = df_measures_auto_man1_all['dice_score'] < 1.0
    df_measures_auto_man2_all["dice_smaller_than_1"] = df_measures_auto_man2_all['dice_score'] < 1.0

    plt.rc('font', family='serif')

    fig, ax = plt.subplots(figsize=(10, 3), nrows=1, ncols=4)
    fig.canvas.set_window_title('Auto vs man1 vs man2 - intra rater variability manual adjustment - all labels')

    sns.set(color_codes=True)

    # Dice score
    ax[0].set_title('1 - Dice Score')
    data_ds = [[1 - df_measures_man1_man2_all['dice_score'][id] for id in df_measures_man1_man2_all.index if df_measures_man1_man2_all["dice_smaller_than_1"][id]],
               [1 - df_measures_auto_man1_all['dice_score'][id] for id in df_measures_auto_man1_all.index if df_measures_auto_man1_all["dice_smaller_than_1"][id]],
               [1 - df_measures_auto_man2_all['dice_score'][id] for id in df_measures_auto_man2_all.index if df_measures_auto_man2_all["dice_smaller_than_1"][id]]]
    ax[0].boxplot(data_ds)
    ax[0].set_ylabel('%', fontsize=8)
    ax[0].set_ylim([-0.001, 0.10])  # set manually for easy comparisons between figures.
    ax[0].set_xticks(range(1, 4))
    ax[0].set_xticklabels(x_labels, rotation=45, fontsize=8)

    # Covariance Distance
    ax[1].set_title('CD')
    data_cd = [[df_measures_man1_man2_all['covariance_distance'][id] for id in df_measures_man1_man2_all.index if df_measures_man1_man2_all["dice_smaller_than_1"][id]],
               [df_measures_auto_man1_all['covariance_distance'][id] for id in df_measures_auto_man1_all.index if df_measures_auto_man1_all["dice_smaller_than_1"][id]],
               [df_measures_auto_man2_all['covariance_distance'][id] for id in df_measures_auto_man2_all.index if df_measures_auto_man2_all["dice_smaller_than_1"][id]]]

    ax[1].boxplot(data_cd)
    ax[1].set_ylabel('mm', fontsize=8)
    ax[1].set_ylim([-0.001, 0.275])  # set manually for easy comparisons between figures.
    ax[1].set_xticks(range(1,4))
    ax[1].set_xticklabels(x_labels, rotation=45, fontsize=8)

    # Hausdorff Distance
    ax[2].set_title('HD')
    data_hd = [[df_measures_man1_man2_all['hausdorff_distance'][id] for id in df_measures_man1_man2_all.index if df_measures_man1_man2_all["dice_smaller_than_1"][id]],
               [df_measures_auto_man1_all['hausdorff_distance'][id] for id in df_measures_auto_man1_all.index if df_measures_auto_man1_all["dice_smaller_than_1"][id]],
               [df_measures_auto_man2_all['hausdorff_distance'][id] for id in df_measures_auto_man2_all.index if df_measures_auto_man2_all["dice_smaller_than_1"][id]]]

    ax[2].boxplot(data_hd)
    ax[2].set_ylabel('mm', fontsize=8)
    ax[2].set_ylim([-0.001, 0.7])  # set manually for easy comparisons between figures.
    ax[2].set_xticks(range(1,4))
    ax[2].set_xticklabels(x_labels, rotation=45, fontsize=8)

    # Normalised symmetric contour distance
    ax[3].set_title('NSCD')
    data_nscd = [[df_measures_man1_man2_all['normalised_symmetric_contour_distance'][id] for id in df_measures_man1_man2_all.index if df_measures_man1_man2_all["dice_smaller_than_1"][id]],
                 [df_measures_auto_man1_all['normalised_symmetric_contour_distance'][id] for id in df_measures_auto_man1_all.index if df_measures_auto_man1_all["dice_smaller_than_1"][id]],
                 [df_measures_auto_man2_all['normalised_symmetric_contour_distance'][id] for id in df_measures_auto_man2_all.index if df_measures_auto_man2_all["dice_smaller_than_1"][id]]]
    ax[3].boxplot(data_nscd)
    ax[3].set_ylabel('mm', fontsize=8)
    ax[3].set_ylim([-0.001, 0.04])  # set manually for easy comparisons between figures.
    ax[3].set_xticks(range(1,4))
    ax[3].set_xticklabels(x_labels, rotation=45, fontsize=8)

    fig.tight_layout()
    plt.savefig(ph.pfi_boxplot_comparison_all, format='pdf', dpi=200)
    plt.show()
