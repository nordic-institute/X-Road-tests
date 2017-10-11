import unittest
from main.maincontroller import MainController
import ts_management


class XroadDeleteTS(unittest.TestCase):
    '''
    UC TRUST_18: Delete an Approved Timestamping Service
    '''

    def test_xroad_delete_ts(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC TRUST_18'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        ts_name = main.config.get('tsa.host')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        test_delete_ts = ts_management.test_delete_ts(case=main, ts_name=ts_name, cs_ssh_host=cs_ssh_host,
                                                      cs_ssh_user=cs_ssh_user, cs_ssh_pass=cs_ssh_pass)

        try:
            # Open webdriver
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)
            # Run the test
            test_delete_ts()
        except:
            main.log('XroadDeleteTS: Failed to delete TS')
            main.save_exception_data()
            assert False
        finally:
            # Test teardown
            main.tearDown()
