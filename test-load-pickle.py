# -*- coding: utf-8 -*-
#
import io, sys
import pickle
from bs4 import BeautifulSoup

# WindowsのPython3で標準出力をUTF8にする
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


with open('334AC0000000121_20230703_505AC0000000051.pickle', mode='rb') as f:
    chapters = pickle.load(f)

for c in chapters:
    for a in c['articles']:
        s = BeautifulSoup(a['body'], 'html.parser')
        a['body'] = s.find('section')
        print(a['body'].find('span'))

# print(chapters)
#
