# -*- coding: utf-8 -*-
from QAutoLibrary.extension import TESTDATA
from selenium.webdriver.common.by import By
from QAutoLibrary.QAutoSelenium import *
from time import sleep
from common_lib import Common_lib
from pagemodel.ss_initial_conf_import_anchor import Ss_initial_conf_import_anchor
from pagemodel.ss_initial_conf_import_conf_dlg import Ss_initial_conf_import_conf_dlg
from pagemodel.ss_initial_conf_server_init_dlg import Ss_initial_conf_server_init_dlg
from pagemodel.ss_initial_conf_server_details import Ss_initial_conf_server_details


class Component_ss_initial_conf(CommonUtils):
    """
    Components common to security server initial configuration view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_lib = Common_lib()
    ss_initial_conf_import_anchor = Ss_initial_conf_import_anchor()
    ss_initial_conf_import_conf_dlg = Ss_initial_conf_import_conf_dlg()
    ss_initial_conf_server_init_dlg = Ss_initial_conf_server_init_dlg()
    ss_initial_conf_server_details = Ss_initial_conf_server_details()

    def import_configuration_anchor(self, section=u'paths'):
        """
        Import configuration anchor

        :param section:  Test data section name
        """
        self.ss_initial_conf_import_anchor.wait_until_element_is_visible_initial_conf()
        self.ss_initial_conf_import_anchor.upload_anchor(TESTDATA[section])
        self.ss_initial_conf_import_conf_dlg.wait_until_element_is_visible_conf_required()
        self.ss_initial_conf_import_conf_dlg.click_button_ui_buttonset_confirm()
        self.wait_until_jquery_ajax_loaded()
        self.ss_initial_conf_server_details.wait_until_element_is_visible_security_server_owner()
        sleep(6)

    def add_initial_server_configuration_values_to_ss(self, section1=u'member_mgm_configuration', section2=u'ss1_url'):
        """
        Add initial server configuration values to security server

        :param section1:  Test data section name
        :param section2:  Test data section name
        """
        self.ss_initial_conf_server_details.fill_input_values_serverconfform(TESTDATA[section1])
        self.ss_initial_conf_server_details.fill_input_values_pincode(TESTDATA[section2])
        self.ss_initial_conf_server_details.submit_serverconfform_noname1()
        self.ss_initial_conf_server_init_dlg.wait_until_element_is_visible_id_alert()
        self.ss_initial_conf_server_init_dlg.submit_serverconfform_noname3()