#!/bin/bash
 
# Declare an array of string with type
declare -a StringArray=("000" "000.234361" "001" "002" "003" "004" "005" "010" "015" "020" "025" "030" "050" "075" "090" "100")
 
# Iterate the string array using for loop
for pct in ${StringArray[@]}; do
   echo "Making jobscripts for percentage: $pct"
   mkdir -p $pct
   cd $pct
   cp ../Xe131_Thermal_job.sh .
   sed -i "s#.*SBATCH -J.*#\#SBATCH -J Xe131_Thermal_${pct}pct \# A single job name for the array#" Xe131_Thermal_job.sh
   sed -i "s#.*SBATCH -o.*#\#SBATCH -o Xe131_Thermal_${pct}pct_%A_%a.out \# Standard output#" Xe131_Thermal_job.sh
   sed -i "s#.*SBATCH -e.*#\#SBATCH -e Xe131_Thermal_${pct}pct_%A_%a.err \# Standard error#" Xe131_Thermal_job.sh
   sed -i "s#.*Pct=.*#Pct=${pct}#" Xe131_Thermal_job.sh
   sbatch --array=1-10 Xe131_Thermal_job.sh
   cd ..
done
