import React from 'react';
import axios from "axios";

class ExpandedRecord extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            predicted_moves: [],
            predicted_positions: [],
            true_moves:[],
            true_positions: []
        }
    }

    async componentDidMount() {
        let {start_time, end_time} = this.props;

        // to_timestamp(${Date.now()} / 1000.0)

        // let moveQuery = `select uid, prediction from DanceMove
        //                  where start_time >= '${start_time}'
        //                  and start_time <= '${end_time}'
        //                  order by start_time, uid`;
        let moveQuery = `select uid, prediction from DanceMove
                         order by start_time, uid`;

        // let positionQuery = `select left_slot, middle_slot, right_slot from DancePosition
        //                      where start_time >= '${start_time}'
        //                      and start_time <= '${end_time}'
        //                      order by start_time`;
        let positionQuery = `select left_slot, middle_slot, right_slot from DancePosition
                             order by start_time`;

        let predicted_moves = [], predicted_positions = [];

        let res = await axios.post("http://127.0.0.1:8000/executeSQL", {
            query: moveQuery
        });

        let rows = res.data.rows;
        let counter = 0, moves = []; // three's moves at nearly same time.
        rows.forEach(row => {
            if (counter === 0) {
                if (moves.length !== 0) predicted_moves.push(moves);
                moves = [];
            }
            moves.push(row.prediction);
            counter = (counter + 1) % 3;
        });

        res = await axios.post("http://127.0.0.1:8000/executeSQL", {
            query: positionQuery
        })
        predicted_positions = res.data.rows;

        console.log(predicted_moves);
        console.log(predicted_positions);

        this.setState({
            predicted_moves: predicted_moves,
            predicted_positions: predicted_positions
        });
    }

    render() {
        // <ul className="list-group">
        //     <li className="list-group-item">Dapibus ac facilisis in</li>
        //
        //
        //     <li className="list-group-item list-group-item-primary">A simple primary list group item</li>
        //     <li className="list-group-item list-group-item-secondary">A simple secondary list group item</li>
        //     <li className="list-group-item list-group-item-success">A simple success list group item</li>
        //     <li className="list-group-item list-group-item-danger">A simple danger list group item</li>
        //     <li className="list-group-item list-group-item-warning">A simple warning list group item</li>
        //     <li className="list-group-item list-group-item-info">A simple info list group item</li>
        //     <li className="list-group-item list-group-item-light">A simple light list group item</li>
        //     <li className="list-group-item list-group-item-dark">A simple dark list group item</li>
        // </ul>
        //

        let predicted_items = this.state.predicted_moves.map((moves, index) => {
            let positions = this.state.predicted_positions[index];
            console.log(moves);
            console.log(positions);
            return (
                <li className="list-group-item">
                    {positions.left_slot} {positions.middle_slot} {positions.right_slot} {moves[0]} {moves[1]} {moves[2]}
                </li>
            );
        })

        return (
            <div>
                <h3>Details</h3>
                <div className="row">
                    <div className="col">
                        <h3>Predictions</h3>
                        {predicted_items}
                    </div>
                    <div className="col">
                        <h3>Ground Truth</h3>
                        <h4>To be implemented</h4>
                    </div>
                </div>
            </div>
        );
    }
}

export default ExpandedRecord;