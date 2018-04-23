"""
Global measurements confusion matrix.
"""
import matplotlib.pyplot as plt
import pandas as pa
from LABelsToolkit.tools.visualiser.graphs_and_stats import confusion_matrix
import benchmarking.cross_validation.a_paths_and_parameters_cross_validation as ph
import seaborn as sns
import path_manager


def run_get_global_measurements_barchart():

    # Load data:
    df_global_dice_score = pa.read_pickle(ph.pfi_df_global_dice_score)

    fig, ax = plt.subplots(figsize=(8, 4), nrows=len(ph.methods_names), ncols=1)
    fig.canvas.set_window_title('1 - Global dice score')
    sns.set(color_codes=True)
    if len(ph.methods_names) > 1:
        for met_num, met in enumerate(ph.methods_names):

            ax[met_num].set_title('1 - (Dice score). Method {}'.format(met))
            one_minus_dice = [1 - m for m in df_global_dice_score.T[met]]
            ax[met_num].bar(range(len(one_minus_dice)), one_minus_dice)
            ax[met_num].set_ylabel('%')
            ax[met_num].set_ylim([0, 0.2])
            ax[met_num].set_xticks(range(len(one_minus_dice)))
            ax[met_num].set_xticklabels(path_manager.atlas_subjects, ha='right', rotation=45, fontsize=6)
    else:

        ax.set_title('1 - Global Dice score'.format(ph.methods_names[0]))
        one_minus_dice = [1 - m for m in df_global_dice_score.T[ph.methods_names[0]]]
        ax.bar(range(len(one_minus_dice)), one_minus_dice)
        ax.set_ylabel('%')
        ax.set_ylim([0, 0.2])
        ax.set_xlabel('Subject Id')
        ax.set_xticks(range(len(one_minus_dice)))
        ax.set_xticklabels(path_manager.atlas_subjects, ha='center', rotation=45, fontsize=10)
        ax.xaxis.labelpad = 20

    plt.tight_layout()
    plt.savefig(ph.pfi_barchart_global_dice_score_per_subjects, format='pdf', dpi=200)

    # confusion matrix is useful when more than one method is applied and compared:
    confusion_matrix(df_global_dice_score, fig_size=(8, 6), title='Leave-1-out cv: Global dice score',
                     pfi_where_to_save=None, show_fig=True)
    plt.show()


if __name__ == '__main__':
    run_get_global_measurements_barchart()
