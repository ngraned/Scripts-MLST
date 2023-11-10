#!/usr/bin/env python

import pandas as pd
import numpy as np
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

df = pd.read_csv(infile)

for f in list(df.columns)[14:]:
    df.loc[df[f].str.contains('refound', na=False)] = np.NAN

df.to_csv(outfile, index=False)
