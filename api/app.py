import re
from flask import Flask
from pyspark.sql import SparkSession
from flask_cors import CORS
import json
import pandas

# Global vars
spark = SparkSession.builder.appName("main").master("local[*]").getOrCreate()
app = Flask(__name__)
CORS(app)
df_cards, df_weather, df_almeria = None, None, None

def init():
    global df_cards, df_weather, df_almeria
    df_cards = spark.read.csv('datos/cards.csv', inferSchema=True, header=True, sep='|')
    df_weather = spark.read.csv('datos/weather.csv', inferSchema=True, header=True, sep=';')
    df_almeria = spark.read.csv('datos/almeria.csv', inferSchema=True, header=True, sep=';')

''' Gasto total por sector ordenado mayor a menor '''
@app.route('/api/test', methods=['GET'])
def test():
    result = df_cards.groupBy('SECTOR').count().orderBy(['count'], ascending=False).toJSON().collect()
    return json.dumps(result)

''' Radiacion + Humedad + ETo para ver si influyen '''
@app.route('/api/rad_hum_eto', methods=['GET'])
def rad_hum_eto():
    result = df_weather.select('FECHA', 'DIA', 'Rad', 'HumMax', 'ETo').toJSON().collect()
    return json.dumps(result)

''' Mostrar 10 codigos_cliente (codigo postal) con mayor gasto '''
@app.route('/api/codigos_gasto', methods=['GET'])
def codigos_gasto():
    df_cards.createOrReplaceTempView('sqlTable')
    result = spark.sql(''' SELECT CP_CLIENTE, SUM(IMPORTE) AS IMPORTE_TOTAL FROM sqlTable GROUP BY CP_CLIENTE ORDER BY IMPORTE_TOTAL DESC LIMIT 10 ''').toJSON().collect()
    return json.dumps(result)

''' Transacciones > 1000€ y que sean del sector = HOGAR. Ordenadas de mayor a menor IMPORTE y dia''' 
@app.route('/api/transaccion_sector', methods=['GET'])
def transaccion_sector():
    result = df_cards.filter((df_cards.IMPORTE > 1000) & (df_cards.SECTOR == "HOGAR")).orderBy(['IMPORTE','DIA'], ascending=False).toJSON().collect()
    return json.dumps(result)

@app.route('/api/cp', methods=['GET'])
def cps():
    rows = df_cards.select('CP_CLIENTE').distinct().orderBy('CP_CLIENTE', ascending=True).collect()
    return json.dumps([row['CP_CLIENTE'] for row in rows])
    
@app.route('/api/almeria', methods=['GET'])
def almeria():
    result = df_almeria.select('CP', 'Municipio').toJSON().collect()
    return json.dumps(result)

@app.route('/api/municipio_cards', methods=['GET'])
def municipio_cards():
    df_cards.createOrReplaceTempView('sqlCards')
    df_almeria.createOrReplaceTempView('sqlAlmeria')
    result = spark.sql(''' SELECT sqlAlmeria.CP, sqlAlmeria.Municipio, sqlCards.SECTOR, sqlCards.DIA, sqlCards.IMPORTE,sqlCards.NUM_OP FROM sqlCards 
    JOIN sqlAlmeria ON sqlCards.CP_CLIENTE = sqlAlmeria.CP ''').toJSON().collect()
    return json.dumps(result)

if __name__ == "__main__":
    init()
    app.run(debug=True)