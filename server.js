var express = require('express');
var app = express();
const bodyparser = require('body-parser')
const axios = require('axios');
app.use(express.json());

app.use(bodyparser.urlencoded());
app.set('view engine', 'ejs');

app.get('/', function(req, res) {
    res.render("frontend/pages/index.ejs", {});
    
});


app.post('/process_login', function(req, res){
        var user = req.body.username;
        var password = req.body.password;
    
        if(user === 'admin' && password === 'password')
        {
            res.render('pages/overview.ejs', {
                auth: true
            });
        }
        else
        {
            res.render('pages/welcome.ejs', {
                auth: false
            });
        }
      })

app.get('/flights', function(req, res){
    var url ='http://127.0.0.1:5000/api/flights'
    axios.get(url)
    .then((response)=>{
        let flightData = response.data;
        let length = flightData.length
        res.render('pages/overview.ejs', {
            flight:flightData,
            length: length
        });
          
          
    });
})

app.get('/planes', function(req, res){
    var url ='http://127.0.0.1:5000/api/planes'
    axios.get(url)
    .then((response)=>{
        let planeData = response.data;
        let length = planeData.length
        res.render('pages/planes.ejs', {
            plane: planeData,
            length: length
        });
          
          
    });
});

app.get('/airports', function(req, res){
    var url ='http://127.0.0.1:5000/api/airports'
    axios.get(url)
    .then((response)=>{
        let airportData = response.data;
        let length = airportData.length
        res.render('pages/airport.ejs', {
            airport: airportData,
            length: length
        });
          
          
    });
});


app.post("/planes" , function(req, res){
    var year = req.body.year;
    var make = req.body.make;
    var model = req.body.model;
    var country = req.body.country;
    console.log(req.body.year)
    axios.post('http://127.0.0.1:5000/api/planes',{make,model,year,country})
        .then((response)=>{            
            res.render('pages/test.ejs',{body: req.body});
            
    });
    
});

app.post("/planes" , function(req, res){
    var year = req.body.code;
    var make = req.body.name;
    var country = req.body.country;
    console.log(req.body.year)
    axios.post('http://127.0.0.1:5000/api/planes',{make,model,year,country})
        .then((response)=>{            
            res.render('pages/test.ejs',{body: req.body});
            
    });
    
});





app.listen(8080);
console.log('8080 is the magic port');
