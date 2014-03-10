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
    } else if (state === cellState[1]) {
        return "deleted";
    } else if (state === cellState[2]) {
        return "changed";
    } else {
        return "";
    }
}

/**
 * Main NBDiff controller for initiating merge/diff.
 */
function NBDiff(notebook, log) {
    this.notebook = notebook;
    this.controller = null;
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
            this.log('Found nbdiff metadata in the notebook.');

            this.log('Hiding the normal notebook container.');
            $('#notebook-container').css("visibility", "hidden");
            $('#notebook-container').hide();

            if (this._isDiff() === true) {
                this.controller = new Diff(this.notebook, this._nbcells);
            } else if (this._isMerge() === true) {
                this.controller = new Merge(this.notebook, this._nbcells);
            }

            this.log('Calling preRender.');
            this.controller.preRender(self);
            
            this.log('Creating a new notebook container.');
            var nbcontainer = this._generateNotebookContainer();
            $('#notebook').append(nbcontainer);

            this.controller.render(nbcontainer);

            this.log('Calling postRender.');
            this.controller.postRender();
        } else {
            this.log('No nbdiff metadata in the notebook.');
            this.log('Showing the normal notebook container.');
        }
    },
    save: function () {
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
    },
    getMergeRows: function() {
        return this.controller.rows;
    }
};

/**
 * Controller for rendering the merge.
 */
function Merge(notebook, nbcells) {
    this._nb = notebook;
    this._nbcells = nbcells;
    this._container = null;
    this.rows = null;
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
    preRender: function (mainController) {
        initToolbar({
            mode: 'merge',
            save: function () {
                mainController.save();
            }
        });
    },
    postRender: function () {
        var dd = new DragDrop();
        dd.enable();
        this._addButtonListeners();
    },
    _generateRows: function () {
        var rows = [];
        this._nbcells.forEach(function (nbcell) {
            var mr;
            if (nbcell.side() === cellSide[0]) {
                mr = new MergeRow(rows.length);
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
    },
    _addButtonListeners: function() {
        var $buttons = $("input.merge-arrow-right");
        var rows = this.rows;
        var click_action_right = function(button, row) {
            if(!$(button).hasClass("undo-button-local"))
            {
                var moveRight = new MoveRightCommand(row);
                Invoker.storeAndExecute(moveRight);
                $(button).addClass("undo-button-local");
                $(button).val("<-");
            }
            else
            {
                Invoker.undo(row.rowID);
                $(button).removeClass("undo-button-local");
                $(button).val("->");
            }
        };
        $buttons.each(function(key, value)
        {
            var id = $(value).closest('.row').attr('id');
            var row = rows[id];
            $(value).click(function() {click_action_right(value, row); });
        });

        $buttons = $("input.merge-arrow-left");
        rows = this.rows;
        var click_action_left = function(button, row) {
            if(!$(button).hasClass("undo-button-remote"))
            {
                var moveLeft = new MoveLeftCommand(row);
                Invoker.storeAndExecute(moveLeft);
                $(button).addClass("undo-button-remote");
                $(button).val("->");
            }
            else
            {
                Invoker.undo(row.rowID);
                $(button).removeClass("undo-button-remote");
                $(button).val("<-");
            }

        };
        $buttons.each(function(key, value)
        {
            var id = $(value).closest('.row').attr('id');
            var row = rows[id];
            $(value).click(function() {click_action_left(value, row); });
        });
    },

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
        return this._container;
    },
    preRender: function (mainController) {
        initToolbar({
            mode: 'diff',
            save: function () {
                mainController.save();
            }
        });
    },
    postRender: function () {
    },
    _generateRows: function () {
        var self = this,
            rows = [];
        this._nbcells.forEach(function (nbcell) {
            if (nbcell.state() === 'modified') {
                if (nbcell.type() === 'heading') { 
                    rows.push(new HeaderDiff(nbcell));
                } else if (nbcell.type() === 'code') {
                    rows.push(new LineDiff(self._nb, nbcell));
                }
            } else {
                rows.push(new DiffRow(nbcell));
            }
        });
        return rows;
    }
};

/**
 * Class for the word Markdown.
 */
function HeaderDiff(nbcell) {
    this._nbcell = nbcell;
}

HeaderDiff.prototype = {
    render: function () {
        var diffData, htmlObject;
        diffData = this._nbcell.headerDiffData();
        htmlObject = $('<h2 class = "diffed-header"></h2>');
        diffData.forEach(function (word) {
            var span = $('<span></span>');
            span.addClass(word.state + '-word');
            span.append(' ' + word.value);
            htmlObject.append(span);
        });
        return htmlObject;
    }
};

/**
 * Class for rendering rows of the merge UI.
 */
function MergeRow(id) {
    this.rowID = id;
    this._cells = {};
}

MergeRow.prototype = {
    render: function () {
        var row;
        row = this._emptyRow(this.rowID);
        this._fillColumn(row, this._cells.local);
        this._fillColumn(row, this._cells.base);
        this._fillColumn(row, this._cells.remote);

        if (this._cells.local.state() !== 'unchanged' &&
                 this._cells.local.state() !== 'empty' ) {

        } else {
            row.find("input.merge-arrow-right").hide();
        }

        if (this._cells.remote.state() !== 'unchanged' &&
               this._cells.remote.state() !== 'empty' ) {
            row.find("input.merge-arrow-left").click(function(state) {
                return function() {

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
    _emptyRow: function (rowID) {
        var html;
        html = "<div id="+rowID+" class='row'>" + "<div class='row-cell-merge-local'></div>" + "<div class='row-cell-merge-controls-local'>" + this._generateMergeControlColumn("local") + "</div>" + "<div class='row-cell-merge-remote'></div>" + "<div class='row-cell-merge-controls-remote'>" + this._generateMergeControlColumn("remote") + "</div>" + "<div class='row-cell-merge-base'></div>" + "</div>";
        return $(html);
    },
    _generateMergeControlColumn: function(side) {
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
    },
    moveLeft: function () {
        console.log("move left");
        this._cells.base.cell.set_text(this._cells.remote.cell.get_text());
        this._cells.base.cell.element.removeClass();
        this._cells.base.cell.element.addClass(this._cells.remote.cell.element.attr("class"));
        var output = this._cells.remote.element().find("div.output_wrapper").clone(true);
        this._cells.base.cell.element.find('.output_wrapper').replaceWith(output);
        this._cells.base.set_state(this._cells.remote.state());
    },
    moveRight: function () {
        console.log("move right");
        this._cells.base.cell.set_text(this._cells.local.cell.get_text());
        this._cells.base.cell.element.removeClass();
        this._cells.base.cell.element.addClass(this._cells.local.cell.element.attr("class"));
        var output = this._cells.local.element().find("div.output_wrapper").clone(true);
        this._cells.base.cell.element.find('.output_wrapper').replaceWith(output);
        this._cells.base.set_state(this._cells.local.state());
    },
    undo: function(base, cell_class, output, old_state) {
        this._cells.base.cell.set_text(base);
        this._cells.base.cell.element.removeClass();
        this._cells.base.cell.element.addClass(cell_class);
        this._cells.base.cell.element.find('.output_wrapper').replaceWith(output);
        this._cells.base.set_state(old_state);
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
        var targetContainer;
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

function LineDiff(notebook, nbcell) {
    this._nb = notebook;
    this._nbcell = nbcell;
}

LineDiff.prototype = {
    render: function () {
        var self = this,
            diffs = this._getDiffData(),
            container = this._empty();
        diffs.forEach(function (item) {
            var line;
            if (item.state === 'deleted') {
                line = self._line(item.value, null);
            } else if (item.state === 'added') {
                line = self._line(null, item.value);
            } else if (item.state === 'unchanged') {
                line = self._line(item.value, item.value);
            }
            container.find('.line-diff').append(line);
        });
        return container;
    },
    _getDiffData: function () {
        return this._nbcell.lineDiffData();
    },
    _line: function (left, right) {
        var row;
        row = $('<div class="row-fluid line-diff-line"><div class="span6 line-diff-left"></div><div class="span6 line-diff-right"></div></div>');
        if (left) {
            row.find('.line-diff-left').append(left);
            if (!right) {
                row.find('.line-diff-left').addClass('line-diff-left-filled');
            }
        }
        if (right) {
            row.find('.line-diff-right').append(right);
            if (!left) {
                row.find('.line-diff-right').addClass('line-diff-right-filled');
            }
        }
        if (left && right) {
            row.find('.line-diff-right,.line-diff-left').addClass('line-diff-unchanged');
        }
        return row;
    },
    _empty: function () {
        return $('<div class="row">' + // 'row' as in UI rows, not lines.
            '<div class="line-diff"></div>' +
            '</div>');
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
    set_state: function (state) {
        this.cell.metadata.state = state;
    },
    type: function () {
        return this.cell.cell_type;
    },
    removeMetadata: function () {
        delete this.cell.metadata.state;
        delete this.cell.metadata.side;
    },
    element: function () {
        return this.cell.element;
    },
    lineDiffData: function () {
        return this.cell.metadata['extra-diff-data'];    
    },
    headerDiffData: function () {
        return this.cell.metadata['extra-diff-data'];
    }
};

//there's probably a better way to get the rows
function MergeRows() {
    this.rows = null;
}

function init() {
    var main = new NBDiff(IPython.notebook, true);
    main.init();
    MergeRows.rows = main.getMergeRows();
}

window.MergeRows = MergeRows;

return {
    NBDiff: NBDiff,
    Merge: Merge,
    Diff: Diff,
    DiffRow: DiffRow,
    MergeRow: MergeRow,
    NBDiffCell: NBDiffCell,
    LineDiff: LineDiff,
    MergeRows: MergeRows,
    init: init
};

}(jQuery));

