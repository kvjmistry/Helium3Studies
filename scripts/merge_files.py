import pandas as pd
import sys
import glob

filewildcard = sys.argv[1]
files = glob.glob(filewildcard)

print(files)

Metadata = []
Energy   = []
Other    = []

for f in files:
    Metadata.append(pd.read_hdf(f,'Metadata'))
    Energy.append(pd.read_hdf(f,'Energy'))
    Other.append(pd.read_hdf(f,'Other'))

Metadata_m = pd.concat(Metadata)
Energy_m   = pd.concat(Energy)
Other_m    = pd.concat(Other)

print(Metadata_m)

file_out = sys.argv[2]
Energy_m.to_hdf(file_out,'Energy')
Metadata_m.to_hdf(file_out,'Metadata')
Other_m.to_hdf(file_out,'Other')

