# VerisAPI

## Flask Web Service API For Veris Community Database

#### Description:
The verisAPI Python(2.7) flask web application is a web service API interface to the Veris Community Database.  MongoDB is currently the only supported database for this web application.  MongoDB also must have user authentication enabled.  

##### Install MongoDB via homebrew
Install homebrew
```
install homebrew @ http://brew.sh/
```
Update homebrew
```
brew update
```
Install mongodb
```
brew install mongodb
```
Make Mongo Data Dir
```
mkdir -p /path/to/mongo/data/dir
```
Point Mongo To The Created data/dir
```
edit mongod.conf:

systemLog:
  destination: file
  path: /path/to/mongo/log/file.log
  logAppend: true
storage:
  dbPath: /path/to/mongo/data/dir
net:
  bindIp: 127.0.0.1
  port: 27017
security:
  authorization: enabled
```
Test Mongo Installation
```
mongo
exit
```

#### Create Required Mongo Database & Collections
```
mongo
use veris
db.createCollection("users")
db.createCollection("verisbase")
exit
```

Add Application User
```
mongo
use veris
db.createUser(
   {
     user: "appuser",
     pwd: "apppassword",
     roles:
       [
         { role: "readWrite", db: "veris" },
       ]
   }
)
```

#### VERISAPI Installation:
1. Update veris.app.conf with MongoDB connection details.
2. Update veris.app.conf with JSON_PATH variable (VCDB JSON Files)
 - Files Located @: https://github.com/vz-risk/VCDB/tree/master/data/json
3. sudo pip install -r requirements.txt
4. python run.py
5. Create user via /veris/register
6. Load Veris JSON via /veris/load

#### Veris API Setup
Create a VerisAPI user
```
$curl -d "username=alice&password=pwd" "http://127.0.0.1:8000/veris/register"
{ "Response" : "User Successfully Created." }
```

Example VerisAPI Call:
```
curl -u "username:password" "http://127.0.0.1:8000/veris/victims"
```

#### -- Veris API Endpoints --

- Web Root Returns 403 Forbidden.

http://127.0.0.1:8000/
- methods = GET
- Returns 403 Forbidden

- Registers A User For VerisAPI Authentication.

http://127.0.0.1:8000/veris/register
- methods = POST
- POST parameters = 'username','password'
```
$curl -d "username=alice&password=pwd" "http://127.0.0.1:8000/veris/register"
```

- Loads MongoDB with JSON VCDB files.

http://127.0.0.1:8000/veris/load
- methods = GET
```
$curl -u "username:password" "http://127.0.0.1:8000/veris/load"
```

- Returns JSON object of all Veris Incident IDs.

http://127.0.0.1:8000/veris/incidents
- methods = GET
```
$curl -u "username:password" "http://127.0.0.1:8000/veris/incidents"
```

- Return JSON object of Veris Incident by ID.

http://127.0.0.1:8000/veris/incident
- methods = POST
- POST parameters = 'incident'
```
$curl -u "username:password" -d "incident:XXXX-XXXX-XXXX-XXXX" "http://127.0.0.1:8000/veris/incident"
```

- Returns JSON object of Veris Victim Titles.

http://127.0.0.1:8000/veris/victims
- methods = GET
```
$curl -u "username:password" "http://127.0.0.1:8000/veris/victims"
```

- Returns JSON object of Veris Victim Incidents By Search.

http://127.0.0.1:8000/veris/victim
- methods = POST
- POST parameters = 'victim'
```
$curl -u "username:password" -d "victim:ACME Inc" "http://127.0.0.1:8000/veris/victim"
```

- Return All Victims by industry ID.

E-Commerce is industy ID: 454112
http://127.0.0.1:8000/veris/incident/industy
- methods = POST
- POST parameters = 'industry'
```
$curl -u "username:password" -d "industry:454112" "http://127.0.0.1:8000/veris/incident/industry"
```

- Returns Top Ten Recent Veris Record Create Dates.

http://127.0.0.1:8000/veris/newest
- methods = GET
```
$curl -u "username:password" "http://127.0.0.1:8000/veris/newest"
```

- Returns Distinct Threat Actions & count.

http://127.0.0.1:8000/veris/actions/count
- methods = GET
```
$curl -u "username:password" "http://127.0.0.1:8000/veris/action/count"
```

- Returns Distinct Threat Actions & count.

http://127.0.0.1:8000/veris/actions/types
- methods = GET
```
$curl -u "username:password" "http://127.0.0.1:8000/veris/action/types"
```

- Returns Distinct Victims By Geo Location.

http://127.0.0.1:8000/veris/victims/geo
- methods = GET
```
$curl -u "username:password" "http://127.0.0.1:8000/veris/victims/geo"
```
