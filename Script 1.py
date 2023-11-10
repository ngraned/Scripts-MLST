#!/usr/bin/env python

#run as common_core_genes.py gene_presence_absence_big gene_presence_absence_small common_core_groups.csv

import sys, csv
import pandas as pd

gpabig = pd.read_csv(sys.argv[1], low_memory=False)
gpasmall = pd.read_csv(sys.argv[2], low_memory=False)
ccg = sys.argv[3]

gpabig_trim = gpabig.drop(columns=["Non-unique Gene name", "Annotation", "No. isolates", "No. sequences", "Avg sequences per isolate", "Genome Fragment", "Order within Fragment", "Accessory Fragment", "Accessory Order with Fragment", "QC", "Min group size nuc", "Max group size nuc", "Avg group size nuc"])
gpasmall_trim = gpasmall.drop(columns=["Non-unique Gene name", "Annotation", "No. isolates", "No. sequences", "Avg sequences per isolate", "Genome Fragment", "Order within Fragment", "Accessory Fragment", "Accessory Order with Fragment", "QC", "Min group size nuc", "Max group size nuc", "Avg group size nuc"])

gpabig_core = gpabig_trim.dropna()
gpasmall_core = gpasmall_trim.dropna()

gpasmall_columns = list(gpasmall_core.columns)

gpabig_core = gpabig_core[gpasmall_columns]

melted_gpabig_core = pd.melt(gpabig_core, id_vars=['Gene'], var_name='Isolate', value_name='Locus_tag')
melted_gpasmall_core = pd.melt(gpasmall_core, id_vars=['Gene'], var_name='Isolate', value_name='Locus_tag')

merged_dfs = pd.merge(melted_gpabig_core, melted_gpasmall_core, how='outer', on='Locus_tag', suffixes=['_big', '_small'])
merged_dfs.to_csv(ccg+'.merged_on_locus_tag.csv', index=False)

merged_gene_list = merged_dfs.dropna().drop(columns=['Isolate_big','Isolate_small','Locus_tag']).drop_duplicates(ignore_index=True)
merged_gene_list.to_csv(ccg+'.core_gene_list.csv', index=False)

gpabig_core_only = gpabig[gpabig['Gene'].isin(merged_gene_list['Gene_big'])]
gpabig_core_only.to_csv(ccg+'.'+sys.argv[1], index=False)
gpasmall_core_only = gpasmall[gpasmall['Gene'].isin(merged_gene_list['Gene_small'])]
gpasmall_core_only.to_csv(ccg+'.'+sys.argv[2], index=False)
