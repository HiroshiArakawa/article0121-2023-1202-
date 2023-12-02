# -*- coding: utf-8 -*-
# import streamlit as st
import io, sys, os
from bs4 import BeautifulSoup
import json, pickle

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
        def register_chapter(chapters, prev_chapter_title, articles):
            if prev_chapter_title is not None:
                if articles is not None and len(articles) > 0:
                    if False: #bug fix
                        # https://lethe2211.hatenablog.com/entry/2014/07/28/145350
                        # https://stackoverflow.com/questions/22626003/pickle-dump-meet-runtimeerror-maximum-recursion-depth-exceeded-in-cmp
                        #
                        # articles[0]['body'] = unicode(articles[0]['body'])
                        if True:
                            articles[0]['body'] = str(articles[0]['body'])
                            print(articles[0]['body']             );
                            print(type(articles[0]['body'])       );
                            s = BeautifulSoup(articles[0]['body'], 'html.parser')
                            articles[0]['body'] = s.find('section')
                        print(type(articles[0]['body']))
                        print(     articles[0]['body'].find('span')); exit()
                    chapter = {'title':prev_chapter_title, 'articles':articles}
                    chapters.append(chapter)
            articles = []
            return chapters, articles
        for i in lis:
            # print(type(i), i['class'], i)
            if is_dg: print(type(i), i['class'])
            # break
            if 'SupplProvision' in i['class']:
                # if is_dg: print('\n', type(i), i['class'], i) # i.get_text())
                # exit()
                if False: #refactoring
                    if prev_chapter_title is not None:
                        if articles is not None and len(articles) > 0:
                            chapter = {'title':prev_chapter_title, 'articles':articles}
                            chapters.append(chapter)
                else:
                    chapters, articles = register_chapter(chapters, prev_chapter_title, articles)
                title = i.find('div', {'class': '_div_SupplProvisionLabel'}).get_text()
                if is_dg: print('\t', title);
                prev_chapter_title = title
            if 'Chapter' in i['class']:
                if False: #refactoring
                    if prev_chapter_title is not None:
                        if articles is not None and len(articles) > 0:
                            chapter = {'title':prev_chapter_title, 'articles':articles}
                            chapters.append(chapter)
                    articles = []
                else:
                    chapters, articles = register_chapter(chapters, prev_chapter_title, articles)
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
        chapters, articles = register_chapter(chapters, prev_chapter_title, articles)
        if True: #debug
            print(len(chapters))
            # [print(c['title']) for c in chapters]
            for c in chapters:
                print(c['title'])
                print('\t', c['articles'][0]['title']); # exit()
        return chapters
# --------------------------------------------------------------------------------
if __name__ == '__main__':
    fname = '334AC0000000121_20230703_505AC0000000051.html'
    base = os.path.splitext(fname)
    # print(base); exit()
    base = base[0]
    chapters = parse_html(fname)
    if False: #debug
        with open( base+'.pickle', mode='wb') as f:
            print(chapters[0]['articles'][0]['body']); exit()
            pickle.dump(chapters[0]['articles'][0]['body'], f)
            pickle.dump(chapters, f)
        for c in chapters:
            for a in c['articles']:
                a['body'] = json.dumps(a['body'].get_text())
    for c in chapters:
        for a in c['articles']:
            a['body'] = str(a['body'])
    with open( base+'.pickle', mode='wb') as f:
        pickle.dump(chapters, f)
    with open( base+'.json', mode='w', encoding='utf-8') as f:
        json.dump(chapters, f, ensure_ascii=False)
#
