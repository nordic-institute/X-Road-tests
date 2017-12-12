import os
import time

from selenium.webdriver.common.by import By

from helpers import ssh_server_actions, xroad, auditchecker
from tests.xroad_client_registration_in_ss_221 import client_registration_in_ss
from tests.xroad_client_registration_in_ss_221.client_registration_in_ss import login, add_client_to_ss, \
    login_with_logout, add_sub_as_client_to_member, approve_requests
from tests.xroad_cs_add_member.add_cs_member import add_member_to_cs
from tests.xroad_cs_revoke_requests.revoke_requests import revoke_requests
from tests.xroad_global_groups_tests import global_groups_tests
from tests.xroad_logging_in_cs_2111.logging_in_cs import add_group, \
    add_client_to_group, delete_member
from tests.xroad_ss_client_certification_213 import client_certification
from view_models import popups, sidebar, groups_table, cs_security_servers, members_table, keys_and_certificates_table, \
    messages, log_constants
from view_models.cs_security_servers import SECURITY_SERVER_TABLE_CSS
from view_models.log_constants import APPROVE_CLIENT_REGISTRATION_REQUST, ADD_SECURITY_SERVER, DELETE_MEMBER
from view_models.messages import CERTIFICATE_IMPORT_SUCCESSFUL, CERTIFICATE_ADDING_NEW_SERVER_REQUEST_ADDED_NOTICE


def remove_member(self, member, group=None, member_has_subsystem_as_client=False, try_cancel=False, log_checker=None):
    """
    Removes a member.
    :param self: MainController object
    :param member: dict - member data
    :return: None
    """

    current_log_lines = None
    if log_checker:
        current_log_lines = log_checker.get_line_count()

    # UC MEMBER_26 1. Select to delete an X-Road member
    self.log('MEMBER_26 1. Select to delete an X-Road member')

    # Get the members table
    self.log('Wait for members table')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MEMBERS_CSS).click()
    self.wait_jquery()
    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    self.wait_jquery()

    # Get the member row
    self.log('Get row by row values')
    row = members_table.get_row_by_columns(table, [member['name'], member['class'], member['code']])
    if row is None:
        # Nothing found - error
        assert False, 'Deletion member not found'

    # Click on the member
    row.click()

    # Open details
    self.log('Click on "DETAILS" button')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.wait_jquery()

    # Click delete button
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()
    self.wait_jquery()

    if try_cancel:
        self.log('MEMBER_26 3a. Cancel member deletion')
        self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
        self.log('Click delete button again')
        self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()

    # UC MEMBER_26 2, 3. System prompts for confirmation, administrator confirms.
    self.log('MEMBER_26 2, 3. System prompts for confirmation, administrator confirms.')

    # Confirm the deletion
    self.log('Confirm deleting member')
    popups.confirm_dialog_click(self)
    if group:
        self.log('MEMBER_26 6.a Delete member in global group from central server')
        self.log('MEMBER_26 6.a1 System removes the member from global groups')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
        self.wait_jquery()

        member_count_after_deletion = self.wait_until_visible(type=By.XPATH,
                                                              element=groups_table.get_global_group_member_count_by_code(
                                                                  group)).text
        self.is_equal(member_count_after_deletion, '0', msg='Global group member count not 0 after deleting member')

    if member_has_subsystem_as_client:
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
        expected_deletion_comment = messages.SUBSYSTEM_DELETION_COMMENT.format(member['identifier'], member['class'],
                                                                               member['code'],
                                                                               member['subsystem_code'])
        self.log('MEMBER_26 5a.1 System creates and saves a security server '
                 'client deletion request with the comment \n"{0}"'.format(expected_deletion_comment))
        self.is_equal(comment,
                      expected_deletion_comment,
                      msg='Subsystem deletion comment not correct, expected {}, got {}'.format(
                          expected_deletion_comment, comment))
    if current_log_lines:
        expected_log_msg = DELETE_MEMBER
        self.log('MEMBER_26 System logs the event "{}"'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)


def test_deleting_member_with_global_group(client, user, test_group):
    """
    Delete member in central server, which has global group test
    :param client: dict - member info
    :param user: dict - user, under which the changes are made
    :param test_group: - test group name
    :return:
    """

    def deleting_member_with_global_group(self):

        # MEMBER_10 Add new X-Road Member
        self.log('MEMBER_10 Add new X-Road Member')
        add_member_to_cs(self, client)
        popups.close_all_open_dialogs(self)

        # SERVICE_33 add the new subsystem to the new group
        self.log('SERVICE_33 add the new subsystem to the new group')
        add_client_to_group(self, user, member=client, group=test_group)

    return deleting_member_with_global_group


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
        client_registration_in_ss.remove_client(self, client=ss_1_client, delete_cert=True)
        '''Remove added client certificate'''
        client_registration_in_ss.remove_certificate(self, client=ss_1_client)

    return remove_client_and_key


def test_deleting_member_with_security_server(self, cs_ssh_host, cs_ssh_user, cs_ssh_pass,
                                              client, user):
    """
    Delete member with security server test
    :param case:
    :param cs_ssh_host: str - central server ssh host
    :param cs_ssh_user: str - central server ssh username
    :param cs_ssh_pass: str - central server ssh password
    :param client: dict - client info
    :param user: dict - username, under which the changes are made
    :return:
    """

    def delete_member_with_security_server():
        self.log('MEMBER_26 4a. Delete member from central server, which has owned security server')
        ssh_client = ssh_server_actions.get_client(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        delete_member(self, ssh_client, user, member=client)

        self.log('MEMBER_26 4a.1 System deletes the security server')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
        try:
            self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_TABLE_ID)
            self.by_xpath(members_table.get_row_by_td_text(client['name']))
            assert False
        except:
            pass

    return delete_member_with_security_server




def add_central_server_member_delete_global_error_cert(case,
                                                       client, ss2_host,
                                                       ss2_username, ss2_password):
    """
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

    def add_cs_member_delete_global_error_cert():
        self.log('Open members page')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MEMBERS_CSS).click()

        # MEMBER_10 Add new X-Road Member
        self.log('MEMBER_10 Add new X-Road Member')
        add_member_to_cs(self, member=client)

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

    return add_cs_member_delete_global_error_cert


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
        client_registration_in_ss.add_member_to_cs(self, cs_member)
        self.log('Login to security server')
        login(self, host=ss1_host, username=ss1_username, password=ss1_password)
        self.log('Wait until data is synced between servers')
        time.sleep(sync_timeout)
        self.log('Add member as client to security server')
        add_client_to_ss(self, ss_1_client, retry_interval=sync_retry, retry_timeout=sync_timeout,
                         wait_input=wait_input)
        self.log('Navigate to security server homepage')
        self.driver.get(ss1_host)
        self.log('Certificate added client')
        client_certification.test_generate_csr_and_import_cert(client_code=ss_1_client['code'],
                                                               client_class=ss_1_client['class'])(self)
        self.log('Log out and log in to central server')
        login_with_logout(self, cs_host, cs_username, cs_password)
        self.log('Add subsystem to client')
        add_sub_as_client_to_member(self, ss1_server_name, ss_1_client, wait_input=wait_input,
                                    step='Adding subsystem')

        self.log('Approve the registration requests')
        approve_requests(self, '2.2.1-5 ', cancel_confirmation=False)

    return setup_member_with_subsystem
