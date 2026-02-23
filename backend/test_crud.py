import requests
import time

BASE_URL = "http://localhost:8001/api/projects"

def run_tests():
    # 1. Create a project
    print("--- Creating a project ---")
    create_payload = {
        "title": "Test Project",
        "description": "This is a test project",
        "tags": ["FastAPI", "MongoDB"]
    }
    create_res = requests.post(BASE_URL + "/", json=create_payload)
    print(f"Status: {create_res.status_code}")
    print(f"Response: {create_res.json()}")
    
    project_id = create_res.json().get("id")

    if project_id:
        # 2. Get all projects
        print("\n--- Getting all projects ---")
        get_all_res = requests.get(BASE_URL + "/")
        print(f"Status: {get_all_res.status_code}")
        print(f"Count: len={len(get_all_res.json())}")

        # 3. Get single project
        print(f"\n--- Getting single project ({project_id}) ---")
        get_single_res = requests.get(f"{BASE_URL}/{project_id}")
        print(f"Status: {get_single_res.status_code}")
        print(f"Response: {get_single_res.json()}")

        # 4. Update the project
        print("\n--- Updating the project ---")
        update_payload = {
            "title": "Updated Test Project",
            "description": "Updated description",
            "tags": ["Updated"]
        }
        update_res = requests.put(f"{BASE_URL}/{project_id}", json=update_payload)
        print(f"Status: {update_res.status_code}")
        print(f"Response: {update_res.json()}")

        # 5. Get single project to verify update
        print(f"\n--- Verify Update ---")
        get_single_res = requests.get(f"{BASE_URL}/{project_id}")
        print(f"Status: {get_single_res.status_code}")
        print(f"Title after update: {get_single_res.json().get('title')}")

        # 6. Delete the project
        print("\n--- Deleting the project ---")
        delete_res = requests.delete(f"{BASE_URL}/{project_id}")
        print(f"Status: {delete_res.status_code}")
        print(f"Response: {delete_res.json()}")

        # 7. Get single project to verify deletion
        print(f"\n--- Verify Deletion ---")
        get_deleted_res = requests.get(f"{BASE_URL}/{project_id}")
        print(f"Status: {get_deleted_res.status_code}")
        print(f"Response: {get_deleted_res.json()}")

if __name__ == "__main__":
    # Give server a second to start if running alongside
    time.sleep(1)
    try:
        run_tests()
    except Exception as e:
        print(f"Error connecting or running tests: {e}")
