import os
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse

import path_manager


data_set = OrderedDict(
           {1201: ['Preterm', 'Male',   (47.6, 1.70), 'in'],
            1203: ['Preterm', 'Male',   (54.2, 1.80), 'in'],
            1305: ['Preterm', 'Male', 	(36.7, 1.68), 'in'],
            1404: ['Preterm', 'Female', (36.6, 1.38), 'in'],
            1505: ['Preterm', 'Male',   (41.6, 1.34), 'out'],
            1507: ['Preterm', 'Male',   (31.5, 1.17), 'in'],
            1510: ['Preterm', 'Male',   (33.1, 1.34), 'in'],
            1702: ['Term',    'Male',   (47.2, 1.81), 'in'],
            1805: ['Term',    'Male', 	(54.2, 1.78), 'in'],
            2002: ['Preterm', 'Female', (31.8, 1.23), 'in'],
            2502: ['Term',    'Female', (62.9, 1.65), 'in'],
            2503: ['Term',    'Female', (66.8, 1.79), 'out'],
            2702: ['Term',    'Male', 	(54.6, 1.79), 'out'],
            2608: ['Term',    'Female', (54.1, 1.79), 'out'],
            3301: ['Preterm', 'Female', (47.4, 1.59), 'in'],
            3303: ['Preterm', 'Male',   (50.3, 1.78), 'out'],
            3404: ['Term',    'Female', (43.3, 1.60), 'in'],
            })

# For graphical visualisation some points are shifted by an epsilon, to avoid overlaps.
epsilon_offset_body = 1
epsilon_offset_brain = 0.01

data_set_epsilon = OrderedDict(
           {1201: ['Preterm', 'Male',   (47.6, 1.70), 'in'],
            1203: ['Preterm', 'Male',   (54.2, 1.80 + epsilon_offset_brain), 'in'],
            1305: ['Preterm', 'Male', 	(36.7, 1.68), 'in'],
            1404: ['Preterm', 'Female', (36.6, 1.38), 'in'],
            1505: ['Preterm', 'Male',   (41.6, 1.34), 'out'],
            1507: ['Preterm', 'Male',   (31.5, 1.17), 'in'],
            1510: ['Preterm', 'Male',   (33.1, 1.34), 'in'],
            1702: ['Term',    'Male',   (47.2, 1.81), 'in'],
            1805: ['Term',    'Male', 	(54.2, 1.78 - epsilon_offset_brain), 'in'],
            2002: ['Preterm', 'Female', (31.8, 1.23), 'in'],
            2502: ['Term',    'Female', (62.9, 1.65), 'in'],
            2503: ['Term',    'Female', (66.8, 1.79), 'out'],
            2702: ['Term',    'Male', 	(54.6 - epsilon_offset_body, 1.79), 'out'],
            2608: ['Term',    'Female', (54.1 + epsilon_offset_body, 1.79), 'out'],
            3301: ['Preterm', 'Female', (47.4, 1.59), 'in'],
            3303: ['Preterm', 'Male',   (50.3, 1.78), 'out'],
            3404: ['Term',    'Female', (43.3, 1.60), 'in'],
            })

if __name__ == '__main__':

    add_id = False
    add_title = False
    include_discarded = True
    add_grid = True

    venus_marker = ur'$\u2640$'
    mars_marker = ur'$\u2642$'

    SMALL_SIZE  = 10
    MEDIUM_SIZE = 12
    BIGGER_SIZE = 14

    plt.rc('font', size=MEDIUM_SIZE)
    plt.rc('axes', titlesize=MEDIUM_SIZE)
    plt.rc('axes', labelsize=MEDIUM_SIZE)
    plt.rc('xtick', labelsize=MEDIUM_SIZE)
    plt.rc('ytick', labelsize=MEDIUM_SIZE)
    plt.rc('legend', fontsize=MEDIUM_SIZE)
    plt.rc('figure', titlesize=MEDIUM_SIZE)

    # plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    if include_discarded:
        body_we  = [data_set_epsilon[k][2][0] for k in data_set_epsilon.keys()]
        brain_we = [data_set_epsilon[k][2][1] for k in data_set_epsilon.keys()]
    else:
        body_we  = [data_set_epsilon[k][2][0] for k in data_set_epsilon.keys() if data_set_epsilon[k][3] == 'in']
        brain_we = [data_set_epsilon[k][2][1] for k in data_set_epsilon.keys() if data_set_epsilon[k][3] == 'in']

    print body_we
    print brain_we

    mu_body  = np.mean(body_we)
    mu_brain = np.mean(brain_we)

    perc_body  = [np.percentile(body_we, 25), np.percentile(body_we, 75)]
    perc_brain = [np.percentile(brain_we, 25), np.percentile(brain_we, 75)]

    std_body = np.std(body_we)
    std_brain = np.std(brain_we)

    cov = np.cov(body_we, brain_we)
    eig_val, eig_vect = np.linalg.eig(cov)
    eig_val = np.sqrt(eig_val)
    eig_vect = eig_vect.T

    a = eig_val[1]
    b = eig_val[0]
    alpha = np.arctan(eig_vect[1][1] / float(eig_vect[0][1]))

    # FIGURE:
    fig, ax = plt.subplots(figsize=(7, 6))

    if add_title:
        ax.set_position([0.1, 0.1, 0.85, 0.8])
    else:
        ax.set_position([0.1, 0.1, 0.85, 0.85])

    # --------- horizontal vertical lines
    ax.axhline(y=mu_brain, color='grey', linestyle='--')
    ax.axvline(x=mu_body, color='grey', linestyle='--')

    # -------- Patch Square std
    # rect = Rectangle((mu_body - std_body, mu_brain - std_brain), 2 * std_body, 2 * std_brain,
    #                  alpha=0.1, facecolor='grey',
    #                  # linewidth=1, edgecolor='grey', facecolor='none', linestyle='--'
    #                  )
    # ax.add_patch(rect)
    # -------- Patch Square percentile
    rect = Rectangle((perc_body[0], perc_brain[0]), perc_body[1] - perc_body[0], perc_brain[1] - perc_brain[0],
                     alpha=0.1, facecolor='grey',
                     # linewidth=1, edgecolor='grey', facecolor='none', linestyle='--'
                     )
    ax.add_patch(rect)

    # --------- Patch Ellipsoid
    elly = Ellipse((mu_body, mu_brain), b, a, angle=alpha)
    elly.set_alpha(0.3)
    ax.add_artist(elly)

    # -----------  term m:
    if include_discarded:
        data_term_m_id = [k for k in data_set_epsilon.keys() if (data_set_epsilon[k][0] == 'Term'
                                                                 and data_set_epsilon[k][1] == 'Male')]
    else:
        data_term_m_id = [k for k in data_set_epsilon.keys() if (data_set_epsilon[k][0] == 'Term'
                                                                 and data_set_epsilon[k][1] == 'Male'
                                                                 and data_set_epsilon[k][3] == 'in')]
    data_term_m_x = [data_set_epsilon[k][2][0] for k in data_term_m_id]
    data_term_m_y = [data_set_epsilon[k][2][1] for k in data_term_m_id]
    term_m    = ax.plot(data_term_m_x, data_term_m_y,
                        color='royalblue', marker=mars_marker, label='Term Male', ls='None', ms=12)

    if add_id:
        for ide, x, y in zip(data_term_m_id, data_term_m_x, data_term_m_y):
            plt.annotate(ide, xy=(x, y), xytext=(13, -14),
                         textcoords='offset points', ha='right', va='bottom')

    # -----------  term f:
    if include_discarded:
        data_term_f_id = [k for k in data_set_epsilon.keys() if (data_set_epsilon[k][0] == 'Term'
                                                                 and data_set_epsilon[k][1] == 'Female')]
    else:
        data_term_f_id = [k for k in data_set_epsilon.keys() if (data_set_epsilon[k][0] == 'Term'
                                                                 and data_set_epsilon[k][1] == 'Female'
                                                                 and data_set_epsilon[k][3] == 'in')]
    data_term_f_x  = [data_set_epsilon[k][2][0] for k in data_term_f_id]
    data_term_f_y  = [data_set_epsilon[k][2][1] for k in data_term_f_id]
    term_f    = ax.plot(data_term_f_x, data_term_f_y,
                        color='royalblue', marker=venus_marker, label='Term Female', ls='None', ms=12)
    if add_id:
        for ide, x, y in zip(data_term_f_id, data_term_f_x, data_term_f_y):
            plt.annotate(ide, xy=(x, y), xytext=(13, -14),
                         textcoords='offset points', ha='right', va='bottom')

    # -----------  preterm m:
    if include_discarded:
        data_preterm_m_id = [k for k in data_set_epsilon.keys() if (data_set_epsilon[k][0] == 'Preterm'
                                                                    and data_set_epsilon[k][1] == 'Male')]
    else:
        data_preterm_m_id = [k for k in data_set_epsilon.keys() if (data_set_epsilon[k][0] == 'Preterm'
                                                                    and data_set_epsilon[k][1] == 'Male'
                                                                    and data_set_epsilon[k][3] == 'in')]
    data_preterm_m_x = [data_set_epsilon[k][2][0] for k in data_preterm_m_id]
    data_preterm_m_y = [data_set_epsilon[k][2][1] for k in data_preterm_m_id]
    pterm_m   = ax.plot(data_preterm_m_x, data_preterm_m_y,
                        color='darkred', marker=mars_marker, label='Preterm Male', ls='None', ms=12)
    if add_id:
        for ide, x, y in zip(data_preterm_m_id, data_preterm_m_x, data_preterm_m_y):
            plt.annotate(ide, xy=(x, y), xytext=(13, 3),  # 30, -6,
                         textcoords='offset points', ha='right', va='bottom')
    # -----------  preterm f:
    if include_discarded:
        data_preterm_f_id = [k for k in data_set_epsilon.keys() if (data_set_epsilon[k][0] == 'Preterm'
                                                                    and data_set_epsilon[k][1] == 'Female')]
    else:
        data_preterm_f_id = [k for k in data_set_epsilon.keys() if (data_set_epsilon[k][0] == 'Preterm'
                                                                    and data_set_epsilon[k][1] == 'Female'
                                                                    and data_set_epsilon[k][3] == 'in')]
    data_preterm_f_x = [data_set_epsilon[k][2][0] for k in data_preterm_f_id]
    data_preterm_f_y = [data_set_epsilon[k][2][1] for k in data_preterm_f_id]
    pterm_f   = ax.plot(data_preterm_f_x, data_preterm_f_y,
                        color='darkred', marker=venus_marker, label='Preterm Female', ls='None', ms=12)
    if add_id:
        for ide, x, y in zip(data_preterm_f_id, data_preterm_f_x, data_preterm_f_y):
            plt.annotate(ide, xy=(x, y), xytext=(13, 3),  # 30, -6,
                         textcoords='offset points', ha='right', va='bottom')

    # -----------  mark the discarded with an X:
    if include_discarded:
        discarded = ax.plot([data_set_epsilon[k][2][0] for k in data_set_epsilon.keys()
                             if data_set_epsilon[k][3] == 'out'],
                               [data_set_epsilon[k][2][1] for k in data_set_epsilon.keys()
                                if data_set_epsilon[k][3] == 'out'],
                               color='red', marker='x', fillstyle='none', label='Discarded', ms=13, ls='None')

    ax.legend(loc='lower right')

    if add_title:
        if add_id:
            ax.set_title('Dataset: id number, sex, gestational age, body versus brain weight')
        else:
            ax.set_title('Dataset: sex, gestational age, body versus brain weight')
    ax.set_xlabel(r'Body weight (g)')
    ax.set_ylabel(r'Brain weight (g)')

    ax.set_xlim([25, 75])
    ax.set_ylim([1.0, 1.9])
    if add_grid:
        ax.grid(True, alpha=0.3)

    # output folder
    pfo_resulting_images_folder = path_manager.pfo_root_for_images
    if add_id:
        if include_discarded:
            plt.savefig(os.path.join(pfo_resulting_images_folder, 'f2_dataset_presetation_with_id_and_discarded.pdf'),
                        dpi=150)
        else:
            plt.savefig(os.path.join(pfo_resulting_images_folder, 'f2_dataset_presetation_with_id.pdf'), dpi=150)
    else:
        if include_discarded:
            plt.savefig(os.path.join(pfo_resulting_images_folder, 'f2_dataset_presetation_with_discarded.pdf'), dpi=150)
        else:
            plt.savefig(os.path.join(pfo_resulting_images_folder, 'f2_dataset_presetation.pdf'), dpi=150)

    plt.show()
