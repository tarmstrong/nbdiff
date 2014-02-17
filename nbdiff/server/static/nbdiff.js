function nbdiff() {

    var cellState = ['added', 'deleted', 'modified', 'unchanged', 'empty'];
    var cellSide = ['local', 'base', 'remote'];
    var cells = IPython.notebook.get_cells();
    
    //The indexing for IPython.notebook.get_cells_element(index) messes up with append in 
    //generate_merge_column so this data-structure was created to preserve index.
    var cellElements = [];
    for(var i = 0; i < cells.length; i++){
        cellElements[i] = IPython.notebook.get_cell_element(i);
    }

    var init = function() {
        var cells = IPython.notebook.get_cells();
        console.log('Initializing nbdiff.');
        if (cells.length > 0 && typeof cells[0].metadata.state !== 'undefined') {
            $('#notebook-container').css("visibility", "hidden");
            console.log('Found nbdiff metadata in the notebook.');
            console.log('Hiding the normal notebook container.');
            $('#notebook-container').hide();
            console.log('Creating a new notebook container.');
            $('#notebook').append(generate_notebook_container());

            console.log('Initializing merge/diff rows.');
            init_notebook_merge_rows();

            $('#nbdiff-save').click(function (event) {
                nbmerge_save();
            });
        } else {
            console.log('No nbdiff metadata in the notebook.');
            console.log('Showing the normal notebook container.');
        }
    };

    var init_notebook_merge_rows = function() {
        var type = IPython.notebook.metadata['nbdiff-type'];
        console.log("This is a ", type, "notebook");
        for (var i = 0; i < cells.length; i++) {
            console.log('Processing cell #' + i + '...');
            if(type === 'merge'){
                parse_merge_row(cells[i], i);
            } else if(type === 'diff'){
                parse_diff_row(cells[i], i);
            } else{
                console.log('nbdiff-type not recognized');
            }
        }
        $('#notebook-container-new').append(generate_notebook_container_end_space());
    };

    var parse_merge_row = function(cell, index) {
        var side = cell.metadata.side;
        var state = cell.metadata.state;
        if (side === cellSide[0]) {
            console.log('New row. Adding local cell.');
            var new_row = $(generate_empty_merge_row());
            new_row.find("input.merge-arrow-right").click(function(index, state, row) {
                return function() {
                    // TODO we need to keep track, in memory, of the in-memory cells we're moving around
                    //      so that we can exfiltrate the data and save the resulting notebook.
                    var rightCell = row.find('.row-cell-merge-local .cell').clone(true);
                    rightCell.addClass(getStateCSS(state));
                    var htmlClass = ".row-cell-merge-base";
                    // TODO this shouldn't obliterate the base cell -- we should
                    //      be able to undo this operation.
                    // TODO allow me to change my mind and merge the
                    //      local version instead of the remote.
                    row.children(htmlClass).find('.cell').replaceWith(rightCell);
                };
            }(index, state, new_row));

            new_row.find("input.merge-arrow-left").click(function(index, state, row) {
                return function() {
                    var rightCell = row.find('.row-cell-merge-remote .cell').clone(true);
                    rightCell.addClass(get_state_css(state));
                    var htmlClass = ".row-cell-merge-base";
                    row.children(htmlClass).find('.cell').replaceWith(rightCell);
                };
            }(index, state, new_row));

            $('#notebook-container-new').append(new_row);
        } else {
            console.log('Adding ' + side + ' cell.');
        }
        generate_merge_column(side, state, index);

        var current_row = $("#notebook-container-new").children().last();
        if (state === cellState[3] || state === cellState[4]) {
            if (side === cellSide[2]) {
                current_row.find("input.merge-arrow-left").hide();
            } else if (side === cellSide[0]) {
                current_row.find("input.merge-arrow-right").hide();
            }
        }
    };

    var parse_diff_row = function (cell, index){
        var state = cell.metadata.state;
        var new_row = $(generate_empty_diff_row());
        $('#notebook-container-new').append(new_row);
        generate_diff_column(state, index);
    };

    var generate_merge_column = function(side, state, index) {
        var cellHTML = cellElements[index];
        cellHTML.addClass(getStateCSS(state));
        var lastRow = $("#notebook-container-new").children().last();
        var htmlClass = ".row-cell-merge-" + side;
        lastRow.children(htmlClass).append(cellHTML);
    };
    
    var generate_diff_column = function(state, index) {
        var cellHTML = cellElements[index];
        var htmlClass, targetContainer;
        var lastRow = $("#notebook-container-new").children('.row').last();
        var targets = [ ".row-cell-diff-left", ".row-cell-diff-right"];

        if (state === cellState[0]) {
            targetContainer = ".row-cell-diff-right";
            cellHTML.addClass('added-cell');
        } else if (state === cellState[1]) {
            targetContainer = ".row-cell-diff-left";
            cellHTML.addClass('deleted');
        }

        if (state === cellState[3]) {
            // If it's an unchanged cell, add to both sides.
            // TODO grey them out as well
            targets.forEach(function (target) {
                lastRow.children(target).append(cellHTML.clone());
            });
        } else {
            // Otherwise, determine based on side where to place.
            lastRow.children(targetContainer).append(cellHTML);
        }
    };

    var getStateCSS = function(state) {
        if (state === cellState[0]) {
            return "added-cell";
        } else if (state == cellState[1]) {
            return "deleted";
        } else if (state == cellState[2]) {
            return "changed";
        } else {
            return "";
        }
    };
    
    var generate_merge_control_column = function(side) {
        var mergeArrowClass = 'merge-arrow-left';
        if (side === cellSide[0]) {
            return "<input value='->' data-cell-idx='0' class='merge-arrow-right' type='button'>";
        } else {
            return "<input value='<-' data-cell-idx='0' class='merge-arrow-left' type='button'>";
        }
    };

    var generate_empty_merge_row = function() {
        return "<div class='row'>" + "<div class='row-cell-merge-local'></div>" + "<div class='row-cell-merge-controls-local'>" + generate_merge_control_column("local") + "</div>" + "<div class='row-cell-merge-remote'></div>" + "<div class='row-cell-merge-controls-remote'>" + generate_merge_control_column("remote") + "</div>" + "<div class='row-cell-merge-base'></div>" + "</div>";
    };

    var generate_empty_diff_row = function() {
        return "<div class='row'>" + "<div class='row-cell-diff-left'></div>" + "" + "<div class='row-cell-diff-right'></div>" + "</div>";
    };

    var generate_notebook_container = function() {
        return "<div class='container' id='notebook-container-new' style='display:inline'></div>";
    };

    var generate_notebook_container_end_space = function() {
        return "<div class='end_space'></div>";
    };
    
    
    init();
};

(function () {

var cellState = ['added', 'deleted', 'modified', 'unchanged', 'empty'];
var cellSide = ['local', 'base', 'remote'];

function getStateCSS(state) {
    if (state === cellState[0]) {
        return "added-cell";
    } else if (state == cellState[1]) {
        return "deleted";
    } else if (state == cellState[2]) {
        return "changed";
    } else {
        return "";
    }
};

function NBDiff(notebook, log) {
    this.notebook = notebook;
    if (log === true) {
        this.log = function () {
            console.log(arguments);
        };
    } else {
        this.log = function () {};
    }

}

NBDiff.prototype = {
    init: function () {
        var self = this;
        this._init_cells();
        this.log('Initializing nbdiff.');
        if (this._hasNBDiffMetadata() === true) {
            $('#notebook-container').css("visibility", "hidden");
            this.log('Found nbdiff metadata in the notebook.');
            this.log('Hiding the normal notebook container.');
            $('#notebook-container').hide();
            this.log('Creating a new notebook container.');

            if (this._isDiff() === true) {
                this.controller = new Diff(this.notebook, this._nbcells);
            } else if (this._isMerge() === true) {
                this.controller = new Merge(this.notebook, this._nbcells);
            }

            $('#notebook').append(this._generateNotebookContainer());
            this.controller.render($('#notebook'));

            $('#nbdiff-save').click(function (event) {
                self.save();
            });
        } else {
            this.log('No nbdiff metadata in the notebook.');
            this.log('Showing the normal notebook container.');
        }
    },
    save: function () {
        var nbdiffCells,
            mergedCells,
            mergedCellElements = $('#notebook-container-new .row .row-cell-merge-base .cell').clone(true),
            index;

        // Clear the original notebook div.
        $('#notebook-container').empty();

        // Copy the chosen cells into the original notebook div.
        for (index = 0; index < mergedcells.length; index++) {
            $('#notebook-container').append(mergedCellElements[index]);
        }

        mergedCells = IPython.notebook.get_cells();
        nbdiffCells = mergedCells.forEach(function (cell) {
            return new NBDiffCell(cell);
        });

        nbdiffCells.forEach(function (item) {
            item.remove_metadata();
        });

        IPython.notebook.save_notebook();
    },
    _init_cells: function () {
        var self = this;
        this._cells = IPython.notebook.get_cells();
        this._nbcells = [];
        this._cells.forEach(function (cell) {
            self._nbcells.push(new NBDiffCell(cell));
        });
    },
    _hasNBDiffMetadata: function () {
        return this._nbcells.length > 0 && this._nbcells[0].state() !== 'undefined';
    },
    _isDiff: function () {
        return typeof this.notebook.metadata['nbdiff-type'] !== 'undefined' && this.notebook.metadata['nbdiff-type'] === 'diff';
    },
    _isMerge: function () {
        return typeof this.notebook.metadata['nbdiff-type'] !== 'undefined' && this.notebook.metadata['nbdiff-type'] === 'merge';
    },
    _generateNotebookContainer: function() {
        return "<div class='container' id='notebook-container-new' style='display:inline'></div>";
    }
};

function Merge(notebook, nbcells) {
    this._nb = notebook;
    this._nbcells = nbcells;
    this._container = null;
}

Merge.prototype = {
    render: function (container) {
        var self = this,
            rows;
        this._container = container;
        rows = this._generateRows();
        rows.forEach(function (mr) {
            console.log('hello');
            self._container.append(mr.render());
        });
        console.log('rows', rows);
    },
    _generateRows: function () {
        var rows = [];
        this._nbcells.forEach(function (nbcell) {
            var mr;
            if (nbcell.side() === cellSide[0]) {
                mr = new MergeRow();
                mr.addLocal(nbcell);
                rows.push(mr);
            } else {
                mr = rows[rows.length-1];
                if (nbcell.side() === cellSide[1]) {
                    mr.addBase(nbcell);
                } else {
                    mr.addRemote(nbcell);
                }
            }
        });
        return rows;
    }
};

function Diff(notebook) {
    this.nb = notebook;
    this.rows = [];
}

Diff.prototype = {
    render: function (container) {
        var self = this,
            rows;
        this._container = container;
        rows = this._generateRows();
        rows.forEach(function (mr) {
            console.log('hello');
            self._container.append(mr.render());
        });
        console.log('rows', rows);
    },
    _generateRows: function () {
        var rows = [];
        this._nbcells.forEach(function (nbcell) {
            console.log(nbcell);
        });
        return rows;
    }
};

function MergeRow() {
    this._cells = {};
}

MergeRow.prototype = {
    render: function () {
        var row;
        row = this._emptyRow();
        this._fillColumn(row, this._cells.local);
        this._fillColumn(row, this._cells.base);
        this._fillColumn(row, this._cells.remote);
        return row;
    },
    _fillColumn: function (target, nbcell) {
        console.log(nbcell);
        var cellHTML = nbcell.element();
        cellHTML.addClass(getStateCSS(nbcell.state()));
        var htmlClass = ".row-cell-merge-" + nbcell.side();
        target.children(htmlClass).append(cellHTML);
    },
    _emptyRow: function () {
        var html;
        html = "<div class='row'>" + "<div class='row-cell-merge-local'></div>" + "<div class='row-cell-merge-controls-local'>" + this._generateMergeControlColumn("local") + "</div>" + "<div class='row-cell-merge-remote'></div>" + "<div class='row-cell-merge-controls-remote'>" + this._generateMergeControlColumn("remote") + "</div>" + "<div class='row-cell-merge-base'></div>" + "</div>";
        return $(html);
    },
    _generateMergeControlColumn: function(side) {
        var mergeArrowClass = 'merge-arrow-left';
        if (side === cellSide[0]) {
            return "<input value='->' data-cell-idx='0' class='merge-arrow-right' type='button'>";
        } else {
            return "<input value='<-' data-cell-idx='0' class='merge-arrow-left' type='button'>";
        }
    },
    addLocal: function (nbcell) {
        this._cells.local = nbcell;
    },
    addBase: function (nbcell) {
        this._cells.base = nbcell;
    },
    addRemote: function (nbcell) {
        this._cells.remote = nbcell;
    }
};

function DiffRow(cells) {
    this.before = cells.before;
    this.after = cells.after;
}

DiffRow.prototype = {
    render: function () {
    }
};

// Decorator for cells.
function NBDiffCell(cell) {
    this.cell = cell;
}

NBDiffCell.prototype = {
    side: function () {
        return this.cell.metadata.side;
    },
    state: function () {
        return this.cell.metadata.state;
    },
    removeMetadata: function () {
        delete this.cell.metadata.state;
        delete this.cell.metadata.side;
    },
    element: function () {
        return this.cell.element;
    }
};


function nbdiff_init() {
    var main = new NBDiff(IPython.notebook, true);
    main.init();
}

if (typeof IPython.notebook === 'undefined') {
    $([IPython.events]).bind('notebook_loaded.Notebook', nbdiff_init);
} else {
    nbdiff_init();
}

}());
