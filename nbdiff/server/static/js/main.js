if (typeof IPython.notebook === 'undefined') {
    $([IPython.events]).bind('notebook_loaded.Notebook', function () {
        NBDiff.init();
    });
} else {
    NBDiff.init();
}
