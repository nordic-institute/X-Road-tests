# -*- coding: utf-8 -*-
import os
from variables import flags
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.parsers.parameter_parser import get_all_parameters
from time import sleep
from common_lib import Common_lib
from pagemodel.cs_backup_restore_dlg_restore_confirm import Cs_backup_restore_dlg_restore_confirm
from pagemodel.cs_backup_restore_dlg_delete_confirm import Cs_backup_restore_dlg_delete_confirm
from pagemodel.cs_backup_restore import Cs_backup_restore
from pagemodel.cs_backup_restore_dlg_back_up_config import Cs_backup_restore_dlg_back_up_config
from pagemodel.cs_backup_restore_dlg_upload_backup import Cs_backup_restore_dlg_upload_backup

class Component_cs_backup(CommonUtils):
    """
    Components common to central server backup view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_lib = Common_lib()
    cs_backup_restore_dlg_restore_confirm = Cs_backup_restore_dlg_restore_confirm()
    cs_backup_restore_dlg_delete_confirm = Cs_backup_restore_dlg_delete_confirm()
    cs_backup_restore = Cs_backup_restore()
    cs_backup_restore_dlg_back_up_config = Cs_backup_restore_dlg_back_up_config()
    cs_backup_restore_dlg_upload_backup = Cs_backup_restore_dlg_upload_backup()

    def __init__(self):
        """
        Initilization method for moving test data to class

        *Updated: 11.07.2017*

        :param parameters:  Test data section dictionary
        """
        CommonUtils.__init__(self)

    def generate_backup(self):
        """
        Generate backup in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_button_id_backup`
                * **Step 2:** :func:`~pagemodel.cs_backup_restore_dlg_back_up_config.Cs_backup_restore_dlg_back_up_config.click_button_ok`
        """
        ## Generate backup
        self.cs_backup_restore.click_button_id_backup()
        self.cs_backup_restore_dlg_back_up_config.click_button_ok()
        flags.set_testdata_flag(flags.restore_backup, True)

    def restore_backup(self):
        """
        Restore backup in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_newest_restore`
                * **Step 2:** :func:`~pagemodel.cs_backup_restore_dlg_restore_confirm.Cs_backup_restore_dlg_restore_confirm.click_button_ui_buttonset_confirm`
                * **Step 3:** :func:`~pagemodel.cs_backup_restore_dlg_back_up_config.Cs_backup_restore_dlg_back_up_config.click_button_ok`
                * **Step 4:** :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_newest_delete`
                * **Step 5:** :func:`~pagemodel.cs_backup_restore_dlg_delete_confirm.Cs_backup_restore_dlg_delete_confirm.click_button_ui_buttonset_confirm`
        """
        ## Restore back up
        self.cs_backup_restore.click_element_newest_restore()
        self.cs_backup_restore_dlg_restore_confirm.click_button_ui_buttonset_confirm()
        self.cs_backup_restore_dlg_back_up_config.click_button_ok()
        flags.set_testdata_flag(flags.restore_backup, False)

    def download_backup(self):
        self.cs_backup_restore.click_element_newest_download()

    def delete_backup(self):
        self.cs_backup_restore.click_element_newest_delete()
        self.cs_backup_restore_dlg_delete_confirm.click_button_ui_buttonset_confirm()

    def upload_backup(self):
        self.cs_backup_restore.click_element_upload_backup_file()
        self.cs_backup_restore_dlg_upload_backup.click_element_upload_button()
        download_folder = TESTDATA.get_parameter(u'paths', u'downloads_folder')
        backup_file = TESTDATA.get_parameter(u'paths', u'backup_file')
        backup_file_path = os.path.join(download_folder, backup_file)
        self.common_lib.type_file_name_pyautogui(backup_file_path)
        self.cs_backup_restore_dlg_upload_backup.click_dialog_confirm()
        self.wait_until_jquery_ajax_loaded()
