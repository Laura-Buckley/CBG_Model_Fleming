"""
Created 23/10/2024 for new revision of Basal Ganglia network model

Description: This class will handle the loading and assignment of the extracellular potential values,
computed from specific FEA models of the DBS electrode and head model.


"""

import numpy as np
from collections import defaultdict
from pathlib import Path


def sort_data_by_yz(filename):
    """
    Reads a data file, processes it to group voltage values by (y, z),
    and sorts each group by the x-coordinate.

    Args:
        filename: Name of the file to read.

    Returns:
        dict: Mapping of (y, z) to sorted lists of (x, voltage).
              Returns None if an error occurs.
    """
    coupled_dir = Path("network_structure")
    coupled_script = coupled_dir / filename

    # Check if the file exists
    if not coupled_script.exists():
        print(f"Error: File '{coupled_script}' does not exist.")
        return None

    # Load the data
    try:
        data = np.genfromtxt(coupled_script, skip_header=9)
    except Exception as e:
        print(f"Error reading the file '{coupled_script}': {e}")
        return None

    # Validate the data structure
    if data.ndim != 2 or data.shape[1] < 4:
        print(f"Error: Data format is incorrect. Shape: {data.shape}. Expected at least 4 columns.")
        return None

    # Handle NaN values
    nan_count = np.isnan(data).sum()
    if nan_count > 0:
        print(f"Warning: Found {nan_count} NaN values. These will be ignored.")
        data = data[~np.isnan(data).any(axis=1)]

    if data.size == 0:
        print("Error: No valid data after removing NaNs.")
        return None

    # Extract x, y, z, and voltage values
    x_values = data[:, 0]
    y_values = data[:, 1]
    z_values = data[:, 2]
    voltage_values = data[:, 3]

    # Group data by (y, z)
    grouped_data = defaultdict(list)
    for x, y, z, v in zip(x_values, y_values, z_values, voltage_values):
        grouped_data[(y, z)].append((x, v))

    # Sort each group by x-coordinate
    sorted_data = {
        key: sorted(value, key=lambda item: item[0])  # Sort by x
        for key, value in grouped_data.items()
    }

    # Debug: Check if grouped data is empty
    if not sorted_data:
        print("Warning: Grouped data is empty. Check input file for valid data.")
        return None

    return sorted_data


def scale_collateral_rx_by_voltage(cortical_population, voltage_data):
    """
    Scale the collateral_rx values of each cell in the cortical population based on voltage data.

    Args:
        cortical_population: List or iterable of cortical cells, each with `position` and `collateral` attributes.
        voltage_data: Dictionary mapping (y, z) -> list of voltage values ordered by x-coordinates.

    Returns:
        None: Updates the `xtra.rx` values of each collateral segment in place.
    """
    if voltage_data is None:
        print("Error: voltage_data is None. Ensure sort_data_by_yz returned valid data.")
        return

    for cell in cortical_population:
        x, y = cell.position[0], cell.position[1]
        xy_key = (x, y)

        if xy_key not in voltage_data:
            print(f"Warning: No voltage data found for cell at x={x}, y={y}. Skipping.")
            continue

        voltage_values = voltage_data[xy_key]

        if len(voltage_values) != len(cell.collateral):
            print(
                f"Warning: Mismatch in voltage data length ({len(voltage_values)}) and "
                f"collateral segments ({len(cell.collateral)}) for cell at x={x}, y={y}."
            )
            continue

        for seg_idx, seg in enumerate(cell.collateral):
            try:
                seg.xtra.rx *= voltage_values[seg_idx]
            except Exception as e:
                print(
                    f"Error: Failed to scale rx for cell at x={x}, y={y}, segment {seg_idx}. "
                    f"Error: {e}"
                )





