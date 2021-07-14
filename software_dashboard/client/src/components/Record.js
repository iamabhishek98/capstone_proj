import React from 'react';

import sidePumpImage from '../img/sidepump.png';
import gunImage from '../img/gun.png';
import hairImage from '../img/hair.png';
import dabImage from '../img/dab.png';
import elbowKickImage from '../img/elbowkick.png';
import listenImage from '../img/listen.png';
import pointHighImage from '../img/pointhigh.png';
import wipeTableImage from '../img/wipetable.png';
import logoutImage from '../img/logout.png';
import idleImage from '../img/idle.png';

import LinePlot from "./LinePlot";

class Record extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            expanded: false,
            withGroundTruth: false,
            text: "",
            submitted: false
        }
    }

    handleChange = (event) => {
        this.setState({
            text: event.target.value
        });
    }

    moveImages = {
        gun: gunImage,
        hair: hairImage,
        sidepump: sidePumpImage,
        idle: idleImage,
        dab: dabImage,
        elbowkick: elbowKickImage,
        listen: listenImage,
        pointhigh: pointHighImage,
        wipetable: wipeTableImage,
        logout: logoutImage
    }

    sync_opt = {
        // title: "Delay (ms)",
        width: 1060,
        height: 150,
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

    // This segment is for week 11 offline analytics demo.
    render() {
        let results;
        let result_style = "card-title font-weight-bold fs-4 text-center";
        if (this.state.submitted) {
            results = (
                <div>
                    <div className={result_style}> <label className="text-success">sidepump</label> <label className="text-success">2 1 3</label> </div>
                </div>
            )
        } else {
            results = (
                <div>
                    <div className={result_style}> sidepump 2 1 3 </div>
                </div>
            )
        }

        return (
            <div className="container-fluid mx-5">
                <h1 className="text-light fs-1"> Summary </h1>
                <div className="row mb-5">
                    <div className="col-4">
                        <div className="card bg-gradient mb-3 shadow" style={{backgroundColor: "#f76c6c", borderRadius: "20px 20px", height: "110px", width: "287px"}} >
                            <div className="card-body p-1">
                                <div className="row">
                                    <div className="col-6 text-center pt-0">
                                        <i className="bi-people-fill" style={{fontSize: "2.5rem", color: "white"}}/>
                                        <h6 className="card-title text-center text-light">Participants</h6>
                                    </div>
                                    <div className="col-6">
                                        <p className="card-text text-center text-light fw-bold fs-1 mt-3">
                                            3
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-4">
                        <div className="card bg-gradient mb-3 shadow" style={{backgroundColor: "#f76c6c", borderRadius: "20px 20px", height: "110px", width: "287px"}} >
                            <div className="card-body p-1">
                                <div className="row">
                                    <div className="col-6 text-center pt-0">
                                        <i className="bi-lightning-charge-fill" style={{fontSize: "2.5rem", color: "white"}}/>
                                        <h6 className="card-title text-center text-light">Hardest Muscle Fatigue</h6>
                                    </div>
                                    <div className="col-6">
                                        <p className="card-text text-center text-light fw-bold fs-3 mt-4">
                                            Medium &nbsp;
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-4">
                        <div className="card bg-gradient mb-3 shadow" style={{backgroundColor: "#f76c6c", borderRadius: "20px 20px", height: "110px", width: "287px"}} >
                            <div className="card-body p-1">
                                <div className="row">
                                    <div className="col-6 text-center pt-0">
                                        <i className="bi-arrows-move" style={{fontSize: "2.5rem", color: "white"}}/>
                                        <h6 className="card-title text-center text-light">Number of Moves</h6>
                                    </div>
                                    <div className="col-6">
                                        <p className="card-text text-center text-light fw-bold fs-3 mt-4">
                                            25 &nbsp;
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <h1 className="text-light fs-1 mt-5"> Check Accuracy </h1>
                <div className="row">
                    <div className="col-2"/>
                    <div className="col-4">
                        <label className="text-light mb-2 fs-3" htmlFor="exampleFormControlTextarea1">Predictions</label>
                        <div className="card bg-gradient bg-light mb-3 shadow" style={{borderRadius: "20px 20px", height: "1100px", width: "350px"}} >
                            {results}
                        </div>
                    </div>
                    <div className="col-4">
                        <form>
                            <div className="form-group">
                                <label className="text-light mb-2 fs-3" htmlFor="exampleFormControlTextarea1">Enter Ground Truth:</label>
                                <textarea className="form-control bg-light shadow" id="exampleFormControlTextarea1" rows="27"
                                          style={{borderRadius: "20px 20px"}}
                                          onChange={this.handleChange}>
                             </textarea>
                            </div>
                        </form>

                        <button className="btn btn-primary btn-lg mt-3"
                                onClick={() => this.setState({submitted: true})}>Submit</button>

                        {(this.state.submitted) ?
                            <div>
                                <div className="text-light fs-4 mt-4">
                                    <img src={this.moveImages.elbowkick} alt="Brand Icon" width="36" height="36" className=" rounded-circle shadow"/>&nbsp;
                                    Dance Move Accuracy: <label className="fs-1 text-white fw-bolder">96.0%</label>
                                </div>
                                <div className="text-light fs-4 mt-4">
                                    <i className="bi-arrows-move" style={{fontSize: "2rem", color: "white"}}/>
                                    &nbsp;Position Accuracy: <div className="fs-1 text-white fw-bolder">88.0%</div>
                                </div>
                            </div>: <div/>
                        }

                    </div>
                    <div className="col-2"/>
                </div>

                <h1 className="text-light fs-1 mt-5"> Dancer Analytics </h1>
                <div className="row">
                    <div className="col-4 px-0">
                        <div className="card bg-gradient bg-light mb-3 shadow" style={{borderRadius: "20px 20px", height: "430px", width: "350px"}} >
                            <div className="card-title fs-4 text-center"> Dancer <span className="fs-2 fw-bold">1</span> </div>
                            <div className="card-body p-3">
                                <div className="row">
                                    <div className="col-6 text-center">
                                        <img src={this.moveImages.dab} alt="Brand Icon" width="100" height="100" className="align-top rounded-circle shadow"/>
                                        <p className="fs-4">{"dab".toUpperCase()}</p>
                                        <label className="fs-6 font-weight-bold text-success">Most Sync Move</label>
                                    </div>
                                    <div className="col-6 text-center">
                                        <img src={this.moveImages.elbowkick} alt="Brand Icon" width="100" height="100" className="align-top rounded-circle shadow"/>
                                        <p className="fs-4">{"elbowkick".toUpperCase()}</p>
                                        <label className="fs-6 font-weight-bold text-danger">Least Sync Move</label>
                                    </div>
                                </div>
                                <div className="text-center fs-6 mt-4">
                                    <label className="fs-6 font-weight-bold">Dance Move Accuracy:</label>
                                    {(this.state.submitted) ? <label className="fs-3 fw-bolder text-success">&nbsp; 96.0%</label> :
                                        <label> &nbsp; -- </label>
                                    }
                                </div>
                                <div className="text-center mt-4">
                                    <i className="bi-alarm-fill" style={{fontSize: "1.3rem"}}/>&nbsp;
                                    <label className="fs-6 font-weight-bold">Average Delay:</label>
                                    <label className="fs-4 fw-bold text-warning">&nbsp; 908 ms</label>
                                </div>
                                <div className="text-center">
                                    <i className="bi-lightbulb-fill" style={{fontSize: "1.3rem", color: "#ffbb73"}}/>
                                    <label className="fs-6 font-weight-bold">
                                        &nbsp; Moves were delayed but acceptable.
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-4 px-0">
                        <div className="card bg-gradient bg-light mb-3 shadow" style={{borderRadius: "20px 20px", height: "430px", width: "350px"}} >
                            <div className="card-title fs-4 text-center"> Dancer <span className="fs-2 fw-bold">2</span> </div>
                            <div className="card-body p-3">
                                <div className="row">
                                    <div className="col-6 text-center">
                                        <img src={this.moveImages.sidepump} alt="Brand Icon" width="100" height="100" className="align-top rounded-circle shadow"/>
                                        <p className="fs-4">{"sidepump".toUpperCase()}</p>
                                        <label className="fs-6 font-weight-bold text-success">Most Sync Move</label>
                                    </div>
                                    <div className="col-6 text-center">
                                        <img src={this.moveImages.pointhigh} alt="Brand Icon" width="100" height="100" className="align-top rounded-circle shadow"/>
                                        <p className="fs-4">{"pointhigh".toUpperCase()}</p>
                                        <label className="fs-6 font-weight-bold text-danger">Least Sync Move</label>
                                    </div>
                                </div>
                                <div className="text-center fs-6 mt-4">
                                    <label className="fs-6 font-weight-bold">Dance Move Accuracy:</label>
                                    {(this.state.submitted) ? <label className="fs-3 fw-bolder text-success">&nbsp; 96.0%</label> :
                                        <label> &nbsp; -- </label>
                                    }
                                </div>
                                <div className="text-center mt-4">
                                    <i className="bi-alarm-fill" style={{fontSize: "1.3rem"}}/>&nbsp;
                                    <label className="fs-6 font-weight-bold">Average Delay:</label>
                                    <label className="fs-4 fw-bold text-success">&nbsp; 308 ms</label>
                                </div>
                                <div className="text-center">
                                    <i className="bi-lightbulb-fill" style={{fontSize: "1.3rem", color: "#ffbb73"}}/>
                                    <label className="fs-6 font-weight-bold">
                                        &nbsp; Your moves were on time. Good Job!
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-4 px-0">
                        <div className="card bg-gradient bg-light mb-3 ms-0 shadow" style={{borderRadius: "20px 20px", height: "430px", width: "350px"}} >
                            <div className="card-title fs-4 text-center"> Dancer <span className="fs-2 fw-bold">3</span> </div>
                            <div className="card-body p-3">
                                <div className="row">
                                    <div className="col-6 text-center">
                                        <img src={this.moveImages.gun} alt="Brand Icon" width="100" height="100" className="align-top rounded-circle shadow"/>
                                        <p className="fs-4">{"gun".toUpperCase()}</p>
                                        <label className="fs-6 font-weight-bold text-success">Most Sync Move</label>
                                    </div>
                                    <div className="col-6 text-center">
                                        <img src={this.moveImages.wipetable} alt="Brand Icon" width="100" height="100" className="align-top rounded-circle shadow"/>
                                        <p className="fs-4">{"wipetable".toUpperCase()}</p>
                                        <label className="fs-6 font-weight-bold text-danger">Least Sync Move</label>
                                    </div>
                                </div>
                                <div className="text-center fs-6 mt-4">
                                    <label className="fs-6 font-weight-bold">Dance Move Accuracy:</label>
                                    {(this.state.submitted) ? <label className="fs-3 fw-bolder text-success">&nbsp; 96.0%</label> :
                                        <label> &nbsp; -- </label>
                                    }
                                </div>
                                <div className="text-center mt-4">
                                    <i className="bi-alarm-fill" style={{fontSize: "1.3rem"}}/>&nbsp;
                                    <label className="fs-6 font-weight-bold">Average Delay:</label>
                                    <label className="fs-4 fw-bold text-danger">&nbsp; 1655 ms</label>
                                </div>
                                <div className="text-center">
                                    <i className="bi-lightbulb-fill" style={{fontSize: "1.3rem", color: "#ffbb73"}}/>
                                    <label className="fs-6 font-weight-bold">
                                        &nbsp; Practice more and stay focused!
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <h1 className="text-light fs-1 mt-5"> Synchronization </h1>
                <div className="row mb-5">
                    <div className="card bg-gradient mb-3 shadow ms-3" style={{backgroundColor: "#f76c6c", borderRadius: "20px 20px", height: "360px", width: "1130px"}} >
                        <div className="card-body">
                            <p className="card-text text-light fw-bold fs-4 m-0">
                                Average Dance Move Delay: <label className="fs-2">923</label> ms
                            </p>
                            <div className="mb-3" style={{borderRadius: "20px 20px"}}>
                                {/*<LinePlot options={this.sync_opt} data={maximum_delay}/>*/}
                                <LinePlot options={this.sync_opt} data={[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],[2876, 972, 2360, 1645, 3587, 980, 6605, 4756, 109, 2000, 6435, 990, 872, 1768, 3544, 3421, 1509, 2010, 4531, 3422, 1234, 1365, 1987, 2908, 3217]]}/>
                            </div>
                            <div className="card-text text-light fs-6 m-0">
                                <i className="bi-lightbulb-fill" style={{fontSize: "1.5rem", color: "white"}}/>
                                &nbsp; Pay attention to synchronization when changing positions.
                            </div>
                            <div className="card-text text-light fs-6 m-0">
                                <i className="bi-lightbulb-fill" style={{fontSize: "1.5rem", color: "white"}}/>
                                &nbsp; Synchronization is generally acceptable.
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        );
    }
}

export default Record;