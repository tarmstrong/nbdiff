
function DragDrop() {}

DragDrop.prototype = (function() {
    //private functions
    var that = function() {
				return this;
        };
    var drag_start = function(ev) {
            var rowID = $(ev.target).closest(".row").attr("id");

            var isLeft = $(ev.target).closest(".row-cell-merge-local").length > 0;

            var data = { id: rowID, isLeft: isLeft};
            ev.dataTransfer.setData('data', JSON.stringify(data));
        };
    var allow_drop = function(ev) {
            var raw_data = ev.dataTransfer.getData("data");
            var data = "";
            if(raw_data === "") {
                data = {id: $(ev.srcElement).closest(".row").attr("id") };
            } else {
                data = JSON.parse(raw_data);
            }
            var $target = $(ev.target);
            var sameRow = $target.closest("div.row").attr("id") === data.id;
            if(sameRow) {
                //prevent default event and allow drag and drop
                console.log("allow_Drop");
                ev.preventDefault();
            }
        };
    var on_drop = function(ev) {
            ev.preventDefault();
            var data = JSON.parse(ev.dataTransfer.getData("data"));

            var $target = $(ev.target).closest("div.row");
            var sameRow = $target.attr("id") === data.id;
				var $button = null;
            if(sameRow) {
                var command = null;

                if(data.isLeft) {
						command = new MoveRightCommand(MergeRows.rows[data.id]);
						$button = $(ev.target).closest(".row").find('.row-cell-merge-controls-local > input');
						$button.val("<-");
                  $button.addClass("undo-button-local");
                } else {
                    command = new MoveLeftCommand(MergeRows.rows[data.id]);
							$button = $(ev.target).closest(".row").find('.row-cell-merge-controls-remote > input');
							$button.val("->");
                    $button.addClass("undo-button-remote");
                }
                Invoker.storeAndExecute(command);
                //the codemirror textbox is conflicting with the allow_drop/on_drop functions
            }
     };
    var on_drag_enter = function(ev) {
            ev.preventDefault();
            return true;
    };
    var add_listeners = function() {
            var cells = $(".nbdiff-added, .nbdiff-deleted");
            cells.each( function ( index, cell )
            {
                cell.draggable = true;
                cell.addEventListener('dragstart', drag_start, false);
            });
            cells = $(".row-cell-merge-base > div");
            cells.each( function ( index, cell ) {
                cell.addEventListener('dragover', allow_drop, false);
                cell.addEventListener('drop', on_drop, false);
                cell.addEventListener('dragenter', on_drag_enter, false);
            });

        };
    var remove_listeners = function() {
            var cells = $(".nbdiff-added, .nbdiff-deleted");
            cells.each( function ( index, cell ) {
                cell.draggable = false;
                cell.removeEventListener('dragstart', drag_start);
            });
            cells = $(".row-cell-merge-base > div");
            cells.each( function ( index, cell ) {
                cell.removeEventListener('dragover', allow_drop);
                cell.removeEventListener('drop', on_drop);
                cell.removeEventListener('dragenter', on_drag_enter);
            });
        };

        //return prototype with public functions
        return {
            constructor: DragDrop,

            enable: add_listeners,
            disable: remove_listeners
        };
    }
)();
