# Assignment-no.1 Design and implement an automated testing framework for a "User Management API", including test cases for core interfaces, execution scripts, and report generation. 
#Python tests

import pytest
from utils.api_client import APIClient

def test_create_user_minimum_fields(client, admin_token, user_payload):
    resp = client.post("/users", json=user_payload)
    assert resp.status_code in (200, 201)
    body = resp.json()
    assert "id" in body or "_id" in body
    assert body["email"] == user_payload["email"]

def test_get_user_by_id(client, admin_token, created_user):
    user_id = created_user.get("id") or created_user.get("_id")
    resp = client.get(f"/users/{user_id}")
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("email") == created_user["email"]

def test_list_users(client, admin_token):
    # simple smoke: list returns array and minimal paging
    resp = client.get("/users")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) or isinstance(data.get("items", []), list)

def test_update_user(client, admin_token, created_user):
    user_id = created_user.get("id") or created_user.get("_id")
    patch = {"first_name": "UpdatedName"}
    resp = client.patch(f"/users/{user_id}", json=patch)
    assert resp.status_code in (200, 204)
    # fetch and verify
    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    body = get_resp.json()
    assert body.get("first_name") == "UpdatedName"

def test_delete_user(client, admin_token, user_payload):
    # create first
    resp = client.post("/users", json=user_payload)
    assert resp.status_code in (200, 201)
    user = resp.json()
    user_id = user.get("id") or user.get("_id")
    # delete
    del_resp = client.delete(f"/users/{user_id}")
    assert del_resp.status_code in (200, 204)
    # verify not found
    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code in (404, 410)

# Negative tests
def test_create_user_without_email(client, admin_token, user_payload):
    payload = dict(user_payload)
    payload.pop("email")
    resp = client.post("/users", json=payload)
    assert resp.status_code == 400

def test_create_duplicate_user(client, admin_token, created_user):
    # attempt to create same email again
    payload = {
        "email": created_user["email"],
        "first_name": "Dup",
        "password": "P@ssw0rd123"
    }
    resp = client.post("/users", json=payload)
    # API should reject duplicates
    assert resp.status_code in (400, 409)

#TEST DESIGN
Positive tests: happy path create → get → update → delete.

Negative tests: missing required fields, duplicate creation, invalid IDs, unauthorized access.

Edge cases: extremely long strings, invalid email format, invalid JSON, concurrency tests (race conditions).

Data isolation: tests should create and clean up their own resources. Use a separate test tenant or DB if possible.

Idempotence: be cautious: delete tests should tolerate multiple delete attempts (200/204/404).

Assertions: check status code, response schema, critical fields, and side effects.

Contract tests: consider adding JSON Schema validation for responses.
