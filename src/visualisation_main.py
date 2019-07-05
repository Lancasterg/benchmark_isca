import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

dir_loc = '/Users/george/isca_python/visualisation/bcp3/whole_node/held_suarez/'


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


def main():
    filename = 'held_suarez_8_T85.csv'
    df = pd.read_csv(dir_loc + filename, delimiter=',')
    df = df[df.Epoch != 'Total']
    df['Epoch'] = df['Epoch'].astype(float)
    print('Mean', df['Time'].mean())
    print('Standard deviation', df['Time'].std())
    print('Variance', df['Time'].var())


if __name__ == '__main__':
    main()
