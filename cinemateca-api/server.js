var restify = require('restify');
var mongodb = require('mongodb');
var moment = require('moment');

var server = restify.createServer({name: 'cinemateca-api'});

server
	.use(restify.fullResponse())
	.use(restify.bodyParser());

server.get('/movies/:year/:month/:day', function(req, res, next){
	var filename = req.params.year + '-' + req.params.month + '-' + req.params.day + '.json';
	var filepath = process.env.HOME + '/events/' + filename;

	new mongodb.Db('scrapy', new mongodb.Server('localhost', 27017, {auto_reconnect: true}), {'safe':false}).open(function(err, db){
		if(err){
			console.log(err);
		}

		db.collection('movies', function(error, collection){
			if(err){
				console.log(err);
			}

			var initDate = moment.utc(req.params.year + '-' + req.params.month + '-' + req.params.day);
				
			var endDate = moment(initDate).add('days', 1);

			collection.find(
				{'date': { $lte: endDate.toDate(), $gte: initDate.toDate()}}
				,{} 
				//,{explain:1}
			).toArray(function(err, items){
				res.header('Content-Type', 'application/json; charset=utf-8')

				console.log(items);

				res.send(items);
			})
		})
	});
});

server.listen(8080, function(){
	console.log('%s listening at %s', server.name, server.url);
});
