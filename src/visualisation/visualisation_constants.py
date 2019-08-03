import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rc
import os
from sklearn import preprocessing

import matplotlib.ticker as mtick

# Data locations
dir_loc = '/Users/george/isca_python/visualisation/bcp3/whole_node/held_suarez/'
spreadsheet_dir = '/Users/george/Dropbox/university_of_bristol/thesis/data_collection/run_measurements.xlsx'
save_path = '/Users/george/Dropbox/university_of_bristol/thesis/Thesis/img'

# Compiler names
gnu = 'GNU'
intel = 'Intel'
cce = 'CCE'
arm = 'Arm'

# Cluster names
bcp3 = 'BCP3'
bcp4 = 'BCP4'
isam = 'Isambard'
bp = 'BP'
clusters = [bcp3, bcp4, isam, bp]

# Configuration names
held_suarez = 'Held_suarez'
grey_mars = 'Grey_mars'
configs = [held_suarez, grey_mars]

# Model resolutions
t21 = 'T21'
t42 = 'T42'
t85 = 'T85'
resolutions = [t21, t42, t85]

# Cluster processor lookup dictionary
cluster_proc = {isam: 'ThunderX2',
                bcp3: 'Sandy Bridge',
                bcp4: 'Broadwell',
                bp:   'Skylake'}
