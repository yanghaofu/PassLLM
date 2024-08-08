import requests

url = 'http://127.0.0.1:6006/submit'
data = {
    'password': 123,
    'name': 'nam12e',
    'email': 'email',
    'phone': 'phone',
    'birthday': 'birthday'
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
