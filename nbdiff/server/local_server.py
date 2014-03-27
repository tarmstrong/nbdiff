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

    def add_notebook(self, nb, fname):
        self.notebooks.append((nb, fname))

app = NbFlask(__name__, static_folder=IPython.html.__path__[0] + '/static')


@app.route('/nbdiff/<path:filename>')
def nbdiff_static(filename):
    return send_from_directory(os.path.dirname(os.path.realpath(__file__))
                               + '/static', filename)


@app.route('/<int:notebookid>')
def home(notebookid):
    return render_template(
        'nbdiff.html',
        project='/',
        base_project_url='/',
        base_kernel_url='/',
        notebook_id='test_notebook' + str(notebookid),
        num_nbks=str(len(app.notebooks)),
        cur_nbk=str(notebookid),
        local=True,
    )


@app.route('/notebooks/test_notebook<int:notebookid>', methods=['GET', 'PUT'])
def notebookjson(notebookid):
    if request.method == 'PUT':
        app.shutdown(request.data, app.notebooks[notebookid][1])
        return ""
    else:
        parsed, filename = app.notebooks[notebookid]
        parsed['metadata']['filename'] = filename
        return json.dumps(parsed)


@app.route('/shutdown')
def shutdown():
    request.environ.get('werkzeug.server.shutdown')()
    return "The server was shutdown."

if __name__ == '__main__':
    app.run(debug=True)
