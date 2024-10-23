"""
Created 23/10/2024 for new revision of Basal Ganglia network model

Description: This class will handle the loading and assignment of the extracellular potential values,
computed from specific FEA models of the DBS electrode and head model.


"""

import numpy as np
import os

def get_data_from_filename(filename):
    coupled_dir = Path("coupled_models")
    coupled_script = coupled_dir / filename
    ex_values = np.loadtxt(coupled_script, delimiter=",")
    return ex_values


def sort_ex_values(ex_values):
    """this will sort the loaded extracellular potential values into an n x d array, where n is the number of rows,
        corresponding to the number of segments in the collateral, and d is the number of cells in the Cortical pop.

    """

