// nbdiff.js
//
// Copyright (c) 2013-2014 the NBDiff team
// 
// Permission is hereby granted, free of charge, to any person obtaining a copy of
// this software and associated documentation files (the "Software"), to deal in
// the Software without restriction, including without limitation the rights to
// use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
// the Software, and to permit persons to whom the Software is furnished to do so,
// subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
// FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
// COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
// IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
// CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

window.NBDiff = (function ($) {

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

/**
 * Main NBDiff controller for initiating merge/diff.
 */
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
                $('#nbdiff-save').hide();
            } else if (this._isMerge() === true) {
                this.controller = new Merge(this.notebook, this._nbcells);
                $('#nbdiff-save').click(function (event) {
                    event.preventDefault();
                    self.save();
                });
            }

            var nbcontainer = this._generateNotebookContainer();
            $('#notebook').append(nbcontainer);
            this.controller.render(nbcontainer);

        } else {
            this.log('No nbdiff metadata in the notebook.');
            this.log('Showing the normal notebook container.');
        }
    },
    save: function () {
        var mergedCellElements,
            nbcell,
            i;

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
            else {
            }
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
    _generateNotebookContainer: function () {
        return $("<div class='container' id='notebook-container-new' style='display:inline'></div>");
    }
};

/**
 * Controller for rendering the merge.
 */
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
            self._container.append(mr.render());
        });
        this.rows = rows;
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

/**
 * Controller for rendering the Diff.
 */
function Diff(notebook, nbcells) {
    this._nb = notebook;
    this._nbcells = nbcells;
    this._container = null;
}

Diff.prototype = {
    render: function (container) {
        var self = this,
            rows;
        this._container = container;
        rows = this._generateRows();
        rows.forEach(function (dr) {
            self._container.append(dr.render());
        });
    },
    _generateRows: function () {
        var rows = [];
        this._nbcells.forEach(function (nbcell) {
            rows.push(new DiffRow(nbcell));
        });
        return rows;
    }
};

/**
 * Class for rendering rows of the merge UI.
 */
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

        if (this._cells.local.state() !== 'unchanged' &&
                 this._cells.local.state() !== 'empty' ) {
            row.find("input.merge-arrow-right").click(function(state) {
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
            }(this._cells.local.state()));
        } else {
            row.find("input.merge-arrow-right").hide();
        }

        if (this._cells.remote.state() !== 'unchanged' &&
               this._cells.remote.state() !== 'empty' ) {
            row.find("input.merge-arrow-left").click(function(state) {
                return function() {
                    var rightCell = row.find('.row-cell-merge-remote .cell').clone(true);
                    rightCell.addClass(getStateCSS(state));
                    var htmlClass = ".row-cell-merge-base";
                    row.children(htmlClass).find('.cell').replaceWith(rightCell);
                };
            }(this._cells.remote.state()));
        } else {
            row.find("input.merge-arrow-left").hide();
        }
        return row;
    },
    _fillColumn: function (target, nbcell) {
        var cellHTML = nbcell.element();
        cellHTML.addClass(getStateCSS(nbcell.state()));
        var htmlClass = ".row-cell-merge-" + nbcell.side();
        cellHTML.addClass('nbdiff-' + nbcell.state());

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

/**
 * Class for rendering rows of the diff UI.
 */
function DiffRow(nbcell) {
    this._nbcell = nbcell;
}

DiffRow.prototype = {
    render: function () {
        var row;
        row = this._emptyRow();
        this._fillColumn(row, this._nbcell);
        return row;
    },
    _fillColumn: function (lastRow, nbcell) {
        var cellHTML = nbcell.element();
        var htmlClass, targetContainer;
        var targets = [ ".row-cell-diff-left", ".row-cell-diff-right"];

        if (nbcell.state() === cellState[0]) {
            targetContainer = ".row-cell-diff-right";
            cellHTML.addClass('added-cell');
        } else if (nbcell.state() === cellState[1]) {
            targetContainer = ".row-cell-diff-left";
            cellHTML.addClass('deleted');
        }

        if (nbcell.state() === cellState[3]) {
            // If it's an unchanged cell, add to both sides.
            // TODO grey them out as well
            targets.forEach(function (target) {
                lastRow.children(target).append(cellHTML.clone());
            });
        } else {
            // Otherwise, determine based on side where to place.
            lastRow.children(targetContainer).append(cellHTML);
        }
    },
    _emptyRow: function () {
        var html = "<div class='row'>" + "<div class='row-cell-diff-left'></div>" + "" + "<div class='row-cell-diff-right'></div>" + "</div>";
        return $(html);
    }
};

// Decorator for cells from IPython's cell.js
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

return {
    NBDiff: NBDiff,
    Merge: Merge,
    Diff: Diff,
    DiffRow: DiffRow,
    MergeRow: MergeRow,
    NBDiffCell: NBDiffCell
};

}(jQuery));

function nbdiff_init() {
    var main = new NBDiff.NBDiff(IPython.notebook, true);
    main.init();
}

if (typeof IPython.notebook === 'undefined') {
    $([IPython.events]).bind('notebook_loaded.Notebook', nbdiff_init);
} else {
    nbdiff_init();
}
