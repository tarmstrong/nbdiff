//Various constants
var leftFileJSON;
var rightFileJSON;
var IPYNBAtt = ["metadata", "nbformat", "nbformat_minor", "worksheets"];
var cellType = ["header","code", "markdown", "raw"];
var headingCell = ["level", "metadata", "source"];
var rawCell = ["metadata", "source"];
var markdownCell = ["metadata", "source"];
var codeCell = ["collapsed", "input", "language", "metadata", "outputs", "prompt_number"];
var outputCell = ["metadata", "output_type", "png", "stream", "prompt_number", "text"];
var worksheetAtt =["cells", "metadata"];
var state = ["unaffected", "new", "deleted", "modified"];
var likePercentage = 0.2;

// Check for the various File API support.
if (window.File && window.FileReader && window.FileList && window.Blob) {
// Great success! All the File APIs are supported.
} else {
  alert('The File APIs are not fully supported in this browser.');
}

//handles the file contents uploaded

function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object

    var srcElementID = evt.srcElement.id;

  var makeOnload = function (reader) {
            return function() {
                var contents = reader.result;
                if (srcElementID == "file1")
                    leftFileJSON = JSON.parse(contents);
                else
                    rightFileJSON = JSON.parse(contents);

                var contentElement = srcElementID + "Content";
                document.getElementById(contentElement).innerHTML = contents;
                resizeContent();
            };
  };

    // Loop through the FileList and render.
    for ( var i = 0; i < files.length; i++) {
    var f = files[i];
        // Only process image files.
        if (f.name.match(/ipynb/g).length === 0) {
            continue;
        }

        var reader = new FileReader();
        reader.onload = makeOnload(reader);

        reader.readAsText(f);
    }
}

//resize the .html
function resizeContent() {
    document.getElementById('file1Content').style.height = "auto";
    document.getElementById('file2Content').style.height = "auto";
    document.getElementById('result').style.height = "auto";

    var heightf1 = document.getElementById('file1Content').clientHeight;
    var heightf2 = document.getElementById('result').clientHeight;
    var heightf3 = document.getElementById('file2Content').clientHeight;

    var size = heightf1;
    if (size < heightf2)
        size = heightf2;
    if (size < heightf3)
        size = heightf3;
    document.getElementById('file1Content').style.height = size + "px";
    document.getElementById('file2Content').style.height = size + "px";
    document.getElementById('result').style.height = size + "px";

}

//generated the middle diff results
function generateDiff() {
    if (document.getElementById('file1').value === "")
        alert("Please Specify the Left File.");
    else if (document.getElementById('file2').value === "")
        alert("Please Specify the Right File.");
    else {
        var results = {};
        results.state = state[0];

        for (var attribute in IPYNBAtt) {
            var att = IPYNBAtt[attribute];
            if (compareIPYNBAtt(att, leftFileJSON[att],
                    rightFileJSON[att])) {
                results[att] = leftFileJSON[att];
                if (att == IPYNBAtt[0]) {
                    results[att].state = state[0];
                } else if (att == IPYNBAtt[3]) {
                    //TODO: add state[0] and add diffIDs to worksheet
                }
            } else {
                if (att != IPYNBAtt[3] && att != IPYNBAtt[0]) {
                    results.state = state[3];
                    results[att + "Diff"] = rightFileJSON[att];
                } else if (att == IPYNBAtt[0]) {
                    results[att].state = state[3];
                    results[att + "Diff"] = rightFileJSON[att];
                } else if (att == IPYNBAtt[3]) {
                    var leftWorkSheet = leftFileJSON[att];
                    var rightWorkSheet = rightFileJSON[att];
                    var minWorkSheet = leftWorkSheet.length;
                    var maxWorkSheet = leftWorkSheet.length;
                    if (rightWorkSheet.length > maxWorkSheet)
                        maxWorkSheet = rightWorkSheet.length;
                    else if (rightWorkSheet.length < minWorkSheet)
                        minWorkSheet = rightWorkSheet.length;
                    results[att] = [];

                    for ( var i = 0; i < minWorkSheet; i++) {
                        results[att][i] = {};
                        results[att][i][worksheetAtt[1]] = {};
                        results[att][i][worksheetAtt[0]] = [];

                        if (compareMetaData(
                                leftWorkSheet[i][worksheetAtt[1]],
                                rightWorkSheet[i][worksheetAtt[1]])) {
                            results[att][i][worksheetAtt[1]] = leftWorkSheet[i][worksheetAtt[1]];
                            results[att][i][worksheetAtt[1]].state = state[0];
                        } else {
                            results[att][i][worksheetAtt[1]] = leftWorkSheet[i][worksheetAtt[1]];
                            results[att][i][worksheetAtt[1]].state = state[3];
                            results[att][i][worksheetAtt[1] + "Diff"] = rightWorkSheet[i][worksheetAtt[1]];
                        }
                        var tempCellList = [];
                        var leftCells = leftWorkSheet[i][worksheetAtt[0]];
                        var rightCells = rightWorkSheet[i][worksheetAtt[0]];
                        var diffID = 0;
                        var rightCellsIndex = 0;
                        var leftCellsIndex = leftCells.length - 1;
                        for ( var j = 0; j < leftCells.length; j++) {
                            if (rightCellsIndex == rightCells.length) {
                                insertDiff(leftCells[j], state[0],
                                        diffID, tempCellList);
                                diffID++;
                                rightCellsIndex++;
                            } else {
                                var cellMatch = false;
                                while (rightCellsIndex < rightCells.length) {
                                    if (compareCell(leftCells[j],
                                            rightCells[rightCellsIndex])) {
                                        insertDiff(leftCells[j],
                                                state[0], diffID,
                                                tempCellList);
                                        diffID++;
                                        rightCellsIndex++;
                                        cellMatch =true;
                                        break;
                                    } else if (likeCell(leftCells[j],
                                            rightCells[rightCellsIndex])) {
                                        insertDiff(leftCells[j],
                                                state[3], diffID,
                                                tempCellList);
                                        insertDiff(
                                                rightCells[rightCellsIndex],
                                                state[3], diffID,
                                                tempCellList);
                                        diffID++;
                                        rightCellsIndex++;
                                        cellMatch =true;
                                        break;
                                    } else {
                                        insertDiff(
                                                rightCells[rightCellsIndex],
                                                state[1], diffID,
                                                tempCellList);
                                        diffID++;
                                        rightCellsIndex++;
                                    }
                                }
                                if(!cellMatch){
                                    insertDiff(
                                            leftCells[j],
                                            state[2], diffID,
                                            tempCellList);
                                    diffID++;
                                }
                            }
                        }
                        while (rightCellsIndex < rightCells.length) {
                            insertDiff(rightCells[rightCellsIndex],
                                    state[1], diffID, tempCellList);
                            diffID++;
                            rightCellsIndex++;
                        }
                        results[att][i][worksheetAtt[0]] = tempCellList;
                    }
                    for ( var k = minWorkSheet; k < maxWorkSheet; k++) {
                        if (leftWorkSheet.length == minWorkSheet) {
                            var temp = rightWorkSheet[k];
                            temp.state = state[1];
                            results[att].push(temp);
                        } else {
                            var temp2 = leftWorkSheet[k];
                            temp2.state = state[2];
                            results[att].push(temp2);
                        }
                    }
                }

            }
        }
        document.getElementById("result").innerHTML = JSON.stringify(
                results, null, 1);
        resizeContent();
    }
}

//compares the ipynb attributes.
function compareIPYNBAtt(att, left, right) {
    if (att != IPYNBAtt[3] && att != IPYNBAtt[0]) {
        return left == right;
    } else if (att == IPYNBAtt[3]) {
        if (left.length != right.length)
            return false;
        for ( var i = 0; i < left.length; i++) {
            if (!compareWorkSheet(left[i], right[i]))
                return false;
        }
        alert("matches");
        return true;
    } else {
        return compareIPYNBMetadata(left, right);
    }
}

//compares ipynb metadata
function compareIPYNBMetadata(left, right) {
    return left.name == right.name;
}

//compares worksheets
function compareWorkSheet(left, right) {
    if (!compareMetaData(left[worksheetAtt[1]], right[worksheetAtt[1]])) {
        return false;
    } else {
        var leftCells = left[worksheetAtt[0]];
        var rightCells = right[worksheetAtt[0]];
        if (leftCells.length != rightCells.length) {
            return false;
        } else {
            for ( var i = 0; i < leftCells.length; i++) {
                var match = compareCell(leftCells[i], rightCells[i]);
                if (!match) {
                    return false;
                }
            }
            return true;
        }
    }
}

//compares general metadata fields
function compareMetaData(left, right) {
    if (left.length != right.length)
        return false;
    try {
        for (var data in left) {
            if (left[data] != right[data])
                return false;
        }
        return true;
    } catch (err) {
        return false;
    }

}

//compares two cells
function compareCell(left, right) {
    if (left.cell_type != right.cell_type) {
        return false;
    } else {
        cellAttributes = getCellAtt(left);
        for (var attribute in cellAttributes) {
            att = cellAttributes[attribute];
            if (att != codeCell[4] && att != codeCell[3]) {
                if (left[att] != right[att])
                    return false;
            } else if (att == codeCell[3]) {
                if (!compareMetaData(left[att], right[att]))
                    return false;
            } else {
                return compareOutputArray(left[att], right[att]);
            }
        }
        return true;
    }
}
//determine the cell attributes by type
function getCellAtt(cell) {
    if (cell.cell_type == cellType[0])
        return headerCell;
    else if (cell.cell_type == cellType[1])
        return codeCell;
    else if (cell.cell_type == cellType[2])
        return markdownCell;
    else if (cell.cell_type == cellType[3])
        return rawCell;
    else
        return [];
}

//compare output array
function compareOutputArray(left, right) {
    if (left.length != right.length) {
        return false;
    } else {
        for (var output in left) {
            if (!compareOutputs(left[output], right[output]))
                return false;
        }
        return true;
    }
}

//compare a single ouput
function compareOutputs(left, right) {
    if (left.length != right.length) {
        return false;
    } else {
        try {
            for (var att in left) {
                if (att == "metadata") {
                    if (!compareMetaData(left[att], right[att]))
                        return false;
                } else if (left[att] != right[att])
                    return false;
            }
            return true;
        } catch (err) {
            return false;
        }
    }
}

//fuzzy like compare for two cells. 
//Fuzzy in the sense that a like input uses a percentage range to determine match.
function likeCell(left, right) {
    if (left.cell_type != right.cell_type) {
        return false;
    } else {
        cellAttributes = getCellAtt(left);
        for (var attribute in cellAttributes) {
            att = cellAttributes[attribute];
            //we ignore the output cell because if the input changed the output will obviously change.
            if (att != codeCell[4] && att != codeCell[3] &&
                    att != codeCell[1]) {
                if (left[att] != right[att])
                    return false;
            } else if (att == codeCell[3]) {
                if (!compareMetaData(left[att], right[att]))
                    return false;
            } else if (att == codeCell[1]) {
                return likeInput(left[att], right[att]);
            }
        }
        return true;
    }
}

//matches input field of cell.
//fussy in likePercentage determins if the cells match. 
function likeInput(left, right) {
    var phrases = left.split(/\n/);
    var matches = 0;
    for (var line in phrases) {
        if (right.indexOf(phrases[line]) != -1)
            matches++;
    }
    if (matches / phrases.length > likePercentage){
        return true;
    }else {
        return false;
    }
}
//insert cell with diff data. 
function insertDiff(cell, state, id, list) {
    var tempCell = cell;
    tempCell.state = state;
    tempCell.diffID = id;
    list.push(tempCell);
}
