const ws =io.connect('http://localhost:5000/login')

ws.on('connect', function() {
  console.log("Connection estalished");
  ws.emit('New user has connected!');
});

ws.on('message', function() {
  console.log("message estalished");
  ws.emit('New user has connected!');
});

var channel = "/chat";
        var socket = io.connect('http://' + document.domain + ':' + location.port + channel);
        socket.on('connect', function() {
            socket.emit('my_connection', {data: 'I\'m connected!'});
        });

        socket.on("message", function (message) {
            console.log('message'+message);
            refreshMessages(message);
        });
