from matplotlib import rc
import matplotlib.pyplot as plt

# Use LaTeX fonts
plt.rc('font', family='serif')
# Bold text by default
plt.rc('text.latex', preamble=r'\renewcommand{\seriesdefault}{\bfdefault} \boldmath')
rc('text', usetex=True)