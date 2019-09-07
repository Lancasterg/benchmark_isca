import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import latex_fonts

import visualisation_constants as Const

# Use LaTeX fonts
plt.rc('font', family='serif')
rc('text', usetex=True)


def format_ax(ax):
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='black')

    # ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    # ax.minorticks_on()
    ax.title.set_text(f'Peak theoretical performance and HPL measured performance of \n'
                      f'the node configurations used in this research project')
    ax.set_xticklabels(['Sandy Bridge', 'Broadwell', 'Skylake', 'ThunderX2'])

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    ax.set_xlabel('Processor Family')


def plot_data():
    colors = ['#c0df85', '#db6c79', '#aec5eb']
    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name='hpl', skiprows=0, usecols='A:D')
    print(df)
    df = df.dropna(axis=0)
    print(df)
    df.plot.bar(x='Cluster', rot=0, legend=False, color=colors, edgecolor="black", linewidth=1)
    ax = plt.gca()
    plt.legend(['Theoretical double-precision peak', 'Theoretical single-precision peak', 'Double precision HPLinpack'],
               loc='upper center', bbox_to_anchor=(0.5, -0.2),
               fancybox=True, shadow=True, ncol=2)
    format_ax(ax)
    plt.ylabel('GFLOPS')
    plt.tight_layout()
    print(f'{Const.save_path}/hpl.pdf')
    plt.savefig(f'{Const.save_path}/hpl.pdf')
    plt.show()


def main():
    read_data()


if __name__ == '__main__':
    main()
