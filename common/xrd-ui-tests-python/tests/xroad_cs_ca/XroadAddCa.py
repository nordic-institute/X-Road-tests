import unittest
from main.maincontroller import MainController
import ca_management
from tests.xroad_cs_ocsp_responder import ocsp_responder


class XroadAddCa(unittest.TestCase):
    '''
    UC TRUST_08 Add an Approved Certification Service
    '''

    def test_xroad_add_ca(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC TRUST_08'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        ca_name = main.config.get('ca.host')
        ca_certificate_filename = 'ca.cert.pem'
        certificate_classpath = main.config.get('ca.profile_class')

        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        ocsp_responder.ca_get_certificates(main, ca_ssh_host, ca_ssh_user, ca_ssh_pass, [ca_certificate_filename])

        ca_certificate = main.get_download_path(ca_certificate_filename)
        invalid_ca_certificate = main.get_download_path('INFO')

        # Configure the service
        test_add_ca = ca_management.test_add_ca(case=main, ca_certificate=ca_certificate,
                                                invalid_ca_certificate=invalid_ca_certificate,
                                                certificate_classpath=certificate_classpath, cs_ssh_host=cs_ssh_host,
                                                cs_ssh_user=cs_ssh_user, cs_ssh_pass=cs_ssh_pass)

        test_delete_ca = ca_management.test_delete_ca(case=main, ca_name=ca_name)

        try:
            # Open webdriver
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

            # Run the test
            test_add_ca()
        except:
            main.log('XroadAddCa: Failed to add CA')
            main.save_exception_data()
            try:
                # Delete service
                main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

                test_delete_ca()
            except:
                main.log('XroadAddCa: Failed to delete added data.')
                main.save_exception_data()
            assert False
        finally:
            # Test teardown
            main.tearDown()
