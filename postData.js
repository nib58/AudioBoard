// We need this to build our post string
var querystring = require('querystring');
var http = require('http');
var fs = require('fs');

function PostCode(codestring) {
	
  //must first save the .img file to the correct path(will be denoted later)
  //direction contains results string for that waveform ie: left,right,left, (left)
  
  var post_data = querystring.stringify({
      'direction' : direction
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
//import requests
// r = requests.post('http://localhost:5000/send_waveform/', data = {'prediction':'prediction','username':'nigel'})