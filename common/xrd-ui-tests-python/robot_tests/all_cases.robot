*** Settings ***

Suite Setup     Test suite setup
Suite Teardown  Test suite teardown
Test Setup      setup
Test Teardown   teardown

Library     QAutoLibrary.QAutoRobot  ${None}

Library     tests.xroad_cs_add_member.XroadAddCsMember
Library     tests.xroad_ss_add_subsystem_as_client.XroadAddSubsystemAsClient
Library     tests.xroad_ss_client.XroadRegisterClient
Library     tests.xroad_cs_add_client_to_member.XroadAddClientToMember
Library     tests.xroad_cs_approve_requests.XroadApproveRequests
Library     tests.xroad_configure_service_222.XroadAddWsdlSecurityServerClient
Library     tests.xroad_configure_service_222.XroadEnableWSDL
Library     tests.xroad_configure_service_222.XroadViewWSDL
Library     tests.xroad_configure_service_222.XroadViewService
Library     tests.xroad_configure_service_222.XroadEditAddressWSDL
Library     tests.xroad_cs_view_central_services.XroadViewCentralService
Library     tests.xroad_global_groups_tests.XroadGlobalGroups
Library     tests.xroad_global_groups_tests.XroadViewGlobalGroups
Library     tests.xroad_global_groups_tests.XroadViewGlobalGroupDetails
Library     tests.xroad_global_groups_tests.XroadEditGlobalGroupDescription
Library     tests.xroad_global_groups_tests.XroadMemberAddToGlobalGroup
Library     tests.xroad_global_groups_tests.XroadMemberRemoveFromGlobalGroup
Library     tests.xroad_add_to_acl_218.XroadAddToAcl
Library     tests.xroad_add_to_acl_from_client_219.XroadAddToAclFromClient
Library     tests.xroad_cs_add_client_to_member.XroadAddClientToMemberExtensions
Library     tests.xroad_cs_revoke_requests.XroadRevokeRequests
Library     tests.xroad_ss_user_logging.XroadSSUserLogging
Library     tests.xroad_cs_user_logging.XroadCsUserLogging
Library     tests.xroad_subsystem_to_member.XroadAddSubToMember
Library     tests.xroad_ss_apply_parameter_value_of_a_service_to_all_services.XroadEditServiceParameters
Library     tests.xroad_parse_users_inputs.XroadCentralServiceInputs
Library     tests.xroad_parse_users_inputs.XroadAddWsdlInputs
Library     tests.xroad_parse_users_inputs.XroadDisableWsdlInputs
Library     tests.xroad_parse_users_inputs.XroadEditCentralService
Library     tests.xroad_parse_users_inputs.XroadEditCsMemberInputs
Library     tests.xroad_parse_users_inputs.XroadEditTimeoutValueInputs
Library     tests.xroad_parse_users_inputs.XroadEditWsdlInputs
Library     tests.xroad_parse_users_inputs.XroadGlobalGroupsInputs
Library     tests.xroad_parse_users_inputs.XroadParseCSRInputs
Library     tests.xroad_parse_users_inputs.XroadParseKeyLabelInputs
Library     tests.xroad_parse_users_inputs.XroadSsClientInputs
Library     tests.xroad_parse_users_inputs.XroadEditAddressServiceInputs
Library     tests.xroad_ss_client_certification_213.XroadGenerateCSRInputParsing
Library     tests.xroad_tokens_keys_certs.XroadEditKeyName
Library     tests.xroad_tokens_keys_certs.XroadKeyDetails
Library     tests.xroad_tokens_keys_certs.XroadTokenDetails
Library     tests.xroad_tokens_keys_certs.XroadViewKeyDetails
Library     tests.xroad_tokens_keys_certs.XroadViewKeyList
Library     tests.xroad_tokens_keys_certs.XroadViewTheList
Library     tests.xroad_edit_token_friendly_name.XroadEditTokenFriendlyName
Library     tests.xroad_cs_upload_trusted_anchor.XroadUploadTrustedAnchor
Library     tests.xroad_cs_view_trusted_anchor.XroadViewTrustedAnchor
Library     tests.xroad_cs_download_trusted_anchor.XroadDownloadTrustedAnchor
Library     tests.xroad_cs_delete_trusted_anchor.XroadDeleteTrustedAnchor
Library     tests.xroad_cs_view_management_service.XroadViewManagementService
Library     tests.xroad_cs_edit_management_service.XroadEditManagementService
Library     tests.xroad_ss_service_local_groups_view.XroadSsServiceLocalGroupsView
Library     tests.xroad_ss_service_local_groups_view_details.XroadSsServiceLocalGroupsViewDetails
Library     tests.xroad_cs_ca.XroadAddCa
Library     tests.xroad_cs_ca.XroadEditCa
Library     tests.xroad_cs_ca.XroadDeleteCa
Library     tests.xroad_cs_ocsp_responder.XroadAddOcspResponder
Library     tests.xroad_cs_ocsp_responder.XroadViewOcspResponder
Library     tests.xroad_cs_ocsp_responder.XroadDeleteOcspResponder
Library     tests.xroad_cs_intermediate_ca.XroadAddIntermediateCA
Library     tests.xroad_cs_intermediate_ca.XroadViewIntermediateCA
Library     tests.xroad_cs_intermediate_ca.XroadViewIntermediateCADetails
Library     tests.xroad_cs_intermediate_ca.XroadDeleteIntermediateCA
Library     tests.xroad_view_approved_timestamping_services.XroadDeleteTS
Library     tests.xroad_view_approved_timestamping_services.XroadAddTS
Library     tests.xroad_view_approved_timestamping_services.XroadVerifyTS
Library     tests.xroad_view_approved_timestamping_services.XroadEditTS
Library     tests.xroad_log_into_a_software_token.XroadLoginToken
Library     tests.xroad_log_out_software_token.XroadLogoutToken
Library     tests.xroad_trust_view_details_cs_settings.XroadTrustViewDetailsCsSettings
Library     tests.xroad_trust_view_details_cs_ca_certificate.XroadTrustViewDetailsCsCaCertificate
Library     tests.xroad_trust_view_details_cs_ca.XroadTrustViewDetailsCsCa
Library     tests.xroad_trust_view_approved_certification_services.XroadTrustViewApprovedCertService
Library     tests.xroad_cs_view_xroad_members.XroadViewCSMembers
Library     tests.xroad_configure_service_222.XroadDeleteService
Library     tests.xroad_configure_service_222.XroadDownloadParseURL


*** Variables ***

*** Test Cases ***

Test a xroad add cs member
    tests.xroad_cs_add_member.XroadAddCsMember.Test a xroad add cs member

Test b xroad add cs existing member
    tests.xroad_cs_add_member.XroadAddCsMember.Test b xroad add cs existing member

Test a add subsystem as client
    tests.xroad_ss_add_subsystem_as_client.XroadAddSubsystemAsClient.Test a add subsystem as client

Test b add subsystem as client by hand
    tests.xroad_ss_add_subsystem_as_client.XroadAddSubsystemAsClient.Test b add subsystem as client by hand

Test c add client input errors
    tests.xroad_ss_add_subsystem_as_client.XroadAddSubsystemAsClient.Test c add client input errors

Test xroad register client
    tests.xroad_ss_client.XroadRegisterClient.Test xroad register client

Test add client to member
    tests.xroad_cs_add_client_to_member.XroadAddClientToMember.Test add client to member

Test approve requests
    tests.xroad_cs_approve_requests.XroadApproveRequests.Test approve requests

Test xroad configure service
    tests.xroad_configure_service_222.XroadAddWsdlSecurityServerClient.Test xroad configure service

Test activate wsdl
    tests.xroad_configure_service_222.XroadEnableWSDL.Test activate wsdl

Test xroad view wsdl
    tests.xroad_configure_service_222.XroadViewWSDL.Test xroad view wsdl

Test xroad view wsdl 2
    tests.xroad_configure_service_222.XroadViewService.Test xroad view wsdl

Test xroad configure service 2
    tests.xroad_configure_service_222.XroadEditAddressWSDL.Test xroad configure service

Test view central service
    tests.xroad_cs_view_central_services.XroadViewCentralService.Test view central service

Test global groups tests
    tests.xroad_global_groups_tests.XroadGlobalGroups.Test global groups tests

Test view global groups
    tests.xroad_global_groups_tests.XroadViewGlobalGroups.Test view global groups

Test view global group details
    tests.xroad_global_groups_tests.XroadViewGlobalGroupDetails.Test view global group details

Test edit global group description
    tests.xroad_global_groups_tests.XroadEditGlobalGroupDescription.Test edit global group description

Test member add to global group
    tests.xroad_global_groups_tests.XroadMemberAddToGlobalGroup.Test member add to global group

Test member remove from global group
    tests.xroad_global_groups_tests.XroadMemberRemoveFromGlobalGroup.Test member remove from global group

Test add to acl
    tests.xroad_add_to_acl_218.XroadAddToAcl.Test add to acl

Test acl
    tests.xroad_add_to_acl_from_client_219.XroadAddToAclFromClient.Test acl

Test add client extensions
    tests.xroad_cs_add_client_to_member.XroadAddClientToMemberExtensions.Test add client extensions

Test xroad revoke requests
    tests.xroad_cs_revoke_requests.XroadRevokeRequests.Test xroad revoke requests

Test ss user logging
    tests.xroad_ss_user_logging.XroadSSUserLogging.Test ss user logging

Test cs user logging
    tests.xroad_cs_user_logging.XroadCsUserLogging.Test cs user logging

Test add sub to member
    tests.xroad_subsystem_to_member.XroadAddSubToMember.Test add sub to member

Test xroad apply TLS value to all services in wsdl
    tests.xroad_ss_apply_parameter_value_of_a_service_to_all_services.XroadEditServiceParameters.Test xroad apply TLS value to all services in wsdl

Test parse central service inputs
    tests.xroad_parse_users_inputs.XroadCentralServiceInputs.Test parse central service inputs

Test parse added wsdl inputs
    tests.xroad_parse_users_inputs.XroadAddWsdlInputs.Test parse added wsdl inputs

Test parse user input SS 41
    tests.xroad_parse_users_inputs.XroadDisableWsdlInputs.Test parse user input SS 41

Test parse edited central service inputs
    tests.xroad_parse_users_inputs.XroadEditCentralService.Test parse edited central service inputs

Test parse edit cs member inputs
    tests.xroad_parse_users_inputs.XroadEditCsMemberInputs.Test parse edit cs member inputs

Test parse edit time out value service
    tests.xroad_parse_users_inputs.XroadEditTimeoutValueInputs.Test parse edit time out value service

Test edit wsdl inputs
     tests.xroad_parse_users_inputs.XroadEditWsdlInputs.Test edit wsdl inputs

Test parse global groups inputs
    tests.xroad_parse_users_inputs.XroadGlobalGroupsInputs.Test parse global groups inputs

Test parse csr inputs
    tests.xroad_parse_users_inputs.XroadParseCSRInputs.Test parse csr inputs

Test parse key label inputs
    tests.xroad_parse_users_inputs.XroadParseKeyLabelInputs.Test parse key label inputs

Test parse ss client inputs
    tests.xroad_parse_users_inputs.XroadSsClientInputs.Test parse ss client inputs

Test parse edit address service
    tests.xroad_parse_users_inputs.XroadEditAddressServiceInputs.Test parse edit address service

Test generate csr input parsing
    tests.xroad_ss_client_certification_213.XroadGenerateCSRInputParsing.Test generate csr input parsing

Test edit key name SS 23
    tests.xroad_tokens_keys_certs.XroadEditKeyName.Test edit key name SS 23

Test view key details SS 21
    tests.xroad_tokens_keys_certs.XroadKeyDetails.Test view key details SS 21

Test view token details SS 20
    tests.xroad_tokens_keys_certs.XroadTokenDetails.Test view token details SS 20

Test view key details SS 21 2
    tests.xroad_tokens_keys_certs.XroadViewKeyDetails.Test view key details SS 21

Test view list tokens keys certs SS 19
    tests.xroad_tokens_keys_certs.XroadViewKeyList.Test view list tokens keys certs SS 19

Test view list tokens keys certs SS 19 2
    tests.xroad_tokens_keys_certs.XroadViewTheList.Test view list tokens keys certs SS 19

Test xroad edit token friendly name
    tests.xroad_edit_token_friendly_name.XroadEditTokenFriendlyName.Test xroad edit token friendly name

Test a upload trusted anchor same instance error
    tests.xroad_cs_upload_trusted_anchor.XroadUploadTrustedAnchor.Test a upload trusted anchor same instance error

Test b upload trusted anchor download error
    tests.xroad_cs_upload_trusted_anchor.XroadUploadTrustedAnchor.Test b upload trusted anchor download error

Test c upload trusted anchor expired error
    tests.xroad_cs_upload_trusted_anchor.XroadUploadTrustedAnchor.Test c upload trusted anchor expired error

Test d upload trusted anchor signature error
    tests.xroad_cs_upload_trusted_anchor.XroadUploadTrustedAnchor.Test d upload trusted anchor signature error

Test e upload trusted anchor internal configuration error
    tests.xroad_cs_upload_trusted_anchor.XroadUploadTrustedAnchor.Test e upload trusted anchor internal configuration error

Test f upload trusted anchor other error
    tests.xroad_cs_upload_trusted_anchor.XroadUploadTrustedAnchor.Test f upload trusted anchor other error

Test g upload trusted anchor
    tests.xroad_cs_upload_trusted_anchor.XroadUploadTrustedAnchor.Test g upload trusted anchor

Test h update trusted anchor
    tests.xroad_cs_upload_trusted_anchor.XroadUploadTrustedAnchor.Test h update trusted anchor

Test i upload trusted anchor not valid file
    tests.xroad_cs_upload_trusted_anchor.XroadUploadTrustedAnchor.Test i upload trusted anchor not valid file

Test view trusted anchor
    tests.xroad_cs_view_trusted_anchor.XroadViewTrustedAnchor.Test view trusted anchor

Test download trusted anchor
    tests.xroad_cs_download_trusted_anchor.XroadDownloadTrustedAnchor.Test download trusted anchor

Test a delete trusted anchor cancel
    tests.xroad_cs_delete_trusted_anchor.XroadDeleteTrustedAnchor.Test a delete trusted anchor cancel

Test b delete trusted anchor
    tests.xroad_cs_delete_trusted_anchor.XroadDeleteTrustedAnchor.Test b delete trusted anchor

Test view management service
    tests.xroad_cs_view_management_service.XroadViewManagementService.Test view management service

Test edit management service
    tests.xroad_cs_edit_management_service.XroadEditManagementService.Test edit management service

Test xroad logout token 2
    tests.xroad_ss_service_local_groups_view.XroadSsServiceLocalGroupsView.Test xroad logout token

Test xroad local groups view details
    tests.xroad_ss_service_local_groups_view_details.XroadSsServiceLocalGroupsViewDetails.Test xroad local groups view details

Test xroad add ca
    tests.xroad_cs_ca.XroadAddCa.Test xroad add ca

Test xroad add ca 2
    tests.xroad_cs_ca.XroadEditCa.Test xroad add ca

Test xroad delete ca
    tests.xroad_cs_ca.XroadDeleteCa.Test xroad delete ca

Test xroad add ocsp responder
    tests.xroad_cs_ocsp_responder.XroadAddOcspResponder.Test xroad add ocsp responder

Test xroad delete ocsp responder
    tests.xroad_cs_ocsp_responder.XroadViewOcspResponder.Test xroad delete ocsp responder

Test xroad delete ocsp responder 2
    tests.xroad_cs_ocsp_responder.XroadDeleteOcspResponder.Test xroad delete ocsp responder

Test xroad intermediate ca adding
    tests.xroad_cs_intermediate_ca.XroadAddIntermediateCA.Test xroad intermediate ca adding

Test xroad intermediate ca invalid file error
    tests.xroad_cs_intermediate_ca.XroadAddIntermediateCA.Test xroad intermediate ca invalid file error

Test xroad intermediate ca deleting
    tests.xroad_cs_intermediate_ca.XroadViewIntermediateCA.Test xroad intermediate ca deleting

Test xroad intermediate ca deleting 2
    tests.xroad_cs_intermediate_ca.XroadViewIntermediateCADetails.Test xroad intermediate ca deleting

Test xroad intermediate ca deleting 3
    tests.xroad_cs_intermediate_ca.XroadDeleteIntermediateCA.Test xroad intermediate ca deleting

Test xroad delete ts
    tests.xroad_view_approved_timestamping_services.XroadDeleteTS.Test xroad delete ts

Test xroad add ts
    tests.xroad_view_approved_timestamping_services.XroadAddTS.Test xroad add ts

Test xroad verify ts
    tests.xroad_view_approved_timestamping_services.XroadVerifyTS.Test xroad verify ts

Test xroad edit ts
    tests.xroad_view_approved_timestamping_services.XroadEditTS.Test xroad edit ts

Test xroad login token
    tests.xroad_log_into_a_software_token.XroadLoginToken.Test xroad login token

Test xroad logout token
    tests.xroad_log_out_software_token.XroadLogoutToken.Test xroad logout token

Test xroad view view cs
    tests.xroad_trust_view_details_cs_settings.XroadTrustViewDetailsCsSettings.Test xroad view view cs

Test xroad view cs ca cert
    tests.xroad_trust_view_details_cs_ca_certificate.XroadTrustViewDetailsCsCaCertificate.Test xroad view cs ca cert

Test xroad view details
    tests.xroad_trust_view_details_cs_ca.XroadTrustViewDetailsCsCa.Test xroad view details

Test xroad view approved cert
    tests.xroad_trust_view_approved_certification_services.XroadTrustViewApprovedCertService.Test xroad view approved cert

Test xroad verify ts 2
    tests.xroad_cs_view_xroad_members.XroadViewCSMembers.Test xroad verify ts

Test xroad configure service 3
    tests.xroad_configure_service_222.XroadDeleteService.Test xroad configure service

Test xroad configure service 4
    tests.xroad_configure_service_222.XroadDownloadParseURL.Test xroad configure service


*** Keywords ***
setup
    Start recording  ${TEST NAME}

teardown
    ${documentation}=  Generate failure documentation  ${TEST_DOCUMENTATION}  ${TEST NAME}
    Run Keyword If Test Failed  Set test documentation  ${documentation}

    Stop recording

Test suite setup
    log  log suite setup

Test suite teardown
    log  log suite teardown
