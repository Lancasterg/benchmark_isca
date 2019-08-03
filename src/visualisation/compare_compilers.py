import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rc

import visualisation_constants as Const

# Use LaTeX fonts
plt.rc('font', family='serif')
rc('text', usetex=True)


def read_compiler_data(sheet_name, resolution, config, compilers):
    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name=sheet_name, skiprows=2,
                       usecols='A:I')
    headings = ['Node Resources', 'Cores', 'Config', 'Resolution']
    headings.extend(compilers)

    df['Cluster'] = sheet_name
    df = df[df.Resolution == resolution]
    df = df[df.Config == config]
    df = df[headings]
    df = df.dropna()

    for compiler in compilers:
        df[compiler] = pd.to_numeric(df[compiler])
    return df


def plot_compiler_data(cluster, resolution, config, compilers):
    df = read_compiler_data(cluster, resolution, config, compilers)
    df_cores = df['Cores']
    df = df.drop('Cores', axis=1)
    colors = ["#3a7ca5", "#d00000"]

    df.plot.bar(rot=0, color=colors, edgecolor="black", linewidth=1, figsize=(8, 5))

    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    ax.legend(compilers)

    plt.title(format_title_string(compilers, cluster, config, resolution))
    plt.xlabel('Number of processor cores')
    plt.ylabel('Runtime (Seconds)')
    ax.set_xticklabels(df_cores)

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    plt.show()


def format_title_string(compilers, cluster, config, resolution):
    if len(compilers) == 3:
        compiler_string = f'{compilers[0]}, {compilers[1]} and {compilers[2]}'
    elif len(compilers) == 2:
        compiler_string = f'{compilers[0]} and {compilers[1]}'
    else:
        compiler_string = compilers[0]

    title_config = config.split('_')[0].capitalize() + '-' + config.split('_')[1].capitalize()

    return f'Performance comparison of the {compiler_string} compilers running the {title_config} configuration \n ' \
           f'at {resolution} resolution on the {Const.cluster_proc[cluster]} processor at varying core counts'


def main():
    plot_compiler_data(Const.isam, Const.t42, Const.held_suarez, [Const.gnu, Const.cce])


if __name__ == '__main__':
    main()
