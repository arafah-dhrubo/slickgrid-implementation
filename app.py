import json

from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine, text

app = Flask(__name__)
engine = create_engine('postgresql+psycopg2://postgres:1@localhost:5432/stockdb')
connection = engine.connect()


@app.route("/")
def index():
    return "Hello world"


@app.route("/example-0070-plugin-state")
def example_0070_plugin_state():
    return render_template("example-0070-plugin-state.html")


@app.route("/example-grid-menu")
def example_grid_menu():
    query_for_header = f"SELECT column_name FROM information_schema.columns WHERE table_name = 'company'"
    fields = connection.execute(text(query_for_header))

    # construct SELECT statement
    headers = [field[0] for field in fields]
    columns = ", ".join(headers)
    query_for_all = f'SELECT {columns} FROM company'

    columns = []
    for header in headers:
        column = {'id': header, 'name': header, 'field': header,
                  "behavior": "select", "cannotTriggerInsert": False,
                  "cssClass": "cell-selection", "defaultSortAsc": True,
                  "excludeFromColumnPicker": True, "focusable": True,
                  "headerCssClass": True, "minWidth": 30, "rerenderOnResize": True, "resizable": True,
                  "selectable": True, "sortable": True, "width": 140, "widthRequest": 60
                  }
        columns.append(column)

    list = connection.execute(text(query_for_all)).fetchall()
    data = [{headers[i]: tup[i] for i in range(len(headers))} for tup in list]
    return render_template("example-grid-menu.html", fields=columns, list=data)
