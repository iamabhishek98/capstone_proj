const http = require('http');
const WebSocket = require('ws');
const app = require('./app');
const {onMessage} = require('./socket/input');

const server = http.createServer(app);
const wss = new WebSocket.Server({server});

wss.on('connection', (ws) => {
    ws.on('message', onMessage);

    // ws.send('[From Server] Lets talk!');
    console.log(`Number of clients connected: ${wss.clients.size}`);
});

module.exports = {wss, server};
