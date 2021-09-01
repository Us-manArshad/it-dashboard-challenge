import time
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.PDF import PDF
import os
import re
from constants import DOWNLOAD_DIR, URL


class ITDashboard:
    uii_links = []
    headers = []
    agencies_data = []
    investment_table_data = {}

    def __init__(self, url):
        """
        Initialize the Selenium, PDF, and Files.

        Set the default download directory.

        Open the website
        :param url:
        """
        self.browser = Selenium()
        self.lib = Files()
        self.pdf = PDF()
        self.browser.set_download_directory(os.path.join(os.getcwd(), f"{DOWNLOAD_DIR}/"))
        self.browser.open_available_browser(url)

    def click_on_dive_in(self, keyword):
        """
        Wait for the keyword and click on it.
        :param keyword:
        :return:
        """
        self.browser.wait_until_page_contains(keyword)
        self.browser.find_element('//a[@class="btn btn-default btn-lg-2x trend_sans_oneregular"]').click()

    def search_for_agencies(self):
        """
        It will search and get the agencies from the web page.
        :return:
        """
        time.sleep(5)
        agencies = self.browser.find_elements('//div[@id="agency-tiles-widget"]//div[@class="col-sm-4 text-center noUnderline"]')
        found_agencies = []
        amounts = []
        for agency in agencies:
            agency_split = agency.text.split("\n")
            found_agencies.append(agency_split[0])
            amounts.append(agency_split[2])
        self.agencies_data = {'Company-Name': found_agencies, 'Amount': amounts}

    def write_agencies_to_excel(self, filename):
        """
        It will write the agencies to an excel file
        :param filename:
        :return:
        """
        w = self.lib.create_workbook(f"{DOWNLOAD_DIR}/{filename}.xlsx")
        w.append_worksheet("Sheet", self.agencies_data)
        w.save()

    def get_table_header(self):
        """
        It will get the investment tables headers.
        :return:
        """
        while True:
            try:
                all_heads = self.browser.find_element(
                    '//table[@class="datasource-table usa-table-borderless dataTable no-footer"]').find_element_by_tag_name(
                    "thead").find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("th")
                if all_heads:
                    break
            except:
                time.sleep(1)
        for head in all_heads:
            self.headers.append(head.text)

    def get_uii_links(self):
        """
        It will read the investment table rows and get the uii associated links and Investment Title.
        :return:
        """
        tr_elements = self.browser.find_elements('//tr[@role="row"]')
        for tr_element in tr_elements[2:]:
            td_elements = tr_element.find_elements_by_tag_name('td')
            try:
                a_element = tr_element.find_element_by_tag_name('a').get_attribute("href")
            except:
                a_element = ''
            if a_element:
                self.uii_links.append(
                    {"link": a_element, "investment_title": td_elements[2].text, "uii": td_elements[0].text}
                )

    def open_agency(self, agency_number):
        """
        It will open the agency page provided in params
        :param agency_number:
        :return:
        """
        self.browser.find_elements(
            '//div[@id="agency-tiles-widget"]//div[@class="col-sm-4 text-center noUnderline"]//div[@class="row top-gutter-20"]//div[@class="col-sm-12"]')[
            agency_number].click()
        self.get_table_header()
        for head in self.headers:
            self.investment_table_data[head] = []
        while True:
            current_label = self.browser.find_element("investments-table-object_info").text
            all_rows = self.browser.find_element("investments-table-object").find_element_by_tag_name(
                "tbody").find_elements_by_tag_name("tr")
            for row in all_rows:
                for i, data in enumerate(row.find_elements_by_tag_name("td")):
                    try:
                        self.investment_table_data[self.headers[i]].append(data.text)
                    except:
                        self.investment_table_data[self.headers[i]].append("")
            self.get_uii_links()
            if self.browser.find_element('investments-table-object_next').get_attribute(
                    "class") == 'paginate_button next disabled':
                break
            else:
                self.browser.find_element('investments-table-object_next').click()
                while True:
                    if current_label != self.browser.find_element("investments-table-object_info").text:
                        break
                    time.sleep(1)

    def write_investment_excel(self, filename):
        """
        It will write the investment table excel file into output folder
        :param filename:
        :return:
        """
        w = self.lib.create_workbook(f"{DOWNLOAD_DIR}/{filename}.xlsx")
        w.append_worksheet("Sheet", self.investment_table_data)
        w.save()

    def download_pdfs(self):
        """
        It will read all uii links and download the PDF's if found on that links
        :return:
        """
        for url in self.uii_links:
            self.browser.go_to(url["link"])
            flag_time = time.time() + 10
            while True:
                try:
                    if flag_time <= time.time():
                        break
                    pdf_link = self.browser.find_element('//*[contains(@id,"business-case-pdf")]//a').get_attribute("href")
                    if pdf_link:
                        self.browser.find_element('//div[@id="business-case-pdf"]').click()
                        while True:
                            try:
                                time.sleep(2)
                                if self.browser.find_element('//div[@id="business-case-pdf"]').find_element_by_tag_name("span"):
                                    time.sleep(1)
                                else:
                                    break
                            except:
                                if self.browser.find_element('//*[contains(@id,"business-case-pdf")]//a[@aria-busy="false"]'):
                                    time.sleep(1)
                                    break
                        break
                except:
                    time.sleep(1)

    def compare_pdf_with_title(self):
        """
        It will read the downloaded PDF files and get the Section A from each PDF then it will compare
         the values "Name of this Investment" with the column "Investment Title",
          and the value "Unique Investment Identifier (UII)" with the column "UII"
        :return:
        """
        self.browser.go_to(URL)
        for link_item in self.uii_links:
            try:
                file_name = f'output/{link_item["uii"]}.pdf'
                new_text = self.pdf.get_text_from_pdf(file_name, 1)
                new_string = re.split(r'Bureau:|Section B', new_text[1])[1]
                investment_title = re.split(r'Name of this Investment|2.', new_string)[1].replace(': ', '')
                uii_text = re.split(r'Name of this Investment|2.', new_string)[2].replace(
                    ' Unique Investment Identifier (UII): ', '')
                if link_item["uii"] == uii_text:
                    print(f'Unique Investment Identifier (UII): {link_item["uii"]} found in PDF ({file_name}).')
                if link_item["investment_title"] == investment_title:
                    print(f'Name of this Investment: {link_item["investment_title"]} found in PDF ({file_name}).')
            except:
                pass

    def close_all_browsers(self):
        """
        Close the browsers
        :return:
        """
        self.browser.close_all_browsers()
