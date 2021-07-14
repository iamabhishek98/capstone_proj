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

class Profile extends React.Component {

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

    render() {
        let {userId, delay, move, position} = this.props;

        const base = 137, increment = 282;
        let x = base + increment * (position - userId + 1);

        return (
            <div className="card bg-gradient bg-light mb-3 ms-3 shadow me-3 d-inline-block" style={{borderRadius: "20px 20px", height: "320px", width: "250px", transform: "translate3d(" + x + "px, 0, 0)", transition: "transform 1s"}} >
                <div className="card-title fs-4 text-center"> Dancer <span className="fs-2 fw-bold">{userId}</span> </div>
                <div className="card-body p-3">
                    <div className="text-center">
                        <img src={this.moveImages[move]} alt="Brand Icon" width="130" height="130" className="align-top rounded-circle shadow"/>
                        <p className="fs-3">{move.toUpperCase()}</p>
                        {delay === 0 ? <label className="fs-4 font-weight-bold mt-2 text-success">On Time!</label> : <label className="fs-4 mt-2 text-danger">Slower by {delay}ms</label>}
                    </div>
                </div>
            </div>
        );
    }
}

export default Profile;