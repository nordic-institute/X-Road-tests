# coding=utf-8
import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_add_to_acl_218 import add_to_acl_2_1_8
from tests.xroad_configure_service_222 import wsdl_validator_errors, configure_service_2_2_2
from view_models import ss_system_parameters


class XroadConfigureService(unittest.TestCase):
    def test_xroad_configure_service(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.2.2'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        requester = xroad.split_xroad_id(main.config.get('ss1.client_id'))

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        service_name = main.config.get('services.test_service')  # xroadGetRandom
        service_url = main.config.get('services.test_service_url')
        service_2_name = main.config.get('services.test_service_2')  # bodyMassIndex
        service_2_url = main.config.get('services.test_service_2_url')

        subject_list = [xroad.get_xroad_subsystem(requester)]

        # Configure the service
        test_configure_service = configure_service_2_2_2.test_configure_service(case=main, client=client,
                                                                                check_add_errors=False,
                                                                                check_edit_errors=True,
                                                                                check_parameter_errors=True,
                                                                                service_name=service_name,
                                                                                service_url=service_url,
                                                                                service_2_name=service_2_name,
                                                                                service_2_url=service_2_url)

        # Add the subject to ACL
        test_configure_service_acl = add_to_acl_2_1_8.test_add_subjects(case=main, client=client,
                                                                        wsdl_url=wsdl_url,
                                                                        service_name=service_name,
                                                                        service_subjects=subject_list,
                                                                        remove_data=False,
                                                                        allow_remove_all=False)
        test_configure_service_acl_2 = add_to_acl_2_1_8.test_add_subjects(case=main, client=client,
                                                                          wsdl_url=wsdl_url,
                                                                          service_name=service_2_name,
                                                                          service_subjects=subject_list,
                                                                          remove_data=False,
                                                                          allow_remove_all=False)
        # Enable the service
        test_enable_service = configure_service_2_2_2.test_enable_service(case=main, client=client, wsdl_url=wsdl_url)

        # Delete the added service
        test_delete_service = configure_service_2_2_2.test_delete_service(case=main, client=client, wsdl_url=wsdl_url)
        wsdl_test_service = main.config.get('wsdl.service_wsdl_test_service1')
        # Delete the other added service
        wsdl_test_service_url = main.config.get('wsdl.remote_path').format(wsdl_test_service)
        test_delete_service1 = configure_service_2_2_2.test_delete_service(case=main, client=client,
                                                                           wsdl_url=wsdl_test_service_url)

        try:
            # Open webdriver
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)

            # TEST PLAN 2.2.2-1, 2.2.2-2 add WSDL and configure service
            test_configure_service()

            # TEST PLAN 2.2.2-3 configure service ACL
            main.log('2.2.2-3 configure service ACL')
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_configure_service_acl()

            # TEST PLAN 2.2.2-3 configure second service ACL
            main.log('2.2.2-3 configure second service ACL')
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_configure_service_acl_2()

            # TEST PLAN 2.2.2-4 enable service
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_enable_service()
        except:
            main.log('XroadConfigureService: Failed to configure service')
            main.save_exception_data()
            try:
                # Delete service
                main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
                test_delete_service()
            except:
                main.log('XroadConfigureService: Failed to delete added data.')
                main.save_exception_data()
            assert False
        finally:
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_delete_service1()
            # Test teardown
            main.tearDown()

class XroadDeleteService(unittest.TestCase):
    def test_xroad_configure_service(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.2.2'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        # Delete the added service
        test_delete_service = configure_service_2_2_2.test_delete_service(case=main, client=client, wsdl_url=wsdl_url)

        try:
            # Delete service
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_delete_service()
        except:
            main.log('XroadDeleteService: Failed to delete service')
            assert False
        finally:
            # Test teardown
            main.tearDown()


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


class XroadWsdlValidatorCrash(unittest.TestCase):
    def test_xroad_wsdl_validator_crash(self):
        main = MainController(self)

        ssh_host = main.config.get('ss1.ssh_host')
        ssh_user = main.config.get('ss1.ssh_user')
        ssh_pass = main.config.get('ss1.ssh_pass')

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        client_id = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        client_name = main.config.get('ss1.client_name')

        wsdl_warning_url = main.config.get('wsdl.remote_path').format(
            main.config.get('wsdl.service_wsdl_warning_filename'))
        wsdl_validator_wrapper_path = ss_system_parameters.WSDL_VALIDATOR_WRAPPER_LOCATION

        test_wsdl_validator_crash = wsdl_validator_errors.test_wsdl_validator_crash(case=main,
                                                                                    ssh_host=ssh_host,
                                                                                    ssh_username=ssh_user,
                                                                                    ssh_password=ssh_pass,
                                                                                    wsdl_url=wsdl_warning_url,
                                                                                    ss_host=ss_host,
                                                                                    ss_user=ss_user,
                                                                                    ss_pass=ss_pass,
                                                                                    client_id=client_id,
                                                                                    client_name=client_name,
                                                                                    wsdl_validator_wrapper_path=wsdl_validator_wrapper_path)

        try:
            '''SERVICE_44 step 1c Testing wsdl validation, when wsdl validator is executed with wrong argument'''
            main.log('SERVICE_44 step 1c Testing wsdl validation, when wsdl validator is executed with wrong argument')
            test_wsdl_validator_crash()
        except:
            main.log('Test failed')
            assert False
        finally:
            main.log('Restoring wsdl wrapper')
            wsdl_validator_errors.restore_wsdl_validator_wrapper(case=main, ssh_host=ssh_host, ssh_username=ssh_user,
                                                                 ssh_password=ssh_pass,
                                                                 wsdl_validator_wrapper_path=wsdl_validator_wrapper_path)
            main.tearDown()
