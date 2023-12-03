# -*- coding: utf-8 -*-
import io, sys
import json, pickle
# import numpy as np
# import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st
import streamlit.components.v1 as components

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
if "chapters" not in st.session_state:
    print('reading chapters', flush=True)
    with open('334AC0000000121_20230703_505AC0000000051.pickle', mode='rb') as f:
        chapters = pickle.load(f)
    for c in chapters:
        for a in c['articles']:
            s = BeautifulSoup(a['body'], 'html.parser')
            a['body'] = s.find('section')
    # print(chapters[0]['articles'][0]['body'].find('span'), flush=True)
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
if sel_a in lis_article:
    idx = lis_article.index(sel_a)
    print(f'HA231203-b, {sel_a}, {idx}')
    # st.text(curr_chapter['articles'][idx])
    # https://docs.streamlit.io/library/components/components-api
    components.html(str(curr_chapter['articles'][idx]['body']), height=200, scrolling=True)


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
