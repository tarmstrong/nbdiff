import os
import unittest
import nbdiff.server.command.AboutUsCommand as aucmd
import nbdiff.server.command.ComparisonCommand as ccmd
import nbdiff.server.command.ContactUsCommand as cucmd
import nbdiff.server.command.DiffCommand as dcmd
import nbdiff.server.command.DiffURLCommand as ducmd
import nbdiff.server.command.FaqCommand as fcmd
import nbdiff.server.command.MergeCommand as mcmd
import nbdiff.server.command.MergeURLCommand as mucmd
import nbdiff.server.command.NotebookRequestCommand as nrcmd
import nbdiff.server.command.ResourceRequestCommand as rrcmd
import nbdiff.server.command.SaveNotebookCommand as sncmd
import nbdiff.server.command.UploadCommand as ucmd
import nbdiff.server.remote_server as rs
import nbdiff.server.database as db
import bitarray
from pretend import stub
from sqlalchemy import create_engine
from nbdiff.server.database.nbdiffModel import nbdiffModel

app = rs.app.test_client()
parentPath = os.path.abspath(
    os.path.join(
        os.path.realpath(os.path.dirname(__file__)),
        os.pardir
    )
)
SCRIPTS_DIR = os.path.join(parentPath, "scripts")
MERGE_NB_DIR = os.path.join(SCRIPTS_DIR, 'example-notebooks', 'merge', '0')
DIFF_NB_DIR = os.path.join(SCRIPTS_DIR, 'example-notebooks', 'diff', '0')
db.engine = create_engine(
    'sqlite:///nbdiff/server/database/TestNbdiffResult',
    convert_unicode=True
)
db.init_db()
nbdiffModel.query.delete()

def mock_redirect(path, **kwargs):
    assert "code" in kwargs
    assert kwargs["code"] == 302
    return path


def mock_render_template(filename, **kwargs):
    assert "err" not in kwargs
    return filename


def mock_make_response(data):
    return stub(headers={"Content-Type": '', "Content-Disposition": ''})


class RemoteServerTest(unittest.TestCase):

    def test_run_command(self):
        ucmd.render_template = mock_render_template
        response = rs.run_command("Upload", None)
        assert response == "upload.html"

    def test_get_Class(self):
        cmd = "nbdiff.server.command.UploadCommand"
        module = "module 'nbdiff.server.command.UploadCommand' "
        assert module in str(rs.get_class(cmd))


class AboutUsCommandTest(unittest.TestCase):

    def test_newInstance(self):
        assert isinstance(
            rs.get_class("nbdiff.server.command.AboutUsCommand").newInstance(),
            aucmd.AboutUsCommand
        )

    def test_process(self):
        aucmd.render_template = mock_render_template
        template = aucmd.AboutUsCommand().process(None, None, None)
        assert template == "aboutUs.html"


class ContactUsCommandTest(unittest.TestCase):

    def test_newInstance(self):
        classname = "nbdiff.server.command.ContactUsCommand"
        assert isinstance(
            rs.get_class(classname).newInstance(),
            cucmd.ContactUsCommand
        )

    def test_process(self):
        cucmd.render_template = mock_render_template
        template = cucmd.ContactUsCommand().process(None, None, None)
        assert template == "contactUs.html"


class FaqCommandTest(unittest.TestCase):

    def test_newInstance(self):
        classname = "nbdiff.server.command.FaqCommand"
        assert isinstance(
            rs.get_class(classname).newInstance(),
            fcmd.FaqCommand
        )

    def test_process(self):
        fcmd.render_template = mock_render_template
        template = fcmd.FaqCommand().process(None, None, None)
        assert template == "faq.html"


class ComparisonCommandTest(unittest.TestCase):

    def test_newInstance(self):
        classname = "nbdiff.server.command.ComparisonCommand"
        assert isinstance(
            rs.get_class(classname).newInstance(),
            ccmd.ComparisonCommand
        )

    def test_process(self):
        ccmd.render_template = mock_render_template
        session = db.db_session()
        ba = bitarray.bitarray()
        ba.fromstring("test")
        obj = nbdiffModel(ba.to01())
        session.add(obj)
        session.commit()
        filename = obj.id
        response = ccmd.ComparisonCommand().process(None, filename, session)
        assert response == "nbdiff.html"
        response = app.get("/Comparision/"+str(filename))
        assert response.status == "200 OK"


class DiffCommandTest(unittest.TestCase):

    def test_newInstance(self):
        classname = "nbdiff.server.command.DiffCommand"
        assert isinstance(
            rs.get_class(classname).newInstance(),
            dcmd.DiffCommand
        )

    def test_process(self):
        dcmd.render_template = mock_render_template
        dcmd.redirect = mock_redirect
        session = db.db_session()
        beforeStream = open(os.path.join(DIFF_NB_DIR, "before.ipynb"), 'r')
        afterStream = open(os.path.join(DIFF_NB_DIR, "after.ipynb"), 'r')
        request = stub(form={
            'beforeJSON': beforeStream.read(),
            'afterJSON': afterStream.read()
        })
        beforeStream.close()
        beforeStream.close()

        response = dcmd.DiffCommand().process(request, None, session)
        assert "/Comparison/" in response
        split = str.split(response, "/")
        assert split[-1].isdigit()


class DiffURLCommandTest(unittest.TestCase):

    def test_newInstance(self):
        classname = "nbdiff.server.command.DiffURLCommand"
        assert isinstance(
            rs.get_class(classname).newInstance(),
            ducmd.DiffURLCommand
        )

    def test_process(self):
        ducmd.redirect = mock_redirect
        ducmd.render_template = mock_render_template
        mainurl = "https://raw.githubusercontent.com/"
        mainurl = mainurl + "tarmstrong/nbdiff/master/scripts/"
        before = mainurl+"example-notebooks/diff/0/before.ipynb"
        after = mainurl+"example-notebooks/diff/0/after.ipynb"
        session = db.db_session()
        request = stub(form={'beforeURL': before, 'afterURL': after})
        response = ducmd.DiffURLCommand().process(request, None, session)
        assert "/Comparison/" in response
        split = str.split(response, "/")
        assert split[-1].isdigit()


class MergeCommandTest(unittest.TestCase):

    def test_newInstance(self):
        classname = "nbdiff.server.command.MergeCommand"
        assert isinstance(
            rs.get_class(classname).newInstance(),
            mcmd.MergeCommand
        )

    def test_process(self):
        mcmd.render_template = mock_render_template
        mcmd.redirect = mock_redirect
        session = db.db_session()
        localStream = open(os.path.join(MERGE_NB_DIR, "local.ipynb"), 'r')
        baseStream = open(os.path.join(MERGE_NB_DIR, "base.ipynb"), 'r')
        remoteStream = open(os.path.join(MERGE_NB_DIR, "remote.ipynb"), 'r')
        request = stub(form={
            'localJSON': localStream.read(),
            'baseJSON': baseStream.read(),
            'remoteJSON': remoteStream.read()
        })
        localStream.close()
        baseStream.close()
        remoteStream.close()

        response = mcmd.MergeCommand().process(request, None, session)
        assert "/Comparison/" in response
        split = str.split(response, "/")
        assert split[-1].isdigit()


class MergeURLCommandTest(unittest.TestCase):

    def test_newInstance(self):
        classname = "nbdiff.server.command.MergeURLCommand"
        assert isinstance(
            rs.get_class(classname).newInstance(),
            mucmd.MergeURLCommand
        )

    def test_process(self):
        mucmd.redirect = mock_redirect
        mucmd.render_template = mock_render_template
        mainurl = "https://raw.githubusercontent.com/"
        mainurl = mainurl + "tarmstrong/nbdiff/master/scripts/"
        local = mainurl+"example-notebooks/merge/0/local.ipynb"
        base = mainurl+"example-notebooks/merge/0/base.ipynb"
        remote = mainurl+"example-notebooks/merge/0/remote.ipynb"
        session = db.db_session()
        request = stub(form={
            'localURL': local,
            'baseURL': base,
            'remoteURL': remote
        })
        response = mucmd.MergeURLCommand().process(request, None, session)
        assert "/Comparison/" in response
        split = str.split(response, "/")
        assert split[-1].isdigit()


class NotebookRequestCommandTest(unittest.TestCase):

    def test_newInstance(self):
        classname = "nbdiff.server.command.NotebookRequestCommand"
        assert isinstance(
            rs.get_class(classname).newInstance(),
            nrcmd.NotebookRequestCommand
        )

    def test_process(self):
        session = db.db_session()
        localStream = open(os.path.join(MERGE_NB_DIR, "local.ipynb"), 'r')
        data = localStream.read()
        ba = bitarray.bitarray()
        ba.fromstring(data)
        obj = nbdiffModel(ba.to01())
        session.add(obj)
        session.commit()
        filename = obj.id
        response = nrcmd.NotebookRequestCommand().process(
            None,
            filename,
            session
        )
        assert response == data
        response = app.get("/notebooks/"+str(filename))
        assert response.data == data


class ResourceRequestCommandTest(unittest.TestCase):

    def test_newInstance(self):
        classname = "nbdiff.server.command.ResourceRequestCommand"
        assert isinstance(
            rs.get_class(classname).newInstance(),
            rrcmd.ResourceRequestCommand
        )

    def test_process(self):
        response = app.get("/nbdiff/js/main.js")
        assert response.status == "200 OK"


class SaveNotebookCommandTest(unittest.TestCase):

    def test_newInstance(self):
        classname = "nbdiff.server.command.SaveNotebookCommand"
        assert isinstance(
            rs.get_class(classname).newInstance(),
            sncmd.SaveNotebookCommand
        )

    def test_process(self):
        sncmd.make_response = mock_make_response
        nbStream = open(os.path.join(MERGE_NB_DIR, "base.ipynb"), 'r')
        request = stub(form={'download_data': nbStream.read()})
        nbStream.close()
        response = sncmd.SaveNotebookCommand().process(request, None, None)
        contentDisposition = "attachment; filename=mergedNotebook.ipynb"
        assert response.headers["Content-Disposition"] == contentDisposition


class UploadCommandTest(unittest.TestCase):

    def test_newInstance(self):
        assert isinstance(
            rs.get_class("nbdiff.server.command.UploadCommand").newInstance(),
            ucmd.UploadCommand
        )

    def test_process(self):
        ucmd.render_template = mock_render_template
        template = ucmd.UploadCommand().process(None, None, None)
        assert template == "upload.html"
