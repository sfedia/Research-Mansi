#!/usr/bin/python3

import re
import requests
import lxml.html


class ArchivePage:
    def __init__(self, archive_url):
        self.ap_request = requests.get(archive_url)
        self.page_code = self.ap_request.text
        self.links = self.__get_no_links()

    def __get_no_links(self):
        ls_prefix = "http://www.khanty-yasang.ru"
        img_link_path = ".view-content table tbody tr td div div a"
        page_html = lxml.html.fromstring(self.page_code)
        img_links = page_html.cssselect(img_link_path)
        return [ls_prefix + link.get('href') for link in img_links]


class NumberPage:
    def __init__(self, number_url):
        self.np_request = requests.get(number_url)
        self.page_code = self.np_request.text
        self.ls_prefix = "http://www.khanty-yasang.ru"
        self.page_html = lxml.html.fromstring(self.page_code)
        strip_path = ".view-content table tbody tr td div span span a"
        self.strip_links = self.page_html.cssselect(strip_path)

    def get_download_objects(self):
        if self.strip_links:
            return self.find_strip_links()
        else:
            return self.find_section_links()

    def find_section_links(self):
        sec_link_path = ".section div ul li a"
        sec_links = self.page_html.cssselect(sec_link_path)
        return [self.create_txt_object(link) for link in sec_links]

    def find_strip_links(self):
        a_link_path = ".view-content table tbody tr td div span span a"
        a_links = self.page_html.cssselect(a_link_path)
        return [self.create_pdf_object(link) for link in a_links]

    def create_txt_object(self, link_object):
        page_code = requests.get(self.ls_prefix + link_object.get('href'))
        ...


    def create_pdf_object(self, link_object):
        page_code = requests.get(self.ls_prefix + link_object.get('href')).text
        pdf_url_regex = r'gdoc-field"\ssrc="[a-z:\/\?\&=\.]+url=([^"]+)'
        pdf_url = re.search(pdf_url_regex, page_code).group(1)
        pdf_url = pdf_url.replace('%2F', '/')
        pdf_url = pdf_url.replace('%3A', ':')
        return PDFdownload(pdf_url)


class TXTdownload:
    def __init__(self):
        ...


class PDFdownload:
    def __init__(self, download_url):
        self.url = download_url

    def download(self):
        ...

