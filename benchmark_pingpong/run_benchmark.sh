#!/usr/local_rwth/bin/zsh
#SBATCH --time=00:10:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=chameleon_pingpong 
#SBATCH --output=chameleon_pingpong.%J.txt
#SBATCH --exclusive
#SBATCH --account=jara0001
#SBATCH --partition=c16m

# =============== Load desired modules
source /home/jk869269/.zshrc
source env_ch_intel.sh

# =============== Settings & environment variables
CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}

# Tests for Type 0
make
make run-sm &> ${CUR_DATE_STR}_result_type0_sm.log
make run-dm &> ${CUR_DATE_STR}_result_type0_dm.log

# Tests for Type 1
ADDITIONAL_COMPILE_FLAGS="-DBENCHMARK_TYPE=1" make
make run-sm &> ${CUR_DATE_STR}_result_type1_sm.log
make run-dm &> ${CUR_DATE_STR}_result_type1_dm.log


