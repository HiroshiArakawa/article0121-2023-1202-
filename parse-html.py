# -*- coding: utf-8 -*-
# import streamlit as st
import io, sys
from bs4 import BeautifulSoup

# WindowsのPython3で標準出力をUTF8にする
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# テスト
# --------------------------------------------------------------------------------
def parse_html(fname):
    with open(fname, encoding='utf-8') as f:
        text = f.read()
    soup = BeautifulSoup(text, 'html.parser')

    if False:
        lis = soup.find_all('div', {'class': '_div_TOCChapter'})
        print(len(lis))
        for i in lis:
            print(type(i), i)
            anchor=i.find_all('a')
            print(anchor)
            # link=i.find_all('a''Link')
            # print(link)
            break
    if False:
        # lis = soup.select('body > div._div_TOCChapter > a.Link')
        # lis = soup.select('body > div._div_TOCChapter')
        lis = soup.select('div._div_TOCChapter')
        print(len(lis))
        for i in lis:
            print(type(i), i)
            break
        # print(lis)
    is_dg=False # is_debug_print =True
    if True:
        lis = soup.find_all('section')
        print(len(lis))
        chapters = []
        prev_chapter_title = None
        articles = None
        for i in lis:
            # print(type(i), i['class'], i)
            if is_dg: print(type(i), i['class'])
            # break
            if 'SupplProvision' in i['class']:
                # if is_dg: print('\n', type(i), i['class'], i) # i.get_text())
                # exit()
                if prev_chapter_title is not None:
                    if articles is not None and len(articles) > 0:
                        chapter = {'title':prev_chapter_title, 'articles':articles}
                        chapters.append(chapter)
                articles = []
                title = i.find('div', {'class': '_div_SupplProvisionLabel'}).get_text()
                if is_dg: print('\t', title);
                prev_chapter_title = title
            if 'Chapter' in i['class']:
                if prev_chapter_title is not None:
                    if articles is not None and len(articles) > 0:
                        chapter = {'title':prev_chapter_title, 'articles':articles}
                        chapters.append(chapter)
                articles = []
                title = i.get_text()
                if is_dg: print('\t', title); #print(i.find('div').get_text())
                prev_chapter_title = title
            if 'Article' in i['class']:
                # print(i)
                num = i.find('div', {'class': '_div_ArticleTitle'}).find('span').get_text()
                try:
                    cap = i.find('div', {'class': '_div_ArticleCaption'}).get_text()
                except AttributeError:
                    cap = ''
                if is_dg: print('\t', num, cap)
                article = {'title':num, 'caption':cap, 'body':i}
                articles.append(article)
        if True: #debug
            print(len(chapters))
            [print(c['title']) for c in chapters]
# --------------------------------------------------------------------------------
if __name__ == '__main__':
    fname = '334AC0000000121_20230703_505AC0000000051.html'
    parse_html(fname)
#
