===========================================================
JavaScript used by IPython for rendering cells
===========================================================

.. contents:: Javascript files

See
`IPython/html/static/notebook/js <https://github.com/ipython/ipython/tree/master/IPython/html/static/notebook/js>`__

notebook.js
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See
`notebook.js <https://github.com/ipython/ipython/blob/master/IPython/html/static/notebook/js/notebook.js>`__.

Related functions:
^^^^^^^^^^^^^^^^^^^^^^^^^

**Notebook.prototype.load_notebook(notebook_id)**

    *Request a notebook's data from the server.*
    
    *@method load_notebook*
    
    *@param {String} notebook_id A notebook to load*

**Notebook.prototype.load_notebook_success(data, status, xhr)**
	
    *Success callback for loading a notebook from the server.*
    
    *Load notebook data from the JSON response.*
    
    *@method load_notebook_success*
    
    *@param {Object} data JSON representation of a notebook*
    
    *@param {String} status Description of response status*
    
    *@param {jqXHR} xhr jQuery Ajax object*
    
**Notebook.prototype.fromJSON(data)**

    *Load a notebook from JSON (.ipynb).*

    *This currently handles one worksheet: others are deleted.*
    
    *@method fromJSON*
    
    *@param {Object} data JSON representation of a notebook*

**Notebook.prototype.toJSON()**

    *Dump this notebook into a JSON-friendly object.*
    
    *@method toJSON*
    
    *@return {Object} A JSON-friendly representation of this notebook.*
 
**Notebook.prototype.insert_cell_below(type, index)**

    *Inserts a cell below*

**Notebook.prototype.insert_cell_at_index(type, index)**

    *Inserts a cell at a given index*

**Notebook.prototype.move_cell_up(index)**

    *Move given (or selected) cell up and select it.*
    
    *@method move_cell_up*
    
    *@param [index] {integer} cell index*
    
    *@return {Notebook} This notebook*

**Notebook.prototype.move_cell_down(index)**

    *Move given (or selected) cell down and select it*
    
    *@method move_cell_down*
    
    *@param [index] {integer} cell index*
    
    *@return {Notebook} This notebook*

**Notebook.prototype.delete_cell(index)**

    *Delete a cell from the notebook.*
    
    *@method delete_cell*
    
    *@param [index] A cell's numeric index*
    
    *@return {Notebook} This notebook*

**Notebook.prototype.create_elements()**

    *Creates html elements for notebook with css*

cell.js
~~~~~~~~~~~~~

The Base `Cell` class from which to inherit @class Cell.

codecell.js
~~~~~~~~~~~~~~~

CodeCell extends Cell.

**CodeCell.prototype = new IPython.Cell();**

Related functions:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**CodeCell.prototype.fromJSON(data)**	

    *Create Text cell from JSON*
    
    *@param {json} data - JSON serialized text-cell*
    
    *@method fromJSON*
    
    *Sets text in cell with code, and cell input number*

**CodeCell.prototype.toJSON**
    
    *Generate JSON from CodeCell*

testcell.js
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TextCell extends Cell.

**TextCell.prototype = new IPython.Cell();**

Related functions:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**TextCell.prototype.toJSON**

    *Generate JSON from cell*

    *@return {object} cell data serialised to json*

**TextCell.prototype.fromJSON(data)**

    *Creates textcell from JSON*

HeadingCell related functions:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The HeadingCell class extends TextCell. 
 
**HeadingCell.prototype.toJSON**

    *@method toJSON*

**HeadingCell.prototype.fromJSON(data)**

    *Creates headingcell from JSON*


outputarea.js
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Related functions:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**OutputArea.prototype.fromJSON(outputs)**

    *JSON serialization*

**OutputArea.prototype.append_output(json, dynamic)**

    *Checks type of output and delegates to one of:*
	
**OutputArea.prototype.append_pyout(json, dynamic)**

    *Appends python output*
	
**OutputArea.prototype.append_pyerr(json)**

    *I assume it appends python output*
	
**OutputArea.prototype.append_display_data(json, dynamic)**

    *If output type is display_data*

**OutputArea.prototype.append_stream(json)**

    *If output type is stream*
