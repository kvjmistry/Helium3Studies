#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on October 2021
@author: Krishan Mistry

Script to read in simulated muon or neutron events that generate Xe127 in Nexus.

Returns an output .h5 file containing two dataframes:
Events  : contains the energies of muons that go on to produce Xe137
Metadata: contains the number of muons simulated and number that interact inside the TPC

Usage (Requires Invisible Cities to be setup in order to run):
python count_xe137_from_neutrons_nrgs_v2.py

"""
import os
import sys
import pandas as pd
import numpy as np
import glob
from glob import iglob
from invisible_cities.io.mcinfo_io import load_mcparticles_df
from invisible_cities.io.mcinfo_io import load_mcconfiguration

# ----------------------------------------------------------------------------------------
# Load the configurations
config = load_mcconfiguration("/Users/mistryk2/Packages/nexus/workdir/files/Muons.next.h5") 
print(config)

# Load in the MC Particles
MC_Particles = load_mcparticles_df("/Users/mistryk2/Packages/nexus/workdir/files/Muons.next.h5")
print(MC_Particles)
# ----------------------------------------------------------------------------------------

# Get the total number of events in the file
Num_Events = int( config[config.param_key.str.contains("num_events")].param_value.iloc[0]  )
print("Total number of events in file:", Num_Events)

# Start ID of events
Start_ID = int( config[config.param_key.str.contains("start_id")].param_value.iloc[0]  )
print("Start ID:", Start_ID)

# Total number of saved events (i.e muons that interact)
Saved_Events = int( config[config.param_key.str.contains("saved_events")].param_value.iloc[0]  )
print("Saved Events:", Saved_Events)

# Array for simulated muon energies that go on to produce Xe137
Muon_E_Xe137 = [] 

# Array for all simulated muon energies -- currently cant retrieve due to saved info in the file
Muon_E = [] 

# Loop over the saved events in the file
for t in range(Start_ID, Start_ID + Saved_Events):
    print("On event: ", t - Start_ID)
    
    # Primary Muons 
    Mu_primary = MC_Particles.loc[t][MC_Particles.loc[t].primary]

    # Total Xe137 Produced
    xe137 = MC_Particles.loc[t][MC_Particles.loc[t].particle_name.str.contains('Xe137')]
    Num_Xe137 = len(xe137)
    
    if (Num_Xe137 > 0):
        print("Neutron capture(s) leading to ", Num_Xe137, "Xe137")
        
    # Loop over the numner of Xe137 produced and append the primary muon energy
    for i in range(Num_Xe137):
        Muon_E_Xe137.append(Mu_primary.kin_energy.iloc[0])
# ---------

# Write the outputs to file
file_out = 'test.h5'
pd.DataFrame({'Muon_E_Xe137':Muon_E_Xe137}).to_hdf(file_out,'Energy')
pd.DataFrame({'Num_Events':[Num_Events], 'Saved_Events':[Saved_Events]}).to_hdf(file_out,'Metadata')