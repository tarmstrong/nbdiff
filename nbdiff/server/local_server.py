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
        static_url=static_url,
        notebook_id='test_notebook' + str(notebookid),
        notebook_name='test_notebook' + str(notebookid),
        notebookName='test_notebook' + str(notebookid),
        notebook_path='./',
        notebookPath='./',
        num_nbks=str(len(app.notebooks)),
        cur_nbk=str(notebookid),
        local=True,
    )


# IPython 1.1.0
@app.route('/notebooks/test_notebook<int:notebookid>', methods=['GET', 'PUT'])
def notebookjson(notebookid):
    if request.method == 'PUT':
        app.shutdown(request.data, app.notebooks[notebookid][1])
        return ""
    else:
        parsed, filename = app.notebooks[notebookid]
        parsed['metadata']['filename'] = filename
        return json.dumps(parsed)


# IPython 2.0.0
# TODO refactor to handle both URIs with same function.
@app.route('/api/notebooks/test_notebook<int:notebookid>',
           methods=['GET', 'PUT'])
def notebook(notebookid):
    if request.method == 'PUT':
        request_data = json.loads(request.data)
        content = request_data['content']
        app.shutdown(json.dumps(content), app.notebooks[notebookid][1])
        return ""
    else:
        parsed, filename = app.notebooks[notebookid]
        parsed['metadata']['filename'] = filename
        dump = {'content': parsed}
        dump['name'] = 'test_notebook{:d}'.format(notebookid)
        dump['path'] = './'
        dump['type'] = 'notebook'
        return json.dumps(dump)


@app.route('/shutdown')
def shutdown():
    request.environ.get('werkzeug.server.shutdown')()
    return "The server was shutdown."


def static_url(path, **kwargs):
    # FIXME obvious kludge
    if 'underscore' in path or 'backbone' in path:
        return path[:-3]
    else:
        return 'static/' + path


if __name__ == '__main__':
    app.run(debug=True)
