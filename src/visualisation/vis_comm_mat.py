import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import numpy as np
import csv
import re
import visualisation_constants as Const
import latex_fonts

held_suarez = 'Held-Suarez'
grey_mars = 'Grey-mars'


def main():
    held_suarez_data = 'data/held_suarez_comm_mat.txt'
    plot_comm_matrix(held_suarez_data, 'Held-Suarez')
    #
    grey_mars_data = 'data/grey_mars_comm_mat.txt'
    plot_comm_matrix(grey_mars_data, 'Grey-mars')

    # held_suarez_collective = 'data/held_suarez_collective_operation.txt'
    # grey_mars_collective = 'data/grey_mars_collective_operation.txt'
    #
    # df_held = read_collective(held_suarez_collective, held_suarez)
    # df_grey = read_collective(grey_mars_collective, grey_mars)
    # df = df_held.merge(df_grey, left_on='Process(Group)', right_on='Process(Group)')
    # df = df[['Process(Group)', held_suarez, grey_mars]]
    # plot_collective(df)


def read_collective(filename, config):
    df = pd.read_csv(filename, delimiter=';')
    df = df[df.Operation == 'MPI_Barrier']
    df = df[['Operation', 'Process(Group)', 'Sum duration [s]']]
    df = df.rename(columns={'Sum duration [s]': f'{config}'})

    if config == Const.held_suarez:
        df['portion'] = ((841.9501616954803 / 12) / df[config])
    else:
        df['portion'] = ((11102.7850935459 / 22) / df[config])
    print(df)
    return df


def plot_collective(df):
    fig, ax = plt.subplots(figsize=(7, 3))
    colors = ['#c0df85', '#db6c79']
    df['Process'] = np.linspace(0, 15, 16, dtype=np.int)
    df.plot.bar(x='Process', color=colors, edgecolor="black", linewidth=1, ax=ax, rot=0)

    ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

    ax.legend(['Held-Suarez', 'Grey-Mars'], loc='upper center',
              bbox_to_anchor=(0.15, -0.1),
              fancybox=True, shadow=True, ncol=2)

    plt.tight_layout()
    # plt.title('Amount of time spent at an MPI barrier ')
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

    data = np.array(data, dtype='float64')
    matrix = np.zeros((16, 16), dtype='float64')
    for i in range(data.shape[0]):
        x, y, val = data[i]
        matrix[int(x), int(y)] = val
    print(matrix[0])
    print(np.mean(matrix[0]))
    print(np.mean(matrix[:,0]))


    # Display matrix
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cmap = plt.cm.jet
    cmap.set_under(color='white')
    cax = ax.matshow(matrix, interpolation='nearest', cmap=cmap)
    cbar = fig.colorbar(cax)
    cbar.set_label('Seconds', rotation=270, labelpad=15)

    plt.ylabel('Sending Process')
    plt.xlabel('Receiving Process')

    plt.xticks(np.arange(0, 16, 1))
    plt.yticks(np.arange(0, 16, 1))
    plt.title(f'MPI communication times for a 30 day simulation\n of the {config} configuration at T42 resolution')

    plt.savefig(f'{Const.save_path}/comm_mat_{config}.pdf')
    plt.show()


def read_comms(config):
    df = pd.read_csv(f'data/{config}_comms.data', delimiter=';')
    df[f'{config} mpi time'] = df[df['Function(Group)'] == 'MPI']["Time Self [s]"]
    df[f'{config} application time'] = df[df['Function(Group)'] == 'Application']["Time Self [s]"]
    df = df.groupby('Process(Group)').max().reset_index()
    df = pd.DataFrame([df['Process(Group)'], df[f'{config} mpi time'], df[f'{config} application time']]).transpose()
    df = df[df['Process(Group)'] != 'All_Processes']
    df[f'{config} total'] = df[f'{config} mpi time'] + df[f'{config} application time']
    df[f'{config} mpi percentage'] = (df[f'{config} mpi time'] / df[f'{config} total']) * 100
    return df


def plot_percentage_comms():
    main()
    fig, ax = plt.subplots(figsize=(7, 3))
    df_held = read_comms(held_suarez)
    df_grey = read_comms(grey_mars)
    df = df_held.merge(df_grey, left_on='Process(Group)', right_on='Process(Group)')
    df['indexNumber'] = [int(i.split(' ')[-1]) for i in df['Process(Group)']]
    df.sort_values('indexNumber', ascending=[True], inplace=True)
    df['Process'] = np.linspace(0, 15, 16, dtype=np.int)

    colors = ['#c0df85', '#db6c79']
    df = pd.DataFrame(
        [df['Process'], df[f'Held-Suarez mpi percentage'], df[f'Grey-mars mpi percentage']]).transpose()

    df.plot.bar(x='Process', ax=ax, color=colors, edgecolor="black", linewidth=1, rot=0)
    print(df)
    print(df['Grey-mars mpi percentage'].mean())
    print(df['Grey-mars mpi percentage'].std())
    print(df['Grey-mars mpi percentage'].max())
    print(df['Grey-mars mpi percentage'].min())

    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='black')
    ax.legend(['Held-Suarez', 'Grey-Mars'], loc='upper center',
              bbox_to_anchor=(0.15, -0.1),
              fancybox=True, shadow=True, ncol=2)
    plt.ylabel('Percentage of runtime spent in MPI')
    plt.xlabel('Process')
    plt.title('Percentage of runtime spent in MPI')
    plt.xticks(np.linspace(0, 15, 16, dtype=np.int), np.linspace(0, 15, 16, dtype=np.int))
    plt.tight_layout()
    plt.savefig(f'{Const.save_path}/mpi-barrier-time.pdf')
    plt.show()


if __name__ == '__main__':
    plot_percentage_comms()