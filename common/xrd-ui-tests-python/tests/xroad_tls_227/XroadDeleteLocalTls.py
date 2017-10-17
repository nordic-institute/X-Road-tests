# coding=utf-8
import unittest

import local_tls_2_2_7
from helpers import xroad
from main.maincontroller import MainController


class XroadDeleteLocalTls(unittest.TestCase):
    def test_tls_227(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.2.7-del'
        main.test_name = self.__class__.__name__

        client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        provider = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        # Configure the tests
        delete_local_tls = local_tls_2_2_7.test_delete_tls(case=main, client=client, provider=provider)

        try:
            # Delete internal certificates from the servers
            delete_local_tls()
        except:
            main.log('XroadDeleteLocalTls: failed to remove TLS from local service')
            assert False
        finally:
            # Test teardown
            main.tearDown()
