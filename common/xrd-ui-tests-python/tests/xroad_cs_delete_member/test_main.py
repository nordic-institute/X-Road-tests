import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_changing_database_rows_with_cs_gui_291.changing_database_rows_with_cs_gui_2_9_1 import USERNAME
from tests.xroad_cs_delete_member import deleting_in_cs
from tests.xroad_global_groups_tests import global_groups_tests


class XroadCsDeleteMemberWithSubSystem(unittest.TestCase):
    """MEMBER_26 5a deleting member with subsystem as security server client"""

    def test_xroad_cs_delete_member_with_subsystem(self):
        main = MainController(self)

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        cs_member = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_server_name = main.config.get('ss1.server_name')

        ss1_host = main.config.get('ss1.host')
        ss1_username = main.config.get('ss1.user')
        ss1_password = main.config.get('ss1.pass')

        cs_member_name = main.config.get('ss1.client_name')
        ss1_client_name = main.config.get('ss1.client_name')

        cs_host = main.config.get('cs.host')
        cs_username = main.config.get('cs.user')
        cs_password = main.config.get('cs.pass')

        user = {USERNAME: cs_username}

        main.log('MEMBER_26 5a deleting member with subsystem as security server client')
        setup_member_with_subsystem_as_ss_client = deleting_in_cs.setup_member_with_subsystem_as_ss_client(main,
                                                                                                           cs_host,
                                                                                                           cs_username,
                                                                                                           cs_password,
                                                                                                           cs_member_name,
                                                                                                           cs_member,
                                                                                                           ss1_host,
                                                                                                           ss1_username,
                                                                                                           ss1_password,
                                                                                                           ss1_client,
                                                                                                           ss1_server_name,
                                                                                                           ss1_client_name)
        remove_client_and_key_from_ss = deleting_in_cs.remove_client_and_key_from_ss(main, ss1_host, ss1_username,
                                                                                     ss1_password, ss1_client_name,
                                                                                     ss1_client)
        test_deleting_member_with_subsystem_as_client = deleting_in_cs.test_deleting_member_with_subsystem_registered_as_client_to_ss(
            case=main,
            cs_member_name=cs_member_name, cs_new_member=cs_member,
            ss1_client=ss1_client,
            cs_ssh_host=cs_ssh_host,
            cs_ssh_username=cs_ssh_user, cs_ssh_password=cs_ssh_pass, user=user)
        try:
            setup_member_with_subsystem_as_ss_client()
            test_deleting_member_with_subsystem_as_client()
        except:
            assert False
        finally:
            remove_client_and_key_from_ss()
            main.tearDown()


class XroadCsDeleteMemberWithGlobalGroup(unittest.TestCase):
    """MEMBER_26 6a deleting member with global group"""

    def test_xroad_cs_delete_member_with_global_group(self):
        main = MainController(self)

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        client_id = main.config.get('ss1.client2_id')
        client_name = main.config.get('ss1.client2_name')
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        cs_host = main.config.get('cs.host')
        cs_username = main.config.get('cs.user')
        cs_password = main.config.get('cs.pass')
        main.log('MEMBER_26 6a deleting member with global group')
        user = {USERNAME: cs_username}
        test_group_name = 'testGroup'
        test_deleting_member_with_global_group = deleting_in_cs.test_deleting_member_with_global_group(
            cs_ssh_host,
            cs_ssh_user,
            cs_ssh_pass,
            client,
            user,
            test_group_name)

        try:
            main.reload_webdriver(url=cs_host, username=cs_username, password=cs_password)
            test_deleting_member_with_global_group(main)
        except:
            assert False
        finally:
            global_groups_tests.remove_group(main, test_group_name)
            main.tearDown()


class XroadCsDeleteMemberWithSecurityServer(unittest.TestCase):
    """MEMBER_26 4a deleting member with owned security server"""

    def test_xroad_cs_delete_member_with_security_server(self):
        main = MainController(self)

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        cs_host = main.config.get('cs.host')
        cs_username = main.config.get('cs.user')
        cs_password = main.config.get('cs.pass')

        ss2_host = main.config.get('ss2.host')
        ss2_username = main.config.get('ss2.user')
        ss2_password = main.config.get('ss2.pass')

        ss2_ssh_host = main.config.get('ss2.ssh_host')

        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        client_id = main.config.get('ss2.client2_id')
        client_name = main.config.get('ss2.client2_name')
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name

        user = {USERNAME: cs_username}
        cert_path = 'temp.pem'

        test_deleting_member_with_security_server = deleting_in_cs.test_deleting_member_with_security_server(
            main,
            cs_ssh_host=cs_ssh_host,
            cs_ssh_user=cs_ssh_user,
            cs_ssh_pass=cs_ssh_pass,
            client=client,
            user=user)

        '''MEMBER_12 add an owned security server to an X-Road Member'''
        main.log('MEMBER_12 add an owned security server to an X-Road Member')
        restore_security_server = deleting_in_cs.restore_security_server_after_member_deletion(
            main,
            cs_ssh_host=cs_ssh_host,
            cs_ssh_user=cs_ssh_user,
            cs_ssh_pass=cs_ssh_pass,
            ca_ssh_host=ca_ssh_host,
            ca_ssh_user=ca_ssh_user,
            ca_ssh_pass=ca_ssh_pass,
            client=client,
            ss2_host=ss2_host,
            ss2_username=ss2_username,
            ss2_password=ss2_password,
            ss2_ssh_host=ss2_ssh_host,
            cert_path=cert_path,
            user=user)

        test_add_ss_to_cs_member = deleting_in_cs.test_add_security_server_to_member(main, cs_host, cs_username,
                                                                                     cs_password,
                                                                                     cs_ssh_host, cs_ssh_user,
                                                                                     cs_ssh_pass,
                                                                                     client, cert_path=cert_path)
        try:
            main.reload_webdriver(url=cs_host, username=cs_username, password=cs_password)
            test_deleting_member_with_security_server()
        except:
            assert False
        finally:
            restore_security_server()
            test_add_ss_to_cs_member()
            main.tearDown()
