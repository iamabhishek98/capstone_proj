const {sendToClients} = require('../socket/output');

const processDBNotification = async (data) => {
    let payload = data.payload;
    sendToClients(payload);
    console.log(payload);
};

module.exports = processDBNotification;