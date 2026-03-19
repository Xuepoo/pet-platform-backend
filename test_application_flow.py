import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_application_flow():
    # 1. Login as Miko
    print("Logging in...")
    login_resp = requests.post(f"{BASE_URL}/auth/login", data={
        "username": "miko@example.com",
        "password": "TestPass123!"
    })
    if login_resp.status_code != 200:
        print(f"Login failed: {login_resp.text}")
        sys.exit(1)
    
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Logged in successfully.")

    # 2. Get available pets
    print("Fetching pets...")
    pets_resp = requests.get(f"{BASE_URL}/pets/", headers=headers)
    pets = pets_resp.json()
    if not pets:
        print("No pets found!")
        sys.exit(1)
    
    target_pet = pets[0]
    print(f"Selected pet: {target_pet['name']} (ID: {target_pet['id']})")

    # 3. Create Application
    print("Creating application...")
    app_data = {
        "pet_id": target_pet['id'],
        "message": "I would love to adopt this pet! I have a big yard."
    }
    create_resp = requests.post(f"{BASE_URL}/applications/", json=app_data, headers=headers)
    
    if create_resp.status_code == 200:
        print("Application created successfully.")
    elif create_resp.status_code == 400 and "already exists" in create_resp.text:
        print("Application already exists (expected if run multiple times).")
    else:
        print(f"Failed to create application: {create_resp.status_code} {create_resp.text}")
        sys.exit(1)

    # 4. List Applications
    print("Listing applications...")
    list_resp = requests.get(f"{BASE_URL}/applications/", headers=headers)
    apps = list_resp.json()
    print(f"Found {len(apps)} applications.")
    for app in apps:
        print(f"- App ID: {app['id']}, Pet ID: {app['pet_id']}, Status: {app['status']}, Message: {app['message']}")

    if len(apps) > 0:
        print("SUCCESS: Applications are showing up.")
    else:
        print("FAILURE: Application created but not showing in list.")

if __name__ == "__main__":
    test_application_flow()