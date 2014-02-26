test("test_nbdiff_construct", function () {
    var nbdiff = new NBDiff.NBDiff(IPython.notebook, false);
    nbdiff.log('hi');
    equal(true, true);
});
