from selenium.webdriver.common.by import By
from view_models import sidebar, popups, ss_system_parameters, messages, log_constants
from helpers import auditchecker, ssh_client, xroad
import time
import os
from shutil import copyfile


def test_ss_backup_conf(case, ssh_host=None, ssh_username=None, ssh_password=None):
    '''
    UC SS 15 Try to backup confiuration file and verify it form audit log

    :param case: MainController object
    :param ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param ssh_username: str|None SSH username
    :param ssh_password: str|None SSH password
    :return:
    '''
    self = case

    def backup_conf():

        self.logdata = []

        if ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_username, password=ssh_password)
            current_log_lines = log_checker.get_line_count()

        '''Add "Back up configuration failed" to comparision variable'''
        self.logdata.append(log_constants.SS_BACKUP_CONFIGURATION_FAILED)

        '''Write file to ss2 to cause error message'''
        create_empty_file = 'sh -c "echo \'\' > {0}"'.format(ss_system_parameters.BACKUP_CORRUPTION_FILE)
        self.log('Connecting ssh client')
        self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)

        self.ssh_client.exec_command(command=create_empty_file, sudo=True)
        change_file_permissions = 'chmod o-r {0}'.format(ss_system_parameters.BACKUP_CORRUPTION_FILE)
        self.ssh_client.exec_command(command=change_file_permissions, sudo=True)

        '''Click "Back Up and Restore" button'''
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.BACKUP_AND_RESTORE_BTN_CSS).click()
        self.wait_jquery()

        '''Click on "Back up configuration" button'''

        self.log('SS administrator selects to back up the security server configuration.')
        self.wait_until_visible(self.by_id(ss_system_parameters.BACKUP_CONFIGURATION_BUTTON_ID)).click()
        self.wait_jquery()

        self.log('System displays the error message.')

        '''Save message error message'''
        error_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text

        '''Verify error message'''
        self.is_true(error_message == messages.SS_CONFIGURATION_BACKUP_ERROR,
                     msg='Wrong error message')

        '''Remove empty file for making successful test'''
        remove_file = 'rm {0}'.format(ss_system_parameters.BACKUP_CORRUPTION_FILE)
        self.ssh_client.exec_command(command=remove_file, sudo=True)

        '''Close Backup Script backup popup'''
        popups.close_console_output_dialog(self)

        '''Check audit log'''
        if ssh_host is not None:
            # Check logs for entries
            self.log(
                'System logs the event "Back up configuration failed" to the audit log')
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))

        '''Reload page and wait until additional data is loaded using jQuery'''
        self.driver.refresh()
        self.wait_jquery()

        '''Click "Delete"'''
        self.by_xpath(ss_system_parameters.DELETE).click()

        '''Confirm delete'''
        popups.confirm_dialog_click(self)

        '''Save delete message'''
        success_deletion = messages.get_notice_message(self)

        '''Verify successful delete'''
        self.is_true(success_deletion == messages.SS_SUCCESSFUL_DELETE,
                     msg='Wrong message for deleted backup')

        self.logdata = []

        if ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_username, password=ssh_password)
            current_log_lines = log_checker.get_line_count()

        '''Click "Back Up and Restore" button'''
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.BACKUP_AND_RESTORE_BTN_CSS).click()
        self.wait_jquery()

        self.log('SS administrator selects to back up the security server configuration.')
        '''Click on "Back up configuration" button'''
        self.wait_until_visible(self.by_id(ss_system_parameters.BACKUP_CONFIGURATION_BUTTON_ID)).click()
        self.wait_jquery()

        '''Save message "Configuration backup created"'''
        success_notice = messages.get_notice_message(self)

        self.log('Verify 2a, 2b, 2c')

        '''Verify correct error message'''
        self.is_true(error_message == messages.SS_CONFIGURATION_BACKUP_ERROR,
                     msg='Wrong error message')

        self.logdata.append(log_constants.SS_BACKUP_CONFIGURATION)

        '''Save "Backup Script Output" message'''
        backup_script_output = messages.get_console_output(self)

        '''Verify dump file location /var/lib/xroad/dbdump.dat '''
        self.is_true(ss_system_parameters.BACKUP_DUMP_LOCATION in backup_script_output,
                     msg='Dump /var/lib/xroad/dbdump.dat not found')

        '''Verify dump file location /etc/xroad/ '''
        self.is_true(ss_system_parameters.BACKUP_DUMP_DIR1 in backup_script_output,
                     msg='Dump directory /etc/xroad/ not found')

        '''Verify dump file location /etc/nginx/sites-enabled/ '''
        self.is_true(ss_system_parameters.BACKUP_DUMP_DIR2 in backup_script_output,
                     msg='Dump directory /etc/nginx/sites-enabled/ not found')

        '''Verify dump file label information '''
        self.is_true(ss_system_parameters.BACKUP_DUMP_VER in backup_script_output,
                     msg='Dump contains different label information')

        self.log('Configuration backup created')
        '''Verify "Configuration backup created"'''
        self.is_true(success_notice == log_constants.SS_BACKUP_SCRIPT_CREATED,
                     msg='Wrong error message')

        if ssh_host is not None:
            # Check logs for entries
            self.log(
                'System logs the event "Back up configuration" to the audit log')
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))
        '''Close Backup Script backup popup'''
        popups.close_console_output_dialog(self)

    return backup_conf


def test_ss_backup_download(case):
    '''
    UC SS 16 Try to download backup file and verify it form local location
    :param case: MainController object
    :return:
    '''
    self = case

    def backup_conf():
        '''Click "Back Up and Restore" button" '''
        self.log('Click "Back Up and Restore" button"')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.BACKUP_AND_RESTORE_BTN_CSS).click()
        self.wait_jquery()

        '''Name of backup file'''
        backup_conf_file_name = self.by_css(ss_system_parameters.BACKUP_FILE_NAME).text

        '''Click "Download"'''
        self.log('Click "Download"')
        self.by_xpath(ss_system_parameters.DOWNLOAD).click()
        self.wait_jquery()

        '''Wait for donwload to be completed'''
        time.sleep(7)

        '''Downloaded backup file location'''
        local_path = self.get_download_path(backup_conf_file_name)
        print local_path
        '''Verify that backup file is downloaded'''
        self.log('Verify that backup file is downloaded')
        if not os.path.isfile(local_path):
            raise RuntimeWarning('Backup file not found: {0}'.format(local_path))

    return backup_conf


def test_ss_backup_delete(case, ssh_host=None, ssh_username=None, ssh_password=None):
    '''
    UC SS 17 Try to delete backup file and verify deletion from audit log
    :param case: MainController object
    :param ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param ssh_username: str|None SSH username
    :param ssh_password: str|None SSH password
    :return:
    '''

    self = case

    def backup_delete():

        self.logdata = []

        if ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_username, password=ssh_password)
            current_log_lines = log_checker.get_line_count()

        '''Click "Back Up and Restore" button" '''
        self.log('Click "Back Up and Restore" button"')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.BACKUP_AND_RESTORE_BTN_CSS).click()
        self.wait_jquery()

        '''Name of backup file'''
        backup_conf_file_name = self.by_css(ss_system_parameters.BACKUP_FILE_NAME).text

        '''Click "Delete"'''
        self.log('Click "Delete"')
        self.by_xpath(ss_system_parameters.DELETE).click()
        self.wait_jquery()

        '''Confirm delete, click cancel button on popup'''
        self.by_xpath(popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()

        delete_backup_conf(self)

        '''Check audit log'''
        if ssh_host is not None:
            # Check logs for entries
            self.log(
                'System logs the event "Delete backup file" to the audit log')
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))
        else:
            raise RuntimeError('Not able to check audit log!')

    return backup_delete


def test_ss_upload_backup(case, ssh_host=None, ssh_username=None, ssh_password=None):
    '''
    UC SS 18 Try to upload backup file and verify successful upload from audit log

    :param case: MainController object
    :param ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param ssh_username: str|None SSH username
    :param ssh_password: str|None SSH password
    :return:
    '''
    self = case

    def backup_conf():

        self.logdata = []

        if ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_username, password=ssh_password)
            current_log_lines = log_checker.get_line_count()

        '''Click "Back Up and Restore" button'''
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.BACKUP_AND_RESTORE_BTN_CSS).click()
        self.wait_jquery()

        '''Name of backup file'''
        backup_conf_file_name = self.by_css(ss_system_parameters.BACKUP_FILE_NAME).text

        '''Click "Download"'''
        self.log('Click "Download"')
        self.by_xpath(ss_system_parameters.DOWNLOAD).click()
        self.wait_jquery()

        '''Wait for donwload to be completed'''
        time.sleep(7)

        '''Path of downloaded file'''
        local_path = self.get_download_path(backup_conf_file_name)

        '''Verify that backup file is downloaded'''
        self.log('Verify that backup file is downloaded')
        if not os.path.isfile(local_path):
            raise RuntimeWarning('Backup file not found: {0}'.format(local_path))

        '''Create invalid character path'''
        invalid_char_dst = self.download_dir + '\\' + ss_system_parameters.INVALID_CHARACTER_FILE

        '''Create copy of real backup file and name it as invalid character file'''
        copyfile(local_path, invalid_char_dst)

        '''Path of invalid extension file'''
        invalid_extension_dst = os.path.join(self.download_dir + '\\' + ss_system_parameters.EMPTY_ZIP_FILE)
        # os.rename(local_path, invalid_extension_dst)
        copyfile(local_path, invalid_extension_dst)

        '''Path of invalid .tar file'''
        invalid_format = self.get_download_path(ss_system_parameters.EMPTY_TAR_FILE)

        check_inputs(self, invalid_char_dst, invalid_extension_dst, invalid_format)
        successful_reupload(self, local_path, backup_conf_file_name)
        successful_upload(self, local_path, backup_conf_file_name)

        print self.logdata
        if ssh_host is not None:
            # Check logs for entries
            self.log(
                'System logs the event "Back up configuration" to the audit log')
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)

            print log_checker.found_lines

            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))

    return backup_conf


def test_view_list_backup_files(case):
    """
    SS 13  View the List of Configuration Backup Files
    :param case: MainController object
    :return:
    """
    self = case

    def test_case():
        """
        :param self: MainController object
        :return: None
        """

        '''UC SS_13 step 1. SS administrator selects to view the list of configuration backup files.'''
        self.log('''UC SS_13 step 1. SS administrator selects to view the list of configuration backup files.''')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.BACKUP_AND_RESTORE_BTN_CSS).click()
        self.wait_jquery()

        '''UC SS_13 step 2. System displays the list of backup files. For each file, the following information 
        is displayed:'''
        self.log('''UC SS_13 step 2. System displays the list of backup files. For each file, the following information 
        is displayed:''')
        list_of_backup_files = self.wait_until_visible(type=By.XPATH,
                                                       element=ss_system_parameters.BACKUP_FILE_NAME_ROW, multiple=True)

        '''UC SS_13 2.1 The file name of the backup file'''
        backup_file_name_displayed = False
        for file_name in list_of_backup_files:
            file_name = file_name.text
            if len(str(file_name)) > 0:
                backup_file_name_displayed = True
            assert backup_file_name_displayed is True
            self.log('''UC SS_13 2.1 The file name of the backup file - {0} - is displayed'''.format(file_name))

    return test_case


def check_inputs(self, invalid_char_dst, invalid_extension_dst, invalid_format):
    '''
    :param self: MainController object
    :param invalid_char_dst: str | invalid characters file to upload
    :param invalid_extension_dst: str | invalid file extension to upload
    :param invalid_format: str | invalid file format to upload
    :return:
    '''
    error_count = 0
    success_count = 0

    URL_TEXT_AND_RESULTS = [
        [invalid_char_dst,
         messages.UPLOAD_CONTAIN_INVALID_CHARACTERS.format(ss_system_parameters.INVALID_CHARACTER_FILE), False],
        [invalid_extension_dst, messages.UPLOAD_WRONG_EXTENSION.format(ss_system_parameters.EMPTY_ZIP_FILE), False],
        [invalid_format, messages.UPLOAD_WRONG_FORMAT, False]
    ]

    local_file_location = [invalid_char_dst, invalid_extension_dst, invalid_format]
    # Loop through different key label names and expected results
    counter = 1

    '''Click on "Upload backup file" button'''
    self.wait_until_visible(self.by_id(ss_system_parameters.BACKUP_UPLOAD_BUTTON_ID)).click()
    self.wait_jquery()

    file_upload_btn = self.wait_until_visible(self.by_id(popups.FILE_UPLOAD_BROWSE_BUTTON_ID))

    for location in range(len(local_file_location)):

        input_text = URL_TEXT_AND_RESULTS[location][0]
        error_message = URL_TEXT_AND_RESULTS[location][1]
        error = error_message is not None

        '''Create upload file'''
        xroad.fill_upload_input(self, file_upload_btn, local_file_location[location])

        '''Click "OK" button'''
        self.by_id(popups.FILE_UPLOAD_SUBMIT_BUTTON_ID).click()
        self.wait_jquery()
        '''Wait for message to be visible'''
        time.sleep(2.5)

        ui_error = messages.get_error_message(self)
        self.logdata.append(ss_system_parameters.UPLOAD_BACKUP_FAILED)

        '''Expecting error'''
        if error:
            if ui_error is not None:
                error_count += 1
                self.is_equal(ui_error, error_message, msg='Wrong error message, expected: {0}'.format(error_message))
            else:
                raise RuntimeError('Not able to verify error messages')
        else:
            self.is_none(ui_error, msg='Got error message for: "{0}"'.format(input_text))

            success_count += 1
        counter += 1

        self.wait_jquery()
    return success_count, error_count, self.logdata


def successful_reupload(self, local_path, backup_conf_file_name):

    file_upload_btn = self.wait_until_visible(self.by_id(popups.FILE_UPLOAD_BROWSE_BUTTON_ID))
    self.wait_jquery()

    '''Create upload file'''
    xroad.fill_upload_input(self, file_upload_btn, local_path)

    '''Click "OK" button'''
    self.by_id(popups.FILE_UPLOAD_SUBMIT_BUTTON_ID).click()
    self.wait_jquery()
    '''Wait for message to be visible'''
    existing_message = self.wait_until_visible(ss_system_parameters.SS_UPDATE_CONFRIM, By.XPATH).text

    '''Verify configuration message'''
    self.is_true(existing_message == messages.UPLOAD_EXISTS.format(backup_conf_file_name),
                 msg='Wrong message for existing file')

    self.wait_until_visible(type=By.XPATH, element=ss_system_parameters.SELECT_CLIENT_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
    time.sleep(3)

    '''Save message "New backup file uploaded successfully"'''
    notice = messages.get_notice_message(self)

    '''Add successful file uplaod to logdata'''
    self.logdata.append(ss_system_parameters.UPLOAD_BACKUP_SUCCESSFUL)

    return self.logdata


def delete_backup_conf(self):
    '''Click "Delete"'''
    self.log('Click "Delete"')
    self.by_xpath(ss_system_parameters.DELETE).click()
    self.wait_jquery()

    '''Confirm delete'''
    popups.confirm_dialog_click(self)
    self.wait_jquery()

    '''Save delete message'''
    success_deletion = messages.get_notice_message(self)
    '''Verify successful delete'''
    self.is_true(success_deletion == messages.SS_SUCCESSFUL_DELETE,
                 msg='Wrong message for deleted backup')
    self.logdata.append(log_constants.SS_BACKUP_FILE_DELETE)


def successful_upload(self, local_path, backup_conf_file_name):
    '''Delete current backup flle'''
    delete_backup_conf(self)

    '''Click on "Upload backup file" button'''
    self.wait_until_visible(self.by_id(ss_system_parameters.BACKUP_UPLOAD_BUTTON_ID)).click()
    self.wait_jquery()

    file_upload_btn = self.wait_until_visible(self.by_id(popups.FILE_UPLOAD_BROWSE_BUTTON_ID))
    self.wait_jquery()

    '''Create upload file'''
    xroad.fill_upload_input(self, file_upload_btn, local_path)

    '''Click "OK" button'''
    self.by_id(popups.FILE_UPLOAD_SUBMIT_BUTTON_ID).click()
    self.wait_jquery()
    time.sleep(2.5)
    '''Save message "New backup file uploaded successfully"'''
    successful_upload = messages.get_notice_message(self)
    '''Verify successful upload'''
    self.is_true(successful_upload == log_constants.SS_BACKUP_NEW_FILE_UPLOAD,
                 msg='Wrong message for backup upload')

    '''Add successful file uplaod to logdata'''
    self.logdata.append(ss_system_parameters.UPLOAD_BACKUP_SUCCESSFUL)

    return self.logdata
