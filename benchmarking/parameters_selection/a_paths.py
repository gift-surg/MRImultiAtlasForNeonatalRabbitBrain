# Path manager
import os
import path_manager
from os.path import join as jph
import numpy as np


pfo_mutli_atlas_leave_one_out = jph('/Users/sebastiano/a_data/TData/B1_leave_one_out/A_MultiAtlas_Neonatal')
atlas_subjects = path_manager.atlas_subjects

np.random.seed(42)
selected_target = '1702'  # np.random.choice(atlas_subjects)

pfo_target = jph('/Users/sebastiano/a_data/TData/B1_leave_one_out', selected_target)

bfc_corrector_cmd = path_manager.bfc_corrector_cmd


