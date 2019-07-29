import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

program_total_performance = 1.54  # GFLOPS
program_total_ai = 0.11  # flop/byte
yticks = [0.001, 0.01, 0.1, 1, 10, 100, 1000]


def main():
    plt.figure(figsize=(10, 6), dpi=300)
    plt.ylabel('Double Precision GFLOPS/Second (SIMD)')
    plt.xlabel('Operational Intensity (FLOPS/byte)')
    plt.title('Roofline model of Isca running on 16 Intel Xeon Gold 6126 cores at 2.6GHz\n (BluePebble)')
    arrowprops = dict(facecolor='black', shrink=0.05, width=0.8, headwidth=5, headlength=5)
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
    ax.text(0.00025, 0.018, 'DRAM Bandwidth 98.06GB/sec', fontsize=10, rotation=25)

    # plot L3 cache line
    l3_x = [0.0001, 1.4, 5.97]
    l3_y = [0.026, 584.99, 584.99]
    plot_roof_line(l3_x, l3_y, ax, 'red')
    ax.text(0.00025, 0.08, 'L3 Bandwidth 429.28GB/sec', fontsize=10, rotation=25)

    # plot L2 cache line
    l2_x = [0.0001, 0.16, 1.4]
    l2_y = [0.23, 584.99, 584.99]
    plot_roof_line(l2_x, l2_y, ax, 'orange')
    ax.text(0.00025, 0.72, 'L2 Bandwidth 3628.36GB/sec', fontsize=10, rotation=25)

    # plot L1 cache line
    l1_x = [0.0001, 0.076, 0.16]
    l1_y = [0.48, 584.99, 584.99]
    plot_roof_line(l1_x, l1_y, ax, 'green')
    ax.text(0.00025, 1.55, 'L1 Bandwidth 7724.67GB/sec', fontsize=10, rotation=25)

    # Peak GFLOPS
    peak = (1, 1000)
    plt.text(peak[0], peak[1], 'DP Vector Peak = 584.99', fontsize=12)

    ax.scatter(program_total_ai, program_total_performance, edgecolor='black', linewidth='1', color='purple',
               label=f'Program total performance', s=100, zorder=2)
    ax.annotate(f'{program_total_performance} GFLOPS\n{program_total_ai} FLOP/Byte',
                xy=(program_total_ai, program_total_performance),
                xytext=(program_total_ai - 0.1, 0.1),
                arrowprops=arrowprops)

    ax.scatter(0.11, 1.68, edgecolor='black', linewidth='1', color='blue',
               label=f'Program total performance', s=100, zorder=2)
    ax.annotate(f'{1.68} GFLOPS\n{0.11} FLOP/Byte',
                xy=(0.11, 1.68),
                xytext=(program_total_ai + 0.1, 10),
                arrowprops=arrowprops)


    ax.scatter(5.69, 0.22, edgecolor='black', linewidth='1', color='red', label='Loop in vpassm at fft99.F90:1081',
               zorder=2, s=100)
    ax.annotate(f'{0.22} GFLOPS\n{5.69} FLOP/Byte',
                xy=(5.69, 0.22),
                xytext=(10, 1),
                arrowprops=arrowprops)

    ax.scatter(4.22, 0.14, edgecolor='black', linewidth='1', color='orange', label='Loop in vpassm at fft99.F90:1049',
               zorder=2, s=100)
    ax.annotate(f'{0.14} GFLOPS\n{4.22} FLOP/Byte',
                xy=(4.22, 0.14),
                xytext=(1.5, 0.01),
                arrowprops=arrowprops)

    ax.legend(loc='lower right')
    plt.show()


def plot_roof_line(x, y, ax, color):
    ax.plot(x, y, '--', color=color, zorder=1)
    ax.plot([x[1], x[1]], [0, 584.99], '--', color=color, zorder=1)


def myLogFormat(y, pos):
    decimalplaces = int(np.maximum(-np.log10(y), 0))  # =0 for numbers >=1
    formatstring = '{{:.{:1d}f}}'.format(decimalplaces)
    return formatstring.format(y)


if __name__ == '__main__':
    main()
