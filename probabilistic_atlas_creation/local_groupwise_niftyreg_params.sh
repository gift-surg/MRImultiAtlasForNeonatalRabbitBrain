#!/bin/bash
############################################################################
###################### PARAMETERS THAT CAN BE CHANGED ######################
############################################################################


export IMG_INPUT=(`ls subjects/*.nii.gz`)
echo $IMG_INPUT
export IMG_INPUT_MASK=(`ls masks/*.nii.gz`) # leave empty to not use floating masks
echo $IMG_INPUT_MASK

echo 'Selected images: '
printf '%s\n' "${IMG_INPUT[@]}"

echo 'Selected masks: '
printf '%s\n' "${IMG_INPUT_MASK[@]}"

echo 'Computations started: '

# template image to use to initialise the atlas creation
export TEMPLATE='subjects/1305_T1.nii.gz'
export TEMPLATE_MASK='masks/1305_mask.nii.gz'

# folder where the result images will be saved
export RES_FOLDER='results'

# argument to use for the affine (reg_aladin)
export AFFINE_args=" -omp 8 -speeeeed "
# argument to use for the non-rigid registration (reg_f3d)
export NRR_args=" -ln 4 -lp 2 -be 0.8  -omp 8 "

# number of affine loop to perform
export AFF_IT_NUM=7

# number of non-rigid loop to perform
export NRR_IT_NUM=7

# grid engine arguments
export QSUB_CMD="qsub -l h_rt=05:00:00 -l tmem=3.5G -l h_vmem=3.5G -l vf=3.5G -l s_stack=10240  -j y -S /bin/csh -b y -cwd -V -e /cluster/project0/fetalsurgery/Data/MRI/KUL_preterm_rabbit_model/software/z_output -o /cluster/project0/fetalsurgery/Data/MRI/KUL_preterm_rabbit_model/software/z_output"
############################################################################
