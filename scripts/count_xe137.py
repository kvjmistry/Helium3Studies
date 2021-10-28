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
python count_xe137.py <input mode> <wildcard to files>
    
<input mode>: # muon, Tneutron, Fneutron. (Tneutron = thermal neutron, Fneutron = fast neutron)


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
# Configuration Parameters
mode = sys.argv[1] # muon, Tneutron, Fneutron. (Tneutron = thermal neutron, Fneutron = fast neutron)
print("Input mode is:", sys.argv[1])

Total_Num_Events   = 0
Total_Saved_Events = 0

# Array for simulated primary uon/neutron energies that go on to produce Xe137
E_Xe137 = [] 

# Array for all simulated muon energies -- currently cant retrieve due to saved info in the file
# Muon_E = [] 
# ----------------------------------------------------------------------------------------
filewildcard = sys.argv[2]
files = glob.glob(filewildcard)
print(files)
print("Total files read in:", len(files))

# Loop over the files
for f in files:
    # Load the configurations
    config = load_mcconfiguration(f) 
    print(config)

    # Load in the MC Particles
    MC_Particles = load_mcparticles_df(f)
    print(MC_Particles)

    # Get the total number of events in the file
    Num_Events = int( config[config.param_key.str.contains("num_events")].param_value.iloc[0]  )
    Total_Num_Events+=Num_Events
    print("Total number of events in file:", Num_Events)

    # Start ID of events
    Start_ID = int( config[config.param_key.str.contains("start_id")].param_value.iloc[0]  )
    print("Start ID:", Start_ID)

    # Total number of saved events (i.e muons that interact)
    Saved_Events = int( config[config.param_key.str.contains("saved_events")].param_value.iloc[0]  )
    Total_Saved_Events+=Saved_Events
    print("Saved Events:", Saved_Events)

    # Percentage of Xenon
    pct  = str( config[config.param_key.str.contains("XePercentage")].param_value.iloc[0]  )
    print("Xenon Percentage Simulated:", pct)

    # Loop over the saved events in the file
    for t in range(Start_ID, Start_ID + Saved_Events):
        
        # Inform the user of the event number
        if mode == "muon":
            print("On event: ", t - Start_ID)

        if (t % 1000 == 0 and mode != "muon"):
            print("On event: ", t - Start_ID)
        
        # Primary Muons/Neutron 
        primary = MC_Particles.loc[t][MC_Particles.loc[t].primary]

        # Total Xe137 Produced
        xe137 = MC_Particles.loc[t][MC_Particles.loc[t].particle_name.str.contains('Xe137')]
        Num_Xe137 = len(xe137)
        
        if (Num_Xe137 > 0):
            print("Neutron capture(s) leading to", Num_Xe137, "Xe137")
            
        # Loop over the numner of Xe137 produced and append the primary muon energy
        for i in range(Num_Xe137):
            E_Xe137.append(primary.kin_energy.iloc[0])
    # ---------
# ---------

# Write the outputs to file
if (mode == "muons"):
    file_out = 'muons_to_Xe137_He_'+ pct +'.h5'
elif (mode == "Tneutron"):
    file_out = 'ThemalNeutrons_to_Xe137_He_'+ pct +'.h5'
elif (mode == "Fneutron"):
    file_out = 'FastNeutrons_to_Xe137_He_'+ pct +'.h5'

pd.DataFrame({'E_Xe137':E_Xe137}).to_hdf(file_out,'Energy')
pd.DataFrame({'Num_Events':[Total_Num_Events], 'Saved_Events':[Total_Saved_Events], 'Percentage':[pct]}).to_hdf(file_out,'Metadata')