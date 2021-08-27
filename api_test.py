import requests
import json

server = 'http://127.0.0.1:5000/api'

tests = 4
passed = 0

print("TEST 1: method GET")

r = requests.get(server)

if r.status_code != 200:
    print("FAIL - server did not respond")

r = r.json()
r = json.dumps(r)

try:
    json.loads(r)
except Exception:
    print("FAIL - not json data")
else:
    print("SUCCESS")
    passed += 1

print("-----------------------------")
print("TEST 2: method POST")

requests.post('http://127.0.0.1:5000/api',
              json={'name': 'Neil Tyson', 'cpf': '91817161514'})

r = requests.get(server)
r = r.json()
r = json.dumps(r)
r = json.loads(r)
x = r[len(r)-1]["name"]
if x != 'Neil Tyson':
    print("FAIL - could not include client")
else:
    print("SUCCESS")
    passed += 1

print("-----------------------------")
print("TEST 3: method PUT")

requests.put('http://127.0.0.1:5000/api',
             json={'cpf': '91817161514', 'status': 1})

r = requests.get(server)
r = r.json()
r = json.dumps(r)
r = json.loads(r)
x = r[len(r)-1]["status"]
if x != 'Aguardando transferência de recursos':
    print("FAIL - could not change client status")
else:
    print("SUCCESS")
    passed += 1

print("-----------------------------")
print("TEST 4: method DELETE")

requests.delete('http://127.0.0.1:5000/api', json={'cpf': '91817161514'})

r = requests.get(server)
r = r.json()
r = json.dumps(r)
r = json.loads(r)
x = r[len(r)-1]["name"]
if x == 'Neil Tyson':
    print("FAIL - could not delete client")
else:
    print("SUCCESS")
    passed += 1

print("\n")
txt = "Passed in {} out of {} tests."
txt = txt.format(passed, tests)
print(txt)
