import React from "react";
import uPlot from "uplot";
import "../../node_modules/uplot/dist/uPlot.min.css";

class LinePlot extends React.Component {
    componentDidMount() {
        this.plot = new uPlot(this.props.options, this.props.data, this.el);
    }

    componentWillUnmount() {
        this.plot.destroy();
        this.plot = null;
    }

    render() {
        if (this.plot) this.plot.setData(this.props.data);
        return <div ref={el => (this.el = el)} />;
    }
}

export default LinePlot;
