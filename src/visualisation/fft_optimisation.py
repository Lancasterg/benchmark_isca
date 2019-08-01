import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rc

import visualisation_constants as Const

# Use LaTeX fonts
plt.rc('font', family='serif')
rc('text', usetex=True)


def read_fftw_data(sheet_name):
    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name=sheet_name, skiprows=2, usecols='J:N')
    df['Cluster'] = sheet_name
    df = df.dropna()
    df = df.drop('vanilla_iteration', axis=1)
    df = df.drop('fftw_iteration', axis=1)
    return df


def plot_fft_data(sheet_name):
    df = read_fftw_data(sheet_name)

    colors = ["#3a7ca5", "#d00000"]

    df.plot.bar(x='grid_size', rot=0, color=colors, edgecolor="black", linewidth=1, figsize=(8, 5))

    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

    ax.legend(['Temperton FFT', 'FFTW'])

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    plt.title(f'Performance comparison of Temperton FFT and FFTW: {Const.cluster_proc[sheet_name]}')
    plt.xlabel('Grid size')
    plt.ylabel('Runtime (Seconds)')
    ax.set_xticklabels(['128x64 (T42)', '256x128 (T85)', '512x256 (T170)'])
    plt.savefig(f'{Const.save_path}/{sheet_name}_fft.pdf')
    plt.show()


def main():
    plot_fft_data(Const.bcp3)
    plot_fft_data(Const.bp)
    plot_fft_data(Const.isam)


if __name__ == '__main__':
    main()
