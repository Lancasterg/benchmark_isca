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


def plot_scaling_graph(resolution):
    df_bcp3 = pd.read_excel(open(spreadsheet_dir, 'rb'), sheet_name='BCP3', skiprows=2, usecols=[0, 1, 2, 3, 4])
    df_bcp3['Cluster'] = 'BCP3'
    df_bcp3 = df_bcp3[df_bcp3.Resolution == resolution]
    df_bcp3 = df_bcp3[df_bcp3['Node Resources'] == 'All']
    df_bcp3 = df_bcp3[df_bcp3.Config == 'Held_suarez']

    df_bcp4 = pd.read_excel(open(spreadsheet_dir, 'rb'), sheet_name='BCP4', skiprows=2, usecols=[0, 1, 2, 3, 4])
    df_bcp4['Cluster'] = 'BCP4'
    df_bcp4 = df_bcp4[df_bcp4.Resolution == resolution]
    df_bcp4 = df_bcp4[df_bcp4['Node Resources'] == 'All']
    df_bcp4 = df_bcp4[df_bcp4.Config == 'Held_suarez']

    df_isam = pd.read_excel(open(spreadsheet_dir, 'rb'), sheet_name='Isambard', skiprows=2, usecols=[0, 1, 2, 3, 4])
    df_isam['Cluster'] = 'Isam'
    df_isam = df_isam[df_isam.Resolution == resolution]
    df_isam = df_isam[df_isam['Node Resources'] == 'All']
    df_isam = df_isam[df_isam.Config == 'Held_suarez']
    df_isam = df_isam.dropna()

    df = pd.concat([df_isam, df_bcp3, df_bcp4])
    fig, ax = plt.subplots()

    df_isam.plot(kind='scatter', x='Cores', y='Runtime', ax=ax, color='red', edgecolors='black', s=30, legend=True)
    df_bcp3.plot(kind='scatter', x='Cores', y='Runtime', ax=ax, color='orange', edgecolors='black', s=30, legend=True)
    df_bcp4.plot(kind='scatter', x='Cores', y='Runtime', ax=ax, color='blue', edgecolors='black', s=30, legend=True)

    ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    ax.legend(['Isambard', 'BCP3', 'BCP4'])
    plt.show()


def main():
    plot_scaling_graph('T42')


if __name__ == '__main__':
    main()
