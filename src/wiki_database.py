#!/usr/local/bin/python3
# -*- Coding: utf-8 -*-

import json
import urllib

import wiki_source
import sqlitedatastore


if __name__ == '__main__':

    sqlitedatastore.connect()
    values = []
    with open('./data/nation_list.txt') as f:
        for nation_name in f:
            print(nation_name.rstrip('\n'))
            title, text = wiki_source.wiki_mining(nation_name.rstrip('\n'))
            nation_url = 'https://ja.wikipedia.org/wiki/' + urllib.parse.quote(nation_name)
            values.append((text, json.dumps({
                'url': nation_url,
                'title': title
            })))
    sqlitedatastore.load(values)

    print(list(sqlitedatastore.get_all_ids(limit=-1)))

    for doc_id in sqlitedatastore.get_all_ids(limit=-1):
        print(doc_id)
        row = sqlitedatastore.get(doc_id, ['id', 'content', 'meta_info'])
        print(row['id'], json.loads(row['meta_info']), row['content'][:100])
    sqlitedatastore.close()
