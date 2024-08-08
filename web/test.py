import requests

url = 'http://180.119.171.109:5000/predict'
data = {'data': 'your input data'}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
