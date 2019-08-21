import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from matplotlib import rc

import visualisation_constants as Const

import latex_fonts


def main():
    edge_col = 'black'
    colors = ['#c0df85', '#db6c79']

    fig, ax = plt.subplots(figsize=(7, 3))

    df = pd.read_excel(open(Const.spreadsheet_dir, 'rb'), sheet_name='vectorisation', skiprows=0, usecols='A:E')

    df_held = df[df['config'] == 'held-suarez']
    df_held.rename(columns={'speedup-t42': 'Held-Suarez'}, inplace=True)
    df_held = pd.DataFrame([df_held['Cluster'], df_held['Held-Suarez']]).transpose()

    df_grey = df[df['config'] == 'grey-mars']
    df_grey.rename(columns={'speedup-t42': 'Grey-Mars'}, inplace=True)
    df_grey = pd.DataFrame([df_grey['Cluster'], df_grey['Grey-Mars']]).transpose()

    df = pd.merge(df_held, df_grey, on='Cluster')

    print(df)
    df.plot.bar(x='Cluster', rot=0, linewidth=0.5, edgecolor="black", colors=colors, ax=ax)

    plt.xlabel('Processor family')
    plt.ylabel('Speedup of vector code vs scalar')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
               fancybox=True, shadow=True, ncol=5)

    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='black')
    plt.xticks(np.linspace(0, 3, 4), ['Sandy Bridge', 'Broadwell', 'Skylake', 'Thunderx2'])
    plt.tight_layout()
    savepath = f'{Const.save_path}/speedup-vector.pdf'

    print(savepath)
    plt.savefig(savepath)
    plt.show()


if __name__ == '__main__':
    main()
