# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/hdus/dev/qgis/wps-plugin/wps/qgswpsgui.ui'
#
# Created: Mon Nov  9 14:20:26 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_QgsWps(object):
    def setupUi(self, QgsWps):
        QgsWps.setObjectName(_fromUtf8("QgsWps"))
        QgsWps.setWindowModality(QtCore.Qt.NonModal)
        QgsWps.resize(780, 604)
        QgsWps.setAcceptDrops(False)
        self.gridLayout = QtGui.QGridLayout(QgsWps)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.GroupBox1 = QtGui.QGroupBox(QgsWps)
        self.GroupBox1.setObjectName(_fromUtf8("GroupBox1"))
        self.gridlayout = QtGui.QGridLayout(self.GroupBox1)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.btnNew = QtGui.QPushButton(self.GroupBox1)
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.gridlayout.addWidget(self.btnNew, 1, 1, 1, 1)
        self.btnEdit = QtGui.QPushButton(self.GroupBox1)
        self.btnEdit.setEnabled(False)
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.gridlayout.addWidget(self.btnEdit, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(171, 30, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 1, 4, 1, 1)
        self.btnConnect = QtGui.QPushButton(self.GroupBox1)
        self.btnConnect.setEnabled(True)
        self.btnConnect.setObjectName(_fromUtf8("btnConnect"))
        self.gridlayout.addWidget(self.btnConnect, 1, 0, 1, 1)
        self.cmbConnections = QtGui.QComboBox(self.GroupBox1)
        self.cmbConnections.setObjectName(_fromUtf8("cmbConnections"))
        self.gridlayout.addWidget(self.cmbConnections, 0, 0, 1, 7)
        self.btnDelete = QtGui.QPushButton(self.GroupBox1)
        self.btnDelete.setEnabled(False)
        self.btnDelete.setObjectName(_fromUtf8("btnDelete"))
        self.gridlayout.addWidget(self.btnDelete, 1, 3, 1, 1)
        self.pushDefaultServer = QtGui.QPushButton(self.GroupBox1)
        self.pushDefaultServer.setObjectName(_fromUtf8("pushDefaultServer"))
        self.gridlayout.addWidget(self.pushDefaultServer, 1, 6, 1, 1)
        self.btnBookmarks = QtGui.QPushButton(self.GroupBox1)
        self.btnBookmarks.setObjectName(_fromUtf8("btnBookmarks"))
        self.gridlayout.addWidget(self.btnBookmarks, 1, 5, 1, 1)
        self.gridLayout.addWidget(self.GroupBox1, 0, 0, 1, 1)
        self.splitter = QtGui.QSplitter(QgsWps)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.label = QtGui.QLabel(self.splitter)
        self.label.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.lneFilter = QtGui.QLineEdit(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lneFilter.sizePolicy().hasHeightForWidth())
        self.lneFilter.setSizePolicy(sizePolicy)
        self.lneFilter.setObjectName(_fromUtf8("lneFilter"))
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)
        self.treeWidget = QtGui.QTreeWidget(QgsWps)
        self.treeWidget.setColumnCount(3)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.gridLayout.addWidget(self.treeWidget, 2, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.btnAbout = QtGui.QPushButton(QgsWps)
        self.btnAbout.setObjectName(_fromUtf8("btnAbout"))
        self.hboxlayout.addWidget(self.btnAbout)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.buttonBox = QtGui.QDialogButtonBox(QgsWps)
        self.buttonBox.setEnabled(True)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.hboxlayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.hboxlayout, 3, 0, 1, 1)

        self.retranslateUi(QgsWps)
        QtCore.QMetaObject.connectSlotsByName(QgsWps)

    def retranslateUi(self, QgsWps):
        QgsWps.setWindowTitle(_translate("QgsWps", "Note: this plugin not considered stable yet. Use it on your own risk", None))
        self.GroupBox1.setTitle(_translate("QgsWps", "Server Connections", None))
        self.btnNew.setText(_translate("QgsWps", "&New", None))
        self.btnEdit.setText(_translate("QgsWps", "Edit", None))
        self.btnConnect.setText(_translate("QgsWps", "C&onnect", None))
        self.btnDelete.setText(_translate("QgsWps", "Delete", None))
        self.pushDefaultServer.setText(_translate("QgsWps", "Add default server", None))
        self.btnBookmarks.setText(_translate("QgsWps", "Bookmarks", None))
        self.label.setText(_translate("QgsWps", "Filter:", None))
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.headerItem().setText(0, _translate("QgsWps", "Identifier", None))
        self.treeWidget.headerItem().setText(1, _translate("QgsWps", "Title", None))
        self.treeWidget.headerItem().setText(2, _translate("QgsWps", "Abstract", None))
        self.btnAbout.setText(_translate("QgsWps", "about", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    QgsWps = QtGui.QDialog()
    ui = Ui_QgsWps()
    ui.setupUi(QgsWps)
    QgsWps.show()
    sys.exit(app.exec_())

