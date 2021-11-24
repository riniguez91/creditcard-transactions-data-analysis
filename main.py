import streamlit as st
import requests
import json

def test_graph(data):
    st.write(data)

def main():
    if __name__ == '__main__':
        r = json.loads(requests.get(url='http://127.0.0.1:5000/api/test'))
        test_graph(r)
        

