# -*- coding: utf-8 -*-
from QAutoLibrary.extension import TESTDATA
from selenium.webdriver.common.by import By
from QAutoLibrary.QAutoSelenium import *
from time import sleep
from pagemodel.ss_version import Ss_version

class Component_cs_version(CommonUtils):
    ss_version = Ss_version()

    def verify_version(self, text=u'Central Server version 6'):
        """
        Verify version view contains right version

        :param text:  String value for text
        """
        self.ss_version.verify_version_text(text)
        print("Version text contains '{}'".format(text))
