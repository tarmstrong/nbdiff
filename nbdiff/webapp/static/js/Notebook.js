function Notebook(data) {
	this.data = data;
}

Notebook.prototype.render = function(cellColumn) {
	for(var row in this.data.worksheets[0].cells)
	{
		this.addCellToGrid(row, cellColumn, this.data.worksheets[0].cells[row]);
	}
};

Notebook.prototype.addCellToGrid = function(cellRow, cellColumn, cellData) {
	if(cellData.cell_type == "heading" || cellData.cell_type == "markdown" || cellData.cell_type == "raw")
	{
		this.addTextCell(cellRow, cellColumn, cellData.source, "input "+cellData.metadata.state);
	}
	else if(cellData.cell_type == "code") {
		this.addTextCell(cellRow, cellColumn, cellData.input, "prettyprint input "+cellData.metadata.state);
		if(typeof cellData.outputs[0] != "undefined")
		{
			if(typeof cellData.outputs[0].png != "undefined" && cellData.outputs[0].png != "")
				$("#"+cellRow+" > td."+cellColumn).append("<div><pre class='output "+cellData.metadata.state+"'><img src='data:image/png;base64,"+cellData.outputs[0].png+"'/></pre></div>");
			if(typeof cellData.outputs[0].text != "undefined")
				this.addTextCell(cellRow, cellColumn, cellData.outputs[0].text, "output "+cellData.metadata.state);
		}
	}
};

Notebook.prototype.addTextCell = function(cellRow, cellColumn, text, css_class) {
	var temp = JSON.parse(JSON.stringify(text));
	var t = "";
	for(var i in text)
	{
		//temp[i] = temp[i].replace("\n", "<br/>");
		t = t.concat(temp[i]);
	}
	
	//$("#"+cellRow+" > td."+cellColumn).append("<div><textarea class='"+css_class+"' style='display: none;' mode='python'>"+t+"</textarea></div>");
	$("#"+cellRow+" > td."+cellColumn).append("<div><pre class='"+css_class+"' >"+t+"</pre></div>");
};

Notebook.prototype.getCellSize = function() {
	return this.data.worksheets[0].cells.length;
}

Notebook.prototype.getCell = function(index) {
	var cell = this.data.worksheets[0].cells[index];
	return cell;
};

Notebook.prototype.getCells = function() {
	return this.data.worksheets[0].cells;
};

Notebook.prototype.setCell = function(index, data) {
	this.data.worksheets[0].cells[index] = data;
}

Notebook.prototype.saveNotebook = function() {
	var blob = new Blob([JSON.stringify(this.data)], {type: "text/plain;charset=utf-8"});
	saveAs(blob, "hello world.ipynb");
};