import React from 'react';
import axios from 'axios';
import Record from './Record';
import LinePlot from "./LinePlot";

class Records extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            records: [], // element: {start_time, end_time}
            expanded: false
        };
    }

    componentDidMount() {
        axios.post("http://127.0.0.1:8000/executeSQL", {
            query: "select start_time, end_time from Session;"
        }).then(res => {
            this.setState({
                records: res.data.rows
            })
        }); // this 'data' has 'rows' attribute.
    }

    calender_opt = {
        // title: "Delay (ms)",
        width: 1100,
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
                scale: "CALENDER"
            }
        ],
        axes: [
            {
                show: false
            },
        ],
        scales: {
            "CALENDER": {
                auto: false,
                range: [0, 10],
            }
        }
    };

    render() {
        if (this.state.expanded) {
            return (
                <Record/>
            );
        } else {
            let cards = this.state.records.map((record, index) => {
                return <Record start_time={record.start_time} end_time={record.end_time} index={index+1}/>
            });

            return(
                <div className="container-fluid">
                    <div className="card bg-gradient mb-3 shadow ms-5" style={{backgroundColor: "#f76c6c", borderRadius: "20px 20px", height: "260px", width: "1150px"}} >
                        <div className="card-body">
                            <p className="card-text text-light fw-bold fs-4">
                                <i className="bi-alarm-fill" style={{fontSize: "1.5rem", color: "white"}}/>
                                &nbsp; Practice Records
                            </p>
                            <h6 className="text-light">
                                Number of dancing practices in recent days.
                            </h6>
                            <div className="" style={{borderRadius: "20px 20px"}}>
                                <LinePlot options={this.calender_opt} data={[[0,1,2,3,4,5,6],[1, 2, 5, 0, 1, 6, 10]]}/>
                            </div>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-3"/>
                        <div className="col-6">
                            <div className="card mb-3" style={{height: "100px", width: "600px", borderRadius:"20px 20px", backgroundColor: "#f76c6c"}}>
                                <div className="card-title fs-2 text-light mt-3 ms-2 text-center"
                                onClick={() => this.setState({expanded: true})}> Session 1</div>
                            </div>

                            <div className="card mb-3" style={{height: "100px", width: "600px", borderRadius:"20px 20px", backgroundColor: "#f76c6c"}}>
                                <div className="card-title fs-2 text-light mt-3 ms-2 text-center"
                                     onClick={() => this.setState({expanded: true})}> Session 2</div>
                            </div>
                        </div>
                        <div className="col-3"/>
                    </div>
                </div>
            );
        }
    }
}

export default Records;