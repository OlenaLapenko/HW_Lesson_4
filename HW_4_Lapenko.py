from flask import jsonify, Flask
from http import HTTPStatus

from webargs import validate, fields
from webargs.flaskparser import use_kwargs

import random
import string
import csv
import pandas as pd


app = Flask(__name__)

@app.route("/")
def main():
    return "Hi, coach!"

@app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def error_handling(error):
    headers = error.data.get("headers", None)
    messages = error.data.get("messages", ["Invalid request."])

    if headers:
        return jsonify(
            {
                'errors': messages
            },
            error.code,
            headers
        )
    else:
        return jsonify(
            {
                'errors': messages
            },
            error.code,
        )


@app.route("/generate-password")
@use_kwargs(
    {
        "length": fields.Int(
            missing=10,
            validate=[validate.Range(min=10, max=25)]
        ),
    },
    location="query"
)
def generate_password(length):
    return "".join(
        random.choices(
            string.ascii_lowercase + string.ascii_uppercase,
            k=length
        )
    )

# calculate_average() without Pandas
@app.route("/average_high_weight")
def calculate_average():
    with open('hw.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        counter = 0
        sum_high = 0
        sum_weight = 0

        for row in reader:
            counter += 1
            sum_high += float(row[1])
            sum_weight += float(row[2])
    return f'Average_high: {round(sum_high/counter, 3)} Inches, ' \
           f'Average_weight: {round(sum_weight/counter, 3)} Pounds'

# calculate_average() using Pandas
@app.route("/average_high_weight_p")
def calculate_average_p():
    students_data = pd.read_csv("hw.csv", na_values=['no info', '.'])
    return f'Average_high: {students_data.iloc[:, 1].mean().round(3)} Inches, ' \
           f'Average_weight: {students_data.iloc[:, 2].mean().round(3)} Pounds'



app.run(port=5001, debug=True)
