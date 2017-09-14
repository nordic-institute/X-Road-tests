import time
from datetime import datetime

from selenium.webdriver.common.by import By

from helpers import ssh_server_actions, ssh_user_actions
from view_models import members_table, sidebar, groups_table, popups, messages, log_constants, \
    sidebar as sidebar_constants
from view_models.log_constants import *
import tests.xroad_parse_users_input_SS_41.parse_user_input_SS_41 as user_input_check
from helpers import auditchecker

USERNAME = 'username'
PASSWORD = 'password'

test_name = 'GLOBAL GROUP USER INPUTS TESTS'


def test_test(ssh_host, ssh_username, ssh_password, users, group, check_global_groups_inputs=False, cs_ssh_host=None,
              cs_ssh_user=None, cs_ssh_pass=None):
    """
    MainController test function. Tests maintentance actions and logging in central server.
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH username
    :param ssh_password: str - SSH password
    :param users: dict - dictionary of users to be added
    :param group: str - group name
    :param check_global_groups_inputs: bool - condition for user inputs
    :param cs_ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param cs_ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param cs_ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :return:
    """

    def test_case(self):

        """EST PLAN SERVICE_32 3, 3a, 4a, 6 """
        self.log('*** SERVICE_32 3, 3a, 4a, 6 / XTKB-37')

        '''Save users to MainController'''
        self.users = users

        '''Get the first user'''
        user = users['user1']

        '''Create SSH session'''
        ssh_client = ssh_server_actions.get_client(ssh_host, ssh_username, ssh_password)
        self.log('Adding users to system')

        '''By default, there is no error.'''
        error = False

        try:
            # TEST PLAN 2.11.1-1 log in to central server UI as user1
            self.log('2.11.1-1 logging in to central server as user1')
            check_login(self, ssh_client, None, users['user1'])

            # TEST PLAN 2.11.1-7, 2.11.1-8 add new group (failure and success test)
            self.log('2.11.1-7, 2.11.1-8 add new group (failure and success test)')
            add_group(self, ssh_client, user, group, check_global_groups_inputs=check_global_groups_inputs,
                      cs_ssh_host=cs_ssh_host, cs_ssh_user=cs_ssh_user, cs_ssh_pass=cs_ssh_pass)

        finally:
            try:
                self.log('2.11.1-del Deleting group')
                remove_group(self, group)
            except:
                self.log('2.11.1-del Deleting group failed')
            self.log('2.11.1-del closing SSH connection')
            ssh_client.close()
            if error:
                # Got an error before, fail the test
                assert False, '2.11.1 failed'

    return test_case


def add_group(self, ssh_client, user, group, check_global_groups_inputs=False, cs_ssh_host=None, cs_ssh_user=None,
              cs_ssh_pass=None):
    """
    Adds a new global group to the system. First tries to add with empty values, then with the correct ones.
    Checks if the action was logged.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param group: str - group name
    :param check_global_groups_inputs bool - condition to check user inputs or not
    :param cs_ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param cs_ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param cs_ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :return: None
    """

    def enter_global_group_data():
        """
        :return: None
        """
        # Start adding new group
        self.log('Click "ADD" to add new group')
        self.wait_until_visible(type=By.ID, element=groups_table.ADD_GROUP_BTN_ID).click()

        # TEST PLAN 2.11.1-8 fill in required fields and try again
        self.log('2.11.1-8 add new group, fill in required fields')
        self.log('Send {0} to code area input'.format(group))
        group_code_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_CODE_AREA_ID)
        self.input(group_code_input, group)
        self.log('Send {0} to code description input'.format(group))
        group_description_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_DESCRIPTION_AREA_ID)
        self.input(group_description_input, group)

    if check_global_groups_inputs:
        '''SERVICE_32 step 3 System verifies global groups inputs in the central server'''

        # TEST PLAN SERVICE_32 step 3 System verifies global groups inputs in the central server
        self.log('*** SERVICE_33_3 / XTKB-56')
        # Open global groups
        self.log('Open Global Groups tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.GLOBAL_GROUPS_CSS).click()
        self.wait_jquery()

        # Loop through data from the groups_table.py
        counter = 1
        for group_data in groups_table.GROUP_DATA:
            # Set necessary parameters
            code = group_data[0]
            description = group_data[1]
            error = group_data[2]
            error_message = group_data[3]
            error_message_label = group_data[4]
            whitespaces = group_data[5]

            # Start adding new group
            enter_global_group(self, code, description, cs_ssh_host=cs_ssh_host, cs_ssh_user=cs_ssh_user,
                               cs_ssh_pass=cs_ssh_pass)

            # Verify group code and description
            parse_user_input(self, error, error_message, error_message_label)

            if error:
                # Close a pop-up window , if there is a error message
                self.log('Click on "Cancel" button')
                self.wait_until_visible(type=By.XPATH,
                                        element=groups_table.NEW_GROUP_POPUP_CANCEL_BTN_XPATH).click()
                self.wait_jquery()
            else:
                # Verify that the added global group code exists
                self.log('Find added code text - ' + code.strip())
                global_croup_code = self.wait_until_visible(type=By.XPATH,
                                                            element=groups_table.
                                                            get_clobal_group_code_description_by_text(code.strip()))
                global_croup_code = global_croup_code.text
                # Verify that the added global group description exists
                self.log('Find added description text - ' + description.strip())
                global_croup_description = self.wait_until_visible(type=By.XPATH,
                                                                   element=groups_table.
                                                                   get_clobal_group_code_description_by_text(
                                                                       description.strip()))
                global_croup_description = global_croup_description.text
                self.log('Found global group code - ' + code)
                self.log('Found global group description - ' + description)

                if whitespaces:
                    find_text_with_whitespaces(self, code, global_croup_code)
                    find_text_with_whitespaces(self, description, global_croup_description)
                else:
                    assert code in global_croup_code
                    assert description in global_croup_description

                # Delete added global group
                delete_global_group(self, code)

            counter += 1

        '''SERVICE_32 step 4a insert a group code that already exists'''

        '''Start adding new group'''
        enter_global_group_data()
        self.log('Click on "OK" to add new group')
        self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        '''Start adding new group with same code, that already exists'''
        enter_global_group_data()
        self.log('Click on "CANCEL" to terminate the use case')
        self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_CANCEL_BTN_XPATH).click()
        self.wait_jquery()

        '''Start adding new group with same code, that already exists, one more time'''
        enter_global_group_data()

        '''We're looking for "Add global group failed" log'''
        self.logdata = [log_constants.ADD_GLOBAL_GROUP_FAILED]

        if cs_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
            current_log_lines = log_checker.get_line_count()

        self.log('Click on "OK" to add new group')
        self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        '''Check error message'''
        user_input_check.parse_user_input(self, True, messages.GLOBAL_GROUP_ALREADY_TAKEN, group)
        self.log('Click on "CANCEL" to terminate the use case')
        self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_CANCEL_BTN_XPATH).click()
        self.wait_jquery()

        '''We're looking for "Add global group failed" log'''
        if cs_ssh_host is not None:
            '''Check logs for entries'''
            self.log('SERVICE_32 6 - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.
                         format(self.logdata, log_checker.found_lines))

        '''Delete added global group'''
        user_input_check.delete_global_group(self, group)

    self.log('Open Global Groups tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
    self.wait_jquery()

    '''We're looking for "Add global group" log'''
    self.logdata = [log_constants.ADD_GLOBAL_GROUP]

    if cs_ssh_host is not None:
        log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
        current_log_lines = log_checker.get_line_count()

    enter_global_group_data()

    self.log('Click on "OK" to add new group')
    self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    if cs_ssh_host is not None:
        '''Check logs for entries'''
        self.log('SERVICE_32 6 - checking logs for: {0}'.format(self.logdata))
        logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                               log_checker.found_lines))

    # TEST PLAN 2.11.1-14 check if adding group actions have been logged
    bool_value, data, date_time = check_logs_for(ssh_client, ADD_GLOBAL_GROUP, user[USERNAME])
    self.is_true(bool_value, test_name,
                 '2.11.1-8/2.11.1-14 log check for added group - check failed',
                 '2.11.1-8/2.11.1-14 log check for added group')


def remove_group(self, group):
    """
    Removes a global group from the system.
    :param self: MainController object
    :param group: str - group name
    :return: None
    """
    # Open global groups
    self.log('Open Global Groups tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
    self.wait_jquery()

    # Find and select the group
    self.log('Select added group')
    table = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_TABLE_ID)
    rows = table.find_elements_by_tag_name('tr')
    for row in rows:
        if row.text != '':
            if row.find_element_by_tag_name('td').text == group:
                row.click()
                self.wait_jquery()

    # Open group details and delete the group
    self.log('Open group details')
    self.wait_until_visible(type=By.ID, element=groups_table.GROUP_DETAILS_BTN_ID).click()
    self.wait_jquery()
    self.log('Click on "DELETE GROUP" button')
    self.wait_until_visible(type=By.XPATH, element=groups_table.DELETE_GROUP_BTN_ID).click()
    self.wait_jquery()
    self.log('Confirm deletion')
    popups.confirm_dialog_click(self)


def delete_client(self, ssh_client, user, member):
    """
    Deletes a member from the system. Checks if the action was logged.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param member: dict - member data
    :return: None
    """
    self.driver.get(self.url)
    self.wait_jquery()
    # Open member details
    open_member_details(self, member=member)
    # Delete the member
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()
    self.wait_jquery()
    # Confirm deletion
    popups.confirm_dialog_click(self)
    time.sleep(10)

    # TEST PLAN 2.11.1-13/2.11.1-14 check if deleting the member was logged
    bool_value, data, date_time = check_logs_for(ssh_client, DELETE_MEMBER, user[USERNAME])
    self.is_true(bool_value, test_name,
                 '2.11.1-13/2.11.1-14 log check for deleting the member - check failed',
                 '2.11.1-13/2.11.1-14 log check for deleting the member')


def add_users_to_system(self, ssh_client):
    """
    Adds test users to system over SSH connection.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :return:
    """
    user = self.users['user1']
    ssh_user_actions.add_user(client=ssh_client, username=user[USERNAME], password=user[PASSWORD],
                              group=user['group'])
    user = self.users['user2']
    ssh_user_actions.add_user(client=ssh_client, username=user[USERNAME], password=user[PASSWORD],
                              group=user['group'])
    user = self.users['user3']
    ssh_user_actions.add_user(client=ssh_client, username=user[USERNAME], password=user[PASSWORD],
                              group=user['group'])


def check_login(self, ssh_client, logout_user=None, login_user=None):
    """
    Login function that also checks if it succeeded. If specified, first logs the user out from existing session.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param logout_user: dict|None - user data for user that should be logged out; None if logout is not necessary
    :param login_user: dict|None - user data for user logging in; None if login not necessary
    :return: None
    """
    # TEST PLAN 2.11.1-14 login and logout checks (all users)

    if logout_user is not None:
        self.log('Checking logout')
        self.logout()

        # Check logs
        bool_value, data, date_time = check_logs_for(ssh_client, LOGOUT, logout_user[USERNAME])
        self.is_true(bool_value, test_name,
                     'Log check for logging out - check failed', 'Log check for logging out',
                     )
    if login_user is not None:
        self.log('Checking login')
        if logout_user is None:
            # Log out the previous user if not yet logged out
            self.logout()

        # Log in the new user
        self.login(login_user[USERNAME], login_user[PASSWORD])

        # Check logs
        bool_value, data, date_time = check_logs_for(ssh_client=ssh_client, event=LOGIN, user=login_user[USERNAME])
        self.is_true(bool_value, test_name,
                     'Log check for logging in - check failed',
                     'Log check for logging in')


def check_logs_for(ssh_client, event, user):
    """
    Checks if an event for user was logged in the system.
    :param ssh_client: SSHClient object
    :param event: str - event to look for in the logs
    :param user: str - username to look for in the logs
    :return: bool - True if event was logged; False otherwise
    """
    print 'Checking logs for {0}'.format(event)
    # Wait 15 seconds for sync
    time.sleep(15)
    log = ssh_server_actions.get_log_lines(ssh_client, LOG_FILE_LOCATION, 1)
    date_time = datetime.strptime(' '.join([log['date'], log['time']]), "%Y-%m-%d %H:%M:%S")
    datetime.strptime(datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S.000000"), '%Y-%m-%d %H:%M:%S.%f')
    return (str(log['msg_service']) == MSG_SERVICE_CENTER) & (str(log['data']['event']) == event) & \
           (str(log['data']['user']) == user), log['data'], date_time


def open_member_details(self, member):
    """
    Opens member details in the user interface.
    :param self: MainController object
    :param member: dict - member data
    :return: None
    """
    self.wait_jquery()
    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    self.wait_jquery()
    row = members_table.get_row_by_columns(table, [member['name'], member['class'], member['code']])
    if row is None:
        self.log('Member not found')
        pass
    '''Click the row. Raises an exception if member was not found. This can be caught outside of this function if 
    necessary.'''
    row.click()
    self.wait_jquery()
    self.log('Open Member Details')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.wait_jquery()


def enter_global_group(self, code, description, cs_ssh_host=None, cs_ssh_user=None,
                       cs_ssh_pass=None):
    """
    :param self: MainController object
    :param code: str - Group code
    :param description: str - Group description
    :param cs_ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param cs_ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param cs_ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :return:
    """
    self.wait_jquery()
    # Start adding new group
    self.log('Click "ADD" to add new group')
    self.wait_until_visible(type=By.ID, element=groups_table.ADD_GROUP_BTN_ID).click()

    # Add new group
    self.log('2.11.1-8 add new group, fill in required fields')
    self.log('Send {0} to code area input'.format(code))
    group_code_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_CODE_AREA_ID)
    self.input(group_code_input, code)
    self.log('Send {0} to code description input'.format(description))
    group_description_input = self.wait_until_visible(type=By.ID, element=groups_table.
                                                      GROUP_DESCRIPTION_AREA_ID)
    self.input(group_description_input, description)

    '''We're looking for "Add global group failed" log'''
    self.logdata = [log_constants.ADD_GLOBAL_GROUP_FAILED]
    if cs_ssh_host is not None:
        log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user,
                                                password=cs_ssh_pass)
        current_log_lines = log_checker.get_line_count()

    self.log('Click on "OK" to add new group')
    self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    try:
        '''We're looking for "Add global group failed" log'''
        if cs_ssh_host is not None:
            '''Check logs for entries'''
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.
                         format(self.logdata, log_checker.found_lines))
            self.log('SERVICE_32 6 - checking logs for: {0}'.format(self.logdata))
    except:
        pass


def parse_user_input(self, error, error_message, error_message_label):
    """
    Function Check for the error messages
    :param self: MainController object
    :param error: bool - Must there be a error message, True if there is and False if not
    :param error_message: str - Expected error message
    :param error_message_label: str - label for a expected error message
    :return:
    """
    if error:
        # Get a error message, compare it with expected error message and close error message

        self.log('Get the error message')
        self.wait_jquery()
        get_error_message = messages.get_error_message(self)
        self.log('Found error message - ' + get_error_message)
        self.log('Expected error message  - ' + error_message.format(error_message_label))

        self.log('Compare error message to the expected error message')
        assert get_error_message in error_message.format(error_message_label)

        self.log('Close the error message')
        messages.close_error_messages(self)
    else:
        # Verify that there is not error messages
        self.log('Verify that there is not error messages')
        get_error_message = messages.get_error_message(self)
        if get_error_message is None:
            error = False
        else:
            error = True
        assert error is False


def delete_global_group(self, code):
    """
    :param self: MainController object
    :param code: str - Group code
    :return:
    """
    # Delete added global group
    self.log('Delete added global group')
    self.log('Click on added global group row')
    self.wait_until_visible(type=By.XPATH, element=groups_table.
                            get_clobal_group_code_description_by_text(code.strip())).click()
    self.log('Click on "DETAILS" button')
    self.wait_until_visible(type=By.ID,
                            element=groups_table.GROUP_DETAILS_BTN_ID).click()
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.XPATH,
                            element=groups_table.DELETE_GROUP_BTN_ID).click()
    self.log('Click on "CONFIRM" button')
    popups.confirm_dialog_click(self)


def find_text_with_whitespaces(self, added_text, expected_text):
    """
    Verifies, that there is not inputs with whitespaces
    :param self: MainController object
    :param added_text: str - added text
    :param expected_text: str - expected text
    :return: None
    """
    try:
        # Compare added text with whitespaces and displayed text
        self.log('Compare added text with whitespaces and displayed text')
        self.log("'" + added_text + "' != '" + expected_text + "'")
        assert added_text in expected_text
        whitespace = True
    except:
        # Compare added text without whitespaces and displayed text
        self.log('Compare added text without whitespaces and displayed text')
        self.log("'" + added_text.strip() + "' == '" + expected_text + "'")
        assert added_text.strip() in expected_text
        whitespace = False
    assert whitespace is False
