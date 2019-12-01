from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np


dataDir = Path('/Volumes/Transcend/EastRiverClimatePaper/data')

topo = dataDir.joinpath('east_topo.npy')
wrf = dataDir.joinpath('WRF_wy2017_daily_east_only.npy')
prism = dataDir.joinpath('PRISM_wy2017_daily_east_only.npy')


topo = np.load(topo)
wrf = np.load(wrf)
prism = np.load(prism)


def kge(a1, a2):
    s = np.std(a1)/np.std(a2)
    m = np.median(a1)/np.median(a2)
    c = np.corrcoef(a1, a2)[0,0]
    return 1 - np.sqrt((1 - s)**2 + (1-m)**2 + (1-c)**2)


kmat = np.zeros_like(topo)

# for i in range(757):
#     kval = kge(np.mean(wrf[:, i]), np.mean(prism[:, i]))
sort_arg = np.argsort(topo)
wrf_sort = wrf[:, sort_arg]
prism_sort = prism[:, sort_arg]

for i in range(len(topo)):
    kmat[i] = kge(wrf_sort[:, i], prism_sort[:, i])
