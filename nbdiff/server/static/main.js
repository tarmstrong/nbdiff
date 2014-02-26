if (typeof IPython.notebook === 'undefined') {
    $([IPython.events]).bind('notebook_loaded.Notebook', nbdiff_init);
} else {
    nbdiff_init();
}
