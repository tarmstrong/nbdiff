module( "merge", {
    setup: function() {
        window.nb_container = $("div.container");
        var cell1Data = {'metadata':{'state':'modified','side':'local'},'input':'y = [1,2,3] # list!\ny = (1, 2) # tuple!\nz = {1, 2, 3, 4, 5, 1, 2, 3, 2, 3} # set!\n\nz','cell_type':'code','prompt_number':3,'outputs':[{'output_type':'pyout','prompt_number':3,'text':'set([1, 2, 3, 4, 5])'}],'language':'python','collapsed':false}; 
        var cell1 = JSON.parse(JSON.stringify(cell1Data));
        cell1.element = $(".row-cell-merge-local > div");
        cell1.toJSON = function() {
            return cell1;
        };   
        var cell2Data = {'metadata':{'state':'unchanged','side':'base'},'input':'x = [1,2,3] # list!\ny = (1, 2) # tuple!\nz = {1, 2, 3, 4, 5, 1, 2, 3, 2, 3} # set!\n\nz','cell_type':'code','prompt_number':3,'outputs':[{'output_type':'pyout','prompt_number':3,'text':'set([1, 2, 3, 4, 5])'}],'language':'python','collapsed':false};
        var cell2 = JSON.parse(JSON.stringify(cell2Data));
        cell2.element = $(".row-cell-merge-base > div");
        cell2.toJSON = function() {
            return cell2;
        };
        var cell3Data = {'metadata':{'state':'deleted','side':'remote'},'input':'x = [1,2,3] # list!\ny = (1, 2) # tuple!\nz = {1, 2, 3, 4, 5, 1, 2, 3, 2, 3} # set!\n\nz','cell_type':'code','prompt_number':3,'outputs':[{'output_type':'pyout','prompt_number':3,'text':'set([1, 2, 3, 4, 5])'}],'language':'python','collapsed':false};
        var cell3 = JSON.parse(JSON.stringify(cell3Data));
        cell3.element = $(".row-cell-merge-remote > div");
        cell3.toJSON = function() {
            return cell3;
        };
        var newCell = {};
        newCell.fromJSON = function(cell_json) {
            for(var k in cell_json) {
                this[k]=cell_json[k];
            }
            this.select = function() {};
        };
        IPython = {
          notebook: {
            metadata: {'nbdiff-type':'merge','name':'Untitled1'},
            get_cells: function () {
              return [cell1,
              cell2,
              cell3];
            },
            insert_cell_at_index: function (cell_type, index) {
               return newCell;
            }
          }
        };
    }, teardown: function() {
    
    }
});

test("test_nbdiff_construct", function () {
    var nbdiff = new NBDiff.NBDiff(IPython.notebook, false);
    nbdiff.log('hi');
    equal(true, true, 'Placeholder assertion');
});

test("test_nbcell", function () {
    var cell = {
        metadata: {
            side: 'local',
            state: 'added',
            'extra-diff-data': [
            ]
        }
    };
    var nbcell = new NBDiff.NBDiffCell(cell);
    equal(nbcell.state(), 'added', '.state() returns "added"');
    equal(nbcell.side(), 'local', '.side() returns "local"');
    deepEqual(nbcell.lineDiffData(), [], 'lineDiffData() returns []');
});

test("test_merge", function() {
	var _nbcells = [];
	IPython.notebook.get_cells().forEach(function (cell) {
       _nbcells.push(new NBDiff.NBDiffCell(cell));
   });
	var mergeController = new NBDiff.Merge(IPython.notebook, _nbcells);
	ok(mergeController._nb);
	ok(mergeController._nbcells);
	mergeController.render(nb_container);
	ok(mergeController._container);
	equal(nb_container.children().children().length, 5, "three notebook cells and two buttons");
	equal(mergeController.rows.length,1, 'One merge row was created');
	deepEqual(IPython.notebook.get_cells()[0].element[0], nb_container.find(".row-cell-merge-local > div")[0], "Check local cell.");
	deepEqual(IPython.notebook.get_cells()[1].element[0], nb_container.find(".row-cell-merge-base > div")[0], "Check base cell.");
	deepEqual(IPython.notebook.get_cells()[2].element[0], nb_container.find(".row-cell-merge-remote > div")[0], "Check remote cell.");
});

test("test_MergeRow", function() {
	var mr = new NBDiff.MergeRow(1);
	equal(mr.rowID, 1, "Check row id");
	ok(mr._cells);
	var cell1 = IPython.notebook.get_cells()[0];
	var cell2 = IPython.notebook.get_cells()[1];
	var cell3 = IPython.notebook.get_cells()[2];
	var local = new NBDiff.NBDiffCell(cell1);
	var base = new NBDiff.NBDiffCell(cell2);
	var remote = new NBDiff.NBDiffCell(cell3);
	mr.addLocal(local);
	mr.addBase(base);
	mr.addRemote(remote);
	deepEqual(cell1, mr._cells.local.cell, "local equal");
	deepEqual(cell2, mr._cells.base.cell, "base equal");
	deepEqual(cell3, mr._cells.remote.cell, "remote equal");
});

test("test_MergeRow_moveLeft", function() {
	var mr = new NBDiff.MergeRow(1);
	var local = new NBDiff.NBDiffCell(IPython.notebook.get_cells()[0]);
	var base = new NBDiff.NBDiffCell(IPython.notebook.get_cells()[1]);
	var remote = new NBDiff.NBDiffCell(IPython.notebook.get_cells()[2]);
	mr.addLocal(local);
	mr.addBase(base);
	mr.addRemote(remote);
	mr.moveLeft();
	deepEqual(mr._cells.base.cell.element[0], mr._cells.remote.cell.element[0], "Compare base cell to remote");
});

test("test_MergeRow_moveRight", function() {
    var mr = new NBDiff.MergeRow(1);
    var local = new NBDiff.NBDiffCell(IPython.notebook.get_cells()[0]);
    var base = new NBDiff.NBDiffCell(IPython.notebook.get_cells()[1]);
    var remote = new NBDiff.NBDiffCell(IPython.notebook.get_cells()[2]);
    mr.addLocal(local);
    mr.addBase(base);
    mr.addRemote(remote);
    mr.moveRight();
    deepEqual(mr._cells.base.cell.element[0], mr._cells.local.cell.element[0], "Compare base cell to local");
});

test("test_MergeRow_getRightButton", function() {
    var mr = new NBDiff.MergeRow(1);
    var actual = mr.getLeftButton()[0];
    equal(actual, $(".row-cell-merge-controls-local > input")[0], "test if getting correct button");
});

test("test_MergeRow_getRightButton", function() {
    var mr = new NBDiff.MergeRow(1);
    var actual = mr.getRightButton()[0];
    equal(actual, $(".row-cell-merge-controls-remote > input")[0], "test if getting correct button");
});

test("test_MergeRow_toggleLeftButton", function() {
    var mr = new NBDiff.MergeRow(1);
    mr.toggleLeftButton();
    equal(mr.getLeftButton().val(), "<-", "check if arrow changed direction");
    ok(mr.getLeftButton().hasClass("undo-button-local"), "check if left button has class");
    mr.toggleLeftButton();
    equal(mr.getLeftButton().val(), "->", "check if arrow changed direction again");
    ok(!mr.getLeftButton().hasClass("undo-button-local"), "check if left button does not have class");
});

test("test_MergeRow_toggleRightButton", function() {
    var mr = new NBDiff.MergeRow(1);
    equal(mr.getRightButton().val(), "<-", "check if arrow points left");
    mr.toggleRightButton();
    equal(mr.getRightButton().val(), "->", "check if arrow changed direction");
    ok(mr.getRightButton().hasClass("undo-button-remote"), "check if right button has class");
    mr.toggleRightButton();
    equal(mr.getRightButton().val(), "<-", "check if arrow changed direction again");
    ok(!mr.getRightButton().hasClass("undo-button-remote"), "check if right button does not have class");
});

test("test_MergeRow_allowsMoveLeft", function() {
    var mr = new NBDiff.MergeRow(1);
    equal(mr.allowsMoveLeft(), true, "check if allows to move right cell to the left");
    mr.toggleRightButton();
    equal(mr.allowsMoveLeft(), false, "check if row does not allow to move right cell to the left after toggle");
});

test("test_MergeRow_allowsMoveRight", function() {
    var mr = new NBDiff.MergeRow(1);
    equal(mr.allowsMoveRight(), true, "check if allows to move left cell to the right");
    mr.toggleLeftButton();
    equal(mr.allowsMoveRight(), false, "check if row does not allow to move right cell left after toggle");
});

test("test_NBDiff_getMergeRows", function() {
    var main = new NBDiff.NBDiff(IPython.notebook, true);
    main.init();
    main.getMergeRows();
    equal(MergeRows.length, 1, "Check if there is one MergeRow");
});

module( "diff", {
    setup: function() {
        window.nb_container = $("div.container");
        var cell1Data = {'metadata':{'state':'added','side':'local'},'input':'y = [1,2,3] # list!\ny = (1, 2) # tuple!\nz = {1, 2, 3, 4, 5, 1, 2, 3, 2, 3} # set!\n\nz','cell_type':'code','prompt_number':3,'outputs':[{'output_type':'pyout','prompt_number':3,'text':'set([1, 2, 3, 4, 5])'}],'language':'python','collapsed':false}; 
        var cell1 = JSON.parse(JSON.stringify(cell1Data));
        cell1.element = $(".row-cell-merge-local > div");
        var cell2Data = {'metadata':{'state':'deleted','side':'base'},'input':'x = [1,2,3] # list!\ny = (1, 2) # tuple!\nz = {1, 2, 3, 4, 5, 1, 2, 3, 2, 3} # set!\n\nz','cell_type':'code','prompt_number':3,'outputs':[{'output_type':'pyout','prompt_number':3,'text':'set([1, 2, 3, 4, 5])'}],'language':'python','collapsed':false};
        var cell2 = JSON.parse(JSON.stringify(cell2Data));
        cell2.element = $(".row-cell-merge-remote > div");
        IPython = {
          notebook: {
            metadata: {'nbdiff-type':'diff','name':'Untitled1'},
            get_cells: function () {
              return [cell1,
              cell2];
            }
          }
        };
    }, teardown: function() {}
});

test("test_diff_linebased_basic", function () {
    var cell = {
        lineDiffData: function () {
            return [
                {state: 'added', value: 'a'},
                {state: 'deleted', value: 'b'},
                {state: 'unchanged', value: 'c'}
            ];
        }
    };
    var nb = {};
    var linediff = new NBDiff.LineDiff(nb, cell);
    var result = linediff.render();
    equal(result.find('.line-diff-line').length, 3, 'Three rows of output were created.');
});

// LineDiff shouldn't choke on an empty diff.
test("test_diff_linebased_empty", function () {
    var cell = {
        lineDiffData: function () {
            return [
            ];
        }
    };
    var nb = {};
    var linediff = new NBDiff.LineDiff(nb, cell);
    var result = linediff.render();
    equal(result.find('.line-diff-line').length, 0, 'Empty line-based diff was created.');
});

test("test_Diff", function() {
    var _nbcells = [];
    IPython.notebook.get_cells().forEach(function (cell) {
       _nbcells.push(new NBDiff.NBDiffCell(cell));
    });
    var diffController = new NBDiff.Diff(IPython.notebook, _nbcells);
    ok(diffController._nb);
    ok(diffController._nbcells);
    diffController.render(nb_container);
    ok(diffController._container);
    equal(nb_container.children().length, 2, "Two diff rows");
    equal($(nb_container.children()[0]).find(".row-cell-diff-right").children().length, 1, "First cell is on the right side");
    equal($(nb_container.children()[1]).find(".row-cell-diff-left").children().length, 1, "Second cell is on the left side");
    var cell1 = IPython.notebook.get_cells()[0];
    var cell2 = IPython.notebook.get_cells()[1];
    deepEqual(cell1.element[0], $(nb_container.children()[0]).find(".row-cell-diff-right > div")[0], "First cell HTML equal");
    deepEqual(cell2.element[0], $(nb_container.children()[1]).find(".row-cell-diff-left > div")[0], "Second cell HTML equal");
    deepEqual(cell1, diffController._nbcells[0].cell, "First cell Object equal");
    deepEqual(cell2, diffController._nbcells[1].cell, "Second cell Object equal");
});

test("test_DiffRow", function () {
    var cell1 = new NBDiff.NBDiffCell(IPython.notebook.get_cells()[0]);
    var nbrow = new NBDiff.DiffRow(cell1);
    var rendered_cell = nbrow.render();
    deepEqual(nbrow._nbcell, cell1, "equal cell");
});
