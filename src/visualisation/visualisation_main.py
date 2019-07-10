import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

dir_loc = '/Users/george/isca_python/visualisation/bcp3/whole_node/held_suarez/'
spreadsheet_dir = '/Users/george/Dropbox/university_of_bristol/thesis/data_collection/run_measurements.xlsx'


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
    df = df[df.Config == 'Held_suarez']
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
    df_bcp3 = process_dataframe('BCP3', resolution, config)
    df_bcp3_max = df_bcp3.loc[df_bcp3['Runtime'].idxmin(), :]

    df_bcp4 = process_dataframe('BCP4', resolution, config)
    df_bcp4_max = df_bcp4.loc[df_bcp4['Runtime'].idxmin(), :]

    df_bp = process_dataframe('BP', resolution, config)
    df_bp_max = df_bp.loc[df_bp['Runtime'].idxmin(), :]

    df_isam = process_dataframe('Isambard', resolution, config)
    df_isam_max = df_isam.loc[df_isam['Runtime'].idxmin(), :]

    df = pd.DataFrame([df_bcp3_max, df_bcp4_max, df_bp_max, df_isam_max])

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


def main():
    # plot_scaling_graph('T21')
    # plot_scaling_graph('T42')
    # plot_scaling_graph('T85')
    plot_bar_graph('T42', 'Grey_mars')


if __name__ == '__main__':
    main()
