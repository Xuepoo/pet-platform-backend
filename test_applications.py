import requests

def test_my_applications():
    # 1. Login
    login_url = "http://localhost:8000/api/v1/login/access-token"
    login_data = {
        "username": "miko@example.com",
        "password": "TestPass123!"
    }
    response = requests.post(login_url, data=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.status_code} {response.text}")
        return

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get My Applications
    apps_url = "http://localhost:8000/api/v1/applications/my"
    response = requests.get(apps_url, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Applications:", response.json())
    else:
        print("Error:", response.text)

if __name__ == "__main__":
    test_my_applications()