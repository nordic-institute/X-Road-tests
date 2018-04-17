import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_configure_service_222 import configure_service
from tests.xroad_add_to_acl_218 import add_to_acl
from tests.xroad_configure_service_222 import configure_add_wsdl


class XroadViewServiceAccessRights(unittest.TestCase):
    """
    SERVICE_16 View the Access Rights of a Service
    RIA URL: https://jira.ria.ee/browse/XTKB-171
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_xroad_view_service_access_rights(self):
        main = MainController(self)

        client_name = main.config.get('ss2.client_name')

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')
        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')
        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)


        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        requester = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        subject_list = [xroad.get_xroad_subsystem(requester)]

        service_name2 = main.config.get('services.test_service_2')

        service_name = main.config.get('services.test_service')  # xroadGetRandom
        service_url = main.config.get('services.test_service_url')
        service_2_name = main.config.get('services.test_service_2')  # bodyMassIndex
        service_2_url = main.config.get('services.test_service_2_url')


        test_add_subjects = add_to_acl.test_add_subjects(main, client=client, wsdl_url=wsdl_url,
                                                         service_name=service_name, service_subjects=subject_list,
                                                         remove_data=False,
                                                         allow_remove_all=False, log_checker=log_checker)

        test_add_subjects1 = add_to_acl.test_add_subjects(main, client=client, wsdl_url=wsdl_url,
                                                          service_name=service_name2, service_subjects=subject_list,
                                                          remove_data=False,
                                                          allow_remove_all=False, log_checker=log_checker)




        test_view_service_access_rights = configure_service.view_service_access_rights(main, client, client_name, wsdl_url)
        test_delete_service = configure_service.test_delete_service(case=main, client=client,
                                                                     wsdl_url=wsdl_url)

        test_configure_service = configure_add_wsdl.test_configure_service(case=main, client=client,
                                                                           check_add_errors=True,
                                                                           check_edit_errors=True,
                                                                           check_parameter_errors=True,
                                                                           service_name=service_name,
                                                                           service_url=service_url,
                                                                           service_2_name=service_2_name,
                                                                           service_2_url=service_2_url)

        try:

            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_delete_service()

            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)

            test_configure_service()


            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_add_subjects()

            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_add_subjects1()

            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_view_service_access_rights()
        finally:
            main.tearDown()
