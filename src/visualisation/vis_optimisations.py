import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd

import visualisation_constants as Const

import latex_fonts


def format_ax(ax, config):
    print()
    ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='black')
    ax.title.set_text(f'{config} at T42 resolution')
    # ax.set_xlabel('Processor Family')
    ax.set_xticklabels(['Sandy Bridge', 'Broadwell', 'Skylake', 'ThunderX2'])

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    # ax.set_xlabel(['Sandy Bridge', 'Broadwell', 'Skylake', 'ThunderX2'])


def read_data():
    colors = ['#c0df85', '#db6c79', '#aec5eb', '#e7a977']
    legend_items = ['Unmodified', 'FFTW', 'Single-precision floats', 'FFTW and single-precision floats']

    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name='opt_eval', skiprows=0, usecols='A:G', nrows=8)
    # df = df[df.Cluster != Const.bcp4]
    # df = df.loc[(df['Cluster'] == Const.isam) | (df['Cluster'] == Const.bp) | (df['Cluster'] == Const.bcp3)]
    # df = df.dropna(axis=1)
    df_held = df[df['config'] == 'held_suarez']
    df_mars = df[df['config'] == 'grey_mars']

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    ax = plt.gca()
    ax.xaxis.labelpad = 10
    df_held.plot.bar(x='Cluster', ax=axes[0], rot=0, legend=False, color=colors, edgecolor="black", linewidth=1, )
    df_mars.plot.bar(x='Cluster', ax=axes[1], rot=0, legend=False, color=colors, edgecolor="black", linewidth=1, )
    format_ax(axes[0], 'Held-Suarez')
    format_ax(axes[1], 'Grey-Mars')

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, ['Unmodified', 'FFTW ($A$)', 'Single precision ($B$)', 'Single precision FFTW ($A$ + $B$)'],
               loc=(0.1, -0.01), ncol=5)

    axes[1].set_ylabel('')
    axes[1].set_xlabel('Processor family')
    axes[0].set_xlabel('Processor family')

    plt.tight_layout()
    fig.subplots_adjust(bottom=0.2)

    plt.savefig(f'{Const.save_path}/opt_comparison.pdf')
    plt.show()


def read_speedup_data(config, col_names):
    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name='opt_eval', skiprows=0, usecols='A:J', nrows=8)
    df = df[df['config'] == config]
    df = df[['fftw_speedup', '4_kind_speedup', 'fftw_4_kind_speedup']]
    df = df.rename(columns={'fftw_speedup': col_names[0],
                            '4_kind_speedup': col_names[1],
                            'fftw_4_kind_speedup': col_names[2]})
    return df


def plot_speedup():
    fftw = 'FFTW ($A$)'
    sp = 'Single precision ($B$)'
    fftw_sp = 'Single precision FFTW ($A$ + $B$)'
    colours = ['#db6c79', '#aec5eb', '#e7a977']

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    legend_items = [fftw, sp, fftw_sp]
    df_held = read_speedup_data('held_suarez', legend_items)
    df_mars = read_speedup_data('grey_mars', legend_items)

    df_held.plot.bar(ax=ax[0], color=colours, edgecolor="black", linewidth=1, legend=False, rot=0)
    df_mars.plot.bar(ax=ax[1], color=colours, edgecolor="black", linewidth=1, legend=False, rot=0)
    handles, labels = ax[0].get_legend_handles_labels()
    format_ax(ax[0], 'Held-Suarez')
    format_ax(ax[1], 'Grey-Mars')
    ax[0].set_ylabel('Speedup relative to unmodified model')
    ax[1].set_ylabel('')
    ax[1].set_xlabel('Processor family')
    ax[0].set_xlabel('Processor family')


    fig.legend(handles, legend_items, loc=(0.1, -0.01), ncol=5)
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.2)
    plt.savefig(f'{Const.save_path}/speedup-opt.pdf')
    plt.show()


def main():
    read_data()
    plot_speedup()


if __name__ == '__main__':
    main()
