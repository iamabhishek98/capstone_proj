import React from 'react';

class Footer extends React.Component {
    render() {
        return(
            <footer className="py-4 bg-light mt-auto">
                <div className="container-fluid">
                    <div className="d-flex align-items-center justify-content-between small">
                        <div className="text-muted">Copyright &copy; CG4002 Group 13 Dashboard</div>
                        <div>
                            <a href="#">Privacy Policy</a>
                            &middot;
                            <a href="#">Terms &amp; Conditions</a>
                        </div>
                    </div>
                </div>
            </footer>
        );
    }
}

export default Footer;