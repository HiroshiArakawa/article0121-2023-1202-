# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import pandas as pd
# テスト
# --------------------------------------------------------------------------------
st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# --------------------------------------------------------------------------------
if False: #test
    if "hoge" not in st.session_state:
        st.session_state.hoge = 0
        # st.settion_state["hoge"] = 0 would be acceptable
 
    if st.button("Button1"):
        st.session_state.hoge += 1
    st.write("hoge is:", st.session_state.hoge)

# --------------------------------------------------------------------------------
if "text" not in st.session_state:
    fname = '334AC0000000121_20230703_505AC0000000051.html'
    with open(fname, encoding='utf-8') as f:
        st.session_state.text = f.read()

# --------------------------------------------------------------------------------
st.title("My first app")
#
