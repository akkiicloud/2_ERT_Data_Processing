# 2_ERT_Data_Processing

## Overview

This repository contains the Python scripts developed for processing ERT data acquired during this study. The scripts were primarily written for the Wendelsheim and Pfäffingen data sets but can also be applied to other ERT datasets with minor modifications.

> **Important**
>
> The scripts should be executed in the order presented below. Each script produces the input required for the next processing step.

Although these scripts can be applied to other ERT datasets, the filtering threshold values (e.g., stacking error, geometric factor, and voltage) **should not be directly copied**. Instead, they should be selected according to the characteristics of the dataset, data quality, survey conditions, and the geological setting of the study area.

---

# Workflow

## Step 1 – Raw Data Visualization

**Script**

- `Raw data plotting.py`

### Purpose

This is the first script that should be executed.

It visualizes the raw ERT measurements to assess the overall quality of the dataset before any filtering is applied.

The script plots the distribution of the principal acquisition parameters, including:

- Apparent resistivity (ρ)
- Geometric factor (k)
- Voltage (V)
- Current (I)
- Stacking error (dev)

These plots help identify unrealistic measurements (anomaly and noise) and provide the basis for selecting appropriate filtering thresholds.

---

## Step 2 – Plotting Raw Pseudosections

**Script**

- `Script for DD and MG separate pseudosection.py`

### Purpose

This script generates pseudosections for the unfiltered datasets.

The DD and MG measurements are plotted separately, allowing a visual assessment of data quality and comparison between acquisition arrays before filtering.

---

## Step 3 – Generate Multiple Filtering Scenarios

### Combined Dataset

**Script**

- `Script for 8 filters.py`

This script generates multiple filtered datasets by combining different thresholds for:

- stacking error (dev)
- geometric factor (k)
- measured voltage (V)

The following filtering scenarios are produced:

| Scenario | Threshold Combination |
|-----------|----------------------|
| f1 | dev < 5%, k < 5000, V > 0.25 mV |
| f2 | dev < 5%, k < 5000, V > 0.50 mV |
| f3 | dev < 5%, k < 10000, V > 0.25 mV |
| f4 | dev < 5%, k < 10000, V > 0.50 mV |
| f5 | dev < 1%, k < 5000, V > 0.25 mV |
| f6 | dev < 1%, k < 5000, V > 0.50 mV |
| f7 | dev < 1%, k < 10000, V > 0.25 mV |
| f8 | dev < 1%, k < 10000, V > 0.50 mV |
| f9 | dev < 1%, k < 8000, V > 0.25 mV |

---

### Individual Array Filtering

The same procedure can also be performed separately for each acquisition array.

**Scripts**

- `Script for 8 filters_DD.py`
- `Script for 4 filters_MG.py`

These scripts follow the same filtering philosophy but are specifically designed for the individual DD and MG datasets.

---

## Step 4 – L-Curve-like Analysis

After generating multiple filtering scenarios, an L-curve-like analysis is performed to identify the most suitable filtering thresholds.

### 4.1 Stacking Error Analysis

**Script**

- `L_curve_stacking_error(dev).py`

Stacking error (dev) thresholds evaluated:

- dev < 10%
- dev < 7%
- dev < 5%
- dev < 3%
- dev < 1%

Each filtered dataset is inverted using pyGIMLi.

The resulting RRMS values are plotted against the number of retained measurements. File which has least RRMS, that was selected for further investigation.

---

### 4.2 Geometric Factor Analysis

**Script**

- `L_curve_dev_k_v.py`

Geometric factor thresholds evaluated:

- k < 13,000
- k < 10,000
- k < 8,000
- k < 5,000

Again, RRMS is evaluated relative to the number of retained measurements. These are values are with dev < 5 (since this file produces least RRMS)

---

### 4.3 Voltage Analysis

**Script**

- `L_curve_dev_k.py`

Voltage thresholds evaluated:

- |V| > 0.25 mV
- |V| > 0.50 mV

The optimal filtering combination is selected by considering the complete L-curve-like analysis. These are the values with dev < 5 and k < 10,000 (since these fils produce least RRMS)

The same workflow can also be applied independently to the DD and MG datasets.

---

## Step 5 – Plotting the Final Filtered Pseudosections

Once the optimal filtering scenario has been selected from the L-curve-like analysis, the final pseudosections can be generated.

### Combined Dataset

**Script**

- `Script for f3 filtered_wendelsheim_pseudosection.py`

### Dipole-Dipole Dataset

**Script**

- `Script for f3 filtered_DD.py`

### Multi-Gradient Dataset

**Script**

- `Script for f3 filtered_MG.py`

These scripts produce the final filtered pseudosections used for interpretation and inversion.

---

# Software and Packages  Requirements

- Python
- NumPy
- Pandas
- Matplotlib
- SciPy
- PyGIMLi

---

# Notes

The workflow presented here was developed for the Wendelsheim and Pfäffingen ERT surveys. However, the scripts are applicable to other ERT datasets after adapting the input file names and selecting filtering thresholds appropriate for the survey conditions and geological setting.
