const {server} = require("./server")
const db = require("./db");
const port = 8000;

server.listen(port, () => {
    console.log(`The app is listening on port ${port}.`)
    console.log(`Address: http://127.0.0.1:${port}/`)
});


