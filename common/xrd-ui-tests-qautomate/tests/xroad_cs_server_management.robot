*** Settings ***
Documentation    Xroad cases for central management test cases \n\n
...              See [https://github.com/nordic-institute/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md|use cases]  for more information

Suite Setup     Test suite setup
Suite Teardown  Test suite teardown
Test Setup      setup
Test Teardown   teardown

Library     QAutoLibrary.QAutoRobot  testdata=${TESTDATA}


*** Variables ***
${cs_url}=  cs_url

${paths}=  paths
${downloads_folder}=  downloads_folder

${backup_directory}=  /var/lib/xroad/backup
${lanquage_eng}=  ENGLISH (EN)
${set_ui_language}=  Set UI language
${version_text}=  Central Server version 6

${tar}=  .tar
${True}=  True
${False}=  False

*** Test Cases ***
Test change the graphical user interface language
    # Step Open central server
    Cs login  ${cs_url}  ${False}

    # Step Change language
    Common open select language_dlg
    Common change language in dlg  ${lanquage_eng}
    Common accept select language dlg

    # Step Verify audit log for language change
    Ssh verify audit log  cs_url  ${set_ui_language}

    # Step Log out of central server
    Log out

Test view the installed software version
    # Step login to central server
    Cs login  ${cs_url}  ${False}

    # Step open version view
    Cs sidebar open version view

    # Step verify version
    Cs version verify version  ${version_text}

    # Step log out of central server
    Log out

Test view backup list
    # Step Login to central server
    Cs login  ${cs_url}  ${False}

    # Step Open backup view
    Cs sidebar open backup restore view

    # Step Generate backup
    Cs backup generate backup

    # Step Verify backup view user actions
    Cs backup restore verify contains all user actions

    # Step Log out of central server
    Log_out

Test backup configuration
    # Step Login to central server
    Cs login  ${cs_url}  ${False}

    # Step Open backup view
    Cs sidebar open backup restore view

    # Step Generate backup
    Cs backup generate invalid backup

    # Step Generate backup
    Cs backup generate backup

    # Step Log out of central server
    Log out

Test restore backup
    # Step Login to central server
    Cs login  ${cs_url}  ${False}

    # Step Open backup view
    Cs sidebar open backup restore view

    # Step Restore invalid backup
    Cs backup restore invalid backup

    # Step Generate backup
    Cs backup generate backup

    # Step Cancel restore backup
    Cs backup cancel restore backup

    # Step Restore backup
    Cs backup restore backup

    # Step Log out of central server
    Log out

Test download backup
    # Step Login to central server
    Cs login  ${cs_url}  ${False}

    # Step Open backup view
    Cs sidebar open backup restore view

    # Step Generate backup
    Cs backup generate backup

    # Step Download backup
    Cs backup download backup

    # Step Log out of central server
    Log out

Test delete backup
    # Step Login to central server
    Cs login  ${cs_url}  ${False}

    # Step Open backup view
    Cs sidebar open backup restore view

    # Step Generate backup
    Cs backup generate backup

    # Step Cancel delete backup
    Cs backup cancel delete backup

    # Step Delete backup
    Cs backup delete backup

    # Step Log out of central server
    Log out

Test upload backup
    # Step Login to central server
    Cs login  ${cs_url}  ${False}

    # Step Open backup view
    Cs sidebar open backup restore view

    # Step Generate backup
    Cs backup generate backup

    # Step Download backup
    Cs backup download backup

    # Step Delete backup
    Cs backup delete backup

    # Step Upload backup
    Cs backup upload backup

    # Step Upload backup that already exists
    Cs backup upload backup already exists

    # Step Upload backup with invalid characters in name
    Cs backup upload backup invalid char

    # Step Upload backup with invalid extension
    Cs backup upload backup invalid extension

    # Step Upload backup with invalid format
    Cs backup upload backup invalid format

    # Step Log out of central server
    Log out


*** Keywords ***
setup
    Start recording  ${TEST NAME}

    Empty all logs from server  ${cs_url}

teardown
    ${download_folder_param}=  Get parameter  ${paths}  ${downloads_folder}

    ${documentation}=  Generate failure documentation  ${TEST_DOCUMENTATION}  ${TEST NAME}
    Run Keyword If Test Failed  Set test documentation  ${documentation}

    ${failure_image_path}=  Get failure image path  ${TEST NAME}
    Run Keyword If Test Failed  Take full screenshot  ${failure_image_path}

    # Step log out if logged in
    ${verify_login_page}=  Ss login verify is login page
    Run Keyword If  "${verify_login_page}"=="${False}"  Log out

    # Step Return server to defaults
    Delete files with extension  ${download_folder_param}  ${tar}
    Ssh delete files from directory  ${cs_url}  ${backup_directory}

    Stop recording

Test suite setup
    ${DefaultBrowser}=  Open browser  ${BROWSER}
    Set suite variable  ${DefaultBrowser}  ${DefaultBrowser}

Test suite teardown
    Close all browsers
