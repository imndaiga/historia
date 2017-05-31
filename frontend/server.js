var express = require('express')
var app = express()
var path = require('path')
var port = process.env.EXPRESS_PORT || 8080

app.use(express.static('./dist'))

app.get('*', function(req, res) {
  res.sendFile(path.resolve(__dirname, 'dist/index.html'));
})

app.listen(port, function () {
    console.log('Server running on port ' + port);
})