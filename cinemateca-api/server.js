var restify = require('restify');
var lazy = require('lazy');
var fs = require('fs');

var server = restify.createServer({name: 'cinemateca-api'});

server
	.use(restify.fullResponse())
	.use(restify.bodyParser())

server.get('/test/:year/:month/:day', function(req, res, next){
	var filename = req.params.year + '_' + req.params.month + '_' + req.params.day + '.json';
	
	console.log(filename);

	var returnLines = [];

	//synchronous, temporary
	
	if(!fs.existsSync('./'+filename)){
		return next(new restify.InternalError('file not found'));
	}

	fs.readFile('./'+filename, function(err, data) {
		console.log('reading file');
	    
	    if(err) res.send(err);

	    var array = data.toString().split("\n");
	    for(i in array) {
	        console.log(array[i]);
	       	var jsonObj = JSON.parse(array[i].toString());
	        console.log(jsonObj);
	        returnLines.push(jsonObj);
	    }
	    res.send(
			returnLines
		);
	});
})

server.listen(3000, function(){
	console.log('%s listening at %s', server.name, server.url);
})
