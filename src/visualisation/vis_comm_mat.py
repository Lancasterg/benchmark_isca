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
    plot_comm_matrix('data/held_suarez_comm_mat.txt', 'Held-Suarez')
    plot_comm_matrix('data/grey_mars_comm_mat.txt', 'Grey-mars')
    df_grey = read_collective('data/Grey-mars-13_comms.data', grey_mars)
    df_held = read_collective('data/held_suarez_collective_operation.txt', held_suarez)
    df = df_held.merge(df_grey, left_on='Process(Group)', right_on='Process(Group)')
    df = df[['Process(Group)', held_suarez, grey_mars]]
    plot_percentage_comms()


def read_collective(filename, config):
    """
    Read communication times of processes
    :param filename: location of input file
    :param config: Model configuration; one of: Held_Suarez, Grey_Mars
    :return: Pandas DataFrame
    """
    df = pd.read_csv(filename, delimiter=';')
    df = df[df.Operation == 'MPI_Barrier']
    df = df[['Operation', 'Process(Group)', 'Sum duration [s]']]
    df = df.rename(columns={'Sum duration [s]': f'{config}'})

    if config == Const.held_suarez:
        df['portion'] = ((841.9501616954803 / 12) / df[config])
    else:
        df['portion'] = ((11102.7850935459 / 22) / df[config])
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
    """
    Plot a communication matrix given a Intel Trace Analyzer output file
    :param send_recv: location of Intel TraceAnalyzer output file
    :param config: Model configuration; one of: Held_Suarez, Grey_Mars
    """
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
    print(np.mean(matrix[:, 0]))

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
    """
    Read an Intel Trace Analyzer output file
    :param config: Model configuration; one of: Held_Suarez, Grey_Mars
    :return: Pandas DataFrame
    """
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
    """
    Plot the percentage of time spent inside the MPI library
    """
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
    plt.title('Percentage of runtime spent in MPI (Sandy Bridge) ')

    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='black')

    ax.legend(['Held-Suarez', 'Grey-Mars'], loc='upper center', bbox_to_anchor=(0.5, -0.2),
               fancybox=True, shadow=True, ncol=5)
    plt.ylabel('Percentage of runtime spent in \nMPI (\%)')
    plt.xlabel('Processor rank')
    plt.xticks(np.linspace(0, 15, 16, dtype=np.int), np.linspace(0, 15, 16, dtype=np.int))
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    plt.tight_layout()
    plt.savefig(f'{Const.save_path}/mpi-barrier-time.pdf')
    plt.show()


def plot_percentage_comms_broadwell():
    """
    Plot the percentage of time spent in the MPI library for the Broadwell processor
    """
    fig, ax = plt.subplots(figsize=(7, 3))
    df_1 = read_comms(f'{grey_mars}-1')
    df_13 = read_comms(f'{grey_mars}-13')
    df = df_1.merge(df_13, left_on='Process(Group)', right_on='Process(Group)')
    df['indexNumber'] = [int(i.split(' ')[-1]) for i in df['Process(Group)']]
    df.sort_values('indexNumber', ascending=[True], inplace=True)
    df['Process'] = np.linspace(0, 15, 16, dtype=np.int)
    df = pd.DataFrame(
        [df['Process'], df[f'Grey-mars-1 mpi percentage'], df[f'Grey-mars-13 mpi percentage']]).transpose()

    df.plot.bar(x='Process', ax=ax, edgecolor="black", linewidth=1, rot=0)
    plt.legend(['Grey-Mars Epoch 1', 'Grey-Mars Epoch 13'], loc='upper center', bbox_to_anchor=(0.5, -0.2),
               fancybox=True, shadow=True, ncol=5)

    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='black')

    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    plt.xticks(np.linspace(0, 15, 16, dtype=np.int), np.linspace(0, 15, 16, dtype=np.int))

    plt.ylabel('Percentage of runtime spent in \nMPI (\%)')
    plt.xlabel('Processor rank')
    plt.title('Percentage of runtime spent in MPI (Broadwell)')
    plt.tight_layout()
    plt.savefig(f'{Const.save_path}/mpi-barrier-time-grey-mars.pdf')
    plt.show()
    print(df)


if __name__ == '__main__':
    plot_percentage_comms()
    plot_percentage_comms_broadwell()
    main()
