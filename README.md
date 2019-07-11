# benchmark_isca
### A collection of Python and Bash scripts for automating runtime and trace data collection for the Isca climate model.

This repository acts as an add-on to the Isca climate model. It can be used to measure the run times of the model on the 
following supercomputers managed by the Advanced Computing Research Centre (ACRC) the University of Bristol:

- BlueCrystal phase 3
- BlueCrystal phase 4
- Bluepebble
- Isambard
- ~~Catalyst~~

You can find the Isca climate model repository at `https://github.com/ExeClim/Isca`

To run the scripts, you must first export the `BENCHMARK_ISCA` and `GFDL_BENCH` environment variable in your .bashrc
```
export BENCHMARK_ISCA=/newhome/<username>/benchmark_isca
export GFDL_BENCH=/newhome/<username>/isca_home/gfdl_bench
```

There are a number of job files for both PBS and Slurm job schedulers. These can be submitted using `qsub <job>.job` or 
`sbatch<job>.sh` respectively. 