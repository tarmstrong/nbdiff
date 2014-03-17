function initToolbar(info) {
    var mode = info.mode;
    var save = info.save;
    var controller = info.controller;
    
    if (mode === 'diff') {
    } else if (mode === 'merge') {
        $('#nbdiff-save').click(function (event) {
            event.preventDefault();
            remoteSave(controller);
        });
        $('#nbdiff-undo').click(function () {
            Invoker.undo();
        });
        $('#nbdiff-redo').click(function () {
            Invoker.redo();
        });
        $('button#nbdiff-undo').show();
        
        $('button#nbdiff-redo').show();
        
        $('button#nbdiff-save').show();

    }

    //append a form that allows saving.
    $('body').append("<form action=\"/SaveNotebook\" method=\"POST\" enctype=\"multipart/form-data\" id=\"download\" style=\"display:none\" target=\"_blank\">"+
                    "<input type=\"hidden\" id=\"download_data\" name=\"download_data\"/></form>");
}

function remoteSave(controller) {

    var mergedCellElements;

    if (controller._isDiff() === true) {
        // Not sure how this would have been called since the button is hidden.
        // But if it is, we want to play it safe.
        return;
    }

    mergedCellElements = $('#notebook-container-new .row .row-cell-merge-base .cell').clone(true);

    // Clear the original notebook div.
    $('#notebook-container').empty();
    $('#notebook-container').append(mergedCellElements);
    $('#notebook-container .cell.nbdiff-deleted').remove();
    $('#notebook-container .cell.nbdiff-empty').remove();

    controller._init_cells();
    controller._nbcells.forEach(function (nbcell) {
        if (nbcell.state() === 'added' || nbcell.state() === 'unchanged') {
            nbcell.removeMetadata();
        }
    });

    delete IPython.notebook.metadata['nbdiff-type'];

    //TODO:replace with server request to save to .ipynb
    //IPython.notebook.save_notebook();
    remoteSaveNotebook(IPython.notebook);
}

//Modified code of IPython.notebook.save_notebook() in order to save notebook. 
function remoteSaveNotebook(notebook){

    var data = notebook.toJSON();
    data.metadata.name = notebook.notebook_name;
    data.nbformat = notebook.nbformat;
    data.nbformat_minor = notebook.nbformat_minor;

    $("#download_data").val(JSON.stringify(data));
    $("#download").submit();
}
