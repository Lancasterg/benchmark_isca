import matplotlib.pyplot as plt
import numpy as np


def main():
    plt.figure(figsize=(12, 6), dpi=300)
    plt.grid(True)
    plt.ylabel('Single Precision GFLOPS/Second (SIMD)')
    plt.xlabel('Operational Intensity FLOPS/byte')
    plt.title('Roofline model of Isca running on 16 cores of BluePebble.')
    ax = plt.gca()
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.plot(0.17, 4.18)

    dram_bandwidth_x = [0, 5.97, 100]
    dram_bandwidth_y = [0.0065, 584.97, 584.97]
    plt.plot(dram_bandwidth_x, dram_bandwidth_y)

    plt.show()

    program_total_performance = 1.54  # GFLOPS
    program_total_ai = 0.11  # flop/byte


if __name__ == '__main__':
    main()
