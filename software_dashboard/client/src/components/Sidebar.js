import React from "react";


class Sidebar extends React.Component {
    render() {
        let {switchPage} = this.props;

        return(
            <nav className="sb-sidenav accordion sb-sidenav-dark" id="sidenavAccordion">
                <div className="sb-sidenav-menu">
                    <div className="nav">
                        <div className="sb-sidenav-menu-heading">Core</div>
                        <a className="nav-link bg-transparent border-0"
                                onClick={() => switchPage('dashboard')}>
                            <div className="sb-nav-link-icon"><i className="fas fa-tachometer-alt"></i>
                            </div>
                            Dashboard
                        </a>
                        {/*<div className="sb-sidenav-menu-heading">Interface</div>*/}
                        {/*<a className="nav-link collapsed" href="#" data-toggle="collapse"*/}
                        {/*   data-target="#collapseLayouts" aria-expanded="false"*/}
                        {/*   aria-controls="collapseLayouts">*/}
                        {/*    <div className="sb-nav-link-icon"><i className="fas fa-columns"></i></div>*/}
                        {/*    Layouts*/}
                        {/*    <div className="sb-sidenav-collapse-arrow"><i className="fas fa-angle-down"></i>*/}
                        {/*    </div>*/}
                        {/*</a>*/}
                        {/*<div className="collapse" id="collapseLayouts" aria-labelledby="headingOne"*/}
                        {/*     data-parent="#sidenavAccordion">*/}
                        {/*    <nav className="sb-sidenav-menu-nested nav">*/}
                        {/*        <a className="nav-link" href="layout-static.html">Static Navigation</a>*/}
                        {/*        <a className="nav-link" href="layout-sidenav-light.html">Light Sidenav</a>*/}
                        {/*    </nav>*/}
                        {/*</div>*/}
                        {/*<a className="nav-link collapsed" href="#" data-toggle="collapse"*/}
                        {/*   data-target="#collapsePages" aria-expanded="false" aria-controls="collapsePages">*/}
                        {/*    <div className="sb-nav-link-icon"><i className="fas fa-book-open"></i></div>*/}
                        {/*    Pages*/}
                        {/*    <div className="sb-sidenav-collapse-arrow"><i className="fas fa-angle-down"></i>*/}
                        {/*    </div>*/}
                        {/*</a>*/}
                        {/*<div className="collapse" id="collapsePages" aria-labelledby="headingTwo"*/}
                        {/*     data-parent="#sidenavAccordion">*/}
                        {/*    <nav className="sb-sidenav-menu-nested nav accordion"*/}
                        {/*         id="sidenavAccordionPages">*/}
                        {/*        <a className="nav-link collapsed" href="#" data-toggle="collapse"*/}
                        {/*           data-target="#pagesCollapseAuth" aria-expanded="false"*/}
                        {/*           aria-controls="pagesCollapseAuth">*/}
                        {/*            Authentication*/}
                        {/*            <div className="sb-sidenav-collapse-arrow"><i*/}
                        {/*                className="fas fa-angle-down"></i></div>*/}
                        {/*        </a>*/}
                        {/*        <div className="collapse" id="pagesCollapseAuth"*/}
                        {/*             aria-labelledby="headingOne" data-parent="#sidenavAccordionPages">*/}
                        {/*            <nav className="sb-sidenav-menu-nested nav">*/}
                        {/*                <a className="nav-link" href="login.html">Login</a>*/}
                        {/*                <a className="nav-link" href="register.html">Register</a>*/}
                        {/*                <a className="nav-link" href="password.html">Forgot Password</a>*/}
                        {/*            </nav>*/}
                        {/*        </div>*/}
                        {/*        <a className="nav-link collapsed" href="#" data-toggle="collapse"*/}
                        {/*           data-target="#pagesCollapseError" aria-expanded="false"*/}
                        {/*           aria-controls="pagesCollapseError">*/}
                        {/*            Error*/}
                        {/*            <div className="sb-sidenav-collapse-arrow"><i*/}
                        {/*                className="fas fa-angle-down"></i></div>*/}
                        {/*        </a>*/}
                        {/*        <div className="collapse" id="pagesCollapseError"*/}
                        {/*             aria-labelledby="headingOne" data-parent="#sidenavAccordionPages">*/}
                        {/*            <nav className="sb-sidenav-menu-nested nav">*/}
                        {/*                <a className="nav-link" href="401.html">401 Page</a>*/}
                        {/*                <a className="nav-link" href="404.html">404 Page</a>*/}
                        {/*                <a className="nav-link" href="500.html">500 Page</a>*/}
                        {/*            </nav>*/}
                        {/*        </div>*/}
                        {/*    </nav>*/}
                        {/*</div>*/}
                        <div className="sb-sidenav-menu-heading">Addons</div>
                        <a className="nav-link bg-transparent border-0"
                           onClick={() => switchPage('records')}>
                            <div className="sb-nav-link-icon"><i className="fas fa-tachometer-alt"></i>
                            </div>
                            Records
                        </a>
                        {/*<a className="nav-link" href="charts.html">*/}
                        {/*    <div className="sb-nav-link-icon"><i className="fas fa-chart-area"></i></div>*/}
                        {/*    Charts*/}
                        {/*</a>*/}
                        {/*<a className="nav-link" href="tables.html">*/}
                        {/*    <div className="sb-nav-link-icon"><i className="fas fa-table"></i></div>*/}
                        {/*    Tables*/}
                        {/*</a>*/}
                    </div>
                </div>
                <div className="sb-sidenav-footer">
                    <div className="small">Logged in as:</div>
                    Start Bootstrap
                </div>
            </nav>
        );
    }
}

export default Sidebar;