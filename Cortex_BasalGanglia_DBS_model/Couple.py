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
    converts coordinates from mm to um, rounds to 2 decimal places,
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

    # Extract x, y, z, and voltage values, converting to um and rounding
    x_values = np.round(data[:, 0] * 1000, 2)
    y_values = np.round(data[:, 1] * 1000, 2)
    z_values = np.round(data[:, 2] * 1000, 2)
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


def scale_by_voltage(cortical_population, voltage_data):
    """
    Generate an array of sorted voltage values for each cell's collateral segments.
    Cells without voltage data will have all segments set to 1.0 for neutral scaling.

    Args:
        cortical_population: List or iterable of cortical cells, each with `position` attribute.
        voltage_data: Dictionary mapping (y, z) -> list of voltage values ordered by x-coordinates.

    Returns:
        np.ndarray: An array of shape (number_of_cells, number_of_segments) with voltage values.
    """
    num_cells = cortical_population.local_size
    num_segments = 11  # Assuming each collateral has 11 segments
    cell_sorted_voltage = np.ones((num_cells, num_segments))  # Initialize with 1.0 for neutral scaling
    print(f"Initialized cell_sorted_voltage: shape={cell_sorted_voltage.shape}")
    for cell_idx, cell in enumerate(cortical_population):
        print(f"Processing cell {cell_idx}...")
        print(f"voltage_data key: {cell.position[:2]}")
        # Get cell position (assumes x-y plane for matching voltage data)
        x, y = cell.position[0], cell.position[1]
        xy_key = (x, y)

        # Check if voltage data exists for this cell
        if xy_key not in voltage_data:
            print(f"Warning: No voltage data found for cell at x={x}, y={y}. Using 1.0 for scaling.")
            continue

        voltage_values = voltage_data[xy_key]

        # Ensure the number of segments matches the voltage data length
        if len(voltage_values) != num_segments:
            print(
                f"Warning: Mismatch in voltage data length ({len(voltage_values)}) and "
                f"number of segments ({num_segments}) for cell at x={x}, y={y}. Using 1.0 for scaling."
            )
            continue

        # Save voltage values for this cell
        cell_sorted_voltage[cell_idx, :] = voltage_values

    return cell_sorted_voltage






