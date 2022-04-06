//Requitred library
const mongoose = require('mongoose');

//Connect to daatbase
mongoose.connect('mongodb://localhost/users_db');

//Acquire to check connection
const db = mongoose.connection;

//If error print error
db.on('error', console.error.bind(console, 'error connecting to db'));

//If working fine then print success
db.once('open', function(){
    console.log('Success in connecting with database');
})