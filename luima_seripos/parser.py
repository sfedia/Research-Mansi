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
        a_link_path = ".view-content table tbody tr td div div a"
        page_html = lxml.html.fromstring(self.page_code)
        a_links = page_html.cssselect(a_link_path)
        return [ls_prefix + link.get('href') for link in a_links]