from util_scale import *


def main():
    max_cores, min_cores, codebase_name, res_list, iteration = parse_arguments()
    core_list = get_core_list(max_cores, min_cores)
    res_list = get_resolution_list(res_list)
    cb, diag, namelist = setup_experiment(codebase_name)
    cb.executable_name = cb.executable_name + '+pat'

    for i, ncores in enumerate(core_list):
        for j, resolution in enumerate(res_list):
            exp_name = f'trace_{codebase_name}_{ncores}_{resolution[0]}'
            exp = Experiment(f'{exp_name}', codebase=cb)
            exp.clear_rundir()
            exp.rm_datadir()
            exp.diag_table = diag
            exp.namelist = namelist.copy()
            exp.set_resolution(*resolution)
            exp.run(1, use_restart=False, num_cores=ncores, save_run=True)


if __name__ == '__main__':
    main()
