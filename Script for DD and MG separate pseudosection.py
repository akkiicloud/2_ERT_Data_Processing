# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 17:25:05 2026

This script can be used for plotting pseudosections for DD and MG separately for raw ERT data.
The input file is mg_only_Wendelsheim.xlsx
This code can be also used for DD with changing in the formula for X_app and Z_app. 


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

file_path = r"D:\ERT_1_Wendelsheim\ERT_250625_Wendelsheim\Main_data\1-Unfilter data\MG Unfilter\mg_only_Wendelsheim.xlsx"
df = pd.read_excel(file_path) # Remember the name :df

# # Rename columns for convenience to plot in future.
df.columns = ['El_array', 'Spa1', 'Spa2', 'Spa3', 'Spa4', 'Rho', 'dev', 'M', 'Sp', 'Vp', 'In']



# Calculate geometric factor k
B, C, D, E = df['Spa1'], df['Spa2'], df['Spa3'], df['Spa4'] # Assigning simple name for Spa1...Spa4. 
term1 = 1 / abs(B - D)
term2 = 1 / abs(C - D)
term3 = 1 / abs(B - E)
term4 = 1 / abs(C - E)
df['k'] = 2 * np.pi/(term1 - term2 - term3 + term4)

# FOR DD###########################

#Xapp_DD = (B + D) / 2
# np.minimum(a, b), returns the minimum value
#Zapp_DD = np.abs((E - C) / 2)
###################################

# FOR MG###########################

Xapp_MG = (D + C) / 2
Zapp_MG = np.minimum(Xapp_MG - B, E - Xapp_MG)
###################################

df['Xapp'] = Xapp_MG
df['Zapp'] = np.abs(Zapp_MG)


df = df[df['Zapp'] <= 60]

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
sc1 = axs[0,0].scatter(df['Xapp'], df['Zapp'],
                       c=np.abs(df['Rho']), s=20, cmap='jet',
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
sc2 = axs[0,1].scatter(df['Xapp'], df['Zapp'],
                       c=df['k'], s=20, cmap='jet',
                       norm=colors.TwoSlopeNorm(vmin=-6000, vcenter=0, vmax=6000),
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
sc3 = axs[1,0].scatter(df['Xapp'], df['Zapp'],
                       c=df['dev'], s=20, cmap='jet',
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
sc4 = axs[1,1].scatter(df['Xapp'], df['Zapp'],
                       c=np.abs(df['Vp']), s=20, cmap='jet',
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

print((df['Zapp'] < 0).sum())

plt.show()