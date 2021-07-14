import React from "react";

import Dancer from "./Dancer";
import Profile from "./Profile"
import EMG from "./EMG"
import Synchronization from "./Synchronization";

class Dashboard extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            accelerations: {
                1: [[], [], [], []], // [time, x, y, z]
                2: [[], [], [], []],
                3: [[], [], [], []]
            },
            IMU: {
                1: [[], [], [], []], // [time, yaw, pitch, roll]
                2: [[], [], [], []],
                3: [[], [], [], []]
            },
            maximum_delay: [[], []],
            move: "idle",
            start_times: [0, 0, 0], // [user_1, user_2, user_3]
            positions: ["1", "2", "3"], // [right_slot, middle_slot, left_slot]
            EMG: [[], [], [], []], // [time, rms, zcs, mav]
            fatigue: "EASE",
        };
    }

    shouldComponentUpdate(nextProps, nextState, nextContext) {
        return false;
    }

    handleBeetleData = (record) => {
        const range = 200; // max 50 data points in a line chart.

        let {uid, time, yaw, pitch, roll, x, y, z} = record;
        let timestamps, xs, ys, zs, yaws, pitches, rolls;
        [timestamps, xs, ys, zs] = this.state.accelerations[uid];
        [timestamps, yaws, pitches, rolls] = this.state.IMU[uid];

        if (timestamps.length > range) {
            timestamps.shift();
            xs.shift();
            ys.shift();
            zs.shift();
            yaws.shift();
            pitches.shift();
            rolls.shift();
        }

        timestamps.push(time);
        xs.push(x);
        ys.push(y);
        zs.push(z);
        yaws.push(yaw);
        pitches.push(pitch);
        rolls.push(roll);

        let updated_accelerations = this.state.accelerations;
        let updated_IMU = this.state.IMU;
        updated_accelerations[uid] = [timestamps, xs, ys, zs];
        updated_IMU[uid] = [timestamps, yaws, pitches, rolls];
        this.setState({
            accelerations: updated_accelerations,
            IMU: updated_IMU
        });
    };

    handleEMGData = (record) => {
        // time    bigint,
        //     local_time timestamp default CURRENT_TIMESTAMP primary key,
        //     rms numeric not null,
        //     zcs numeric not null,
        //     mav numeric not null,
        let {time, rms, mav, zcs} = record;
        const range = 100; // max 50 data points in a line chart.

        let [timestamps, rms_line, mav_line, zcs_line] = this.state.EMG;
        if (timestamps.length > range) {
            timestamps.shift();
            rms_line.shift();
            mav_line.shift();
            zcs_line.shift();
        }

        timestamps.push(time);
        rms_line.push(rms);
        mav_line.push(mav);
        zcs_line.push(zcs);
        let updatedEMG = [timestamps, rms_line, mav_line, zcs_line];

        let segment = rms_line.slice(Math.max(rms_line.length - 10, 0), rms_line.length);
        let average = segment.reduce((a, b) => a + b, 0) / (segment.length + 0.01);
        const threshold_medium = 6000, threshold_high = 10000;

        let fatigue;
        if (average < threshold_medium) {
            fatigue = "EASE";
        } else if (average >= threshold_medium && average <= threshold_high) {
            fatigue = "MEDIUM";
        } else fatigue = "HIGH";

        this.setState({
            fatigue: fatigue,
            EMG: updatedEMG
        });
    }

    handleMoveData = (record) => {
        let {start_time, start_time_one, start_time_two, start_time_three, prediction} = record;
        let updated_maximum_delay = this.state.maximum_delay;
        updated_maximum_delay[1].push(Math.max(start_time_one, start_time_two, start_time_three) - Math.min(start_time_one, start_time_two, start_time_three));
        updated_maximum_delay[0].push(updated_maximum_delay[1].length);

        this.setState({
            move: prediction,
            start_times: [start_time_one, start_time_two, start_time_three],
            maximum_delay: updated_maximum_delay,
        });
    };

    handlePositionData = (record) => {
        let {start_time, left_slot, middle_slot, right_slot} = record;
        this.setState({
            positions: [left_slot, middle_slot, right_slot]
        });
    }

    handlers = { // table_name: handler.
        Beetle: this.handleBeetleData,
        EMG: this.handleEMGData,
        DanceMove: this.handleMoveData,
        DancePosition: this.handlePositionData
    }

    componentDidMount() {
        this.ws = new WebSocket('ws://127.0.0.1:8000');
        this.ws.onmessage = (message) => {
            let payload = JSON.parse(message.data);
            this.handlers[payload.table_name](payload.record);
        };

        this.refresingInterval = setInterval(() => {
            this.forceUpdate();
        }, 200);
    }

    componentWillUnmount() {
        clearInterval(this.refresingInterval);
        this.ws.close();
    }

    render() {
        let ranking = [1, 2, 3];
        ranking.sort((userA, userB) => this.state.start_times[userA-1] - this.state.start_times[userB-1]);

        if (this.props.mode === "dashboard") {
            return (
                <div className="container-fluid mx-5">
                    <div className="row">
                        <div className="col-7">
                            <div className="row">
                                <Synchronization maximum_delay={this.state.maximum_delay}/>
                            </div>
                            <div className="row">
                                <div className="col-7 ps-0">
                                    <div className="card bg-gradient mb-3 shadow ms-3" style={{backgroundColor: "#f76c6c", borderRadius: "20px 20px", height: "100px", width: "400px"}} >
                                        <div className="card-body p-1">
                                            <div className="row">
                                                <div className="col-5 text-center pt-0">
                                                    <i className="bi-person-dash-fill" style={{fontSize: "2.5rem", color: "white"}}/>
                                                    <i className="bi-person-dash-fill" style={{fontSize: "2.5rem", color: "white"}}/>
                                                    <i className="bi-person-fill" style={{fontSize: "2.5rem", color: "white"}}/>
                                                    <h6 className="card-title text-center text-light">POSITIONS</h6>
                                                </div>
                                                <div className="col-7">
                                                    <p className="card-text text-center text-light fw-bold fs-1 mt-3">
                                                        {this.state.positions[0]} &nbsp;&nbsp;&nbsp;&nbsp;
                                                        {this.state.positions[1]} &nbsp;&nbsp;&nbsp;&nbsp;
                                                        {this.state.positions[2]}
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="col-5 ps-0">
                                    <div className="card bg-gradient mb-3 shadow" style={{backgroundColor: "#f76c6c", borderRadius: "20px 20px", height: "100px", width: "287px"}} >
                                        <div className="card-body p-1">
                                            <div className="row">
                                                <div className="col-4 text-center pt-0">
                                                    <i className="bi-lightning-charge-fill" style={{fontSize: "2.5rem", color: "white"}}/>
                                                    <h6 className="card-title text-center text-light">FATIGUE</h6>
                                                </div>
                                                <div className="col-8">
                                                    <p className="card-text text-center text-light fw-bold fs-3 mt-3">
                                                        {this.state.fatigue} &nbsp;
                                                        {this.state.fatigue === "EASE" ?
                                                            <i className="bi-emoji-smile-fill" style={{fontSize: "2.5rem", color: "white"}}/>:
                                                            this.state.fatigue === "MEDIUM" ?
                                                                <i className="bi-emoji-neutral-fill" style={{fontSize: "2.5rem", color: "white"}}/>:
                                                                <i className="bi-emoji-frown-fill" style={{fontSize: "2.5rem", color: "white"}}/>
                                                        }
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="col-5">
                            <div className="row">
                                <div className="card bg-gradient mb-3 shadow" style={{backgroundColor: "#24305e", borderRadius: "20px 20px", height: "350px", width: "400px"}} >
                                    <div className="card-body">
                                        <h6 className="card-title text-center text-light">
                                            <i className="bi-bar-chart-steps" style={{fontSize: "1.5rem", color: "white"}}/>
                                            &nbsp;SPEED RANKING
                                        </h6>
                                        <p className="card-text">
                                            {
                                                ranking.map(value => {
                                                    return (
                                                        <div className="card bg-gradient mt-2 mb-3" style={{backgroundColor: "#f76c6c", borderRadius: "20px 20px", width: "340px", height: "70px"}}>
                                                            <div className="card-body pt-0">
                                                                <div className="row">
                                                                    <div className="col-5">
                                                                        <label className="fs-4 text-light mt-3">Dancer {value}</label>
                                                                    </div>
                                                                    <div className="col-2"/>
                                                                    <div className="col-5 text-center">
                                                                        <i className="bi-alarm-fill" style={{fontSize: "1.5rem", color: "white"}}/>
                                                                        <div className="fs-4 text-light">{this.state.start_times[value-1]}ms</div>
                                                                    </div>
                                                                </div>
                                                                {/*<label className="fs-4 text-light">Dancer {value}</label>*/}
                                                                {/*<label className="fs-4 text-light">{this.state.start_times[value-1]}ms</label>*/}
                                                            </div>
                                                        </div>
                                                    );
                                                })
                                            }
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <Profile userId={1} move={this.state.move} delay={this.state.start_times[0]} position={this.state.positions.indexOf("1")}/>
                    <Profile userId={2} move={this.state.move} delay={this.state.start_times[1]} position={this.state.positions.indexOf("2")}/>
                    <Profile userId={3} move={this.state.move} delay={this.state.start_times[2]} position={this.state.positions.indexOf("3")}/>
                </div>
            );

        } else if (this.props.mode === "sensors") {
            return (
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-3">
                            <div className="card bg-gradient mb-2 rounded-pill" style={{backgroundColor: "#f76c6c", height: "100px"}}>
                                <div className="card-body">
                                    <h6 className="card-title text-center text-light">POSITIONS</h6>
                                    <p className="card-text text-center text-light fw-bold fs-3">
                                        <div className="row">
                                            <div className="col-3"/>
                                            <label className="col-2">

                                                {this.state.positions[0]}
                                            </label>
                                            <label className="col-2">

                                                {this.state.positions[1]}
                                            </label>
                                            <label className="col-2">

                                                {this.state.positions[2]}
                                            </label>
                                            <div className="col-3"/>
                                        </div>
                                    </p>
                                </div>
                            </div>
                            <div className="card mb-2 rounded-pill" style={{backgroundColor: "#24305e", height: "100px"}}>
                                <div className="card-body">
                                    <h6 className="card-title text-center text-light">
                                        TIME DEVIATION (ms)
                                    </h6>
                                    <p className="card-text">
                                        <div className="row">
                                            <label className="fw-bold text-center text-light fs-3">
                                                {Math.max(...this.state.start_times) - Math.min(...this.state.start_times)}
                                            </label>
                                        </div>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div className="col-3">
                            <EMG data={this.state.EMG}/>
                        </div>
                        <div className="col-6">
                            <Dancer
                                userId={1}
                                acceleration={this.state.accelerations['1']}
                                IMU={this.state.IMU['1']}
                                move={this.state.move}
                            />
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-6">
                            <Dancer
                                userId={2}
                                acceleration={this.state.accelerations['2']}
                                IMU={this.state.IMU['2']}
                                move={this.state.move}
                            />
                        </div>
                        <div className="col-6">

                            <Dancer
                                userId={3}
                                acceleration={this.state.accelerations['3']}
                                IMU={this.state.IMU['3']}
                                move={this.state.move}
                            />
                        </div>
                    </div>
                </div>
            );
        }
    }
}

export default Dashboard;