#!/bin/bash

# Declare an array of string with type
declare -a StringArray=("000" "000.234361" "001" "002" "003" "004" "005" "010" "015" "020" "025" "030" "050" "075" "090" "100")
#declare -a StringArray=("1")

source ~/packages/IC/setup_IC.sh
# Iterate the string array using for loop
for pct in ${StringArray[@]}; do
	python ~/packages/Helium3Studies/scripts/merge_files.py "$SCRATCH/guenette_lab/Users/$USER/NeutronStudies/Thermal/Xe131_Thermal_${pct}pct/*/*.h5" "$SCRATCH/guenette_lab/Users/$USER/NeutronStudies/Thermal/Xe131_Thermal_${pct}pct/ThemalNeutrons_to_Xe137_Xe131_${pct}.h5"
done
conda deactivate
conda deactivate
