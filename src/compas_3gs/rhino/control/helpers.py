from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

try:
    import rhinoscriptsyntax as rs
    import scriptcontext as sc
    import Rhino
except ImportError:
    compas.raise_if_ironpython()


__all__ = [
    'get_initial_point',
    'get_target_point'
]


def get_initial_point(message='Point to move from?'):
    ip = Rhino.Input.Custom.GetPoint()
    ip.SetCommandPrompt(message)
    ip.Get()
    ip = ip.Point()
    return ip


def get_target_point(constraint, OnDynamicDraw, option='None', message='Point to move to?'):
    gp = Rhino.Input.Custom.GetPoint()
    gp.SetCommandPrompt(message)
    if option == 'None':
        gp.Constrain(constraint)
    if option != 'None':
        gp.Constrain(constraint, option)
    gp.DynamicDraw += OnDynamicDraw
    gp.Get()
    gp = gp.Point()
    return gp
