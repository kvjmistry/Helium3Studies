import os
import numpy as np
from time      import time
from Def       import *


cwd = os.getcwd()

TemplateCONF  = cwd + "/../Config_Templates/NextTon_muons_vertical.config.mac"
TemplateINIT  = cwd + "/../Config_Templates/NextTon_muons_vertical.init.mac"

MacrosDir  =  "/n/holylfs02/LABS/guenette_lab/users/lrogers/Winter/data/Helium3_01percent/Config/"
OutputDir  =  "/n/holylfs02/LABS/guenette_lab/users/lrogers/Winter/data/Helium3_01percent/Output/"
ScriptDir  =  "/n/holylfs02/LABS/guenette_lab/users/lrogers/Winter/data/Helium3_01percent/Scripts/"
LogDir     =  "/n/holylfs02/LABS/guenette_lab/users/lrogers/Winter/data/Helium3_01percent/Logs/"

NexusDir      = "/n/holylfs02/LABS/guenette_lab/software/next/nexus/build_neutron_muon_studies/source/nexus"

## Put the config specific variables in a dictionary
## That way you can only put the ones you need
config_vars = {}
config_vars['active_diam']    = 260
config_vars['active_length']  = 260
config_vars['fcage_thickn']   = 1
config_vars['ics_thickn']     = 12
config_vars['vessel_thickn']  = 2
config_vars['gas_temperature'] = 300
config_vars['gas_pressure']    = 15
config_vars['Xe136DecayMode']  = 1 # Decay0 interface for BB decays ... (BB0nu: DecayMode 1), (BB2nu: DecayMode 4)
config_vars['threshold']      = 2.3
config_vars['min_eng']        = 1
config_vars['max_eng']        = 3000
config_vars['region']         ="MUONS"

WorkType = "Muons"
import random
SEED = random.sample(range(10, 10000000), 100003)
seed_index = 1

Njobs    = int(100000)
Njobs=int(400000)
Nevents  = int(250)
    
for i in range(Njobs):
    seed_index += 1
    config_vars['seed']     = SEED[seed_index]
    eventnum     =   (i+1)*Nevents
    config_vars['event_id'] = eventnum

    GEN_CONFIGURATION(i, TemplateCONF, WorkType, MacrosDir, **config_vars)
    
    GEN_INITIALIZATION(i, TemplateINIT, WorkType, MacrosDir, config_vars['region'] )
    
    ScriptGen(i, Nevents, WorkType, MacrosDir, OutputDir,
                  ScriptDir, LogDir, NexusDir, config_vars['region'])

    
