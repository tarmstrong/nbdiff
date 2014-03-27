module( "command", {
    setup: function() {
        window.nb_container = $("div.container");
        var cell1Data = {'metadata':{'state':'modified','side':'local'},'input':'y = [1,2,3] # list!\ny = (1, 2) # tuple!\nz = {1, 2, 3, 4, 5, 1, 2, 3, 2, 3} # set!\n\nz','cell_type':'code','prompt_number':3,'outputs':[{'output_type':'pyout','prompt_number':3,'text':'set([1, 2, 3, 4, 5])'}],'language':'python','collapsed':false}; 
        var cell1 = JSON.parse(JSON.stringify(cell1Data));
        cell1.element = $(".row-cell-merge-local > div");
        cell1.toJSON = function() {
            return cell1;
        };   
        var cell2Data = {'metadata':{'state':'unchanged','side':'base'},'input':'x = [1,2,3] # list!\ny = (1, 2) # tuple!\nz = {1, 2, 3, 4, 5, 1, 2, 3, 2, 3} # set!\n\nz','cell_type':'code','prompt_number':3,'outputs':[{'output_type':'pyout','prompt_number':3,'text':'set([1, 2, 3, 4, 5])'}],'language':'python','collapsed':false};
        var cell2 = JSON.parse(JSON.stringify(cell2Data));
        cell2.element = $(".row-cell-merge-base > div");
        cell2.toJSON = function() {
            return cell2;
        };
        var cell3Data = {'metadata':{'state':'deleted','side':'remote'},'input':'x = [1,2,3] # list!\ny = (1, 2) # tuple!\nz = {1, 2, 3, 4, 5, 1, 2, 3, 2, 3} # set!\n\nz','cell_type':'code','prompt_number':3,'outputs':[{'output_type':'pyout','prompt_number':3,'text':'set([1, 2, 3, 4, 5])'}],'language':'python','collapsed':false};
        var cell3 = JSON.parse(JSON.stringify(cell3Data));
        cell3.element = $(".row-cell-merge-remote > div");
        cell3.toJSON = function() {
            return cell3;
        };
        var newCell = {};
        newCell.fromJSON = function(cell_json) {
            for(var k in cell_json) {
                this[k]=cell_json[k];
            }
            this.select = function() {};
        };
        IPython = {
          notebook: {
            metadata: {'nbdiff-type':'merge','name':'Untitled1'},
            get_cells: function () {
              return [cell1,
              cell2,
              cell3];
            },
            insert_cell_at_index: function (cell_type, index) {
               return newCell;
            }
          }
        };
    }, teardown: function() {
    
    }
});

test("test_invoker_empty", function() {
    throws(
        function() {
            Invoker.undo();
        },
        "Throws message for empty undo stack"
    );
    throws(
        function() {
            Invoker.undo(0);
        },
        "Throws message for empty undo stack"
    );
});

test("test_invoker", function() {
    var mr = new NBDiff.MergeRow(1);
    var cell1 = IPython.notebook.get_cells()[0];
    var cell2 = IPython.notebook.get_cells()[1];
    var cell3 = IPython.notebook.get_cells()[2];
    var local = new NBDiff.NBDiffCell(cell1);
    var base = new NBDiff.NBDiffCell(cell2);
    var remote = new NBDiff.NBDiffCell(cell3);
    mr.addLocal(local);
    mr.addBase(base);
    mr.addRemote(remote);
    var command = new MoveLeftCommand(mr);
    Invoker.storeAndExecute(command);
    deepEqual(mr._cells.base.cell.element[0], mr._cells.remote.cell.element[0], "Compare base cell to remote");
    Invoker.undo();
    deepEqual(mr._cells.base.cell.element[0], cell2.element[0], "Compare base cell to previous base");
    throws(
        function() {
            Invoker.undo();
        },
        "Throws message for empty undo stack"
    );
});
