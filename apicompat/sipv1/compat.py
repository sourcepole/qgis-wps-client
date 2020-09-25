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

def pystring(qvar):
    return str(qvar.toString()) if hasattr(qvar, 'toString') else str(qvar)

builtins.pystring = pystring
def pylist(qvar):
    return list(qvar.toList()) if hasattr(qvar, 'toList') else qvar
builtins.pylist = pylist
def pyint(qvar):
    if hasattr(qvar, 'toInt'): 
        val, ok = qvar.toInt()
        if not ok:
            raise ValueError('QVariant conversion error')
        return int(val)
    else:
        return qvar
builtins.pyint = pyint
def pyfloat(qvar):
    if hasattr(qvar, 'toFloat'): 
        val, ok = qvar.toFloat()
        if not ok:
            raise ValueError('QVariant conversion error')
        return float(val)
    else:
        return qvar
builtins.pyfloat = pyfloat
def pystringlist(qvar):
    return list([str(s) for s in qvar.toStringList()]) if hasattr(qvar, 'toStringList') else qvar
builtins.pystringlist = pystringlist
def pybytearray(qvar):
    return bytearray(qvar.toByteArray()) if hasattr(qvar, 'toByteArray') else qvar
builtins.pybytearray = pybytearray
def pyobject(qvar):
    return qvar.toPyObject() if hasattr(qvar, 'toPyObject') else qvar
builtins.pyobject = pyobject
