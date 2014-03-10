

var Invoker = (function () {
    var _undo_commands = [];
    var storeAndExecute = function(command){
	for(var i = 0;i < _undo_commands.length; i++)
	{
		if(command.id === _undo_commands[i].id)
		{
			_undo_commands.splice(i, 1);
		}
	}
		_undo_commands.push(command);
		command.execute();
	};
	var undo = function(id) {
			if(_undo_commands.length > 0) {
				for(var i = 0;i < _undo_commands.length; i++)
            {
                if(_undo_commands[i].id === id)
                {
                    var command = _undo_commands[i];
                    _undo_commands.splice(i, 1);
                    command.undo();
                }
            }
        }
        else {
            throw "Nothing to undo.";
        }
    };
    return {
        storeAndExecute: storeAndExecute,
        undo: undo
    };
})();

function MoveLeftCommand(merge_row) {
    this.merge_row = merge_row;
    this.old_classes = merge_row._cells.base.element().attr("class");
    this.old_state = merge_row._cells.base.state();
    this.id = merge_row.rowID;
    this.cell_JSON = merge_row._cells.base.cell.toJSON();
}

/* The Command for turning on the light - ConcreteCommand #1 */
MoveLeftCommand.prototype = {
    execute: function() {
        this.merge_row.moveLeft();
    },
    undo: function() {
        this.merge_row.undo(this.cell_JSON, this.old_classes, this.old_state);
    }
};

function MoveRightCommand(merge_row) {
    this.merge_row = merge_row;
    this.old_classes = merge_row._cells.base.element().attr("class");
    this.old_state = merge_row._cells.base.state();
    this.id = merge_row.rowID;
    this.cell_JSON = merge_row._cells.base.cell.toJSON();
}

/* The Command for turning off the light - ConcreteCommand #2 */
MoveRightCommand.prototype = {
    execute: function() {
        this.merge_row.moveRight();
    },
    undo: function() {
        this.merge_row.undo(this.cell_JSON, this.old_classes, this.old_state);
    }
};
