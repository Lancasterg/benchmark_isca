from isca import Experiment
from util_output import write_to_csvfile
import argparse
import constants
import time


def parse_arguments():
    """
    Parse arguments from the command line.
    -mincores: The minimum number of cores to test
    -maxcores: The maximum number of cores to test
    -maxres: The maximum resolution to test
    -codebase: Which experiment to run. One of: held_suarez, grey_mars
    -i: Iteration number for concurrent experiments
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-maxcores', type=int, default=16, help='The maximum number of cores to test')
    parser.add_argument('-mincores', type=int, default=1, help='The minimum number of cores to test')
    parser.add_argument('-r', type=str, action='append', required=True,
                        help='A list of resolutions to test. For example: -r T21 -r T42 -r T85')
    parser.add_argument('-codebase', type=str, default='held_suarez',
                        help='Which experiment to run. One of: held_suarez, grey_mars')
    parser.add_argument('-i', type=str, default='',
                        help='Iteration number for concurrent experiments')
    parser.add_argument('-fc', type=str, help='Which Fortran compiler are you using? One of: INTEL, CRAY, GNU',
                        default='INTEL')
    args = parser.parse_args()
    iteration = ''
    if args.i != '':
        try:
            iteration = int(args.i)
        except ValueError:
            print('Argument -i must be integer')
            print('eg: -i 4')

    return args.maxcores, args.mincores, args.codebase, args.r, iteration, args.fc


def get_core_list(max_cores, min_cores):
    """
    Return a list of cores, given the maximum number of cores on a node
    :param max_cores: The maximum number of cores on a node
    :param min_cores: The minimum number of cores on a node
    """
    num_list = [1, 2, 4, 8, 16, 32, 64, 128]
    return sorted(i for i in num_list if min_cores <= i <= max_cores)


def get_resolution_list(res_list, pressure_level=25):
    """
    Return a list of usable resolutions, given a list of resolutions
    :param res_list: list of resolutions [ 'T21', 'T42', 'T85', ... ]
    :param pressure_level: number of pressure levels
    """
    return [(item, pressure_level) for item in res_list]


def setup_experiment(codebase):
    """
    Setup an experiment given the experiment name.
    :param codebase:  one of 'held_suarez', 'grey_mars'
    """
    if codebase == constants.HELD_SUAREZ:
        from config.held_suarez_config import setup_held_suarez_codebase, setup_held_suarez_diag, \
            setup_held_suarez_namelist
        return setup_held_suarez_codebase(), setup_held_suarez_diag(), setup_held_suarez_namelist()
    if codebase == constants.GREY_MARS:
        from config.grey_mars_config import setup_grey_mars_codebase, setup_grey_mars_namelist, setup_grey_mars_diag
        return setup_grey_mars_codebase(), setup_grey_mars_diag(), setup_grey_mars_namelist()
    return None


def run_experiment(ncores, codebase, diag, namelist, resolution, exp_name, codebase_name):
    """
    Measure the time taken to complete the experiment
    :param ncores: Number of processor cores to be used
    :param codebase: One of: Held-Suarez, Grey-Mars
    :param diag: Diagnostics
    :param namelist: Namelist file
    :param resolution: Resolution of simulatin. One of: T21, T42, T85
    :param exp_name: Name of the experiment
    :param codebase_name: Name of the codebase
    """
    runs = 0
    if codebase_name == constants.HELD_SUAREZ:
        runs = 13
    elif codebase_name == constants.GREY_MARS:
        runs = 23

    exp = Experiment(f'{exp_name}', codebase=codebase)
    exp.rm_datadir()
    exp.clear_rundir()
    exp.diag_table = diag
    exp.namelist = namelist.copy()
    exp.set_resolution(*resolution)
    start = time.time()
    print(exp.namelist)
    exp.run(1, use_restart=False, num_cores=ncores)
    end = time.time()
    time_delta = end - start
    data = [ncores, resolution[0], 1, time_delta]
    write_to_csvfile(f'{constants.GFDL_BENCH}/{exp_name}', data)
    for i in range(2, runs):  # 13 as there are 12 months (12+1=13)(241 for grey_mars) / (13 for held_suarez)
        start = time.time()
        exp.run(i, num_cores=ncores)
        end = time.time()
        time_delta = end - start
        data = [ncores, resolution[0], i, time_delta]
        write_to_csvfile(f'{constants.GFDL_BENCH}/{exp_name}', data)
