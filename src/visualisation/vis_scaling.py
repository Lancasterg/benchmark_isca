import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import os
from sklearn import preprocessing
import matplotlib.ticker as mtick
import itertools
import numpy as np

import visualisation_constants as Const

# Use LaTeX fonts
plt.rc('font', family='serif')
rc('text', usetex=True)


def read_resolution(resolution):
    directory = os.fsencode(Const.dir_loc)
    frames = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if resolution in filename:
            frames.append(pd.read_csv(Const.dir_loc + filename, delimiter=','))
    df = pd.concat(frames)
    return df


def plot_resolution(df):
    fig, ax = plt.subplots()
    df.plot(kind='scatter', x='Cores', y='Time', ax=ax, edgecolors='black', s=30)
    ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()


def plot_all_resolutions():
    resolutions = ['T21', 'T42', 'T85']
    for resolution in resolutions:
        df = read_resolution(resolution)
        df = df[df.Epoch == 'Total']
        plot_resolution(df)


def runtime_stats():
    filename = 'held_suarez_8_T85.csv'
    df = pd.read_csv(Const.dir_loc + filename, delimiter=',')
    df = df[df.Epoch != 'Total']
    df['Epoch'] = df['Epoch'].astype(float)
    print('Mean', df['Time'].mean())
    print('Standard deviation', df['Time'].std())
    print('Variance', df['Time'].var())


def process_dataframe(sheet_name, resolution, config):
    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name=sheet_name, skiprows=2, usecols=[0, 1, 2, 3, 4])
    df['Cluster'] = sheet_name
    df = df[df.Resolution == resolution]
    df = df[df['Node Resources'] == 'All']
    df = df[df.Config == config]
    df = df.dropna()
    df["Runtime"] = pd.to_numeric(df["Runtime"])
    return df


def lookup_scale(resolution, config):
    scale = {}
    if resolution == Const.t21:
        scale = {Const.held_suarez: [1000, 10000], Const.grey_mars: [10000, 100000]}
    elif resolution == Const.t42:
        scale = {Const.held_suarez: [1000, 10000, 10000], Const.grey_mars: [10000, 100000, 1000000]}
    elif resolution == Const.t85:
        scale = {Const.held_suarez: [10000, 100000]}

    return scale[config]



def plot_scaling_graph(resolution, config, show_node=True):
    df_bcp3 = process_dataframe(Const.bcp3, resolution, config)
    df_bcp4 = process_dataframe(Const.bcp4, resolution, config)
    df_isam = process_dataframe(Const.isam, resolution, config)
    df_bp = process_dataframe(Const.bp, resolution, config)

    fig, ax = plt.subplots()

    df_isam.plot(kind='line', x='Cores', y='Runtime', ax=ax, color='red', style=':o', markeredgecolor='black', ms=5,
                 zorder=2)
    df_bcp3.plot(kind='line', x='Cores', y='Runtime', ax=ax, color='magenta', style=':^', markeredgecolor='black', ms=5,
                 zorder=2)
    df_bcp4.plot(kind='line', x='Cores', y='Runtime', ax=ax, color='blue', style=':s', markeredgecolor='black', ms=5,
                 zorder=2)
    df_bp.plot(kind='line', x='Cores', y='Runtime', ax=ax, color='green', style=':X', markeredgecolor='black', zorder=2,
               ms=5)

    plt.yscale('log')
    ax.set_xlim(xmin=0, xmax=max(ax.get_xlim()) + 4)
    # ax.set_ylim(ymin=0)
    ax.set_ylabel('Wallclock runtime (seconds)')

    ax.legend(['ThunderX2', 'Sandy Bridge', 'Broadwell', 'Skylake'], loc='upper center', bbox_to_anchor=(0.5, -0.2),
              fancybox=True, shadow=True, ncol=5)

    # x ticks
    ax.xaxis.set_ticks(Const.xtick_dict[resolution])

    # y ticks
    fmt = '{x:,.0f}'
    tick = mtick.StrMethodFormatter(fmt)
    ax.yaxis.set_major_formatter(tick)

    ax.yaxis.set_ticks(lookup_scale(resolution, config))

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    title_config = config.split('_')[0].capitalize() + '-' + config.split('_')[1].capitalize()
    plt.title(f'Wallclock runtime for the {title_config} simulation using {resolution} resolution')
    plt.xlabel('Number of processor cores')

    if show_node:
        if resolution == 'T85':
            ax.axvline(x=64, linewidth=1, color='red', ymin=0, zorder=1)
        ax.axvline(x=16, linewidth=1, color='purple', ymin=0, zorder=1)
        ax.axvline(x=28, linewidth=1, color='green', ymin=0, zorder=1)
        ax.axvline(x=24, linewidth=1, color='blue', ymin=0, zorder=1)
    plt.tight_layout()
    plt.savefig(f'{Const.save_path}/scaling_graph_{resolution}_{config}.pdf')
    plt.show()


def fix_data():
    df = pd.read_csv('/Users/george/benchmark_isca/data/bluepebble/grey_mars_4_T42.csv')
    df = df.append(
        pd.DataFrame([[4, 'T42', 'Total', df['Time'].sum()]], columns=['Cores', 'Resolution', 'Epoch', 'Time']))
    print(df)


def plot_bar_graph(resolution, config):
    arr = []
    for cluster in Const.clusters:
        df_temp = process_dataframe(cluster, resolution, config)
        df_temp_min = df_temp.loc[df_temp['Runtime'].idxmin(), :]
        arr.append(df_temp_min)

    df = pd.DataFrame(arr)

    ax = df.plot.bar(x='Cluster', y='Runtime', rot=0, edgecolor="black", linewidth=0.5)
    ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.title(f'Total program runtime for {config}, resolution: {resolution}')
    # Could annotate the number of cores used...
    plt.show()


def plot_split_bar_graph(resolution):
    arr = []
    for cluster in Const.clusters:
        for config in Const.configs:
            df_temp = process_dataframe(cluster, resolution, config)
            df_temp_min = df_temp.loc[df_temp['Runtime'].idxmin(), :]
            arr.append(df_temp_min)
    df = pd.DataFrame(arr)
    df_plot = pd.DataFrame([df[(df.Config == config)]['Runtime'].reset_index(drop=True) for config in Const.configs],
                           index=Const.configs).T
    df_plot.rename(index={0: Const.bcp3, 1: Const.bcp4, 2: Const.bp, 3: Const.isam}, inplace=True)
    axes = df_plot.plot.bar(rot=0, subplots=True, edgecolor="black", linewidth=0.5)
    for ax in axes:
        ax.set_axisbelow(True)
        ax.set_ylabel('Wallclock runtime (seconds)')
        ax.minorticks_on()
        ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
        ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()


def plot_total_program():
    data_list = ['bcp3/grey_mars_16_T42.csv', 'bcp4/grey_mars_16_T42.csv', 'isambard/grey_mars_32_T42.csv']
    plt.figure()
    ax = plt.gca()
    for data in data_list:
        df = pd.read_csv(f'/Users/george/benchmark_isca/data/{data}', skiprows=0)
        df = df[df.Epoch != 'Total']
        times = df[['Time']].values.astype(float)
        min_max_scaler = preprocessing.MinMaxScaler()
        times_scaled = min_max_scaler.fit_transform(times)
        df['Time'] = times_scaled
        df.plot(x='Epoch', y='Time', ax=ax, style='-o')

    ax.set_axisbelow(True)
    ax.set_ylabel('Wallclock runtime (normalised)')
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()


def plot_speedup(resolution, config):
    df_bcp3 = process_dataframe(Const.bcp3, resolution, config)
    df_bcp4 = process_dataframe(Const.bcp4, resolution, config)
    df_isam = process_dataframe(Const.isam, resolution, config)
    df_bp = process_dataframe(Const.bp, resolution, config)

    calc_speedup(df_bcp3)
    calc_speedup(df_bcp4)
    calc_speedup(df_bp)
    calc_speedup(df_isam)

    ax = plt.gca()
    scale = calc_scale(resolution)
    perfect = np.linspace(0, scale, scale + 1)
    plt.plot(perfect, perfect, color='black', linestyle=':')

    df_isam.plot(kind='line', x='Cores', y='Speedup', ax=ax, color='red', style=':o', markeredgecolor='black', ms=5,
                 zorder=2)
    df_bcp3.plot(kind='line', x='Cores', y='Speedup', ax=ax, color='magenta', style=':^', markeredgecolor='black', ms=5,
                 zorder=2)
    df_bcp4.plot(kind='line', x='Cores', y='Speedup', ax=ax, color='blue', style=':s', markeredgecolor='black', ms=5,
                 zorder=2)
    df_bp.plot(kind='line', x='Cores', y='Speedup', ax=ax, color='green', style=':X', markeredgecolor='black', ms=5,
               zorder=2)

    ax.set_xlim(xmin=0, xmax=max(ax.get_xlim()) + 4)
    ax.xaxis.set_ticks(Const.xtick_dict[resolution])

    plt.ylabel('Speedup relative to 1 core')
    plt.xlabel('Number of processor cores')
    ax.legend(['Linear scaling', 'ThunderX2', 'Sandy Bridge', 'Broadwell', 'Skylake'], loc='upper center',
              bbox_to_anchor=(0.5, -0.2),
              fancybox=True, shadow=True, ncol=3)

    # plt.yscale('log')
    # change the style of the axis spines
    # ax.set_axisbelow(True)
    # ax.minorticks_on()
    # ax.grid(which='major', linestyle=':', linewidth='0.5', color='black')
    # ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    title_config = config.split('_')[0].capitalize() + '-' + config.split('_')[1].capitalize()
    plt.title(f'Speedup for the {title_config} simulation using {resolution} resolution')

    plt.tight_layout()
    filename = f'speedup-{resolution}-{config}.pdf'
    print(filename)
    plt.savefig(f'{Const.save_path}/{filename}')
    plt.show()


def calc_speedup(df):
    df['Speedup'] = df.apply(lambda row: df['Runtime'].iloc[0] / row.Runtime, axis=1)
    return df


def calc_scale(resolution):
    return 16 if resolution == Const.t21 else 32 if resolution == Const.t42 else 64 if resolution == Const.t85 else 0


def main():
    # plot_total_program()
    # plot_split_bar_graph('T42')
    plot_pairs = list(itertools.product(Const.resolutions, Const.configs))
    plot_pairs.remove((Const.t85, Const.grey_mars))
    [plot_scaling_graph(item[0], item[1]) for item in plot_pairs]
    [plot_speedup(item[0], item[1]) for item in plot_pairs]

    # df_bcp3 = process_dataframe(Const.bcp3, Const.t85, Const.held_suarez)
    # plot_bar_graph('T42', 'Held_suarez')


if __name__ == '__main__':
    main()
