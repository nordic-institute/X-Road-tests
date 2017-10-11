# coding=utf-8
import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_add_to_acl_218 import add_to_acl_2_1_8
from tests.xroad_configure_service_222 import configure_service_2_2_2


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
                                                                                check_add_errors=True,
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

