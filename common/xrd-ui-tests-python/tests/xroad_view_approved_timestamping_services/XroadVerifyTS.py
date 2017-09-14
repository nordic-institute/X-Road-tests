import unittest
from main.maincontroller import MainController
import ts_management


class XroadVerifyTS(unittest.TestCase):
    '''
    UC TRUST_15 View Approved Timestamping Services
    '''

    def test_xroad_verify_ts(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC TRUST_15'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        ts_name = main.config.get('tsa.host')

        # Configure the service
        test_view_approved_ts = ts_management.test_view_approved_ts(case=main, ts_name=ts_name)
        try:
            # Open webdriver
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

            # Run the test
            test_view_approved_ts()
        except:
            main.log('XroadViewTs: Failed to verify Timestamping services')
            main.save_exception_data()
            assert False
        finally:
            # Test teardown
            main.tearDown()
