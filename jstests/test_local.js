module("local");

test("test_initToolbar_merge", function () {
    var info = { mode: "merge", save: function() {}};
    initToolbar(info);
    notEqual($('button#nbdiff-undo').css("display"), "none", 'undo button visible');
    notEqual($('button#nbdiff-save').css("display"), "none", 'save button visible');
    notEqual($('button#nbdiff-shutdown').css("display"), "none", 'shutdown button visible');
    equal($('button#nbdiff-previous').css("display"), "none", 'previous page button invisible');
    equal($('button#nbdiff-next').css("display"), "none", 'next page button invisible');
});

test("test_initToolbar_diff", function () {
    var info = { mode: "diff", save: function() {}};
    initToolbar(info);
    equal($('button#nbdiff-undo').css("display"), "none", 'undo button invisible');
    equal($('button#nbdiff-save').css("display"), "none", 'save button invisible');
    notEqual($('button#nbdiff-shutdown').css("display"), "none", 'shutdown button visible');
    equal($('button#nbdiff-previous').css("display"), "none", 'next page invisible');
    equal($('button#nbdiff-next').css("display"), "none", 'next page button invisible');
});
/*
test("test_loadNextPage", function () {
    var alerted = false;
    window.alert = function() {alerted = true;};
    loadNextPage();
    ok(alerted, "alert shown");
});

test("test_loadPreviousPage", function () {
    var alerted = false;
    window.alert = function() {alerted = true;};
    loadPreviousPage();
    ok(alerted, "alert shown");
});*/

test("test_getPageInfo", function () {
    var pageInfo = getPageInfo();
    equal(pageInfo.total, 1, "Single notebook");
    equal(pageInfo.current, 0, "First notebook");
});
