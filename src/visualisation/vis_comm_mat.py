import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import numpy as np
import csv
import re
import visualisation_constants as Const

# Use LaTeX fonts
plt.rc('font', family='serif')
rc('text', usetex=True)

held_suarez = 'Held-Suarez'
grey_mars = 'Grey-mars'


def main():
    # held_suarez_data = 'data/held_suarez_comm_mat.txt'
    # plot_comm_matrix(held_suarez_data, 'Held-Suarez')

    # grey_mars_data = 'data/grey_mars_comm_mat.txt'
    # plot_comm_matrix(grey_mars_data, 'Grey-mars')

    held_suarez_collective = 'data/held_suarez_collective_operation.txt'
    grey_mars_collective = 'data/grey_mars_collective_operation.txt'

    df_held = read_collective(held_suarez_collective, held_suarez)
    df_grey = read_collective(grey_mars_collective, grey_mars)
    df = df_held.merge(df_grey, left_on='Process(Group)', right_on='Process(Group)')
    df = df[['Process(Group)', held_suarez, grey_mars]]
    plot_collective(df)


def read_collective(filename, config):
    df = pd.read_csv(filename, delimiter=';')
    df = df[df.Operation == 'MPI_Barrier']
    df = df[['Operation', 'Process(Group)', 'Sum duration [s]']]
    df = df.rename(columns={'Sum duration [s]': f'{config}'})
    return df


def plot_collective(df):
    colors = ['#c0df85', '#db6c79']
    df.plot.bar(x='Process(Group)', color=colors, edgecolor="black", linewidth=1)

    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

    plt.title('Amount of time spent at an MPI barrier ')
    plt.savefig(f'{Const.save_path}/mpi-barrier-time.pdf')
    plt.show()


def plot_comm_matrix(send_recv, config):
    data = []
    with open(send_recv, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for i, line in enumerate(reader):
            if i > 0:
                data.append([re.sub('[^0-9]', '', line[0]), re.sub('[^0-9]', '', line[1]), line[3]])
    data = [[float(a) for a in d] for d in data]
    data.sort()
    [print(d) for d in data]

    data = np.array(data, dtype='float64')
    matrix = np.zeros((16, 16), dtype='float64')
    for i in range(data.shape[0]):
        x, y, val = data[i]
        matrix[int(x), int(y)] = val

    # Display matrix
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cmap = plt.cm.jet
    cmap.set_under(color='white')
    cax = ax.matshow(matrix, interpolation='nearest', cmap=cmap)
    cbar = fig.colorbar(cax)
    cbar.set_label('Seconds', rotation=270, labelpad=15)

    plt.ylabel('Sending Rank')
    plt.xlabel('Receiving Rank')

    plt.xticks(np.arange(0, 15, 1))
    plt.yticks(np.arange(0, 15, 1))
    plt.title(f'MPI communication times for a 30 day simulation\n of the {config} configuration at T42 resolution')

    plt.savefig(f'{Const.save_path}/comm_mat_{config}.pdf')
    plt.show()


if __name__ == '__main__':
    main()
