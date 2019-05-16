#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import pandas as pd
import altair as alt
import json
from datamanager import DataManager
import os

data_manager = DataManager()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/hook', methods=["GET", "POST", 'OPTIONS'])
def change_plot():
    if request.method == 'POST':
        chart = data_manager.change_plot(request)

        return json.dumps(chart)


@app.route('/hook_type', methods=["GET", "POST", 'OPTIONS'])
def change_plot_type():
    if request.method == 'POST':
        chart = data_manager.change_plot_type(request)

        return json.dumps(chart)


@app.route('/hook_add', methods=["GET", "POST", 'OPTIONS'])
def change_plot_add():
    if request.method == 'POST':
        chart = data_manager.change_plot_add(request)

        return json.dumps(chart)


@app.route('/hook_topic', methods=["GET", "POST", 'OPTIONS'])
def change_plot_topic():
    if request.method == 'POST':
        chart = data_manager.change_plot_topic(request)

        return json.dumps(chart)


@app.route('/hook_rubric', methods=["GET", "POST", 'OPTIONS'])
def change_plot_rubric():
    if request.method == 'POST':
        chart = data_manager.change_plot_rubric(request)

        return json.dumps(chart)


@app.route('/initial', methods=["GET", "POST", 'OPTIONS'])
def get_data():
    if request.method == 'GET':
        data_dict = data_manager.get_initial_data()
        print('data_dict', data_dict.keys())
        # data_dict = {'rubrics_dict': rubrics_dict, 'topics_dict': topics_dict}
        return json.dumps(data_dict)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
