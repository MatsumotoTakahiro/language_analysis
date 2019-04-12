#!/usr/local/bin/python3
# -*- Coding: utf-8 -*-

import sys
import urllib3
import certifi
import bs4
import urllib
import unicodedata as ud


def wiki_mining(nation_name):

    # url_encoding
    nation_url = 'https://ja.wikipedia.org/wiki/' + urllib.parse.quote(nation_name)

    # page_sourcecode
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    source = http.request('GET', nation_url)
    soup = bs4.BeautifulSoup(source.data, 'html.parser')

    # text_mining
    wiki_title = ud.normalize('NFKC', soup.head.title.text.replace(' - Wikipedia', ''))
    wiki_text = ud.normalize('NFKC', '\n'.join(block.text.strip() for block in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4'])))

    return wiki_title, wiki_text


if __name__ == '__main__':

    # input
    argv = sys.argv

    if len(argv) < 2:
        print('Usage: python wiki_source.py <nation_name>')
        quit()

    nation_name = argv[1]

    print('[title]: ', wiki_mining(nation_name)[0])
    print('[title]: ', wiki_mining(nation_name)[1])
