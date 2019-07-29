import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn import preprocessing

dir_loc = '/Users/george/isca_python/visualisation/bcp3/whole_node/held_suarez/'
spreadsheet_dir = '/Users/george/Dropbox/university_of_bristol/thesis/data_collection/run_measurements.xlsx'
clusters = ['BCP3', 'BCP4', 'BP', 'Isambard']
configs = ['Held_suarez', 'Grey_mars']

colours = {'BCP3': ''}


def read_resolution(resolution):
    directory = os.fsencode(dir_loc)
    frames = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if resolution in filename:
            frames.append(pd.read_csv(dir_loc + filename, delimiter=','))
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
    df = pd.read_csv(dir_loc + filename, delimiter=',')
    df = df[df.Epoch != 'Total']
    df['Epoch'] = df['Epoch'].astype(float)
    print('Mean', df['Time'].mean())
    print('Standard deviation', df['Time'].std())
    print('Variance', df['Time'].var())


def process_dataframe(sheet_name, resolution, config):
    df = pd.read_excel(open(spreadsheet_dir, 'rb'), sheet_name=sheet_name, skiprows=2, usecols=[0, 1, 2, 3, 4])
    df['Cluster'] = sheet_name
    df = df[df.Resolution == resolution]
    df = df[df['Node Resources'] == 'All']
    df = df[df.Config == config]
    df = df.dropna()
    df["Runtime"] = pd.to_numeric(df["Runtime"])
    return df


def plot_scaling_graph(resolution, show_node=True):
    df_bcp3 = process_dataframe('BCP3', resolution, 'Held_suarez')
    df_bcp4 = process_dataframe('BCP4', resolution, 'Held_suarez')
    df_isam = process_dataframe('Isambard', resolution, 'Held_suarez')
    df_bp = process_dataframe('BP', resolution, 'Held_suarez')

    fig, ax = plt.subplots()
    df_isam.plot(kind='scatter', x='Cores', y='Runtime', ax=ax, color='red', edgecolors='black', s=30, legend=True)
    df_bcp3.plot(kind='scatter', x='Cores', y='Runtime', ax=ax, color='orange', edgecolors='black', s=30, legend=True)
    df_bcp4.plot(kind='scatter', x='Cores', y='Runtime', ax=ax, color='blue', edgecolors='black', s=30, legend=True)
    df_bp.plot(kind='scatter', x='Cores', y='Runtime', ax=ax, color='green', edgecolors='black', s=30, legend=True)

    ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    ax.legend(['Isambard', 'BCP3', 'BCP4', 'Bluepebble'])
    plt.title(f'Resolution = {resolution}')

    if show_node:
        if resolution == 'T85':
            ax.axvline(x=64, linewidth=3, color='red', ymin=0.5)
        ax.axvline(x=16, linewidth=3, color='orange', ymin=0.5)
        ax.axvline(x=28, linewidth=3, color='green', ymin=0.5)
        ax.axvline(x=24, linewidth=3, color='blue', ymin=0.5)

    plt.show()


def fix_data():
    df = pd.read_csv('/Users/george/benchmark_isca/data/bluepebble/grey_mars_4_T42.csv')
    df = df.append(
        pd.DataFrame([[4, 'T42', 'Total', df['Time'].sum()]], columns=['Cores', 'Resolution', 'Epoch', 'Time']))
    print(df)


def plot_bar_graph(resolution, config):
    arr = []
    for cluster in clusters:
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
    for cluster in clusters:
        for config in configs:
            df_temp = process_dataframe(cluster, resolution, config)
            df_temp_min = df_temp.loc[df_temp['Runtime'].idxmin(), :]
            arr.append(df_temp_min)
    df = pd.DataFrame(arr)
    df_plot = pd.DataFrame([df[(df.Config == config)]['Runtime'].reset_index(drop=True) for config in configs],
                           index=configs).T
    df_plot.rename(index={0: 'BCP3', 1: 'BCP4', 2: 'BP', 3: 'Isambard'}, inplace=True)
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


def main():
    # plot_total_program()
    # plot_split_bar_graph('T42')
    # plot_scaling_graph('T21')
    # plot_scaling_graph('T42')
    # plot_scaling_graph('T85')
    plot_bar_graph('T42', 'Held_suarez')


if __name__ == '__main__':
    main()
