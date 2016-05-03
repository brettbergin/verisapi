# VerisAPI

http://127.0.0.1:8000/
- methods = GET
- Returns 403 Forbidden

### Registers A User For Basic Authentication
http://127.0.0.1:8000/register
- methods = POST
- POST parameters = 'username','password'
- Register username/password as POST parameters

### Loads MongoDB with JSON VCDB files.
http://127.0.0.1:8000/veris/load
- methods = GET
- Files Located Here: https://github.com/vz-risk/VCDB/tree/master/data/json

### Returns JSON object of all Veris Incident IDs
http://127.0.0.1:8000/veris/incidents
- methods = GET

### Return JSON object of Veris Incident by ID.
http://127.0.0.1:8000/veris/incident
- methods = POST
- POST parameters = 'incident'

### Return JSON object of Veris Victim Titles
http://127.0.0.1:8000/veris/victims
- methods = GET

### Retuns All Victims by industry ID.
#### E-Commerce is industy ID: 454111
http://127.0.0.1:8000/veris/industry
- methods = POST
- POST parameters = 'industry'

### Returns Top Ten Recent Veris Record Create Dates
http://127.0.0.1:8000/veris/newest
- methods = GET

### Returns Distinct Threat Actions & count
http://127.0.0.1:8000/veris/actions/count
- methods = GET
