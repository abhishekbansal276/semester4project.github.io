const express = require('express');
const fs = require('fs');
const path = require('path');
const port = 8002;
const db = require('./config/mongoose');
const User = require('./models/users')

const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.urlencoded());

app.use(express.static('assets'));

app.get('/', function (req, res) {
    return res.render('home');
});

app.get('/signup', function (req, res) {
    return res.render('signup');
});

app.post('/create_user', async (req, res) => {
    let email = req.body.email;
    const userEmail = await User.findOne({ email: email });

    console.log(userEmail);

    if (userEmail == null) {
        User.create({
            email: req.body.email,
            password: req.body.password,
        }, function (err, newUser) {
            if (err) {
                console.log('error in creating user');
                return;
            }
            console.log('*********', newUser);
            return res.render('home');
        });
    }

    else {
        return res.send('Already registered with this email')
    }
});

app.post('/login', async (req, res) => {
    try {
        let email = req.body.email;
        let password = req.body.password;

        const userEmail = await User.findOne({ email: email });

        console.log(req.body);

        if (userEmail.password === password) {
            res.render('response');
        }
        else {
            res.send('Invalid login');
        }

    }
    catch (error) {
        alert('Invalid login');
    }
});

// app.post('/response', async function (req, res) {
//     if (req.body.response == 'yes' || req.body.response == 'Yes' || req.body.response == 'YES') {
//         const filter = {permission: 'NULL'};
//         const update = {permission: 'yes'};

//         let doc = await User.findOneAndUpdate(filter, update);
//         console.log(doc);
//         return res.send('Ok response taken');
//     }
    
//     if (req.body.response == 'no' || req.body.response == 'No' || req.body.response == 'NO') {
//         const filter = {permission: 'NULL'};
//         const update = {permission: 'no'};

//         let doc = await User.findOneAndUpdate(filter, update);
//         console.log(doc);
//         return res.send('Ok response taken');
//     }

//     else {
//         return res.send('Incorrect response');
//     }
// });

app.listen(port, function (err) {
    if (err) {
        console.log('error');
    }
    console.log('good and port is : ', port);
});