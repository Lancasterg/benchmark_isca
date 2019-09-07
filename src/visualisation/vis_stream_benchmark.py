import visualisation_constants as Const
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import rc
import numpy as np

import latex_fonts


def main():
    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name='benchmarks', skiprows=1,
                       usecols='A:M')
    for cluster in Const.clusters:
        df[cluster] = df[cluster] / 1000

    fig, ax = plt.subplots(figsize=(7, 3.5))
    df.plot.line(x='Threads', style=['m:^', 'b:s', 'g:X', 'r:o'], markeredgecolor='black', ax=ax)
    nice_ax(ax)
    plt.savefig(f'{Const.save_path}/stream-triad.pdf')
    plt.show()


def nice_ax(ax):
    """
    Prettify axes
    """
    plt.loglog()
    legend_items = ['Sandy Bridge', 'Broadwell', 'Skylake', 'ThunderX2']
    plt.title('STREAM TRIAD memory-bandwidth measurments')
    ax.set_axisbelow(True)
    ax.set_ylabel('Memory-bandwidth (GB/s)')
    # ax.grid(which='major', linestyle=':', linewidth='0.5', color='black')
    ax.legend(legend_items, loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=5)

    # change ticks
    fmt = '{x:,.0f}'
    tick = mtick.StrMethodFormatter(fmt)
    ax.yaxis.set_major_formatter(tick)
    ax.xaxis.set_major_formatter(tick)

    ax.xaxis.set_ticks([1, 20, 200])
    ax.yaxis.set_ticks([100, 1000])
    plt.tight_layout()
    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')


if __name__ == '__main__':
    main()
