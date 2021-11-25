import streamlit as st
import pandas as pd
import requests
import json
import numpy as np

def test_graph(data):
    res = json.loads(data)
    for idx,i in enumerate(res):
        res[idx] = json.loads(i)
    st.write(res)

    df = pd.DataFrame(res).astype(str)
    df = df.set_index('SECTOR')
    df['count'] = pd.to_numeric(df['count'])
    st.bar_chart(df)


if __name__ == '__main__':
    r = requests.get(url='http://127.0.0.1:5000/api/test').content
    test_graph(r)
        

