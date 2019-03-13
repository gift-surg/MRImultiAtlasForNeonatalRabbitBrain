# Path manager
import os
from os.path import join as jph
import numpy as np


pfo_benchmarking_parameters_leave_one_out = ''
atlas_subjects = []

selected_target = np.random.choice(atlas_subjects)
bfc_corrector_cmd = ''

pfo_target_for_mono = jph()
pfo_target_for_multi = jph()
