#!/usr/local_rwth/bin/zsh

export CHAM_AFF_TASK_SELECTION_STRAT=3
export CHAM_AFF_PAGE_SELECTION_STRAT=8
export CHAM_AFF_PAGE_WEIGHTING_STRAT=2
export CHAM_AFF_CONSIDER_TYPES=1
export CHAM_AFF_PAGE_SELECTION_N=3
export CHAM_AFF_TASK_SELECTION_N=3
export CHAM_AFF_MAP_MODE=0
export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=0

export AUTOMATIC_NUMA_BALANCING=0

export OMP_NUM_THREADS=47

export PROG="mxm_chameleon"

export MXM_PARAMS="1000 100 100 100 100"

#export DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-apps/applications/matrix_example}

export CHAMELEON_VERSION="chameleon/intel"

export_vars="CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,CHAM_AFF_TASK_SELECTION_STRAT,CHAM_AFF_PAGE_SELECTION_STRAT,CHAM_AFF_PAGE_WEIGHTING_STRAT,CHAM_AFF_CONSIDER_TYPES,CHAM_AFF_PAGE_SELECTION_N,CHAM_AFF_TASK_SELECTION_N,CHAM_AFF_MAP_MODE,CHAM_AFF_ALWAYS_CHECK_PHYSICAL,NO_NUMA_BALANCING,AUTOMATIC_NUMA_BALANCING,PROG,DIR_MXM_EXAMPLE"

#############
# Domain Mode
#############

#export CHAMELEON_VERSION="chameleon/intel"
#export CHAM_AFF_MAP_MODE=0
#export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=0
#export NO_NUMA_BALANCING="no_numa_balancing"
#sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=48 --job-name=affinity_mxm \
#--output=mxm_affinity_domain_nonumabal.%J.txt \
#--export=CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,\
#CHAM_AFF_TASK_SELECTION_STRAT,CHAM_AFF_PAGE_SELECTION_STRAT,CHAM_AFF_PAGE_WEIGHTING_STRAT,CHAM_AFF_CONSIDER_TYPES,CHAM_AFF_PAGE_SELECTION_N,CHAM_AFF_TASK_SELECTION_N,CHAM_AFF_MAP_MODE,CHAM_AFF_ALWAYS_CHECK_PHYSICAL \
#run_experiments.sh

#export CHAMELEON_VERSION="chameleon/intel"
#export CHAM_AFF_MAP_MODE=0
#export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=0
#export NO_NUMA_BALANCING=""
#sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=48 --job-name=affinity_mxm \
#--output=mxm_affinity_domain_numabal.%J.txt \
#--export=CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,\
#CHAM_AFF_TASK_SELECTION_STRAT,CHAM_AFF_PAGE_SELECTION_STRAT,CHAM_AFF_PAGE_WEIGHTING_STRAT,CHAM_AFF_CONSIDER_TYPES,CHAM_AFF_PAGE_SELECTION_N,CHAM_AFF_TASK_SELECTION_N,CHAM_AFF_MAP_MODE,CHAM_AFF_ALWAYS_CHECK_PHYSICAL \
#run_experiments.sh

###############
# Temporal Mode
###############

# export CHAMELEON_VERSION="chameleon/intel"
# export NO_NUMA_BALANCING="no_numa_balancing"
# export AUTOMATIC_NUMA_BALANCING=0
# export CHAM_AFF_MAP_MODE=1
# export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=0
# sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=48 --job-name=affinity_mxm \
# --output=mxm_affinity_temporal_nonumabal.%J.txt \
# --export=${export_vars} \
# run_experiments.sh

# export CHAMELEON_VERSION="chameleon/intel"
# export NO_NUMA_BALANCING="no_numa_balancing"
# export CHAM_AFF_MAP_MODE=1
# export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=1
# sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=48 --job-name=affinity_mxm \
# --output=mxm_affinity_temporal_nonumabal.%J.txt \
# --export=CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,\
# CHAM_AFF_TASK_SELECTION_STRAT,CHAM_AFF_PAGE_SELECTION_STRAT,CHAM_AFF_PAGE_WEIGHTING_STRAT,CHAM_AFF_CONSIDER_TYPES,CHAM_AFF_PAGE_SELECTION_N,CHAM_AFF_TASK_SELECTION_N,CHAM_AFF_MAP_MODE,CHAM_AFF_ALWAYS_CHECK_PHYSICAL,NO_NUMA_BALANCING \
# run_experiments.sh

# export CHAMELEON_VERSION="chameleon/intel"
# export NO_NUMA_BALANCING=""
# export CHAM_AFF_MAP_MODE=1
# export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=1
# sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=48 --job-name=affinity_mxm \
# --output=mxm_affinity_temporal_numabal.%J.txt \
# --export=CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,\
# CHAM_AFF_TASK_SELECTION_STRAT,CHAM_AFF_PAGE_SELECTION_STRAT,CHAM_AFF_PAGE_WEIGHTING_STRAT,CHAM_AFF_CONSIDER_TYPES,CHAM_AFF_PAGE_SELECTION_N,CHAM_AFF_TASK_SELECTION_N,CHAM_AFF_MAP_MODE,CHAM_AFF_ALWAYS_CHECK_PHYSICAL,NO_NUMA_BALANCING \
# run_experiments.sh



#########################################################
#   Test with varying Task selection strategy and mode  #
#########################################################

# export CHAMELEON_VERSION="chameleon/intel"
# export AUTOMATIC_NUMA_BALANCING=1
# export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=1
# for istrat in 0 1 2 3 4;
# do
#     export CHAM_AFF_TASK_SELECTION_STRAT=${istrat};
#     for imode in 0 1;
#     do
#         export CHAM_AFF_MAP_MODE=${imode};
#         sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=48 --job-name=affinity_mxm \
#         --output=mxm_test_taskstrat${istrat}_mapmode${imode}.%J.txt \
#         --export=${export_vars} \
#         run_experiments.sh;
#     done
# done

############################
# Chameleon without affinity
############################

#export CHAMELEON_VERSION="chameleon/intel_no_affinity"
#export AUTOMATIC_NUMA_BALANCING=0
#sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=48 --job-name=no_affinity_mxm \
#--output=mxm_no_affinity_nonumabal.%J.txt \
#--export=CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS \
#run_experiments.sh

# export CHAMELEON_VERSION="chameleon/intel_no_affinity"
# export AUTOMATIC_NUMA_BALANCING=1
# sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=48 --job-name=no_affinity_mxm \
# --output=mxm_no_affinity_numabal.%J.txt \
# --export=CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,AUTOMATIC_NUMA_BALANCING \
# run_experiments.sh

# teste für ohne chameleon matrix beispiel explizit einzeln um OMP_NUM_THREADS=48 nutzen zu können
##############################
# Tasking only, no chameleon #
##############################
export PROG=mxm_tasking
export AUTOMATIC_NUMA_BALANCING=1
export OMP_NUM_THREADS=48
sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=48 --job-name=no_cham_mxm \
--output=mxm_no_chameleon_numabal.%J.txt \
--export=CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,AUTOMATIC_NUMA_BALANCING,PROG,DIR_MXM_EXAMPLE \
run_experiments.sh