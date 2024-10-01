# -*- coding: utf-8 -*-
"""
Created on Wed April 03 14:27:26 2019

Description: Functions for calculating cell distances to electrode. Distance is
             calculated similar to space.distance, but distance is now between
             a cell position and a point for an electrode rather than between
             two cell positions

Edits:
    10-01-18: Created electrode_distance function

@author: John Fleming, john.fleming@ucdconnect.ie

"""

# There must be some Python package out there that provides most of this stuff.
# Distance computations are provided by scipy.spatial, but scipy is a fairly
# heavy dependency.

import numpy as np
import logging

logger = logging.getLogger("PyNN")


def distance_to_electrode(src_electrode, tgt_cell, mask=None):
    """
    Return the Euclidian distance from a point source electrode to a cell.
    `mask` allows only certain dimensions to be considered, e.g.::
            * to ignore the z-dimension, use `mask=array([0,1])`
            * to ignore y, `mask=array([0,2])`
            * to just consider z-distance, `mask=array([2])`
    'src_electrode' is the electrode positon in xyz co-ordinates.
    'tgt_cell' is the cell that the distance will be calculated to.
    """
    d = src_electrode - tgt_cell.position

    if mask is not None:
        d = d[mask]
    return np.sqrt(np.dot(d, d))


def distances_to_electrode(src_electrode, tgt_pop, coordinate_mask=None):
    """
    Return an array of the Euclidian distances from a point source
    electrode to a population of cells.
    `coordinate_mask` allows only certain dimensions to be considered, e.g.::
            * to ignore the z-dimension, use `coordinate_mask=array([0,1])`
            * to ignore y, `coordinate_mask=array([0,2])`
            * to just consider z-distance, `coordinate_mask=array([2])`
    'src_electrode' is the electrode positon in xyz co-ordinates.
    'tgt_pop' is the target population of cells.
    """

    cell_electrode_distances = np.zeros((tgt_pop.local_size, 1))
    cell_electrode_distances.flatten()

    for ii, tgt_cell in enumerate(tgt_pop):
        cell_electrode_distances[ii] = distance_to_electrode(
            src_electrode, tgt_cell, mask=coordinate_mask
        )

    return cell_electrode_distances

def Interneuron_distances_to_electrode(src_electrode, tgt_pop, coordinate_mask=None):
    """
    Return an array of the Euclidian distances from a point source
    electrode to a population of cells.
    `coordinate_mask` allows only certain dimensions to be considered, e.g.::
            * to ignore the z-dimension, use `coordinate_mask=array([0,1])`
            * to ignore y, `coordinate_mask=array([0,2])`
            * to just consider z-distance, `coordinate_mask=array([2])`
    'src_electrode' is the electrode positon in xyz co-ordinates.
    'tgt_pop' is the target population of cells.
    """

    cell_electrode_distances = np.zeros((tgt_pop.local_size, 1))
    cell_electrode_distances.flatten()

    for ii, tgt_cell in enumerate(tgt_pop):
        cell_electrode_distances[ii] = distance_to_electrode(
            src_electrode, tgt_cell,
        )

    return cell_electrode_distances


def collateral_distances_to_electrode(src_electrode, tgt_pop, L, nseg):
    """
    Return an nd-array of the Euclidian distances from a point source
    electrode to a population of cells. Each row corresponds to a collateral
    from the cortical population. Each column corresponds to the segments of
    the collateral, with 0 being the furthest segment from the 2d plane the
    cells are distributed in and 1 being in the plane.
    'src_electrode' is the electrode positon in xyz co-ordinates.
    'tgt_pop' is the target population of cells.
    'L' is the length of the cortical collateral
    'nseg' is the number of segments in a collateral
    'segment_electrode_distances' is the distance from the centre of each
    collateral segment to the stimulating electrode. Each row corresponds to
    a collateral of a single cortical cell. Each column corresponds to a
    segment of the collateral.
    """
    segment_electrode_distances = np.zeros((tgt_pop.local_size, nseg))

    segment_centres = np.arange(0, nseg + 3 - 1) * (1 / nseg)
    segment_centres = segment_centres - (1 / (2 * nseg))
    segment_centres[0] = 0
    segment_centres[-1] = 1
    segment_centres = segment_centres[1 : len(segment_centres) - 1]

    z_coordinate = L * segment_centres - L / 2
    # print(z_coordinate)

    for ii, tgt_cell in enumerate(tgt_pop):
        for seg in np.arange(nseg):
            tgt_cell.position = np.array(
                [tgt_cell.position[0], tgt_cell.position[1], z_coordinate[seg]]
            )
            segment_electrode_distances[ii][seg] = distance_to_electrode(
                src_electrode, tgt_cell
            )

    return segment_electrode_distances

def axon_distances_to_electrode(src_electrode, tgt_pop, node_L, myelin_L, ais_L, soma_L,myelin_L_0,
                                num_axon_compartments, ais_nseg, soma_nseg):
    """
        Return an nd-array of the Euclidian distances from a point source
        electrode to a population of cells. Each row corresponds to an axon
        from the cortical population. Each column corresponds to the segments
        of the nodes in the axon, with 0 being the furthest node from the 2d
        plane the cells are distributed in.
        'src_electrode' is the electrode positon in xyz co-ordinates.
        'tgt_pop' is the target population of cells.
        'node_L' is the length of the Nodes of Ranvier in each cortical cell.
        'myelin_L' is the length of the myelin compartments in each cortical cell.
        'num_axon_compartments' is the number of Nodes of Ranvier per cortical cell.
        'nseg' is the number of segments in each Node of Ranvier.
        'segment_electrode_distances' is the distance from the centre of each
         segment to the stimulating electrode. Each row corresponds to an
        axon of a single cortical cell. Each column corresponds to a segment.
        """

    #initialise array for storage of electrode distances for each segment for every compartment
    segment_electrode_distances_nodes = np.zeros((tgt_pop.local_size, num_axon_compartments))

    Y_coords_nodes = np.zeros(num_axon_compartments)
    for n in np.arange(num_axon_compartments):
        Y_coords_nodes[n] = (num_axon_compartments-1-n)*(node_L+myelin_L) + (node_L*0.5)

    for ii, tgt_cell in enumerate(tgt_pop):
        for n in np.arange(num_axon_compartments):
            tgt_cell.position = np.array(
                [tgt_cell.position[0], (tgt_cell.position[1] + Y_coords_nodes[n]),
                 tgt_cell.position[2]]
            )
            segment_electrode_distances_nodes[ii][n] = distance_to_electrode(
                src_electrode, tgt_cell
            )

    axon_L = Y_coords_nodes[0] + node_L + myelin_L_0

    # initialise array for storage of electrode distances for each segment for every compartment
    segment_electrode_distances_ais = np.zeros((tgt_pop.local_size, ais_nseg))

    segment_centres_ais = np.arange(0, ais_nseg + 3 - 1) * (1 / ais_nseg)
    segment_centres_ais = segment_centres_ais - (1 / (2 * ais_nseg))
    segment_centres_ais[0] = 0
    segment_centres_ais[-1] = 1
    segment_centres_ais = segment_centres_ais[1: len(segment_centres_ais) - 1]

    Y_coords_ais = ais_L*segment_centres_ais

    for ii, tgt_cell in enumerate(tgt_pop):
        for seg in np.arange(ais_nseg):
            tgt_cell.position = np.array(
                [tgt_cell.position[0], (Y_coords_ais[seg] + axon_L), tgt_cell.position[2]]
            )
            segment_electrode_distances_ais[ii][seg] = distance_to_electrode(
                src_electrode, tgt_cell
            )

        # initialise array for storage of electrode distances for each segment for every compartment
        segment_electrode_distances_soma = np.zeros((tgt_pop.local_size, soma_nseg))

        segment_centres_soma = np.arange(0, soma_nseg + 3 - 1) * (1 / soma_nseg)
        segment_centres_soma = segment_centres_soma - (1 / (2 * soma_nseg))
        segment_centres_soma[0] = 0
        segment_centres_soma[-1] = 1
        segment_centres_soma = segment_centres_soma[1: len(segment_centres_soma) - 1]

        Y_coords_soma = soma_L * segment_centres_soma
        total_L = axon_L + ais_L
        for ii, tgt_cell in enumerate(tgt_pop):
            for seg in np.arange(soma_nseg):
                tgt_cell.position = np.array(
                    [tgt_cell.position[0], (Y_coords_soma[seg] + total_L), tgt_cell.position[2]]
                )
                segment_electrode_distances_soma[ii][seg] = distance_to_electrode(
                    src_electrode, tgt_cell
                )

    return segment_electrode_distances_nodes, segment_electrode_distances_ais, segment_electrode_distances_soma

