import datetime
import glob
import os
import time

from selenium.webdriver.common.by import By

from helpers import ssh_server_actions, xroad, auditchecker
from tests.xroad_client_registration_in_ss_221 import client_registration_in_ss_2_2_1
from tests.xroad_client_registration_in_ss_221.client_registration_in_ss_2_2_1 import add_client_to_ss, \
    login_with_logout, add_sub_as_client_to_member, approve_requests, login
from tests.xroad_global_groups_tests import global_groups_tests
from tests.xroad_logging_in_cs_2111.logging_in_cs_2_11_1 import add_member_to_cs, add_group, \
    add_client_to_group, delete_client
from tests.xroad_ss_client_certification_213 import client_certification_2_1_3
from view_models import popups, sidebar, groups_table, cs_security_servers, members_table, keys_and_certificates_table, \
    messages, log_constants


def test_deleting_member_with_global_group(cs_ssh_host, cs_ssh_username, cs_ssh_password, client, user, test_group):
    """
    Deletes member in central server, which has global group
    :param cs_ssh_host: string - central server ssh host
    :param cs_ssh_username: string - central server ssh username
    :param cs_ssh_password:  string - central server ssh password
    :param client: dict - member info
    :param user: dict - user, under which the changes are made
    :param test_group: - test group name
    :return:
    """

    def deleting_member_with_global_group(self):
        '''Central server ssh client'''
        ssh_client = ssh_server_actions.get_client(cs_ssh_host, cs_ssh_username, cs_ssh_password)
        self.log('Adding new member to central server')
        add_member_to_cs(self, ssh_client, user, member=client)
        popups.close_all_open_dialogs(self)
        self.log('Adding new global group to central server')
        add_group(self, ssh_client, user, group=test_group)
        self.log('Adding added member to added group')
        add_client_to_group(self, ssh_client, user, member=client, group=test_group)
        self.log('Delete added member from central server')
        delete_client(self, ssh_client, user, member=client)
        self.wait_jquery()
        self.log('Check if previously added group is empty after deleting its only member')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
        self.wait_jquery()
        '''Added group member count after deletion'''
        member_count_after_deletion = self.wait_until_visible(type=By.XPATH,
                                                              element=groups_table.get_global_group_member_count_by_code(
                                                                  test_group)).text
        self.is_equal(member_count_after_deletion, '0', msg='Global group member count not 0 after deleting member')
        self.log('Remove group from central server')

    return deleting_member_with_global_group


def test_deleting_member_with_subsystem_registered_as_client_to_ss(case, cs_member_name, cs_new_member,
                                                                   ss1_client, cs_ssh_host,
                                                                   cs_ssh_username, cs_ssh_password, user):
    """
    Deletes member in central server with subsystem registered as security server client
    :param case:
    :param cs_member_name: str - new member name
    :param cs_new_member: dict - member to add
    :param ss1_client: dict - ss1 client info
    :param cs_ssh_host: str - central server ssh host
    :param cs_ssh_username: str - central server ssh username
    :param cs_ssh_password: str - central server ssh password
    :param user:
    :return:
    """
    self = case
    cs_member = {'name': cs_member_name, 'class': cs_new_member['class'], 'code': cs_new_member['code']}
    ss1_instance = ss1_client['instance']

    def deleting_member_with_subsystem_registered_as_client_to_ss():
        '''Central server ssh client instance'''
        ssh_client = ssh_server_actions.get_client(cs_ssh_host, cs_ssh_username, cs_ssh_password)
        self.log('Deleting member from central server')
        delete_client(self, ssh_client, user, member=cs_member)
        self.log('Open management requests')
        self.by_css(sidebar.MANAGEMENT_REQUESTS_CSS).click()
        requests_table = self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_TABLE_ID)
        self.wait_jquery()
        self.log('Find first table row and click on it')
        requests_table.find_element_by_tag_name('tbody').find_element_by_tag_name('tr').click()
        self.log('Open request details')
        self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
        '''Request details dialog element'''
        client_deletion_details_dialog = self.wait_until_visible(type=By.ID,
                                                                 element=cs_security_servers.CLIENT_DELETION_REQUEST_DETAILS_DIALOG_ID)
        '''Request details comment field text'''
        comment = client_deletion_details_dialog.find_element_by_class_name(
            cs_security_servers.CLIENT_DELETION_REQUEST_DETAILS_DIALOG_COMMENTS_INPUT_CLASS).text
        self.log('Check if request details is about subsystem deletion')
        self.is_equal(comment,
                      messages.SUBSYSTEM_DELETION_COMMENT.format(ss1_instance, ss1_client['class'], ss1_client['code'],
                                                                 ss1_client['subsystem']),
                      msg='Subsystem deletion comment not correct')

    return deleting_member_with_subsystem_registered_as_client_to_ss


def remove_client_and_key_from_ss(case, ss1_host, ss1_username, ss1_password, ss1_client_name, ss1_client):
    """
    Removes client and key from security server
    :param case:
    :param ss1_host: str - security server host
    :param ss1_username: str - security server username
    :param ss1_password:  str - security server password
    :param ss1_client_name:  str - security server client name
    :param ss1_client:  dict - security server client info
    :return:
    """
    self = case
    ss_1_client = {'name': ss1_client_name, 'class': ss1_client['class'], 'code': ss1_client['code'],
                   'subsystem_code': ss1_client['subsystem']}

    def remove_client_and_key():
        '''Open securtiy server homepage'''
        self.reload_webdriver(url=ss1_host, username=ss1_username, password=ss1_password)
        '''Remove added client'''
        client_registration_in_ss_2_2_1.remove_client(self, client=ss_1_client, delete_cert=True)
        '''Remove added client certificate'''
        client_registration_in_ss_2_2_1.remove_certificate(self, client=ss_1_client)

    return remove_client_and_key


def test_deleting_member_with_security_server(case, cs_ssh_host, cs_ssh_user, cs_ssh_pass,
                                              client, user):
    """
    Deletes member with security server
    :param case:
    :param cs_ssh_host: str - central server ssh host
    :param cs_ssh_user: str - central server ssh username
    :param cs_ssh_pass: str - central server ssh password
    :param client: dict - client info
    :param user: dict - username, under which the changes are made
    :return:
    """
    self = case

    def delete_member_with_security_server():
        '''Central server ssh client instance'''
        ssh_client = ssh_server_actions.get_client(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        self.log('Delete member from central server')
        delete_client(self, ssh_client, user, member=client)
        self.log('Check if security server owned by deleted member is not visible')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
        try:
            self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_TABLE_ID)
            self.by_xpath(members_table.get_row_by_td_text(client['name']))
            assert False
        except:
            pass

    return delete_member_with_security_server


def test_add_security_server_to_member(case, cs_host, cs_username, cs_password, cs_ssh_host, cs_ssh_user, cs_ssh_pass,
                                       client, cert_path, check_inputs=False):
    """
    MEMBER_12 ALL steps , except 7
    Adds security server to member in central server
    :param case:
    :param cs_host: str - central server host
    :param cs_username:  str - central server username
    :param cs_password:  str - central server password
    :param cs_ssh_host:  str - central server ssh host
    :param cs_ssh_user:  str - central server ssh username
    :param cs_ssh_pass:  str - central server ssh password
    :param client:  dict - client info
    :param cert_path:  str - cert filename
    :return:
    """
    self = case
    local_cert_path = self.get_download_path(cert_path)
    file_abs_path = os.path.abspath(local_cert_path)

    def add_security_server_to_member():
        '''Log checker instance for central server'''
        log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
        '''Current line count in log'''
        current_log_lines = log_checker.get_line_count()
        self.log('Open central server homepage')
        self.reload_webdriver(url=cs_host, username=cs_username, password=cs_password)
        self.log('Open added member details')
        global_groups_tests.open_member_details(self, client)
        self.wait_jquery()
        self.log('Open owned servers tab')
        self.by_xpath(cs_security_servers.SERVER_MANAGEMENT_OWNED_SERVERS_TAB).click()
        self.log('Click on add owned servers button')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=cs_security_servers.ADD_OWNED_SERVER_BTN_CSS).click()
        self.log('Check if fields are prefilled')
        self.is_equal(client['name'], self.wait_until_visible(type=By.ID,
                                                              element=cs_security_servers.OWNED_SERVERS_UPLOAD_OWNER_NAME_ID).text)
        self.is_equal(client['class'], self.wait_until_visible(type=By.ID,
                                                               element=cs_security_servers.OWNED_SERVERS_UPLOAD_OWNER_CLASS_ID).text)
        self.is_equal(client['code'], self.wait_until_visible(type=By.ID,
                                                              element=cs_security_servers.OWNED_SERVERS_UPLOAD_OWNER_CODE_ID).text)
        self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).click()
        server_code_input = self.wait_until_visible(type=By.ID,
                                                    element=cs_security_servers.OWNED_SERVERS_SERVER_CODE_INPUT_ID)
        self.log('Submit button disabled when fields are empty')
        self.is_false(self.by_id(cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).is_enabled())
        '''Upload button'''
        file_upload = self.by_id(cs_security_servers.OWNED_SERVERS_UPLOAD_CERT_BTN_ID)
        self.log('Uploading certificate to central server')
        xroad.fill_upload_input(self, file_upload, file_abs_path)
        self.wait_jquery()
        notice_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
        self.is_equal(messages.CERTIFICATE_IMPORT_SUCCESSFUL, notice_msg)
        '''MEMBER_12 7, 7.a. System parses the user input '''
        if check_inputs:
            self.log('MEMBER_12 7, 7.a. System parses the user input ')
            self.log('Submit button disabled when one field is empty')
            self.is_false(self.by_id(cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).is_enabled())
            self.log('MEMBER_12 7.a. Error is shown when input is 256 char long')
            self.input(element=server_code_input, text='A' * 256)
            '''Submit server registration form'''
            self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).click()
            '''Expected error message'''
            expected_error_msg = messages.INPUT_EXCEEDS_255_CHARS.format('serverCode')
            self.log('MEMBER_12 7.a.1 System displays the "{0}" error message'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            '''Expected log message'''
            expected_log_msg = log_constants.ADD_SECURITY_SERVER_FAILED
            self.log('MEMBER_12 7a.2. System logs the event {0}'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines)
            self.is_true(logs_found)
            self.log('MEMBER_12 7a.3. The server code is reinserted. '
                     'This time 255 chars, starting and ending with whitespace')
            name_255 = ' {0} '.format('A' * 255)
            self.input(element=server_code_input, text=name_255)
            '''Submit server registration form'''
            self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).click()
            '''Visible notice message text'''
            notice_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
            self.is_equal(messages.CERTIFICATE_ADDING_NEW_SERVER_REQUEST_ADDED_NOTICE.format(
                '{0}/{1}/{2}/{3}'.format(client['instance'], client['class'], client['code'], name_255.strip())),
                notice_msg)
            '''Revoke added security server request'''
            self.reload_webdriver(cs_host, cs_username, cs_password)
            client_registration_in_ss_2_2_1.revoke_requests(self, auth=True)
            '''Add server to member without input parsing check'''
            test_add_security_server_to_member(self, cs_host, cs_username, cs_password, cs_ssh_host, cs_ssh_user,
                                               cs_ssh_pass, client, cert_path)()
            return

        self.log('Insert server code to server code field')
        self.input(element=server_code_input, text=client['name'])
        self.log('Click ok')
        self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).click()
        self.wait_jquery()
        self.log('Check if certificate adding request is present')
        self.is_equal(messages.CERTIFICATE_ADDING_NEW_SERVER_REQUEST_ADDED_NOTICE.format(
            '{0}/{1}/{2}/{3}'.format(client['instance'], client['class'], client['code'], client['name'])),
            messages.get_notice_message(self))
        self.log('Check if log contains "Add security server" event"')
        logs_found = log_checker.check_log(log_constants.ADD_SECURITY_SERVER, from_line=current_log_lines + 1)
        self.is_true(logs_found, msg="Add security server log message not found")
        '''Log line count after adding'''
        current_log_lines = log_checker.get_line_count()
        self.log('Approve registration requests')
        approve_requests(self, step='MEMBER_36 ')
        self.log('Check if log contains event about Client registration request approval')
        logs_found = log_checker.check_log(log_constants.APPROVE_CLIENT_REGISTRATION_REQUST,
                                           from_line=current_log_lines + 1)
        self.is_true(logs_found, msg='"Approve client registration request" event not found in log"')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
        self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_TABLE_ID)
        self.wait_jquery()
        self.log('Check if added security server is visible in security servers table')
        self.is_not_none(self.by_xpath(members_table.get_row_by_td_text(client['name'])))

    return add_security_server_to_member


def restore_security_server_after_member_deletion(case, cs_ssh_host, cs_ssh_user, cs_ssh_pass,
                                                  client, ss2_host,
                                                  ss2_username, ss2_password, user):
    """
    MEMBER_01 steps 3(only auth cert part) - 7
    Restores security server after member being deleted in central server
    :param case:
    :param cs_ssh_host: str - central server ssh host
    :param cs_ssh_user: str - central server ssh username
    :param cs_ssh_pass: str - central server ssh password
    :param ca_ssh_host: str - ca ssh host
    :param ca_ssh_user: str - ca ssh username
    :param ca_ssh_pass: str - ca ssh password
    :param client: dict - client info
    :param ss2_host: str - security server 2 host
    :param ss2_username: str - security server 2 username
    :param ss2_password: str - security server 2 password
    :param ss2_ssh_host: str - security server 2 ssh host
    :param cert_path: str - certificate filename
    :param user: dict - user, under which the changes are made
    :return:
    """
    self = case
    sync_timeout = 120

    def restore_security_server():
        ssh_client = ssh_server_actions.get_client(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        self.log('Open members page')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MEMBERS_CSS).click()
        self.log('Add  member to central server')
        add_member_to_cs(self, ssh_client, user, member=client)
        self.log('Wait until servers have synchronized')
        time.sleep(sync_timeout)
        self.log('Open security server, which was deleted from central server')
        self.reload_webdriver(url=ss2_host, username=ss2_username, password=ss2_password)
        self.log('Open keys and certificates')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.KEYS_AND_CERTIFICATES_TABLE_ID)
        self.wait_jquery()
        self.log('Click on the certificate, which has global error status and delete it')
        self.by_xpath(keys_and_certificates_table.GLOBAL_ERROR_CERTIFICATE_ROW_XPATH).click()
        self.by_id(keys_and_certificates_table.DELETE_BTN_ID).click()
        popups.confirm_dialog_click(self)
        self.wait_jquery()
    return restore_security_server


def setup_member_with_subsystem_as_ss_client(case, cs_host, cs_username, cs_password, cs_member_name, cs_new_member,
                                             ss1_host, ss1_username,
                                             ss1_password, ss1_client,
                                             ss1_server_name, ss1_client_name):
    """
    Adds member in central server who has subsystem as security server client
    :param case:
    :param cs_host: str - central server host
    :param cs_username: str - central server username
    :param cs_password:  str - central server password
    :param cs_member_name:  str - central server member name
    :param cs_new_member:  dict - central server new member info
    :param ss1_host: str - security server host
    :param ss1_username: str - security server username
    :param ss1_password: str - security server password
    :param ss1_client: dict - security server client info
    :param ss1_server_name: str - security server name
    :param ss1_client_name:  str - security server client name
    :return:
    """
    self = case
    sync_retry = 30
    sync_timeout = 120
    wait_input = 2

    cs_member = {'name': cs_member_name, 'class': cs_new_member['class'], 'code': cs_new_member['code']}

    ss_1_client = {'name': ss1_client_name, 'class': ss1_client['class'], 'code': ss1_client['code'],
                   'subsystem_code': ss1_client['subsystem']}

    def setup_member_with_subsystem():
        self.log('Login to central server')
        login(self, host=cs_host, username=cs_username, password=cs_password)
        self.log('Adding new member to central server')
        client_registration_in_ss_2_2_1.add_member_to_cs(self, cs_member)
        self.log('Login to security server')
        login(self, host=ss1_host, username=ss1_username, password=ss1_password)
        self.log('Wait until data is synced between servers')
        time.sleep(sync_timeout)
        self.log('Add previously added member as client to security server')
        add_client_to_ss(self, ss_1_client, retry_interval=sync_retry, retry_timeout=sync_timeout,
                         wait_input=wait_input)
        self.log('Navigate to security server homepage')
        self.driver.get(ss1_host)
        self.log('Certificate added client')
        client_certification_2_1_3.test_generate_csr_and_import_cert(client_code=ss_1_client['code'],
                                                                     client_class=ss_1_client['class'])(self)
        self.log('Log out and log in to central server')
        login_with_logout(self, cs_host, cs_username, cs_password)
        self.log('Add subsystem to client')
        add_sub_as_client_to_member(self, ss1_server_name, ss_1_client, wait_input=wait_input,
                                    step='Adding subsystem')

        self.log('Approve the registration requests')
        approve_requests(self, '2.2.1-5 ', cancel_confirmation=False)

    return setup_member_with_subsystem
