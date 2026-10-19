def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "lead-ingestion"}


def test_create_lead_success_and_sanitization(client):
    payload = {
        "full_name": "  kavita sharma  ",
        "email": "KAVITA@VENTURES.CO",
        "budget_inr": "₹1,25,000",
        "phone": "+91 987-654-3210",
    }
    response = client.post("/leads", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["full_name"] == "Kavita Sharma"  # Capitalized
    assert data["email"] == "kavita@ventures.co"  # Lowercased
    assert data["budget_inr"] == 125000  # Sanitized integer
    assert data["phone"] == "9876543210"  # Normalized 10 digits


def test_create_lead_validation_failure(client):
    invalid_payload = {
        "full_name": "Test User",
        "email": "invalid-email-no-at-symbol",
        "budget_inr": -500,
        "phone": "123",
    }
    response = client.post("/leads", json=invalid_payload)
    assert response.status_code == 422


def test_get_lead_not_found(client):
    response = client.get("/leads/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Lead with ID 999 not found"


def test_update_lead_partial(client):
    # 1. Create initial record
    create_res = client.post(
        "/leads",
        json={
            "full_name": "Rohan Das",
            "email": "rohan@test.com",
            "budget_inr": 50000,
            "phone": "9876543210",
        },
    )
    lead_id = create_res.json()["id"]

    # 2. Update only the budget
    update_res = client.patch(f"/leads/{lead_id}", json={"budget_inr": "₹75,000"})
    assert update_res.status_code == 200
    assert update_res.json()["budget_inr"] == 75000
    assert update_res.json()["full_name"] == "Rohan Das"


def test_delete_lead(client):
    # 1. Create lead
    create_res = client.post(
        "/leads",
        json={
            "full_name": "Delete Me",
            "email": "delete@test.com",
            "budget_inr": 20000,
            "phone": "9998887776",
        },
    )
    lead_id = create_res.json()["id"]

    # 2. Delete lead
    delete_res = client.delete(f"/leads/{lead_id}")
    assert delete_res.status_code == 204
    assert delete_res.text == ""

    # 3. Verify it is gone
    get_res = client.get(f"/leads/{lead_id}")
    assert get_res.status_code == 404


def test_pagination_and_filtering(client):
    # Seed 3 records
    client.post(
        "/leads",
        json={
            "full_name": "User Low",
            "email": "low@a.com",
            "budget_inr": 10000,
            "phone": "1111111111",
        },
    )
    client.post(
        "/leads",
        json={
            "full_name": "User Mid",
            "email": "mid@b.com",
            "budget_inr": 50000,
            "phone": "2222222222",
        },
    )
    client.post(
        "/leads",
        json={
            "full_name": "User High",
            "email": "high@c.com",
            "budget_inr": 100000,
            "phone": "3333333333",
        },
    )

    # Test min_budget filter
    res = client.get("/leads?min_budget=40000")
    assert res.status_code == 200
    data = res.json()
    assert data["total_count"] == 2
    assert len(data["data"]) == 2

    # Test limit pagination
    res_paginated = client.get("/leads?limit=1")
    assert res_paginated.status_code == 200
    assert len(res_paginated.json()["data"]) == 1
    assert res_paginated.json()["data"][0]["budget_inr"] == 100000
