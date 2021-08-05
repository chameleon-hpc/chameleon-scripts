#!/usr/local_rwth/bin/zsh

# ============================================================
# ===== Parameters
# ============================================================
export ASAGI_DIR=${ASAGI_DIR:-"/path/to/ASAGI_install"}
export SAMOA_DIR=${SAMOA_DIR:-"/path/to/samoa_chameleon"}
export SAMOA_PATCH_ORDER=${SAMOA_PATCH_ORDER:-7}
export DG_LIMITER=${DG_LIMITER:-"unlimited"}

# 0: no chameleon
# 1: chameleon version
# 2: no chameleon but same packing methods required to run chameleon (fair comparison)
#CHAMELEON_VALUES=(0 1 2)
CHAMELEON_VALUES=(1)

# ============================================================
# ===== Loading Modules
# ============================================================
source ./samoa_load_modules.sh

# ============================================================
# ===== DEBUG Output
# ============================================================
echo "===== DEBUG Output ====="
echo "ASAGI_DIR=${ASAGI_DIR}"
echo "SAMOA_DIR=${SAMOA_DIR}"
module list
echo "===== DEBUG Output ====="

# ============================================================
# ===== Building targets
# ============================================================
# remeber previous directory
CUR_DIR=$(pwd)
# switch to samoa directory
cd ${SAMOA_DIR}
# build different versions of samoa
for cur_ch in "${CHAMELEON_VALUES[@]}"
do
    # standard builds # boundary=file?
    EXE_NAME="samoa_swe_radial_chameleon_${cur_ch}"
    #scons machine=host asagi=off target=release scenario=swe swe_patch_order=${SAMOA_PATCH_ORDER} swe_scenario=radial_dam_break chameleon=${cur_ch} flux_solver=aug_riemann assertions=on compiler=intel exe=${EXE_NAME} -j8
    EXE_NAME="samoa_swe_oscillating_chameleon_${cur_ch}"
    #scons machine=host asagi=off target=release scenario=swe swe_patch_order=${SAMOA_PATCH_ORDER} swe_scenario=oscillating_lake chameleon=${cur_ch} flux_solver=aug_riemann assertions=on compiler=intel exe=${EXE_NAME} -j8
    EXE_NAME="samoa_swe_asagi_chameleon_${cur_ch}"
    scons machine=host asagi=on  target=release scenario=swe swe_patch_order=${SAMOA_PATCH_ORDER}                               chameleon=${cur_ch} flux_solver=aug_riemann assertions=on compiler=intel exe=${EXE_NAME} asagi_dir=${ASAGI_DIR} -j8
done
# go back to previous directory
cd ${CUR_DIR}
