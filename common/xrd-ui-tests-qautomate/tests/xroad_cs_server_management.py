# -*- coding: utf-8 -*-
import os
from variables import strings, flags
from webframework import TESTDATA
from webframework.extension.base.setupTest import SetupTest
from webframework.extension.util.common_utils import *
from time import sleep
from pagemodel.open_application import Open_application
from common_lib.component_cs import Component_cs
from common_lib.common_lib import Common_lib
from common_lib.component_common import Component_common
from common_lib.common_lib_ssh import Common_lib_ssh
from common_lib.component_cs_sidebar import Component_cs_sidebar
from common_lib.component_cs_version import Component_component_cs_version
from pagemodel.cs_backup_restore import Cs_backup_restore
from common_lib.component_cs_backup import Component_cs_backup
from pagemodel.ss_login import Ss_login
from pagemodel.cs_login import Cs_login

class Xroad_cs_server_management(SetupTest):
    """
    .. _document: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md
    .. _2.5: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#25-uc-cs_04-change-the-graphical-user-interface-language
    .. _2.6: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#26-uc-cs_05-view-the-installed-software-version
    .. _2.7: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#27-uc-cs_06-view-the-list-of-configuration-backup-files
    .. _2.8: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#28-uc-cs_07-back-up-configuration
    .. _2.9: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#29-uc-cs_08-restore-configuration-from-a-backup-file
    .. _2.10: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#210-uc-cs_09-download-a-backup-file
    .. _2.11: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#211-uc-cs_10-delete-a-backup-file
    .. _2.12: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#212-uc-cs_11-upload-a-backup-file

    Xroad cases for central management test cases

    Use cases `document`_

    **Use cases:**
        * `2.5`_: Change the Graphical User Interface Language
        * `2.6`_: View the Installed Software Version
        * `2.7`_: View the List of Configuration Backup Files
        * `2.8`_: Back Up Configuration
        * `2.9`_: Restore Configuration from a Backup File
        * `2.10`_: Download a Backup File
        * `2.11`_: Delete a Backup File
        * `2.12`_: Upload a Backup File

    **Changelog:**

    * 15.05.2017
        | Test set created and cases + documentation links added
    """
    common_utils = CommonUtils()
    open_application = Open_application()
    component_cs = Component_cs()
    common_lib = Common_lib()
    component_common = Component_common()
    common_lib_ssh = Common_lib_ssh()
    component_cs_sidebar = Component_cs_sidebar()
    component_cs_version = Component_component_cs_version()
    cs_backup_restore = Cs_backup_restore()
    component_cs_backup = Component_cs_backup()
    ss_login = Ss_login()
    cs_login = Cs_login()

    @classmethod
    def setUpTestSet(self):
        """
        Method that runs before every unittest

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.autogen_browser = self.Autogen_browser = self.common_utils`
        """
        self.autogen_browser = self.common_utils.open_browser()

    @classmethod
    def tearDownTestSet(self):
        """
        Method that runs after every unittest

        **Test steps:**
                * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.close_all_browsers`
        """
        self.common_utils.close_all_browsers()

    def setUp(self):
        """
        Method that runs before every test case
        """
        self.start_log_time = self.common_lib.get_log_utc_time()
        self.common_lib_ssh.empty_all_logs_from_server("cs_url")

    def tearDown(self):
        """
        Method that runs after every test case
        """
        stop_log_time = self.common_lib.get_log_utc_time()
        if not self.is_last_test_passed():
            _, copy_log = self.get_log_file_paths()
            self.common_lib_ssh.get_all_logs_from_server(u'cs_url')
            self.common_lib_ssh.find_exception_from_logs_and_save(self.start_log_time, stop_log_time, u'cs_url', copy_log)

        # Delete all tar files from downloads
        self.common_lib.delete_files_with_extension(TESTDATA.get_parameter(u'paths', u'downloads_folder'), u'.tar')

        # Step restore backup if not restored durring run
        if flags.get_testdata_flag(flags.backup_running):
            if self.cs_login.verify_is_login_page():
                self.component_cs.login(u'cs_url', False)
            self.component_cs_backup.restore_backup()

        # Step log out if logged in
        if not self.cs_login.verify_is_login_page():
            self.common_lib.log_out()

    def test_change_the_graphical_user_interface_language(self):
        """
        Test case for changeing the graphical user interface language

        **Use cases:**
            * `2.5`_: Change the Graphical User Interface Language
        """
        # Step Open central server
        self.component_cs.login(u'cs_url', False)

        # Step Change language
        self.component_common.open_select_language_dlg()
        self.component_common.change_language_in_dlg(strings.lanquage_eng)
        self.component_common.accept_select_language_dlg()

        # Step Verify audit log for language change
        self.common_lib_ssh.verify_audit_log(u'cs_url', strings.set_ui_language)

        # Step Log out of central server
        self.common_lib.log_out()

    def test_view_the_installed_software_version(self):
        """
        Test case for viewing the installed software version

        **Use cases:**
            * `2.6`_: View the Installed Software Version
        """
        # Step login to central server
        self.component_cs.login(u'cs_url', False)

        # Step open version view
        self.component_cs_sidebar.open_version_view()

        # Step verify version
        self.component_cs_version.verify_version(u'Central Server version 6')

        # Step log out of central server
        self.common_lib.log_out()

    def test_back_up_cases(self):
        """
        Test all back up cases

        **Use cases:**
            * `2.7`_: View the List of Configuration Backup Files
            * `2.8`_: Back Up Configuration
            * `2.9`_: Restore Configuration from a Backup File
            * `2.10`_: Download a Backup File
            * `2.11`_: Delete a Backup File
            * `2.12`_: Upload a Backup File
        """
        # Step Login to central server
        self.component_cs.login(u'cs_url', False)

        # Step Open backup view
        self.component_cs_sidebar.open_backup_restore_view()

        # Step Generate backup
        self.component_cs_backup.generate_backup()

        # Step Verify backup view user actions
        self.cs_backup_restore.verify_contains_all_user_actions()

        # Step Download backup
        self.component_cs_backup.download_backup()

        # Step Restore backup
        self.component_cs_backup.restore_backup()

        # Step Upload backup
        self.component_cs_backup.upload_backup()

        # Delete all back up files
        self.component_cs_backup.delete_all_backups()

        # Step Log out of central server
        self.common_lib.log_out()
