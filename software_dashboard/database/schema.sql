drop table if exists Beetle, EMG, DanceMove, DancePosition, Session cascade;
drop type if exists uid_t, dance_move_t, activation_t;

create type uid_t as enum ('1', '2', '3');
create type dance_move_t as enum ('dab', 'elbowkick', 'listen', 'pointhigh', 'hair', 'gun', 'sidepump', 'wipetable', 'logout');
create type activation_t as enum ('0', '1', '2');

create table Beetle
(
    uid        uid_t,
    local_time timestamp default CURRENT_TIMESTAMP,
    time       bigint,
    yaw        numeric not null,
    pitch      numeric not null,
    roll       numeric not null,
    x          numeric not null,
    y          numeric not null,
    z          numeric not null,
    activation activation_t not null,
    primary key (uid, local_time)
);

create table EMG
(
    time       bigint,
    local_time timestamp default CURRENT_TIMESTAMP primary key,
    rms        numeric not null,
    mav        numeric not null,
    zcr        numeric not null
);

create table DanceMove
(
    local_time       timestamp default CURRENT_TIMESTAMP,
    start_time       bigint,
    start_time_one   integer,
    start_time_two   integer,
    start_time_three integer,
    prediction       dance_move_t not null,
    primary key (local_time)
);

create table DancePosition
(
    start_time  bigint,
    local_time  timestamp default CURRENT_TIMESTAMP primary key,
    left_slot   uid_t not null,
    middle_slot uid_t not null,
    right_slot  uid_t not null
);

create table Session
(
    start_time bigint,
    local_time timestamp default CURRENT_TIMESTAMP primary key,
    end_time   bigint default null
);

