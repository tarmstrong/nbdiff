module("remote");

test("test_initToolbar_merge", function () {
    var info = { mode: "merge", save: function() {}};
    initToolbar(info);
    notEqual($('button#nbdiff-undo').css("display"), "none", 'undo button visible');
    notEqual($('button#nbdiff-save').css("display"), "none", 'save button visible');
});

test("test_initToolbar_diff", function () {
    var info = { mode: "diff", save: function() {}};
    initToolbar(info);
    equal($('button#nbdiff-undo').css("display"), "none", 'undo button invisible');
    equal($('button#nbdiff-save').css("display"), "none", 'save button invisible');
});