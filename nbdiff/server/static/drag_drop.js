
function DragDrop() {}

DragDrop.prototype = (function() {
    //private functions
    var drag_start = function(ev) {
            //TODO: create command containing drag source
            var sourceID = $(ev.target).closest(".row").attr("id");
            ev.dataTransfer.setData('data', sourceID);
            console.log("Drag " + sourceID);
        };
    var allow_drop = function(ev) {
            var sourceID = ev.dataTransfer.getData("data");
            var $target = $(ev.target);
            var targetIsBase = $target.closest("div.row").attr("id") == sourceID;
            if(targetIsBase)
            {
                //prevent default event and allow drag and drop
                console.log("allow_Drop");
                ev.preventDefault();
            }
        };
    var on_drop = function(ev) {
            ev.preventDefault();
            var sourceID = ev.dataTransfer.getData("data");
            //TODO: set command destination
            //TODO: execute command to set destination cell data to source data
            //this would help with undo/redo
            //the codemirror textbox is conflicting with the allow_drop/on_drop functions
            console.log("Drop");
     };
    var on_drag_enter = function(ev) {
            ev.preventDefault();
            return true;
    };
    var add_listeners = function()
        {
            var cells = $(".nbdiff-added, .nbdiff-deleted");
            cells.each( function ( index, cell )
            {
                cell.draggable = true;
                cell.addEventListener('dragstart', drag_start, false);
            });
            cells = $(".row-cell-merge-base > div");
            cells.each( function ( index, cell )
            {
                cell.addEventListener('dragover', allow_drop, false);
                cell.addEventListener('drop', on_drop, false);
                cell.addEventListener('dragenter', on_drag_enter, false);
            });

        };
    var remove_listeners = function()
        {
            var cells = $(".nbdiff-added, .nbdiff-deleted");
            cells.each( function ( index, cell )
            {
                cell.removeEventListener('dragstart', drag_start);
            });
            cells = $(".row-cell-merge-base > div");
            cells.each( function ( index, cell )
            {
                cell.removeEventListener('dragover', allow_drop);
                cell.removeEventListener('drop', on_drop);
                cell.removeEventListener('dragenter', on_drag_enter);
            });
        }
        //return prototype with public functions
        return {
            constructor: DragDrop,

            enable: add_listeners,
            disable: remove_listeners
        };
    }
)();