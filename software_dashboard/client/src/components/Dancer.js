import React from 'react';
import LinePlot from "./LinePlot";

class Dancer extends React.Component {

    acceleration_opt = {
        title: "Accel",
        width: 250,
        height: 180,
        legend: {
            live: false, // removes the reading on cursors
            width: 2
        },
        series: [
            {},
            {
                label: "AX",
                stroke: "red",
                width: 1,
                scale: "ACC"
            },
            {
                label: "AY",
                stroke: 'green',
                width: 1,
                scale: "ACC"
            },
            {
                label: "AZ",
                stroke:'blue',
                width: 1,
                scale: "ACC"
            }
        ],
        axes: [
            {
                show: false
            },
        ],
        scales: {
            "ACC": {
                auto: false,
                range: [-2, 2],
            }
        }
    };

    IMU_opt = {
        title: "Gyro",
        width: 250,
        height: 180,
        legend: {
            live: false, // removes the reading on cursors
            width: 2
        },
        series: [
            {},
            {
                label: "Yall",
                stroke: "red",
                width: 1,
                scale: "IMU"
            },
            {
                label: "Pitch",
                stroke: "green",
                width: 1,
                scale: "IMU"
            },
            {
                label: "Roll",
                stroke: "blue",
                width: 1,
                scale: "IMU"
            }
        ],
        axes: [
            {
                show: false
            },
        ],
        scales: {
            "IMU": {
                auto: false,
                range: [-450, 450],
            }
        }
    };

    render() {
        let {userId, acceleration, IMU, move} = this.props;

        return (
            <div className="card bg-gradient bg-light mb-3 shadow" >
                <div className="card-body p-3">
                    {/*<div className="row">*/}
                    {/*    <div className="card-title col-8">*/}
                    {/*        User {userId}*/}
                    {/*    </div>*/}
                    {/*    <div className="card-title col-4">*/}
                    {/*        Move: {move}*/}
                    {/*    </div>*/}
                    {/*</div>*/}
                    <div className="row">
                        <div className="col-1">
                            <label className="font-weight-bold fs-1">{userId}</label>
                        </div>
                        <div className="col-11">
                            <div className="row text-center">
                                <h5>Move: {move.toUpperCase()}</h5>
                            </div>
                            <div className="row">
                                <div className="col-6 p-0">
                                    <LinePlot options={this.acceleration_opt} data={acceleration}/>
                                </div>
                                <div className="col-6 p-0">
                                    <LinePlot options={this.IMU_opt} data={IMU}/>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Dancer;