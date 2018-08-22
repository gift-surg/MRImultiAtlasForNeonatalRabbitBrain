"""
Module to run all the benchmarking cross validation in sequence on the cluster
"""
import os
import sys
from collections import OrderedDict

from benchmarking.cross_validation.b_create_flipped_multi_atlas import run_create_flipped_multi_atlas
from benchmarking.cross_validation.c_generate_automatic_segmentation_leave_one_out import run_generate_automatic_segmentation_leave_one_out
from benchmarking.cross_validation.d_separate_macro_regions import run_separate_brain_regions
from benchmarking.cross_validation.e_collect_measurements import get_global_measurements, get_local_measurements
from benchmarking.cross_validation.f1_get_barchart_global_measurements import run_get_global_measurements_barchart
from benchmarking.cross_validation.f2_get_boxplot import run_create_boxplots
from benchmarking.cross_validation.f3_get_bullseyes_leave_one_out import run_create_bull_eye_each_couple


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(dir_path))

# parser = argparse.ArgumentParser()
# parser.add_argument('-i', dest='str_input', type=str, required=True)
# args = parser.parse_args()
#
# print args.str_input


b_phases = {1: True, 2: True}
d_controller = {'verbose'              : True,
                'Nomenclature'         : 'taxonomical',
                'Divide_manual_segm'   : True,
                'Divide_automatic_segm': True}

run_create_flipped_multi_atlas(b_phases)
run_generate_automatic_segmentation_leave_one_out()
run_separate_brain_regions(d_controller)
get_global_measurements()
get_local_measurements(nomenclature=['taxonomical', 'all'])
run_get_global_measurements_barchart()
run_create_boxplots(nomenclature='all', see=True)
run_create_boxplots(nomenclature='taxonomical', see=True)
run_create_bull_eye_each_couple()
