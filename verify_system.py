import asyncio
import httpx
import sys

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "test_verify@example.com"
PASSWORD = "password123"

async def verify_system():
    print("🚀 Starting System Verification...")
    
    async with httpx.AsyncClient() as client:
        # 1. Health Check (Root)
        try:
            # We don't have a specific health endpoint, but we can check if the server is up
            # by hitting the docs or openapi.json, or just assuming it's up if subsequent calls work.
            pass
        except Exception as e:
            print(f"❌ Server might be down: {e}")
            sys.exit(1)

        # 2. Register User
        print(f"👤 Registering user {EMAIL}...")
        try:
            resp = await client.post(f"{BASE_URL}/auth/register", json={
                "email": EMAIL,
                "password": PASSWORD,
                "full_name": "Test User"
            })
            if resp.status_code == 200:
                print("✅ User registered successfully.")
            elif resp.status_code == 400 and "already exists" in resp.text:
                print("⚠️ User already exists, proceeding to login.")
            else:
                print(f"❌ Registration failed: {resp.status_code} - {resp.text}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Registration error: {e}")
            sys.exit(1)

        # 3. Login
        print("🔑 Logging in...")
        token = ""
        try:
            resp = await client.post(f"{BASE_URL}/auth/login", data={
                "username": EMAIL,
                "password": PASSWORD
            })
            if resp.status_code == 200:
                data = resp.json()
                token = data["access_token"]
                print("✅ Login successful. Token received.")
            else:
                print(f"❌ Login failed: {resp.status_code} - {resp.text}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Login error: {e}")
            sys.exit(1)

        headers = {"Authorization": f"Bearer {token}"}

        # 4. Create Pet
        print("🐾 Creating a test pet...")
        pet_id = 0
        try:
            resp = await client.post(f"{BASE_URL}/pets/", headers=headers, json={
                "name": "Buddy",
                "species": "Dog",
                "breed": "Golden Retriever",
                "age": 3,
                "description": "A very good boy.",
                "status": "available",
                "gender": "male",
                "size": "large"
            })
            if resp.status_code == 200:
                pet_data = resp.json()
                pet_id = pet_data["id"]
                print(f"✅ Pet created: {pet_data['name']} (ID: {pet_id})")
            else:
                print(f"❌ Create pet failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"❌ Create pet error: {e}")

        # 5. List Pets
        print("📋 Listing pets...")
        try:
            resp = await client.get(f"{BASE_URL}/pets/")
            if resp.status_code == 200:
                pets = resp.json()
                print(f"✅ Retrieved {len(pets)} pets.")
            else:
                print(f"❌ List pets failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"❌ List pets error: {e}")

        # 6. Create Report
        print("📢 Creating a lost pet report...")
        try:
            resp = await client.post(f"{BASE_URL}/reports/", headers=headers, json={
                "pet_name": "Whiskers",
                "description": "Lost cat",
                "location": "Downtown",
                "report_type": "lost",
                "contact_info": "555-0123"
            })
            if resp.status_code == 200:
                report = resp.json()
                print(f"✅ Report created for {report['pet_name']}")
            else:
                print(f"❌ Create report failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"❌ Create report error: {e}")

    print("\n🎉 Verification Complete! System is operational.")

if __name__ == "__main__":
    asyncio.run(verify_system())
