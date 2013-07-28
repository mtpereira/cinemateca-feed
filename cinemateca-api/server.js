var restify = require('restify');

var mongodb = require('mongodb');

var server = restify.createServer({name: 'cinemateca-api'});

server
	.use(restify.fullResponse())
	.use(restify.bodyParser());

/*server.get('/all', funtion(){

})*/

server.get('/movies/:year/:month/:day', function(req, res, next){
	var filename = req.params.year + '-' + req.params.month + '-' + req.params.day + '.json';
	var filepath = process.env.HOME + '/events/' + filename;

	new mongodb.Db('scrapy', new mongodb.Server('localhost', 27017, {auto_reconnect: true})).open(function(err, db){
		if(err){
			console.log(err);
		}

		db.collection('movies', function(error, collection){
			if(err){
				console.log(err);
			}

			var searchDate = req.params.year + '-' + req.params.month + '-' + req.params.day + 'T00:00:00.000Z';

			console.log(searchDate);

			collection.find({'date': { '$gt': searchDate}}).toArray(function(err, items){

				res.send(items);
			})
		})
	});

	//return returnLines;
	//synchronous, temporary
	/*
	if(!fs.existsSync(filepath)){
		return next(new restify.InternalError('file not found'));
	}

	fs.readFile(filepath, 'utf8', function(err, data) {
	    if(err) res.send(err);

	    var array = data.toString().split("\n");

	    for(i in array) {
	    	if(array[i]){
	       		var jsonObj = JSON.parse(array[i].toString());
	        	returnLines.push(jsonObj);
			}
	    }
	    res.send(
			returnLines
		);
	});
	*/
});

server.listen(8080, function(){
	console.log('%s listening at %s', server.name, server.url);
});
