#!/bin/bash
#SBATCH -J Xe_He3_Thermal_0_1pct # A single job name for the array
#SBATCH -c 1 # Number of cores
#SBATCH -p shared # Partition
#SBATCH --mem 4000 # Memory request (4Gb)
#SBATCH -t 0-2:00 # Maximum execution time (D-HH:MM)
#SBATCH -o Xe_He3_Thermal_0_1pct_%A_%a.out # Standard output
#SBATCH -e Xe_He3_Thermal_0_1pct_%A_%a.err # Standard error

echo "Initialising NEXUS environment"
start=`date +%s`

# Gas percentage
Pct=99.9
echo "Configuring gas percentage: $Pct"

# Create the directory
cd $SCRATCH/guenette_lab/Users/$USER/
mkdir -p Xe_He3_Thermal_${Pct}pct/jobid_"${SLURM_ARRAY_TASK_ID}"
cd Xe_He3_Thermal_${Pct}pct/jobid_"${SLURM_ARRAY_TASK_ID}"

# Copy the file over
cp ~/packages/Helium3Studies/macros_/NextTon_ThermalNeutrons_XeHe.config.mac .
cp ~/packages/Helium3Studies/macros_/NextTon_ThermalNeutrons_XeHe.init.mac .
cp ~/packages/nexus/macros/physics/Xe137.mac .

# Edit the file configs
sed -i "s#.*Xe137.mac.*#/nexus/RegisterDelayedMacro Xe137.mac#" NextTon_ThermalNeutrons_XeHe.init.mac
sed -i "s#.*NextTon_ThermalNeutrons_XeHe.*#/nexus/RegisterMacro NextTon_ThermalNeutrons_XeHe.config.mac#" NextTon_ThermalNeutrons_XeHe.init.mac
sed -i "s#.*XePercentage.*#/Geometry/NextTonScale/XePercentage $Pct#" NextTon_ThermalNeutrons_XeHe.config.mac
sed -i "s#.*outputFile.*#/nexus/persistency/outputFile NextTon_ThermalNeutron_XeHe.next#" NextTon_ThermalNeutrons_XeHe.config.mac

# Setup nexus and run
echo "Setting Up NEXUS"
source ~/packages/nexus/setup_nexus.sh

echo "Running NEXUS"
for i in {1..10}; do

	# Replace the seed in the file	
	echo "The seed number is: $((1111111*${SLURM_ARRAY_TASK_ID}+$i))"
	sed -i "s#.*random_seed.*#/nexus/random_seed $((1111111*${SLURM_ARRAY_TASK_ID}+$i))#" NextTon_ThermalNeutrons_XeHe.config.mac
	
	~/packages/nexus/bin/nexus -n 10000 NextTon_ThermalNeutrons_XeHe.init.mac  2>&1 | tee log_nexus_"${SLURM_ARRAY_TASK_ID}".txt

	# Rename the output file
	mv NextTon_ThermalNeutron_XeHe.next.h5 "$(basename NextTon_ThermalNeutron_XeHe.next.h5 .next.h5)_${SLURM_ARRAY_TASK_ID}_$i.next.h5"
	echo; echo; echo;
done

# Now setting up invisible cities
echo "Executing Xe 137 Counting Script"
source ~/packages/IC/setup_IC.sh
python ~/packages/Helium3Studies/scripts/count_xe137.py Tneutron "NextTon_ThermalNeutron*.h5" 2>&1 | tee -a log_nexus_"${SLURM_ARRAY_TASK_ID}".txt
mv ThemalNeutrons_to_Xe137_He_${Pct}.h5 "$(basename ThemalNeutrons_to_Xe137_He_${Pct}.h5 .h5)_${SLURM_ARRAY_TASK_ID}.h5"

# Cleaning up
rm -v NextTon_ThermalNeutron*.h5

echo "FINISHED....EXITING"
end=`date +%s`
runtime=$((end-start))
echo "$runtime s"
