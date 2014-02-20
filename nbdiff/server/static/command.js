

var Invoker = (function () {
    var _undo_commands = [];
    var _redo_commands = [];
    var storeAndExecute = function(command){
        _undo_commands.push(command);
        command.execute();
        console.log("Undo list items: "+_undo_commands.length);
        console.log("Redo list items: "+_redo_commands.length);
    };
    var undo = function() {
        if(_undo_commands.length > 0)
        {
            var command = _undo_commands.pop();
            command.undo();
            _redo_commands.push(command);
            console.log("Undo list items: "+_undo_commands.length);
            console.log("Redo list items: "+_redo_commands.length);
        }
        else
            throw "Nothing to undo."
    };
    var redo = function() {
        if(_redo_commands.length > 0)
        {
            storeAndExecute(_redo_commands.pop());
        }
        else
            throw "Nothing to redo.";
    };
    return {
        storeAndExecute: storeAndExecute,
        undo: undo,
        redo: redo
    }
})();

function MoveLeftCommand(merge_row) {
    this.merge_row = merge_row;
    this.text = merge_row._cells.base.cell.get_text();
}

/* The Command for turning on the light - ConcreteCommand #1 */
MoveLeftCommand.prototype = {
    execute: function() {
        this.merge_row.moveLeft();
    },
    undo: function() {
        this.merge_row.undo(this.text);
    }
}

function MoveRightCommand(merge_row) {
    this.merge_row = merge_row;
    this.text = merge_row._cells.base.cell.get_text();
}

/* The Command for turning off the light - ConcreteCommand #2 */
MoveRightCommand.prototype = {
    execute: function() {
        this.merge_row.moveRight();
    },
    undo: function() {
        this.merge_row.undo(this.text);
    }
}