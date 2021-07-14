# CG4002 Software Dashboard
## Setup
- Set up database.

In pg terminal, execute
 ```sql
CREATE DATABASE cg4002
\c cg4002
\i database/schema.sql
\i database/triggers.sql
```

- Set up node.js server
```
cd server
yarn install
yarn start
```
Server will start on http://localhost:8000.

- Set up react.js client
```
cd client
yarn install
yarn start
```
React server will start on http://localhost:3000.

- (Optional) Run simulated sample input. This is solely prepared for individual component test. Data format may be invalid after integration.
```
cd server/src/db
node data.js
```

## Troubleshooting
- Cannot connect to database

    * Check database connection settings in files under `server/src/db`
      , and align the settings with local postgre server settings.
    * Check postgresSQL server status with "pg_ctl status"
        * start server with "pg_ctl start"
