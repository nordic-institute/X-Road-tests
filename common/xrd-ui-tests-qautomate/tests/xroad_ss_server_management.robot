*** Settings ***
Documentation    Xroad cases for security server management test cases \n\n
...              See [https://github.com/nordic-institute/X-Road/blob/develop/doc/UseCases/uc-ss_x-road_use_case_model_for_security_server_management_1.4_Y-883-4.md|use cases] for more information

Suite Setup     Test suite setup
Suite Teardown  Test suite teardown
Test Setup      setup
Test Teardown   teardown

Library     QAutoLibrary.QAutoRobot  testdata=${TESTDATA}


*** Variables ***
${cs_url}=  cs_url
${ss1_url}=  ss1_url
${security_server_url_wrong_password}=  security_server_url_wrong_password

${login_user}=  Log in user
${logout_user}=  Log out user
${login_user_failed}=  Log in user failed
${login_restore_in_progress}=  Restore in progress, try again later
${authentication_failed}=  Authentication failed

${backup_directory}=  /var/lib/xroad/backup
${lanquage_eng}=  ENGLISH (EN)
${set_ui_language}=  Set UI language
${version_text}=  Security Server version 6

${delete_timestamping_services}=  Delete timestamping service
${add_timestamping_services}=  Add timestamping service
${add_timestamping_services_failed}=  Add timestamping service failed


${True}=  True
${False}=  False

*** Test Cases ***
Test login and logout ss gui

    # Step Open security server for login add user name password
    # Step System verify's login success and log file
    Ss login  ${ss1_url}

    # Step System logs the event "Log in user" to the audit log
    Ssh verify audit log  ${ss1_url}  ${login_user}

    # Step Log out from system GUI
    Log out

    # Step System logs the event “Log out user” to the audit log.
    Ssh verify audit log  ${ss1_url}  ${logout_user}

Test login with wrong password
    # Step Open security server The user with the inserted user name does not exist or the password is incorrect.
    Ss login  ${security_server_url_wrong_password}  initial_conf=${True}  wait_for_jquery=${False}

    # Step System displays the error message “Authentication failed”.
    Ss verify login fail  ${authentication_failed}
    Ssh verify audit log  ${ss1_url}  ${login_user_failed}

Test login restore back up in process
    # Step Open browser and start restoring backup
    Open browser
    Ss login  ${ss1_url}
    Ss sidebar open backup restore view
    Ss backup generate backup
    Ss backup restore click element first row restore
    Ss backup restore confirm restore click button confirm  ${False}
    Close browser

    # Step Open security server for login add user name password
    Ss login  ${ss1_url}  initial_conf=${True}  wait_for_jquery=${False}

    # The system is currently undergoing the system restore process.
    # 3a.1. System displays the error message “Restore in progress, try again later”.
    Ss verify login fail  ${login_restore_in_progress}
    # 3a.2. System logs the event “Log out user” to the audit log.
    Ssh verify audit log  ${ss1_url}  ${logout_user}
    # TODO add verification that back up is done
    Sleep  120

Test change language
    # Step Open security server for login add user name password
    Ss login  ${ss1_url}

    # Step Change language
    Common open select language_dlg
    Common change language in dlg  ${lanquage_eng}
    Common accept select language dlg

    # Step Verify audit log for language change
    Ssh verify audit log  ss1_url  ${set_ui_language}

Test view installed software version
    # Step Open security server for login add user name password
    Ss login  ${ss1_url}

    # Step Open version view
    Ss sidebar open version view

    # Step Verify version
    Ss version verify version  ${version_text}

    # Step Log out
    Log out

Test timestamping services
    # Add timestamping service, view timestamping service, try add existing tsp service and delete tsp service
    # Step Open security server for login add user name password
    Ss login  ss1_url
    Ss sidebar open system parameters view

    # Step Delete timestamp services
    Ss delete timestamping url from ss  ${cs_url}
    Ssh verify audit log  ${ss1_url}  ${delete_timestamping_services}

    # Step Add timestamp services
    Ss add timestamping url to ss  ${cs_url}
    Ssh verify audit log  ${ss1_url}  ${add_timestamping_services}

    # Step Add timestamp services fail
    Ss add timestamping url to ss  ${cs_url}
    Ssh verify audit log  ${ss1_url}  ${add_timestamping_services_failed}

    # Step Log out
    Log out

Test view certificate details
    # Step Open security server for login add user name password
    Ss login  ${ss1_url}  ${False}  ${True}

    # Step View certificate details
    Ss sidebar open keys and certs view
    Ss keys and certs verify details dlg

    # Step Log out
    Log out

Test open multiple diagnostics simultaneously
    Ss login  ${ss1_url}  ${False}  ${True}

    ${browser2}=  Open browser
    Ss login  ${ss1_url}  ${False}  ${True}

    Switch_browser  ${DefaultBrowser}
    Ss sidebar open diagnostics view

    Switch_browser  ${browser2}
    Ss sidebar open diagnostics view
    Close_browser

    Log out

*** Keywords ***
setup
    Start recording  ${TEST NAME}

    Empty all logs from server  ${ss1_url}

teardown
    ${documentation}=  Generate failure documentation  ${TEST_DOCUMENTATION}  ${TEST NAME}
    Run Keyword If Test Failed  Set test documentation  ${documentation}

    ${failure_image_path}=  Get failure image path  ${TEST NAME}
    Run Keyword If Test Failed  Take full screenshot  ${failure_image_path}

    # Step log out if logged in
    ${verify_login_page}=  Ss login verify is login page
    Run Keyword If  "${verify_login_page}"=="${False}"  Log out

    Stop recording

Test suite setup
    ${DefaultBrowser}=  Open browser  ${BROWSER}
    Set suite variable  ${DefaultBrowser}  ${DefaultBrowser}

Test suite teardown
    Close all browsers
    Ssh delete files from directory  ${cs_url}  ${backup_directory}

