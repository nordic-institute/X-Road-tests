*** Settings ***

Suite Setup     Test suite setup
Suite Teardown  Test suite teardown
Test Setup      setup
Test Teardown   teardown

Library     QAutoLibrary.QAutoRobot  testdata=${TESTDATA}


*** Variables ***
${cs_url}=  cs_url
${ss1_url}=  ss1_url

${paths}=  paths
${auth}=  auth
${sign}=  sign
${member_name}=  member_name

${sign_key_label_2}=  ta_generated_key_sign_b
${auth_key_label_2}=  ta_generated_key_auth_b
${member1_configuration}=  member1_configuration
${server_environment}=  server_environment
${approved_ca}=  approved_ca

${True}=  True
${False}=  False

*** Test Cases ***
Test generate and delete cert
    Ss login  ${ss1_url}
    Ss sidebar open keys and certs view
    Ss keys and certs generate and select certificate key in ss  ${sign_key_label_2}
    # Step Delete generated key
    Ss keys and cert click delete cert
    # Step Click delete cert confirm key
    Ss keys and cert dlg delete click delete cert confirm  ${sign_key_label_2}
    # Step Log out security server
    Log out

Test generate cert request
    Ss login  ${ss1_url}
    Ss sidebar open keys and certs view
    Ss keys and certs generate and select certificate key in ss  ${sign_key_label_2}
    Ss keys and certs generate sign certificate request in ss  ${member1_configuration}
    Ss keys and certs verify key request  ${paths}
    Ss keys and certs delete key by label  ${sign_key_label_2}
    Sleep  3
    # Step Click logout
    Log out

Test generate cert request and import
    Ss login  ${ss1_url}
    Ss sidebar open keys and certs view
    Ss keys and certs generate and select certificate key in ss  ${sign_key_label_2}
    Ss keys and certs generate sign certificate request in ss  ${member1_configuration}
    Ss keys and certs verify key and sign certificate_sign  ${paths}
    Ss keys and certs import and upload key certificate  ${sign}
    ${_}  ${cert_key}=  Ss keys and certs verify uploaded certificate  ${sign}
    # Step Delete cert request
    Ss keys and cert delete imported cert key  ${cert_key}

    log  ${cert_key}
    # Step Click delete cert confirm key
    Ss keys and cert dlg delete click delete cert confirm  ${sign_key_label_2}

    ${path_section}=  Get section  ${paths}
    Revoke cert  ${path_section}
    Sleep  3
    # Step Log out from securityserver
    Log out

Test generate cert request and import auth
    Ss login  ${ss1_url}
    Ss sidebar open keys and certs view
    Ss keys and certs generate and select certificate key in ss  ${auth_key_label_2}
    Ss keys and certs generate auth certificate request in ss  ${member1_configuration}
    Ss keys and certs verify key and sign certificate auth  ${paths}
    Ss keys and certs import and upload key certificate  ${auth}
    ${cert_number}  ${cert_key}=  Ss keys and certs verify uploaded certificate  ${auth}
    ${approved_ca_value}=  get parameter  ${server_environment}  ${approved_ca}
    ${key_auth_name}=  Set variable  ${approved_ca_value} ${cert_number}
    Ss keys and certs register auth certificate in ss  ${key_auth_name}  ${member1_configuration}
    Log out

    Cs login  ${cs_url}
    Cs sidebar open security servers view
    # Step Find security server by member name
    ${member_name_parameter}=  Get parameter  ${member1_configuration}  ${member_name}
    Cs sec servers click security servers row with text  ${member_name_parameter}
    # Step Click ss details server
    Cs sec servers click ss details
    Cs sec servers details verify ss details view
    # Step Click authentication certificates
    Cs sec servers details click authentication certificates tab
    # Step Add auth certificate to server
    Cs sec servers details auth click button id securityserver authcert add
    # Step Upload auth cert file
    Cs sec servers auth dlg click upload auth cert
    # Step Make cert file upload
    Ss keys and certs make cert file upload  ${auth}
    Sleep  2
    # Step Submit auth cert add
    Cs sec servers auth dlg click button id auth cert add submit
    Cs sec servers details wait until submitted certificate
    # Step Click mgm requests tab
    Cs sec servers details click mgm requests tab
    Sleep  3
     # Step Find and click mgm request
    Cs sec servers mgm requests find and click mgm request
    Sleep  1
    # Step Accept request in central server
    Cs sec serves mgm request approve click approve request
    Sleep  1
    # Step Click confirm approve request
    Cs sec servers mgm request app conf click confirm approve request
    Sleep  3
    Cs sec servers mgm requests click close mgm req dlg
    Sleep  5
    # Step Log out from central server
    Log out

    Ss login  ${ss1_url}
    Ss sidebar verify sidebar title
    # Step Click keys and cert dev ss
    Ss sidebar click keys and certificates
    Ss keys and cert verify keys and cert title
    # Step Verify that key is registered
    Sleep  100
    Reload page
    Sleep  5

    Ss keys and cert find texts from table keys auth  ${cert_number}

    # Step Delete auth cert request
    Ss keys and cert delete imported cert key  ${cert_key}
    log  ${cert_key}

    # Step Click unregister and delete cert confirm
    Ss keys and cert dlg delete click unregister and delete cert confirm  ${auth_key_label_2}
    # Step Revoke cert
    ${path_section}=  Get section  ${paths}
    Revoke cert auth  ${path_section}
    Sleep  3
    # Step Log out security server
    Log out

*** Keywords ***
setup
    Start recording  ${TEST NAME}

    ${path_section}=  Get section  ${paths}
    Remove cert from downloads  ${path_section}

    Ssh empty all logs from server  ${cs_url}
    Ssh empty all logs from server  ${ss1_url}

teardown
    ${documentation}=  Generate failure documentation  ${TEST_DOCUMENTATION}  ${TEST NAME}
    Run Keyword If Test Failed  Set test documentation  ${documentation}

    ${failure_image_path}=  Get failure image path  ${TEST NAME}
    Run Keyword If Test Failed  Take full screenshot  ${failure_image_path}

    ${path_section}=  Get section  ${paths}
    Remove cert from downloads  ${path_section}
    Get ui error message
    Sleep  1

    # Step log out if logged in
    ${verify_login_page}=  Ss login verify is login page
    Run Keyword If  "${verify_login_page}"=="${False}"  Log out

    Stop recording

Test suite setup
    ${DefaultBrowser}=  Open browser  ${BROWSER}
    Set suite variable  ${DefaultBrowser}  ${DefaultBrowser}

Test suite teardown
    Close all browsers