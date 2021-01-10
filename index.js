var express = require('express');
var app = express();

app.use(express.static(__dirname))

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/semviewer.html')
})

// Warning: file size limit is 32MB in google cloud run, hence this wont work
app.use(express.json({limit: '70mb'}));
app.use(express.urlencoded({limit: '70mb'}));

app.listen(8080, function () {
  console.log('Nodejs is listening at port 8080.')
})