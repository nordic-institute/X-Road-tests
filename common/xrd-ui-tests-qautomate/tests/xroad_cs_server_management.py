# -*- coding: utf-8 -*-
from webframework.extension.base.setupTest import SetupTest
from webframework.extension.util.common_utils import *
from time import sleep
from pagemodel.open_application import Open_application

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
        pass

    def tearDown(self):
        """
        Method that runs after every test case
        """
        pass

    def test_change_the_graphical_user_interface_language(self):
        """
        Test case for changeing the graphical user interface language

        **Use cases:**
            * `2.5`_: Change the Graphical User Interface Language
        """
        pass

    def test_view_the_installed_software_version(self):
        """
        Test case for viewing the installed software version

        **Use cases:**
            * `2.6`_: View the Installed Software Version
        """
        pass

    def test_view_the_list_of_configuration_backup_files(self):
        """
        Test case for viewing the list of configuration backup files

        **Use cases:**
            * `2.7`_: View the List of Configuration Backup Files
        """
        pass

    def test_back_up_configuration(self):
        """
        Test case for backing up configuration

        **Use cases:**
            * `2.8`_: Back Up Configuration
        """
        pass

    def test_restore_configuration_from_a_backup_file(self):
        """
        Test case for restoring configuration from a backup file

        **Use cases:**
            * `2.9`_: Restore Configuration from a Backup File
        """
        pass

    def test_download_a_backup_file(self):
        """
        Test case for downloading a backup file

        **Use cases:**
            * `2.10`_: Download a Backup File
        """
        pass

    def test_delete_a_backup_file(self):
        """
        Test case for deleting a backup file

        **Use cases:**
            * `2.11`_: Delete a Backup File
        """
        pass

    def test_upload_a_backup_file(self):
        """
        Test case for uploading a backup file

        **Use cases:**
            * `2.12`_: Upload a Backup File
        """
        pass
