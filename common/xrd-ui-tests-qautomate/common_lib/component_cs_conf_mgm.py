# -*- coding: utf-8 -*-
import glob
import os

from variables import strings
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from common_lib import Common_lib
from pagemodel.cs_conf_mgm_external import Cs_conf_mgm_external
from pagemodel.cs_conf_mgm import Cs_conf_mgm
from pagemodel.cs_conf_mgm_internal_new_key import Cs_conf_mgm_internal_new_key
from pagemodel.cs_conf_mgm_enter_pin import Cs_conf_mgm_enter_pin
from pagemodel.cs_conf_mgm_delete_confirm_dlg import Cs_conf_mgm_delete_confirm_dlg
from pagemodel.cs_conf_mgm_activate_confirm_dlg import Cs_conf_mgm_activate_confirm_dlg
from common_lib_ssh import Common_lib_ssh
from component_common import Component_common
from pagemodel.upload_configuration_part import Upload_configuration_part

class Component_cs_conf_mgm(CommonUtils):
    """
    Components common to central server conf management view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_lib = Common_lib()
    cs_conf_mgm_external = Cs_conf_mgm_external()
    cs_conf_mgm = Cs_conf_mgm()
    cs_conf_mgm_internal_new_key = Cs_conf_mgm_internal_new_key()
    cs_conf_mgm_enter_pin = Cs_conf_mgm_enter_pin()
    cs_conf_mgm_delete_confirm_dlg = Cs_conf_mgm_delete_confirm_dlg()
    cs_conf_mgm_activate_confirm_dlg = Cs_conf_mgm_activate_confirm_dlg()
    common_lib_ssh = Common_lib_ssh()
    component_common = Component_common()
    upload_configuration_part = Upload_configuration_part()

    def download_source_anchor_from_cs(self):
        """
        Donwload source anchor from central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_download_source_anchor`
        """
        self.cs_conf_mgm.click_button_id_download_source_anchor()

    def generate_new_internal_config_key_in_cs(self):
        """
        Generate new internal configuration key in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_generate_signing_key`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm_internal_new_key.Cs_conf_mgm_internal_new_key.click_button_ok`
        """
        # Generate config key
        self.cs_conf_mgm.click_button_id_generate_signing_key()
        self.cs_conf_mgm_internal_new_key.click_button_ok()

        # Step Verify config generation audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.generate_internal_config_signing_key)

    def generate_new_external_config_key_in_cs(self):
        """
        Generate new external configuration key in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_link_external_configuration`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm_external.Cs_conf_mgm_external.click_button_id_generate_signing_key`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm_internal_new_key.Cs_conf_mgm_internal_new_key.click_button_ok`
        """
        self.cs_conf_mgm.click_link_external_configuration()
        self.cs_conf_mgm_external.click_button_id_generate_signing_key()
        self.cs_conf_mgm_internal_new_key.click_button_ok()

    def try_insert_pin_code(self, section=u'cs_url'):
        """
        Try inserting pin code to token in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm_enter_pin.Cs_conf_mgm_enter_pin.input_text_to_id_activate_token_pin`, *TESTDATA[section]*
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm_enter_pin.Cs_conf_mgm_enter_pin.click_button_ok`
        """
        # Sometimes it will not ask pin code, recovery added
        try:
            self.cs_conf_mgm_enter_pin.input_text_to_id_activate_token_pin(TESTDATA[section])
            self.cs_conf_mgm_enter_pin.click_button_ok()
        except:
            print("Pin code query not prompted this time")
        sleep(2)

    def log_in_to_software_token(self, section=u'cs_url'):
        """
        Login to token in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_login`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_ok_pin_login_button`
        """
        # Step Login to software token
        self.cs_conf_mgm.click_element_login()
        self.try_insert_pin_code(section)
        self.cs_conf_mgm.click_element_ok_pin_login_button()

        # Step Verify log in token audit log audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.login_token)

    def log_in_to_software_token_invalid_pin(self, section=u'invalid_cs_url'):
        """
        Login to token in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_login`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_ok_pin_login_button`
        """
        # Step Login to software token
        self.cs_conf_mgm.click_element_login()
        self.try_insert_pin_code(section)
        self.cs_conf_mgm.click_element_ok_pin_login_button()

        # Step Verify log in token invalid pin audit log audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.login_token_failed)
        self.component_common.verify_notice_message(message=strings.login_software_token_invalid_pin)

        # Step Close login dialog
        self.cs_conf_mgm_enter_pin.close_dialog()

    def log_in_to_software_token_empty_pin(self, section=u'invalid_cs_url'):
        """
        Login to token in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_login`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_ok_pin_login_button`
        """
        # Step Login to software token
        self.cs_conf_mgm.click_element_login()
        self.try_insert_pin_code(section)
        self.cs_conf_mgm.click_element_ok_pin_login_button()

        # Step Verify log in token invalid pin audit log audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.login_token_failed)
        self.component_common.verify_notice_message(message=strings.login_software_token_missing_pin)

        # Step Close login dialog
        self.cs_conf_mgm_enter_pin.close_dialog()

    def verify_external_configuration_view(self):
        """
        Verify external configuration view

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_link_external_configuration`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_hash_value_is_visible`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_date_time_is_visible`
                * **Step 4:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_download_url_contains`, *"/externalconf"*
                * **Step 5:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_signing_keys`
                * **Step 6:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_conf_parts`
        """
        self.cs_conf_mgm.click_link_external_configuration()
        sleep(1)
        self.cs_conf_mgm.verify_hash_value_is_visible()
        self.cs_conf_mgm.verify_date_time_is_visible()
        self.cs_conf_mgm.verify_download_url_contains("/externalconf")
        self.cs_conf_mgm.verify_signing_keys()
        self.cs_conf_mgm.verify_conf_parts()

    def verify_internal_configuration_view(self):
        """
        Verify internal configuration view

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_link_internal_configuration`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_hash_value_is_visible`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_date_time_is_visible`
                * **Step 4:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_download_url_contains`, *"/internalconf"*
                * **Step 5:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_signing_keys`
                * **Step 6:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_conf_parts`
        """
        self.cs_conf_mgm.click_link_internal_configuration()
        sleep(1)
        self.cs_conf_mgm.verify_hash_value_is_visible()
        self.cs_conf_mgm.verify_date_time_is_visible()
        self.cs_conf_mgm.verify_download_url_contains("/internalconf")
        self.cs_conf_mgm.verify_signing_keys()
        self.cs_conf_mgm.verify_conf_parts()

    def recreate_source_anchor_from_cs(self):
        """
        Recreate source anchor from central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_generate_source_anchor`
        """
        # Step Generate source anchor
        self.cs_conf_mgm.click_button_id_generate_source_anchor()
        # Step Verify notice message
        self.component_common.verify_notice_message(message=strings.internal_conf_anchor_generated_success)
        # Step Verify audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.recreate_internal_configuration_anchor)

    def logout_software_token(self):
        """
        Logout signing key

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_logout`
        """
        # Step
        self.cs_conf_mgm.click_button_logout()
        # Step Verify log out token audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.logout_token)

    def activate_newest_signing_key(self):
        """
        Activate newest signing key

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_newest_signing_key`
            * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_activate_signing_key`
            * **Step 3:** :func:`~pagemodel.cs_conf_mgm_activate_confirm_dlg.Cs_conf_mgm_activate_confirm_dlg.click_confirm`
        """
        self.cs_conf_mgm.click_newest_signing_key()
        self.cs_conf_mgm.click_button_id_activate_signing_key()
        self.cs_conf_mgm_activate_confirm_dlg.click_confirm()

    def activate_oldest_signing_key(self):
        """
        Activate oldest signing key

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_oldest_signing_key`
            * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_activate_signing_key`
            * **Step 3:** :func:`~pagemodel.cs_conf_mgm_activate_confirm_dlg.Cs_conf_mgm_activate_confirm_dlg.click_confirm`
        """
        self.cs_conf_mgm.click_oldest_signing_key()
        self.cs_conf_mgm.click_button_id_activate_signing_key()
        self.cs_conf_mgm_activate_confirm_dlg.click_confirm()

    def delete_newest_signing_key(self):
        """
        Delete newest signing key

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_newest_signing_key`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_delete_signing_key`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm_delete_confirm_dlg.Cs_conf_mgm_delete_confirm_dlg.click_confirm`
        """
        self.cs_conf_mgm.click_newest_signing_key()
        self.cs_conf_mgm.click_button_id_delete_signing_key()
        self.cs_conf_mgm_delete_confirm_dlg.click_confirm()

    def generate_conf_part_file(self, part_file="test.ini", identifier="FOO", file_name="foo.xml", val_program=""):
        """
        Generate configuration file
        """
        configuration_part_path = os.path.join(strings.configuration_parts_directory, part_file)
        init_content =  "content-identifier = {} \n".format(identifier)
        init_content += "file-name = {} \n".format(file_name)
        if val_program:
            init_content += "validation-program = {}".format(val_program)
        self.common_lib_ssh.generate_and_write_to_file_as_xroad("cs_url", configuration_part_path, init_content)
        self.reload_page()
        self.wait_until_jquery_ajax_loaded()

    def delete_conf_part_file(self, part_file):
        """
        Delete configuration part file
        """
        configuration_part_path = os.path.join(strings.configuration_parts_directory, part_file)
        self.common_lib_ssh.delete_file("cs_url", configuration_part_path)

    def download_configuration_part_file(self, identifier):
        """
        Donwload configuration part file
        """
        self.cs_conf_mgm.click_element_from_table_conf_parts(identifier)
        self.cs_conf_mgm.click_download()

        download_path = os.path.join(TESTDATA[u'paths'][u'downloads_folder'], '*.xml')
        downloaded_xml_file = glob.glob(download_path)
        newest_file = max(downloaded_xml_file, key=os.path.getctime)
        print newest_file
        return newest_file

    def upload_configuration_part_file(self, identifier="FOO", path="downloads"):
        """
        Upload configuration part file
        """
        self.cs_conf_mgm.click_element_from_table_conf_parts(identifier)
        self.cs_conf_mgm.click_conf_upload()
        self.upload_configuration_part.click_browse()
        self.common_lib.type_file_name_pyautogui(path)
        self.upload_configuration_part.click_ok()
        self.component_common.verify_notice_message(strings.configuration_file_upload.format(identifier))
        self.common_lib_ssh.verify_audit_log(u'cs_url', strings.configuration_part_upload_audit_log)

    def upload_conf_part_validation_fail(self, identifier="FOO", path="downloads"):
        """
        Upload configuration part file with fail
        """
        self.cs_conf_mgm.click_element_from_table_conf_parts(identifier)
        self.cs_conf_mgm.click_conf_upload()
        self.upload_configuration_part.click_browse()
        self.common_lib.type_file_name_pyautogui(path)
        self.upload_configuration_part.click_ok()
        # Has to sleep for
        sleep(3)
        self.component_common.verify_notice_message(strings.configuration_file_upload_validation_fail.format(identifier))
        self.common_lib_ssh.verify_audit_log(u'cs_url', strings.failed_configuration_part_upload_audit_log)
        self.upload_configuration_part.click_close()
