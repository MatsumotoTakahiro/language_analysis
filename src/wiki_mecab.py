#!/usr/local/bin/python3
# -*- Coding: utf-8 -*-

import numpy as np
import pandas as pd
import sqlite3
import sys
import MeCab

if __name__ == '__main__':

    argv = sys.argv

    if len(argv) < 2:
        print('Usage: python wiki_mecab.py <db_name>')
        quit()

    db_name = argv[1]
    
    conn = sqlite3.connect(db_name)
    
    data = pd.read_sql_query('SELECT * FROM docs', conn)
    
    m = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    
    for i in range(len(data.index)):
        mecab_result = m.parseToNode(data.content[i])
        
        resultdf = pd.DataFrame({'word':[], 'hinsi':[], 'hinsi1':[], 'hinsi2':[], 'hinsi3':[], 'genkei':[]})
        n = 0
        while mecab_result:
            print(n)
            n = n+1
            word = mecab_result.surface
            hinsi = mecab_result.feature.split(",")[0]
            hinsi1 = mecab_result.feature.split(",")[1]
            hinsi2 = mecab_result.feature.split(",")[2]
            hinsi3 = mecab_result.feature.split(",")[3]
            genkei = mecab_result.feature.split(',')[6]
            pieceraw = pd.DataFrame({'word':[word], 'hinsi':[hinsi], 'hinsi1':[hinsi1], 'hinsi2':[hinsi2], 'hinsi3':[hinsi3], 'genkei':[genkei]})
            resultdf = resultdf.append(pieceraw)
            mecab_result = mecab_result.next 
        
        data.at[i, 'chunk'] = resultdf.reset_index(drop=True)
    
    data.to_pickle('wiki_nation_mecabed.pkl')
    conn.close()
    