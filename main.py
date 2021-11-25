import streamlit as st
import pandas as pd
import requests
import json
import numpy as np

def test_graph(data):
    res = json.loads(data)
    for idx,i in enumerate(res):
        res[idx] = json.loads(i)
    st.sidebar.write("Datos Cantidad gastada ordenado de mayor a menor por sector")
    st.sidebar.write(res)

    st.write("Gráfica Cantidad gastada por sector")
    df = pd.DataFrame(res).astype(str)
    df = df.set_index('SECTOR')
    df['count'] = pd.to_numeric(df['count'])
    st.bar_chart(df)

def rad_hum_eto_table(data):
    res = json.loads(data)
    for idx,i in enumerate(res):
        res[idx] = json.loads(i)
    limit_res = res[:11]    # limitar a 10 valores
    # st.sidebar.write("Datos Radiacion, humedad, Eto gasto")
    # st.sidebar.write(limit_res)
    
    st.write("Tabla Radiacion + Humedad + ETo para ver si influyen")
    df = pd.DataFrame(limit_res).astype(str)
    st.write(df)

def codigos_gasto(data):
    # Print json format
    res = json.loads(data)
    for idx,i in enumerate(res):
        res[idx] = json.loads(i)
    st.sidebar.write("Datos 10 codigo cliente con mas gasto")
    st.sidebar.write(res)

    st.write("Gráfica de los 10 codigos_cliente con mayor gasto")
    # Load to pandas to use with streamlit
    df = pd.DataFrame(res).astype(str)
    df = df.set_index('CP_CLIENTE')
    df['IMPORTE_TOTAL'] = pd.to_numeric(df['IMPORTE_TOTAL'])
    st.bar_chart(df)
    
def init_sidebar(cps):
    st.sidebar.title('Selector de zona')
    st.sidebar.markdown('Seleccione el codigo postal correspondiente con la zona deseado:')
    st.write(json.loads(cps))
    st.sidebar.selectbox('Seleccione CP', json.loads(cps))

def transaccion_sector(data):
    res = json.loads(data)
    for idx,i in enumerate(res):
        res[idx] = json.loads(i)
    limit_res = res[:21]    # limitar a 20 valores
    st.sidebar.write("Datos Transacciones > 1000€ y que sean del sector = HOGAR. Ordenadas de mayor a menor IMPORTE y dia")
    st.sidebar.write(limit_res)
    
    st.write("Datos Transacciones > 1000€ y que sean del sector = HOGAR. Ordenadas de mayor a menor IMPORTE y dia")
    df = pd.DataFrame(limit_res).astype(str)
    st.write(df)

def almeria_table(data):
    st.sidebar.title("Código postal y Municipio: ")
    res = json.loads(data)
    for idx,i in enumerate(res):
        res[idx] = json.loads(i)
    df = pd.DataFrame(res).astype(str)
    st.sidebar.write(df)


if __name__ == '__main__':
    st.title('Patrones de consumo')
    # r_test = requests.get(url='http://127.0.0.1:5000/api/test').content
    r_rad_hum_eto = requests.get(url='http://127.0.0.1:5000/api/rad_hum_eto').content
    r_codigos_gasto = requests.get(url='http://127.0.0.1:5000/api/codigos_gasto').content
    r_transaccion_sector = requests.get(url='http://127.0.0.1:5000/api/transaccion_sector').content
    r_cp = requests.get(url='http://127.0.0.1:5000/api/cp').content
    r_almeria = requests.get(url='http://127.0.0.1:5000/api/almeria').content
    
    # test_graph(r)
    rad_hum_eto_table(r_rad_hum_eto)
    # codigos_gasto(r_codigos_gasto)
    # transaccion_sector(r_transaccion_sector)
    init_sidebar(r_cp)
    almeria_table(r_almeria)
        

