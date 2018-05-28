*** Settings ***
Documentation    Xroad cases for global configurations \n\n
...              See [https://github.com/nordic-institute/X-Road/blob/develop/doc/UseCases/uc-gconf_x-road_use_case_model_for_global_configuration_distribution_1.4_Y-883-8.md|use cases]  for more information


Suite Setup     Test suite setup
Suite Teardown  Test suite teardown
Test Setup      setup
Test Teardown   teardown

Library     QAutoLibrary.QAutoRobot  testdata=${TESTDATA}


*** Variables ***
${cs_url}=  cs_url
${ss1_url}=  ss1_url
${empty_pin}=  empty_pin
${invalid_cs_url}=  invalid_cs_url
${new_cs_url}=  new_cs_url
${whitespace_address}=  whitespace_address
${empty_address}=  empty_address
${long_address}=  long_address
${internal_conf_url}=  internal_conf_url
${configuration_timeout}=  configuration_timeout

${paths}=  paths
${downloads_folder}=  downloads_folder

${valid_part_file}=  ${CURDIR}${/}..${/}data${/}valid_conf_part.xml
${invalid_part_file}=  ${CURDIR}${/}..${/}data${/}invalid_conf_part.xml

# Generated conf part file
${identifier}=  FOO
${ini_file}=  foo.ini
${file_name}=  foo.xml
${existing_val_script}=  ${/}usr${/}share${/}xroad${/}scripts${/}validate-monitoring-params.sh
${missing_val_script}=  ${/}usr${/}share${/}xroad${/}scripts${/}validate.sh

${v2_path}=  ${/}var${/}lib${/}xroad${/}public${/}V2
${internal_conf_path}=  ${v2_path}${/}internalconf
${external_conf_path}=  ${v2_path}${/}externalconf

${xml_ext}=  .xml
${True}=  True
${False}=  False


*** Test Cases ***
Test global configuration view source
    # Step Login to central server and open configuration view
    Cs login  section=${cs_url}
    Cs sidebar open global configuration view

    # Step Verify displayed information internalconf
    Cs conf mgm verify internal configuration view

    # Step Verify displayed information externalconf
    Cs conf mgm verify external configuration view

    # Step Log out
    Log out

Test global configuration download and recreate
    # Step Login to central server and open configuration view
    Cs login  section=${cs_url}
    Cs sidebar open global configuration view

    # Step Download configuration source anchor
    Cs conf mgm download source anchor from cs

    # Step Recreate configuration source anchor
    Cs conf mgm recreate source anchor from cs

    # Step Log out
    Log out

Test optional conf parts
    # Step Login to central server and open configuration view
    Cs login  section=${cs_url}
    Cs sidebar open global configuration view

    # Step Generate optional configuration part file with validation file
    Cs conf mgm generate conf part_file  foo.ini  ${identifier}  ${file_name}  ${existing_val_script}
    # Step Upload configuration part file
    Cs conf mgm upload configuration part file  ${identifier}  ${valid_part_file}
    # Step Download configuration part file
    Cs conf mgm download configuration part file  ${identifier}

    # Step Upload configuration part file fail
    Cs conf mgm upload conf part validation fail  ${identifier}  ${invalid_part_file}

    # Step Generate optional configuration part file with out validation file
    Cs conf mgm generate conf part file  ${ini_file}  ${identifier}  ${file_name}
    # Step Upload configuration part file
    Cs conf mgm upload configuration part file  ${identifier}  ${valid_part_file}

    # Step Generate optional configuration part file with missing validation file
    Cs conf mgm generate conf part file  ${ini_file}  ${identifier}  ${file_name}  ${missing_val_script}
    # Step Upload configuration part file fail missing validation
    Cs conf mgm upload conf part validation fail missing validation  ${identifier}  ${valid_part_file}  ${missing_val_script}

    # Step Delete generated conf part file
    Cs conf mgm delete conf part file  ${ini_file}

    # Step Log out
    Log out

Test login and log out software security token
    # Step Login to central server and open configuration view
    Cs login  section=${cs_url}
    Cs sidebar open global configuration view

    # Step Log out software token
    Cs conf mgm logout software token
    Set suite variable  ${login_to_token}  ${True}

    # Step Log in software token empty pin
    Cs conf mgm log in to software token empty pin  section=${empty_pin}

    # Step Log in software token invalid pin
    Cs conf mgm log in to software token invalid pin  section=${invalid_cs_url}

    # Step Log in software token
    Cs conf mgm log in to software token  section=${cs_url}
    Set suite variable  ${login_to_token}  ${False}

    # Step Log out
    Log out

Test activate and delete config signing key
    # Step Login to central server and open configuration view
    Cs login  section=${cs_url}
    Cs sidebar open global configuration view

    # Step Generate signing key
    Cs conf mgm generate config key

    # Step Activate signing_key
    Cs conf mgm activate newest signing key

    # Step Activate old signing key
    Cs conf mgm activate oldest signing key

    # Step Delete signing key
    Cs conf mgm delete newest signing key

    # Step Generate signing key
    Cs conf mgm generate config key
    # Step Get newest signing key
    ${key}=  Cs conf mgm get newest key id
    # Step Delete signing key from console
    Ssh delete signing key from signer console  section=${cs_url}  key=${key}
    # Step Delete signing key
    Cs conf mgm delete signing key fail  key=${key}

    # Step log out and generate key with out log in
    Cs conf mgm logout software token
    Set suite variable  ${login_to_token}  ${True}
    Cs conf mgm generate config key not logged in  ${cs_url}
    Set suite variable  ${login_to_token}  ${False}
    # Step Delete signing key
    Cs conf mgm delete newest signing key

    # Step Log out
    Log out

Test view sys param and edit address of cs
    # Step Login to central server and open system settings
    Cs login  section=${cs_url}
    Cs sidebar open system settings view

    # Step Change central server url
    Cs system settings change server address  ${new_cs_url}
    # Step Verify edit cs address
    Ssh verify audit log  section=${cs_url}  event=Edit central server address

    # Step Change central server url invalid
    Cs system settings change server address  ${invalid_cs_url}
    # Step Verify edit cs address failed
    Ssh verify audit log  section=${cs_url}  event=Edit central server address failed
    # Step Verify address must be dns
    Common verify notice message  message=Central server address must be DNS name or IP address
    Cs system settings cancel server address dlg

    # Step Change central server url invalid
    Cs system settings change server address  section=${invalid_cs_url}
    # Step Verify edit cs address failed
    Ssh verify audit log  section=${cs_url}  event=Edit central server address failed
    # Step Verify address must be dns
    Common verify notice message  message=Central server address must be DNS name or IP address
    # Step Input valid adress
    Cs system settings input server address in dlg  section=${cs_url}
    Cs system settings confirm server address dlg
    # Step Verify edit cs address
    Ssh verify audit log  section=${cs_url}  event=Edit central server address

    # Step Verify whitespace is parsed
    #Create whitespace address testdata  ${whitespace_address}
    #Cs system settings change server address  section=${whitespace_address}
    #Cs system settings verify central address does not contain whitespace

    # Step Verify parse input empty
    Create empty address testdata  ${empty_address}
    Cs system settings change server address  section=${empty_address}
    # Step Verify address must be dns
    Common verify notice message  message=Missing parameter: centralServerAddress
    Cs system settings cancel server address dlg

    # Step Verify parse input max 255 characters
    create_long_address_testdata  ${long_address}
    Cs system settings change server address  section=${long_address}
    # Step Verify address must be dns
    Common verify notice message  message=Parameter 'centralServerAddress' input exceeds 255 characters
    Cs system settings cancel server address dlg

    # Step Log out
    Log out

Test generate configuration
    # Step Verify if V2 folder exists in server
    Ssh verify if server contains directory  ${cs_url}  ${v2_path}

    # Step Verify external and internal conf files from server
    Ssh verify if server contains file  ${cs_url}  ${internal_conf_path}
    Ssh verify if server contains_file  ${cs_url}  ${external_conf_path}

    # Step Verify configuration directory time
    ${configuration_timeout_parameter}=  Get parameter  ${cs_url}  ${configuration_timeout}
    Sleep  ${configuration_timeout_parameter}

    ${v2_newest_dir}=  Ssh get newest directory  ${cs_url}  ${v2_path}
    ${time_since_last_generation}=  Ssh get newest directory age

    Log  Set configuration timeout ${configuration_timeout_parameter}
    Log  Time since last dir generation ${time_since_last_generation}
    Should Be True 	${configuration_timeout_parameter} > ${time_since_last_generation}

    # Step Verify newest configuration directory content
    ${newest_directory_path}=  Set Variable  ${v2_path}${/}${v2_newest_dir}
    ${private_xml_file}=  Set Variable  ${newest_directory_path}${/}private-params.xml
    ${shared_xml_file}=  Set Variable  ${newest_directory_path}${/}shared-params.xml

    Ssh verify if server contains file  ${cs_url}  ${private_xml_file}
    Ssh verify if server contains file  ${cs_url}  ${shared_xml_file}

    # Step Login to central server and open configuration view
    Cs login  section=${cs_url}
    Cs sidebar open global configuration view

    # Step Log out software token
    Cs conf mgm logout software token
    Set suite variable  ${login_to_token}  ${True}

    # Step Verify global configuration failing
    Sleep  ${configuration_timeout_parameter}
    Reload_page
    Common verify alert message  Global configuration generation failing since
    Ssh verify jetty log  ${cs_url}  Processing internal configuration failed:

    # Step Log in software token
    Cs conf mgm log in to software token  section=${cs_url}
    Set suite variable  ${login_to_token}  ${False}

    # Step Log out
    Log out

Test handle configuration download request
    # Step Test internalconf url download
    ${internal_conf_url_parameter}=  Get parameter  ${cs_url}  ${internal_conf_url}
    log  ${internal_conf_url_parameter}
    ${content}=  Ssh curl url  ${cs_url}  ${internal_conf_url_parameter}
    Should not contain any  ${content}  404 Not Found
    log  ${content}

*** Keywords ***
setup
    Start recording  ${TEST NAME}

    ${download_folder}=  Get parameter  ${paths}  ${downloads_folder}
    ${paths_section}=  Get section  ${paths}

    Set suite variable  ${login_to_token}  ${False}

    Remove anchor and certs from downloads  ${paths_section}
    Delete files with extension  ${download_folder}  ${xml_ext}
    Empty all logs from server  ${cs_url}
    Empty all logs from server  ${ss1_url}

teardown
    ${stop_log_time}=  Get log utc time
    ${test_data_section}=  Get section  ${cs_url}
    ${download_folder_param}=  Get parameter  ${paths}  ${downloads_folder}

    ${documentation}=  Generate failure documentation  ${TEST_DOCUMENTATION}  ${TEST NAME}
    Run Keyword If Test Failed  Set test documentation  ${documentation}

    ${failure_image_path}=  Get failure image path  ${TEST NAME}
    Run Keyword If Test Failed  Take full screenshot  ${failure_image_path}

    ${verify_login_page}=  Ss login verify is login page
    Run Keyword If  "${login_to_token}"=="${True}"  Cs sidebar open global configuration view
    Run Keyword If  "${login_to_token}"=="${True}"  Cs conf mgm log in to software token  section=${cs_url}
    Run Keyword If  "${login_to_token}"=="${True}" and "${verify_login_page}'"=="${True}"  Cs login  section=${cs_url}

    Open application url  ${TestDataSection}

    # Step log out if logged in
    ${verify_login_page}=  Ss login verify is login page
    Run Keyword If  "${verify_login_page}"=="${False}"  Log out

    # Step revert to defaults
    Delete files with extension  ${download_folder_param}  ${xml_ext}

    Cs conf mgm delete conf part file  ${ini_file}  try_expect=${True}

    Stop recording

Test suite setup
    ${DefaultBrowser}=  Open browser  ${BROWSER}
    Set suite variable  ${DefaultBrowser}  ${DefaultBrowser}

Test suite teardown
    Close all browsers
