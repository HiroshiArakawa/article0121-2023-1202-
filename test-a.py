# -*- coding: utf-8 -*-
import io, sys
import re
import json, pickle
# import numpy as np
# import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st
import streamlit.components.v1 as components

# https://qiita.com/papasim824/items/b6aef456644321af0010
# https://github.com/joy13975/streamlit-nested-layout/tree/main
import streamlit_nested_layout

# WindowsのPython3で標準出力をUTF8にする
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# テスト
# --------------------------------------------------------------------------------
if False: #test
    st.sidebar.selectbox(
        "How would you like to be contacted?",
        ("Email", "Home phone", "Mobile phone")
    )
    st.sidebar.selectbox( "select chapter", ("a", "b", "c") )
if False: #test
    st.checkbox("Disable selectbox widget", key="disabled")
    res = st.radio(
        "Set selectbox label visibility ??",
        key="visibility",
        options=["visible", "hidden", "collapsed"],
    )
    print(res, flush=True)
# --------------------------------------------------------------------------------
dic_articles = {} # title:{body, caption}
if "chapters" not in st.session_state:
    print('reading chapters', flush=True)
    with open('334AC0000000121_20230703_505AC0000000051.pickle', mode='rb') as f:
        chapters = pickle.load(f)
    dic_articles = {}
    for c in chapters:
        for a in c['articles']:
            s = BeautifulSoup(a['body'], 'html.parser')
            a['body'] = s.find('section')
            # dic_articles[a['title']] = a['body']
            dic_articles[a['title']] = {'body':a['body'], 'caption':a['caption']}
    # print(chapters[0]['articles'][0]['body'].find('span'), flush=True)
    st.session_state.dic_articles = dic_articles
    st.session_state.chapters = chapters
    st.session_state.lis_chapter_title = [c['title'] for c in st.session_state.chapters]

# --------------------------------------------------------------------------------
# st.sidebar.selectbox( "select chapter", ("a", "b", "c") )
# st.sidebar.selectbox( "select chapter a", ("a", "b", "c") )
sel_c = st.sidebar.selectbox( "select chapter", st.session_state.lis_chapter_title )

if False: #test
    for c in st.session_state.chapters:
        # st.sidebar.text(c['title'])
        lis = [c['title'] for c in st.session_state.chapters]

        # print(type(lis[0]), lis[0])
        # st.sidebar.selectbox( "select chapter", tuple(list('abc')) )
        # st.sidebar.selectbox( "select chapter a", ("a", "b", "c") )
        # st.sidebar.selectbox( "select chapter", lis[:2] )

# --------------------------------------------------------------------------------
# st.title("My first app")

# --------------------------------------------------------------------------------
def get_article_in_text(s, exclude=None):
    tmp = s
    res = []
    s1='[一二三四五六七八九十百]'
    # ----------------------------------------
    re_num=re.compile('第'+s1+'+条の'+s1+'+')
    res += re_num.findall(tmp)
    tmp = re_num.sub('', tmp)
    # ----------------------------------------
    re_num=re.compile('第'+s1+'+条')
    res += re_num.findall(tmp)
    # ----------------------------------------
    if exclude in res:
        res.remove(exclude)
    # ----------------------------------------
    tmp = s
    for a in res:
        # tmp = re.sub(f'({a})', '***\\1', tmp)
        pfx = '<span style="color:#0000ee; font-weight:bold">'
        sfx = '</span>'
        tmp = re.sub(f'({a})', pfx+'\\1'+sfx, tmp)
    return res, tmp
if False: #debug
    lis,_ = get_article_in_text('特許庁長官は、遠隔又は交通不便の地にある者のため、請求により又は職権で、第四十六条の二第一項第三号、第百八条第一 項、第百二十一条第一項又は第百七十三条第一項に規定する期間を延長することができる。')
    print(lis)
# --------------------------------------------------------------------------------
lis_article = None
curr_chapter = None
if sel_c in st.session_state.lis_chapter_title:
    idx = st.session_state.lis_chapter_title.index(sel_c)
    c = st.session_state.chapters[idx]
    print(f'HA231203-a, {sel_c}, {idx}, {c["title"]}')
    lis_article = [a['title']+a['caption'] for a in c['articles']]
    # print(lis_article)
    sel_a = st.sidebar.selectbox("select article", lis_article)
    curr_chapter = c
lis_rel_article = []
sel_rel_article = None
if sel_a in lis_article:
    idx = lis_article.index(sel_a)
    print(f'HA231203-b, {sel_a}, {idx}')
    # st.text(curr_chapter['articles'][idx])
    # https://docs.streamlit.io/library/components/components-api
    with st.expander('Expander 1', expanded=True):
        body = curr_chapter['articles'][idx]['body']
        lis_rel_article, mod_body = \
            get_article_in_text( str(body), exclude=body.find('span').get_text() )
        components.html(mod_body, height=200, scrolling=True)
        # st.selectbox( "select related article", ("a", "b", "c") )
        # print(body)
        sel_rel_article = st.sidebar.selectbox( "select related article", lis_rel_article )
# print('sel_rel_article', sel_rel_article)
if sel_rel_article is not None:
    print('HA231203-c', 'sel_rel_article', sel_rel_article)
    # print(list(st.session_state.dic_articles.keys()))
    tmp_dic = st.session_state.dic_articles
    if (sel_rel_article in tmp_dic.keys()):
        with st.expander('Expander 2', expanded=True):
            components.html(str(tmp_dic[sel_rel_article]['body']), height=200, scrolling=True)
        # st.sidebar.markdown("- Item1")
        for i in lis_rel_article:
            if False:
                st.sidebar.markdown(f"- {i}{tmp_dic[i]['caption']}")
            else: # https://discuss.streamlit.io/t/change-font-size-and-font-color/12377/2
                tmp = '- <p style="font-size: 10px;">'+f"{i}{tmp_dic[i]['caption']}"+'</p>'
                st.sidebar.markdown(tmp, unsafe_allow_html=True)

# --------------------------------------------------------------------------------
if False: #test
    if "hoge" not in st.session_state:
        st.session_state.hoge = 0
        # st.settion_state["hoge"] = 0 would be acceptable
 
    if st.button("Button1"):
        st.session_state.hoge += 1
    st.write("hoge is:", st.session_state.hoge)

# --------------------------------------------------------------------------------
if False: #test
    if "text" not in st.session_state:
        fname = '334AC0000000121_20230703_505AC0000000051.html'
        with open(fname, encoding='utf-8') as f:
            st.session_state.text = f.read()


#
