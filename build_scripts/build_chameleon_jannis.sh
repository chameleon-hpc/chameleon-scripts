#!/usr/local_rwth/bin/zsh

# clean directory first
make clean -C ../../src/

# build clang version first because of annoying fortran o file
source env_ch_target.sh
INSTALL_DIR=~/install/chameleon-lib/clang_1.0 make -C ../../src/

# API version compiled with Intel compiler
source env_ch_intel.sh
INSTALL_DIR=~/install/chameleon-lib/intel_1.0 make -C ../../src/


