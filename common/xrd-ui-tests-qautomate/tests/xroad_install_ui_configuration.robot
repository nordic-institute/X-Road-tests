*** Settings ***

Suite Setup     Test suite setup
Suite Teardown  Test suite teardown
Test Setup      setup
Test Teardown   teardown

Library     QAutoLibrary.QAutoRobot  testdata=${TESTDATA}


*** Variables ***
${cs_url}=  cs_url
${ss1_url}=  ss1_url
${ss2_url}=  ss2_url
${ss_mgm_url}=  ss_mgm_url
${service_mgm_address}=  service_mgm_address
${member1_configuration}=  member1_configuration
${member2_configuration}=  member2_configuration
${member_mgm_configuration}=  member_mgm_configuration

${paths}=  paths
${server_environment}=  server_environment
${approved_ca}=  approved_ca
${sync_timeout}=  sync_timeout
${auth}=  auth
${sign}=  sign

${service_wsdl_client_reg}=  service_wsdl_client_reg
${service_wsdl_client_deletion}=  service_wsdl_client_deletion
${service_wsdl_auth_cert_deletion}=  service_wsdl_auth_cert_deletion
${wsdl_service_auth_cert_deletion}=  wsdl_service_auth_cert_deletion
${wsdl_service_client_deletion}=  wsdl_service_client_deletion
${wsdl_service_client_reg}=  wsdl_service_client_reg


*** Test Cases ***

Test configure cs and ss mgm servers 1
    # Step Initialize server and add new member in central server
    Cs login  ${cs_url}  initial_conf=True
    Cs system settings initialize cs server config  ${cs_url}
    Cs system settings add init member class  ${member_mgm_configuration}

    # Step Add CA certification services in central server
    Cs sidebar open certification services view
    Cs cert services add certification service and upload ca root to cs  ${paths}  ${cs_url}  ${server_environment}

    # Step Add timestamping to central server
    Cs sidebar open timestamping services view
    Cs tsp services add timestamping service to cs  ${paths}  ${cs_url}

    # Step Add members to central server
    Cs sidebar open members view
    Cs members add member to cs  ${member_mgm_configuration}

    # Step Add subsystem code to central server
    Cs members add new subsystem to existing member in cs  ${member_mgm_configuration}

    # Step Edit management service in central server
    Cs sidebar open system settings view
    Cs system settings edit mgm service provider in cs  ${member_mgm_configuration}

    # Step Set global conf internal conf key in central server
    Cs sidebar open global configuration view
    Cs conf mgm generate config key  key_type=internal
    Cs conf mgm try insert pin code  ${cs_url}
    Wait until jquery ajax loaded

    # Step Set global conf external key in central server
    Cs conf mgm click link external configuration
    Cs conf mgm generate config key  key_type=external

    ## Might show double pin dialog
    Cs conf mgm try insert pin code  ${cs_url}
    Wait until jquery ajax loaded

    # Step set OCSP responder in central server
    Cs sidebar open certification services view
    Cs cert services add new ocsp responder  ${cs_url}
    Log out
    Sleep  30

    # Step Download anchor from central server
    Cs login  ${cs_url}
    Cs sidebar open global configuration view
    Cs conf mgm download source anchor from cs
    Log out

    # Step Import configuration anchor to security server
    Ss login  ${ss_mgm_url}  initial_conf=True
    Ss initial conf import configuration anchor  ${paths}
    Ss initial conf add initial server configuration values to ss  ${member_mgm_configuration}  ${ss_mgm_url}

    # Step Verify token active in security server
    Ss sidebar verify sidebar title
    Ss sidebar open keys and certs view
    Ss keys and certs active token and insert pin code if needed  ${ss_mgm_url}

    # Step Add timestamping services to security server
    Ss sidebar verify sidebar title
    Ss sidebar open system parameters view
    Ss add timestamping url to ss  ${ss_mgm_url}

    # Step Add sign certificate to security server
    Ss sidebar open keys and certs view
    Ss keys and certs generate and select certificate key in ss  ta_generated_key_${sign}
    Ss keys and certs generate sign certificate request in ss  ${member_mgm_configuration}
    Ss keys and certs verify key and sign certificate sign  ${paths}
    Ss keys and certs import and upload key certificate  ${sign}
    Ss keys and certs verify uploaded certificate  ${sign}

    # Step Add auth certificate to security serverta_generated_key_auth
    Ss sidebar open keys and certs view
    Ss keys and certs generate and select certificate key in ss  ta_generated_key_${auth}
    Ss keys and certs generate auth certificate request in ss  ${member_mgm_configuration}
    Ss keys_and_certs verify key and sign certificate auth  ${paths}
    Ss keys and certs import and upload key certificate  ${auth}
    ${cert_number}  ${_}=  Ss keys and certs verify uploaded certificate  ${auth}
    ${approved_ca_value}=  get parameter  ${server_environment}  ${approved_ca}
    ${key_auth_name}=  Set variable  ${approved_ca_value} ${cert_number}

    # Step Register request auth certificate and activate
    Ss keys and certs register auth certificate in ss  ${key_auth_name}  ${member_mgm_configuration}
    Ss keys and cert click cert activate
    # Step Log out securityserver
    Log out

    # Step Accept auth key request in central server
    Cs login  ${cs_url}
    Cs sidebar open members view
    Cs members accept auth certificate request in cs  ${member_mgm_configuration}

    # Step Copy WSDL addressitle PHASE 17 -> COPY WSDL AND REGISTER SUBSYSTEM IN CS
    Cs sidebar open system settings view
    Cs system settings copy wsdl addresses in cs  ${cs_url}

    # Step Register subsystem in central server
    Cs system settings register subsystem system settings in cs  ${member_mgm_configuration}
    Log out

    ${sync_timeout_value}=  Get parameter  ${cs_url}  ${sync_timeout}
    Sync global conf  ${sync_timeout_value}

    # Step Add subsystem to security server
    Ss login  ${ss_mgm_url}
    Ss sidebar verify sidebar title
    Ss clients add from search existing client in ss  ${member_mgm_configuration}
    Sleep  2
    Log out
    Sleep  30

    # Step Add WSDL service to security server subsystem
    Ss login  ${ss_mgm_url}
    Ss clients open clients details dlg with subsystem code  ${member_mgm_configuration}
    Ss services add new wsdl  ${cs_url}
    Ss clients dlg services click wsdl enable
    Sleep  2
    Ss clients dlg services open wsdl service

    # Step Add management service parameters to auth cert deletion
    Ss services edit wsdl service parameters in ss  ${wsdl_service_auth_cert_deletion}  ${service_wsdl_auth_cert_deletion}  ${cs_url}  ${service_mgm_address}
    Ss services add service access rights to all in ss

    # Step Add management service parameters to client deletion
    Ss services edit wsdl service parameters in ss  ${wsdl_service_client_deletion}  ${service_wsdl_client_deletion}  ${cs_url}  ${service_mgm_address}
    Ss services add service access rights to all in ss

    # Step Add management service parameters to auth client registration
    Ss services edit wsdl service parameters in ss  ${wsdl_service_client_reg}  ${service_wsdl_client_reg}  ${cs_url}  ${service_mgm_address}
    Ss services add service access rights to all in ss
    Ss clients dlg services click close services dlg
    Log out
    Sleep  2

Test configure ss server with new member add to existing cs 3
    # Step Add new member to central server
    Cs login  ${cs_url}
    Cs sidebar open members view
    Cs members add member to cs  ${member1_configuration}

    # Step Add new subsystem to to existing member
    Cs members add new subsystem to existing member in cs  ${member1_configuration}

    # Step Download anchor from central server
    Cs sidebar open global configuration view
    Cs conf mgm download source anchor from cs
    Log out

    Sleep  41

    # Step Import configuration anchor to security server
    Ss login  ${ss1_url}  initial_conf=True
    Ss initial conf import configuration anchor  ${paths}
    Ss initial conf add initial server configuration values to ss  ${member1_configuration}  ${ss1_url}

    # Step Verify and insert pin if needed in security server
    Ss sidebar verify sidebar title
    Ss sidebar open keys and certs view
    Ss keys and certs active token and insert_pin code if needed  ${ss1_url}

    # Step Add timestamping services to security server
    Ss sidebar open system parameters view
    Ss add timestamping url to ss  ${ss1_url}

    # Step Add sign certificate to security server
    Ss sidebar verify sidebar title
    Ss sidebar open keys and certs view
    Ss keys and certs generate and select certificate key in ss  ta_generated_key_${sign}
    Ss keys and certs generate sign certificate request in ss  ${member1_configuration}
    Ss keys and certs verify key and sign certificate sign  ${paths}
    Ss keys and certs import and upload key certificate  ${sign}
    Ss keys and certs verify uploaded certificate  ${sign}

    # Step Add auth certificate to security server
    Ss sidebar open keys and certs view
    Ss keys and certs generate and select certificate key in ss  ta_generated_key_${auth}
    Ss keys and certs generate auth certificate request in ss  ${member1_configuration}
    Ss keys and certs verify key and sign certificate auth  ${paths}
    Ss keys and certs import and upload key certificate  ${auth}

    ${cert_number}  ${_}=  Ss keys and certs verify uploaded certificate  ${auth}
    ${approved_ca_value}=  Get parameter  ${server_environment}  ${approved_ca}
    ${key_auth_name}=  Set variable  ${approved_ca_value} ${cert_number}

    # Step Register request auth certificate and activate
    Ss keys and certs register auth certificate in ss  ${key_auth_name}  ${member1_configuration}
    Ss keys and cert click cert activate
    Log out

    # Step Accept auth key request in central server
    Cs login  ${cs_url}
    Cs sidebar open members view
    Cs members accept auth certificate request in cs  ${member1_configuration}

    # Step Get WSDL address
    Cs sidebar open system settings view
    # Step Get wsdl and services address #Webpage: cs_system_settings
    ${cs_url_section}=  Get section  ${cs_url}
    Cs system settings get wsdl and services address  ${cs_url_section}
    Log out

    # Step Add subsystem to central server
    Cs login  ${cs_url}
    Cs sidebar open members view
    Cs members new client registration request in cs  ${member1_configuration}
    Cs sec servers mgm requests click close mgm req dlg
    Cs members close member details dlg
    Log out

    ${sync_timeout_value}=  Get parameter  ${cs_url}  ${sync_timeout}
    Sync global conf  ${sync_timeout_value}

    # Step Add subsystem to security server
    Ss login  ${ss1_url}
    Ss clients add new subsystem to ss  ${member1_configuration}
    Log out

    Sleep   10

    # Step Accept subsystem in in central server
    Cs login  ${cs_url}
    Cs sidebar open members view
    Cs members accept mgm requests in cs  ${member1_configuration}
    Log out

    Sync global conf  ${sync_timeout_value}

    # Step Check registration complete
    Ss login  ${ss1_url}
    Ss sidebar verify sidebar title
    # Step Check service registration complete #Webpage: ss_clients #Parameters: server_configuration
    ${member1_configuration_section}=  Get section  ${member1_configuration}
    ss clients verify service registration complete  ${member1_configuration_section}
    Log out

Test configure ss server with new member add to existing cs 4
    # Step Add new member to central server
    Cs login  ${cs_url}
    Cs sidebar open members view
    Cs members add member to cs  ${member2_configuration}

    # Step Add new subsystem to to existing member
    Cs members add new subsystem to existing member in cs  ${member2_configuration}

    # Step Download anchor from central server
    Cs sidebar open global configuration view
    Cs conf mgm download source anchor from cs
    Log out

    ${sync_timeout_value}=  Get parameter  ${cs_url}  ${sync_timeout}
    Sync global conf  ${sync_timeout_value}

    # Step Import configuration anchor to security server
    Ss login  ${ss2_url}  initial_conf=True
    Ss initial conf import configuration anchor  ${paths}
    Ss initial conf add initial server configuration values to ss  ${member2_configuration}  ${ss2_url}

    # Step Verify and insert pin if needed in security server
    Ss sidebar verify sidebar title
    Ss sidebar open keys and certs view
    Ss keys and certs active token and insert_pin code if needed  ${ss2_url}

    # Step Add timestamping services to security server
    Ss sidebar open system parameters view
    Ss add timestamping url to ss  ${ss2_url}

    # Step Add sign certificate to security server
    Ss sidebar verify sidebar title
    Ss sidebar open keys and certs view
    Ss keys and certs generate and select certificate key in ss  ta_generated_key_${sign}
    Ss keys and certs generate sign certificate request in ss  ${member2_configuration}
    Ss keys and certs verify key and sign certificate sign  ${paths}
    Ss keys and certs import and_upload_key_certificate  ${sign}
    Ss keys and certs verify uploaded certificate  ${sign}

    # Step Add auth certificate to security server
    Ss sidebar open keys and certs view
    Ss keys and certs generate and select certificate key in ss  ta_generated_key_${auth}
    Ss keys and certs generate auth certificate request in ss  ${member2_configuration}
    Ss keys and certs verify key and sign certificate auth  ${paths}
    Ss keys and certs import and upload key certificate  ${auth}

    ${cert_number}  ${_}=  Ss keys and certs verify uploaded certificate  ${auth}
    ${approved_ca_value}=  Get parameter  ${server_environment}  ${approved_ca}
    ${key_auth_name}=  Set variable  ${approved_ca_value} ${cert_number}

    # Step Register request auth certificate and activate
    Ss keys and certs register auth certificate in ss  ${key_auth_name}  ${member2_configuration}
    Ss keys and cert click cert activate
    Log out

    # Step Accept auth key request in central server
    Cs login  ${cs_url}
    Cs sidebar open members view
    Cs members accept auth certificate request in cs  ${member2_configuration}

    # Step Get WSDL address
    Cs sidebar open system settings view
    # Step Get wsdl and services address #Webpage: cs_system_settings
    ${cs_url_section}=  Get section  ${cs_url}
    Cs system settings get wsdl and services address  ${cs_url_section}
    Log out

    # Step Add subsystem to central server
    Cs login  ${cs_url}
    Cs sidebar open members view
    Cs members new client registration request in cs  ${member2_configuration}
    Cs sec servers mgm requests click close mgm req dlg
    Cs members close member details dlg
    Log out

    Sync global conf  ${sync_timeout_value}

    # Step Add subsystem to security server
    Ss login  ${ss2_url}
    Ss clients add new subsystem to ss  ${member2_configuration}
    Log out

    Sleep   10

    # Step Accept subsystem in in central server
    Cs login  ${cs_url}
    Cs sidebar open members view
    Cs members accept mgm requests in cs  ${member2_configuration}
    Log out

    Sync global conf  ${sync_timeout_value}

    # Step Check registration complete
    Ss login  ${ss2_url}
    Ss sidebar verify sidebar title
    # Step Check service registration complete #Webpage: ss_clients #Parameters: server_configuration
    ${member2_configuration_section}=  Get section  ${member2_configuration}
    ss clients verify service registration complete  ${member2_configuration_section}
    Log out

*** Keywords ***
setup
    Start recording  ${TEST NAME}

    ${paths_section}=  Get section  ${paths}

    Remove anchor and certs from downloads  ${paths_section}
    Empty all logs from server  ${cs_url}
    Empty all logs from server  ${ss1_url}
    Empty all logs from server  ${ss2_url}
    Empty all logs from server  ${ss_mgm_url}

teardown
    ${paths_section}=  Get section  ${paths}

    Get ui error message
    Remove anchor and certs from downloads  ${paths_section}

    ${documentation}=  Generate failure documentation  ${TEST_DOCUMENTATION}  ${TEST NAME}
    Run Keyword If Test Failed  Set test documentation  ${documentation}

    ${failure_image_path}=  Get failure image path  ${TEST NAME}
    Run Keyword If Test Failed  Take full screenshot  ${failure_image_path}

    Stop recording

Test suite setup
    ${DefaultBrowser}=  Open browser  ${BROWSER}
    Set suite variable  ${DefaultBrowser}  ${DefaultBrowser}

Test suite teardown
    Close all browsers
