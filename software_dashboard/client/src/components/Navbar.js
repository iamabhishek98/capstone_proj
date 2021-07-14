import React from 'react';
import logo from '../img/dancer.png';
import people_fill from '../img/people-fill.svg'

class Navbar extends React.Component {
    render() {
        const {switchPage, activePage} = this.props;

        let styles = {};
        ["DASHBOARD", "SENSORS", "RECORDS"].forEach((page) => {
            if (page === activePage) styles[page] = "nav-link text-light bg-transparent border-0 fw-bold";
            else styles[page] = "nav-link text-light bg-transparent border-0";
        });

        return (
            <div>
                <nav className="navbar navbar-expand-lg navbar-light mb-2">
                    <div className="container-fluid">
                        <a className="navbar-brand fw-bolder text-light" href="#">
                            <img src={logo} alt="Brand Icon" width="40" height="40" className="align-top"/>
                            <div className="d-inline-block">
                                <p className="m-0 lh-1 fs-5">&nbsp;DANCER</p>
                                <p className="m-0 lh-1 fs-5">&nbsp;DASHBOARD</p>
                            </div>
                        </a>
                        <ul className="navbar-nav">
                            <li className="nav-item">
                                <button className={styles.DASHBOARD} onClick={()=> switchPage('DASHBOARD')}>DASHBOARD</button>
                            </li>
                            <li className="nav-item">
                                <button className={styles.SENSORS} onClick={()=> switchPage('SENSORS')}>SENSORS</button>
                            </li>
                            <li className="nav-item">
                                <button className={styles.RECORDS} onClick={()=> switchPage('RECORDS')}>RECORDS</button>
                            </li>
                        </ul>

                        <div className="navbar-text text-light">
                            <img src={people_fill} alt="Brand Icon" width="25" height="25" className="align-top" />
                            &nbsp;CG4002 Group 13
                        </div>
                    </div>
                </nav>
                <hr className="bg-white"/>
            </div>

        );

        // return (
        //     <nav className="sb-topnav navbar navbar-expand navbar-dark bg-dark">
        //         <a className="navbar-brand" href="index.html">Dancer Dashboard</a>
        //         <button className="btn btn-link btn-sm order-1 order-lg-0" id="sidebarToggle" href="#"><i
        //             className="fas fa-bars"></i></button>
        //
        //         <form className="d-none d-md-inline-block form-inline ml-auto mr-0 mr-md-3 my-2 my-md-0">
        //             <div className="input-group">
        //                 <input className="form-control" type="text" placeholder="Search for..." aria-label="Search"
        //                        aria-describedby="basic-addon2"/>
        //                 <div className="input-group-append">
        //                     <button className="btn btn-primary" type="button"><i className="fas fa-search"></i>
        //                     </button>
        //                 </div>
        //             </div>
        //         </form>
        //
        //         <ul className="navbar-nav ml-auto ml-md-0">
        //             <li className="nav-item dropdown">
        //                 <a className="nav-link dropdown-toggle" id="userDropdown" href="#" role="button"
        //                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i
        //                     className="fas fa-user fa-fw"></i></a>
        //                 <div className="dropdown-menu dropdown-menu-right" aria-labelledby="userDropdown">
        //                     <a className="dropdown-item" href="#">Settings</a>
        //                     <a className="dropdown-item" href="#">Activity Log</a>
        //                     <div className="dropdown-divider"></div>
        //                     <a className="dropdown-item" href="login.html">Logout</a>
        //                 </div>
        //             </li>
        //         </ul>
        //     </nav>
        // );
    }
}

export default Navbar;