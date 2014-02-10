from flask import Flask, render_template, send_from_directory
import jinja2
import json
import IPython.html
import os


class NbFlask(Flask):
    jinja_loader = jinja2.FileSystemLoader([
        IPython.html.__path__[0] + '/templates',
        os.path.dirname(os.path.realpath(__file__)) + '/templates'
    ])

app = NbFlask(__name__, static_folder=IPython.html.__path__[0] + '/static')


@app.route('/nbdiff/<path:filename>')
def nbdiff_static(filename):
    return send_from_directory(os.path.dirname(os.path.realpath(__file__))
                               + '/static', filename)


@app.route('/')
def home():
    return render_template('nbdiff.html', project='/', base_project_url='/',
                           base_kernel_url='/', notebook_id='test_notebook')


@app.route('/notebooks/test_notebook')
def notebookjson():
    parsed = app.pre_merged_notebook
    return json.dumps(parsed)


if __name__ == '__main__':
    app.run(debug=True)
