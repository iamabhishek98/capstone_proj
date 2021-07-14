import React from "react";
import LinePlot from "./LinePlot";

class EMG extends React.Component {

    EMG_opts = {
        title: "EMG",
        width: 250,
        height: 180,
        legend: {
            live: false, // removes the reading on cursors
            width: 2
        },
        series: [
            {},
            {
                label: "RMS",
                stroke: "red",
                width: 1,
                value: (self, rawValue) => rawValue.toFixed(2),
            },
            {
                label: "ZCS",
                stroke: "green",
                width: 1,
                value: (self, rawValue) => rawValue.toFixed(2),
            },
            {
                label: "MAV",
                stroke: "blue",
                width: 1,
                value: (self, rawValue) => rawValue.toFixed(2),
            }
        ],
        axes: [
            {
                show: false
            },
        ]
    };

    render() {
        let {data} = this.props;
        let layer = data[1];
        let segment;
        if (layer.length >= 5) {
            segment = layer.slice(layer.length - 5, layer.length);
        } else segment = layer;
        let average = segment.reduce((a, b) => a + b, 0) / (segment.length + 0.01);
        const threshold_medium = 6000, threshold_high = 8000;

        let opacities = {
            Low: 0.2,
            Medium: 0.2,
            High: 0.2,
        };
        if (average < threshold_medium) {
            opacities.Low = 1;
        } else if (average >= threshold_medium && average <= threshold_high) {
            opacities.Medium = 1;
        } else opacities.High = 1;

        // opacities.Low = 1;
        // opacities.Medium = 0.2;
        // opacities.High = 0.2;

        return (
            <div className="card bg-light bg-gradient mb-3 shadow" >
                {/*<div className="card-header">Header</div>*/}
                <div className="card-body">
                    <h5 className="card-title"></h5>
                    <LinePlot options={this.EMG_opts} data={data} />

                    <div className="row">
                        <div className="col-4">
                            <div className="card-text rounded-pill bg-success text-center" style={{opacity: opacities.Low}}>
                                <label className="text-light">Low</label>
                            </div>
                        </div>
                        <div className="col-4">
                            <div className="card-text rounded-pill bg-warning text-center" style={{opacity: opacities.Medium}}>
                                <label className="text-light">Medium</label>
                            </div>
                        </div>
                        <div className="col-4">
                            <div className="card-text rounded-pill bg-danger text-center" style={{opacity: opacities.High}}>
                                <label className="text-light">High</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default EMG;