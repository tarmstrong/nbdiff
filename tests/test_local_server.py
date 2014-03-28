from flask import request
import IPython

from nbdiff.server.local_server import (
    NbFlask,
    app,
    nbdiff_static,
    home,
    notebookjson,
    shutdown,
)
 
callback = True

def fake_callback(contents, filename):
    callback = True


def test_home():
    client = app.test_client()
    result = client.get('/1')
    assert result.status_code == 200
 
 
def test_notebookjson():
    client = app.test_client()
    app.add_notebook({'metadata': {}}, 'foo.ipynb')
    result = client.get('/notebooks/test_notebook0')
    assert result.status_code == 200

    app.shutdown_callback(fake_callback)
    contents = ''
    result = client.put('/notebooks/test_notebook0', contents)
    filename = 'hello.ipynb'
    app.shutdown(result.data, filename)
    assert callback

    
