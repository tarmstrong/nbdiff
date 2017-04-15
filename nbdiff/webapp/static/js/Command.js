function Command() { }

Command.prototype.execute = function() { };

function MergeLeft()
{
	Command.call(this);
}

MergeLeft.prototype = Object.create(Command.prototype);

MergeLeft.prototype.execute = function() { 
	
};

function MergeRight()
{
	Command.call(this);
}

MergeRight.prototype = Object.create(Command.prototype);

MergeRight.prototype.execute = function() { 
	
};