#!/usr/local/bin/python3
# -*- Coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
import sqlite3
from pyknp import Juman

if __name__ == '__main__':

    argv = sys.argv

    if len(argv) < 2:
        print('Usage: python wiki_juman.py <db_name>')
        quit()

    db_name = argv[1]
    
    conn = sqlite3.connect(db_name)
    
    data = pd.read_sql_query('SELECT * FROM docs', conn)
    
    jumanpp = Juman()
    
    for i in range(1):#len(data.index)):
        result = jumanpp.analysis(data.content[i])
        
        resultdf = pd.DataFrame({'midasi':[], 'hinsi':[], 'genkei':[]})
        
        for j in range(3):#len(result.mrph_list)):
            pieceraw = pd.DataFrame({'midasi':[result.mrph_list()[j].midasi], 'hinsi':[result.mrph_list()[j].hinsi], 'genkei':[result.mrph_list()[j].genkei]})
            resultdf = resultdf.append(pieceraw)
        
        data[i]['chunk'] = resultdf
    
    data.to_csv('test.csv')    
    conn.close()
    