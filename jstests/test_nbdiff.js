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
            'line-diff': [
            ]
        }
    };
    var nbcell = new NBDiff.NBDiffCell(cell);
    equal(nbcell.state(), 'added', '.state() returns "added"');
    equal(nbcell.side(), 'local', '.side() returns "local"');
    deepEqual(nbcell.lineDiffData(), [], 'lineDiffData() returns []');
});
