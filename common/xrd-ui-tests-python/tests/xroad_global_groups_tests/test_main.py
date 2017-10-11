from __future__ import absolute_import

import unittest

from helpers import xroad, soaptestclient
from main.maincontroller import MainController
from tests.xroad_global_groups_tests.global_groups_tests import add_group, add_member_to_group, remove_group


class XroadGlobalGroups(unittest.TestCase):
    def test_global_groups_tests(self):
        main = MainController(self)

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        group = main.config.get('cs.global_group')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        wsdl_url = main.config.get('wsdl.remote_path').format(
            main.config.get('wsdl.service_wsdl'))

        testservice_name = main.config.get('services.test_service')

        query_url = main.config.get('ss1.service_path')
        query_filename = main.config.get('services.request_template_filename')
        query = main.get_xml_query(query_filename)
        client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        client['name'] = main.config.get('ss1.client_name')
        provider = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        service_name = main.config.get('services.test_service')
        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')
        identifier = main.config.get('cs.identifier')

        testclient_params = {
            'xroadProtocolVersion': main.config.get('services.xroad_protocol'),
            'xroadIssue': main.config.get('services.xroad_issue'),
            'xroadUserId': main.config.get('services.xroad_userid'),
            'serviceMemberInstance': provider['instance'],
            'serviceMemberClass': provider['class'],
            'serviceMemberCode': provider['code'],
            'serviceSubsystemCode': provider['subsystem'],
            'serviceCode': xroad.get_service_name(testservice_name),
            'serviceVersion': xroad.get_service_version(testservice_name),
            'memberInstance': client['instance'],
            'memberClass': client['class'],
            'memberCode': client['code'],
            'subsystemCode': client['subsystem'],
            'requestBody': main.config.get('services.testservice_request_body')
        }
        sync_retry = main.config.get('services.request_sync_delay')
        sync_max_seconds = main.config.get('services.request_sync_timeout')
        '''Not expected faults, query fails'''
        faults_unsuccessful = ['Server.ClientProxy.SslAuthenticationFailed', 'Server.ServerProxy.AccessDenied']
        '''Expected faults'''
        faults_successful = ['Server.ServerProxy.ServiceFailed']

        testclient = soaptestclient.SoapTestClient(url=query_url, body=query,
                                                   retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                   faults_successful=faults_successful,
                                                   faults_unsuccessful=faults_unsuccessful,
                                                   params=testclient_params)

        main.tearDown()
        try:
            '''Log in to central server'''
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            main.log('SERVICE_32 Add a Global Group')
            add_group(main, group, check_global_groups_inputs=True,
                      cs_ssh_host=cs_ssh_host, cs_ssh_user=cs_ssh_user, cs_ssh_pass=cs_ssh_pass)
            main.log('SERVICE_34 Add Members to a Global Group')
            add_member_to_group(main, client, group, ss2_host, ss2_user, ss2_pass, testclient, wsdl_url, service_name,
                                identifier)

        finally:
            try:
                main.log('SERVICE_39 Delete a Global Group')
                main.reload_webdriver(cs_host, cs_user, cs_pass)
                remove_group(main, group, cs_ssh_host=cs_ssh_host, cs_ssh_user=cs_ssh_user, cs_ssh_pass=cs_ssh_pass)
            except:
                main.log('2.11.1-del Deleting group failed')
            main.tearDown()
