#!/usr/local_rwth/bin/zsh
##SBATCH --job-name=samoa_chameleon
##SBATCH --output=output_samoa_chameleon.%J.txt
#SBATCH --time=01:00:00
#SBATCH --partition=c18m
#SBATCH --account=thes0986

#SBATCH --hwctr=vtune ##! vtune
module load intelvtune #! vtune

source ./samoa_load_modules.sh

/rwthfs/rz/SW/intel/vtune/XE2020-u01/vtune_profiler_2020.1.0.607630/bin64/vtune -collect hotspots -app-working-dir /home/ka387454/repos/chameleon-scripts/samoa_claix -- /home/ka387454/repos/chameleon-scripts/samoa_claix/samoa_chameleon_run_batch.sh