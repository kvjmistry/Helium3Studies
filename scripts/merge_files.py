import pandas as pd
import sys
import glob

filewildcard = sys.argv[1]
files = glob.glob(filewildcard)

print(files)

Metadata = []
Energy   = []

for f in files:
    Metadata.append(pd.read_hdf(f,'Metadata'))
    Energy.append(pd.read_hdf(f,'Energy'))

Metadata_m = pd.concat(Metadata)
Energy_m   = pd.concat(Energy)

print(Metadata_m)

file_out = sys.argv[2]
Energy_m.to_hdf(file_out,'Energy')
Metadata_m.to_hdf(file_out,'Metadata')

