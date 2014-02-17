from flask import Flask, render_template, send_from_directory, request
import jinja2
import json
import IPython.html
import os


class NbFlask(Flask):
    jinja_loader = jinja2.FileSystemLoader([
        IPython.html.__path__[0] + '/templates',
        os.path.dirname(os.path.realpath(__file__)) + '/templates'
    ])

    notebooks = []

    def shutdown_callback(self, callback):
        self.shutdown = callback

    def add_notebook(self, nb):
        self.notebooks.append(nb)

app = NbFlask(__name__, static_folder=IPython.html.__path__[0] + '/static')


@app.route('/nbdiff/<path:filename>')
def nbdiff_static(filename):
    return send_from_directory(os.path.dirname(os.path.realpath(__file__))
                               + '/static', filename)


@app.route('/')
def home():
    return render_template('nbdiff.html', project='/', base_project_url='/',
                           base_kernel_url='/', notebook_id='test_notebook')


@app.route('/notebooks/test_notebook', methods=['GET', 'PUT'])
def notebookjson():
    if request.method == 'PUT':
        app.shutdown(request.data)
        request.environ.get('werkzeug.server.shutdown')()
        return ""
    else:
        parsed = app.notebooks[0]
        return json.dumps(parsed)

if __name__ == '__main__':
    app.run(debug=True)
