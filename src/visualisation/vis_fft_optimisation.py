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
    df = df.drop('vanilla-iteration', axis=1)
    df = df.drop('fftw-iteration', axis=1)
    return df


def plot_fft_data(df, ax):
    colors = ["#3a7ca5", "#d00000"]

    df.plot.bar(x='grid_size', rot=0, color=colors, edgecolor="black", linewidth=1, ax=ax, legend=False)

    ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    ax.set_title(f'{Const.cluster_proc[sheet_name]}')
    ax.set_xlabel('Grid size')
    ax.set_ylabel('Runtime (Seconds)')
    ax.set_xticklabels(['128x64 (T42)', '256x128 (T85)', '512x256 (T170)'])


def plot_data(ax, df, res):
    colors = ["#3a7ca5", "#d00000"]
    resolutions = {'64x32': 'T21', '128x64': 'T42', '256x128': 'T85', '512x256': 'T170'}

    df[df['grid-size'] == res].plot.bar(x='Cluster', ax=ax, rot=0, color=colors, edgecolor="black", legend=False,
                                        linewidth=1)
    ax.set_xticklabels(['ThunderX2', 'Sandy Bridge', 'Broadwell', 'Skylake'])
    ax.set_xlabel('Processor family')
    ax.set_ylabel('Runtime (Seconds)')

    a = resolutions[res]
    ax.set_title(f'{res} ({a})')

    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='black')

    ax.set_ylabel('Runtime (seconds)')
    # ax.minorticks_on()
    # ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    # ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')


def main():
    fig, axes = plt.subplots(2, 2, figsize=(10, 6))

    df = read_fftw_data(Const.isam)
    df = df.append(read_fftw_data(Const.bcp3))
    df = df.append(read_fftw_data(Const.bcp4))
    df = df.append(read_fftw_data(Const.bp))

    plot_data(axes[0, 0], df, '64x32')
    plot_data(axes[0, 1], df, '128x64')
    plot_data(axes[1, 0], df, '256x128')
    plot_data(axes[1, 1], df, '512x256')
    axes[0, 1].set_ylabel('')
    axes[1, 1].set_ylabel('')

    axes[0, 0].set_xlabel('')
    axes[0, 1].set_xlabel('')
    axes[1, 0].set_xlabel('Processor Family')
    axes[1, 1].set_xlabel('Processor Family')

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, ['Temperton FFT', 'FFTW'], loc=(0.35, 0), ncol=5)
    plt.tight_layout()
    plt.savefig(f'{Const.save_path}/compare_fft.pdf')
    plt.show()

    # plot_fft_data(Const.bcp3, axes[0, 0])
    # plot_fft_data(Const.bcp4, axes[0, 1])
    # plot_fft_data(Const.bp, axes[1, 0])
    # plot_fft_data(Const.isam, axes[1, 1])
    #

    # axes[0, 1].set_ylabel('')
    # axes[1, 1].set_ylabel('')
    # plt.tight_layout()
    # plt.savefig(f'{Const.save_path}/compare_fft.pdf')
    # plt.show()


if __name__ == '__main__':
    main()
