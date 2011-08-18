# -*- coding: utf-8 -*-

"""
Module implementing QgsWpsDockWidget.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtNetwork import *
from PyQt4 import QtXml
from PyQt4 import QtWebKit
from PyQt4 import QtNetwork
from qgis.core import *
from qgswpsgui import QgsWpsGui
from qgswpsdescribeprocessgui import QgsWpsDescribeProcessGui
from qgsnewhttpconnectionbasegui import QgsNewHttpConnectionBaseGui
#from QgsWpsServerThread import QgsWpsServerThread
from qgswpstools import QgsWpsTools
from qgswpsgui import QgsWpsGui

import resources_rc,  urllib

DEBUG = False

from Ui_QgsWpsDockWidget import Ui_QgsWpsDockWidget

class QgsWpsDockWidget(QDockWidget, Ui_QgsWpsDockWidget):
    """
    Class documentation goes here.
    """
    def __init__(self, iface):
        """
        Constructor
        """
        QDockWidget.__init__(self, iface.mainWindow())
        self.setupUi(self)
        self.iface = iface
        
        self.tools = QgsWpsTools(self.iface)
        
        self.theManager = QNetworkAccessManager( self )
#        QObject.connect(self.theNetwork, SIGNAL("started()"), self.setProcessStarted)          
        QObject.connect(self.theManager, SIGNAL("finished(QNetworkReply*)"), self.setProcessFinished)          
#        QObject.connect(self.theNetwork, SIGNAL("terminated()"), self.setProcessTerminated)        
#        QObject.connect(self.theNetwork, SIGNAL("serviceFinished(QString)"), self.tools.resultHandler) 
        
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
        self.dlg = QgsWpsGui(self.iface.mainWindow(),  self.tools,  flags)    
        QObject.connect(self.dlg, SIGNAL("getDescription(QString, QTreeWidgetItem)"), self.createProcessGUI)    
        QObject.connect(self.dlg, SIGNAL("newServer()"), self.newServer)    
        QObject.connect(self.dlg, SIGNAL("editServer(QString)"), self.editServer)    
        QObject.connect(self.dlg, SIGNAL("deleteServer(QString)"), self.deleteServer)        
        QObject.connect(self.dlg, SIGNAL("connectServer(QString)"), self.dlg.createCapabilitiesGUI)    
        
            
        self.doc = QtXml.QDomDocument()
        self.tmpPath = QDir.tempPath()
    

        
    
    @pyqtSignature("")
    def on_btnConnect_clicked(self):
        self.dlg.initQgsWpsGui()
        self.dlg.show()
        
        
    
    def setProcessStarted(self):
#      self.dlgProcess.lneStatus.setText("Process started and running ... ")
        groupBox = QGroupBox(self.groupBox)
        layout = QHBoxLayout()
        self.lblProcess = QLabel(groupBox)
        self.lblProcess.setText(QString(self.processIdentifier+QApplication.translate("QgsWps", " is running ...")))

        self.btnProcessCancel = QToolButton(groupBox)
        self.btnProcessCancel.setIcon(QIcon(":/plugins/wps/images/button_cancel.png") )
        self.btnProcessCancel.setMinimumWidth(30)
        self.btnProcessCancel.setMaximumWidth(30)
        layout.addWidget(self.lblProcess)
        layout.addStretch(10)
#        layout.addWidget(self.btnProcessCancel)

        self.groupBox.setLayout(layout)
        self.btnConnect.setEnabled(False)
        QObject.connect(self.btnProcessCancel,SIGNAL("clicked()"),self.terminateProcessing)
        pass


    def setProcessFinished(self,  netWorkReply):
        self.btnConnect.setEnabled(True)
        self.reply = netWorkReply
        self.resultHandler(self.reply.readAll().data())
        
        self.lblProcess.setText(QString(self.processIdentifier+QApplication.translate("QgsWps", " finished successful")))

      
    def setProcessTerminated(self):
        QMessageBox.information(None,'Status', self.processIdentifier+QApplication.translate("QgsWps", " terminated"))
        self.btnConnect.setEnabled(True)

        
    def closeDialog(self):
      self.close()
      
    def removeProcessFromWidget(self):
      pass

    def terminateProcessing( self ):
       if self.theManager != None:
         result = self.tools.getServer(self.processName)
         scheme = result["scheme"]
         path = result["path"]
         server = result["server"]
         url = QUrl(scheme+'://'+server+'/path')
         reply = self.theManager.deleteResource(QNetworkRequest(url))
         
         self.lblProcess.setText(self.processIdentifier+QApplication.translate("QgsWps", " terminated"))
         btnProcessRemove = self.btnProcessCancel
         btnProcessRemove.setText('remove')
         self.btnConnect.setEnabled(True)
         QObject.connect(btnProcessRemove,SIGNAL("clicked()"),self.removeProcessFromWidget)         
   
    def stopProcessing( self ):
       if self.theThread != None:
         self.theThread.stop()
         self.theThread = None            
         
         

    def createProcessGUI(self,name, item):
        """Create the GUI for a selected WPS process based on the DescribeProcess
           response document. Mandatory inputs are marked as red, default is black"""
        try:
          self.processIdentifier = item.text(0)
        except:
          QMessageBox.warning(None,'',QCoreApplication.translate("QgsWps",'Please select a Process'))
          return 0
    
        # Lists which store the inputs and meta information (format, occurs, ...)
        # This list is initialized every time the GUI is created
        self.complexInputComboBoxList = [] # complex input for single raster and vector maps
        self.complexInputListWidgetList = [] # complex input for multiple raster and vector maps
        self.complexInputTextBoxList = [] # complex inpt of type text/plain
        self.literalInputComboBoxList = [] # literal value list with selectable answers
        self.literalInputLineEditList = [] # literal value list with single text line input
        self.complexOutputComboBoxList = [] # list combo box
        self.inputDataTypeList = {}
        self.inputsMetaInfo = {} # dictionary for input metainfo, key is the input identifier
        self.outputsMetaInfo = {} # dictionary for output metainfo, key is the output identifier
        self.outputDataTypeList = {}
    
        self.processName = name
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
        # Recive the XML process description
        self.doc.setContent(self.tools.getServiceXML(self.processName,"DescribeProcess",self.processIdentifier), True)     
        DataInputs = self.doc.elementsByTagName("Input")
        DataOutputs = self.doc.elementsByTagName("Output")
    
        # Create the layouts and the scroll area
        self.dlgProcess = QgsWpsDescribeProcessGui(self.dlg, flags)
        self.dlgProcessLayout = QGridLayout()
        # Two tabs, one for the process inputs and one for the documentation
        # TODO: add a tab for literal outputs
        self.dlgProcessTab = QTabWidget()
        self.dlgProcessTabFrame = QFrame()
        self.dlgProcessTabFrameLayout = QGridLayout()
        # The process description can be very long, so we make it scrollable
        self.dlgProcessScrollArea = QScrollArea(self.dlgProcessTab)
    
        self.dlgProcessScrollAreaWidget = QFrame()
        self.dlgProcessScrollAreaWidgetLayout = QGridLayout()
    
        # First part of the gui is a short overview about the process
        identifier, title, abstract = self.tools.getIdentifierTitleAbstractFromElement(self.doc)
        self.addIntroduction(identifier, title)
        
        # If no Input Data  are requested
        if DataInputs.size()==0:
          self.defineProcess()
          return 0
      
        # Generate the input GUI buttons and widgets
        self.generateProcessInputsGUI(DataInputs)
        # Generate the editable outpt widgets, you can set the output to none if it is not requested
        self.generateProcessOutputsGUI(DataOutputs)
        
        self.dlgProcessScrollAreaWidgetLayout.setSpacing(10)
        self.dlgProcessScrollAreaWidget.setLayout(self.dlgProcessScrollAreaWidgetLayout)
        self.dlgProcessScrollArea.setWidget(self.dlgProcessScrollAreaWidget)
        self.dlgProcessScrollArea.setWidgetResizable(True)
    
        self.dlgProcessTabFrameLayout.addWidget(self.dlgProcessScrollArea)
    
        self.addOkCancelButtons(self.dlgProcess,  self.dlgProcessTabFrameLayout)
        
        self.dlgProcessTabFrame.setLayout(self.dlgProcessTabFrameLayout)
        self.dlgProcessTab.addTab(self.dlgProcessTabFrame, "Process")
    
        self.tools.addDocumentationTab(self.dlgProcessTab,  abstract)
    
        self.dlgProcessLayout.addWidget(self.dlgProcessTab)
        self.dlgProcess.setLayout(self.dlgProcessLayout)
        self.dlgProcess.setGeometry(QRect(190,100,800,600))
        self.dlgProcess.show()
        
    def generateProcessInputsGUI(self, DataInputs):
        """Generate the GUI for all Inputs defined in the process description XML file"""
    
        # Create the complex inputs at first
        for i in range(DataInputs.size()):
          f_element = DataInputs.at(i).toElement()
    
          inputIdentifier, title, abstract = self.tools.getIdentifierTitleAbstractFromElement(f_element)
    
          complexData = f_element.elementsByTagName("ComplexData")
          minOccurs = int(f_element.attribute("minOccurs"))
          maxOccurs = int(f_element.attribute("maxOccurs"))
    
          # Iterate over all complex inputs and add combo boxes, text boxes or list widgets 
          if complexData.size() > 0:
            # Das i-te ComplexData Objekt auswerten
            complexDataTypeElement = complexData.at(0).toElement()
            complexDataFormat = self.tools.getDefaultMimeType(complexDataTypeElement)
            supportedComplexDataFormat = self.tools.getSupportedMimeTypes(complexDataTypeElement)
    
            # Store the input formats
            self.inputsMetaInfo[inputIdentifier] = supportedComplexDataFormat
            self.inputDataTypeList[inputIdentifier] = complexDataFormat
    
            # Attach the selected vector or raster maps
            if self.tools.isMimeTypeVector(complexDataFormat["MimeType"]) != None:
              # Vector inputs
              layerNamesList = self.tools.getLayerNameList(0)
              if maxOccurs == 1:
                self.complexInputComboBoxList.append(self.tools.addComplexInputComboBox(title, inputIdentifier, str(complexDataFormat), layerNamesList, minOccurs,  self.dlgProcessScrollAreaWidget,  self.dlgProcessScrollAreaWidgetLayout))
              else:
                self.complexInputListWidgetList.append(self.tools.addComplexInputListWidget(title, inputIdentifier, str(complexDataFormat), layerNamesList, minOccurs,  self.dlgProcessScrollAreaWidget,  self.dlgProcessScrollAreaWidgetLayout))
            elif self.tools.isMimeTypeText(complexDataFormat["MimeType"]) != None:
              # Text inputs
              self.complexInputTextBoxList.append(self.tools.addComplexInputTextBox(title, inputIdentifier, minOccurs,  self.dlgProcessScrollAreaWidget,  self.dlgProcessScrollAreaWidgetLayout))
            elif self.tools.isMimeTypeRaster(complexDataFormat["MimeType"]) != None:
              # Raster inputs
              layerNamesList = self.getLayerNameList(1)
              if maxOccurs == 1:
                self.complexInputComboBoxList.append(self.tools.addComplexInputComboBox(title, inputIdentifier, str(complexDataFormat), layerNamesList, minOccurs,  self.dlgProcessScrollAreaWidget,  self.dlgProcessScrollAreaWidgetLayout))
              else:
                self.complexInputListWidgetList.append(self.tools.addComplexInputListWidget(title, inputIdentifier, str(complexDataFormat), layerNamesList, minOccurs,  self.dlgProcessScrollAreaWidget,  self.dlgProcessScrollAreaWidgetLayout))
            else:
              # We assume text inputs in case of an unknown mime type
              self.complexInputTextBoxList.append(self.tools.addComplexInputTextBox(title, inputIdentifier, minOccurs,  self.dlgProcessScrollAreaWidget,  self.dlgProcessScrollAreaWidgetLayout))            
    
        # Create the literal inputs as second
        for i in range(DataInputs.size()):
          f_element = DataInputs.at(i).toElement()
    
          inputIdentifier, title, abstract = self.tools.getIdentifierTitleAbstractFromElement(f_element)
    
          literalData = f_element.elementsByTagName("LiteralData")
          minOccurs = int(f_element.attribute("minOccurs"))
          maxOccurs = int(f_element.attribute("maxOccurs"))
    
          if literalData.size() > 0:
            allowedValuesElement = literalData.at(0).toElement()
            aValues = allowedValuesElement.elementsByTagNameNS("http://www.opengis.net/ows/1.1","AllowedValues")
            dValue = str(allowedValuesElement.elementsByTagName("DefaultValue").at(0).toElement().text())
    #        print "Checking allowed values " + str(aValues.size())
            if aValues.size() > 0:
              valList = self.tools.allowedValues(aValues)
              if len(valList) > 0:
                if len(valList[0]) > 0:
                  self.literalInputComboBoxList.append(self.tools.addLiteralComboBox(title, inputIdentifier, valList, minOccurs,  self.dlgProcessScrollAreaWidget,  self.dlgProcessScrollAreaWidgetLayout))
                else:
                  self.literalInputLineEditList.append(self.tools.addLiteralLineEdit(title, inputIdentifier, minOccurs,  self.dlgProcessScrollAreaWidget,  self.dlgProcessScrollAreaWidgetLayout, str(valList)))
            else:
              self.literalInputLineEditList.append(self.tools.addLiteralLineEdit(title, inputIdentifier, minOccurs,  self.dlgProcessScrollAreaWidget,  self.dlgProcessScrollAreaWidgetLayout, dValue))
    
        # At last, create the bounding box inputs
        for i in range(DataInputs.size()):
          f_element = DataInputs.at(i).toElement()
    
          inputIdentifier, title, abstract = self.tools.getIdentifierTitleAbstractFromElement(f_element)
          
          bBoxData = f_element.elementsByTagName("BoundingBoxData")
          minOccurs = int(f_element.attribute("minOccurs"))
          maxOccurs = int(f_element.attribute("maxOccurs"))
    
          if bBoxData.size() > 0:
            crsListe = []
            bBoxElement = bBoxData.at(0).toElement()
            defaultCrsElement = bBoxElement.elementsByTagName("Default").at(0).toElement()
            defaultCrs = defaultCrsElement.elementsByTagName("CRS").at(0).toElement().attributeNS("http://www.w3.org/1999/xlink", "href")
            crsListe.append(defaultCrs)
            self.addLiteralLineEdit(title+"(minx,miny,maxx,maxy)", inputIdentifier, minOccurs,  self.dlgProcessScrollAreaWidget,  self.dlgProcessScrollAreaWidgetLayout)
    
            supportedCrsElements = bBoxElement.elementsByTagName("Supported")
    
            for i in range(supportedCrsElements.size()):
              crsListe.append(supportedCrsElements.at(i).toElement().elementsByTagName("CRS").at(0).toElement().attributeNS("http://www.w3.org/1999/xlink", "href"))
    
            self.literalInputComboBoxList.append(self.addLiteralComboBox("Supported CRS", inputIdentifier,crsListe, minOccurs))
    
    
        self.tools.addCheckBox(QCoreApplication.translate("QgsWps","Process selected objects only"), QCoreApplication.translate("QgsWps","Selected"),  self.dlgProcessScrollAreaWidget,  self.dlgProcessScrollAreaWidgetLayout)
        
  ##############################################################################

    def generateProcessOutputsGUI(self, DataOutputs):
        """Generate the GUI for all complex ouputs defined in the process description XML file"""
    
        if DataOutputs.size() < 1:
            return
    
        groupbox = QGroupBox(self.dlgProcessScrollAreaWidget)
        groupbox.setTitle("Complex output(s)")
        layout = QVBoxLayout()
    
        # Add all complex outputs
        for i in range(DataOutputs.size()):
          f_element = DataOutputs.at(i).toElement()
    
          outputIdentifier, title, abstract = self.tools.getIdentifierTitleAbstractFromElement(f_element)
          complexOutput = f_element.elementsByTagName("ComplexOutput")
    
          # Iterate over all complex inputs and add combo boxes, text boxes or list widgets 
          if complexOutput.size() > 0:
            # Das i-te ComplexData Objekt auswerten
            complexOutputTypeElement = complexOutput.at(0).toElement()
            complexOutputFormat = self.tools.getDefaultMimeType(complexOutputTypeElement)
            supportedcomplexOutputFormat = self.tools.getSupportedMimeTypes(complexOutputTypeElement)
    
            # Store the input formats
            self.outputsMetaInfo[outputIdentifier] = supportedcomplexOutputFormat
            self.outputDataTypeList[outputIdentifier] = complexOutputFormat
            
            widget, comboBox = self.tools.addComplexOutputComboBox(groupbox, outputIdentifier, title, str(complexOutputFormat),  self.processIdentifier)
            self.complexOutputComboBoxList.append(comboBox)
            layout.addWidget(widget)
        
        # Set the layout
        groupbox.setLayout(layout)
        # Add the outputs
        self.dlgProcessScrollAreaWidgetLayout.addWidget(groupbox)
        
        
        
  ##############################################################################

    def addIntroduction(self,  name, title):

      groupbox = QGroupBox(self.dlgProcessScrollAreaWidget)
      groupbox.setTitle(name)
      layout = QVBoxLayout()

      myLabel = QLabel(groupbox)
      myLabel.setObjectName("qLabel"+name)
      myLabel.setText(QString(title))
      myLabel.setMinimumWidth(600)
      myLabel.setMinimumHeight(25)
      myLabel.setWordWrap(True)

      layout.addWidget(myLabel)

      groupbox.setLayout(layout)

      self.dlgProcessScrollAreaWidgetLayout.addWidget(groupbox)
      
  ##############################################################################
        

          ##############################################################################  
    def defineProcess(self):
        """Create the execute request"""
        self.doc.setContent(self.tools.getServiceXML(self.processName,"DescribeProcess",self.processIdentifier))
        dataInputs = self.doc.elementsByTagName("Input")
        dataOutputs = self.doc.elementsByTagName("Output")
    
        QApplication.setOverrideCursor(Qt.WaitCursor)
        result = self.tools.getServer(self.processName)
        scheme = result["scheme"]
        path = result["path"]
        server = result["server"]
    
        checkBoxes = self.dlgProcess.findChildren(QCheckBox)
    
        if len(checkBoxes) > 0:
          useSelected = checkBoxes[0].isChecked()
    
        postString = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        postString += "<wps:Execute service=\"WPS\" version=\""+ self.tools.getServiceVersion() + "\"" + \
                       " xmlns:wps=\"http://www.opengis.net/wps/1.0.0\"" + \
                       " xmlns:ows=\"http://www.opengis.net/ows/1.1\"" +\
                       " xmlns:xlink=\"http://www.w3.org/1999/xlink\"" +\
                       " xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""\
                       " xsi:schemaLocation=\"http://www.opengis.net/wps/1.0.0" +\
                       " http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd\">"
                       
        postString += "<ows:Identifier>"+self.processIdentifier+"</ows:Identifier>\n"
        postString += "<wps:DataInputs>"
    
        # text/plain inputs ########################################################
        for textBox in self.complexInputTextBoxList:
          # Do not add undefined inputs
          if textBox == None or str(textBox.document().toPlainText()) == "":
            continue
    
          postString += self.tools.xmlExecuteRequestInputStart(textBox.objectName())
          postString += "<wps:ComplexData>" + textBox.document().toPlainText() + "</wps:ComplexData>\n"
          postString += self.tools.xmlExecuteRequestInputEnd()
    
    
        # Single raster and vector inputs ##########################################
        for comboBox in self.complexInputComboBoxList:
          # Do not add undefined inputs
          if comboBox == None or unicode(comboBox.currentText(), 'latin1') == "<None>":
            continue
               
          postString += self.tools.xmlExecuteRequestInputStart(comboBox.objectName())
    
          # TODO: Check for more types
          mimeType = self.inputDataTypeList[comboBox.objectName()]["MimeType"]
          schema = self.inputDataTypeList[comboBox.objectName()]["Schema"]
          encoding = self.inputDataTypeList[comboBox.objectName()]["Encoding"]
          self.myLayer = self.tools.getVLayer(comboBox.currentText())
          
          if self.tools.isMimeTypeVector(mimeType) != None and mimeType == "text/xml":
            postString += "<wps:ComplexData mimeType=\"" + mimeType + "\" schema=\"" + schema + "\" enconding=\"" + encoding + "\">"
            postString += self.tools.createTmpGML(comboBox.currentText(), useSelected).replace("> <","><")
            postString = postString.replace("xsi:schemaLocation=\"http://ogr.maptools.org/ qt_temp.xsd\"", "xsi:schemaLocation=\"http://schemas.opengis.net/gml/3.1.1/base/ gml.xsd\"")
          elif self.tools.isMimeTypeVector(mimeType) != None or self.tools.isMimeTypeRaster(mimeType) != None:
            postString += "<wps:ComplexData mimeType=\"" + mimeType + "\" encoding=\"base64\">\n"
            postString += self.tools.createTmpBase64(comboBox.currentText())
    
          postString += "</wps:ComplexData>\n"
          postString += self.tools.xmlExecuteRequestInputEnd()
    
        # Multiple raster and vector inputs ########################################
        for listWidgets in self.complexInputListWidgetList:
          # Do not add undefined inputs
          if listWidgets == None:
            continue
            
          mimeType = self.inputDataTypeList[listWidgets.objectName()]["MimeType"]
          schema = self.inputDataTypeList[listWidgets.objectName()]["Schema"]
          encoding = self.inputDataTypeList[listWidgets.objectName()]["Encoding"]
          
          # Iterate over each seletced item
          for i in range(listWidgets.count()):
            listWidget = listWidgets.item(i)
            if listWidget == None or listWidget.isSelected() == False or str(listWidget.text()) == "<None>":
              continue
              
            postString += self.tools.xmlExecuteRequestInputStart(listWidgets.objectName())
    
            # TODO: Check for more types
            if self.tools.isMimeTypeVector(mimeType) != None and mimeType == "text/xml":
              postString += "<wps:ComplexData mimeType=\"" + mimeType + "\" schema=\"" + schema + "\" enconding=\"" + encoding + "\">"
    #          postString += self.createTmpGML(listWidget.text(), useSelected).replace("> <","><").replace("http://ogr.maptools.org/ qt_temp.xsd","http://ogr.maptools.org/qt_temp.xsd")
              postString += self.tools.createTmpGML(listWidget.text(), useSelected).replace("> <","><")
            elif self.tools.isMimeTypeVector(mimeType) != None or self.tools.isMimeTypeRaster(mimeType) != None:
              postString += "<wps:ComplexData mimeType=\"" + mimeType + "\" encoding=\"base64\">\n"
              postString += self.tools.createTmpBase64(listWidget.text())
    
            postString += "</wps:ComplexData>\n"
            postString += self.tools.xmlExecuteRequestInputEnd()
    
        # Literal data as combo box choice #########################################
        for comboBox in self.literalInputComboBoxList:
          if comboBox == None or comboBox.currentText() == "":
              continue
    
          postString += self.tools.xmlExecuteRequestInputStart(comboBox.objectName())
          postString += "<wps:LiteralData>"+comboBox.currentText()+"</wps:LiteralData>\n"
          postString += self.tools.xmlExecuteRequestInputEnd()
    
       # Literal data as combo box choice #########################################
        for lineEdit in self.literalInputLineEditList:
          if lineEdit == None or lineEdit.text() == "":
              continue
    
          postString += self.tools.xmlExecuteRequestInputStart(lineEdit.objectName())
          postString += "<wps:LiteralData>"+lineEdit.text()+"</wps:LiteralData>\n"
          postString += self.tools.xmlExecuteRequestInputEnd()
    
        postString += "</wps:DataInputs>\n"
        
        # Attach only defined outputs
        if dataOutputs.size() > 0 and len(self.complexOutputComboBoxList) > 0:
          postString += "<wps:ResponseForm>\n"
          # The server should store the result. No lineage should be returned or status
          postString += "<wps:ResponseDocument lineage=\"false\" storeExecuteResponse=\"true\" status=\"false\">\n"
    
          # Attach ALL literal outputs #############################################
          for i in range(dataOutputs.size()):
            f_element = dataOutputs.at(i).toElement()
            outputIdentifier = f_element.elementsByTagName("ows:Identifier").at(0).toElement().text().simplified()
            literalOutputType = f_element.elementsByTagName("LiteralOutput")
    
            # Complex data is always requested as reference
            if literalOutputType.size() != 0:
              postString += "<wps:Output>\n"
              postString += "<ows:Identifier>"+outputIdentifier+"</ows:Identifier>\n"
              postString += "</wps:Output>\n"
    
          # Attach selected complex outputs ########################################
          for comboBox in self.complexOutputComboBoxList:
            # Do not add undefined outputs
            if comboBox == None or str(comboBox.currentText()) == "<None>":
              continue
            outputIdentifier = comboBox.objectName()
            
            mimeType = self.outputDataTypeList[outputIdentifier]["MimeType"]
            schema = self.outputDataTypeList[outputIdentifier]["Schema"]
            encoding = self.outputDataTypeList[outputIdentifier]["Encoding"]
            
            postString += "<wps:Output asReference=\"true\" mimeType=\"" + mimeType + "\" schema=\"" + schema + "\">"
            postString += "<ows:Identifier>" + outputIdentifier + "</ows:Identifier>\n"
            postString += "</wps:Output>\n"
    
          postString += "</wps:ResponseDocument>\n"
          postString  += "</wps:ResponseForm>\n"
          
        postString += "</wps:Execute>\n"
    
        # This is for debug purpose only
        if DEBUG == True:
    #        self.popUpMessageBox("Execute request", postString)
            # Write the request into a file
            outFile = open('/tmp/qwps_execute_request.xml', 'w')
            outFile.write(postString)
            outFile.close()
    
        QApplication.restoreOverrideCursor()
        QApplication .setOverrideCursor(Qt.ArrowCursor)
        
        self.postBuffer = QBuffer()
        self.postBuffer.open(QBuffer.ReadWrite)
        self.postBuffer.write(QByteArray.fromRawData(postString))
        self.postBuffer.close()
        self.setProcessStarted()
        url = str(scheme)+"://"+str(server)+""+str(path)
        result = self.theManager.put(QNetworkRequest(QUrl(url)),  self.postBuffer )

  ##############################################################################

    def addOkCancelButtons(self,  dlgProcess,  dlgProcessTabFrameLayout):

        groupBox = QFrame()
        layout = QHBoxLayout()
    
        btnOk = QPushButton(groupBox)
        btnOk.setText(QString(QApplication.translate("QgsWps", "Run")))
        btnOk.setMinimumWidth(100)
        btnOk.setMaximumWidth(100)
    
        btnCancel = QPushButton(groupBox)
        btnCancel.setText(QApplication.translate("QgsWps", "Back"))
        btnCancel.setMinimumWidth(100)
        btnCancel.setMaximumWidth(100)
    
        layout.addStretch(10)
        layout.addWidget(btnCancel)
        layout.addWidget(btnOk)
        
        groupBox.setLayout(layout)
        dlgProcessTabFrameLayout.addWidget(groupBox)
        
        QObject.connect(btnOk,SIGNAL("clicked()"), self.defineProcess)
        QObject.connect(btnCancel,SIGNAL("clicked()"), self.dlgProcess.close)            
        
    def resultHandler(self, resultXML,  resultType="store"):
        """Handle the result of the WPS Execute request and add the outputs as new
           map layers to the regestry or open an information window to show literal
           outputs."""
           
# This is for debug purpose only
        if DEBUG == True:
            self.popUpMessageBox("Result XML", resultXML)
            # Write the response into a file
            outFile = open('/tmp/qwps_execute_response.xml', 'w')
            outFile.write(resultXML)
            outFile.close()
            
        self.doc.setContent(resultXML,  True)
        resultNodeList = self.doc.elementsByTagNameNS("http://www.opengis.net/wps/1.0.0","Output")
        
        # TODO: Check if the process does not run correctly before
        if resultNodeList.size() > 0:
            for i in range(resultNodeList.size()):
              f_element = resultNodeList.at(i).toElement()
    
              # Fetch the referenced complex data
              if f_element.elementsByTagNameNS("http://www.opengis.net/wps/1.0.0", "Reference").size() > 0:
                identifier = f_element.elementsByTagNameNS("http://www.opengis.net/ows/1.1","Identifier").at(0).toElement().text().simplified()
                reference = f_element.elementsByTagNameNS("http://www.opengis.net/wps/1.0.0","Reference").at(0).toElement()
    
                # Get the reference
                fileLink = reference.attribute("href", "0")
    
                # Try with namespace if not successful
                if fileLink == '0':
                  fileLink = reference.attributeNS("http://www.w3.org/1999/xlink", "href", "0")
                if fileLink == '0':
                  QMessageBox.warning(None, '', str(QApplication.translate("QgsWps", "WPS Error: Unable to download the result of reference: ")) + str(fileLink))
                  return
    
                # Get the mime type of the result
                mimeType = str(reference.attribute("mimeType", "0").toLower())
    
                if fileLink != '0':                            
                  # Set a valid layerName
                  layerName = self.tools.uniqueLayerName(self.processIdentifier + "_" + identifier)
                  # The layername is normally defined in the comboBox
                  for comboBox in self.complexOutputComboBoxList:
                    if comboBox.objectName() == identifier:
                      layerName = comboBox.currentText()
    
                  resultFileConnector = urllib.urlretrieve(unicode(fileLink,'latin1'))
                  resultFile = resultFileConnector[0]
                  # Vector data 
                  # TODO: Check for schema GML and KML
                  if self.tools.isMimeTypeVector(mimeType) != None:
                    vlayer = QgsVectorLayer(resultFile, layerName, "ogr")
                    vlayer.setCrs(self.myLayer.dataProvider().crs())
                    QgsMapLayerRegistry.instance().addMapLayer(vlayer)
                  # Raster data
                  elif self.tools.isMimeTypeRaster(mimeType) != None:
                    # We can directly attach the new layer
                    rLayer = QgsRasterLayer(resultFile, layerName)
                    QgsMapLayerRegistry.instance().addMapLayer(rLayer)
                  # Text data
                  elif self.tools.isMimeTypeText(mimeType) != None:
                    #TODO: this should be handled in a separate diaqgswps.pylog to save the text output as file'
                    QApplication.restoreOverrideCursor()
                    text = open(resultFile, 'r').read()
                    # TODO: This should be a text dialog with safe option
                    self.popUpMessageBox(QCoreApplication.translate("QgsWps",'Process result (text/plain)'),text)
                  # Everything else
                  else:
                    # For unsupported mime types we assume text
                    QApplication.restoreOverrideCursor()
                    content = open(resultFile, 'r').read()
                    # TODO: This should have a safe option
                    self.popUpMessageBox(QCoreApplication.translate("QgsWps", 'Process result (unsupported mime type)'), content)
                    
              elif f_element.elementsByTagNameNS("http://www.opengis.net/wps/1.0.0", "LiteralData").size() > 0:
                QApplication.restoreOverrideCursor()
                literalText = f_element.elementsByTagNameNS("http://www.opengis.net/wps/1.0.0", "LiteralData").at(0).toElement().text()
                self.popUpMessageBox(QCoreApplication.translate("QgsWps",'Result'),literalText)
              else:
                QMessageBox.warning(None, '', str(QApplication.translate("QgsWps", "WPS Error: Missing reference or literal data in response")))
        else:
            print "Error"
            self.errorHandler(resultXML)
    
        pass
        
 ##############################################################################

    def errorHandler(self, resultXML):
         errorDoc = QtXml.QDomDocument()
         errorDoc = self.doc

         myResult = errorDoc.setContent(resultXML.strip(), True)
         resultExceptionNodeList = errorDoc.elementsByTagNameNS("http://www.opengis.net/wps/1.0.0","ExceptionReport")
         exceptionText = ''
         if not resultExceptionNodeList.isEmpty():
           for i in range(resultExceptionNodeList.size()):
             resultElement = resultExceptionNodeList.at(i).toElement()
             exceptionText += resultElement.text()
    
         resultExceptionNodeList = errorDoc.elementsByTagNameNS("http://www.opengis.net/wps/1.0.0","ExceptionText")
         if not resultExceptionNodeList.isEmpty():
           for i in range(resultExceptionNodeList.size()):
             resultElement = resultExceptionNodeList.at(i).toElement()
             exceptionText += resultElement.text()
      
         resultExceptionNodeList = errorDoc.elementsByTagNameNS("http://www.opengis.net/ows/1.1","ExceptionText")
         if not resultExceptionNodeList.isEmpty():
           for i in range(resultExceptionNodeList.size()):
             resultElement = resultExceptionNodeList.at(i).toElement()
             exceptionText += resultElement.text()
    
         resultExceptionNodeList = errorDoc.elementsByTagName("Exception")
         if not resultExceptionNodeList.isEmpty():
           resultElement = resultExceptionNodeList.at(0).toElement()
           exceptionText += resultElement.attribute("exceptionCode")
    
         if len(exceptionText) > 0:
             print resultXML
             QMessageBox.about(None, '', resultXML)
    #         self.popUpMessageBox("WPS Error", resultXML)
             pass
    


##############################################################################

    def deleteServer(self,  name):
        settings = QSettings()
        settings.beginGroup("WPS")
        settings.remove(name)
        settings.endGroup()
        self.dlg.initQgsWpsGui() 

  ##############################################################################   
 

  ##############################################################################

    def editServer(self, name):
        info = self.tools.getServer(name)
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
        dlgEdit = QgsNewHttpConnectionBaseGui(self.dlg,  flags)  
        dlgEdit.txtName.setText(name)
        dlgEdit.txtUrl.setText(info["scheme"]+"://"+info["server"]+info["path"])
        dlgEdit.show()
        self.dlg.initQgsWpsGui()     
    


  ##############################################################################

    
  ##############################################################################

    def newServer(self):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
        dlgNew = QgsNewHttpConnectionBaseGui(self.dlg,  flags)  
        dlgNew.show()
        self.dlg.initQgsWpsGui()