# Running Samoa on CLAIX-2018

## Prerequisites

* In order to run realistic scenarios based on measurements you need ASAGI (https://github.com/TUM-I5/ASAGI)
* Build and install ASAGI to a user directory of your choice using CMake

## Build Samoa Experiments (Example)

```bash
# setting env variables
export ASAGI_DIR="/work/jk869269/repos/hpc-projects/chameleon/ASAGI_install"
export SAMOA_DIR="/work/jk869269/repos/hpc-projects/chameleon/samoa-chameleon"

# build various scenarios
zsh samoa_chameleon_build.sh
```

## Run Samoa Experiments (Example)

```bash
# setting env variables
export SAMOA_DIR="/work/jk869269/repos/hpc-projects/chameleon/samoa-chameleon"
export SAMOA_OUTPUT_DIR="/work/jk869269/repos/hpc-projects/chameleon/samoa-output"

# make sure that the ouput dir exists event if nothing will be written to it
mkdir -p ${SAMOA_OUTPUT_DIR}

export ASAGI_PARAMS="-fbath /work/jk869269/repos/hpc-projects/chameleon/samoa_data/tohoku_static/bath.nc -fdispl /work/jk869269/repos/hpc-projects/chameleon/samoa_data/tohoku_static/displ.nc"

# build various scenarios
sbatch --export=SAMOA_DIR,SAMOA_OUTPUT_DIR,ASAGI_PARAMS samoa_chameleon_run_batch.sh

# automatically create different batch jobs testing balanced and imbalanced
zsh ./create_batchjobs.sh
```

 
