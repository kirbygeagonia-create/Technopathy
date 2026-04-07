import requests
import json

# Test login
url = "http://127.0.0.1:8000/api/users/login/"
data = {
    "username": "safety_admin",
    "password": "TechnoPath@Safety2024!"
}

try:
    print(f"Testing login at {url}")
    response = requests.post(url, json=data, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")
except requests.exceptions.ConnectionError:
    print("ERROR: Cannot connect to server. Is Django running?")
    print("Run: python manage.py runserver")
except Exception as e:
    print(f"ERROR: {e}")
