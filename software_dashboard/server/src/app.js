const express = require('express');
const cors = require('cors');
const db = require('./db/db');
const bodyParser = require('body-parser');

const app = express();

app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json())

app.get('/', (req, res) => {
    res.send("This is the root REST endpoint.");
});

app.post('/executeSQL', (req, res) => {

    console.log(req.body);
    // res.send("dummy");

    let query = req.body.query;

    db.query(query)
        .then(db_res => {
            res.send(db_res);
        });
});

module.exports = app;
