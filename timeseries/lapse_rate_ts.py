from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np


dataDir = Path('/Volumes/Transcend/EastRiverClimatePaper/data')

topo = dataDir.joinpath('east_topo.npy')
wrf = dataDir.joinpath('WRF_wy2017_daily_east_only_tmean.npy')
prism = dataDir.joinpath('PRISM_wy2017_daily_east_only_tmean.npy')

topo = np.load(topo)
wrf = np.load(wrf)
prism = np.load(prism)

def calc_inversion(topo, var, frac=2):  # i.e. the botom is 1/3 of the valley 
    tsort = np.sort(topo)
    top_min = int(len(tsort)*.5)
    bottom_max = int(len(tsort)*.5)
    valley = np.argwhere(topo < topo[bottom_max])
    highs = np.argwhere(topo > topo[top_min])

    highs_var = np.median(var[:, highs[:, 0]], axis=1)
    valley_var = np.median(var[:, valley[:, 0]], axis=1)

    inversion = valley_var - highs_var

    piv, tsort = calc_inversion(topo, prism, frac=2)
    wiv, tsort = calc_inversion(topo, wrf, frac=2)

    plt.plot(piv, label='prism')
    plt.plot(wiv, label='wrf')
    plt.legend()
    plt.show()

    return inversion, tsort


def degree_days(topo, var):
    pass


