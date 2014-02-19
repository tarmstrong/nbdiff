function Command(source_nb, destination_nb)
{
    var source_notebook = source_nb;
    var destination_notebook = destination_nb;
    var source_side = ""; // local, remote
    var source = "source";
    var destination = "destination";
}

Command.prototype = (function() {
    //private functions

        //return prototype with public functions
        return {
            constructor: Command,

            execute: function() {

            },

            undo: function() {

            }
        };
    }
)();