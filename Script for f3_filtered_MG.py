

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# ==========================================================
# Read Excel
# ==========================================================

file_path = r"D:\ERT_2_Pfaffingen\dev_10 rho_ERT_26_Pfaffingen\8 filters\202604combined_f3_dev5_k10000_v05.xlsx"

df = pd.read_excel(file_path)

# # Rename columns for convenience to plot in future.
df.columns = ['El_array','Spa.1','Spa.2', 'Spa.3','Spa.4','Spa1', 'Spa2', 'Spa3', 'Spa4', 'Rho', 'dev', 'M', 'Sp', 'Vp', 'In','k']

# ==========================================================
# Separate DD and MG measurements
# ==========================================================

# DD: Excel rows 2–5535 and 9712–13499


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
# ==========================================================
# APPARENT ELECTRODE POSITIONS FOR DD
# ==========================================================

B = df_MG['Spa.1']
C = df_MG['Spa.2']
D = df_MG['Spa.3']
E = df_MG['Spa.4']

# Mid-Gradient pseudosection coordinates
Xapp_MG = (C + D) / 2
Zapp_MG = np.minimum(Xapp_MG - B, E - Xapp_MG)

df_MG['Xapp'] = Xapp_MG
df_MG['Zapp'] = np.abs(Zapp_MG)

# Keep shallow data only

df_MG = df_MG[df_MG['Zapp'] <= 60].copy()

print(df_DD[['Spa1','Spa2','Spa3','Spa4']].head())

# ==========================================================
# Plot style
# ==========================================================

plt.rcParams.update({
    "font.size": 14,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
})

# ==========================================================
# Figure
# ==========================================================

fig, axs = plt.subplots(2,2,
                        figsize=(12,11),
                        dpi=400)

plt.subplots_adjust(left=0.09,
                    right=0.86,
                    hspace=0.25,
                    wspace=0.25)

# ==========================================================
# (a) Apparent resistivity
# ==========================================================

sc1 = axs[0,0].scatter(
    df_MG['Xapp'],
    df_MG['Zapp'],
    c=np.abs(df_MG['Rho']),
    s=20,
    cmap='jet',
    norm=colors.LogNorm(vmin=1, vmax=1000),
    edgecolors='none'
)

axs[0,0].set_xlim(0,360)
axs[0,0].set_ylim(60,0)
axs[0,0].grid(ls='--',alpha=0.4)
axs[0,0].set_xlabel("Distance (m)")
axs[0,0].set_ylabel("Depth (m)")


cbar = plt.colorbar(sc1,
                    ax=axs[0,0],
                    orientation='horizontal',
                    pad=0.18)

cbar.set_label("Apparent resistivity (Ωm)")

# ==========================================================
# (b) Geometric factor
# ==========================================================

sc2 = axs[0,1].scatter(
    df_MG['Xapp'],
    df_MG['Zapp'],
    c=df_MG['k'],
    s=20,
    cmap='jet',
    norm=colors.TwoSlopeNorm(
        vmin=-6000,
        vcenter=0,
        vmax=6000),
    edgecolors='none'
)

axs[0,1].set_xlim(0,360)
axs[0,1].set_ylim(60,0)
axs[0,1].grid(ls='--',alpha=0.4)
axs[0,1].set_xlabel("Distance (m)")
axs[0,1].set_ylabel("Depth (m)")


cbar = plt.colorbar(sc2,
                    ax=axs[0,1],
                    orientation='horizontal',
                    pad=0.18)

cbar.set_label("Geometric factor")

# ==========================================================
# (c) Stacking error
# ==========================================================

sc3 = axs[1,0].scatter(
    df_MG['Xapp'],
    df_MG['Zapp'],
    c=df_MG['dev'],
    s=20,
    cmap='jet',
    norm=colors.LogNorm(vmin=1,vmax=1000),
    edgecolors='none'
)

axs[1,0].set_xlim(0,360)
axs[1,0].set_ylim(60,0)
axs[1,0].grid(ls='--',alpha=0.4)
axs[1,0].set_xlabel("Distance (m)")
axs[1,0].set_ylabel("Depth (m)")


cbar = plt.colorbar(sc3,
                    ax=axs[1,0],
                    orientation='horizontal',
                    pad=0.18)

cbar.set_label("Stacking error (%)")

# ==========================================================
# (d) Voltage
# ==========================================================

sc4 = axs[1,1].scatter(
    df_MG['Xapp'],
    df_MG['Zapp'],
    c=np.abs(df_MG['Vp']),
    s=20,
    cmap='jet',
    norm=colors.LogNorm(vmin=1,vmax=1000),
    edgecolors='none'
)

axs[1,1].set_xlim(0,360)
axs[1,1].set_ylim(60,0)
axs[1,1].grid(ls='--',alpha=0.4)
axs[1,1].set_xlabel("Distance (m)")
axs[1,1].set_ylabel("Depth (m)")


cbar = plt.colorbar(sc4,
                    ax=axs[1,1],
                    orientation='horizontal',
                    pad=0.18)

cbar.set_label("Voltage (mV)")

# ==========================================================
# Panel labels
# ==========================================================

fig.text(0.06,0.90,"(a)",fontsize=14,fontweight='bold')
fig.text(0.52,0.90,"(b)",fontsize=14,fontweight='bold')
fig.text(0.06,0.47,"(c)",fontsize=14,fontweight='bold')
fig.text(0.52,0.47,"(d)",fontsize=14,fontweight='bold')

plt.show()