from flask import Flask, request
import jinja2
import IPython.html
import os

class NbFlask(Flask):
  jinja_loader = jinja2.FileSystemLoader([
      IPython.html.__path__[0] + '/templates',
      os.path.dirname(os.path.realpath(__file__)) + '/templates'
  ])
  
  def shutdown_callback(self, callback):
      self.shutdown = callback

  def add_notebook(self, nb):
      self.notebooks.append(nb)

app = NbFlask(__name__, static_folder=IPython.html.__path__[0] + '/static')

def get_class( classname ):
  components = classname.split('.')
  module = ".".join(components)
  obj = __import__( module)
  for comp in components[1:]:
      obj = getattr(obj, comp)            
  return obj

def run_command(cmdName, request, filename):
  cmd = "nbdiff.server.command."+cmdName+"Command"
  command = get_class(cmd).newInstance()
  return command.process(request, filename)

#index
@app.route("/")
def upload():
  return run_command("Upload", request, None)

#runs depending on different command URL
@app.route("/<path:command>", methods=['GET', 'POST'])
def redirectCommand(command):
  return run_command(command, request, None)

#notebook request handler
@app.route('/notebooks/<path:filename>', methods=['GET', 'PUT'])
def notebookRequest(filename):
  if request.method == 'PUT':
    app.shutdown(request.data)
    request.environ.get('werkzeug.server.shutdown')()
    return ""
  else:
    return run_command("NotebookRequest", request, filename)

#used to get specific resources in the html pages. 
@app.route('/nbdiff/<path:filename>')
def nbdiff_static(filename):
  return run_command("ResourceRequest", request, filename)
  
if __name__ == "__main__":
    app.debug = False
    app.run()

