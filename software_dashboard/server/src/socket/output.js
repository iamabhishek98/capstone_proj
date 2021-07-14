const {wss} = require('../server');

const sendToClients = (data) => {
    wss.clients.forEach(client => {
        client.send(data);
    });
};

module.exports = {sendToClients};