import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd

import visualisation_constants as Const

# Use LaTeX fonts
plt.rc('font', family='serif')
rc('text', usetex=True)


def format_ax(ax, config):
    ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    ax.minorticks_on()
    ax.title.set_text(f'Wallclock runtime for the {config} configuration running at T42 resolution')
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    ax.set_xticklabels(['Sandy Bridge', 'Broadwell', 'Skylake', 'ThunderX2'])

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    # ax.set_xlabel(['Sandy Bridge', 'Broadwell', 'Skylake', 'ThunderX2'])


def read_data():
    colors = ['#c0df85', '#db6c79', '#aec5eb', '#e7a977']
    legend_items = ['Unmodified', 'FFTW', 'Single-precision floats', 'FFTW and single-precision floats']

    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name='opt_eval', skiprows=0, usecols='A:G')
    # df = df[df.Cluster != Const.bcp4]
    # df = df.loc[(df['Cluster'] == Const.isam) | (df['Cluster'] == Const.bp) | (df['Cluster'] == Const.bcp3)]
    df = df.dropna(axis=1)
    df_held = df[df['config'] == 'held_suarez']
    df_mars = df[df['config'] == 'grey_mars']

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(9, 8), sharex=True)
    ax = plt.gca()
    ax.xaxis.labelpad = 10
    df_held.plot.bar(x='Cluster', ax=axes[0], rot=0, legend=False, color=colors, edgecolor="black", linewidth=1,)
    df_mars.plot.bar(x='Cluster', ax=axes[1], rot=0, legend=False, color=colors, edgecolor="black", linewidth=1,)
    format_ax(axes[0], 'Held-Suarez')
    format_ax(axes[1], 'Grey-Mars')
    axes[1].legend(legend_items, loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=5)

    ax.set_xlabel('Processor Family')
    plt.savefig(f'{Const.save_path}/opt_comparison.pdf')
    plt.show()


def main():
    read_data()


if __name__ == '__main__':
    main()
