from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_global_groups_tests import global_groups_tests


class XroadGlobalGroups(unittest.TestCase):
    def test_global_groups_tests(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SERVICE_32 3, 3a, 4a, 6'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')
        if main.driver is None:
            main.reset_webdriver(main.url, username=main.username, password=main.password, init_new_webdriver=False)

        group = main.config.get('cs.global_group')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        server_groups = '{0},{1},{2}'.format(main.config.get('xroad.registration_officer_group'),
                                             main.config.get('xroad.system_administrator_group'),
                                             main.config.get('xroad.security_officer_group'))

        users = {'user1': {'username': main.config.get('xroad.user1'), 'password': main.config.get('xroad.user1'),
                           'group': server_groups},
                 'user2': {'username': main.config.get('xroad.user2'), 'password': main.config.get('xroad.user2'),
                           'group': server_groups},
                 'user3': {'username': main.config.get('xroad.user3'), 'password': main.config.get('xroad.user3'),
                           'group': server_groups}
                 }
        main.log('TEST: LOGGING TEST IN CENTRAL SERVER')
        test_func = global_groups_tests.test_test(main.config.get('cs.ssh_host'),
                                                  main.config.get('cs.ssh_user'),
                                                  main.config.get('cs.ssh_pass'),
                                                  group=group,
                                                  users=users,
                                                  check_global_groups_inputs=True, cs_ssh_host=cs_ssh_host,
                                                  cs_ssh_user=cs_ssh_user, cs_ssh_pass=cs_ssh_pass)
        test_func(main)
        main.tearDown()


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(XroadGlobalGroups)
    unittest.TextTestRunner().run(suite)
