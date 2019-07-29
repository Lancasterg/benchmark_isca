import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

dir_loc = '/Users/george/isca_python/visualisation/bcp3/whole_node/held_suarez/'
spreadsheet_dir = '/Users/george/Dropbox/university_of_bristol/thesis/data_collection/run_measurements.xlsx'
clusters = ['BCP3', 'BCP4', 'BP', 'Isambard']
configs = ['Held_suarez', 'Grey_mars']


def read_fft_data(sheet_name):
    df = pd.read_excel(open(spreadsheet_dir, 'rb'), sheet_name=sheet_name, skiprows=2, usecols=[7, 8, 9, 10, 11, 12],
                       nrows=3, dtype=str)
    df['vanilla_iteration'] = df['vanilla_iteration'].astype(np.float64)
    df['vanilla_full'] = df['vanilla_full'].astype(np.float64)
    df['fftw_iteration'] = df['fftw_iteration'].astype(np.float64)
    df['fftw_full'] = df['fftw_full'].astype(np.float64)

    return df


def plot_fft_bar():
    df = read_fft_data(clusters[0])
    df = df.drop('vanilla_iteration', axis=1)
    df = df.drop('fftw_iteration', axis=1)
    ax = df.plot.bar(x='grid_size',rot=0, edgecolor="black", linewidth=0.5)
    ax.set_axisbelow(True)
    ax.set_ylabel('Runtime (seconds)')
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

    plt.show()

def main():
    plot_fft_bar()


if __name__ == '__main__':
    main()
