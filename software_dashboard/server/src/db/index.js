const {Client} = require('pg');
const processDBNotification = require('./processor')

const notification_channel = 'streaming_data';

const db = new Client({
    user: 'postgres',
    host: 'localhost',
    database: 'cg4002',
    password: 'cg4002',
    port: 5433,
});

db.connect();
db.query(`listen ${notification_channel}`);
db.on('notification', processDBNotification);

module.exports = db;
