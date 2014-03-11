

var Invoker = (function () {
    var _undo_command_stack = [];
    var _undo_commands = [];
    var storeAndExecute = function(command){
        if(typeof _undo_commands[command.id] !== "undefined")
        {
            _undo_commands[command.id].push(command);
        }
        else
        {
            _undo_commands[command.id] = [];
            _undo_commands[command.id].push(command);
        }
        _undo_command_stack.push(command);
        command.execute();
    };
    var undo = function(id) {
        var command = null;
        if(typeof id !== "undefined")
        {
            if(_undo_commands[id].length > 0) {
                command = _undo_commands[id].pop();
                var index = _undo_command_stack.indexOf(command);
                _undo_command_stack.splice(index, 1);
                command.undo();
            }
            else {
                throw "Nothing to undo.";
            }
        }
        else
        {
            if(_undo_command_stack.length > 0) {
                command = _undo_command_stack.pop();
                _undo_commands[command.id].pop();
                command.undo();
            }
            else {
                throw "Nothing to undo.";
            }
        }
    };
    return {
        storeAndExecute: storeAndExecute,
        undo: undo
    };
})();

/* Base command class */
function Command(merge_row) {
    this.merge_row = merge_row;
    this.old_classes = merge_row._cells.base.element().attr("class");
    this.old_state = merge_row._cells.base.state();
    this.id = merge_row.rowID;
    this.cell_JSON = merge_row._cells.base.cell.toJSON();
}

function MoveLeftCommand(merge_row) {
    Command.call(this, merge_row);
}

MoveLeftCommand.prototype = Object.create(Command.prototype);

/* The Command for Moving left - ConcreteCommand #1 */
MoveLeftCommand.prototype = {
    execute: function() {
        this.merge_row.moveLeft();
    },
    undo: function() {
        this.merge_row.toggleRightButton();
        this.merge_row.undo(this.cell_JSON, this.old_classes, this.old_state);
    }
};

function MoveRightCommand(merge_row) {
    Command.call(this, merge_row);
}

MoveRightCommand.prototype = Object.create(Command.prototype);

/* The Command for Moving right - ConcreteCommand #2 */
MoveRightCommand.prototype = {
    execute: function() {
        this.merge_row.moveRight();
    },
    undo: function() {
        this.merge_row.toggleLeftButton();
        this.merge_row.undo(this.cell_JSON, this.old_classes, this.old_state);
    }
};
