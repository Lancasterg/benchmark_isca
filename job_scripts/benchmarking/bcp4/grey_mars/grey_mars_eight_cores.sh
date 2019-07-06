#!/bin/bash

#SBATCH --job-name=benchmark_grey_mars_eight_cores
#SBATCH --partition=cpu
#SBATCH --time=5-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#number of cpus (cores) per task (process)
#SBATCH --cpus-per-task=1
#SBATCH --output=grey_mars_eight_cores_%j.o
#SBATCH --mail-type=ALL
#SBATCH --mail-user=qv18258@bristol.ac.uk


echo Running on host `hostname`
echo Time is `date`
echo Directory is `pwd`


module purge
source $HOME/.bashrc
source $GFDL_BASE/src/extra/env/bristol-bc4
source activate isca_env


$HOME/.conda/envs/isca_env/bin/python $BENCHMARK_ISCA/src/main.py -mincores 8 -maxcores 8 -r T21 -r T42 -r T85 -codebase grey_mars