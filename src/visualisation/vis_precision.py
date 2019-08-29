import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as mtick
import numpy as np
from matplotlib import rc

import visualisation_constants as Const

import latex_fonts


def main():
    fig, ax = plt.subplots(figsize=(8, 4))
    Const.clusters.remove(Const.bcp4)
    # Const.clusters.remove(Const.isam)
    line_colors = {Const.isam: 'red', Const.bcp3: 'magenta', Const.bcp4: 'blue', Const.bp: 'green'}
    line_colors_kind_4 = {Const.isam: 'orange', Const.bcp3: 'purple', Const.bcp4: 'yellow', Const.bp: 'brown'}
    line_styles = {Const.isam: ':o', Const.bcp3: ':^', Const.bcp4: ':s', Const.bp: ':X'}

    for cluster in Const.clusters:
        df_temp = read_data(pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name=cluster, skiprows=2,
                                          usecols='A:I'), cluster)
        df_temp.plot(x='Cores', y='Runtime', ax=ax, color=line_colors[cluster], style=line_styles[cluster],
                     markeredgecolor='black', label=f'DP {Const.cluster_proc[cluster]}')
        df_temp.plot(x='Cores', y='kind_4', ax=ax, color=line_colors_kind_4[cluster], style=line_styles[cluster],
                     markeredgecolor='black', label=f'SP {Const.cluster_proc[cluster]}')
    nice_ax(ax, Const.t42)
    plt.title('Single vs double precision floating point numbers, Held-Suarez T42')
    plt.tight_layout()
    # fig.subplots_adjust(bottom=0.13)
    plt.savefig(f'{Const.save_path}/single-double-precision.pdf')
    plt.show()


def read_data(df, cluster):
    df = df[['Runtime', 'kind_4', 'Resolution', 'Config', 'Cores']]
    df['cluster'] = cluster
    df = df.dropna(axis=0)
    df = df[df.Config == 'Held_suarez']
    df = df[df.Resolution == 'T42']
    return df


def nice_ax(ax, resolution):
    plt.yscale('log')
    ax.set_xlim(xmin=0, xmax=max(ax.get_xlim()) + 4)
    ax.set_ylim(ymin=0)
    # ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    # ax.minorticks_on()
    # ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    # ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=3)
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start, end, 2 if resolution == Const.t21 else 4 if resolution == Const.t42 else 8))

    # change ticks
    fmt = '{x:,.0f}'
    tick = mtick.StrMethodFormatter(fmt)
    ax.yaxis.set_major_formatter(tick)

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')


if __name__ == '__main__':
    main()
