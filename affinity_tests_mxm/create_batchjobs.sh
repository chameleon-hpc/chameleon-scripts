#!/usr/local_rwth/bin/zsh

export CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
export OUT_DIR="/home/ka387454/repos/chameleon-scripts/affinity_tests_mxm/outputs/Output_"${CUR_DATE_STR}
mkdir ${OUT_DIR}

export_vars="OUT_DIR"

sbatch --nodes=4 --ntasks-per-node=1 --job-name=mxm_affinity_testing \
--output=./outputs/mxm_test_${CUR_DATE_STR}.%J.txt \
--export=${export_vars} \
run_experiments.sh