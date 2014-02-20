

var Invoker = (function () {
    var _commands = [];
    var storeAndExecute = function(command){
        _commands.push(command);
        command.execute();
    };
    var undo = function() {
        var command = _commands.pop();
        command.undo();
    };
    return {
        storeAndExecute: storeAndExecute,
        undo: undo
    }
})();

function MoveLeftCommand(merge_row) {
    this.merge_row = merge_row;
    this.base = merge_row._cells.base.cell.get_text();
}

/* The Command for turning on the light - ConcreteCommand #1 */
MoveLeftCommand.prototype = {
    execute: function() {
        this.merge_row.moveLeft();
    },
    undo: function() {
        this.merge_row.undo(this.base);
    }
}

function MoveRightCommand(merge_row) {
    this.merge_row = merge_row;
    this.base = merge_row._cells.base.cell.get_text();
}

/* The Command for turning off the light - ConcreteCommand #2 */
MoveRightCommand.prototype = {
    execute: function() {
        this.merge_row.moveRight();
    },
    undo: function() {
        this.merge_row.undo(this.base);
    }
}