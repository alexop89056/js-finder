import argparse
import re
import time
from typing import List

import requests as r
from requests import ConnectTimeout, Session
from tqdm import tqdm

import config


class SourceParser:
    sess: Session = r.Session()
    source_html: str = ''

    def __init__(self, url: str, search_string: str | List[str], file_type: str, delay: int | float = None):
        self.url = url
        self.search_string = search_string
        self.file_type = file_type
        self.delay = delay

    def update_headers(self):
        self.sess.headers.update(config.USER_AGENT)

    def fetch_source(self):
        self.update_headers()
        try:
            resp = self.sess.get(self.url, timeout=3)
            return resp.text
        except ConnectTimeout:
            raise Exception('Url that provided is invalid')

    def extract_links(self):
        links = []
        for file_type in self.file_type:
            matches = re.findall(config.FILE_PATTERNS.get(file_type), self.source_html)
            links.extend(match[1] for match in matches)

        return links

    def find_string(self, link: str, string: str):
        try:
            source = self.sess.get(url=link)
            if string in source.text:
                self.c_print(color='green', string=f' STRING: {string} | FINDED IN {link}', to_file=True)
        except Exception as e:
            self.c_print(color='red', string=f'Error: {str(e)}', to_file=False)
        time.sleep(self.delay)

    def start(self):
        self.show_preview()
        self.source_html = self.fetch_source()
        links = self.extract_links()

        for search_str in self.search_string:
            for link in tqdm(links, desc=f'\033[91m   Parsing static urls for {search_str} \033[0m'):
                self.find_string(link=link, string=search_str)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value: str):
        if re.match(config.URL_REGEX, value):
            self._url = value
        else:
            raise Exception('The URL you provided is not valid http/https')

    @property
    def search_string(self):
        return self._search_string

    @search_string.setter
    def search_string(self, value: str):
        exists_array = value.replace(' ', '').split(",")
        if len(exists_array) == 1:
            self._search_string = [value]
        elif len(exists_array) > 1:
            self._search_string = [value for value in exists_array]

    @property
    def file_type(self):
        return self._file_type

    @file_type.setter
    def file_type(self, value: str):
        exists_array = value.replace(' ', '').split(",")
        if len(exists_array) == 1:
            if value in config.FILE_PATTERNS.keys():
                self._file_type = [value]
            else:
                raise Exception(f'The file type you specified is not supported: {value}')
        elif len(exists_array) > 1:
            self._file_type = [value for value in exists_array if value in config.FILE_PATTERNS]
            unsupported_types = [value for value in exists_array if value not in config.FILE_PATTERNS]
            if unsupported_types:
                raise Exception(f'The file types you specified are not supported: {", ".join(unsupported_types)}')

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value: str):
        if value:
            self._delay = value
        else:
            self._delay = config.DELAY_DEFAULT

    @staticmethod
    def c_print(color: str, string: str, to_file=False):
        if color == 'green':
            print(f'\033[92m{string}\033[0m')
        elif color == 'red':
            print(f'\033[91m{string}\033[0m')

        if to_file:
            with open('result_urls.txt', 'w+') as file:
                file.write(string)

    def show_preview(self):
        self.c_print(color='red', string=config.APP_LOGO)
        self.c_print(color='red', string='The program starts...')
        self.c_print(color='red', string='----------------------------------------------------------'
                                         '----------------------------')
        time.sleep(2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--url', '-u', help='Url to source page', action='store', required=True)
    parser.add_argument('--file-type', '-f',
                        help=f'Filetype to find, (Can be seperated by comma, Exists: {",".join(config.FILE_PATTERNS.keys())})',
                        action='store', required=True)
    parser.add_argument('--search-string', '-s', help='String to search (Can be seperated by comma)',
                        action='store', required=True)
    parser.add_argument('--delay', '-d', help='Delay between every request',
                        action='store')

    args = parser.parse_args()

    SourceParser(url=args.url,
                 file_type=args.file_type, search_string=args.search_string, delay=args.delay).start()
