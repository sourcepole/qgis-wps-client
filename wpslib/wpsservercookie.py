# -*- coding: utf-8 -*-
"""
 /***************************************************************************
   QGIS Web Processing Service Plugin
  -------------------------------------------------------------------
 Date                 : 01 October 2016
 Copyright            : (C) 2016 by Jing YANG
 email                : euniceyangjing@gmail.com

  ***************************************************************************
  *                                                                         *
  *   This program is free software; you can redistribute it and/or modify  *
  *   it under the terms of the GNU General Public License as published by  *
  *   the Free Software Foundation; either version 2 of the License, or     *
  *   (at your option) any later version.                                   *
  *                                                                         *
  ***************************************************************************/
"""

from PyQt4.QtCore import QSettings, QObject
from PyQt4.QtNetwork import QNetworkCookie, QNetworkRequest
from PyQt4.QtGui import QApplication,QMessageBox

class WpsServerCookie(QObject):
    def __init__(self, processUrl):
        QObject.__init__(self)
        self.server = pystring(processUrl.host())
        self.path = pystring(processUrl.path())
        self.port = pystring(processUrl.port())
        self.cookieSettings = "WPS-Cookie/" + self.server + ":" + self.port + self.path

    # if the cookie exists, delete the old one then add, otherwise add directly
    def setServerCookies(self, qt_cookies):
        if self.checkServerCookies():
            self.removeServerCookies()
        self.addServerCookies(qt_cookies)

    # remove server cookies
    def removeServerCookies(self):
        settings = QSettings()
        settings.beginGroup(self.cookieSettings)
        cookie_keys = settings.childKeys()
        if cookie_keys is not None:
            for key in cookie_keys:
                settings.remove(key)
                QMessageBox.information(None, '', "just remove the cookies of " + self.cookieSettings)
        settings.endGroup()

    # add new cookies
    def addServerCookies(self, qt_cookies):
        settings = QSettings()
        settings.beginGroup(self.cookieSettings)
        if qt_cookies is not None:
            for cookie in qt_cookies:
                if isinstance(cookie, QNetworkCookie):
                    settings.setValue(pystring(cookie.name()), pystring(cookie.value()))
                    QMessageBox.information(None, '', "just save " + pystring(cookie.name()) + ": " + pystring(cookie.value()))
                else:
                    settings.setValue(pystring(cookie[0]), pystring(cookie[1]))
        settings.endGroup()

    # get specified cookie information in setting and contain them in the header when doing http request
    def getServerCookies(self):
        cookieList = []
        settings = QSettings()
        settings.beginGroup(self.cookieSettings)
        childKeys = settings.childKeys()
        if childKeys is not None:
            for key in childKeys:
                # cookie = QNetworkCookie()
                # cookie.setName(pystring(key))
                # cookie.setValue(pystring(settings.value(key)))
                # cookies.append(cookie)
                cookieList.append(key + "=" + settings.value(key))
        settings.endGroup()
        return ";".join(cookieList)

    # check whether the coookie exist
    def checkServerCookies(self):
        settings = QSettings()
        settings.beginGroup(self.cookieSettings)
        childKeys = settings.childKeys()
        if childKeys is not None:
            for key in childKeys:
                QMessageBox.information(None, '', "the system has already saved " + pystring(key) + ": " + pystring(settings.value(key)))
        return True if childKeys is not None and len(childKeys) > 0 else False







