/* The Invoker function */
var Invoker = function(){
    var _commands = [];
    this.storeAndExecute = function(command){
        _commands.push(command);
        command.execute();
    }
}

function MoveLeftCommand(merge_row) {
    this.merge_row = merge_row;
}

/* The Command for turning on the light - ConcreteCommand #1 */
MoveLeftCommand.prototype = {
    execute: function() {
        this.merge_row.moveLeft();
    },
    undo: function() {

    }
}

function MoveRightCommand(merge_row) {
    this.merge_row = merge_row;
}

/* The Command for turning off the light - ConcreteCommand #2 */
MoveRightCommand.prototype = {
    execute: function() {
        this.merge_row.moveRight();
    },
    undo: function() {

    }
}