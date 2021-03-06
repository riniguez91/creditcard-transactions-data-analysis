import re
from flask import Flask, request
from pyspark.sql import SparkSession
from flask_cors import CORS
import json
import pandas

# Global vars
spark = SparkSession.builder.appName("main").master("local[*]").getOrCreate()
app = Flask(__name__)
CORS(app)
df_cards, df_weather, df_almeria = None, None, None
cp = 4001

def init():
    global df_cards, df_weather, df_almeria
    df_cards = spark.read.csv('datos/cards.csv', inferSchema=True, header=True, sep='|')
    df_weather = spark.read.csv('datos/weather.csv', inferSchema=True, header=True, sep=';')
    df_almeria = spark.read.csv('datos/almeria.csv', inferSchema=True, header=True, sep=';')

''' Gasto total por sector ordenado mayor a menor '''
@app.route('/api/total_cost_per_sector', methods=['GET'])
def total_cost_per_sector():
    result = df_cards.groupBy('SECTOR').count().orderBy(['count'], ascending=False).toJSON().collect()
    return json.dumps(result)

''' Evapotranspiración dependiendo de la Humedad y la Radiación Solar '''
@app.route('/api/rad_hum_eto', methods=['GET'])
def rad_hum_eto():
    result = df_weather.select('FECHA', 'DIA', 'Rad', 'HumMax', 'ETo').toJSON().collect()
    return json.dumps(result)

''' Mostrar los 10 codigos_cliente (codigo postal) con mayor gasto '''
@app.route('/api/codigos_gasto', methods=['GET'])
def codigos_gasto():
    df_cards.createOrReplaceTempView('sqlTable')
    result = spark.sql(''' SELECT CP_CLIENTE, SUM(IMPORTE) AS IMPORTE_TOTAL FROM sqlTable GROUP BY CP_CLIENTE ORDER BY IMPORTE_TOTAL DESC LIMIT 10 ''').toJSON().collect()
    return json.dumps(result)

''' Transacciones > 1000€ y que sean del sector = HOGAR. Ordenadas de mayor a menor IMPORTE y dia, con CP introducido por usuario ''' 
@app.route('/api/transaccion_sector', methods=['GET'])
def transaccion_sector():
    result = df_cards.filter((df_cards.IMPORTE > 1000) & (df_cards.SECTOR == "HOGAR") & (df_cards.CP_CLIENTE == cp)).orderBy(['IMPORTE','DIA'], ascending=False).toJSON().collect()
    return json.dumps(result)

''' Seleccionar el CP unico ordenado de menor a mayor '''
@app.route('/api/cp', methods=['GET'])
def cps():
    rows = df_cards.select('CP_CLIENTE').distinct().orderBy('CP_CLIENTE', ascending=True).collect()
    return json.dumps([row['CP_CLIENTE'] for row in rows])

''' Seleccionar CP y Municipio del dataframe almería '''
@app.route('/api/almeria', methods=['GET'])
def almeria():
    result = df_almeria.select('CP', 'Municipio').toJSON().collect()
    return json.dumps(result)

''' Recoger el valor del CP desde el selectBox '''
@app.route('/api/cp_selected', methods=['POST'])
def cp_selected():
    global cp
    request_data = json.loads(request.data)
    cp = request_data['cp']
    return json.dumps({'message': 'success'})

''' JOIN de cards y almeria '''
@app.route('/api/municipio_cards', methods=['GET'])
def municipio_cards():
    df_cards.createOrReplaceTempView('sqlCards')
    df_almeria.createOrReplaceTempView('sqlAlmeria')
     
    result = spark.sql(''' SELECT sqlAlmeria.CP, sqlAlmeria.Municipio, sqlCards.SECTOR, sqlCards.DIA, sqlCards.IMPORTE,sqlCards.NUM_OP FROM sqlCards 
    JOIN sqlAlmeria ON sqlCards.CP_CLIENTE = sqlAlmeria.CP WHERE CP = {} '''.format(cp)).toJSON().collect()
    return json.dumps(result)

if __name__ == "__main__":
    init()
    app.run(debug=True)