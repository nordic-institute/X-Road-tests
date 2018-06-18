*** Settings ***

Suite Setup     Test suite setup
Suite Teardown  Test suite teardown
Test Setup      setup
Test Teardown   teardown

Library     QAutoLibrary.QAutoRobot  testdata=${TESTDATA}


*** Variables ***
${cs_url}=  cs_url
${ss1_url}=  ss1_url

${member1_configuration}=  member1_configuration
${member_name}=  member_name
${subsystem_code}=  subsystem_code
${security_server_code}=  security_server_code

${backup_directory}=  /var/lib/xroad/backup

${request_cert_deletion}=  Certificate deletion
${reg_auth_cert_deletion}=  Authentication certificate deletion

${url}=  url

${True}=  True
${False}=  False

*** Test Cases ***
Test deletion of the owner of ss from cs
    # Step Login to central server
    Cs login  ${cs_url}

    # Step Generate central server backup in central server
    Cs sidebar open backup restore_view
    Cs backup generate backup
    Set suite variable  ${restore_cs}  ${True}

    # Step Delete member from cs with ss in central server
    Cs sidebar open members view
    Cs members open member details dlg  ${member1_configuration}  ${member_name}
    Cs members delete member in member details dlg

    # Step Verify members is removed in central server
    Cs members verify members does not contain member  ${member1_configuration}  ${member_name}
    Cs sidebar open security servers view
    Cs sec servers verify servers does not contain server  ${member1_configuration}  ${member_name}

    # Step Verify request comment in central server
    ${request_comment}=  Server request comment  ${member1_configuration}
    Cs sidebar open management request view
    Cs mgm requests open request details dlg  ${request_cert_deletion}
    Cs mgm requests verify comment in request details dlg  ${request_comment}
    Cs mgm requests close request details dlg

Test deletion of xroad member from cs
    # Step Login to central server
    Cs login  ${cs_url}

    # Step Generate central server backup in central server
    Cs sidebar open backup restore view
    Cs backup generate backup
    Set suite variable  ${restore_cs}  ${True}

    # Step Delete member from cs in central server
    Cs sidebar open members view
    Cs members open member details dlg  ${member1_configuration}  ${member_name}
    Cs members delete member in member details dlg

Test deletion of ss from cs
    # Step Login to central server
    Cs login  ${cs_url}

    # Step Generate central server backup in central server
    Cs sidebar open backup restore view
    Cs backup generate backup
    Set suite variable  ${restore_cs}  ${True}

    # Step Delete security server in central server
    Cs sidebar open security servers view
    Cs sec servers open server details dlg  ${member1_configuration}  ${security_server_code}
    Cs sec servers delete server in server details dlg

    # Step Verify member subsystem state in central server
    Cs sidebar open members view
    Cs members open member details dlg  ${member1_configuration}  ${member_name}
    Cs members verify subsystem is removable in member details dlg  ${member1_configuration}  ${subsystem_code}
    Cs members close member details dlg

    # Step Verify request comment in central server
    Cs sidebar open management request view
    ${request_comment}=  Server request comment  ${member1_configuration}
    Cs mgm requests open request details dlg  ${request_cert_deletion}
    Cs mgm requests verify comment in request details dlg  ${request_comment}
    Cs mgm requests close request details dlg

Test deletion of client of ss from cs
    # Step Login to central server
    Cs login  ${cs_url}

    # Step Generate central server backup in central server
    Cs sidebar open backup restore view
    Cs backup generate backup
    Set suite variable  ${restore_cs}  ${True}

    # Step Delete server client in central server
    Cs sidebar open security servers view
    Cs sec servers open server details dlg  ${member1_configuration}  ${security_server_code}
    Cs sec servers delete client in server details dlg  ${member1_configuration}
    Cs sec servers close server details dlg

    # Step Verify member subsystem state in central server
    Cs sidebar open members view
    Cs members open member details dlg  ${member1_configuration}  ${member_name}
    Cs members verify subsystem is removable in member details dlg  ${member1_configuration}  ${subsystem_code}
    Cs members close member details dlg

Test deletion of authentication certificate from cs
    # Step Login to central server
    Cs login  ${cs_url}

    # Step Generate central server backup in central server
    Cs sidebar open backup restore view
    Cs backup generate backup
    Set suite variable  ${restore_cs}  ${True}

    # Step Delete security server auth cert in central server
    Cs sidebar open security servers view
    Cs sec servers open server details dlg  ${member1_configuration}  ${member_name}
    Cs sec servers delete auth cert in server details dlg
    Cs sec servers close server details dlg

    # Step Verify reguest comment in central server
    Cs sidebar open management request view
    Cs mgm requests open request details dlg  ${request_cert_deletion}
    Cs mgm requests verify comment in request details dlg  ${reg_auth_cert_deletion}
    Cs mgm requests close request details dlg

Test deletion of client of ss from ss
    # Step Login to central server
    Cs login  ${cs_url}

    # Step Generate central server backup in central server
    Cs sidebar open backup restore view
    Cs backup generate backup
    Set suite variable  ${restore_cs}  ${True}

    # Step Login to security server
    Ss login  ${ss1_url}

    # Step Generate security server backup in security server
    Ss sidebar open backup restore view
    Ss backup generate backup
    Set suite variable  ${restore_ss}  ${True}
    Sleep  200

    # Step Delete client of security server in security server
    Ss sidebar open security servers client view
    ${member_configuration_section}=  Get section  ${member1_configuration}
    Ss clients find and open by text dlg by subsystem code  ${member_configuration_section}
    Ss clients unregister and delete subsystem in subsystem details dlg

    # Step Open central server url
    Cs open central server url  ${cs_url}

    # Step Verify management request of client deletion in central server
    Cs sidebar open management request view

    # Step Verify subsystem state in central server
    Cs sidebar open members view
    Cs members open member details dlg  ${member1_configuration}  ${member_name}
    Cs members verify subsystem is removable in member details dlg  ${member1_configuration}  ${subsystem_code}
    Cs members close member details dlg


*** Keywords ***
setup
    Start recording  ${TEST NAME}

    Set suite variable  ${restore_ss}  ${False}
    Set suite variable  ${restore_cs}  ${False}

    Empty all logs from server  ${cs_url}
    Empty all logs from server  ${ss1_url}

teardown
    Stop recording

    ${documentation}=  Generate failure documentation  ${TEST_DOCUMENTATION}  ${TEST NAME}
    Run Keyword If Test Failed  Set test documentation  ${documentation}

    ${failure_image_path}=  Get failure image path  ${TEST NAME}
    Run Keyword If Test Failed  Take full screenshot  ${failure_image_path}

    ${cs_url_parameter}=  get_parameter  ${cs_url}  ${url}
    ${ss1_url_parameter}=  get_parameter  ${ss1_url}  ${url}

    # Step Restore central server backup in central server if needed
    Run Keyword If  "${restore_cs}"=="${True}"  Open_url  ${cs_url_parameter}
    Run Keyword If  "${restore_cs}"=="${True}"  Cs sidebar open backup restore view
    Run Keyword If  "${restore_cs}"=="${True}"  Cs backup restore backup

    # Step Restore security server in security server if needed
    Run Keyword If  "${restore_ss}"=="${True}"  Open_url  ${ss1_url_parameter}
    Run Keyword If  "${restore_ss}"=="${True}"  Ss sidebar open backup restore view
    Run Keyword If  "${restore_ss}"=="${True}"  Ss backup restore backup

    Sleep  10

    # Step Log out from central server if logged in
    Open_url  ${cs_url_parameter}
    ${verify_login_page}=  Ss login verify is login page
    Run Keyword If  "${verify_login_page}"=="${False}"  Log out

    # Step Log out from security if logged in
    Open_url  ${ss1_url_parameter}
    ${verify_login_page}=  Cs login verify is login page
    Run Keyword If  "${verify_login_page}"=="${False}"  Log out

    # Step Return server to defaults
    Ssh delete files from directory  ${cs_url}  ${backup_directory}
    Ssh delete files from directory  ${ss1_url}  ${backup_directory}

Test suite setup
    ${DefaultBrowser}=  Open browser  ${BROWSER}
    Set suite variable  ${DefaultBrowser}  ${DefaultBrowser}

Test suite teardown
    Close all browsers

Server request comment
    [Arguments]    ${section}
    ${instance_identifier}=  Get parameter  ${section}  instance_identifier
    ${member_class}=  Get parameter  ${section}  member_class
    ${member_code}=  Get parameter  ${section}  member_code
    ${member_server}=  Get parameter  ${section}  security_server_code
    ${request_comment}=  catenate  'SERVER:${instance_identifier}${/}${member_class}${/}${member_code}${/}${member_server}' deletion
    [Return]  ${request_comment}
