import React from 'react';
import Layout from './components/Layout';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import '../node_modules/bootstrap-icons/font/bootstrap-icons.css';

class App extends React.Component {

    constructor(props) {
        super(props);

    }

    render() {
        return (
            <Layout/>
        );
    }
}

export default App;