# -*- coding: utf-8 -*-
import subprocess
import os
from QAutoLibrary.extension import TESTDATA
import glob
from urlparse import urlparse
from selenium.webdriver.common.by import By
from QAutoLibrary.QAutoSelenium import *
from time import sleep

# Library file allows define common methods, which can be
# added to test cases or page models
from pagemodel.common_elements import Common_elements

class Common_lib(CommonUtils):
    """
    Common library that contains useful methods for testing

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_elements = Common_elements()

    def sync_global_conf(self, parameters=None):
        """

        :param parameters:  Test data section dictionary
        """
        print("Waiting global conf sync time: " + str(parameters))
        sleep(float(parameters))

    def log_out(self):
        """

        """
        print("waiting logout")
        sleep(2)
        self.wait_until_jquery_ajax_loaded()
        self.common_elements.click_user_info()
        sleep(2)
        try:
            self.common_elements.click_log_out()
        except:
            current_url = urlparse(self.get_current_url())
            current_url = current_url.scheme + "://" + current_url.netloc + "/login/logout"
            print(current_url)
            self.go_to(current_url)
            self.warning("Logged out using browser url")
        sleep(2)

    def verify_cert_request(self, parameters):
        """

        :param parameters:  Test data section dictionary
        """
        # Wait while for downloading der file
        sleep(10)
        try:
            newest_der = max(glob.iglob(parameters[u'downloads_folder'] + '*.der'), key=os.path.getctime)
            print(newest_der)
        except:
            print("Certificate download failed")
            print(subprocess.check_output("ls " + parameters[u'downloads_folder'], shell=True))
            raise Exception("Certificate download failed")

        cert_string = subprocess.check_output("openssl req -in " +  newest_der + " -text -noout -inform DER", shell=True)
        begin_index = str(cert_string).find("Subject:")
        end_index = str(cert_string).find("Subject Public Key")
        print(str(cert_string)[begin_index:end_index])
        return True

    def remove_anchor_and_certs_from_downloads(self, parameters):
        """

        :param parameters:  Test data section dictionary
        """
        self.delete_files_with_extension(parameters[u'downloads_folder'], ".p10")
        self.delete_files_with_extension(parameters[u'downloads_folder'], ".der")
        self.delete_files_with_extension(parameters[u'downloads_folder'], ".pem")
        self.delete_files_with_extension(parameters[u'downloads_folder'], ".xml")

    def remove_cert_from_downloads(self, parameters):
        """

        :param parameters:  Test data section dictionary
        """
        self.delete_files_with_extension(parameters[u'downloads_folder'], ".der")

    def delete_files_with_extension(self, folder, extension):
        """

        """
        files = glob.iglob(folder + '*' + extension)
        for _file in files:
            print ("delete file: ", _file)
            try:
                os.system("sudo rm " + _file)
            except:
                print("Could not delete", _file, "file from Downloads")

    def read_cert_number_request(self, cert_type):
        """

        """
        cert_number = subprocess.check_output("openssl x509 -in " +  "scripts/" + cert_type + "-cert_automation.der" + " -serial -noout", shell=True)
        print(cert_number)
        cert_number = cert_number.split('=')
        number_decimal = int("0x" + str(cert_number[1].lower()), 16)
        print(number_decimal)
        return str(number_decimal)

    def copy_and_sign_cert_request(self, parameters):
        """

        :param parameters:  Test data section dictionary
        """
        print("copy and sign start")
        print(os.getcwd() + "\n")
        call_string = "./scripts/copy_and_sign.sh " + parameters[u'downloads_folder'] + " " + parameters[u'sign_cert_format'] + " '" + parameters[u'sign_cert_server_connect_parameters'] + " sign-sign'"
        print(call_string)
        subprocess.call(call_string,shell=True)

    def copy_and_auth_cert_request(self, parameters):
        """

        :param parameters:  Test data section dictionary
        """
        print("copy and auth start")
        print(os.getcwd() + "\n")
        call_string = "./scripts/copy_and_auth.sh " + parameters[u'downloads_folder'] + " " + parameters[u'sign_cert_format'] + " '" + parameters[u'sign_cert_server_connect_parameters'] + " sign-auth'"
        print(call_string)
        subprocess.call(call_string,shell=True)

    def revoke_cert(self, parameters):
        """

        :param parameters:  Test data section dictionary
        """
        print("revoke start")
        print("./scripts/revoke.sh " + parameters[u'sign_cert_format'] + " " + parameters[u'sign_cert_server_connect_parameters'])
        subprocess.call("./scripts/revoke.sh " + parameters[u'sign_cert_format'] + " '" + parameters[u'sign_cert_server_connect_parameters'] + "'",shell=True)
        os.system("sudo mv " + "scripts/sign-cert_automation.der old.der" )

    def revoke_cert_auth(self, parameters):
        """
        :param parameters:  Test data section dictionary
        """
        print("revoke auth start")
        subprocess.call("./scripts/revoke_auth.sh " + parameters[u'sign_cert_format'] + " '" + parameters[u'sign_cert_server_connect_parameters'] + "'",shell=True)
        os.system("sudo mv " + "scripts/auth-cert_automation.der old.der" )

    def get_ui_error_message(self):
        """

        """
        if self.is_visible((By.CLASS_NAME, u'alerts'), 2):
            msg = self.get_text((By.CLASS_NAME, u'alerts'))
            print("ALERT IS PRESENT: " + msg)
        if self.is_visible((By.CLASS_NAME, u'message'), 1):
            msg = self.get_text((By.CLASS_NAME, u'message'))
            print("MESSAGE: " + msg)

    def get_log_utc_time(self):
        """

        """
        from datetime import datetime
        log_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"
        print(log_time)
        return log_time

    def type_file_name_pyautogui(self, type_string):
        """

        """
        sleep(3)
        import pyautogui
        try:
            output = subprocess.check_output('lsb_release -r', shell=True)
            print(output)
        except Exception as e:
            print(e)
        pyautogui.press('end')
        for i in range(0,30):
            pyautogui.press('backspace', interval=0.01)
        if "16" in output:
            splitted_path = type_string.split("/")
            for i in range(0,len(splitted_path)):
                if not splitted_path[i] == "" and i > 0:
                    pyautogui.hotkey('shift','7')
                    pyautogui.typewrite(splitted_path[i])
            sleep(1)
            pyautogui.press('enter')
        else:
            pyautogui.typewrite(type_string, interval=0.05)
        sleep(0.5)
        pyautogui.press('enter')
