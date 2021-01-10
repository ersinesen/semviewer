var express = require('express');
var app = express();

app.use(express.static(__dirname))

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/semviewer.html')
})




app.listen(8080, function () {
  console.log('Nodejs is listening at port 8080.')
})