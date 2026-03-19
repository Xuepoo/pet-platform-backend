import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_application_flow():
    # 1. Login
    print("Logging in...")
    data = urllib.parse.urlencode({
        "username": "miko@example.com",
        "password": "TestPass123!"
    }).encode()
    
    req = urllib.request.Request(f"{BASE_URL}/auth/login", data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as f:
            resp = json.loads(f.read().decode())
            token = resp["access_token"]
            print("Login successful.")
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # 2. Get Pets
    print("Fetching pets...")
    req = urllib.request.Request(f"{BASE_URL}/pets/")
    with urllib.request.urlopen(req) as f:
        pets = json.loads(f.read().decode())
    
    if not pets:
        print("No pets found!")
        sys.exit(1)
    
    target_pet = pets[0]
    print(f"Selected pet: {target_pet['name']} (ID: {target_pet['id']})")

    # 3. Create Application
    print("Creating application...")
    app_data = {
        "pet_id": target_pet['id'],
        "message": "I would love to adopt this pet! using urllib"
    }
    
    req = urllib.request.Request(
        f"{BASE_URL}/applications/", 
        data=json.dumps(app_data).encode(), 
        headers=headers, 
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as f:
            print(f"Application created: {f.getcode()}")
    except urllib.error.HTTPError as e:
        if e.code == 400: # Already exists
            print("Application likely already exists (400).")
        else:
            print(f"Failed to create application: {e}")
            print(e.read().decode())
            sys.exit(1)

    # 4. List Applications
    print("Listing applications...")
    req = urllib.request.Request(f"{BASE_URL}/applications/", headers=headers)
    try:
        with urllib.request.urlopen(req) as f:
            apps = json.loads(f.read().decode())
            print(f"Found {len(apps)} applications.")
            for app in apps:
                print(f"- App ID: {app['id']}, Pet ID: {app['pet_id']}, Status: {app['status']}")
            
            if len(apps) > 0:
                print("SUCCESS: Applications flow working.")
            else:
                print("FAILURE: Created application not found.")
    except urllib.error.HTTPError as e:
        print(f"Failed to list applications: {e}")
        print(e.read().decode())

if __name__ == "__main__":
    test_application_flow()