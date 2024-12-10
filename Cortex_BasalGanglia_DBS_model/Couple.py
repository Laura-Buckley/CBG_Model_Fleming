"""
Created 23/10/2024 for new revision of Basal Ganglia network model

Description: This class will handle the loading and assignment of the extracellular potential values,
computed from specific FEA models of the DBS electrode and head model.


"""

import numpy as np
import os
from collections import defaultdict
from pathlib import Path

def sort_data_by_yz(filename):
    coupled_dir = Path("coupled_models")
    coupled_script = coupled_dir / filename

    # Load the data, ignoring lines starting with '%' and skipping the header
    try:
        data = np.genfromtxt(coupled_script, skip_header=9)
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

    # Check if data is valid and handle NaNs
    if data.ndim != 2 or data.shape[1] < 4:
        print("Data format is incorrect. Expected at least 4 columns.")
        return None
    nan_count = np.isnan(data).sum()
    if nan_count > 0:
        print(f"Found {nan_count} NaN values, which will be ignored.")
        data = data[~np.isnan(data).any(axis=1)]

    # Extract x, y, z, and voltage values- from COMSOL coordinates convention- a y-z plane
    x_values = data[:, 0]
    y_values = data[:, 1]
    z_values = data[:, 2]
    voltage_values = data[:, 3]

    # Group data by (y, z) according to 2D plane of collaterals
    grouped_data = defaultdict(list)
    for x, y, z, v in zip(x_values, y_values, z_values, voltage_values):
        grouped_data[(y, z)].append((x, v))

    # Sort each group by x- the coordinate along the collateral length
    sorted_data = {
        key: sorted(value, key=lambda item: item[0])  # Sort by x-coordinate
        for key, value in grouped_data.items()
    }

    return sorted_data


def scale_collateral_rx_by_voltage(cortical_population, voltage_data):
    """
    Scale the collateral_rx values of each cell in the cortical population based on the voltage data.

    Args:
        cortical_population: List or iterable of cortical cells, each with `position` and `collateral` attributes.
                             - `position`: 3-element list/array [x, y, z]
                             - `collateral`: Iterable of segments with `xtra.rx` attributes
        voltage_data: Dictionary mapping (y, z) -> list of voltage values ordered by x-coordinates.

    Returns:
        None: Updates the `xtra.rx` values of each collateral segment in place.
    """
    for cell in cortical_population:
        # Extract the x and y position of the cell (2D plane in network is x-y plane)
        x, y = cell.position[0], cell.position[1]
        xy_key = (x, y)

        if xy_key not in voltage_data:
            print(f"No voltage data found for x={x}, y={y}. Skipping cell.")
            continue

        # Get the ordered voltage values for this (x, y) pair
        voltage_values = voltage_data[xy_key]

        # Scale rx for each segment in the collateral
        for seg_idx, seg in enumerate(cell.collateral):
            seg.xtra.rx *= voltage_values[seg_idx]

