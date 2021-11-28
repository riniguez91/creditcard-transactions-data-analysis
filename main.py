import streamlit as st
import pandas as pd
import requests
import json
import numpy as np

cp_selected = 4001

def total_cost_per_sector_graph(data):
    res = json.loads(data)
    for idx,i in enumerate(res):
        res[idx] = json.loads(i)
    
    st.header('Cantidad gastada por sector')
    df = pd.DataFrame(res).astype(str)
    df = df.set_index('SECTOR')
    df['count'] = pd.to_numeric(df['count'])
    st.bar_chart(df)

def rad_hum_eto_table(data):
    res = json.loads(data)
    for idx,i in enumerate(res):
        res[idx] = json.loads(i)
    limit_res = res[:11]    # limitar a 10 valores
        
    st.header('Evapotranspiración frente a la Humedad y la Radiación Solar')
    df = pd.DataFrame(limit_res).astype(str)
    st.write(df)

def codigos_gasto(data):
    # Print json format
    res = json.loads(data)
    for idx,i in enumerate(res):
        res[idx] = json.loads(i)
    
    st.header('Gráfica de los 10 CP con mayor gasto')
    # Load to pandas to use with streamlit
    df = pd.DataFrame(res).astype(str)
    df = df.set_index('CP_CLIENTE')
    df['IMPORTE_TOTAL'] = pd.to_numeric(df['IMPORTE_TOTAL'])
    st.bar_chart(df)
    
def init_sidebar(cps, almeria):
    st.sidebar.title('Selector de zona')
    st.sidebar.markdown('Seleccione el codigo postal correspondiente con la zona deseado:')
    global cp_selected
    cp_selected = st.sidebar.selectbox('Seleccione CP', json.loads(cps))
    st.write('Has seleccionado el código postal: ', cp_selected)

    st.sidebar.title('Código postal y Municipio: ')
    res = json.loads(almeria)
    for idx,i in enumerate(res):
        res[idx] = json.loads(i)
    df = pd.DataFrame(res).astype(str)
    st.sidebar.write(df)

def transaccion_sector(data):
    res = json.loads(data)
    for idx,i in enumerate(res):
        res[idx] = json.loads(i)
    limit_res = res[:21]    # limitar a 20 valores
    
    st.header('Transacciones mayores a 1000€ del sector HOGAR para el CP ' + str(cp_selected))
    df = pd.DataFrame(limit_res).astype(str)
    st.write(df)

def municipio_cards_table(data):
    st.header('Municipio y su información para el CP ' + str(cp_selected))
    res = json.loads(data)
    for idx,i in enumerate(res):
        res[idx] = json.loads(i)
    df = pd.DataFrame(res).astype(str)
    st.write(df)

def settings_st():
    # Page settings
    st.set_page_config(
        page_title="Grandes Volumenes de Datos",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={'About':"""
            ## Authors: 
               Ramón Íñiguez Bascuas\n
               Víctor Hernández Sanz\n
               Rubén Ortiz Nieto\n
            [Link to Github repository](https://github.com/riniguez91/creditcard-transactions-data-analysis)"""}
    )
    st.title('Patrones de consumo')

def sidebar_requests():
    r_cp = requests.get(url='http://127.0.0.1:5000/api/cp').content
    r_almeria = requests.get(url='http://127.0.0.1:5000/api/almeria').content
    init_sidebar(r_cp, r_almeria)

def mainpage_requests():
    requests.post(url='http://127.0.0.1:5000/api/cp_selected', data=json.dumps({'cp': cp_selected}))
    r_municipio_cards = requests.get(url='http://127.0.0.1:5000/api/municipio_cards').content
    r_transaccion_sector = requests.get(url='http://127.0.0.1:5000/api/transaccion_sector').content
    r_total_cost_per_sector = requests.get(url='http://127.0.0.1:5000/api/total_cost_per_sector').content
    r_codigos_gasto = requests.get(url='http://127.0.0.1:5000/api/codigos_gasto').content
    r_rad_hum_eto = requests.get(url='http://127.0.0.1:5000/api/rad_hum_eto').content

    municipio_cards_table(r_municipio_cards)
    transaccion_sector(r_transaccion_sector)
    total_cost_per_sector_graph(r_total_cost_per_sector)
    codigos_gasto(r_codigos_gasto)
    rad_hum_eto_table(r_rad_hum_eto)

if __name__ == '__main__':
    settings_st()
    try:
        sidebar_requests()
        mainpage_requests()
    except requests.exceptions.ConnectionError:
        print("Connection refused")
    
    
        

