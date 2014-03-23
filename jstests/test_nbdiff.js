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

test("test_invoker_empty", function() {
	throws(
		function() {
			Invoker.undo();
		},
		"Throws message for empty undo stack"
	);
	throws(
		function() {
			Invoker.undo(0);
		},
		"Throws message for empty undo stack"
	);
});

test("test_nbmerge", function() {
	var _nbcells = [];
	IPython.notebook.get_cells().forEach(function (cell) {
       _nbcells.push(new NBDiff.NBDiffCell(cell));
   });
	var mergeController = new NBDiff.Merge(IPython.notebook, _nbcells);
	mergeController.render(nb_container);
	equal(true,true, 'Placeholder assertion');
});


