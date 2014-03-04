function initToolbar(info) {
    var mode = info.mode;
    var save = info.save;
    
    if (mode === 'diff') {
    } else if (mode === 'merge') {
        $('#nbdiff-save').click(function (event) {
            event.preventDefault();
            remoteSave();
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
}
function remoteSave(){

    var mergedCellElements;

    if (this._isDiff() === true) {
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


    this._init_cells();
    this._nbcells.forEach(function (nbcell) {
        if (nbcell.state() === 'added' || nbcell.state() === 'unchanged') {
            nbcell.removeMetadata();
        }
    });

    delete IPython.notebook.metadata['nbdiff-type'];

    //TODO:replace with server request to save to .ipynb
    //IPython.notebook.save_notebook();
}
