import flask
from flask import jsonify
from flask import request, make_response
from sql import create_connection
from sql import execute_read_query
from sql import execute_query
import creds



app = flask.Flask(__name__)
app.config["DEBUG"] = True
#credentails for the login API
masterPassword = "Password"
masterUsername = 'username'
#Login api
@app.route('/login', methods=['GET'])
def auth():
    if request.authorization:
        if request.authorization.username == masterUsername and request.authorization.password == masterPassword:
            return '<h1> WE ARE ALLOWED TO BE HERE </h1>'
    return make_response('COULD NOT VERIFY!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route('/', methods=['GET'])
def home():
    return "<h1> Test run </h1>"


#GET for the airport
@app.route('/api/airports' , methods = ['GET'])
def airports_get():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "SELECT * FROM airports"
    airports = execute_read_query(conn, sql)
    results = []
    for airport in airports:
        results.append(airport)
    return jsonify(results)

#POST for airports
@app.route('/api/airports', methods =['POST'])
def airports_post():
    post_list = []
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    request_data = request.get_json()
    newairportcode = request_data['airportcode']
    newairportname = request_data['airportname']
    newcounrty = request_data['country']
    post_list.append({'airportcode': newairportcode, 'airportname':newairportname, 'country':newcounrty})
    sql = "INSERT INTO airports (airportcode, airportname, country) VALUES ('{}','{}','{}');".format(newairportcode, newairportname, newcounrty)
    execute_query(conn, sql)
    return jsonify(post_list)

@app.route('/api/airports', methods = ['DELETE'])
def airports_delete():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    request_data = request.get_json()
    idToDelete = request_data['id']
    sql = 'DELETE FROM airports WHERE id = {}'.format(idToDelete)
    execute_query(conn, sql)
    return "Delete request successful"

@app.route('/api/airports', methods = ['PUT'])
def airports_put():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    request_data = request.get_json()
    idToUpdate = request_data['id']
    upairportcode = request_data['airportcode']
    upairportname = request_data['airportname']
    upcountry = request_data['country']
    sql = "UPDATE airports SET airportcode = '{}', airportname = '{}', country = '{}' WHERE id = {}".format(
        upairportcode, upairportname, upcountry, idToUpdate
    )
    execute_query(conn, sql)
    return "Update request successful"

@app.route('/api/planes', methods =['GET'])
def plane_get():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "SELECT * FROM planes"
    planes = execute_read_query(conn, sql)
    results = []
    for plane in planes:
        results.append(plane)
    return jsonify(results)

@app.route('/api/planes', methods =['POST'])
def plane_post():
    post_list = []
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    request_data = request.get_json()
    newmake = request_data['make']
    newmodel = request_data['model']
    newyear = request_data['year']
    newcounrty = request_data['country']
    post_list.append({'make': newmake, 'model':newmodel, 'year':newyear, 'counrty':newcounrty})
    sql = "INSERT INTO planes (make, model, year, country) VALUES ('{}','{}','{}','{}');".format(
        newmake, newmodel, newyear, newcounrty
    )
    execute_query(conn, sql)
    return "Success"

@app.route('/api/planes', methods =['DELETE'])
def plane_delete():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    request_data = request.get_json()
    idToDelete = request_data['id']
    sql = 'DELETE FROM planes WHERE id = {}'.format(idToDelete)
    execute_query(conn, sql)
    return "Delete request successful"

@app.route('/api/planes', methods =['PUT'])
def plane_put():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    request_data = request.get_json()
    idToUpdate = request_data['id']
    upmake = request_data['make']
    upmodel = request_data['model']
    upyear = request_data['year']
    upcountry = request_data['country']
    sql = "UPDATE planes SET make = '{}', model = '{}', year = '{}', country = '{}' WHERE id = {}".format(
        upmake, upmodel, upyear, upcountry, idToUpdate
    )
    execute_query(conn, sql)
    return "Update request successful"


#I used a normal GET API for this table, I alreday loaded the flights table with a foregin key constraint on the other ID's
#I tried a lot to join the tables but I counldn't get it work 
@app.route('/api/flights', methods =['GET'])
def flight_get():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "select * from flights"
    airports = execute_read_query(conn, sql)
    results = []
    for airport in airports:
        results.append(airport)
    return jsonify(results)


@app.route('/api/flights', methods = ['POST'])
def flight_post():
    post_list =[]
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    request_data = request.get_json()
    newplaneid = request_data['planeid']
    newairportfrom = request_data['airportfromid']
    newairportto = request_data['airporttoid']
    newdate = request_data['date']
    post_list.append({'planeid': newplaneid, 'airportfrom': newairportfrom, 'airportto':newairportto, 'date': newdate })
    sql = "INSERT INTO flights (planeid, airportfromid, airporttoid, date) VALUES ({},{},{},'{}');".format(
        newplaneid, newairportfrom, newairportto, newdate
    )
    execute_query(conn, sql)
    return jsonify(post_list)
    
@app.route('/api/flights', methods = ['DELETE'])
def flight_delete():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    request_data = request.get_json()
    idToDelete = request_data['id']
    sql = 'DELETE FROM flights WHERE id = {}'.format(idToDelete)
    execute_query(conn, sql)
    return "Delete request successful"



app.run()
