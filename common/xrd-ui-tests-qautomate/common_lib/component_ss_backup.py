# -*- coding: utf-8 -*-
from QAutoLibrary.extension import TESTDATA
from selenium.webdriver.common.by import By
from QAutoLibrary.QAutoSelenium import *
from time import sleep
from pagemodel.ss_backup_restore import Ss_backup_restore
from pagemodel.ss_backup_restore_back_up_config import Ss_backup_restore_back_up_config
from pagemodel.ss_backup_restore_confirm_delete import Ss_backup_restore_confirm_delete
from pagemodel.ss_backup_restore_confirm_restore import Ss_backup_restore_confirm_restore

class Component_ss_backup(CommonUtils):
    """
    Components common to security server backup view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    ss_backup_restore = Ss_backup_restore()
    ss_backup_restore_back_up_config = Ss_backup_restore_back_up_config()
    ss_backup_restore_confirm_delete = Ss_backup_restore_confirm_delete()
    ss_backup_restore_confirm_restore = Ss_backup_restore_confirm_restore()

    def generate_backup(self):
        """
        Generate backup

        """
        self.ss_backup_restore.click_button_id_backup()
        self.ss_backup_restore_back_up_config.click_button_ok()

    def restore_backup(self):
        """
        Restore backup

        """
        self.ss_backup_restore.click_element_first_row_restore()
        self.ss_backup_restore_confirm_restore.click_button_confirm()
        self.ss_backup_restore_back_up_config.click_button_ok()
        self.ss_backup_restore.click_element_first_row_delete()
        self.ss_backup_restore_confirm_delete.click_button_confirm()
