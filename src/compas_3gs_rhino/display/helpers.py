from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import compas
import compas_rhino

from compas.utilities import i_to_rgb
from compas.utilities import i_to_green
from compas.utilities import i_to_red
from compas.utilities import i_to_blue

from compas.geometry import distance_point_point
from compas.geometry import midpoint_point_point
from compas.geometry import centroid_points
from compas.geometry import project_points_plane
from compas.geometry import bestfit_plane
from compas.geometry import scale_vector
from compas.geometry import add_vectors

from compas_rhino.utilities import xdraw_lines
from compas_rhino.utilities import xdraw_points
from compas_rhino.utilities import xdraw_labels
from compas_rhino.utilities import xdraw_faces

try:
    import rhinoscriptsyntax as rs
    import scriptcontext as sc
except ImportError:
    compas.raise_if_ironpython()


__author__     = ['Juney Lee']
__copyright__  = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'juney.lee@arch.ethz.ch'


__all__ = ['get_index_colordict',
           'get_value_colordict',
           'get_force_color']


def get_index_colordict(key_list):
    color_dict = {}
    if key_list:
        for index, key in enumerate(key_list):
            if len(key_list) == 1:
                value = 1
            else:
                value  = float(index) / (len(key_list) - 1)
            color  = i_to_rgb(value)
            color_dict[key] = color
    return color_dict


def get_value_colordict(value_dict):
    """From value_dict to color_dict.
    """
    color_dict = {}
    ub = max(value_dict.values())
    for key in value_dict:
        color = i_to_rgb(value_dict[key] / ub)
        color_dict[key] = color
    return color_dict


def get_force_color(volmesh, network):
    """Determines whether an edge of the form diagram is in compression (blue)or tension (red).
    """
    colors = {}
    for u, v in network.edges():
        u_hfkey, v_hfkey = volmesh.cell_pair_hfkeys(u, v)
        face_normal   = volmesh.halfface_normal(u_hfkey)
        edge_vector   = network.edge_vector(u, v)
        dot = dot_vectors(face_normal, edge_vector)
        if dot < 0:
            value = (0, 0, 255)
        else:
            value = (255, 0, 0)
        colors[(u, v)] = value
    return colors