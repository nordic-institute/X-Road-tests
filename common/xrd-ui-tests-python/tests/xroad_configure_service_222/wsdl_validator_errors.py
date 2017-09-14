import time

import requests
from selenium.webdriver.common.by import By

from helpers import ssh_client, auditchecker
from tests.xroad_configure_service_222 import configure_service_2_2_2
from tests.xroad_refresh_wsdl_225 import refresh_wsdl_2_2_5
from tests.xroad_refresh_wsdl_225.refresh_wsdl_2_2_5 import webserver_set_wsdl
from view_models import clients_table_vm, popups, messages, ss_system_parameters, log_constants


def test_wsdl_validator_crash(case, wsdl_url, ssh_host, ssh_username, ssh_password, ss_host, ss_user, ss_pass,
                              client_name, client_id, wsdl_validator_wrapper_path):
    self = case

    def wsdl_validator_crash():
        '''Security server ssh client instance'''
        self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
        self.log('Backing up wsdlvalidator wrapper')
        self.ssh_client.exec_command('cp {0} {0}.backup'.format(wsdl_validator_wrapper_path), sudo=True)
        self.log('Adding invalid argument(asd) to wsdlvalidator_wrapper to execution command')
        self.ssh_client.exec_command('sed -i -e "s/-r/-asd/g" {0}'.format(wsdl_validator_wrapper_path), sudo=True)
        self.ssh_client.close()

        self.log('Opening security server homepage')
        self.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
        self.log('Open client services tab')
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)
        self.log('Try to add wsdl')
        warning, error, console = configure_service_2_2_2.add_wsdl(self, wsdl_url=wsdl_url)
        self.log('Check if wsdl validation error is correct')
        self.is_equal(error, messages.WSDL_ERROR_VALIDATION_FAILED.format(wsdl_url),
                      msg='Validation failed error message not correct')
        self.log('Check if wsdl validation error popup contains expected strings')
        self.is_true("WSDLValidator Error" and "Unexpected argument" in console)

    return wsdl_validator_crash


def test_wsdl_validator_not_set(case, wsdl_url, wsdl_warning, wsdl_filename, wsdl_error, wsdl_local_path, ss_host, ss_user, ss_pass,
                                client_name, client_id, ssh_host, ssh_username, ssh_password):
    self = case

    def test_success_no_wsdl_validator():
        self.log('Server has finished reloading, starting browser')
        self.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
        '''Security server ssh client instance'''
        self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
        self.log('Set testservice wsdl to wsdl, which with validator gives warning')
        webserver_set_wsdl(self, wsdl_source_filename=wsdl_local_path.format(wsdl_warning),
                           wsdl_target_filename=wsdl_local_path.format(wsdl_filename))
        self.log('Open client services tab')
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        '''SERVICE_08 Adding wsdl(6a) when wsdl validator is not set, wsdl will not be checked'''
        self.log('SERVICE_08 Adding wsdl(6a) when wsdl validator is not set, wsdl will not be checked')
        self.log('Try to add wsdl, which gives warning with wsdl validator')
        warning, error, console = configure_service_2_2_2.add_wsdl(self, wsdl_url=wsdl_url)
        self.log('Check if wsdl was added successfully')
        self.is_none(warning)
        self.is_none(error)
        self.is_none(console)
        self.log('Check if wsdl is visible in services table')
        self.is_not_none(clients_table_vm.find_wsdl_by_name(self, wsdl_url))
        self.log('Set testservice wsdl to wsdl, which with validator gives error')
        webserver_set_wsdl(self, wsdl_source_filename=wsdl_local_path.format(wsdl_error),
                           wsdl_target_filename=wsdl_local_path.format(wsdl_filename))
        self.log('Close ssh client')
        self.ssh_client.close()
        self.log('Select added wsdl from table')
        clients_table_vm.client_services_popup_select_wsdl(self, wsdl_url=wsdl_url)

        '''SERVICE_14 Refreshing wsdl(3a) when wsdl validator is not set, wsdl will not be checked'''
        self.log('SERVICE_14 Refreshing wsdl(3a) when wsdl validator is not set, wsdl will not be checked')
        self.log('Refresh added wsdl')
        warning, error, console = refresh_wsdl_2_2_5.refresh_wsdl(self)
        self.log('Check if wsdl was refreshed successfully')
        self.is_none(warning)
        self.is_none(error)
        self.is_none(console)

    return test_success_no_wsdl_validator


def remove_wsdl_validator_from_conf(self, ssh_host, ssh_username, ssh_password, ss_host):
    '''Command to backup local.ini to local.ini.backup file'''
    backup_local_ini_command = 'cp {0} {1}'.format(ss_system_parameters.WSDL_VALIDATOR_CONF_LOCATION,
                                                   '/etc/xroad/conf.d/local.ini.backup')
    '''Command to create empty local.ini file'''
    create_empty_local_ini_command = 'sh -c "echo \'\' > {0}"'.format(
        ss_system_parameters.WSDL_VALIDATOR_CONF_LOCATION)
    self.log('Connecting ssh client')
    self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
    self.log('Creating backup from local.ini')
    self.ssh_client.exec_command(command=backup_local_ini_command, sudo=True)
    self.log('Create empty local.ini file, so WSDL parser path is not set')
    self.ssh_client.exec_command(command=create_empty_local_ini_command, sudo=True)

    self.log('Reload application config')
    self.ssh_client.exec_command(command=ss_system_parameters.RELOAD_APP_COMMAND, sudo=True)
    self.log('Waiting until server has fully reloaded')
    wait_until_server_up(ss_host)


def test_wsdl_validator_invalid_command(case, wsdl_url, ss_host,
                                        ss_user, ss_pass, ss_ssh_host, ss_ssh_user, ss_ssh_pass,
                                        client_name, client_id, wsdl_warning_url):
    self = case

    def test_wsdl_validator_invalid_command_validation():
        self.log('Open ss page')
        self.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
        self.log('Open client services table')
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        log_checker = auditchecker.AuditChecker(host=ss_ssh_host, username=ss_ssh_user, password=ss_ssh_pass)
        current_log_lines = log_checker.get_line_count()
        '''SERVICE_08 Adding wsdl(6d) when wsdl validator is invalid command, error is displayed'''
        self.log('SERVICE_08 Adding wsdl(6d) when wsdl validator is invalid command, error is displayed')
        self.log('Trying to add wsdl to client')
        warning, error, console = configure_service_2_2_2.add_wsdl(self, wsdl_url=wsdl_warning_url)
        self.log('Check if command not found error exists')
        self.is_equal(messages.WSDL_ADD_ERROR_VALIDATOR_COMMAND_NOT_FOUND, error,
                      msg='WSDL Validator command not found error different from expected')
        logs_found = log_checker.check_log(log_constants.ADD_WSDL_FAILED, from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                         log_constants.ADD_WSDL_FAILED,
                         log_checker.found_lines))
        self.log('Cancel WSDL adding')
        self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_CANCEL_BTN_XPATH).click()
        self.log('Select wsdl which was added before')
        clients_table_vm.client_services_popup_select_wsdl(self, wsdl_url=wsdl_url)

        current_log_lines = log_checker.get_line_count()

        '''SERVICE_14 Refreshing wsdl(3d) when wsdl validator is invalid command, error is displayed'''
        self.log('SERVICE_14 Refreshing wsdl(3d) when wsdl validator is invalid command, error is displayed')
        warning, error, console = refresh_wsdl_2_2_5.refresh_wsdl(self)
        self.is_equal(messages.WSDL_REFRESH_ERROR_VALIDATOR_COMMAND_NOT_FOUND, error,
                      msg='WSDL Validator command not found error different from expected')

        logs_found = log_checker.check_log(log_constants.REFRESH_WSDL_FAILED, from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                         log_constants.REFRESH_WSDL_FAILED,
                         log_checker.found_lines))

    return test_wsdl_validator_invalid_command_validation


def set_wsdl_validator_invalid_command(self, ssh_host, ssh_username, ssh_password, ss_host):
    '''Command to create local.ini with not existing command'''
    create_not_existing_wsdl_validator_path_local_ini_command = 'sh -c "echo \'{0}\' > {1}"'.format(
        '\n[proxy-ui]\nwsdl-validator-command=randasd', ss_system_parameters.WSDL_VALIDATOR_CONF_LOCATION)
    self.log('Connecting ssh client')
    self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
    self.log('Creating local.ini with non-existing wsdl-validator command')
    self.ssh_client.exec_command(command=create_not_existing_wsdl_validator_path_local_ini_command, sudo=True)
    self.log('Reload application')
    self.ssh_client.exec_command(command=ss_system_parameters.RELOAD_APP_COMMAND, sudo=True)
    self.log('Wait until server up again')
    wait_until_server_up(ss_host)


def test_wsdl_validator_not_executable(case, wsdl_url, wsdl_warning_url, ss_host,
                                       ss_user, ss_pass, ss_ssh_host, ss_ssh_user, ss_ssh_pass,
                                       client_name, client_id):
    self = case

    def test_wsdl_validator_not_executable_warning():
        self.log('Open ss page')
        self.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
        self.log('Open client services tab')
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        '''SERVICE_08 Adding wsdl(6e) when wsdl validator is not executable, error is displayed'''
        self.log('SERVICE_08 Adding wsdl(6e) when wsdl validator is not executable, error is displayed')
        log_checker = auditchecker.AuditChecker(host=ss_ssh_host, username=ss_ssh_user, password=ss_ssh_pass)
        current_log_lines = log_checker.get_line_count()
        self.log('Try to add wsdl')
        warning, error, console = configure_service_2_2_2.add_wsdl(self, wsdl_url=wsdl_warning_url)
        self.log('Check if command not executable error exists')
        self.is_equal(messages.WSDL_ERROR_VALIDATOR_COMMAND_NOT_EXECUTABLE, error,
                      msg='WSDL Validator command not executable error different from expected')
        logs_found = log_checker.check_log(log_constants.ADD_WSDL_FAILED, from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                         log_constants.ADD_WSDL_FAILED,
                         log_checker.found_lines))
        self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_CANCEL_BTN_XPATH).click()
        clients_table_vm.client_services_popup_select_wsdl(self, wsdl_url=wsdl_url)
        current_log_lines = log_checker.get_line_count()

        '''SERVICE_14 Refreshing wsdl(3e) when wsdl validator is not executable, error is displayed'''
        self.log('SERVICE_14 Refreshing wsdl(3e) when wsdl validator is not executable, error is displayed')
        warning, error, console = refresh_wsdl_2_2_5.refresh_wsdl(self)
        self.is_equal(messages.WSDL_REFRESH_ERROR_VALIDATOR_COMMAND_NOT_EXECUTABLE, error,
                      msg='WSDL Validator command not executable error different from expected')
        logs_found = log_checker.check_log(log_constants.REFRESH_WSDL_FAILED, from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                         log_constants.REFRESH_WSDL_FAILED,
                         log_checker.found_lines))

    return test_wsdl_validator_not_executable_warning


def set_wsdl_validator_not_executable(self, ssh_host, ssh_username, ssh_password, ss_host, not_exec_file_path):
    '''Command to create not executable file'''
    create_not_exec_file_command = 'touch {0}'.format(not_exec_file_path)
    '''Set wsdl validator path to not executable file'''
    set_wsdl_validator_path_to_not_executable_file = 'sh -c "echo \'{0}\' > {1}"'.format(
        '\n[proxy-ui]\nwsdl-validator-command=/etc/xroad/conf.d/notExecutableParser',
        ss_system_parameters.WSDL_VALIDATOR_CONF_LOCATION)
    self.log('Connecting to ssh client')
    self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
    self.log('Creating not executable file')
    self.ssh_client.exec_command(command=create_not_exec_file_command, sudo=True)
    self.log('Set wsdl validator path to not executable file')
    self.ssh_client.exec_command(command=set_wsdl_validator_path_to_not_executable_file, sudo=True)
    self.log('Reload application')
    self.ssh_client.exec_command(command=ss_system_parameters.RELOAD_APP_COMMAND, sudo=True)
    self.log('Wait until server is up')
    wait_until_server_up(ss_host)


def restore_wsdl_validator(case, ssh_host, ssh_username, ssh_password, not_exec_file_path):
    self = case
    '''Restore wsdl validator location conf from backup'''
    restore_backup_command = 'cp /etc/xroad/conf.d/local.ini.backup {0}'.format(
        ss_system_parameters.WSDL_VALIDATOR_CONF_LOCATION)
    '''Command to remove not executable file'''
    remove_not_exec_file = 'rm {0}'.format(not_exec_file_path)
    self.log('Connect ssh client')
    self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
    self.log('Remove not executable file')
    self.ssh_client.exec_command(command=remove_not_exec_file, sudo=True)
    self.log('Restore wsdl validator location conf')
    self.ssh_client.exec_command(command=restore_backup_command, sudo=True)
    self.log('Reload application')
    self.ssh_client.exec_command(command=ss_system_parameters.RELOAD_APP_COMMAND, sudo=True)
    self.log('Close ssh connection')
    self.ssh_client.close()


def restore_wsdl_validator_wrapper(case, ssh_host, ssh_username, ssh_password, wsdl_validator_wrapper_path):
    self = case
    '''Security server ssh client instance'''
    self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
    self.log('Restore wsdl validator wrapper')
    self.ssh_client.exec_command('cp {0}.backup {0}'.format(wsdl_validator_wrapper_path), sudo=True)
    self.log('Remove wsdl validator wrapper backup')
    self.ssh_client.exec_command('rm {0}.backup'.format(wsdl_validator_wrapper_path), sudo=True)
    self.ssh_client.close()


def wait_until_server_up(ss_host):
    '''Wait until reloading process has started'''
    time.sleep(5)
    '''Make get request on ss server, without cert verification'''
    response = requests.get(ss_host, verify=False)
    '''Make get request on ss server until response code is 200 
    one moment it gets the connection, but waits reply for a while'''
    while response.status_code != 200:
        time.sleep(10)
        response = requests.get(ss_host, verify=False)
    time.sleep(5)
