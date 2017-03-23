
var express = require('express')
var path = require('path')
var app = express()

// Define port
app.set('port', 8080);

app.use(express.static(path.join(__dirname, '/public')))
app.use('/scripts', express.static(path.join(__dirname, '/node_modules')))

// Listen for requests
var server = app.listen(app.get('port'), function() {
	var port = server.address().port
	console.log('Serving on port: ' + port)
})