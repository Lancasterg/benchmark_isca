import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
from matplotlib.lines import Line2D

import visualisation_constants as Const

# Use LaTeX fonts
plt.rc('font', family='serif')
rc('text', usetex=True)

size = 20
lw = 1
edgecolor = 'black'


def process_dataframe(sheet_name, resolution, config):
    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name=sheet_name, skiprows=2, usecols=[0, 1, 2, 3, 4])
    df['Cluster'] = sheet_name
    df = df[df.Resolution == resolution]
    df = df[df['Node Resources'] == 'All']
    df = df[df.Config == config]
    df = df.dropna()
    df["Runtime"] = pd.to_numeric(df["Runtime"])
    if resolution == Const.t42 and config == Const.held_suarez and sheet_name == Const.bcp3:
        df = df[(df.Cores != 32)]
    return df


def calc_cell_rate(resolution):
    df = process_dataframe(Const.bcp3, resolution, Const.held_suarez)
    Const.clusters.remove(Const.bcp3)
    for cluster in Const.clusters:
        df = df.append(process_dataframe(cluster, resolution, Const.held_suarez))
    df[Const.per_grid] = df['Runtime'] / Const.grid_lookup[resolution] * df['Cores'] / Const.n_timesteps[
        Const.held_suarez]
    df['Cores'] = pd.to_numeric(df['Cores'])
    df['Per_grid'] = pd.to_numeric(df['Per_grid'])

    return df


def calc_grid_rate(df, resolution):
    df[Const.per_grid] = (df['Runtime'] / Const.grid_lookup[resolution]) * (
            df['Cores'] / Const.n_timesteps[Const.held_suarez])

    df['oo'] = (df['Runtime'] * df['Cores']) / (Const.n_timesteps[Const.held_suarez] * Const.grid_lookup[resolution])

    df['Cores'] = pd.to_numeric(df['Cores'])
    df['Per_grid'] = pd.to_numeric(df['Per_grid'])
    return df


def calc_scale(resolution):
    return 16 if resolution == Const.t21 else 32 if resolution == Const.t42 else 64 if resolution == Const.t85 else 0


def plot_data(resolution, config, ax):
    df_bcp3 = calc_grid_rate(process_dataframe(Const.bcp3, resolution, config), resolution)
    df_bcp4 = calc_grid_rate(process_dataframe(Const.bcp4, resolution, config), resolution)
    df_isam = calc_grid_rate(process_dataframe(Const.isam, resolution, config), resolution)
    df_bp = calc_grid_rate(process_dataframe(Const.bp, resolution, config), resolution)

    # print(df_bcp3)
    # print(df_bcp4)
    # print(df_isam)

    if resolution == Const.t42 and config == Const.grey_mars:
        print(df_isam)

    a = df_isam.plot(kind='scatter', x='Cores', y=Const.per_grid, ax=ax, color='red', marker='o', s=size,
                     zorder=2, lw=lw, edgecolor=edgecolor, legend=True)
    b = df_bcp3.plot(kind='scatter', x='Cores', y=Const.per_grid, ax=ax, color='magenta', marker='^', s=size,
                     zorder=2, lw=lw, edgecolor=edgecolor, legend=True)
    c = df_bcp4.plot(kind='scatter', x='Cores', y=Const.per_grid, ax=ax, color='blue', marker='s', s=size,
                     zorder=2, lw=lw, edgecolor=edgecolor, legend=True)
    d = df_bp.plot(kind='scatter', x='Cores', y=Const.per_grid, ax=ax, color='green', marker='X', s=size,
                   zorder=2, lw=lw, edgecolor=edgecolor, legend=True)

    ax.set_xlim(xmin=0, xmax=max(ax.get_xlim()) + 4)
    ax.xaxis.set_ticks(Const.xtick_cppg[resolution])

    ax.set_ylabel('Cost per grid point (Seconds)')
    ax.set_xlabel('Number of processor cores')

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='black')

    ax.set_ylim(ymin=0)
    title_config = config.split('_')[0].capitalize() + '-' + config.split('_')[1].capitalize()
    ax.set_title(f'{title_config} simulation at {resolution}')

    return [a, b, c, d]


def main():
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    plot_data(Const.t21, Const.held_suarez, axes[0, 0])
    plot_data(Const.t21, Const.grey_mars, axes[0, 1])
    plot_data(Const.t42, Const.held_suarez, axes[1, 0])
    plot_data(Const.t42, Const.grey_mars, axes[1, 1])
    # plot_data(Const.t85, Const.held_suarez, axes[2, 0])

    # handles = plot_data(Const.t42, Const.grey_mars, axes[1, 2])

    axes[0, 1].set_ylabel('')
    axes[1, 1].set_ylabel('')
    axes[0, 0].set_xlabel('')
    axes[0, 1].set_xlabel('')

    legend_elements = [Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor='red', markersize=5,
                              markeredgecolor='black'),
                       Line2D([0], [0], marker='^', color='w', label='Scatter', markerfacecolor='magenta', markersize=5,
                              markeredgecolor='black'),
                       Line2D([0], [0], marker='s', color='w', label='Scatter', markerfacecolor='blue', markersize=5,
                              markeredgecolor='black'),
                       Line2D([0], [0], marker='X', color='w', label='Scatter', markerfacecolor='green', markersize=5,
                              markeredgecolor='black')]

    fig.legend(legend_elements, ['ThunderX2', 'Sandy Bridge', 'Broadwell', 'Skylake'],
               loc=(0.2, 0), ncol=5)
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.13)
    filename = f'cost-per-grid-point.pdf'
    print(filename)
    plt.savefig(f'{Const.save_path}/{filename}')
    plt.show()


if __name__ == '__main__':
    main()
