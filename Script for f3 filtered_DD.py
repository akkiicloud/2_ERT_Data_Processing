# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 17:43:57 2026

@author: akagupta
"""

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.colors as colors
from matplotlib.colors import SymLogNorm
from matplotlib import colors
import matplotlib.gridspec as gridspec

file_path = r"D:\ERT_2_Pfaffingen\dev_10 rho_ERT_26_Pfaffingen\8 filters\202604combined_f3_dev5_k10000_v05.xlsx"
df = pd.read_excel(file_path) # Remember the name :df

# # Rename columns for convenience to plot in future.
df.columns = ['El_array','Spa.1','Spa.2', 'Spa.3','Spa.4','Spa1', 'Spa2', 'Spa3', 'Spa4', 'Rho', 'dev', 'M', 'Sp', 'Vp', 'In','k']

# ==========================================================
# Separate DD and MG measurements based on Excel row numbers
# (Excel rows are 1-based, pandas indices are 0-based)
# ==========================================================

# DD: Excel rows 2–5535 and 9712–13499
df_DD = pd.concat([
    df.iloc[0:5146], 
    df.iloc[8995:9215],       # Excel rows 2–5535
    df.iloc[9693:15014],
    df.iloc[18589:18946]     
])

# MG: Excel rows 5536–9711 and 13500–16546
df_MG = pd.concat([
    df.iloc[5147:8994],     # Excel rows 5536–9711
    df.iloc[9216:9692],
    df.iloc[15015:18588],
    df.iloc[18947:19595]    
])

# Reset indices
df_DD = df_DD.reset_index(drop=True)
df_MG = df_MG.reset_index(drop=True)



# Calculate geometric factor k
B, C, D, E = df_DD['Spa.1'], df_DD['Spa.2'], df_DD['Spa.3'], df_DD['Spa.4'] # Assigning simple name for Spa1...Spa4. 
# term1 = 1 / abs(B - D)
# term2 = 1 / abs(C - D)
# term3 = 1 / abs(B - E)
# term4 = 1 / abs(C - E)
# df['k'] = 2 * np.pi/(term1 - term2 - term3 + term4)

# FOR DD###########################

Xapp_DD = (B + D) / 2
# np.minimum(a, b), returns the minimum value
Zapp_DD = np.abs((E - C) / 2)
###################################

# FOR MG###########################

#Xapp_MG = (D + C) / 2
#Zapp_MG = np.minimum(Xapp_MG - B, E - Xapp_MG)
###################################



df_DD['Xapp'] = Xapp_DD
df_DD['Zapp'] = Zapp_DD

df_DD = df_DD[df_DD['Zapp'] <= 60].copy()

print(df[['Spa1','Spa2','Spa3','Spa4']].iloc[0])

# ---------------- GLOBAL STYLE ----------------
plt.rcParams.update({
    "font.size": 14,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
})

# ---------------- FIGURE ----------------
fig, axs = plt.subplots(2, 2, figsize=(12,11), dpi=400)

plt.subplots_adjust(left=0.09, right=0.85, hspace=0.20, wspace=0.25)

# ---------------- (a) RHO ----------------
sc1 = axs[0,0].scatter(df_DD['Xapp'], df_DD['Zapp'],
                       c=np.abs(df_DD['Rho']), s=20, cmap='jet',
                       norm=colors.LogNorm(vmin=1, vmax=1000),
                       edgecolors='none')

axs[0,0].set_xlabel(r"Distance (m)")
axs[0,0].set_ylabel(r"Depth (m)")
axs[0,0].set_xlim(0,360)
axs[0,0].set_ylim(0,60)
axs[0,0].invert_yaxis()
axs[0,0].grid(True, linestyle="--", alpha=0.4)

cbar1 = plt.colorbar(sc1, ax=axs[0,0], orientation='horizontal', pad=0.20)
cbar1.set_label(r"Apparent resistivity (Ωm)")


# ---------------- (b) K ----------------
sc2 = axs[0,1].scatter(df_DD['Xapp'], df_DD['Zapp'],
                       c=df_DD['k'], s=20, cmap='jet',
                       norm=colors.TwoSlopeNorm(vmin=-15000, vcenter=0, vmax=15000),
                       edgecolors='none')

axs[0,1].set_xlabel(r"Distance (m)")
axs[0,1].set_ylabel(r"Depth (m)")
axs[0,1].set_xlim(0,360)
axs[0,1].set_ylim(0,60)
axs[0,1].invert_yaxis()
axs[0,1].grid(True, linestyle="--", alpha=0.4)

cbar2 = plt.colorbar(sc2, ax=axs[0,1], orientation='horizontal', pad=0.20)
cbar2.set_label("Geometric factor")


# ---------------- (c) DEV ----------------
sc3 = axs[1,0].scatter(df_DD['Xapp'], df_DD['Zapp'],
                       c=df_DD['dev'], s=20, cmap='jet',
                       norm=colors.LogNorm(vmin=1, vmax=1000),
                       edgecolors='none')

axs[1,0].set_xlabel(r"Distance (m)")
axs[1,0].set_ylabel(r"Depth (m)")
axs[1,0].set_xlim(0,360)
axs[1,0].set_ylim(0,60)
axs[1,0].invert_yaxis()
axs[1,0].grid(True, linestyle="--", alpha=0.4)

cbar3 = plt.colorbar(sc3, ax=axs[1,0], orientation='horizontal', pad=0.20)
cbar3.set_label("Stacking error (%)")


# ---------------- (d) VP ----------------
sc4 = axs[1,1].scatter(df_DD['Xapp'], df_DD['Zapp'],
                       c=np.abs(df_DD['Vp']), s=20, cmap='jet',
                       #norm=SymLogNorm(linthresh=1, vmin=-1000, vmax=1000)
                       norm=colors.LogNorm(vmin=1, vmax=1000),
                       edgecolors='none')

axs[1,1].set_xlabel(r"Distance (m)")
axs[1,1].set_ylabel(r"Depth (m)")
axs[1,1].set_xlim(0,360)
axs[1,1].set_ylim(0,60)
axs[1,1].invert_yaxis()
axs[1,1].grid(True, linestyle="--", alpha=0.4)

cbar4 = plt.colorbar(sc4, ax=axs[1,1], orientation='horizontal', pad=0.20)
cbar4.set_label("Voltage (mV)")


# ---------------- PANEL LABELS (OUTSIDE) ----------------
fig.text(0.06, 0.90, "(a)", fontsize=14, fontweight="bold")
fig.text(0.52, 0.90, "(b)", fontsize=14, fontweight="bold")
fig.text(0.06, 0.49, "(c)", fontsize=14, fontweight="bold")
fig.text(0.52, 0.49, "(d)", fontsize=14, fontweight="bold")



plt.show()
