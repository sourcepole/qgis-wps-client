# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QgsWpsAbout.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlgAbout(object):
    def setupUi(self, dlgAbout):
        dlgAbout.setObjectName("dlgAbout")
        dlgAbout.resize(686, 477)
        self.gridLayout = QtWidgets.QGridLayout(dlgAbout)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(dlgAbout)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setMaximumSize(QtCore.QSize(180, 16777215))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblVersion = QtWidgets.QLabel(self.widget)
        self.lblVersion.setMaximumSize(QtCore.QSize(16777215, 14))
        self.lblVersion.setObjectName("lblVersion")
        self.verticalLayout.addWidget(self.lblVersion)
        self.lblDate = QtWidgets.QLabel(self.widget)
        self.lblDate.setMaximumSize(QtCore.QSize(16777215, 14))
        self.lblDate.setObjectName("lblDate")
        self.verticalLayout.addWidget(self.lblDate)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(dlgAbout)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.memAbout = QtWidgets.QTextEdit(self.tab)
        self.memAbout.setUndoRedoEnabled(False)
        self.memAbout.setReadOnly(True)
        self.memAbout.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.memAbout.setObjectName("memAbout")
        self.gridLayout_2.addWidget(self.memAbout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.memContrib = QtWidgets.QTextEdit(self.tab_3)
        self.memContrib.setUndoRedoEnabled(False)
        self.memContrib.setReadOnly(True)
        self.memContrib.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.memContrib.setObjectName("memContrib")
        self.gridLayout_3.addWidget(self.memContrib, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.memSponsoring = QtWidgets.QTextEdit(self.tab_4)
        self.memSponsoring.setUndoRedoEnabled(False)
        self.memSponsoring.setReadOnly(True)
        self.memSponsoring.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.memSponsoring.setObjectName("memSponsoring")
        self.gridLayout_5.addWidget(self.memSponsoring, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.memAcknowl = QtWidgets.QTextEdit(self.tab_2)
        self.memAcknowl.setUndoRedoEnabled(False)
        self.memAcknowl.setReadOnly(True)
        self.memAcknowl.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.memAcknowl.setObjectName("memAcknowl")
        self.gridLayout_4.addWidget(self.memAcknowl, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)

        self.retranslateUi(dlgAbout)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(dlgAbout.accept)
        self.buttonBox.rejected.connect(dlgAbout.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgAbout)

    def retranslateUi(self, dlgAbout):
        _translate = QtCore.QCoreApplication.translate
        dlgAbout.setWindowTitle(_translate("dlgAbout", "About QgsWPS"))
        self.lblVersion.setText(_translate("dlgAbout", "Version:"))
        self.lblDate.setText(_translate("dlgAbout", "Date:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("dlgAbout", "About QgsWPS"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("dlgAbout", "Contributors"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("dlgAbout", "Sponsors"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("dlgAbout", "License"))
