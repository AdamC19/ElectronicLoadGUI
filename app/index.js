const express = require('express');
const { spawn } = require('node:child_process')
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

// PYTHON SCRIPT THINGS
var load_comms = spawn('python', ['repowered.py','/dev/ttyS1']);

load_comms.stdout.on('data', (data) => {
    try{
        var load_data = JSON.parse(data);
        io.emit('update', load_data);
    }catch(err){
        console.log(err);
    }
});

load_comms.stderr.on('data', (data) => {
    console.log(data);
});

// BEGIN BASIC SERVER STUFF
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.get('/style.css', (req, res) => {
    res.sendFile(__dirname + '/style.css');
});

app.get('/control_scripts.js', (req, res) => {
    res.sendFile(__dirname + '/control_scripts.js');
});

// SOCKET IO STUFF
io.on('connection', (socket) => {
    socket.on('configure', (config) => {
        var conf = config;
        console.log(conf);
        load_comms.stdin.write(JSON.stringify(conf) + "\n", "UTF8");
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});


server.listen(8080, () => {
    console.log('listening on *:8080');
});