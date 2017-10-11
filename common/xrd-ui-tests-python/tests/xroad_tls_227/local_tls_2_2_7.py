import os
import tarfile
import time

from requests.exceptions import SSLError
from selenium.webdriver.common.by import By

from helpers import xroad, soaptestclient, auditchecker, ssh_client, ssh_server_actions
from tests.xroad_configure_service_222 import configure_service_2_2_2
from view_models import popups, clients_table_vm, sidebar, ss_system_parameters, messages, log_constants

# These faults are checked when we need the result to be unsuccessful. Otherwise the checking function returns True.
faults_unsuccessful = ['Server.ClientProxy.SslAuthenticationFailed']
# These faults are checked when we need the result to be successful. Otherwise the checking function returns False.
faults_successful = ['Server.ServerProxy.AccessDenied', 'Server.ServerProxy.UnknownService',
                     'Server.ServerProxy.ServiceDisabled', 'Server.ClientProxy.*', 'Client.*']


def test_delete_tls(case, client, provider):
    self = case

    ss1_host = self.config.get('ss1.host')
    ss1_user = self.config.get('ss1.user')
    ss1_pass = self.config.get('ss1.pass')

    ss2_host = self.config.get('ss2.host')
    ss2_user = self.config.get('ss2.user')
    ss2_pass = self.config.get('ss2.pass')

    ss1_ssh_host = self.config.get('ss1.ssh_host')
    ss1_ssh_user = self.config.get('ss1.ssh_user')
    ss1_ssh_pass = self.config.get('ss1.ssh_pass')

    ss2_ssh_host = self.config.get('ss2.ssh_host')
    ss2_ssh_user = self.config.get('ss2.ssh_user')
    ss2_ssh_pass = self.config.get('ss2.ssh_pass')

    client_id = xroad.get_xroad_subsystem(client)
    provider_id = xroad.get_xroad_subsystem(provider)

    testservice_name = self.config.get('services.test_service')
    wsdl_url = self.config.get('wsdl.remote_path').format(self.config.get('wsdl.service_wsdl'))
    new_service_url = self.config.get('services.test_service_url')

    def delete_tls():
        '''Getting auditchecker instance for ss1'''
        log_checker = auditchecker.AuditChecker(host=ss1_ssh_host, username=ss1_ssh_user, password=ss1_ssh_pass)
        '''Get current log lines count'''
        current_log_lines = log_checker.get_line_count()
        self.reload_webdriver(url=ss1_host, username=ss1_user, password=ss1_pass)

        self.log('2.2.7 delete_tls')
        self.log('2.2.7-delete setting {0} connection type to HTTP'.format(client_id))

        # Open "Security Server Clients" page
        self.by_css(sidebar.CLIENTS_BTN_CSS).click()

        # Wait until list is loaded
        self.wait_jquery()

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_internal_servers(self, client_id=client_id)

        # Set connection type to HTTPS_NO_AUTH (SSLNOAUTH)
        self.is_true(clients_table_vm.client_servers_popup_set_connection(self, 'NOSSL'),
                     msg='2.2.7-delete-2 Failed to set connection type')

        # Delete all internal certificates
        deleted_certs = clients_table_vm.client_servers_popup_delete_tls_certs(self, cancel_deletion=True)

        expected_log_msg = log_constants.DELETE_INTERNAL_TSL_CERT
        '''If cert(s) were deleted check audit.log'''
        if deleted_certs > 0:
            '''Log message expected to be present in audit.log after deletion'''
            logs_found = log_checker.check_log(expected_log_msg,
                                               from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                             expected_log_msg,
                             log_checker.found_lines))

        '''Get auditchecker instance for ss2'''
        log_checker = auditchecker.AuditChecker(host=ss2_ssh_host, username=ss2_ssh_user, password=ss2_ssh_pass)
        # Switch to Security server 2
        self.reload_webdriver(url=ss2_host, username=ss2_user, password=ss2_pass)

        # Open "Security Server Clients" page
        self.by_css(sidebar.CLIENTS_BTN_CSS).click()

        # Wait until list is loaded
        self.wait_jquery()

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_services(self, client_id=provider_id)

        # Find the service under the specified WSDL in service list (and expand the WSDL services list if not open yet)
        service_row = clients_table_vm.client_services_popup_find_service(self, wsdl_url=wsdl_url,
                                                                          service_name=testservice_name)

        # Click on the service row to select it
        service_row.click()

        # Open service parameters by finding the "Edit" button and clicking it.
        edit_service_button = self.by_id(popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID)

        # Click the "Edit" button to open "Edit Service Parameters" popup
        edit_service_button.click()

        warning, error = configure_service_2_2_2.edit_service(self, service_url=new_service_url)
        case.is_none(error, msg='2.2.7-14 Got error when trying to update service URL')

        # Click tab "Internal Servers"
        self.by_css(clients_table_vm.INTERNAL_CERTS_TAB_TITLE_CSS).click()

        # Wait until everything is loaded.
        self.wait_jquery()

        '''Get current log lines count'''
        current_log_lines = log_checker.get_line_count()
        # Delete all internal certificates
        deleted_certs = clients_table_vm.client_servers_popup_delete_tls_certs(self)
        '''If certs were deleted, check log'''
        if deleted_certs > 0:
            '''Checks if expected message present in log'''
            logs_found = log_checker.check_log(expected_log_msg,
                                               from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                             expected_log_msg,
                             log_checker.found_lines))

    return delete_tls


def test_tls(case, client, provider):
    self = case

    certs_download_filename = self.config.get('certs.downloaded_ss_certs_filename')
    certs_ss1_filename = self.config.get('certs.ss1_certs')
    certs_ss2_filename = self.config.get('certs.ss2_certs')
    verify_cert_filename = self.config.get('certs.server_cert_filename')
    client_cert_filename = self.config.get('certs.client_cert_filename')
    client_key_filename = self.config.get('certs.client_key_filename')
    mock_cert_filename = self.config.get('certs.service_cert_filename')

    download_check_interval = 1  # Seconds
    download_time_limit = self.config.get('certs.cert_download_time_limit')
    delete_created_files = False

    sync_retry = self.config.get('services.request_sync_delay')
    sync_max_seconds = self.config.get('services.request_sync_timeout')

    client_id = xroad.get_xroad_subsystem(client)
    provider_id = xroad.get_xroad_subsystem(provider)

    ss1_ssh_host = self.config.get('ss1.ssh_host')
    ss1_ssh_user = self.config.get('ss1.ssh_user')
    ss1_ssh_pass = self.config.get('ss1.ssh_pass')

    ss1_host = self.config.get('ss1.host')
    ss1_user = self.config.get('ss1.user')
    ss1_pass = self.config.get('ss1.pass')

    ss2_host = self.config.get('ss2.host')
    ss2_user = self.config.get('ss2.user')
    ss2_pass = self.config.get('ss2.pass')

    wsdl_url = self.config.get('wsdl.remote_path').format(self.config.get('wsdl.service_wsdl'))
    testservice_name = self.config.get('services.test_service')
    new_service_url = self.config.get('services.test_service_url_ssl')

    query_url = self.config.get('ss1.service_path')
    query_url_ssl = self.config.get('ss1.service_path_ssl')
    query_filename = self.config.get('services.request_template_filename')
    query = self.get_xml_query(query_filename)
    client_cert_path = self.get_cert_path(client_cert_filename)
    client_key_path = self.get_cert_path(client_key_filename)
    mock_cert_path = self.get_cert_path(mock_cert_filename)

    ss2_certs_directory = self.config.get('certs.ss2_certificate_directory')

    testclient_params = {
        'xroadProtocolVersion': self.config.get('services.xroad_protocol'),
        'xroadIssue': self.config.get('services.xroad_issue'),
        'xroadUserId': self.config.get('services.xroad_userid'),
        'serviceMemberInstance': provider['instance'],
        'serviceMemberClass': provider['class'],
        'serviceMemberCode': provider['code'],
        'serviceSubsystemCode': provider['subsystem'],
        'serviceCode': xroad.get_service_name(testservice_name),
        'serviceVersion': xroad.get_service_version(testservice_name),
        'memberInstance': client['instance'],
        'memberClass': client['class'],
        'memberCode': client['code'],
        'subsystemCode': client['subsystem'],
        'requestBody': self.config.get('services.testservice_request_body')
    }

    testclient_http = soaptestclient.SoapTestClient(url=query_url, body=query,
                                                    retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                    faults_successful=faults_successful,
                                                    faults_unsuccessful=faults_unsuccessful, params=testclient_params)
    testclient_https = soaptestclient.SoapTestClient(url=query_url_ssl, body=query,
                                                     retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                     server_certificate=self.get_download_path(verify_cert_filename),
                                                     faults_successful=faults_successful,
                                                     faults_unsuccessful=faults_unsuccessful, params=testclient_params)
    testclient_https_ss2 = soaptestclient.SoapTestClient(url=query_url_ssl, body=query,
                                                         retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                         server_certificate=self.get_download_path(
                                                             os.path.join(ss2_certs_directory, verify_cert_filename)),
                                                         client_certificate=(client_cert_path, client_key_path),
                                                         faults_successful=faults_successful,
                                                         faults_unsuccessful=faults_unsuccessful,
                                                         params=testclient_params)

    def local_tls():
        """
        :param self: MainController class object
        :return: None
        ''"""

        # TEST PLAN 2.2.7 test local TLS
        self.log('*** 2.2.7 / XT-471')

        self.reload_webdriver(url=ss1_host, username=ss1_user, password=ss1_pass)

        certs_filename = self.get_download_path(certs_download_filename)

        ss1_filename = self.get_download_path(certs_ss1_filename)
        ss2_filename = self.get_download_path(certs_ss2_filename)

        ss2_certs_directory_abs = self.get_download_path(ss2_certs_directory)

        # Create directory if not exists
        if not os.path.isdir(ss2_certs_directory_abs):
            os.mkdir(ss2_certs_directory_abs)

        self.remove_files([certs_filename, ss1_filename, ss2_filename, ss2_certs_directory_abs])

        created_files = [certs_filename]

        self.start_mock_service()

        # TEST PLAN 2.2.7-1 generate new internal TLS key.
        self.log('2.2.7-1 generate new internal TLS key.')

        # Click "System Parameters" in sidebar
        self.by_css(sidebar.SYSTEM_PARAMETERS_BTN_CSS).click()

        '''Get auditcheker instance for ss1'''
        log_checker = auditchecker.AuditChecker(host=ss1_ssh_host, username=ss1_ssh_user, password=ss1_ssh_pass)
        '''Get current audit.log line count'''
        current_log_lines = log_checker.get_line_count()

        '''Get TLS hash before generating process'''
        tls_hash_before_generating = self.wait_until_visible(type=By.ID,
                                                             element=ss_system_parameters.INTERNAL_TLS_CERT_HASH_ID).text
        '''Verify "Certificate Details" button'''
        certificate_details_btn = self.wait_until_visible(self.by_id(ss_system_parameters.CERTIFICATE_DETAILS_BUTTON_ID)).is_enabled()
        self.is_true(certificate_details_btn,
                     msg='Certificate Details not enabled')

        '''Click "Generate New TLS Key" button'''
        self.wait_until_visible(ss_system_parameters.GENERATE_INTERNAL_TLS_KEY_BUTTON_ID, type=By.ID).click()
        ssh_client = ssh_server_actions.get_client(ss1_ssh_host, ss1_ssh_user, ss1_ssh_pass)
        '''SS_11 3a Generating TLS key is canceled'''
        self.log('SS_11 3a Generating TLS key is canceled')
        self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
        '''Get TLS hash after canceling generation'''
        tls_hash_after_canceling = self.wait_until_visible(type=By.ID,
                                                           element=ss_system_parameters.INTERNAL_TLS_CERT_HASH_ID).text
        '''Check if TLS hash is same as before after canceling'''
        self.is_equal(tls_hash_before_generating, tls_hash_after_canceling)
        '''Click "Generate New TLS Key" button again'''
        self.wait_until_visible(ss_system_parameters.GENERATE_INTERNAL_TLS_KEY_BUTTON_ID, type=By.ID).click()
        '''Script which generates TLS key'''
        cert_gen_script_path = '/usr/share/xroad/scripts/generate_certificate.sh'
        '''Script new name'''
        cert_gen_scipt_new_path = cert_gen_script_path + '.backup'
        '''Rename script'''
        ssh_server_actions.mv(ssh_client, src=cert_gen_script_path,
                              destination=cert_gen_scipt_new_path, sudo=True)

        '''A confirmation dialog should open. Confirm the question.'''
        popups.confirm_dialog_click(self)

        '''Wait until the TLS certificate has been generated.'''
        self.wait_jquery()

        '''SS_11 4a.1 system failed to generate key error check'''
        try:
            self.log('Check if "Certificate generation script not found" error is equal to expected')
            error_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(messages.GENERATE_CERTIFICATE_NOT_FOUND_ERROR.format(cert_gen_script_path), error_message)
        except:
            self.log('"Certificate generation script not found" error not present')
            assert False
        finally:
            self.log('Rename generation script back to original')
            ssh_server_actions.mv(ssh_client, src=cert_gen_scipt_new_path,
                                  destination=cert_gen_script_path, sudo=True)

        self.wait_until_visible(ss_system_parameters.GENERATE_INTERNAL_TLS_KEY_BUTTON_ID, type=By.ID).click()
        popups.confirm_dialog_click(self)

        '''Wait until the TLS certificate has been generated.'''
        self.wait_jquery()

        '''Get TLS hash after confirming generation'''
        tls_hash_after_confirming = self.wait_until_visible(type=By.ID,
                                                            element=ss_system_parameters.INTERNAL_TLS_CERT_HASH_ID).text
        '''Check if TLS hash is not same as before'''
        self.not_equal(tls_hash_before_generating, tls_hash_after_confirming)

        '''Log message expected to present after changing Service consumer connection type'''
        expected_log_msg = log_constants.GENERATE_TLS_KEY_AND_CERT
        '''Checks if expected log message present in log'''
        logs_found = log_checker.check_log(expected_log_msg,
                                           from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                         expected_log_msg,
                         log_checker.found_lines))

        self.log('2.2.7-1 new key has been generated, downloading certificate')

        # If file already exists, delete it first
        if os.path.isfile(certs_filename):
            os.remove(certs_filename)

        # Find and click the "Export" button. Download should start automatically.
        self.by_id(ss_system_parameters.EXPORT_INTERNAL_TLS_CERT_BUTTON_ID).click()

        # Check if file exists every 0.5 seconds or until limit has passed.
        start_time = time.time()
        while True:
            if time.time() - start_time > download_time_limit:
                # Raise AssertionError
                raise AssertionError('Download time limit of {0} seconds passed for file {1}'.format(
                    download_time_limit, certs_download_filename))
            if os.path.isfile(certs_filename):
                try:
                    os.rename(certs_filename, ss1_filename)
                    break
                except OSError:
                    pass
            time.sleep(download_check_interval)


        created_files.append(ss1_filename)
        self.log('2.2.7-1 certificate archive has been downloaded, extracting')

        # We're here, so download succeeded.
        # Extract the archive (tgz format) to downloads directory.
        with tarfile.open(ss1_filename, 'r:gz') as tar:
            # tarfile.extractall does not overwrite files so we need to extract them one by one.
            for fileobj in tar:
                filename = os.path.join(os.path.dirname(fileobj.name), os.path.basename(fileobj.name))
                file_target = self.get_download_path(filename)
                if os.path.isfile(file_target):
                    os.remove(file_target)
                created_files.append(file_target)
                tar.extract(fileobj, self.get_download_path())

        self.log('2.2.7-1 certificate archive has been extracted')

        # TEST PLAN 2.2.7-2 setting connection type to HTTPS_NO_AUTH
        self.log('2.2.7-2 setting {0} connection type to HTTPS_NO_AUTH'.format(client_id))

        # Open "Security Server Clients" page
        self.by_css(sidebar.CLIENTS_BTN_CSS).click()

        # Wait until list is loaded
        self.wait_jquery()

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_internal_servers(self, client_id=client_id)

        '''Get current audit.log line count'''
        current_log_lines = log_checker.get_line_count()

        '''Set connection type to HTTPS_NO_AUTH (SSLNOAUTH)'''
        case.is_true(clients_table_vm.client_servers_popup_set_connection(self, 'SSLNOAUTH'),
                     msg='2.2.7-2 Failed to set connection type')
        '''Log message expected to present after changing Service consumer connection type'''
        expected_log_msg = log_constants.SET_SERVICE_CONSUMER_CONNECTION_TYPE
        '''Checks if expected log message present in log'''
        logs_found = log_checker.check_log(expected_log_msg,
                                           from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                         expected_log_msg,
                         log_checker.found_lines))

        # TEST PLAN 2.2.7-3 test query from TS1:CLIENT1:sub to test service. Query should fail.
        self.log('2.2.7-3 test query {0} to test service. Query should fail.'.format(query_filename))

        case.is_true(testclient_http.check_fail(), msg='2.2.7-3 test query succeeded')

        # TEST PLAN 2.2.7-4/5 test query to test service using SSL and client certificate. Query should succeed.
        self.log('2.2.7-4/5 test query to test service using SSL and client certificate. Query should succeed.')
        case.is_true(testclient_https.check_success(), msg='2.2.7-5 test query failed')

        # TEST PLAN 2.2.7-6 setting connection type to HTTPS
        self.log('2.2.7-6 setting {0} connection type to HTTPS'.format(client_id))

        # Set connection type to HTTPS (SSLAUTH)
        case.is_true(clients_table_vm.client_servers_popup_set_connection(self, 'SSLAUTH'),
                     msg='2.2.7-6 Failed to set connection type')

        # TEST PLAN 2.2.7-7 test query to test service using SSL and client certificate. Query should fail.
        self.log('2.2.7-7 test query to test service using SSL and client certificate. Query should fail.')
        case.is_true(testclient_https.check_fail(), msg='2.2.7-7 test query succeeded')

        # TEST PLAN 2.2.7-8 upload certificate to TS1 client CLIENT1:sub
        self.log('2.2.7-8 upload certificate to TS1 client {0}'.format(client_id))

        '''Gets current audit.log line count'''
        current_log_lines = log_checker.get_line_count()
        '''Click add certificate button'''
        self.by_id(popups.CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_ADD_CERTIFICATE_BTN_ID).click()

        '''Get upload button'''
        upload_button = self.by_id(popups.FILE_UPLOAD_BROWSE_BUTTON_ID)
        '''File with wrong extension'''
        not_existing_file_with_wrong_extension = 'C:\\file.asd'
        xroad.fill_upload_input(self, upload_button, not_existing_file_with_wrong_extension)

        '''Find submit button'''
        submit_button = self.by_id(popups.FILE_UPLOAD_SUBMIT_BUTTON_ID)
        '''Click submit button'''
        submit_button.click()
        '''Wait until error message is visible'''
        time.sleep(0.5)
        self.wait_jquery()
        error_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
        '''Check if wrong file format error message is correct'''
        self.is_equal(error_message, messages.TSL_CERTIFICATE_INCORRECT_FILE_FORMAT,
                      msg='Already existing certificate message not correct')
        '''Cancel uploading'''
        self.by_xpath(popups.FILE_UPLOAD_CANCEL_BTN_XPATH).click()
        '''Checks if expected log message present in log'''
        expected_log_msg=log_constants.ADD_INTERNAL_TLS_CERT_FAILED
        logs_found = log_checker.check_log(expected_log_msg,
                                           from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                         expected_log_msg,
                         log_checker.found_lines))

        '''Find the "Add" button and click it.'''
        self.by_id(popups.CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_ADD_CERTIFICATE_BTN_ID).click()

        '''Fill the upload popup'''
        xroad.fill_upload_input(self, upload_button, client_cert_path)

        submit_button = self.by_id(popups.FILE_UPLOAD_SUBMIT_BUTTON_ID)
        submit_button.click()
        '''Wait until notice message visible'''
        time.sleep(0.5)
        self.wait_jquery()
        notice_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
        '''Check if successful import message is correct'''
        self.is_equal(notice_message, messages.CERTIFICATE_IMPORT_SUCCESSFUL,
                      msg='Certificate successful import message not correct.')

        '''Expected internal TLS adding log message'''
        expected_log_msg = log_constants.ADD_INTERNAL_TLS_CERT
        '''Check if expected messsage is present'''
        logs_found = log_checker.check_log(expected_log_msg,
                                           from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                         expected_log_msg,
                         log_checker.found_lines))
        current_log_lines=log_checker.get_line_count()
        '''Find the "Add" button and click it.'''
        self.by_id(popups.CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_ADD_CERTIFICATE_BTN_ID).click()

        '''Get the upload button'''
        upload_button = self.by_id(popups.FILE_UPLOAD_BROWSE_BUTTON_ID)
        '''Fill the upload popup'''
        xroad.fill_upload_input(self, upload_button, client_cert_path)

        '''Confirm TLS adding'''
        submit_button = self.by_id(popups.FILE_UPLOAD_SUBMIT_BUTTON_ID)
        submit_button.click()
        '''Wait until error message visible'''
        time.sleep(0.5)
        self.wait_jquery()
        error_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
        '''Check if error message is expected'''
        self.is_equal(error_message, messages.TSL_CERTIFICATE_ALREADY_EXISTS,
                      msg='Already existing certificate message not correct')
        '''Cancel TLS adding'''
        self.by_xpath(popups.FILE_UPLOAD_CANCEL_BTN_XPATH).click()

        '''Checks if expected log message present in log'''
        expected_log_msg=log_constants.ADD_INTERNAL_TLS_CERT_FAILED
        logs_found = log_checker.check_log(expected_log_msg,
                                           from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                         expected_log_msg,
                         log_checker.found_lines))

        # TEST PLAN 2.2.7-9 test query to test service using SSL and client certificate. Query should succeed.
        self.log('2.2.7-9 test query to test service using SSL and client certificate. Query should succeed.')

        # Set client certificate and key
        testclient_https.client_certificate = (client_cert_path, client_key_path)

        case.is_true(testclient_https.check_success(), msg='2.2.7-9 test query failed')

        # TEST PLAN 2.2.7-10 set test client to use TS2 TLS certificate
        self.log('2.2.7-10 set test client to use TS2 TLS certificate')

        # First, get the certificate. For this, we need to get webdriver to go to TS2
        self.reload_webdriver(url=ss2_host, username=ss2_user, password=ss2_pass)

        # Click "System Parameters" in sidebar
        self.by_css(sidebar.SYSTEM_PARAMETERS_BTN_CSS).click()

        self.wait_jquery()

        self.log('2.2.7-10 downloading TS2 certificate')

        if os.path.isfile(certs_filename):
            os.remove(certs_filename)

        # Find and click the "Export" button. Download should start automatically.
        self.by_id(ss_system_parameters.EXPORT_INTERNAL_TLS_CERT_BUTTON_ID).click()

        # Check if file exists every 0.5 seconds or until limit has passed.
        start_time = time.time()
        while True:
            if os.path.isfile(certs_filename):
                break
            if time.time() - start_time > download_time_limit:
                # Raise AssertionError
                raise AssertionError('Download time limit of {0} seconds passed for file {1}'.format(
                    download_time_limit, certs_download_filename))
            time.sleep(download_check_interval)

        os.rename(certs_filename, ss2_filename)

        created_files.append(ss2_filename)
        self.log('2.2.7-10 certificate archive has been downloaded, extracting')

        # We're here, so download succeeded.

        # Extract the archive (tgz format) to downloads directory.
        with tarfile.open(ss2_filename, 'r:gz') as tar:
            # tarfile.extractall does not overwrite files so we need to extract them one by one.
            for fileobj in tar:
                filename = self.get_download_path(os.path.join(ss2_certs_directory, os.path.dirname(fileobj.name),
                                                               os.path.basename(fileobj.name)))
                file_target = self.get_download_path(filename)
                if os.path.isfile(file_target):
                    os.remove(file_target)
                created_files.append(file_target)
                tar.extract(fileobj, self.get_download_path(ss2_certs_directory))

        self.log('2.2.7-10 certificate archive has been extracted')

        # TEST PLAN 2.2.7-11 test query to test service using SSL and TS2 certificate. Query should fail.
        self.log('2.2.7-11 test query to test service using SSL and client certificate, verify TS2. Query should fail.')

        try:
            testclient_https_ss2.check_fail()
            case.is_true(False, msg='2.2.7-11 test query failed but not with an SSLError.')
        except SSLError:
            # We're actually hoping to get an SSLError so we're good.
            pass

        # TEST PLAN 2.2.7-12/13 test query to test service using SSL and TS1 certificate. Query should succeed.
        self.log(
            '2.2.7-12/13 test query to test service using SSL and client certificate, verify TS1. Query should succeed.')

        case.is_true(testclient_https.check_success(), msg='2.2.7-13 test query failed')

        # TEST PLAN 2.2.7-14 TS2 test service is configured from http to https. TLS check disabled.
        self.log(
            '2.2.7-14 TS2 test service is configured from http to https. TLS check disabled.'.format(new_service_url))

        # Open "Security Server Clients" page
        self.by_css(sidebar.CLIENTS_BTN_CSS).click()

        # Wait until list is loaded
        self.wait_jquery()

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_services(self, client_id=provider_id)

        # Find the service under the specified WSDL in service list (and expand the WSDL services list if not open yet)
        service_row = clients_table_vm.client_services_popup_find_service(self, wsdl_url=wsdl_url,
                                                                          service_name=testservice_name)

        # Click on the service row to select it
        service_row.click()

        # Open service parameters by finding the "Edit" button and clicking it.
        edit_service_button = self.by_id(popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID)

        # Click the "Edit" button to open "Edit Service Parameters" popup
        edit_service_button.click()

        warning, error = configure_service_2_2_2.edit_service(self, service_url=new_service_url, verify_tls=False)
        case.is_none(error, msg='2.2.7-14 Got error when trying to update service URL')

        # TEST PLAN 2.2.7-15 test query to test service using SSL and TS1 certificate. Query should succeed.
        self.log('2.2.7-15 test query to test service using SSL and client certificate. Query should succeed.')
        case.is_true(testclient_https.check_success(), msg='2.2.7-15 test query failed')

        # TEST PLAN 2.2.7-16 TS2 test service is as https with TLS certificate check enabled.

        # Click the "Edit" button to open "Edit Service Parameters" popup
        edit_service_button.click()

        configure_service_2_2_2.edit_service(self, service_url=new_service_url, verify_tls=True)

        # TEST PLAN 2.2.7-17 test query to test service using SSL and TS1 certificate. Query should succeed.
        self.log('2.2.7-17 test query to test service using SSL and client certificate. Query should fail.')

        case.is_true(testclient_https.check_fail(faults=['Server.ServerProxy.ServiceFailed.SslAuthenticationFailed']),
                     msg='2.2.7-17 test query succeeded')

        # TEST PLAN 2.2.7-18 import test service TLS certificate to security server TS2
        self.log('2.2.7-18 import test service TLS certificate to security server TS2')

        # Click tab "Internal Servers"
        self.by_css(clients_table_vm.INTERNAL_CERTS_TAB_TITLE_CSS).click()

        # Wait until everything is loaded.
        self.wait_jquery()

        # Find the "Add" button and click it.
        self.by_id(popups.CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_ADD_CERTIFICATE_BTN_ID).click()

        # Get the upload button
        upload_button = self.by_id(popups.FILE_UPLOAD_BROWSE_BUTTON_ID)
        xroad.fill_upload_input(self, upload_button, mock_cert_path)

        submit_button = self.by_id(popups.FILE_UPLOAD_SUBMIT_BUTTON_ID)
        submit_button.click()

        # TEST PLAN 2.2.7-19 test query to test service using SSL and client certificate. Should succeed.
        self.log('2.2.7-19 test query to test service using SSL and client certificate. Query should succeed.')

        case.is_true(testclient_https.check_success(), msg='2.2.7-19 test query failed')

        # Remove all created files
        if delete_created_files:
            self.log('2.2.7 removing downloaded files')
            self.remove_files(created_files)

    return local_tls
