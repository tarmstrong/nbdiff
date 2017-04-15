function NotebookMerge(data)
{
	this.data = data;	
}

NotebookMerge.prototype.getBase = function() {
	var nb = this.filter("base");
	return new Notebook(nb);
};

NotebookMerge.prototype.getLocal = function() {
	var nb = this.filter("local");
	return new Notebook(nb);
};

NotebookMerge.prototype.getRemote = function() {
	var nb = this.filter("remote");
	return new Notebook(nb);
};

NotebookMerge.prototype.filter = function(side)
{
	var temp = JSON.parse(JSON.stringify(this.data));
	for(var i = temp.worksheets[0].cells.length - 1; i >=0 ; i--)
	{
	   if(temp.worksheets[0].cells[i].metadata.side !== side)
		   temp.worksheets[0].cells.splice(i, 1);
	}
	return temp;
};