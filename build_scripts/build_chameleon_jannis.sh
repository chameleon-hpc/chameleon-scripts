#!/usr/local_rwth/bin/zsh

CH_SRC_DIR=${CH_SRC_DIR:-../../chameleon-lib/src/}

# clean directory first
make clean -C ${CH_SRC_DIR}

# build clang version first because of annoying fortran o file
source env_ch_target.sh
TARGET=claix_clang_target INSTALL_DIR=~/install/chameleon-lib/clang_1.0 make -C ${CH_SRC_DIR}

# API version compiled with Intel compiler
source env_ch_intel.sh
TARGET=claix_intel INSTALL_DIR=~/install/chameleon-lib/intel_1.0 make -C ${CH_SRC_DIR}


