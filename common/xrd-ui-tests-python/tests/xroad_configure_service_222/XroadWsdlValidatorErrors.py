# coding=utf-8
import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_configure_service_222 import wsdl_validator_errors, configure_service_2_2_2


class XroadWsdlValidatorErrors(unittest.TestCase):
    '''Reloading application in this test may take up to ~10 minutes,
    so the whole test worst case running time is around 40 minutes'''

    def test_xroad_wsdl_validator_errors(self):
        main = MainController(self)

        ssh_host = main.config.get('ss1.ssh_host')
        ssh_user = main.config.get('ss1.ssh_user')
        ssh_pass = main.config.get('ss1.ssh_pass')

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        client_id = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        client_name = main.config.get('ss1.client_name')

        '''Not executable file path'''
        not_exec_file_path = '/etc/xroad/conf.d/notExecutableParser'
        wsdl_local_path = main.config.get('wsdl.local_path')
        wsdl_remote_path = main.config.get('wsdl.remote_path')
        wsdl_warning = main.config.get('wsdl.service_wsdl_warning_filename')
        wsdl_filename = main.config.get('wsdl.service_wsdl')
        wsdl_url = wsdl_remote_path.format(wsdl_filename)
        wsdl_error = main.config.get('wsdl.service_wsdl_error_filename')
        wsdl_warning_url = wsdl_remote_path.format(wsdl_warning)

        test_wsdl_validator_not_set = wsdl_validator_errors.test_wsdl_validator_not_set(case=main,
                                                                                        wsdl_url=wsdl_url,
                                                                                        wsdl_local_path=wsdl_local_path,
                                                                                        wsdl_filename=wsdl_filename,
                                                                                        wsdl_warning=wsdl_warning,
                                                                                        wsdl_error=wsdl_error,
                                                                                        ss_host=ss_host,
                                                                                        ss_user=ss_user,
                                                                                        ss_pass=ss_pass,
                                                                                        client_id=client_id,
                                                                                        client_name=client_name,
                                                                                        ssh_host=ssh_host,
                                                                                        ssh_username=ssh_user,
                                                                                        ssh_password=ssh_pass)
        test_wsdl_validator_invalid_command = wsdl_validator_errors.test_wsdl_validator_invalid_command(case=main,
                                                                                                        wsdl_url=wsdl_url,
                                                                                                        wsdl_warning_url=wsdl_warning_url,
                                                                                                        ss_host=ss_host,
                                                                                                        ss_user=ss_user,
                                                                                                        ss_pass=ss_pass,
                                                                                                        client_id=client_id,
                                                                                                        client_name=client_name,
                                                                                                        ss_ssh_host=ssh_host,
                                                                                                        ss_ssh_user=ssh_user,
                                                                                                        ss_ssh_pass=ssh_pass)
        test_wsdl_validator_not_executable = wsdl_validator_errors.test_wsdl_validator_not_executable(case=main,
                                                                                                      wsdl_url=wsdl_url,
                                                                                                      wsdl_warning_url=wsdl_warning_url,
                                                                                                      ss_host=ss_host,
                                                                                                      ss_user=ss_user,
                                                                                                      ss_pass=ss_pass,
                                                                                                      client_id=client_id,
                                                                                                      client_name=client_name,
                                                                                                      ss_ssh_host=ssh_host,
                                                                                                      ss_ssh_user=ssh_user,
                                                                                                      ss_ssh_pass=ssh_pass)
        delete_service = configure_service_2_2_2.test_delete_service(main, client_name=client_name,
                                                                     client_id=client_id,
                                                                     wsdl_url=wsdl_url,
                                                                     try_cancel=False)
        try:
            main.log('Testing wsdl validation, if wsdl validator path is not set')
            wsdl_validator_errors.remove_wsdl_validator_from_conf(main, ssh_host, ssh_user, ssh_pass, ss_host)
            test_wsdl_validator_not_set()
            main.log('Testing wsdl validation, if wsdl validator is set to not existing command')
            wsdl_validator_errors.set_wsdl_validator_invalid_command(main, ssh_host, ssh_user, ssh_pass, ss_host)
            test_wsdl_validator_invalid_command()
            main.log('Testing wsdl validation, if wsdl validator is set to not exectable command')
            wsdl_validator_errors.set_wsdl_validator_not_executable(main, ssh_host, ssh_user, ssh_pass, ss_host,
                                                                    not_exec_file_path)
            test_wsdl_validator_not_executable()
        except:
            main.log('Test failed')
            assert False
        finally:
            main.log('Reload page')
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            main.log('Delete added service')
            delete_service()
            main.log('Restore local.ini')
            wsdl_validator_errors.restore_wsdl_validator(case=main, ssh_host=ssh_host, ssh_username=ssh_user,
                                                         ssh_password=ssh_pass, not_exec_file_path=not_exec_file_path)
            main.log('Wait until server responds before continuing with tests')
            wsdl_validator_errors.wait_until_server_up(ss_host)
            main.tearDown()

