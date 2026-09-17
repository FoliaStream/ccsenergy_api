from flask import Flask, jsonify, request
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# INIT API
app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def load_data():
    return pd.read_sql("SELECT * FROM plants", engine)

@app.route("/")
def home():
    res = jsonify({"message":"CCS Energy app is running!"})
    return res

@app.get("/items")
def get_all():
    df = load_data()
    res = jsonify(df.to_dict(orient='records'))
    return res

@app.route("/plants/<int:plant_id>", methods=["GET"])
def get_one(plant_id):
    df = load_data()
    if plant_id < 0 or plant_id >= len(df):
        return jsonify({"error": "Plant not found"}), 404
    return jsonify(df.iloc[plant_id].to_dict())

@app.route("/search", methods=["GET"])
def search():
    df = load_data()
    country = request.args.get("country")
    usage = request.args.get("usage")

    result = df
    if country:
        result = result[result["country"].str.lower() == country.lower()]
    if usage:
        result = result[result["usage"].str.lower() == usage.lower()]

    return jsonify(result.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)