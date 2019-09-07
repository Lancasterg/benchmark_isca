import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rc
import matplotlib as mpl
import latex_fonts
from matplotlib.patches import Patch

import visualisation_constants as Const

# Use LaTeX fonts
plt.rc('font', family='serif')
rc('text', usetex=True)

h = 'Held-Suarez'
g = 'Grey-Mars'

legends = {h: ['Intel', 'GNU', 'CCE'], g: ['Intel', 'GNU']}
labels = {h: ['Sandy Bridge', 'Broadwell', 'Thunderx2'], g: ['Sandy Bridge', 'Broadwell']}


def plot_compiler_data(config, ax, res):
    """
    Plot the performance of various compilers
    """
    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name='compilers', skiprows=0,
                       usecols='A:E')
    df = df[df.Resolution == res]
    df = df[df.Config == config]
    colours = ["#3a7ca5", '#60b564']
    barlist = df.plot.bar(x='Cluster', rot=0, color=colours, edgecolor="black", linewidth=1, ax=ax, legend=False)

    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='black')
    # ax.minorticks_on()
    # ax.grid(which='major', linestyle=':', linewidth='0.5', color='black')
    # ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.set_xlabel('')

    ax.set_title(f'{config} {res}')
    ax.set_xticklabels(labels[config])


def red_bar(ax):
    """
    Change colour of CCE bar to red
    """
    bars = [rect for rect in ax.get_children() if isinstance(rect, mpl.patches.Rectangle)]
    bars[len(bars) - 2].set_facecolor('#d00000')


def main():
    legend_elements = [Patch(facecolor='#3a7ca5', edgecolor='black',
                             label='ICC'),
                       Patch(facecolor='#60b564', edgecolor='black',
                             label='GCC'),
                       Patch(facecolor='#d00000', edgecolor='black',
                             label='CCE')]

    fig, axes = plt.subplots(2, 2, figsize=(9, 6))
    plot_compiler_data('Held-Suarez', axes[0, 0], 'T21')
    plot_compiler_data('Held-Suarez', axes[0, 1], 'T42')
    plot_compiler_data('Grey-Mars', axes[1, 0], 'T21')
    plot_compiler_data('Grey-Mars', axes[1, 1], 'T42')

    red_bar(axes[0, 0])
    red_bar(axes[0, 1])

    axes[0, 0].set_ylabel('Wallclock runtime (seconds)')
    axes[1, 0].set_ylabel('Wallclock runtime (seconds)')

    axes[1, 0].set_xlabel('Processor family')
    axes[1, 1].set_xlabel('Processor family')

    fig.legend(legend_elements, ['ICC', 'GNU', 'CCE'], loc=(0.38, 0), ncol=5)
    fig.subplots_adjust(bottom=0.13)
    plt.tight_layout()
    plt.savefig(f'{Const.save_path}/compiler-comparison.pdf')
    plt.show()


if __name__ == '__main__':
    main()
