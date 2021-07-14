const {Client} = require('pg');

const db = new Client({
    user: 'postgres',
    host: 'localhost',
    database: 'cg4002',
    password: 'cg4002',
    port: 5433,
});

db.connect();

const T = 10;
const unit_angle = 0.05;
const b1 = 0, b2 = 0.5, b3 = 1, b = 0.5;

// insert into Beetle(uid, yaw, pitch, roll, x, y, z) values ('2', 1.0, 1.0, 2.0, 3, 5, 6);
// insert into EMG(voltage) values (3.6);
// insert into DanceMove(uid, prediction) values ('1', 'elbow kick');
// insert into DancePosition(left_slot, middle_slot, right_slot) values ('3', '1', '2');

function insertBeetle(uid, yaw, pitch, roll, x, y, z) {
    db.query(`insert into Beetle(uid, yaw, pitch, roll, x, y, z) 
    values ('${uid}', ${yaw}, ${pitch}, ${roll}, ${x}, ${y}, ${z})`);
}

function insertEMG(voltage) {
    db.query(`insert into EMG(voltage) values (${voltage});`);
}

function insertDanceMove(uid, prediction) {
    db.query(`insert into DanceMove(uid, prediction) values ('${uid}', '${prediction}');`);
}

function insertDancePosition(left_slot, middle_slot, right_slot) {
    db.query(`insert into DancePosition(left_slot, middle_slot, right_slot) 
    values ('${left_slot}', '${middle_slot}', '${right_slot}');`);
}

let session_start_time;

function startSession() {
    session_start_time = Date.now();
    db.query(`insert into Session(start_time) values(to_timestamp(${session_start_time} / 1000.0));`);
}

function endSession() {
    db.query(`update Session set end_time = to_timestamp(${Date.now()} / 1000.0) where start_time = to_timestamp(${session_start_time} / 1000.0)`);
}

// ************ Debug session

// ************ The following simulate an entire session.

startSession();

let counter = 0, angle = 0;
let intervalID = setInterval(() => {
    console.log("JOJO!" + counter);
    insertBeetle('1', Math.sin(angle + b3) - b, Math.sin(angle + b3), Math.sin(angle + b3) + b, Math.cos(angle + b3) - b, Math.cos(angle + b3), Math.cos(angle + b3) + b);
    insertBeetle('2', Math.sin(angle + b1) - b, Math.sin(angle + b1), Math.sin(angle + b1) + b, Math.cos(angle + b1) - b, Math.cos(angle + b1), Math.cos(angle + b1) + b);
    insertBeetle('3', Math.sin(angle + b2) - b, Math.sin(angle + b2), Math.sin(angle + b2) + b, Math.cos(angle + b2) - b, Math.cos(angle + b2), Math.cos(angle + b2) + b);
    insertEMG(Math.cos(angle + b1));

    angle += unit_angle;
    counter ++;
    }, T);

let counter2 = 0;
const moves = ['dab', 'elbow kick', 'listen', 'point high', 'hair', 'gun', 'side pump', 'wipe table'];
const positions = [[1, 2, 3], [2, 3, 1], [3, 1, 2], [1, 3, 2], [1, 2, 3], [1, 3, 2], [2, 3, 1], [3, 1, 2]];
let intervalID2 = setInterval(() => {
    insertDanceMove('1', moves[counter2]);
    insertDanceMove('2', moves[counter2]);
    insertDanceMove('3', moves[counter2]);
    let position = positions[counter2];
    insertDancePosition(position[0], position[1], position[2]);
    counter2 = (counter2 + 1) % moves.length;
}, 3000);

setTimeout(() => {
    clearInterval(intervalID);
    clearInterval(intervalID2);
    insertDanceMove('1', 'completion');
    insertDanceMove('2', 'completion');
    insertDanceMove('3', 'completion');

    endSession();
}, 20000);