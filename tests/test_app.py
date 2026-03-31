def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success_adds_participant(client):
    test_email = "test_student@mergington.edu"
    activity = "Chess Club"

    # Arrange
    starting_count = len(client.get("/activities").json()[activity]["participants"])

    # Act
    response = client.post(f"/activities/{activity}/signup?email={test_email}")

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    new_count = len(client.get("/activities").json()[activity]["participants"])
    assert new_count == starting_count + 1


def test_signup_duplicate_returns_400(client):
    test_email = "duplicate@mergington.edu"
    activity = "Programming Class"

    # Arrange
    client.post(f"/activities/{activity}/signup?email={test_email}")

    # Act again
    response = client.post(f"/activities/{activity}/signup?email={test_email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_invalid_activity_returns_404(client):
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404


def test_unregister_success_removes_participant(client):
    test_email = "remove_me@mergington.edu"
    activity = "Gym Class"

    client.post(f"/activities/{activity}/signup?email={test_email}")
    starting_count = len(client.get("/activities").json()[activity]["participants"])

    response = client.delete(f"/activities/{activity}/signup?email={test_email}")

    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    new_count = len(client.get("/activities").json()[activity]["participants"])
    assert new_count == starting_count - 1


def test_unregister_not_signed_up_returns_400(client):
    no_email = "not_there@mergington.edu"
    activity = "Basketball Team"

    response = client.delete(f"/activities/{activity}/signup?email={no_email}")

    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_invalid_activity_returns_404(client):
    response = client.delete("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404
