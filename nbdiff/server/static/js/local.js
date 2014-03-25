function initToolbar(info) {
    var mode = info.mode;
    var save = info.save;
    var pageInfo = getPageInfo();
    
    if (mode === 'diff') {
        $('button#nbdiff-shutdown').show();
    } else if (mode === 'merge') {
        $('button#nbdiff-save').show();
        $('button#nbdiff-undo').show();
        $('button#nbdiff-redo').show();

        $('#nbdiff-save').click(function (event) {
            event.preventDefault();
            save();
        });
        $('#nbdiff-undo').click(function () {
            Invoker.undo();
        });
        $('#nbdiff-redo').click(function () {
            Invoker.redo();
        });
    }
    
    if (pageInfo.current !== 0) {
        $('button#nbdiff-previous').show();
    }
    
    if (pageInfo.current !== pageInfo.total-1) {
        $('button#nbdiff-next').show();
    }
    
    $('button#nbdiff-shutdown').show();
    
    $('#nbdiff-previous').click(function () {
        loadPreviousPage();
    });
    $('#nbdiff-next').click(function () {
        loadNextPage();
    });
    $('#nbdiff-shutdown').click(function () {
        shutdownServer();
    });
}

function loadNextPage() {
    var pageInfo = getPageInfo();
    if (pageInfo.current < pageInfo.total-1) {
        var next = pageInfo.current + 1;
        location.href = 'http://127.0.0.1:5000/' + next;        
    }
    else {
        alert("There is no notebook after this one!");
    }
}

function loadPreviousPage() {
    var pageInfo = getPageInfo();
    if (pageInfo.current > 0) {
        var prev_id = pageInfo.current - 1;
        location.href = '/' + prev_id;
    }
    else {
        alert("There is no notebook before this one!");
    }
}

function shutdownServer() {
    location.href = '/shutdown';
}

$([IPython.events]).on('notebook_saved.Notebook', 
    function () { 
        alert("The notebook has been saved");
 });

// If we are merging/diffing multiple notebooks, these are shown
// on separate pages. This information is passed to the Javascript
// through HTML attributes:
// * The current notebook index is attached to the notebook id, e.g.,
//      <body data-notebook-id='notebook1'>
// * The total number of notebooks (i.e., the number of pages to show to
//   the user) is in an attribute of a hidden div with id
//   `num-notebooks`.
function getPageInfo() {
    var num_nbks = parseInt(document.getElementById('num-notebooks').getAttribute('data-num-notebooks'), 10);
    var current_id = parseInt(document.getElementById('current-notebook').getAttribute('data-current-notebook'), 10);
    return {
        total: num_nbks,
        current: current_id
    };
}
