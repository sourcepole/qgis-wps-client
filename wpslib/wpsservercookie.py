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
        settings.endGroup()

    # add new cookies
    def addServerCookies(self, qt_cookies):
        settings = QSettings()
        settings.beginGroup(self.cookieSettings)
        for cookie in qt_cookies:
            if isinstance(cookie, QNetworkCookie):
                settings.setValue(pystring(cookie.name()), pystring(cookie.value()))
            else:
                settings.setValue(pystring(cookie[0]), pystring(cookie[1]))
        settings.endGroup()

    # get specified cookie information in setting and contain them in the header when doing http request
    def getServerCookies(self):
        cookieList = []
        settings = QSettings()
        settings.beginGroup(self.cookieSettings)
        for key in settings.childKeys():
            # cookie = QNetworkCookie()
            # cookie.setName(pystring(key))
            # cookie.setValue(pystring(settings.value(key)))
            # cookies.append(cookie)
            cookieList.append(key + "=" + settings.value(key))
        settings.endGroup()
        return cookieList

    # check whether the coookie exist
    def checkServerCookies(self):
        settings = QSettings()
        settings.beginGroup(self.cookieSettings)
        cookie_keys = settings.childKeys()
        return True if len(cookie_keys) > 0 else False

    # add cookies in the header when doing request
    def addHeaderCookies(self, request):
        if self.checkServerCookies():
            # request.setHeader(QNetworkRequest.CookieHeader, serverCookie.getServerCookies())
            request.setRawHeader("Cookie", ";".join(self.getServerCookies()))







