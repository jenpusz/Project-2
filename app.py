import numpy as np
import pandas

import datetime as dt

# import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, json, jsonify, render_template

#################################################
# Database Setup
#################################################
app = Flask(__name__)
# app.config = create_engine('postgresql://postgres:postgres@localhost:5432/climate_impact_on_food')




#################################################
# Flask Setup
#################################################

def connect ():
    db_server_info = {"host": "localhost", 
                  "port": 5432, 
                  "dbname": "Climate_Temp", 
                  "user": "postgres", 
                  "password": "postgres"} 
    conn_str = "{}://{}:{}@{}:{}/{}".format(
                                  "postgresql+psycopg2", 
                                  db_server_info["user"], 
                                  db_server_info["password"], 
                                  db_server_info["host"], 
                                  db_server_info["port"], 
                                  db_server_info["dbname"]) 
    alchemyEngine = create_engine(conn_str, pool_recycle=3600)
    postgreSQLConnection = alchemyEngine.connect() 
    return (postgreSQLConnection)

#Create route that renders index.html template
@app.route("/")
def home():
    return render_template ("index.html")


#Create a route for each table and return a dictionary 
@app.route("/ghg")
def ghg():
   
        #Return the data
        conn = connect()
        data = pandas.read_sql('SELECT * FROM ghg', conn)
        return jsonify(data.to_dict (orient='records'))

@app.route("/world_agriculture_emissions")
def emissions():
   
        #Return the data
        conn = connect()
        data = pandas.read_sql("SELECT * FROM world_agriculture_emissions WHERE \"Area\" = 'Afghanistan'", conn)
        return jsonify(data.to_dict (orient='records'))



@app.route("/regions")
def regions():
   
        #Return the data
        conn = connect()
        data = pandas.read_sql('SELECT * FROM regions', conn)
        return jsonify(data.to_dict (orient='records'))


@app.route("/food_production")
def food():
   
        #Return the data
        conn = connect()
        data = pandas.read_sql('SELECT * FROM food_production', conn)
        return jsonify(data.to_dict (orient='records'))

@app.route("/temp_simple")
def temp_simple():
   
        #Return the data
        conn = connect()
        data = pandas.read_sql('SELECT * FROM temp_simple', conn)
        return jsonify(data.to_dict (orient='records'))

@app.route("/temp_full")
def temp_full():
   
        #Return the data
        conn = connect()
        data = pandas.read_sql('SELECT * FROM temp_full', conn)
        return jsonify(data.to_dict (orient='records'))


@app.route("/year_temp")
def year_temp():
   
        #Return the data
        conn = connect()
        data = pandas.read_sql('SELECT * FROM year_temp', conn)
        return jsonify(data.to_dict (orient='records'))




        


if __name__ == "__main__":
    app.run(debug=True)






