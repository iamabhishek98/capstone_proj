import React from 'react';
import Navbar from "./Navbar";
import Dashboard from "./Dashboard";
import Footer from "./Footer";
import Records from "./Records";

class Layout extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            page: 'DASHBOARD'
        }
    }

    switchPage = (page) => {
        if (this.state.page === page) return;
        this.setState({
            page: page
        });
    }

    pageMap = {
        'DASHBOARD': <Dashboard mode="dashboard"/>,
        'SENSORS': <Dashboard mode="sensors"/>,
        'RECORDS': <Records/>
    }

    render() {
        return (
            <div className="" style={{backgroundColor: "#a8d0e6"}}>
                <Navbar switchPage={this.switchPage} activePage={this.state.page}/>
                <main>
                    { this.pageMap[this.state.page] }
                </main>
                <Footer/>
            </div>
        );
    }
}

export default Layout;