# coding=utf-8

from view_models import sidebar, certification_services, timestamp_services
from selenium.webdriver.common.by import By
import re


def select_ts(self, ts_name):
    '''
    Clicks on Timestaming services from menu and clicks one time (activates) on certificate
    :param self:
    :param ts_name: TS display name
    :return:
    '''
    # Click on Timestamping Services
    self.log('UC TRUST_15_1     CS administrator selects to view approved timestamping services.: {0}'.format(ts_name))

    self.wait_until_visible(self.by_css(sidebar.TIMESTAMPING_SERVICES_CSS)).click()
    self.wait_jquery()

    # Activate timestamp services - make one click on it.
    self.log(
        'UC TRUST_15_2    The value of the subject common name (CN) element from the TSA certificate is displayed as the name of the timestamping service')
    self.wait_until_visible(element=certification_services.ts_get_ca_by_td_text(ts_name), type=By.XPATH).click()
    self.wait_jquery()


def verify_ts(self):
    '''
    Verifies valid dates with regex (format 0000-00-00 00:00:00) and enabled Add, Delete, Edit buttons
    :param self: MainController object
    :return: None
    '''

    # Date verification
    # Get Valid from time
    from_date = self.by_xpath(timestamp_services.SERTIFICATE_VALID_FROM).text

    # Get Valid to time
    to_date = self.by_xpath(timestamp_services.SERTIFICATE_VALID_TO).text

    from_date_match = re.match(timestamp_services.DATE_REGEX, from_date)
    to_date_match = re.match(timestamp_services.DATE_REGEX, to_date)

    self.log('UC TRUST_15_2    "Valid From" verification {0}'.format(from_date))

    self.is_true(from_date_match,
                 msg='From date in wrong format')

    self.log('UC TRUST_15_2    "Valid To" verification {0}'.format(from_date))

    self.is_true(to_date_match,
                 msg='To date in wrong format')

    # Locate visible "Add" button
    self.log('UC TRUST_15_2    "Add button verification"')

    ts_add_btn = self.wait_until_visible(self.by_id(certification_services.TSADD_BTN_ID)).is_enabled()
    self.is_true(ts_add_btn,
                 msg='Add button not enabled')

    self.log('UC TRUST_15_2    "Delete button verification"')

    # Locate visible "Delete" button
    ts_delete_btn = self.wait_until_visible(self.by_id(certification_services.TSDELETE_BTN_ID)).is_enabled()
    self.is_true(ts_delete_btn,
                 msg='Delete button not enabled')

    self.log('UC TRUST_15_2    "Edit button verification"')
    # Locate visible "Edit" button
    ts_edit_btn = self.wait_until_visible(self.by_id(certification_services.TSEDIT_BTN_ID)).is_enabled()
    self.is_true(ts_edit_btn,
                 msg='Edit button not enabled')



    # Locate visible View certificate button


def click_ts(self):
    '''
    Selects on row and verifies View certificate button
    :param self: MainController object
    :return: None
    '''

    self.by_id(certification_services.TSEDIT_BTN_ID).click()

    view_certificate_btn = self.wait_until_visible(self.by_id(certification_services.VIEW_CERTIFICATE)).is_enabled()

    self.log('UC TRUST_15_2    "View sertificate" button verification"')
    self.is_true(view_certificate_btn,
                 msg='View certificate button not found')


def test_view_approved_ts(case, ts_name):
    '''
    UC TRUST_15 main test method. Verifies Timestamp services buttons and dates.
    :param case: MainController object
    :param ts_name: str - TS display name (hostname)
    :return:
    '''
    self = case

    def view_ts():
        # UC TRUST_15: View Approved Timestamping Services
        self.log('UC TRUST_15 -  View Approved Timestamping Services: {0}'.format(ts_name))

        # Open "Timestamping services"
        select_ts(self, ts_name)

        # Verify "Timestaming services" displayed information
        verify_ts(self)

        # Verify View certificate button verification
        click_ts(self)

    return view_ts
