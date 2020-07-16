#!/usr/bin/env python

from pathlib import Path

import pandas as pd

files = sorted([f for f in Path().glob("data/**/*-1-country-inputs.csv")])
print("Num files", len(files))


for i, f in enumerate(files):
    co = f.stem.split("-")[0]
    print(co)
    pop = pd.read_csv(f, usecols=["Pop"])

    pop = pop.assign(Bin=pd.cut(pop.Pop, bins=[0, 10, 100, 500, 1e3, 1e4, 1e5, 1e99]))
    clust_count = pop.Bin.value_counts().sort_index().rename(co)
    pop_count = pop.groupby("Bin").sum().Pop.rename(co)

    clust_pc = clust_count / clust_count.sum()
    pop_pc = pop_count / pop_count.sum()

    if i == 0:
        df_clust_count = pd.DataFrame(clust_count)
        df_clust_pc = pd.DataFrame(clust_pc)
        df_pop_count = pd.DataFrame(pop_count)
        df_pop_pc = pd.DataFrame(pop_pc)
    else:
        df_clust_count[co] = clust_count
        df_clust_pc[co] = clust_pc
        df_pop_count[co] = pop_count
        df_pop_pc[co] = pop_pc

    df_clust_count.to_csv("df_clust_count.csv")
    df_clust_pc.to_csv("df_clust_pc.csv")
    df_pop_count.to_csv("df_pop_count.csv")
    df_pop_pc.to_csv("df_pop_pc.csv")
