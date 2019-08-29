import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from matplotlib import rc
import pandas as pd

import visualisation_constants as Const

import latex_fonts

# Performance as measured from BluePebble
program_total_performance = 1.54  # GFLOPS
program_total_ai = 0.11  # flop/byte
yticks = [0.001, 0.01, 0.1, 1, 10, 100, 1000]

held_suarez_performance_t21 = 0.91  # GFLOPS
held_suarez_ai_t21 = 0.11  # flop/byte

held_suarez_performance_t85 = 0.00  # GFLOPS
held_suarez_ai_t85 = 0.00  # flop/byte

grey_mars_performance_t42 = 1.96
grey_mars_ai_t42 = 0.11

sp_program_total_performance = 2.71
sp_program_total_ai = 0.21

arrowprops = dict(facecolor='black', arrowstyle='->')


def plot_original_roofline():
    plt.figure(figsize=(10, 6), dpi=300)
    plt.ylabel('Double Precision GFLOPS/Second (SIMD)')
    plt.xlabel('Operational Intensity (FLOPS/byte)')
    plt.title('Roofline model of Isca running on 16 Intel Xeon Gold 6126 cores at 2.6GHz\n (Skylake)')
    ax = plt.gca()
    ax.axis([0.0001, 100, 0.0001, 10000])
    ax.loglog()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(myLogFormat))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(myLogFormat))
    ax.grid()

    # plot dram line
    dram_x = [0.0001, 5.97, 100]
    dram_y = [0.0057, 584.99, 584.99]
    plot_roof_line(dram_x, dram_y, ax, 'grey')
    ax.text(0.00025, 0.018, 'DRAM Bandwidth 98.06GB/sec', fontsize=10, rotation=23)

    # plot L3 cache line
    l3_x = [0.0001, 1.4, 5.97]
    l3_y = [0.026, 584.99, 584.99]
    plot_roof_line(l3_x, l3_y, ax, 'red')
    ax.text(0.00025, 0.08, 'L3 Bandwidth 429.28GB/sec', fontsize=10, rotation=23)

    # plot L2 cache line
    l2_x = [0.0001, 0.16, 1.4]
    l2_y = [0.23, 584.99, 584.99]
    plot_roof_line(l2_x, l2_y, ax, 'orange')
    ax.text(0.00025, 0.72, 'L2 Bandwidth 3628.36GB/sec', fontsize=10, rotation=23)

    # plot L1 cache line
    l1_x = [0.0001, 0.076, 0.16]
    l1_y = [0.48, 584.99, 584.99]
    plot_roof_line(l1_x, l1_y, ax, 'green')
    ax.text(0.00025, 1.55, 'L1 Bandwidth 7724.67GB/sec', fontsize=10, rotation=23)

    # Peak GFLOPS
    peak = (1, 1000)
    plt.text(peak[0], peak[1], 'DP Vector Peak = 584.99', fontsize=12)

    ax.scatter(program_total_ai, program_total_performance, edgecolor='black', linewidth='1', color='purple',
               label=f'Held-Suarez T42', zorder=2)
    ax.annotate(f'{program_total_performance} GFLOPS\n{program_total_ai} FLOP/Byte',
                xy=(program_total_ai, program_total_performance),
                xytext=(0.015, 0.13),
                arrowprops=arrowprops)

    ax.scatter(grey_mars_ai_t42, grey_mars_performance_t42, edgecolor='black', linewidth='1', color='blue',
               label=f'Grey-Mars T42', zorder=2)
    ax.annotate(f'{grey_mars_performance_t42} GFLOPS\n{grey_mars_ai_t42} FLOP/Byte',
                xy=(grey_mars_ai_t42, grey_mars_performance_t42),
                xytext=(grey_mars_ai_t42 + 0.1, 1.5),
                arrowprops=arrowprops)

    # ax.scatter(0.11, 1.68, edgecolor='black', linewidth='1', color='blue',
    #            label=f'Program total performance', zorder=2)
    # ax.annotate(f'{1.68} GFLOPS\n{0.11} FLOP/Byte',
    #             xy=(0.11, 1.68),
    #             xytext=(program_total_ai + 0.1, 10),
    #             arrowprops=arrowprops)

    ax.scatter(5.69, 0.22, edgecolor='black', linewidth='1', color='red', label=r'Loop $x$ (\texttt{vpassm:1081})',
               zorder=2)
    ax.annotate(f'{0.22} GFLOPS\n{5.69} FLOP/Byte',
                xy=(5.69, 0.22),
                xytext=(10.5, 0.15),
                arrowprops=arrowprops)

    ax.scatter(4.22, 0.14, edgecolor='black', linewidth='1', color='orange', label=r'Loop $y$ (\texttt{vpassm:1049})',
               zorder=2)
    ax.annotate(f'{0.14} GFLOPS\n{4.22} FLOP/Byte',
                xy=(4.22, 0.14),
                xytext=(10.5, 0.015),
                arrowprops=arrowprops)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=4)
    plt.tight_layout()
    plt.savefig(f'{Const.save_path}/roofline_model_bluepebble.pdf')
    plt.show()


def plot_opt_roofline():
    plt.figure(figsize=(10, 6), dpi=300)
    plt.ylabel('GFLOPS/Second (SIMD)')
    plt.xlabel('Operational Intensity (FLOPS/byte)')
    plt.title('Roofline model of Isca running on 16 Intel Xeon Gold 6126 cores at 2.6 GHz\n (Skylake)')
    ax = plt.gca()
    ax.axis([0.0001, 100, 0.0001, 10000])
    ax.loglog()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(myLogFormat))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(myLogFormat))
    ax.grid()

    # plot dram line
    dram_x = [0.0001, 5.97, 100]
    dram_y = [0.0057, 584.99, 584.99]
    plot_roof_line(dram_x, dram_y, ax, 'grey')
    ax.text(0.00025, 0.018, 'DRAM Bandwidth 98.06GB/sec', fontsize=10, rotation=23)

    # plot L3 cache line
    l3_x = [0.0001, 1.4, 5.97]
    l3_y = [0.026, 584.99, 584.99]
    plot_roof_line(l3_x, l3_y, ax, 'red')
    ax.text(0.00025, 0.08, 'L3 Bandwidth 429.28GB/sec', fontsize=10, rotation=23)

    # plot L2 cache line
    l2_x = [0.0001, 0.16, 1.4]
    l2_y = [0.23, 584.99, 584.99]
    plot_roof_line(l2_x, l2_y, ax, 'orange')
    ax.text(0.00025, 0.72, 'L2 Bandwidth 3628.36GB/sec', fontsize=10, rotation=23)

    # plot L1 cache line
    l1_x = [0.0001, 0.076, 0.16]
    l1_y = [0.48, 584.99, 584.99]
    plot_roof_line(l1_x, l1_y, ax, 'green')
    ax.text(0.00025, 1.55, 'L1 Bandwidth 7724.67GB/sec', fontsize=10, rotation=23)

    # Peak GFLOPS
    peak = (1, 1000)
    plt.text(peak[0], peak[1], 'DP Vector Peak = 584.99', fontsize=12)

    colours = ['blue', 'yellow', 'orange', 'purple', 'brown', 'magenta', 'turquoise']
    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name='roofline', skiprows=0, usecols='A:E')
    df = df.dropna(axis=0)
    df = df[(df['optimisation'] == 'double precision') | (df['optimisation'] == 'single precision')]
    df = df[df['resolution'] == 'T42']
    df['label'] = df['Config'] + ' ' + df['optimisation']

    for x in range(len(df.index)):
        ax.scatter(df.iloc[x].ai, df.iloc[x].performance, edgecolor='black', linewidth='1', color=colours[x],
                   label=df.iloc[x].label)
        if x % 2 == 0:
            drawArrow((df.iloc[x].ai, df.iloc[x].performance), (df.iloc[x + 1].ai, df.iloc[x + 1].performance), ax)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2)
    plt.tight_layout()
    plt.savefig(f'{Const.save_path}/roofline_model_bluepebble_precision.pdf')
    plt.show()


def plot_roof_line(x, y, ax, color):
    ax.plot(x, y, '--', color=color, zorder=1)
    ax.plot([x[1], x[1]], [0, 584.99], '--', color=color, zorder=1)


def myLogFormat(y, pos):
    decimalplaces = int(np.maximum(-np.log10(y), 0))  # =0 for numbers >=1
    formatstring = '{{:.{:1d}f}}'.format(decimalplaces)
    return formatstring.format(y)


def drawArrow(A, B, ax):
    ax.annotate('', xytext=(A[0], A[1]), xy=(B[0], B[1]), arrowprops=arrowprops)


if __name__ == '__main__':
    plot_original_roofline()
    plot_opt_roofline()
