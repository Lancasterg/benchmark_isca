import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rc

import visualisation_constants as Const

# Use LaTeX fonts
plt.rc('font', family='serif')
rc('text', usetex=True)

h = 'Held-Suarez'
g = 'Grey-Mars'

legends = {h: ['Intel', 'GNU', 'CCE'], g: ['Intel', 'GNU']}
labels = {h: ['Sandy Bridge', 'Broadwell', 'Thunderx2'], g: ['Sandy Bridge', 'Broadwell']}


# colors = {h: ["#3a7ca5", '#60b564', "#d00000"], g:['#60b564', "#d00000"]}


def plot_compiler_data(config, ax, res):
    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name='compilers', skiprows=0,
                       usecols='A:I')
    df = df[df.Resolution == res]
    df = df[df.Config == config]
    colours = ["#3a7ca5", '#60b564', "#d00000"]
    df.plot.bar(x='Cluster', rot=0, color=colours, edgecolor="black", linewidth=1, ax=ax, legend=False)

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


def main():
    res = 'T42'
    fig, axes = plt.subplots(2, 2, figsize=(10, 6))
    plot_compiler_data('Held-Suarez', axes[0, 0], 'T21')
    plot_compiler_data('Held-Suarez', axes[0, 1], 'T42')
    plot_compiler_data('Grey-Mars', axes[1, 0], 'T21')
    plot_compiler_data('Grey-Mars', axes[1, 1], 'T42')

    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=5)
    # axes[0, 0].get_legend().remove()
    axes[0, 0].set_ylabel('Wallclock runtime (seconds)')
    handles, labels = axes[0, 0].get_legend_handles_labels()

    axes[1, 0].set_xlabel('Processor family')
    axes[1, 1].set_xlabel('Processor family')

    fig.legend(handles, ['Intel', 'GNU', 'CCE'], loc=(0.35, 0), ncol=5)
    # plt.xlabel("common X")
    # fig.xlabel('Processor Family')
    plt.tight_layout()
    plt.savefig(f'{Const.save_path}/compiler-comparison.pdf')
    plt.show()


if __name__ == '__main__':
    main()
