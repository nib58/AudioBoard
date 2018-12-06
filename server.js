//Start local express server and listen on port 3000

var net = require('net');
var fs = require('fs');
var i = 0;
var filename = 'data'
var writeable = fs.createWriteStream(filename+'.txt');
var querystring = require('querystring');
var http = require('http');
var fs = require('fs');

var server = net.createServer(function(socket) {
  socket.on('data', function(data) {
	writeable.write(data)});
  socket.on('newFile', function(data){
	writeable = fs.createWriteStream(filename+'.txt')});

});

function PostCode(codestring) {
	
  //must first save the .img file to the correct path(will be denoted later)
  //direction contains results string for that waveform ie: left,right,left, (left)
  direction = 'left';
  var post_data = querystring.stringify({
      'direction' : direction//
  });

  // An object of options to indicate where to post to
  var post_options = {
      host: 'localhost',
      port: '5000',
      path: '/predict/',
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Content-Length': Buffer.byteLength(post_data)
      }
  };

  // Set up the request
  var post_req = http.request(post_options, function(res) {
      res.setEncoding('utf8');
      res.on('data', function (chunk) {
          console.log('Response: ' + chunk);
      });
  });

  // post the data
  post_req.write(post_data);
  post_req.end();

}

//in Python...
//import requests
//input username
//r = requests.post('http://localhost:5000/predict/send_waveform', data = {'prediction':'prediction','username':'nigel'})

//server.listen(3000, '172.20.10.3');
server.listen(3000, '10.0.0.171');
PostCode('something');


