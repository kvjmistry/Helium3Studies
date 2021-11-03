#!/bin/bash

# Declare an array of string with type
declare -a StringArray=("000" "000.234361" "001" "002" "003" "004" "005" "010" "015" "020" "025" "030" "050" "075" "090" "100")
#declare -a StringArray=("1")

# Iterate the string array using for loop
for pct in ${StringArray[@]}; do
	rm -rv ${pct}
	rm -rv $SCRATCH/guenette_lab/Users/$USER/NeutronStudies/Thermal/Xe131_Thermal_${pct}pct
done
