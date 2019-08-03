#!/bin/bash

#SBATCH --job-name=benchmark_held_suarez_thirty_two
#SBATCH --partition=cpu
#SBATCH --time=14-00:00:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=16
#number of cpus (cores) per task (process)
#SBATCH --cpus-per-task=1
#SBATCH --output=held_suarez_sixteen_cores_%j.o
#SBATCH --mail-type=ALL
#SBATCH --mail-user=qv18258@bristol.ac.uk


echo Running on host `hostname`
echo Time is `date`
echo Directory is `pwd`


module purge
source $HOME/.bashrc
source $GFDL_BASE/src/extra/env/bristol-bc4
source activate isca_env


$HOME/.conda/envs/isca_env/bin/python $BENCHMARK_ISCA/src/main.py -mincores 16 -maxcores 16 -r T21 -r T42 -r T85 -codebase held_suarez