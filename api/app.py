from flask import Flask
from pyspark.sql import SparkSession
from flask_cors import CORS
import json
import pandas

# Global vars
spark = SparkSession.builder.appName("main").master("local[*]").getOrCreate()
app = Flask(__name__)
CORS(app)
df_cards, df_weather = None, None

def init():
    global df_cards, df_weather
    df_cards = spark.read.csv('datos/cards.csv', inferSchema=True, header=True, sep='|')
    df_weather = spark.read.csv('datos/weather.csv', inferSchema=True, header=True, sep=';')


@app.route('/api/test', methods=['GET'])
def test():
    result = df_cards.groupBy('SECTOR').count().toJSON().collect()
    return json.dumps(result)

    
if __name__ == "__main__":
    init()
    app.run(debug=True)