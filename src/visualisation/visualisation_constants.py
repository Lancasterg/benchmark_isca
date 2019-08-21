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
                bp: 'Skylake'}

# Grid size for resolutions
t21_grid = 64 * 32
t42_grid = 128 * 64
t85_grid = 256 * 128

grid_lookup = {t21: t21_grid, t42: t42_grid, t85: t85_grid}

n_timesteps = {held_suarez: 12 * 30, grey_mars: 270}

per_grid = 'Per_grid'

xtick_dict = {t21: [1, 2, 4, 8, 16],
              t42: [1, 2, 4, 8, 16, 24, 28, 32],
              t85: [1, 4, 8, 16, 24, 28, 32, 64]}

xtick_cppg = {t21: [1, 2, 4, 8, 16],
              t42: [1, 2, 4, 8, 16, 32],
              t85: [1, 4, 8, 16, 24, 64]}
