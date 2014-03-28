from nbdiff.server.local_server import (
    app,
)


def test_home():
    client = app.test_client()
    result = client.get('/1')
    assert result.status_code == 200


def test_notebookjson():
    client = app.test_client()
    app.add_notebook({'metadata': {}}, 'foo.ipynb')
    result = client.get('/notebooks/test_notebook0')
    assert result.status_code == 200

    def fake_callback(contents, filename):
        fake_callback.called = True

    app.shutdown_callback(fake_callback)
    contents = ''
    result = client.put('/notebooks/test_notebook0', contents)
    assert result.data == "", result
    assert fake_callback.called
