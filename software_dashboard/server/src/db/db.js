const {Client} = require('pg');

const db = new Client({
    user: 'postgres',
    host: 'localhost',
    database: 'cg4002',
    password: 'cg4002',
    port: 5433,
});

db.connect();

module.exports = db;