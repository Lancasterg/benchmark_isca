import matplotlib.pyplot as plt
from numpy import exp, loadtxt, pi, sqrt
import numpy as np
import latex_fonts
import visualisation_constants as Const
import pandas as pd

from lmfit import Model

x = [1, 2, 4, 8, 16, 32]
y = [1.000000, 1.978665, 3.872101, 6.423682, 12.664421, 18.654791]
p = 0.97755377
arrowprops = dict(facecolor='black', arrowstyle='->')


def main():
    plot_least_squares()
    plot_estimate()


def plot_estimate():
    """
    Plot estimated performance
    """
    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name=Const.isam, skiprows=2, usecols='A:E')
    df = df[(df.Config == Const.held_suarez) & (df.Resolution == Const.t42)]
    slowdown = 1.073732491
    df['Scalar'] = df['Runtime'] * slowdown

    a64_cores = 96
    a64_freq = 1.9
    a64_effc = 1 / ((1 - p) + p / a64_cores)
    a64_gflop = a64_freq * a64_effc

    tx2_cores = 64
    tx2_freq = 2.1
    tx2_effc = 1 / ((1 - p) + p / tx2_cores)
    tx2_gflop = tx2_freq * tx2_effc

    df['a64_est'] = ((tx2_gflop / a64_gflop) * df['Scalar']) / 1.2
    df['error'] = (df['a64_est'] / 100) * 10

    fig, ax = plt.subplots(figsize=(7, 3.5))

    (_, caps, _) = plt.errorbar(df['Cores'], df['a64_est'], color='green', linestyle=':', markeredgecolor='black',
                                ms=10,
                                zorder=2,
                                marker='.', yerr=df['error'], capsize=5)
    df.plot(kind='line', x='Cores', y='Runtime', ax=ax, color='red', style=':o', markeredgecolor='black', ms=5,
            zorder=1)

    plt.xlabel('Number of processor cores')
    plt.ylabel('Wallclock runtime (seconds)')

    ax.xaxis.set_ticks([1, 2, 4, 8, 16, 32])
    ax.set_xlim(xmin=0, xmax=max(ax.get_xlim()) + 1)
    plt.yscale('log')

    # ax.yaxis.set_ticks([1000, 10000, 100000])

    for cap in caps:
        cap.set_markeredgewidth(1)

    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    ax.legend(['ThunderX2', 'A64FX projected'], loc='upper center',
              bbox_to_anchor=(0.5, -0.2),
              fancybox=True, shadow=True, ncol=4)
    plt.tight_layout()
    plt.savefig(f'{Const.save_path}/a64fx-projection.pdf')

    print(df)
    print(df['Runtime'])
    plt.show()


def amdahl_law(x, p):
    return 1 / ((1 - p) + (p / x))


def plot_least_squares():
    """
    Use least squares regression to find the value for p
    """
    gmodel = Model(amdahl_law)
    result = gmodel.fit(y, x=x, p=0.98)

    print(result.fit_report())
    fig, ax = plt.subplots(figsize=(7, 3.5))
    plt.scatter(x, y, color='red', marker='o',
                zorder=2, lw=1, edgecolors='black', )
    plt.plot(x, result.best_fit, color='orange', linestyle=':')
    print(result.best_fit)

    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='black')

    plt.xlabel('Number of processor cores ($n$)')
    plt.ylabel('Speedup relative to 1 core $S(n)$')
    ax.annotate(r'$S(n) = \frac{1}{(1-0.9776) + \frac{0.9776}{n}}$',
                xy=(10.5, 8.5),
                xytext=(15, 8),
                arrowprops=arrowprops,
                size=14)

    ax.legend(['Least squares regression curve', 'ThunderX2'], loc='upper center',
              bbox_to_anchor=(0.5, -0.2),
              fancybox=True, shadow=True, ncol=4)

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    plt.tight_layout()
    plt.savefig(f'{Const.save_path}/a64fx-estimate.pdf')
    plt.show()


if __name__ == '__main__':
    main()
