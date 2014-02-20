

var Invoker = (function () {
    var _commands = [];
    var _undone_commands = [];
    var storeAndExecute = function(command){
        _commands.push(command);
        command.execute();
        console.log("Undo list items: "+_commands.length);
        console.log("Redo list items: "+_undone_commands.length);
    };
    var undo = function() {
        if(_commands.length > 0)
        {
            var command = _commands.pop();
            command.undo();
            _undone_commands.push(command);
            console.log("Undo list items: "+_commands.length);
            console.log("Redo list items: "+_undone_commands.length);
        }
        else
            throw "Nothing to undo."
    };
    var redo = function() {
        if(_undone_commands.length > 0)
        {
            storeAndExecute(_undone_commands.pop());
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