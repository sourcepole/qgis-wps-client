from __future__ import absolute_import
from processing.gui.ToolboxAction import ToolboxAction
from processing.core.Processing import Processing
from .WpsAlgorithm import WpsAlgorithm
from wps.wpslib.processdescription import ProcessDescription
import os
from qgis.PyQt import QtGui
from PyQt4.QtCore import *

class WpsServerAction(ToolboxAction):

    def __init__(self, server):
        self.server = server
        self.processalgs = []
        self.name = "Load processes from server"
        self.group = WpsAlgorithm.groupName(server)

    def execute(self):
        self.server.capabilitiesRequestFinished.connect(self._capabilitiesRequestFinished)
        self.server.requestCapabilities()

    def _capabilitiesRequestFinished(self):
        self.processalgs = []
        self.server.parseCapabilitiesXML()
        for process in self.server.processes:
            self.processalgs.append( WpsAlgorithm(process) )
        processing.updateAlgsList()
