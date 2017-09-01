# -*- coding: utf-8 -*-
from variables import strings
from webframework.extension.base.baseTest import BaseTest
from webframework.extension.parsers.parameter_parser import get_all_parameters
from webframework.extension.util.common_utils import *
from time import sleep
from pagemodel.open_application import Open_application
from pagemodel.ss_login import Ss_login
from pagemodel.ss_sidebar import Ss_sidebar
from common_lib.common_lib import Common_lib
from pagemodel.ss_clients import Ss_clients
from pagemodel.ss_clients_dlg_services import Ss_clients_dlg_services
from pagemodel.ss_clients_dlg_services_add_wsdl import Ss_clients_dlg_services_add_wsdl
from pagemodel.ss_clients_dlg_services_acl_for_service import Ss_clients_dlg_services_acl_for_service
from pagemodel.ss_clients_dlg_services_edit_wsdl import Ss_clients_dlg_services_edit_wsdl
from pagemodel.ss_clients_services_dlg_add_subjects import Ss_clients_services_dlg_add_subjects
from pagemodel.ss_clients_services_dlg_acl_confirm import Ss_clients_services_dlg_acl_confirm
from pagemodel.ss_client_services_dlg_delete import Ss_client_services_dlg_delete
from pagemodel.cs_login import Cs_login
from pagemodel.cs_sidebar import Cs_sidebar
from pagemodel.cs_sec_servers import Cs_sec_servers
from pagemodel.cs_sec_servers_details import Cs_sec_servers_details
from pagemodel.cs_sec_servers_details_clients import Cs_sec_servers_details_clients
from pagemodel.cs_sec_servers_new_client_req import Cs_sec_servers_new_client_req
from pagemodel.cs_sec_servers_new_client_req_search import Cs_sec_servers_new_client_req_search
from pagemodel.cs_sec_servers_mgm_requests import Cs_sec_servers_mgm_requests
from pagemodel.cs_sec_serves_mgm_request_approve import Cs_sec_serves_mgm_request_approve
from pagemodel.cs_sec_servers_mgm_request_app_conf import Cs_sec_servers_mgm_request_app_conf
from pagemodel.ss_clients_add_client import Ss_clients_add_client
from pagemodel.ss_clients_add_client_conf import Ss_clients_add_client_conf
from pagemodel.ss_client_dlg_details import Ss_client_dlg_details
from pagemodel.ss_client_dlg_unregister import Ss_client_dlg_unregister
from pagemodel.ss_client_dlg_delete_unregister import Ss_client_dlg_delete_unregister
from pagemodel.cs_conf_mgm import Cs_conf_mgm
from pagemodel.cs_members import Cs_members
from pagemodel.cs_add_member_dlg import Cs_add_member_dlg
from pagemodel.cs_members_details_dlg import Cs_members_details_dlg
from pagemodel.ss_initial_conf_import_anchor import Ss_initial_conf_import_anchor
from pagemodel.ss_initial_conf_import_conf_dlg import Ss_initial_conf_import_conf_dlg
from pagemodel.ss_initial_conf_server_details import Ss_initial_conf_server_details
from pagemodel.ss_initial_conf_server_init_dlg import Ss_initial_conf_server_init_dlg
from pagemodel.cs_remove_member_dlg import Cs_remove_member_dlg
from pagemodel.ss_system_parameters import Ss_system_parameters
from pagemodel.ss_system_param_add_timestamp_dlg import Ss_system_param_add_timestamp_dlg
from pagemodel.ss_softoken_enter_pin import Ss_softoken_enter_pin
from pagemodel.ss_enter_pin_dlg import Ss_enter_pin_dlg
from pagemodel.ss_keys_and_cert import Ss_keys_and_cert
from pagemodel.cs_sec_servers_details_auth import Cs_sec_servers_details_auth
from pagemodel.cs_sec_servers_auth_dlg import Cs_sec_servers_auth_dlg
from pagemodel.cs_member_details_owned_servers import Cs_member_details_owned_servers
from pagemodel.cs_members_owned_auth_cert_reg_dlg import Cs_members_owned_auth_cert_reg_dlg
from pagemodel.cs_members_mgm_requests_dlg import Cs_members_mgm_requests_dlg
from pagemodel.ss_clients_add_warning import Ss_clients_add_warning
from pagemodel.cs_mgm_requests import Cs_mgm_requests
from pagemodel.ss_keys_and_cert_generate_csr import Ss_keys_and_cert_generate_csr
from pagemodel.ss_keys_and_cert_dlg_subject_dname import Ss_keys_and_cert_dlg_subject_dname
from pagemodel.ss_keys_cert_dlg_generate_key import Ss_keys_cert_dlg_generate_key
from pagemodel.ss_keys_and_cert_dlg_registration_req import Ss_keys_and_cert_dlg_registration_req
from pagemodel.ss_keys_and_cert_dlg_delete import Ss_keys_and_cert_dlg_delete
from pagemodel.ss_keys_and_cert_dlg_import_cert import Ss_keys_and_cert_dlg_import_cert

class Pvayla_stress_tests(BaseTest):
    """
    Stress tests

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    parameters = get_all_parameters()
    common_utils = CommonUtils()
    open_application = Open_application()
    ss_login = Ss_login()
    ss_sidebar = Ss_sidebar()
    common_lib = Common_lib()
    ss_clients = Ss_clients()
    ss_clients_dlg_services = Ss_clients_dlg_services()
    ss_clients_dlg_services_add_wsdl = Ss_clients_dlg_services_add_wsdl()
    ss_clients_dlg_services_acl_for_service = Ss_clients_dlg_services_acl_for_service()
    ss_clients_dlg_services_edit_wsdl = Ss_clients_dlg_services_edit_wsdl()
    ss_clients_services_dlg_add_subjects = Ss_clients_services_dlg_add_subjects()
    ss_clients_services_dlg_acl_confirm = Ss_clients_services_dlg_acl_confirm()
    ss_client_services_dlg_delete = Ss_client_services_dlg_delete()
    cs_login = Cs_login()
    cs_sidebar = Cs_sidebar()
    cs_sec_servers = Cs_sec_servers()
    cs_sec_servers_details = Cs_sec_servers_details()
    cs_sec_servers_details_clients = Cs_sec_servers_details_clients()
    cs_sec_servers_new_client_req = Cs_sec_servers_new_client_req()
    cs_sec_servers_new_client_req_search = Cs_sec_servers_new_client_req_search()
    cs_sec_servers_mgm_requests = Cs_sec_servers_mgm_requests()
    cs_sec_serves_mgm_request_approve = Cs_sec_serves_mgm_request_approve()
    cs_sec_servers_mgm_request_app_conf = Cs_sec_servers_mgm_request_app_conf()
    ss_clients_add_client = Ss_clients_add_client()
    ss_clients_add_client_conf = Ss_clients_add_client_conf()
    ss_client_dlg_details = Ss_client_dlg_details()
    ss_client_dlg_unregister = Ss_client_dlg_unregister()
    ss_client_dlg_delete_unregister = Ss_client_dlg_delete_unregister()
    cs_conf_mgm = Cs_conf_mgm()
    cs_members = Cs_members()
    cs_add_member_dlg = Cs_add_member_dlg()
    cs_members_details_dlg = Cs_members_details_dlg()
    ss_initial_conf_import_anchor = Ss_initial_conf_import_anchor()
    ss_initial_conf_import_conf_dlg = Ss_initial_conf_import_conf_dlg()
    ss_initial_conf_server_details = Ss_initial_conf_server_details()
    ss_initial_conf_server_init_dlg = Ss_initial_conf_server_init_dlg()
    cs_remove_member_dlg = Cs_remove_member_dlg()
    ss_system_parameters = Ss_system_parameters()
    ss_system_param_add_timestamp_dlg = Ss_system_param_add_timestamp_dlg()
    ss_softoken_enter_pin = Ss_softoken_enter_pin()
    ss_enter_pin_dlg = Ss_enter_pin_dlg()
    ss_keys_and_cert = Ss_keys_and_cert()
    cs_sec_servers_details_auth = Cs_sec_servers_details_auth()
    cs_sec_servers_auth_dlg = Cs_sec_servers_auth_dlg()
    cs_member_details_owned_servers = Cs_member_details_owned_servers()
    cs_members_owned_auth_cert_reg_dlg = Cs_members_owned_auth_cert_reg_dlg()
    cs_members_mgm_requests_dlg = Cs_members_mgm_requests_dlg()
    ss_clients_add_warning = Ss_clients_add_warning()
    cs_mgm_requests = Cs_mgm_requests()
    ss_keys_and_cert_generate_csr = Ss_keys_and_cert_generate_csr()
    ss_keys_and_cert_dlg_subject_dname = Ss_keys_and_cert_dlg_subject_dname()
    ss_keys_cert_dlg_generate_key = Ss_keys_cert_dlg_generate_key()
    ss_keys_and_cert_dlg_registration_req = Ss_keys_and_cert_dlg_registration_req()
    ss_keys_and_cert_dlg_delete = Ss_keys_and_cert_dlg_delete()
    ss_keys_and_cert_dlg_import_cert = Ss_keys_and_cert_dlg_import_cert()

    @classmethod
    def setUpTestSet(self):
        """
        Method that runs before every unittest

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~common_lib.common_lib.Common_lib.remove_cert_from_downloads`, *self.parameters[u'paths']*
                * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.add_dynamic_content_to_parameters`, *self.parameters*, *"count"*, *value*, *u'round'*
        """
        self.common_lib.remove_cert_from_downloads(self.parameters[u'paths'])
        value = 1
        self.common_utils.add_dynamic_content_to_parameters(self.parameters, "count", value, u'round')

    def setUp(self):
        """
        Method that runs before every test case

        *Updated: 11.07.2017*

        """
        pass

    def tearDown(self):
        """
        Method that runs after every test case

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        sleep(1)
        driver = self.common_utils.get_current_driver()
        if not "https://test-ss2.i.palveluvayla.com:4000/login" in driver.current_url:
            try:
                self.common_lib.log_out()
            except:
                pass

    def test_measure_request_loading(self):
        """
        Measure request loading

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: click link data name requests management #webpage: cs_sidebar**
                * :func:`~pagemodel.cs_sidebar.Cs_sidebar.click_link_data_name_requests_management`
            * **Step 2: wait until element is visible id records count #webpage: cs_mgm_requests**
                * :func:`~pagemodel.cs_mgm_requests.Cs_mgm_requests.wait_until_element_is_visible_id_records_count`
                * :func:`~webframework.extension.util.common_utils.CommonUtils.get_resource_timings`, *u'loading_req_res'*
            * **Step 3: log out #webpage: common_lib**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        self.open_application.open_application_url(self.parameters[u'cs_url'])
        self.cs_login.login_dev_cs(self.parameters[u'cs_url'])
        self.cs_sidebar.verify_central_server_title()
        # Step Click link data name requests management #Webpage: cs_sidebar
        self.cs_sidebar.click_link_data_name_requests_management()
        #self.common_utils.get_measurements(u'loading_req_navi')
        # Step Wait until element is visible id records count #Webpage: cs_mgm_requests
        self.cs_mgm_requests.wait_until_element_is_visible_id_records_count()
        self.common_utils.get_resource_timings(u'loading_req_res')
        # Step Log out #Webpage: common_lib
        sleep(2)
        self.common_lib.log_out()
        sleep(4)

    def test_measure_generating_cert_keys(self):
        """
        Measure generating cert keys

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: click keys and certificates #webpage: ss_sidebar**
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.click_keys_and_certificates`
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.verify_keys_and_cert_title`
            * **Step 2: click soft token #webpage: ss_keys_and_cert**
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_soft_token`
            * **Step 3: click generate key #webpage: ss_keys_and_cert**
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_generate_key`
            * **Step 4: generate key label #webpage: ss_keys_cert_dlg_generate_key #parameters: certificate**
                * :func:`~pagemodel.ss_keys_cert_dlg_generate_key.Ss_keys_cert_dlg_generate_key.generate_key_label`, *strings.sign_key_label*
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.wait_until_cert_req_active`
            * **Step 5: find generated key request #webpage: ss_keys_and_cert**
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_generated_key_request`, *strings.sign_key_label*
            * **Step 6: click enerate certificate request button #webpage: ss_keys_and_cert**
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_generate_certificate_request`
            * **Step 7: fill input values keys csr #webpage: ss_keys_and_cert_generate_csr #parameters: certificate**
                * :func:`~pagemodel.ss_keys_and_cert_generate_csr.Ss_keys_and_cert_generate_csr.fill_input_values_keys_csr_sign`, *u'member1_configuration'*
            * **Step 8: click button id generate csr submit #webpage: ss_keys_and_cert_generate_csr**
                * :func:`~pagemodel.ss_keys_and_cert_generate_csr.Ss_keys_and_cert_generate_csr.click_button_id_generate_csr_submit`
            * **Step 9: fill input values keys dname #webpage: ss_keys_and_cert_dlg_subject_dname #parameters: certificate**
                * :func:`~pagemodel.ss_keys_and_cert_dlg_subject_dname.Ss_keys_and_cert_dlg_subject_dname.fill_input_values_keys_dname_sign`, *self.parameters[u'member1_configuration']*
            * **Step 10: submit keys dname #webpage: ss_keys_and_cert_dlg_subject_dname**
                * :func:`~pagemodel.ss_keys_and_cert_dlg_subject_dname.Ss_keys_and_cert_dlg_subject_dname.submit_keys_dname`
                * :func:`~webframework.extension.util.common_utils.CommonUtils.get_resource_timings`, *u'generate_keys'*
            * **Step 11: click logout**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        print "Test Round: " + str(self.parameters['round']['count'])
        next_round_value = int(self.parameters['round']['count']) + 1
        self.common_utils.add_dynamic_content_to_parameters(self.parameters, "count", next_round_value, u'round')
        self.open_application.open_application_url(self.parameters[u'ss1_url'])
        # step Login security server
        self.ss_login.login(self.parameters[u'ss1_url'])
        self.ss_sidebar.verify_sidebar_title()
        # Step Click keys and certificates #Webpage: ss_sidebar
        self.ss_sidebar.click_keys_and_certificates()
        self.ss_keys_and_cert.verify_keys_and_cert_title()
        # Step Click soft token #Webpage: ss_keys_and_cert
        self.ss_keys_and_cert.click_soft_token()
        # Step Click generate key #Webpage: ss_keys_and_cert
        self.ss_keys_and_cert.click_generate_key()
        # Step Generate key label #Webpage: ss_keys_cert_dlg_generate_key #Parameters: certificate
        self.ss_keys_cert_dlg_generate_key.generate_key_label(strings.sign_key_label)
        self.ss_keys_and_cert.wait_until_cert_req_active()
        # Step Find generated key request #Webpage: ss_keys_and_cert
        self.ss_keys_and_cert.click_generated_key_request(strings.sign_key_label)
        sleep(2)
        # Step Click enerate certificate request button #Webpage: ss_keys_and_cert
        self.ss_keys_and_cert.click_generate_certificate_request()
        # Step Fill input values keys csr #Webpage: ss_keys_and_cert_generate_csr #Parameters: certificate
        self.ss_keys_and_cert_generate_csr.fill_input_values_keys_csr_sign(u'member1_configuration')
        # Step Click button id generate csr submit #Webpage: ss_keys_and_cert_generate_csr
        self.ss_keys_and_cert_generate_csr.click_button_id_generate_csr_submit()
        # Step Fill input values keys dname #Webpage: ss_keys_and_cert_dlg_subject_dname #Parameters: certificate
        self.ss_keys_and_cert_dlg_subject_dname.fill_input_values_keys_dname_sign(self.parameters[u'member1_configuration'])
        # Step Submit keys dname #Webpage: ss_keys_and_cert_dlg_subject_dname
        self.ss_keys_and_cert_dlg_subject_dname.submit_keys_dname()
        self.common_utils.get_resource_timings(u'generate_keys')
        sleep(8)
        # Step Click logout
        self.common_lib.log_out()
        sleep(3)
