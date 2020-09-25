# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ApiCompat
                                 A QGIS plugin
 API compatibility layer
                              -------------------
        begin                : 2013-07-02
        copyright            : (C) 2013 by Pirmin Kalberer, Sourcepole
        email                : pka@sourcepole.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from future import standard_library
standard_library.install_aliases()
from builtins import str
from qgis.PyQt.QtCore import *
from qgis.core import *

import builtins

#Define backwards compatibility functions
def pystring(qvar):
    return str(qvar)
builtins.pystring = pystring
def pylist(qvar):
    return list(qvar)
builtins.pylist = pylist
def pyint(qvar):
    return int(qvar)
builtins.pyint = pyint
def pyfloat(qvar):
    return float(qvar)
builtins.pyfloat = pyfloat
def pystringlist(qvar):
    return list(qvar)
builtins.pystringlist = pystringlist
def pybytearray(qvar):
    return bytearray(qvar)
builtins.pybytearray = pybytearray
def pyobject(qvar):
    return qvar
builtins.pyobject = pyobject
