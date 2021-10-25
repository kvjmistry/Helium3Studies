#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 13:51:02 2019
@author: rogerslc
"""
import os
import sys
import tables as tb
import pandas as pd
import numpy as np

import glob
from glob import iglob


def load_mc_particles(iFileName: str) -> pd.DataFrame:

    # Loading data
    extents   = pd.read_hdf(iFileName, 'MC/extents')

    with tb.open_file(iFileName ,mode='r') as iFile:
        parts_tb = iFile.root.MC.particles

        # Generating parts DataFrame
        parts = pd.DataFrame({'particle_id'    : parts_tb.col('particle_indx'),
                              'name'           : parts_tb.col('particle_name').astype('U20'),
                              'primary'        : parts_tb.col('primary').astype('bool'),
                              'mother_id'      : parts_tb.col('mother_indx'),
                              'kin_energy'     : parts_tb.col('kin_energy'),
                              'creator_proc'   : parts_tb.col('creator_proc').astype('U20')})

        # Adding event info
        evt_part_df = extents[['last_particle', 'evt_number']]
        evt_part_df.set_index('last_particle', inplace = True)
        parts = parts.merge(evt_part_df, left_index=True, right_index=True, how='left')
        parts.rename(columns={"evt_number": "event_id"}, inplace = True)
        parts.event_id.fillna(method='bfill', inplace = True)
        parts.event_id = parts.event_id.astype(int)

        # Setting the indexes
        parts.set_index(['event_id', 'particle_id'], inplace=True)

    return parts




#path to the data
locat = sys.argv[1]
# path to save the file
savelocat = sys.argv[2]

start_file = int(sys.argv[3])
end_file   = int(sys.argv[4])
nrg=str(10000000)
#nrg='1e-06'
perc=str(100)
PERCS=[90,91,92,93,94,95,96,97,98,98.5,99,99.25,99.5,99.75]
PERCS=[99.85,99.92]
#fileformat= 'InternalNeutrons-{}-FIELD_CAGE_Xe'+perc+'.h5'


for P in PERCS:
    perc=str(P)
    fileformat= 'InternalNeutrons-{}-FIELD_CAGE_Xe'+perc+'minE'+nrg+'.h5'
    xe137muonnrgs=[]
    total_sim_events = 0
    for i in range(start_file, end_file):
        fn = locat + fileformat.format(str(i).zfill(4))
        print("Starting on file "+fn)

        try:
            evt_nums = pd.read_hdf(fn, 'MC/extents').evt_number.unique()
            part_muon_data =load_mc_particles(fn)
            config    = pd.read_hdf(fn, 'MC/configuration')
            evtInFile = int(config[config.param_key.str.contains("num_events")].param_value.iloc[0])
        except FileNotFoundError:
            print('File not there')
            continue
        except KeyError:
            print('No FUCKING EXTENTS...')
            continue
        except tb.HDF5ExtError:
            print('Fucked file')
            continue
        except OSError:
            print('Another type of fucked')
            continue
        except IndexError:
            print('No-one knows why the fuck this happens')
            continue


        total_sim_events += evtInFile

        for t in evt_nums:
            xe137 = part_muon_data.loc[t][part_muon_data.loc[t].name.str.contains('Xe137')]
            numofxe137 = len(xe137)
            muon = part_muon_data.loc[t][part_muon_data.loc[t].primary]
            for i in  range(numofxe137):
                xe137muonnrgs.append(muon.kin_energy.iloc[0])

    xe137_out = savelocat+'Xe137_counts_sim'+str(total_sim_events)+'neutrons_f'+str(start_file)+'-'+str(end_file)+'_'+perc+'He3E'+nrg+'.h5'
    pd.DataFrame({'Xemunrg':xe137muonnrgs}).to_hdf(xe137_out,'munnuenergy')