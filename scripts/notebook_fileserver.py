from flask import Flask, render_template, send_from_directory, request
import jinja2
import json
import IPython.html
import os

static = os.path.abspath(os.path.dirname(__file__)) + '/example-notebooks'

app = Flask(
    __name__,
    static_folder=static,
)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
