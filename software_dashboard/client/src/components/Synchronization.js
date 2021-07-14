import React from 'react';
import LinePlot from "./LinePlot";

class Synchronization extends React.Component {
    sync_opt = {
        // title: "Delay (ms)",
        width: 660,
        height: 135,
        legend: {
            live: false, // removes the reading on cursors
            show: false,
            width: 2
        },
        series: [
            {},
            {
                label: "delay",
                stroke: "white",
                fill: "#f6abab",
                width: 2,
                scale: "SYNC"
            }
        ],
        axes: [
            {
                show: false
            },
        ],
        scales: {
            "SYNC": {
                auto: false,
                range: [0, 9000],
            }
        }
    };

    render() {
        let {maximum_delay} = this.props;
        let current_delay = (maximum_delay[1].length === 0) ? 0 : maximum_delay[1][maximum_delay[1].length - 1];

        return (
            <div className="card bg-gradient mb-3 shadow ms-3" style={{backgroundColor: "#f76c6c", borderRadius: "20px 20px", height: "235px", width: "700px"}} >
                <div className="card-body">
                    <h6 className="card-title text-center text-light">
                        <i className="bi-alarm-fill" style={{fontSize: "1.5rem", color: "white"}}/>
                        &nbsp; SYNCHRONIZATION
                    </h6>
                    <p className="card-text text-light fw-bold fs-4 m-0">
                        Current Dance Move Delay: {current_delay}ms
                    </p>
                    <div className="" style={{borderRadius: "20px 20px"}}>
                        <LinePlot options={this.sync_opt} data={maximum_delay}/>
                        {/*<LinePlot options={this.sync_opt} data={[[0,1,2,3,4,5],[90, 980, 321, 434, 256, 1008]]}/>*/}
                    </div>
                </div>
            </div>
        );
    }

}

export default Synchronization;