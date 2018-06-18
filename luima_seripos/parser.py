#!/usr/bin/python3

import re
import requests
import lxml.html
import json


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
        document_url = self.ls_prefix + link_object.get('href')
        page_code = requests.get(document_url).text
        mansi_block_path = ".field-name-body div.field-item.even div"
        page_html = lxml.html.fromstring(page_code)
        mns_blocks = page_html.cssselect(mansi_block_path)
        mns_text = " ".join([block.text for block in mns_blocks if block.text.strip(" ")])
        mns_text = mns_text.replace("\n", "")
        mns_text = mns_text.replace("\t", "")
        mns_text = re.sub(r"\.[^\s]", ". ", mns_text)

        try:
            mns_title = page_html.cssselect(".field-title")[0]
        except IndexError:
            return VoidDownload()

        mns_title = mns_title.text.strip(" ")
        mns_title = re.sub(r'\s{2,}|\t', ' ', mns_title)
        return TXTdownload(mns_title, mns_text, document_url)

    def create_pdf_object(self, link_object):
        page_url = self.ls_prefix + link_object.get('href')
        page_code = requests.get(page_url).text
        pdf_url_regex = r'gdoc-field"\ssrc="[a-z:\/\?\&=\.]+url=([^"]+)'
        pdf_url = re.search(pdf_url_regex, page_code).group(1)
        pdf_url = pdf_url.replace('%2F', '/')
        pdf_url = pdf_url.replace('%3A', ':')
        return PDFdownload(pdf_url, page_url)


class VoidDownload:
    def __init__(self):
        pass

    def download(self):
        raise EmptyPage()


class TXTdownload:
    def __init__(self, doc_title, doc_text, doc_url):
        self.title = doc_title
        self.text = doc_text
        self.url = doc_url

    def download(self):
        return json.dumps({
            "title": self.title,
            "text": self.text,
            "url": self.url
        })


class PDFdownload:
    def __init__(self, download_url, page_url):
        self.url = download_url
        self.page_url = page_url

    def download(self):
        return requests.get(self.url).content


class Downloader:
    def __init__(self, path_folder):
        self.path_folder = path_folder
        if self.path_folder.endswith('/'):
            self.path_folder = self.path_folder[:-1]

    def save(self, file_name, content, binary=False):
        if file_name.startswith('/'):
            file_name = file_name[1:]
        path_to_save = self.path_folder + '/' + file_name

        with open(path_to_save, 'wb' if binary else 'w') as f2save:
            f2save.write(content)
            f2save.close()


class EmptyPage(Exception):
    pass
