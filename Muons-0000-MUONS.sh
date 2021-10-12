#!/bin/bash
#SBATCH -n 1                # Number of cores 
#SBATCH -N 1                # Ensure that all cores are on one machine
#SBATCH -t 0-05:00          # Runtime in D-HH:MM, minimum of 10 minutes
#SBATCH -p guenette         # Partition to submit to 
#SBATCH --mem=2000          # Memory pool for all cores (see also --mem-per-cpu)
source /n/holylfs02/LABS/guenette_lab/software/next/ups_products/setup 
setup cmake  v3_14_3 
setup geant4 v4_10_5_p01 -q e17:prof 
setup gsl v2_5 -q prof 
setup root v6_16_00 -q e17:prof 
setup hdf5 v1_10_5 -q e17 
export LD_LIBRARY_PATH=/n/holylfs02/LABS/guenette_lab/software/next/GATE/2.0/lib:$LD_LIBRARY_PATH 

cd /n/holylfs02/LABS/guenette_lab/users/amcdonald/NEXT_TON_JOB_CONRTOL/JUNK 
/n/holylfs02/LABS/guenette_lab/software/next/nexus/build_neutron_muon_studies/source/nexus -b -n 250 /n/holylfs02/LABS/guenette_lab/users/lrogers/Winter/data/Helium3_01percent/Config/Muons-0000-MUONS.init.mac >& /scratch/Muons-0000-MUONS.log
mv /scratch/Muons-0000-MUONS.log /n/holylfs02/LABS/guenette_lab/users/lrogers/Winter/data/Helium3_01percent/Logs/
mv /scratch/Muons-0000-MUONS.h5 /n/holylfs02/LABS/guenette_lab/users/lrogers/Winter/data/Helium3_01percent/Output/
