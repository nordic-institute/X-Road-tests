import unittest

from helpers import auditchecker
from main.maincontroller import MainController
from tests.xroad_cs_register_management_service.register_management_service import register_management_service


class XroadRegisterManagementService(unittest.TestCase):
    def __init__(self, methodName='test_register_management_service'):
        unittest.TestCase.__init__(self, methodName)

    def test_register_management_service(self):
        """
        MEMBER_57 Register the Management Service Provider as a Security Server Client
        RIA URL: https://jira.ria.ee/browse/XTKB-134
        Depends on finishing other test(s): MEMBER_25
        Requires helper scenarios:
        X-Road version: 6.16.0
        :return:
        """
        main = MainController(self)
        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        server_name = main.config.get('ss1.server_name')
        register_management = register_management_service(main, server_name, try_cancel=True,
                                                          log_checker=auditchecker.AuditChecker(cs_ssh_host,
                                                                                                cs_ssh_user,
                                                                                                cs_ssh_pass))
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            register_management()
        finally:
            main.tearDown()
